"""OpenGoPro BLE and HTTP client primitives."""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any, Callable

from aiohttp import BasicAuth, ClientError, ClientSession

from . import protocol
from .models import (
    CameraMediaItem,
    CameraSnapshot,
    CohnCredentials,
    ConnectionPhase,
    OpenGoProCommandError,
    OpenGoProConnectionError,
    OpenGoProError,
    OpenGoProHttpError,
    WifiScanEntry,
)
from .state import normalize_camera_state


class OpenGoProClient:
    """Small OpenGoPro transport wrapper.

    BLE command encoding is intentionally isolated here. HTTP command/control is
    used whenever possible because OpenGoPro's high-throughput features and media
    APIs are exposed there.
    """

    def __init__(
        self,
        session: ClientSession,
        ble_address: str,
        *,
        name: str | None = None,
        http_host: str = protocol.DEFAULT_HTTP_HOST,
        http_port: int = protocol.DEFAULT_HTTP_PORT,
        http_scheme: str = protocol.DEFAULT_HTTP_SCHEME,
        http_username: str | None = None,
        http_password: str | None = None,
        verify_ssl: bool = True,
        ble_device: Any | None = None,
        ble_device_callback: Callable[[], Any | None] | None = None,
    ) -> None:
        self._session = session
        self.ble_address = ble_address
        self._ble_device = ble_device
        self._ble_device_callback = ble_device_callback
        self.name = name or "GoPro"
        self.http_host = http_host
        self.http_port = http_port
        self.http_scheme = http_scheme
        self.http_username = http_username or None
        self.http_password = http_password or None
        self.verify_ssl = verify_ssl
        self.phase = ConnectionPhase.DISCONNECTED
        self._ble_client: Any | None = None
        self._ble_response_queue: asyncio.Queue[bytes] = asyncio.Queue()
        self._ble_accumulators: dict[str, _BlePacketAccumulator] = {}
        self._preview_active = False
        self.last_provision_stage = "idle"
        self.last_connect_trace: list[dict[str, Any]] = []
        self.last_notification_trace: list[dict[str, Any]] = []

    @property
    def base_url(self) -> str:
        """Return camera HTTP API base URL."""
        return f"{self.http_scheme}://{self.http_host}:{self.http_port}"

    async def async_ble_connect(self) -> None:
        """Connect to the camera over BLE.

        Home Assistant provides the Bluetooth adapter and discovery cache. Bleak
        is imported lazily so tests and non-BLE deployments can still load the
        integration.
        """
        try:
            from bleak import BleakClient
            from bleak.backends.device import BLEDevice
            from bleak_retry_connector import establish_connection
        except ImportError as err:  # pragma: no cover - HA installs requirements
            raise OpenGoProConnectionError("Bleak retry connector is not installed") from err

        if self._ble_client and self._ble_client.is_connected:
            self.phase = ConnectionPhase.BLE_CONNECTED
            return

        ble_device = self._ble_device
        if ble_device is None and self._ble_device_callback is not None:
            ble_device = self._ble_device_callback()
        if ble_device is None:
            ble_device = BLEDevice(self.ble_address, self.name, {})
        try:
            client = await asyncio.wait_for(
                establish_connection(
                    BleakClient,
                    ble_device,
                    self.name,
                    ble_device_callback=self._ble_device_callback,
                ),
                timeout=30,
            )
        except Exception as err:  # noqa: BLE connection libraries raise broad errors
            detail = f"{type(err).__name__}: {err!r}"
            raise OpenGoProConnectionError(f"BLE connection failed: {detail}") from err

        self._ble_device = ble_device
        self._ble_client = client
        await self._ble_start_notifications()
        self.phase = ConnectionPhase.BLE_CONNECTED

    async def async_ble_disconnect(self) -> None:
        """Disconnect BLE if connected."""
        if self._ble_client and self._ble_client.is_connected:
            await self._ble_client.disconnect()
        self._ble_client = None
        self._ble_accumulators = {}
        self.phase = ConnectionPhase.DISCONNECTED

    async def async_wake(self) -> None:
        """Wake the camera and make the HTTP API reachable."""
        await self.async_ble_connect()
        await self.async_enable_wifi()
        await self.async_wait_http_ready()

    async def async_enable_wifi(self) -> None:
        """Enable camera Wi-Fi through BLE.

        OpenGoPro documents this as the Set AP Control TLV command, ID 0x17,
        parameter mode=1. The HTTP readiness probe remains the source of truth
        because AP startup time varies by model and firmware.
        """
        if self.phase == ConnectionPhase.DISCONNECTED:
            await self.async_ble_connect()
        await self._ble_write_command(protocol.GOPRO_COMMAND_UUID, protocol.BLE_CMD_SET_AP_CONTROL, [1])
        self.phase = ConnectionPhase.WIFI_ENABLED

    async def async_provision_cohn(
        self,
        ssid: str,
        password: str,
        *,
        clear_certificate: bool = True,
        force_new_credentials: bool = False,
        timeout: float = 120,
    ) -> CohnCredentials:
        """Provision HERO12+ Camera on the Home Network over BLE."""
        if self.phase == ConnectionPhase.DISCONNECTED:
            self.last_provision_stage = "ble_connect"
            await self.async_ble_connect()
        self.last_provision_stage = "set_datetime"
        await self.async_set_local_datetime()
        self.last_provision_stage = "connect_wifi"
        await self.async_connect_to_access_point(
            ssid,
            password,
            force_new_credentials=force_new_credentials,
            timeout=timeout,
        )
        if clear_certificate:
            self.last_provision_stage = "clear_certificate"
            await self.async_clear_cohn_certificate()
        self.last_provision_stage = "create_certificate"
        await self.async_create_cohn_certificate()
        self.last_provision_stage = "get_certificate"
        certificate = await self.async_get_cohn_certificate()
        self.last_provision_stage = "wait_cohn_status"
        status = await self.async_wait_cohn_status(timeout=timeout)
        self.last_provision_stage = "cohn_status_received"
        credentials = CohnCredentials(
            certificate=certificate,
            username=_first_string(status, 3) or "",
            password=_first_string(status, 4) or "",
            ip_address=_first_string(status, 5) or "",
            ssid=_first_string(status, 7),
            mac_address=_first_string(status, 8),
        )
        if not credentials.username or not credentials.password or not credentials.ip_address:
            raise OpenGoProConnectionError("COHN provisioning did not return complete credentials")
        self.http_scheme = "https"
        self.http_host = credentials.ip_address
        self.http_port = 443
        self.http_username = credentials.username
        self.http_password = credentials.password
        self.last_provision_stage = "done"
        return credentials

    async def async_set_local_datetime(self) -> None:
        """Set camera local date/time via BLE before COHN certificate creation."""
        now = datetime.now().astimezone()
        offset_minutes = int((now.utcoffset().total_seconds() if now.utcoffset() else 0) / 60)
        dst_minutes = int((now.dst().total_seconds() if now.dst() else 0) / 60)
        is_dst = bool(dst_minutes)
        standard_offset = offset_minutes - dst_minutes
        payload = bytes(
            [
                protocol.BLE_CMD_SET_LOCAL_DATE_TIME,
                10,
                *now.year.to_bytes(2, "big", signed=False),
                now.month,
                now.day,
                now.hour,
                now.minute,
                now.second,
                *standard_offset.to_bytes(2, "big", signed=True),
                int(is_dst),
            ]
        )
        await self._ble_write_payload(protocol.GOPRO_COMMAND_UUID, payload)
        response = await self._ble_next_payload(
            feature=protocol.BLE_CMD_SET_LOCAL_DATE_TIME,
            timeout=10,
        )
        if len(response) < 2 or response[1] != 0:
            raise OpenGoProCommandError(f"Set local datetime failed: {response.hex(':')}")

    async def async_scan_access_points(
        self,
        *,
        timeout: float = 45,
        trace: list[dict[str, Any]] | None = None,
    ) -> list[WifiScanEntry]:
        """Scan Wi-Fi access points from the camera."""
        if trace is not None:
            trace.append({"step": "scan_write"})
        await self._ble_write_payload(
            protocol.GOPRO_NETWORK_MANAGEMENT_UUID,
            bytes([protocol.PROTO_FEATURE_NETWORK, protocol.PROTO_ACTION_SCAN_START_REQ]),
        )
        scan_id: int | None = None
        total_entries: int | None = None
        try:
            async with asyncio.timeout(timeout):
                while scan_id is None:
                    feature, action, message = await self._ble_next_protobuf(timeout=timeout)
                    if feature != protocol.PROTO_FEATURE_NETWORK:
                        continue
                    fields = _decode_protobuf_fields(message)
                    if trace is not None:
                        trace.append(
                            {
                                "step": "scan_response",
                                "action": action,
                                "fields": _debug_proto_fields(fields),
                            }
                    )
                    if action == protocol.PROTO_ACTION_SCAN_START_RSP:
                        _assert_proto_success(fields, "Start Wi-Fi scan")
                    elif action == protocol.PROTO_ACTION_SCAN_NOTIFY:
                        if _first_int(fields, 1) == protocol.PROTO_SCAN_SUCCESS:
                            scan_id = _first_int(fields, 2)
                            total_entries = _first_int(fields, 3)
        except TimeoutError as err:
            raise OpenGoProConnectionError(f"Wi-Fi scan timed out: {trace}") from err
        if scan_id is None:
            raise OpenGoProConnectionError("Wi-Fi scan did not return a scan ID")
        if total_entries == 0:
            return []
        return await self.async_get_access_point_entries(
            scan_id,
            total_entries=total_entries,
            timeout=timeout,
            trace=trace,
        )

    async def async_release_network(self) -> None:
        """Disconnect the camera from the current Station-mode access point."""
        await self._ble_write_payload(
            protocol.GOPRO_NETWORK_MANAGEMENT_UUID,
            bytes([protocol.PROTO_FEATURE_NETWORK, protocol.PROTO_ACTION_RELEASE_NETWORK_REQ]),
        )
        await self._wait_generic_protobuf_response(
            protocol.PROTO_FEATURE_NETWORK,
            protocol.PROTO_ACTION_RELEASE_NETWORK_RSP,
            "Release Wi-Fi network",
        )

    async def async_get_access_point_entries(
        self,
        scan_id: int,
        *,
        total_entries: int | None = None,
        timeout: float = 45,
        trace: list[dict[str, Any]] | None = None,
    ) -> list[WifiScanEntry]:
        """Get Wi-Fi scan results for a completed scan."""
        max_entries = max(1, total_entries or 100)
        request = bytes(
            [protocol.PROTO_FEATURE_NETWORK, protocol.PROTO_ACTION_GET_AP_ENTRIES_REQ]
        ) + _proto_int(1, 0) + _proto_int(2, max_entries) + _proto_int(3, scan_id)
        if trace is not None:
            trace.append({"step": "scan_entries_write", "scan_id": scan_id})
        await self._ble_write_payload(protocol.GOPRO_NETWORK_MANAGEMENT_UUID, request)
        try:
            async with asyncio.timeout(timeout):
                while True:
                    feature, action, message = await self._ble_next_protobuf(timeout=timeout)
                    if feature != protocol.PROTO_FEATURE_NETWORK:
                        continue
                    fields = _decode_protobuf_fields(message)
                    if trace is not None:
                        trace.append(
                            {
                                "step": "scan_entries_response",
                                "action": action,
                                "fields": _debug_proto_fields(fields),
                            }
                        )
                    if action != protocol.PROTO_ACTION_GET_AP_ENTRIES_RSP:
                        continue
                    _assert_proto_success(fields, "Get Wi-Fi scan results")
                    entries: list[WifiScanEntry] = []
                    raw_entries = fields.get(3, [])
                    if isinstance(raw_entries, bytes):
                        raw_entries = [raw_entries]
                    for raw_entry in raw_entries:
                        if not isinstance(raw_entry, bytes):
                            continue
                        entry_fields = _decode_protobuf_fields(raw_entry)
                        ssid = _first_string(entry_fields, 1)
                        if not ssid:
                            continue
                        entries.append(
                            WifiScanEntry(
                                ssid=ssid,
                                signal_strength_bars=_first_int(entry_fields, 2),
                                signal_frequency_mhz=_first_int(entry_fields, 4),
                                flags=_first_int(entry_fields, 5) or 0,
                            )
                        )
                    return entries
        except TimeoutError as err:
            raise OpenGoProConnectionError(f"Wi-Fi scan entries timed out: {trace}") from err

    async def async_connect_to_access_point(
        self,
        ssid: str,
        password: str,
        *,
        force_new_credentials: bool = False,
        timeout: float = 90,
        entries: list[WifiScanEntry] | None = None,
        trace: list[dict[str, Any]] | None = None,
    ) -> None:
        """Connect the camera to an access point in Station mode."""
        trace = trace if trace is not None else []
        trace.append(
            {
                "step": "scan_start",
                "ssid": ssid,
                "force_new_credentials": force_new_credentials,
                "cached_entries": entries is not None,
            }
        )
        self.last_connect_trace = trace
        if entries is None:
            entries = await self.async_scan_access_points(timeout=timeout, trace=trace)
        trace.append(
            {
                "step": "scan_done",
                "entries": [
                    {
                        "ssid": entry.ssid,
                        "bars": entry.signal_strength_bars,
                        "frequency": entry.signal_frequency_mhz,
                        "flags": entry.flags,
                        "configured": entry.is_configured,
                    }
                    for entry in entries
                ],
            }
        )
        matched = next((entry for entry in entries if entry.ssid == ssid), None)
        if matched is None:
            available = ", ".join(entry.ssid for entry in entries) or "none"
            raise OpenGoProConnectionError(f"SSID not found by GoPro scan: {ssid}. Found: {available}")
        if matched.is_configured:
            request = bytes([protocol.PROTO_FEATURE_NETWORK, protocol.PROTO_ACTION_CONNECT_REQ]) + _proto_string(1, ssid)
            expected_response = protocol.PROTO_ACTION_CONNECT_RSP
        else:
            request = (
                bytes([protocol.PROTO_FEATURE_NETWORK, protocol.PROTO_ACTION_CONNECT_NEW_REQ])
                + _proto_string(1, ssid)
                + _proto_string(2, password)
                + _proto_bool(10, True)
            )
            expected_response = protocol.PROTO_ACTION_CONNECT_NEW_RSP
        trace.append(
            {
                "step": "connect_write",
                "action": expected_response,
                "matched_flags": matched.flags,
                "payload_length": len(request),
                "packet_lengths": [len(packet) for packet in _packetize_ble_payload(request)],
            }
        )
        await self._ble_write_payload(protocol.GOPRO_NETWORK_MANAGEMENT_UUID, request)
        try:
            async with asyncio.timeout(timeout):
                while True:
                    feature, action, message = await self._ble_next_protobuf(timeout=timeout)
                    if feature != protocol.PROTO_FEATURE_NETWORK:
                        continue
                    fields = _decode_protobuf_fields(message)
                    trace.append(
                        {
                            "step": "connect_response",
                            "action": action,
                            "fields": _debug_proto_fields(fields),
                        }
                    )
                    if action == expected_response:
                        _assert_proto_success(fields, "Connect Wi-Fi")
                        continue
                    if action != protocol.PROTO_ACTION_CONNECT_NOTIFY:
                        continue
                    state = _first_int(fields, 1)
                    if state in (
                        protocol.PROTO_PROVISIONING_SUCCESS_NEW_AP,
                        protocol.PROTO_PROVISIONING_SUCCESS_OLD_AP,
                    ):
                        trace.append({"step": "connect_done", "state": state})
                        return
                    if state != protocol.PROTO_PROVISIONING_STARTED:
                        raise OpenGoProConnectionError(f"Unexpected Wi-Fi provisioning state: {state}")
        except TimeoutError as err:
            raise OpenGoProConnectionError(f"Wi-Fi provisioning timed out: {trace}") from err

    async def async_clear_cohn_certificate(self) -> None:
        """Clear the current COHN certificate."""
        await self._ble_write_payload(
            protocol.GOPRO_COMMAND_UUID,
            bytes([protocol.PROTO_FEATURE_COMMAND, protocol.PROTO_ACTION_CLEAR_COHN_CERT_REQ]),
        )
        await self._wait_generic_protobuf_response(
            protocol.PROTO_FEATURE_COMMAND,
            protocol.PROTO_ACTION_CLEAR_COHN_CERT_RSP,
            "Clear COHN certificate",
        )

    async def async_create_cohn_certificate(self) -> None:
        """Create a new COHN certificate."""
        await self._ble_write_payload(
            protocol.GOPRO_COMMAND_UUID,
            bytes([protocol.PROTO_FEATURE_COMMAND, protocol.PROTO_ACTION_CREATE_COHN_CERT_REQ]),
        )
        await self._wait_generic_protobuf_response(
            protocol.PROTO_FEATURE_COMMAND,
            protocol.PROTO_ACTION_CREATE_COHN_CERT_RSP,
            "Create COHN certificate",
        )

    async def async_get_cohn_certificate(self) -> str:
        """Read the current COHN certificate."""
        await self._ble_write_payload(
            protocol.GOPRO_QUERY_UUID,
            bytes([protocol.PROTO_FEATURE_QUERY, protocol.PROTO_ACTION_GET_COHN_CERT_REQ]),
        )
        while True:
            feature, action, message = await self._ble_next_protobuf(timeout=20)
            if feature != protocol.PROTO_FEATURE_QUERY or action != protocol.PROTO_ACTION_GET_COHN_CERT_RSP:
                continue
            fields = _decode_protobuf_fields(message)
            _assert_proto_success(fields, "Get COHN certificate")
            certificate = _first_string(fields, 2)
            if not certificate:
                raise OpenGoProCommandError("COHN certificate response did not include a certificate")
            return certificate

    async def async_wait_cohn_status(self, *, timeout: float = 120) -> dict[int, Any]:
        """Wait until COHN reports a connected home-network state."""
        await self._ble_write_payload(
            protocol.GOPRO_QUERY_UUID,
            bytes([protocol.PROTO_FEATURE_QUERY, protocol.PROTO_ACTION_GET_COHN_STATUS_REQ]) + _proto_bool(1, True),
        )
        async with asyncio.timeout(timeout):
            while True:
                feature, action, message = await self._ble_next_protobuf(timeout=timeout)
                if feature != protocol.PROTO_FEATURE_QUERY or action != protocol.PROTO_ACTION_GET_COHN_STATUS_RSP:
                    continue
                fields = _decode_protobuf_fields(message)
                if _first_int(fields, 2) == protocol.PROTO_COHN_NETWORK_CONNECTED:
                    return fields

    async def async_wait_http_ready(self) -> None:
        """Wait until the HTTP API returns a camera state response."""
        last_error: Exception | None = None
        for _ in range(10):
            try:
                await self.async_get_state()
            except OpenGoProError as err:
                last_error = err
                await asyncio.sleep(1)
                continue
            self.phase = ConnectionPhase.HTTP_READY
            return
        raise OpenGoProConnectionError("HTTP API did not become ready") from last_error

    async def async_sleep(self) -> None:
        """Put camera to sleep over HTTP where supported."""
        await self._get_json("/gp/gpControl/command/system/sleep", timeout=15)
        self.phase = ConnectionPhase.DISCONNECTED

    async def async_ble_sleep(self) -> None:
        """Put camera to sleep over BLE TLV where supported."""
        try:
            if self.phase == ConnectionPhase.DISCONNECTED:
                await self.async_ble_connect()
            await self._ble_write_command(protocol.GOPRO_COMMAND_UUID, protocol.BLE_CMD_SLEEP)
        finally:
            await self.async_ble_disconnect()

    async def async_keep_alive(self) -> None:
        """Reset the camera Keep Alive timer."""
        if self._ble_client and self._ble_client.is_connected:
            await self._ble_write_command(
                protocol.GOPRO_SETTING_UUID, protocol.BLE_CMD_KEEP_ALIVE, [protocol.BLE_KEEP_ALIVE_VALUE]
            )
            return
        await self._get_json("/gopro/camera/keep_alive")

    async def async_shutter(self, active: bool) -> None:
        """Start or stop the shutter."""
        action = "start" if active else "stop"
        await self._get_json(f"/gopro/camera/shutter/{action}")

    async def async_set_mode(self, mode: str) -> None:
        """Set a broad camera mode.

        OpenGoPro exposes the main Video / Photo / Timelapse switch as a
        Preset Group. Preset IDs themselves are camera-specific and must not be
        hard-coded for mode switching.
        """
        group_ids = {"video": 1000, "photo": 1001, "timelapse": 1002}
        group_id = group_ids.get(mode)
        if group_id is None:
            raise OpenGoProCommandError(f"Unsupported mode: {mode}")
        await self._get_json(f"/gopro/camera/presets/set_group?id={group_id}")

    async def async_set_preset(self, preset: str) -> None:
        """Load a camera preset by id/name."""
        await self._get_json(f"/gopro/camera/presets/load?id={preset}")

    async def async_get_preset_status(self, *, include_hidden: bool = True) -> dict[str, Any]:
        """Return the camera's currently available preset hierarchy."""
        if not include_hidden:
            return await self._get_json("/gopro/camera/presets/get")
        try:
            return await self._get_json("/gopro/camera/presets/get?include-hidden=1")
        except OpenGoProHttpError as err:
            if err.status != 400:
                raise
            return await self._get_json("/gopro/camera/presets/get")

    async def async_set_setting(self, setting: str, option: str) -> None:
        """Set an OpenGoPro setting option."""
        await self._get_json(f"/gopro/camera/setting?setting={setting}&option={option}")

    async def async_start_preview(self, *, port: int | None = None) -> None:
        """Start the camera preview stream without proxying it to the browser."""
        path = "/gopro/camera/stream/start"
        if port is not None:
            path = f"{path}?port={port}"
        await self._get_json(path, timeout=60)
        self._preview_active = True

    async def async_stop_preview(self) -> None:
        """Stop the camera preview stream."""
        await self._get_json("/gopro/camera/stream/stop", timeout=30)
        self._preview_active = False

    async def async_get_state(self) -> CameraSnapshot:
        """Fetch and normalize camera state."""
        payload = await self._get_json("/gopro/camera/state")
        self.phase = ConnectionPhase.HTTP_READY
        return self._normalize_state(payload)

    async def async_list_media(self) -> list[CameraMediaItem]:
        """List media files on the camera."""
        payload = await self._get_json("/gopro/media/list")
        media: list[CameraMediaItem] = []
        for directory in payload.get("media", []):
            dirname = directory.get("d", "")
            for item in directory.get("fs", []):
                name = item.get("n")
                if not name:
                    continue
                media.append(
                    CameraMediaItem(
                        directory=dirname,
                        name=name,
                        size=_int_or_none(item.get("s")),
                        created=item.get("cre"),
                        media_type=_guess_media_type(name),
                    )
                )
        return media

    def media_url(self, path: str) -> str:
        """Return the direct camera media URL for a camera-relative path."""
        return f"{self.base_url}/videos/DCIM/{path.lstrip('/')}"

    def media_thumbnail_url(self, path: str) -> str:
        """Return the direct camera thumbnail endpoint for a media path."""
        return f"{self.base_url}/gopro/media/thumbnail?path={path.lstrip('/')}"

    async def _ble_write_command(
        self,
        characteristic_uuid: str,
        command_id: int,
        parameters: list[int] | None = None,
    ) -> None:
        """Write a small OpenGoPro TLV command to a BLE characteristic."""
        if not self._ble_client or not self._ble_client.is_connected:
            raise OpenGoProConnectionError("BLE is not connected")
        payload = bytes([command_id])
        for value in parameters or []:
            payload += bytes([1, value])
        await self._ble_write_payload(characteristic_uuid, payload)

    async def _ble_write_payload(self, characteristic_uuid: str, payload: bytes) -> None:
        """Write an OpenGoPro BLE message payload, fragmenting when needed."""
        if not self._ble_client or not self._ble_client.is_connected:
            raise OpenGoProConnectionError("BLE is not connected")
        for packet in _packetize_ble_payload(payload):
            await self._ble_client.write_gatt_char(
                characteristic_uuid,
                packet,
                response=True,
            )

    async def _ble_start_notifications(self) -> None:
        """Subscribe to response characteristics needed by commands and COHN."""
        if not self._ble_client:
            return
        self.last_notification_trace = []
        for uuid in (
            protocol.GOPRO_COMMAND_RESPONSE_UUID,
            protocol.GOPRO_SETTING_RESPONSE_UUID,
            protocol.GOPRO_QUERY_RESPONSE_UUID,
            protocol.GOPRO_NETWORK_MANAGEMENT_RESPONSE_UUID,
        ):
            try:
                await self._ble_client.start_notify(uuid, self._ble_notification_handler)
                self.last_notification_trace.append({"uuid": uuid, "ok": True})
            except Exception as err:
                self.last_notification_trace.append(
                    {
                        "uuid": uuid,
                        "ok": False,
                        "error": str(err),
                        "error_type": type(err).__name__,
                    }
                )
                # Some cameras/firmware may not expose every response UUID. COHN
                # will fail later with a concrete timeout if the required one is absent.
                continue

    def _ble_notification_handler(self, characteristic: Any, data: bytearray) -> None:
        """Handle a BLE notification packet from Bleak."""
        uuid = str(getattr(characteristic, "uuid", characteristic)).lower()
        accumulator = self._ble_accumulators.setdefault(uuid, _BlePacketAccumulator())
        payload = accumulator.add(bytes(data))
        if payload is None:
            return
        self._ble_accumulators[uuid] = _BlePacketAccumulator()
        self._ble_response_queue.put_nowait(payload)

    async def _ble_next_payload(
        self,
        *,
        feature: int | None = None,
        action: int | None = None,
        timeout: float = 30,
    ) -> bytes:
        """Return the next BLE payload matching optional leading bytes."""
        async with asyncio.timeout(timeout):
            while True:
                payload = await self._ble_response_queue.get()
                if feature is not None and (not payload or payload[0] != feature):
                    continue
                if action is not None and (len(payload) < 2 or payload[1] != action):
                    continue
                return payload

    async def _ble_next_protobuf(self, timeout: float = 30) -> tuple[int, int, bytes]:
        """Return the next Protobuf feature/action/body tuple."""
        payload = await self._ble_next_payload(timeout=timeout)
        if len(payload) < 2:
            raise OpenGoProCommandError(f"Invalid protobuf payload: {payload.hex(':')}")
        return payload[0], payload[1], payload[2:]

    async def _wait_generic_protobuf_response(
        self,
        feature: int,
        action: int,
        operation: str,
    ) -> None:
        """Wait for a generic protobuf success response."""
        while True:
            response_feature, response_action, message = await self._ble_next_protobuf(timeout=20)
            if response_feature != feature or response_action != action:
                continue
            _assert_proto_success(_decode_protobuf_fields(message), operation)
            return

    async def _get_json(self, path: str, *, timeout: float = 15) -> dict[str, Any]:
        """GET an endpoint and parse JSON."""
        url = f"{self.base_url}{path}"
        try:
            async with asyncio.timeout(timeout):
                response = await self._session.get(
                    url,
                    auth=self._http_auth(),
                    ssl=self.verify_ssl,
                )
                if response.content_type == "application/json":
                    data = await response.json()
                else:
                    text = await response.text()
                    data = {} if not text.strip() else {"response": text}
                status = getattr(response, "status", 200)
                if status >= 400:
                    payload = data if isinstance(data, dict) else {}
                    detail = payload.get("error") or payload.get("message") or response.reason
                    raise OpenGoProHttpError(
                        f"HTTP {status} {detail}: {url}",
                        status=status,
                        payload=payload,
                        url=url,
                    )
        except (TimeoutError, ClientError) as err:
            raise OpenGoProConnectionError(f"HTTP request failed: {url}") from err
        if isinstance(data, dict) and data.get("error"):
            raise OpenGoProCommandError(str(data["error"]))
        return data if isinstance(data, dict) else {}

    def _http_auth(self) -> BasicAuth | None:
        """Return HTTP auth for COHN, if configured."""
        if self.http_username is None or self.http_password is None:
            return None
        return BasicAuth(self.http_username, self.http_password)

    def _normalize_state(self, payload: dict[str, Any]) -> CameraSnapshot:
        """Convert raw OpenGoPro state into stable HA-facing keys."""
        return normalize_camera_state(
            payload,
            phase=self.phase,
            name=self.name,
            preview_active=self._preview_active,
        )


