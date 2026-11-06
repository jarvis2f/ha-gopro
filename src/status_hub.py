"""Share camera status updates among connected clients."""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import Any


class CameraStatusHub:
    """Run at most one status sampler per camera while it has subscribers."""

    def __init__(self, sample: Callable[[str], Awaitable[dict[str, Any] | None]]) -> None:
        self.sample = sample
        self.subscribers: dict[str, set[asyncio.Queue[dict[str, Any]]]] = {}
        self.tasks: dict[str, asyncio.Task[None]] = {}
        self.retired: set[asyncio.Task[None]] = set()
        self.wakeups: dict[str, asyncio.Event] = {}
        self.latest: dict[str, dict[str, Any]] = {}

    def subscribe(self, camera_id: str) -> asyncio.Queue[dict[str, Any]]:
        queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue(maxsize=1)
        self.subscribers.setdefault(camera_id, set()).add(queue)
        if camera_id in self.latest:
            queue.put_nowait(self.latest[camera_id])
        if camera_id not in self.tasks:
            self.wakeups[camera_id] = asyncio.Event()
            self.tasks[camera_id] = asyncio.create_task(self._run(camera_id))
        return queue

    def unsubscribe(self, camera_id: str, queue: asyncio.Queue[dict[str, Any]]) -> None:
        subscribers = self.subscribers.get(camera_id)
        if not subscribers:
            return
        subscribers.discard(queue)
        if not subscribers:
            self.subscribers.pop(camera_id, None)
            task = self.tasks.pop(camera_id, None)
            self.wakeups.pop(camera_id, None)
            self.latest.pop(camera_id, None)
            if task:
                task.cancel()
                self.retired.add(task)
                task.add_done_callback(self.retired.discard)

    def refresh(self, camera_id: str) -> None:
        event = self.wakeups.get(camera_id)
        if event:
            event.set()

    async def _run(self, camera_id: str) -> None:
        event = self.wakeups[camera_id]
        while True:
            event.clear()
            try:
                result = await self.sample(camera_id)
            except asyncio.CancelledError:
                raise
            except Exception:
                logging.exception("Camera status sampling failed")
                result = {"power": "unknown", "phase": "unknown", "http_ready": False,
                          "status_error": "Camera status monitoring failed"}
            if not event.is_set() and result is not None and result != self.latest.get(camera_id):
                self.latest[camera_id] = result
                for queue in tuple(self.subscribers.get(camera_id, ())):
                    if queue.full():
                        queue.get_nowait()
                    queue.put_nowait(result)
            # Camera commands temporarily hold its lock. A skipped sample is not
            # an offline result, so retry promptly instead of waiting 30 seconds.
            interval = 1 if result is None else 10 if result.get("http_ready") else 30
            try:
                await asyncio.wait_for(event.wait(), timeout=interval)
            except TimeoutError:
                pass

    async def close(self) -> None:
        tasks = list(self.tasks.values()) + list(self.retired)
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        self.tasks.clear()
        self.retired.clear()
        self.subscribers.clear()
        self.wakeups.clear()
        self.latest.clear()
