"""UDP-to-HTTP preview relay for standalone OpenGoPro."""

from __future__ import annotations

import asyncio
import socket
import time
from collections import deque
from typing import Any


class PreviewSession:
    """Runtime state for one standalone preview stream."""

    def __init__(self, camera_id: str, port: int, transport: asyncio.DatagramTransport) -> None:
        self.camera_id = camera_id
        self.port = port
        self.transport = transport
        self.subscribers: set[asyncio.Queue[bytes | None]] = set()
        self.recent_datagrams: deque[bytes] = deque(maxlen=256)
        self.datagrams_received = 0
        self.bytes_received = 0
        self.last_datagram_at: float | None = None
        self.first_datagram = asyncio.Event()
        self.error: str | None = None


class PreviewDatagramProtocol(asyncio.DatagramProtocol):
    """Forward GoPro preview MPEG-TS UDP datagrams to HTTP subscribers."""

    def __init__(self, manager: "PreviewManager") -> None:
        self._manager = manager
        self.session: PreviewSession | None = None

    def datagram_received(self, data: bytes, addr: tuple[str, int]) -> None:
        if self.session is None:
            return
        self.session.recent_datagrams.append(data)
        self.session.datagrams_received += 1
        self.session.bytes_received += len(data)
        self.session.last_datagram_at = time.monotonic()
        self.session.error = None
        self.session.first_datagram.set()
        for queue in list(self.session.subscribers):
            self._manager.queue_put_latest(queue, data)

    def error_received(self, exc: Exception) -> None:
        if self.session is not None:
            self.session.error = f"{type(exc).__name__}: {exc}"

    def connection_lost(self, exc: Exception | None) -> None:
        if self.session is None:
            return
        if exc:
            self.session.error = f"{type(exc).__name__}: {exc}"
        for queue in list(self.session.subscribers):
            self._manager.queue_put_latest(queue, None)


class PreviewManager:
    """Manage GoPro UDP MPEG-TS preview sessions for standalone mode."""

    def __init__(self, error_cls: type[Exception] = RuntimeError) -> None:
        self._sessions: dict[str, PreviewSession] = {}
        self._error_cls = error_cls

    async def start(self, camera_id: str, *, port: int | None = None) -> PreviewSession:
        """Start or return a running preview session."""
        existing = self._sessions.get(camera_id)
        if existing and (port is None or existing.port == port):
            return existing
        if existing:
            await self.stop(camera_id)

        port = port or _free_udp_port()
        protocol = PreviewDatagramProtocol(self)
        transport, _ = await asyncio.get_running_loop().create_datagram_endpoint(
            lambda: protocol,
            local_addr=("0.0.0.0", port),
            allow_broadcast=False,
        )
        session = PreviewSession(camera_id, port, transport)
        protocol.session = session
        self._sessions[camera_id] = session
        return session

    async def stop(self, camera_id: str) -> None:
        """Stop a preview session if present."""
        session = self._sessions.pop(camera_id, None)
        if session is None:
            return
        for queue in list(session.subscribers):
            self._queue_put_latest(queue, None)
        session.transport.close()

    def status(self, camera_id: str) -> dict[str, Any]:
        """Return preview relay status for a camera."""
        session = self._sessions.get(camera_id)
        running = bool(session and not session.transport.is_closing())
        return {
            "available": True,
            "running": running,
            "port": session.port if session else None,
            "datagrams_received": session.datagrams_received if session else 0,
            "bytes_received": session.bytes_received if session else 0,
            "seconds_since_last_datagram": (
                round(time.monotonic() - session.last_datagram_at, 3)
                if session and session.last_datagram_at is not None
                else None
            ),
            "error": session.error if session else None,
            "transport": "mpegts",
            "stream_url": (
                f"/api/cameras/{camera_id}/preview.ts"
                if running and session and session.datagrams_received
                else None
            ),
        }

    def subscribe(self, camera_id: str) -> asyncio.Queue[bytes | None]:
        """Subscribe to MPEG-TS bytes for a camera."""
        session = self._sessions.get(camera_id)
        if session is None or session.transport.is_closing():
            raise self._error_cls("预览尚未启动")
        queue: asyncio.Queue[bytes | None] = asyncio.Queue(maxsize=8)
        session.subscribers.add(queue)
        for datagram in session.recent_datagrams:
            self._queue_put_latest(queue, datagram)
        return queue

    def unsubscribe(self, camera_id: str, queue: asyncio.Queue[bytes | None]) -> None:
        """Remove a preview subscriber."""
        session = self._sessions.get(camera_id)
        if session:
            session.subscribers.discard(queue)

    async def wait_for_datagram(self, camera_id: str, timeout: float) -> bool:
        """Return whether the camera has sent preview bytes within timeout."""
        session = self._sessions.get(camera_id)
        if session is None or session.transport.is_closing():
            return False
        if session.datagrams_received:
            return True
        try:
            await asyncio.wait_for(session.first_datagram.wait(), timeout=timeout)
            return True
        except TimeoutError:
            session.error = (
                f"预览已启动但 {timeout:g}s 内没有收到 UDP 数据；"
                f"请确认相机能向本机 UDP {session.port} 发送预览流。"
            )
            return False

    async def close(self) -> None:
        """Stop all preview sessions."""
        await asyncio.gather(
            *(self.stop(camera_id) for camera_id in list(self._sessions)),
            return_exceptions=True,
        )

    def queue_put_latest(self, queue: asyncio.Queue[bytes | None], item: bytes | None) -> None:
        """Put an item into a bounded queue, dropping stale preview bytes."""
        self._queue_put_latest(queue, item)

    @staticmethod
    def _queue_put_latest(queue: asyncio.Queue[bytes | None], item: bytes | None) -> None:
        """Put an item into a bounded queue, dropping stale preview bytes."""
        if queue.full():
            try:
                queue.get_nowait()
            except asyncio.QueueEmpty:
                pass
        try:
            queue.put_nowait(item)
        except asyncio.QueueFull:
            pass


def _free_udp_port() -> int:
    """Return an available UDP port for GoPro preview."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(("0.0.0.0", 0))
        return int(sock.getsockname()[1])