def _guess_media_type(name: str) -> str:
    """Guess media type from file extension."""
    suffix = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    if suffix in {"jpg", "jpeg"}:
        return "image/jpeg"
    if suffix == "png":
        return "image/png"
    if suffix in {"mp4", "lrv"}:
        return "video/mp4"
    return "application/octet-stream"


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


class _BlePacketAccumulator:
    """Accumulate OpenGoPro BLE packets into complete message payloads."""

    def __init__(self) -> None:
        self.expected_length: int | None = None
        self.payload = bytearray()

    def add(self, packet: bytes) -> bytes | None:
        """Add a packet and return the complete payload when available."""
        if not packet:
            return None
        first = packet[0]
        if first & 0x80:
            self.payload.extend(packet[1:])
        elif first & 0x60 == 0x20:
            self.expected_length = int.from_bytes(packet[:2], "big") & 0x1FFF
            self.payload = bytearray(packet[2:])
        elif first & 0x60 == 0x40:
            self.expected_length = int.from_bytes(packet[1:3], "big")
            self.payload = bytearray(packet[3:])
        else:
            self.expected_length = first & 0x1F
            self.payload = bytearray(packet[1:])
        if self.expected_length is not None and len(self.payload) >= self.expected_length:
            return bytes(self.payload[: self.expected_length])
        return None


def _packetize_ble_payload(payload: bytes) -> list[bytes]:
    """Add OpenGoPro BLE extended packet headers, fragmenting when needed."""
    if len(payload) >= 2**13:
        raise OpenGoProCommandError("BLE payload is too large for 13-bit packet writer")
    packets: list[bytes] = []
    header = (len(payload) | 0x2000).to_bytes(2, "big")
    index = 0
    counter = 0
    while index < len(payload):
        if not packets:
            packet_header = header
        else:
            packet_header = bytes([0x80 | (counter & 0x0F)])
            counter += 1
        size = 20 - len(packet_header)
        packets.append(packet_header + payload[index : index + size])
        index += size
    return packets


def _encode_varint(value: int) -> bytes:
    """Encode an integer as a protobuf varint."""
    if value < 0:
        value &= (1 << 64) - 1
    out = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            return bytes(out)


def _decode_varint(data: bytes, index: int) -> tuple[int, int]:
    """Decode a protobuf varint from data starting at index."""
    shift = 0
    value = 0
    while index < len(data):
        byte = data[index]
        index += 1
        value |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return value, index
        shift += 7
    raise OpenGoProCommandError("Truncated protobuf varint")


def _proto_key(field: int, wire_type: int) -> bytes:
    return _encode_varint((field << 3) | wire_type)


def _proto_int(field: int, value: int) -> bytes:
    return _proto_key(field, 0) + _encode_varint(value)


def _proto_bool(field: int, value: bool) -> bytes:
    return _proto_int(field, int(value))


def _proto_string(field: int, value: str) -> bytes:
    encoded = value.encode()
    return _proto_key(field, 2) + _encode_varint(len(encoded)) + encoded


def _decode_protobuf_fields(message: bytes) -> dict[int, Any]:
    """Decode simple protobuf fields used by OpenGoPro COHN messages."""
    fields: dict[int, list[Any]] = {}
    index = 0
    while index < len(message):
        key, index = _decode_varint(message, index)
        field = key >> 3
        wire_type = key & 0x07
        if wire_type == 0:
            value, index = _decode_varint(message, index)
        elif wire_type == 2:
            length, index = _decode_varint(message, index)
            value = message[index : index + length]
            index += length
        else:
            raise OpenGoProCommandError(f"Unsupported protobuf wire type: {wire_type}")
        fields.setdefault(field, []).append(value)
    return {key: values[0] if len(values) == 1 else values for key, values in fields.items()}


def _debug_proto_fields(fields: dict[int, Any]) -> dict[str, Any]:
    """Return protobuf fields in a JSON-safe form for diagnostics."""
    return {str(key): _debug_proto_value(value) for key, value in fields.items()}


def _debug_proto_value(value: Any) -> Any:
    """Return a protobuf value without leaking arbitrary binary bytes."""
    if isinstance(value, list):
        return [_debug_proto_value(item) for item in value]
    if isinstance(value, bytes):
        try:
            return value.decode()
        except UnicodeDecodeError:
            return {"hex": value.hex(":")}
    return value


def _first_int(fields: dict[int, Any], field: int) -> int | None:
    value = fields.get(field)
    if isinstance(value, list):
        value = value[0] if value else None
    return _int_or_none(value)


def _first_string(fields: dict[int, Any], field: int) -> str | None:
    value = fields.get(field)
    if isinstance(value, list):
        value = value[0] if value else None
    if isinstance(value, bytes):
        try:
            return value.decode()
        except UnicodeDecodeError:
            return None
    return value if isinstance(value, str) else None


def _assert_proto_success(fields: dict[int, Any], operation: str) -> None:
    result = _first_int(fields, 1)
    if result != protocol.PROTO_RESULT_SUCCESS:
        raise OpenGoProCommandError(f"{operation} failed with result: {result}")
