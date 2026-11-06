"""Standalone OpenGoPro HTTP service."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from dataclasses import asdict, is_dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import quote, unquote

from aiohttp import ClientError, ClientSession, ClientTimeout, web

import client as client_module
from ble_process import (
    run_ble_sleep_helper,
    run_ble_wake_helper,
    run_ble_worker,
    run_ble_worker_stream,
)
from preview import PreviewManager
from schedules import (CRON_LOOKBACK, ScheduleStore, cron_missed_before, local_zone,
                       next_occurrence, now_local, validate_schedule)
from store import CameraStore
from status_hub import CameraStatusHub
OpenGoProClient = client_module.OpenGoProClient
OpenGoProError = client_module.OpenGoProError

DEFAULT_GUARD_LEAD_HOURS = 6.0
MAX_GUARD_LEAD_HOURS = 7.5
MIN_GUARD_LEAD_HOURS = 0.25


def json_response(payload: Any, status: int = 200) -> web.Response:
    """Return a JSON response."""
    return web.Response(
        text=json.dumps(payload, ensure_ascii=False, default=_json_default),
        status=status,
        content_type="application/json",
    )


def _json_default(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)
    if hasattr(value, "value"):
        return value.value
    raise TypeError(f"Object is not JSON serializable: {type(value)!r}")


def public_camera(camera: dict[str, Any]) -> dict[str, Any]:
    """Return a camera without secrets."""
    data = dict(camera)
    if data.get("http_password"):
        data["http_password"] = "***"
    return data


def create_client(
    session: ClientSession,
    camera: dict[str, Any],
    *,
    ble_device: Any | None = None,
) -> Any:
    """Create an OpenGoPro client from stored camera data."""
    return OpenGoProClient(
        session,
        camera["ble_address"],
        name=camera.get("name"),
        http_scheme=camera.get("http_scheme", "http"),
        http_host=camera.get("http_host", "10.5.5.9"),
        http_port=int(camera.get("http_port", 8080)),
        http_username=camera.get("http_username") or None,
        http_password=camera.get("http_password") or None,
        verify_ssl=bool(camera.get("verify_ssl", True)),
        ble_device=ble_device,
    )


async def health(request: web.Request) -> web.Response:
    return json_response(
        {
            "ok": True,
            "python": sys.executable,
            "ble_worker": str(
                Path(__file__).resolve().parent / "ble_worker.py"
            ),
        }
    )


async def index(request: web.Request) -> web.FileResponse:
    return web.FileResponse(Path(__file__).parent / "static" / "index.html")


async def console_asset(request: web.Request) -> web.FileResponse:
    return web.FileResponse(Path(__file__).parent / "static" / "opengopro-console.js")


async def console_styles_asset(request: web.Request) -> web.FileResponse:
    return web.FileResponse(Path(__file__).parent / "static" / "opengopro-console-styles.js")


async def mpegts_asset(request: web.Request) -> web.FileResponse:
    return web.FileResponse(Path(__file__).parent / "static" / "vendor" / "mpegts.min.js")


async def list_cameras(request: web.Request) -> web.Response:
    store: CameraStore = request.app["store"]
    return json_response({"cameras": [public_camera(camera) for camera in store.list()]})


async def add_camera(request: web.Request) -> web.Response:
    store: CameraStore = request.app["store"]
    payload = await request.json()
    try:
        camera = store.add(payload)
    except KeyError:
        return json_response({"error": "ble_address 是必填字段"}, status=400)
    return json_response({"camera": public_camera(camera)})


async def scan_ble(request: web.Request) -> web.Response:
    payload = await _optional_json(request)
    root = Path(__file__).resolve().parent
    scan_timeout = float(payload.get("timeout", 10))
    all_devices = bool(payload.get("all", False))
    worker_timeout = scan_timeout + 10 if all_devices else scan_timeout * 2 + 15
    try:
        result = await run_ble_worker(
            {
                "command": "scan",
                "timeout": scan_timeout,
                "all": all_devices,
            },
            timeout=worker_timeout,
            cwd=root,
            label="BLE 扫描 worker",
            error_cls=OpenGoProError,
        )
    except OpenGoProError as err:
        return json_response(
            {
                "devices": [],
                "error": {
                    "message": str(err),
                    "type": type(err).__name__,
                },
            },
            status=504,
        )
    status = 502 if result.get("error") else 200
    return json_response(result, status=status)


async def scan_access_points(request: web.Request) -> web.Response:
    payload = await request.json()
    address = str(payload.get("ble_address") or "").strip()
    if not address:
        return json_response(
            {"error": {"message": "ble_address 是必填字段", "type": "InvalidInput"}},
            status=400,
        )
    root = Path(__file__).resolve().parent
    result = await run_ble_worker(
        {
            "command": "scan_access_points",
            "ble_address": address,
            "resolve_timeout": float(payload.get("resolve_timeout", 10)),
            "timeout": float(payload.get("timeout", 60)),
        },
        timeout=float(payload.get("timeout", 60)) + 30,
        cwd=root,
        label="Wi-Fi 接入点扫描 worker",
        error_cls=OpenGoProError,
    )
    status = 502 if result.get("error") else 200
    return json_response(result, status=status)


async def provision_cohn(request: web.Request) -> web.Response:
    store: CameraStore = request.app["store"]
    payload = await request.json()
    address = str(payload.get("ble_address") or "").strip()
    if not address:
        return json_response(
            {"error": {"message": "ble_address 是必填字段", "type": "InvalidInput"}},
            status=400,
        )
    try:
        root = Path(__file__).resolve().parent
        worker_result = await run_ble_worker(
            {
                "command": "provision_cohn",
                "ble_address": address,
                "name": payload.get("name") or "GoPro",
                "ssid": payload["ssid"],
                "password": payload["password"],
                "verify_ssl": bool(payload.get("verify_ssl", False)),
                "keep_certificate": bool(payload.get("keep_certificate", False)),
                "force_new_credentials": bool(payload.get("force_new_credentials", True)),
                "resolve_timeout": float(payload.get("resolve_timeout", 10)),
                "timeout": float(payload.get("timeout", 360)),
            },
            timeout=float(payload.get("timeout", 360)) + 60,
            cwd=root,
            label="COHN 配置 worker",
            error_cls=OpenGoProError,
        )
        if worker_result.get("error"):
            return json_response(
                {"error": worker_result["error"], "worker": worker_result},
                status=502,
            )
        credentials = worker_result.get("credentials") or {}
        if not credentials.get("ip_address") or not credentials.get("username") or not credentials.get("password"):
            return json_response({"error": "COHN 配置未返回完整连接信息", "credentials": credentials}, status=502)
        existing = _find_camera_by_ble(store, address)
        camera_payload = {
            "name": payload.get("name") or "GoPro",
            "ble_address": address,
            "http_scheme": "https",
            "http_host": credentials.get("ip_address"),
            "http_port": 443,
            "http_username": credentials.get("username"),
            "http_password": credentials.get("password"),
            "cohn_ssid": credentials.get("ssid"),
            "cohn_mac_address": credentials.get("mac_address"),
            "verify_ssl": bool(payload.get("verify_ssl", False)),
        }
        camera = (
            store.update(existing["id"], camera_payload)
            if existing
            else store.add(camera_payload)
        )
        return json_response(
            {
                "camera": public_camera(camera),
                "credentials": credentials,
                "certificate": worker_result.get("certificate"),
            }
        )
    except OpenGoProError as err:
        return json_response({"error": str(err)}, status=502)


async def provision_cohn_stream(request: web.Request) -> web.StreamResponse:
    store: CameraStore = request.app["store"]
    payload = await request.json()
    address = str(payload.get("ble_address") or "").strip()
    if not address:
        return json_response(
            {"error": {"message": "ble_address 是必填字段", "type": "InvalidInput"}},
            status=400,
        )
    response = web.StreamResponse(
        status=200,
        headers={
            "Content-Type": "application/x-ndjson; charset=utf-8",
            "Cache-Control": "no-cache",
        },
    )
    await response.prepare(request)

    async def send(event: dict[str, Any]) -> None:
        await response.write(
            (json.dumps(event, ensure_ascii=False, default=_json_default) + "\n").encode()
        )

    root = Path(__file__).resolve().parent
    worker_payload = {
        "command": "provision_cohn",
        "progress": True,
        "ble_address": address,
        "name": payload.get("name") or "GoPro",
        "ssid": payload["ssid"],
        "password": payload["password"],
        "verify_ssl": bool(payload.get("verify_ssl", False)),
        "keep_certificate": bool(payload.get("keep_certificate", False)),
        "force_new_credentials": bool(payload.get("force_new_credentials", True)),
        "resolve_timeout": float(payload.get("resolve_timeout", 10)),
        "timeout": float(payload.get("timeout", 360)),
    }
    try:
        await send({"type": "stage", "stage": "start"})
        worker_result = await run_ble_worker_stream(
            worker_payload,
            timeout=float(payload.get("timeout", 360)) + 60,
            cwd=root,
            send=send,
            error_cls=OpenGoProError,
        )
        if worker_result.get("error"):
            await send({"type": "error", "error": worker_result["error"], "worker": worker_result})
            return response
        credentials = worker_result.get("credentials") or {}
        if not credentials.get("ip_address") or not credentials.get("username") or not credentials.get("password"):
            await send(
                {
                    "type": "error",
                    "error": "COHN 配置未返回完整连接信息",
                    "worker": worker_result,
                }
            )
            return response
        existing = _find_camera_by_ble(store, address)
        camera_payload = {
            "name": payload.get("name") or "GoPro",
            "ble_address": address,
            "http_scheme": "https",
            "http_host": credentials.get("ip_address"),
            "http_port": 443,
            "http_username": credentials.get("username"),
            "http_password": credentials.get("password"),
            "cohn_ssid": credentials.get("ssid"),
            "cohn_mac_address": credentials.get("mac_address"),
            "verify_ssl": bool(payload.get("verify_ssl", False)),
        }
        camera = (
            store.update(existing["id"], camera_payload)
            if existing
            else store.add(camera_payload)
        )
        await send(
            {
                "type": "done",
                "camera": public_camera(camera),
                "credentials": {
                    "ip_address": credentials.get("ip_address"),
                    "username": credentials.get("username"),
                    "ssid": credentials.get("ssid"),
                    "mac_address": credentials.get("mac_address"),
                    "has_password": bool(credentials.get("password")),
                },
                "worker": worker_result,
            }
        )
    except Exception as err:
        await send({"type": "error", "error": str(err), "error_type": type(err).__name__})
    finally:
        await response.write_eof()
    return response


async def camera_state(request: web.Request) -> web.Response:
    store: CameraStore = request.app["store"]
    session: ClientSession = request.app["session"]
    camera = store.get(request.match_info["camera_id"])
    if camera is None:
        raise web.HTTPNotFound(text="camera not found")
    client = create_client(session, camera)
    trace: list[dict[str, Any]] = [
        {
            "step": "http_state",
            "host": camera.get("http_host"),
            "scheme": camera.get("http_scheme"),
            "port": camera.get("http_port"),
        }
    ]
    try:
        state = await client.async_get_state()
        if not _camera_lock(request.app, camera["id"]).locked():
            _ensure_keep_alive(request.app, camera["id"])
            trace.append({"step": "keep_alive_started"})
        return json_response({"state": state, "trace": trace})
    except OpenGoProError as err:
        trace.append({"step": "http_state_failed", "error": str(err)})
        return json_response({"error": str(err), "trace": trace}, status=502)


async def camera_presence(request: web.Request) -> web.Response:
    """Return a non-waking HTTP/BLE reachability snapshot for one camera."""
    store: CameraStore = request.app["store"]
    session: ClientSession = request.app["session"]
    camera = store.get(request.match_info["camera_id"])
    if camera is None:
        raise web.HTTPNotFound(text="camera not found")
    if _camera_lock(request.app, camera["id"]).locked():
        return json_response({"power": "checking", "phase": "checking", "http_ready": False, "ble_available": None})
    client = create_client(session, camera)
    timeout = float(request.query.get("timeout", 3))
    url = f"{client.base_url}/gopro/camera/state"
    try:
        async with session.get(
            url,
            auth=client._http_auth(),
            ssl=client.verify_ssl,
            timeout=ClientTimeout(total=timeout),
        ) as response:
            response.raise_for_status()
            return json_response(
                {
                    "power": "on",
                    "phase": "http_ready",
                    "http_ready": True,
                    "ble_available": True,
                    "endpoint": client.base_url,
                }
            )
    except (TimeoutError, ClientError) as err:
        http_error = f"{type(err).__name__}: {err}"
    root = Path(__file__).resolve().parent
    ble_timeout = float(request.query.get("ble_timeout", 5))
    try:
        ble_result = await run_ble_worker(
            {
                "command": "presence",
                "ble_address": camera["ble_address"],
                "resolve_timeout": ble_timeout,
            },
            timeout=ble_timeout + 5,
            cwd=root,
            label="BLE 状态 worker",
            error_cls=OpenGoProError,
        )
    except OpenGoProError as ble_err:
        ble_result = {"ble_available": False, "error": _error_trace(ble_err)}
    ble_available = bool(ble_result.get("ble_available"))
    return json_response(
        {
            "power": "standby" if ble_available else "off",
            "phase": "ble_standby" if ble_available else "offline",
            "http_ready": False,
            "ble_available": ble_available,
            "endpoint": client.base_url,
            "error": None if ble_available else http_error,
            "http_error": http_error,
            "ble": ble_result,
        }
    )


async def _sample_camera_status(app: web.Application, camera_id: str) -> dict[str, Any] | None:
    """Read one non-waking snapshot; never recover credentials or start keepalive."""
    camera = app["store"].get(camera_id)
    if camera is None:
        return {"power": "off", "phase": "offline", "http_ready": False, "removed": True}
    if _camera_lock(app, camera_id).locked():
        return None
    client = create_client(app["session"], camera)
    try:
        payload = await client._get_json("/gopro/camera/state", timeout=3)
        if _camera_lock(app, camera_id).locked():
            return None
        client.phase = client_module.ConnectionPhase.HTTP_READY
        return {
            "power": "on", "phase": "http_ready", "http_ready": True,
            "endpoint": client.base_url, "state": asdict(client._normalize_state(payload)),
        }
    except OpenGoProError:
        pass
    if _camera_lock(app, camera_id).locked():
        return None
    try:
        ble = await run_ble_worker(
            {"command": "presence", "ble_address": camera["ble_address"], "resolve_timeout": 5},
            timeout=10, cwd=Path(__file__).resolve().parent,
            label="BLE 状态 worker", error_cls=OpenGoProError,
        )
        available = bool(ble.get("ble_available"))
    except OpenGoProError:
        available = False
    if _camera_lock(app, camera_id).locked():
        return None
    return {
        "power": "standby" if available else "off",
        "phase": "ble_standby" if available else "offline",
        "http_ready": False, "ble_available": available,
        "state": {"battery": None, "remaining_storage": None, "current_mode": None,
                  "preset": None, "recording": None, "sd_card_status": None},
    }


async def camera_status_stream(request: web.Request) -> web.StreamResponse:
    camera_id = request.match_info["camera_id"]
    if not request.app["store"].get(camera_id):
        raise web.HTTPNotFound(text="camera not found")
    hub: CameraStatusHub = request.app["status_hub"]
    queue = hub.subscribe(camera_id)
    response = web.StreamResponse(headers={
        "Content-Type": "text/event-stream", "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no",
    })
    try:
        await response.prepare(request)
        while True:
            try:
                value = await asyncio.wait_for(queue.get(), timeout=20)
                data = json.dumps(value, ensure_ascii=False, default=_json_default)
                await response.write(f"data: {data}\n\n".encode())
            except TimeoutError:
                await response.write(b": heartbeat\n\n")
    except (ConnectionResetError, BrokenPipeError):
        pass
    finally:
        hub.unsubscribe(camera_id, queue)
    return response


async def camera_status_snapshot(request: web.Request) -> web.Response:
    """Return a non-waking status snapshot when the event stream is delayed."""
    camera_id = request.match_info["camera_id"]
    if not request.app["store"].get(camera_id):
        raise web.HTTPNotFound(text="camera not found")
    if _camera_lock(request.app, camera_id).locked():
        return json_response({"error": "Camera is busy"}, status=409)
    hub: CameraStatusHub = request.app["status_hub"]
    snapshot = hub.latest.get(camera_id)
    if snapshot is None:
        snapshot = await _sample_camera_status(request.app, camera_id)
    if snapshot is None:
        return json_response({"error": "Camera is busy"}, status=409)
    return json_response(snapshot)


async def camera_wake_schedule(request: web.Request) -> web.Response:
    """Create, update, or disable the daily wake guard schedule."""
    store: CameraStore = request.app["store"]
    camera_id = request.match_info["camera_id"]
    camera = store.get(camera_id)
    if camera is None:
        raise web.HTTPNotFound(text="camera not found")
    payload = await _optional_json(request)
    if payload.get("enabled") is False:
        schedule = {"enabled": False}
    else:
        target_time = _parse_hhmm(payload.get("target_time"))
        guard_lead_hours = _coerce_guard_lead_hours(
            payload.get("guard_lead_hours", DEFAULT_GUARD_LEAD_HOURS)
        )
        schedule = {
            "enabled": True,
            "target_time": _format_hhmm(target_time),
            "guard_lead_hours": guard_lead_hours,
            "guard_time": _format_hhmm(_guard_time(target_time, guard_lead_hours)),
            "last_guard_date": camera.get("wake_schedule", {}).get("last_guard_date"),
            "last_target_date": camera.get("wake_schedule", {}).get("last_target_date"),
            "last_error": None,
            "last_event": camera.get("wake_schedule", {}).get("last_event"),
        }
    updated = store.update(camera_id, {"wake_schedule": schedule})
    if updated is None:
        raise web.HTTPNotFound(text="camera not found")
    return json_response({"ok": True, "camera": public_camera(updated)})


async def camera_media(request: web.Request) -> web.Response:
    client = _client_for_request(request)
    try:
        media = await client.async_list_media()
        return json_response({"media": media_payload(request.match_info["camera_id"], media)})
    except OpenGoProError as err:
        return json_response({"error": str(err)}, status=502)


async def camera_media_delete(request: web.Request) -> web.Response:
    """Delete selected camera files, reporting each failure independently."""
    try:
        payload = await request.json()
    except (ValueError, TypeError):
        return json_response({"error": "Invalid JSON"}, status=400)
    paths = payload.get("paths") if isinstance(payload, dict) else None
    if not isinstance(paths, list) or not paths or len(paths) > 1000 or any(not isinstance(path, str) or not path for path in paths) or len(set(paths)) != len(paths):
        return json_response({"error": "paths must be a non-empty list of unique media paths"}, status=400)
    client = _client_for_request(request)
    try:
        available = {item.path for item in await client.async_list_media()}
    except OpenGoProError as err:
        return json_response({"error": str(err)}, status=502)
    if any(path not in available for path in paths):
        return json_response({"error": "One or more media files are no longer available; refresh the list"}, status=400)
    deleted, failed = [], []
    for path in paths:
        try:
            await client.async_delete_media(path)
            deleted.append(path)
        except OpenGoProError as err:
            failed.append({"path": path, "error": str(err)})
    return json_response({"deleted": deleted, "failed": failed})


async def camera_presets(request: web.Request) -> web.Response:
    client = _client_for_request(request)
    try:
        return json_response(await client.async_get_preset_status())
    except OpenGoProError as err:
        return json_response({"error": str(err)}, status=502)


async def camera_media_file(request: web.Request) -> web.StreamResponse:
    return await _proxy_camera_url(request, thumbnail=False)


async def camera_media_thumbnail(request: web.Request) -> web.StreamResponse:
    return await _proxy_camera_url(request, thumbnail=True)


async def camera_preview_stream(request: web.Request) -> web.StreamResponse:
    """Stream GoPro UDP MPEG-TS preview output to a browser."""
    camera_id = request.match_info["camera_id"]
    manager: PreviewManager = request.app["preview_manager"]
    queue = manager.subscribe(camera_id)
    response = web.StreamResponse(
        status=200,
        headers={
            "Content-Type": "video/MP2T",
            "Cache-Control": "no-store",
        },
    )
    await response.prepare(request)
    try:
        while True:
            chunk = await queue.get()
            if chunk is None:
                break
            await response.write(chunk)
    except asyncio.CancelledError:
        raise
    except ConnectionResetError:
        return response
    finally:
        manager.unsubscribe(camera_id, queue)
    try:
        await response.write_eof()
    except ConnectionResetError:
        pass
    return response


async def camera_preview_status(request: web.Request) -> web.Response:
    """Return standalone preview runtime status."""
    manager: PreviewManager = request.app["preview_manager"]
    return json_response(manager.status(request.match_info["camera_id"]))


def _camera_lock(app: web.Application, camera_id: str) -> asyncio.Lock:
    return app["camera_locks"].setdefault(camera_id, asyncio.Lock())


async def _guard_camera_ble_operation(request: web.Request, handler: Any) -> web.StreamResponse:
    payload = await request.json()
    camera = _find_camera_by_ble(request.app["store"], str(payload.get("ble_address") or "").strip())
    if not camera:
        return await handler(request)
    lock = _camera_lock(request.app, camera["id"])
    if lock.locked():
        return json_response({"error": "Camera is busy with another operation"}, status=409)
    async with lock:
        return await handler(request)


async def guarded_scan_access_points(request: web.Request) -> web.StreamResponse:
    return await _guard_camera_ble_operation(request, scan_access_points)


async def guarded_provision_cohn(request: web.Request) -> web.StreamResponse:
    return await _guard_camera_ble_operation(request, provision_cohn)


async def guarded_provision_cohn_stream(request: web.Request) -> web.StreamResponse:
    return await _guard_camera_ble_operation(request, provision_cohn_stream)


async def camera_command(request: web.Request) -> web.Response:
    camera_id = request.match_info["camera_id"]
    lock = _camera_lock(request.app, camera_id)
    if lock.locked():
        return json_response({"error": "Camera is busy with another operation"}, status=409)
    try:
        async with lock:
            return await _camera_command_locked(request)
    finally:
        request.app["status_hub"].refresh(camera_id)


async def _camera_command_locked(request: web.Request) -> web.Response:
    store: CameraStore = request.app["store"]
    session: ClientSession = request.app["session"]
    camera = store.get(request.match_info["camera_id"])
    if camera is None:
        raise web.HTTPNotFound(text="camera not found")
    payload = await request.json()
    command = payload.get("command")
    client = create_client(session, camera)
    trace: list[dict[str, Any]] = [{"step": "command", "command": command}]
    state = None
    try:
        if command == "wake":
            if _is_cohn_camera(camera):
                trace.append({"step": "ble_wake_start", "ble_address": camera["ble_address"]})
                wake_result = await run_ble_wake_helper(camera, OpenGoProError)
                trace.append({"step": "ble_wake_done", "result": wake_result})
                try:
                    trace.append(
                        {
                            "step": "http_ready_check",
                            "host": camera.get("http_host"),
                            "scheme": camera.get("http_scheme"),
                            "port": camera.get("http_port"),
                        }
                    )
                    state = await _wait_http_ready_short(client)
                    trace.append({"step": "http_ready_ok"})
                except OpenGoProError as http_err:
                    trace.append({"step": "http_ready_failed", "error": str(http_err)})
                    camera = await _recover_cohn_camera(store, camera, trace=trace)
                    client = create_client(session, camera)
                    trace.append(
                        {
                            "step": "http_ready_retry",
                            "host": camera.get("http_host"),
                            "scheme": camera.get("http_scheme"),
                            "port": camera.get("http_port"),
                        }
                    )
                    state = await _wait_http_ready_short(client)
                    trace.append({"step": "http_ready_retry_ok"})
            else:
                wake_result = await run_ble_wake_helper(
                    camera,
                    OpenGoProError,
                    enable_wifi=True,
                )
                trace.append({"step": "ble_enable_wifi_done", "result": wake_result})
                state = await _wait_http_ready_short(client)
            _ensure_keep_alive(request.app, camera["id"])
            trace.append({"step": "keep_alive_started"})
        elif command == "sleep":
            _stop_keep_alive(request.app, camera["id"])
            trace.append({"step": "keep_alive_stopped"})
            manager: PreviewManager = request.app["preview_manager"]
            await manager.stop(camera["id"])
            trace.append({"step": "preview_proxy_stopped"})
            await _run_http_command_with_recovery(
                request.app,
                store,
                camera,
                client,
                trace,
                "sleep",
                lambda: client.async_sleep(),
                lambda retry_client: retry_client.async_sleep(),
            )
            return json_response(
                {
                    "ok": True,
                    "state": {
                        "power": "standby",
                        "phase": "ble_standby",
                        "http_ready": False,
                        "preview_active": False,
                        "preview_url": None,
                        "recording": False,
                    },
                    "trace": trace,
                }
            )
        elif command == "shutter":
            await _run_http_command_with_recovery(
                request.app,
                store,
                camera,
                client,
                trace,
                "shutter",
                lambda active=bool(payload.get("active")): client.async_shutter(active),
                lambda retry_client, active=bool(payload.get("active")): retry_client.async_shutter(active),
            )
        elif command == "mode":
            await _run_http_command_with_recovery(
                request.app,
                store,
                camera,
                client,
                trace,
                "mode",
                lambda mode=str(payload["mode"]): client.async_set_mode(mode),
                lambda retry_client, mode=str(payload["mode"]): retry_client.async_set_mode(mode),
            )
        elif command == "preset":
            await _run_http_command_with_recovery(
                request.app,
                store,
                camera,
                client,
                trace,
                "preset",
                lambda preset=str(payload["preset"]): client.async_set_preset(preset),
                lambda retry_client, preset=str(payload["preset"]): retry_client.async_set_preset(preset),
            )
        elif command == "setting":
            await _run_http_command_with_recovery(
                request.app,
                store,
                camera,
                client,
                trace,
                "setting",
                lambda setting=str(payload["setting"]), option=str(payload["option"]): client.async_set_setting(setting, option),
                lambda retry_client, setting=str(payload["setting"]), option=str(payload["option"]): retry_client.async_set_setting(setting, option),
            )
        elif command == "keep_alive":
            await _run_http_command_with_recovery(
                request.app,
                store,
                camera,
                client,
                trace,
                "keep_alive",
                lambda: client.async_keep_alive(),
                lambda retry_client: retry_client.async_keep_alive(),
            )
        elif command == "start_preview":
            manager: PreviewManager = request.app["preview_manager"]
            await _stop_preview_http_best_effort(client, trace)
            try:
                preview = await manager.start(camera["id"], port=8554)
                client = await _start_preview_with_recovery(
                    request.app,
                    store,
                    camera,
                    client,
                    None,
                    trace,
                )
                trace.append({"step": "preview_default_port_ok", "port": 8554})
            except Exception as err:
                trace.append({"step": "preview_default_port_failed", **_error_trace(err)})
                await manager.stop(camera["id"])
                preview = await manager.start(camera["id"])
                try:
                    client = await _start_preview_with_recovery(
                        request.app,
                        store,
                        camera,
                        client,
                        preview.port,
                        trace,
                    )
                    trace.append({"step": "preview_custom_port_fallback_ok", "port": preview.port})
                except Exception:
                    await manager.stop(camera["id"])
                    raise
            trace.append(
                {
                    "step": "preview_started",
                    "port": preview.port,
                    "transport": "mpegts",
                    "stream_url": f"/api/cameras/{camera['id']}/preview.ts",
                }
            )
            if await manager.wait_for_datagram(camera["id"], timeout=5):
                trace.append(
                    {
                        "step": "preview_udp_ready",
                        "status": manager.status(camera["id"]),
                    }
                )
            else:
                trace.append(
                    {
                        "step": "preview_udp_timeout",
                        "status": manager.status(camera["id"]),
                    }
                )
            return json_response(
                {
                    "ok": True,
                    "preview": manager.status(camera["id"]),
                    "state": {"preview_active": True},
                    "trace": trace,
                }
            )
        elif command == "stop_preview":
            manager = request.app["preview_manager"]
            warning = None
            try:
                await _run_http_command_with_recovery(
                    request.app,
                    store,
                    camera,
                    client,
                    trace,
                    "preview_stop",
                    lambda: client.async_stop_preview(),
                    lambda retry_client: retry_client.async_stop_preview(),
                )
            except OpenGoProError as err:
                warning = str(err)
                trace.append({"step": "preview_stop_failed", **_error_trace(err)})
            finally:
                await manager.stop(camera["id"])
            trace.append({"step": "preview_stopped"})
            return json_response(
                {
                    "ok": True,
                    "warning": warning,
                    "preview": manager.status(camera["id"]),
                    "state": {"preview_active": False, "preview_url": None},
                    "trace": trace,
                }
            )
        else:
            return json_response({"error": f"未知命令: {command}"}, status=400)
    except OpenGoProError as err:
        trace.append({"step": "command_failed", **_error_trace(err)})
        return json_response({"error": str(err), "trace": trace}, status=502)
    except Exception as err:
        trace.append({"step": "command_failed", "error": f"{type(err).__name__}: {err}"})
        return json_response({"error": f"{type(err).__name__}: {err}", "trace": trace}, status=500)
    response = {"ok": True, "trace": trace}
    if state is not None:
        response["state"] = state
    return json_response(response)


def _client_for_request(request: web.Request) -> Any:
    store: CameraStore = request.app["store"]
    session: ClientSession = request.app["session"]
    camera = store.get(request.match_info["camera_id"])
    if camera is None:
        raise web.HTTPNotFound(text="camera not found")
    return create_client(session, camera)


def media_payload(camera_id: str, media: list[Any]) -> list[dict[str, Any]]:
    """Return media items with standalone proxy URLs for the shared UI."""
    payload = []
    for item in media:
        path = item.path
        quoted_path = quote(path, safe="")
        payload.append(
            {
                **asdict(item),
                "path": path,
                "url": f"/api/cameras/{camera_id}/media/file/{quoted_path}",
                "thumbnail": f"/api/cameras/{camera_id}/media/thumbnail/{quoted_path}",
            }
        )
    return payload


async def _proxy_camera_url(request: web.Request, *, thumbnail: bool) -> web.StreamResponse:
    """Proxy a camera media or thumbnail URL through standalone service."""
    client = _client_for_request(request)
    path = unquote(request.match_info["path"])
    url = client.media_thumbnail_url(path) if thumbnail else client.media_url(path)
    session: ClientSession = request.app["session"]
    response = None
    stream = None
    try:
        request_headers = {"Accept-Encoding": "identity"}
        for name in ("Range", "If-Range", "If-None-Match", "If-Modified-Since"):
            if name in request.headers:
                request_headers[name] = request.headers[name]
        response = await session.request(
            request.method,
            url,
            auth=client._http_auth(),
            ssl=client.verify_ssl,
            headers=request_headers,
            timeout=ClientTimeout(total=None, sock_connect=15, sock_read=60),
            auto_decompress=False,
        )
        if response.status >= 400 and response.status != 416:
            response.raise_for_status()
        headers = {
            name: response.headers[name]
            for name in ("Content-Length", "Content-Range", "Accept-Ranges", "Content-Encoding",
                         "ETag", "Last-Modified", "Cache-Control")
            if name in response.headers
        }
        content_type = response.headers.get("Content-Type", "application/octet-stream")
        if not thumbnail and content_type.split(";", 1)[0].strip().lower() in (
            "application/octet-stream", "application/download"
        ):
            content_type = client_module._guess_media_type(path)
        headers["Content-Type"] = content_type
        if not thumbnail:
            filename = path.rsplit("/", 1)[-1]
            headers["Content-Disposition"] = f"inline; filename*=UTF-8''{quote(filename, safe='')}"
        stream = web.StreamResponse(status=response.status, headers=headers)
        await stream.prepare(request)
        if request.method != "HEAD" and response.status != 304:
            async for chunk in response.content.iter_chunked(1024 * 64):
                await stream.write(chunk)
        await stream.write_eof()
        return stream
    except (ConnectionResetError, BrokenPipeError):
        # Browsers routinely cancel range requests when seeking or closing a player.
        if stream is not None:
            return stream
        raise
    except Exception as err:
        if stream is not None and stream.prepared:
            # Once response headers have been sent, an error body cannot replace them.
            if request.transport:
                request.transport.close()
            return stream
        return json_response(
            {
                "error": f"{type(err).__name__}: {err}",
                "url": url,
            },
            status=502,
        )
    finally:
        if response is not None:
            response.release()


def _is_cohn_camera(camera: dict[str, Any]) -> bool:
    """Return whether the camera uses HERO12+ COHN HTTPS/LAN mode."""
    return (
        camera.get("http_scheme") == "https"
        and camera.get("http_host")
        and camera.get("http_host") != "10.5.5.9"
    )


def _find_camera_by_ble(store: CameraStore, address: str) -> dict[str, Any] | None:
    """Find a configured camera by BLE address."""
    return next((camera for camera in store.list() if camera.get("ble_address") == address), None)


async def _wait_http_ready_short(client: Any) -> Any:
    """Wait briefly for HTTP after wake without making the web UI look frozen."""
    last_error: Exception | None = None
    for _ in range(6):
        try:
            snapshot = await client.async_get_state()
            client.phase = client_module.ConnectionPhase.HTTP_READY
            return snapshot
        except OpenGoProError as err:
            last_error = err
            await asyncio.sleep(2)
    raise OpenGoProError("BLE 唤醒已执行，但相机 HTTP API 尚未就绪") from last_error


async def _start_preview_with_recovery(
    app: web.Application,
    store: CameraStore,
    camera: dict[str, Any],
    client: Any,
    port: int | None,
    trace: list[dict[str, Any]],
) -> Any:
    """Start preview, refreshing COHN endpoint once when HTTP is stale."""
    try:
        await client.async_start_preview(port=port)
        trace.append(
            {
                "step": "preview_http_start_ok",
                "host": client.http_host,
                "port": port or 8554,
            }
        )
        return client
    except OpenGoProError as err:
        trace.append({"step": "preview_http_start_failed", **_error_trace(err)})
        if _http_status(err) == 409:
            trace.append({"step": "preview_conflict_stop_before_retry"})
            await _stop_preview_http_best_effort(client, trace)
            await asyncio.sleep(1)
            await client.async_start_preview(port=port)
            trace.append({"step": "preview_conflict_retry_ok", "port": port or 8554})
            return client
        if not _is_cohn_camera(camera):
            raise
        try:
            snapshot = await client.async_get_state()
            trace.append(
                {
                    "step": "preview_preflight_state_ok",
                    "phase": snapshot.phase.value,
                    "preview_active": snapshot.preview_active,
                    "mode": snapshot.current_mode,
                }
            )
        except OpenGoProError as state_err:
            trace.append({"step": "preview_preflight_state_failed", **_error_trace(state_err)})
        raise


async def _stop_preview_http_best_effort(client: Any, trace: list[dict[str, Any]]) -> None:
    """Stop camera-side preview if it is already running."""
    try:
        await client.async_stop_preview()
        trace.append({"step": "preview_stop_before_start_ok"})
    except OpenGoProError as err:
        trace.append({"step": "preview_stop_before_start_ignored", **_error_trace(err)})


async def _run_http_command_with_recovery(
    app: web.Application,
    store: CameraStore,
    camera: dict[str, Any],
    client: Any,
    trace: list[dict[str, Any]],
    label: str,
    action: Any,
    retry_action: Any,
    *,
    allow_recovery: bool = False,
) -> None:
    """Run an HTTP command, optionally refreshing COHN endpoint once when stale."""
    try:
        await action()
        trace.append({"step": f"{label}_http_ok"})
        return
    except OpenGoProError as err:
        trace.append({"step": f"{label}_http_failed", **_error_trace(err)})
        if _http_status(err) == 403:
            raise
        if not allow_recovery or not _is_cohn_camera(camera):
            raise
    recovered = await _recover_cohn_camera(store, camera, trace=trace)
    retry_client = create_client(app["session"], recovered)
    trace.append(
        {
            "step": f"{label}_http_retry",
            "host": recovered.get("http_host"),
            "scheme": recovered.get("http_scheme"),
            "port": recovered.get("http_port"),
        }
    )
    await retry_action(retry_client)
    trace.append({"step": f"{label}_http_retry_ok"})


def _error_trace(err: Exception) -> dict[str, Any]:
    """Return structured error details for UI trace logs."""
    cause = err.__cause__
    return {
        "error": str(err),
        "error_type": type(err).__name__,
        "cause_type": type(cause).__name__ if cause else None,
        "cause": repr(cause) if cause else None,
        "http_status": _http_status(err),
        "response_body": getattr(err, "payload", None),
    }


def _http_status(err: Exception) -> int | None:
    """Return an HTTP response status from an aiohttp-backed exception."""
    direct_status = getattr(err, "status", None)
    if isinstance(direct_status, int):
        return direct_status
    cause = err.__cause__
    status = getattr(cause, "status", None)
    return int(status) if isinstance(status, int) else None


def _ensure_keep_alive(app: web.Application, camera_id: str) -> None:
    """Start a standalone KeepAlive task for a camera."""
    tasks: dict[str, asyncio.Task[None]] = app["keepalive_tasks"]
    task = tasks.get(camera_id)
    if task and not task.done():
        return
    tasks[camera_id] = asyncio.create_task(_keep_alive_loop(app, camera_id))


def _stop_keep_alive(app: web.Application, camera_id: str) -> None:
    """Stop a standalone KeepAlive task for a camera."""
    tasks: dict[str, asyncio.Task[None]] = app["keepalive_tasks"]
    task = tasks.pop(camera_id, None)
    if task:
        task.cancel()


async def _keep_alive_loop(app: web.Application, camera_id: str) -> None:
    """Keep a woken camera alive until HTTP becomes unavailable or sleep is requested."""
    interval = float(app["keepalive_interval"])
    store: CameraStore = app["store"]
    session: ClientSession = app["session"]
    try:
        while True:
            await asyncio.sleep(interval)
            camera = store.get(camera_id)
            if camera is None:
                return
            try:
                await create_client(session, camera).async_keep_alive()
            except OpenGoProError:
                return
    except asyncio.CancelledError:
        raise
    finally:
        app["keepalive_tasks"].pop(camera_id, None)


async def _wake_schedule_loop(app: web.Application) -> None:
    """Run daily guard and target wake events for configured cameras."""
    while True:
        try:
            await _run_due_wake_schedules(app)
        except asyncio.CancelledError:
            raise
        except Exception:
            pass
        await asyncio.sleep(60)


async def _run_due_wake_schedules(app: web.Application) -> None:
    store: CameraStore = app["store"]
    now = datetime.now().replace(second=0, microsecond=0)
    for camera in store.list():
        schedule = camera.get("wake_schedule")
        if not isinstance(schedule, dict) or not schedule.get("enabled"):
            continue
        for event in _due_wake_events(schedule, now):
            await _run_wake_schedule_event(app, camera, event, now.date())


async def _run_wake_schedule_event(
    app: web.Application,
    camera: dict[str, Any],
    event: str,
    today: date,
) -> None:
    lock = _camera_lock(app, camera["id"])
    if lock.locked():
        return
    async with lock:
        await _run_wake_schedule_event_locked(app, camera, event, today)


async def _run_wake_schedule_event_locked(
    app: web.Application,
    camera: dict[str, Any],
    event: str,
    today: date,
) -> None:
    store: CameraStore = app["store"]
    camera_id = camera["id"]
    schedule = dict(camera.get("wake_schedule") or {})
    try:
        if event == "guard":
            wake_result = await run_ble_wake_helper(camera, OpenGoProError)
            await asyncio.sleep(3)
            sleep_result = await run_ble_sleep_helper(camera, OpenGoProError)
            event_payload = {
                "event": "guard",
                "wake": wake_result,
                "sleep": sleep_result,
                "ran_at": datetime.now().isoformat(timespec="seconds"),
            }
            schedule["last_guard_date"] = today.isoformat()
        else:
            session: ClientSession = app["session"]
            client = create_client(session, camera)
            wake_result = await run_ble_wake_helper(camera, OpenGoProError, enable_wifi=True)
            await _wait_http_ready_short(client)
            _ensure_keep_alive(app, camera_id)
            event_payload = {
                "event": "target",
                "wake": wake_result,
                "ran_at": datetime.now().isoformat(timespec="seconds"),
            }
            schedule["last_target_date"] = today.isoformat()
        schedule["last_event"] = event_payload
        schedule["last_error"] = None
    except Exception as err:
        schedule["last_error"] = {
            "event": event,
            "ran_at": datetime.now().isoformat(timespec="seconds"),
            **_error_trace(err),
        }
    store.update(camera_id, {"wake_schedule": schedule})


def _due_wake_events(schedule: dict[str, Any], now: datetime) -> list[str]:
    """Return schedule events due at the current minute."""
    target_time = _parse_hhmm(schedule.get("target_time"))
    guard_lead_hours = _coerce_guard_lead_hours(
        schedule.get("guard_lead_hours", DEFAULT_GUARD_LEAD_HOURS)
    )
    today = now.date()
    events: list[str] = []
    guard_at = datetime.combine(today, _guard_time(target_time, guard_lead_hours))
    target_at = datetime.combine(today, target_time)
    if _minute_due(now, guard_at) and schedule.get("last_guard_date") != today.isoformat():
        events.append("guard")
    if _minute_due(now, target_at) and schedule.get("last_target_date") != today.isoformat():
        events.append("target")
    return events


def _minute_due(now: datetime, scheduled_at: datetime) -> bool:
    return scheduled_at <= now < scheduled_at + timedelta(minutes=1)


def _parse_hhmm(value: Any) -> time:
    if not isinstance(value, str):
        raise web.HTTPBadRequest(text="target_time must be HH:MM")
    try:
        hour_text, minute_text = value.strip().split(":", 1)
        return time(hour=int(hour_text), minute=int(minute_text))
    except (TypeError, ValueError) as err:
        raise web.HTTPBadRequest(text="target_time must be HH:MM") from err


def _format_hhmm(value: time) -> str:
    return f"{value.hour:02d}:{value.minute:02d}"


def _guard_time(target_time: time, guard_lead_hours: float) -> time:
    target = datetime.combine(date(2000, 1, 2), target_time)
    return (target - timedelta(hours=guard_lead_hours)).time().replace(second=0, microsecond=0)


def _coerce_guard_lead_hours(value: Any) -> float:
    try:
        guard_lead_hours = float(value)
    except (TypeError, ValueError) as err:
        raise web.HTTPBadRequest(text="guard_lead_hours must be a number") from err
    if not MIN_GUARD_LEAD_HOURS <= guard_lead_hours <= MAX_GUARD_LEAD_HOURS:
        raise web.HTTPBadRequest(
            text=f"guard_lead_hours must be between {MIN_GUARD_LEAD_HOURS} and {MAX_GUARD_LEAD_HOURS}"
        )
    return guard_lead_hours


async def _recover_cohn_camera(
    store: CameraStore,
    camera: dict[str, Any],
    *,
    trace: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Refresh COHN IP/credentials over BLE and update the camera store."""
    if trace is not None:
        trace.append({"step": "cohn_status_start", "ble_address": camera["ble_address"]})
    credentials = await _run_cohn_status_helper(camera)
    if trace is not None:
        trace.append(
            {
                "step": "cohn_status_done",
                "ip_address": credentials.get("ip_address"),
                "username": credentials.get("username"),
                "ssid": credentials.get("ssid"),
                "mac_address": credentials.get("mac_address"),
            }
        )
    ip_address = credentials.get("ip_address")
    username = credentials.get("username")
    password = credentials.get("password")
    if not ip_address or not username or not password:
        raise OpenGoProError(f"COHN 状态未返回完整连接信息: {credentials}")
    updated = store.update(
        camera["id"],
        {
            "http_scheme": "https",
            "http_host": ip_address,
            "http_port": 443,
            "http_username": username,
            "http_password": password,
            "cohn_ssid": credentials.get("ssid"),
            "cohn_mac_address": credentials.get("mac_address"),
            "verify_ssl": camera.get("verify_ssl", False),
        },
    )
    if updated is None:
        raise OpenGoProError("COHN 状态恢复成功，但相机配置更新失败")
    if trace is not None:
        trace.append({"step": "camera_store_updated", "host": updated.get("http_host")})
    return updated


async def _run_cohn_status_helper(camera: dict[str, Any]) -> dict[str, Any]:
    """Read COHN status through a short-lived helper process."""
    root = Path(__file__).resolve().parent
    payload = await run_ble_worker(
        {
            "command": "cohn_status",
            "ble_address": camera["ble_address"],
        },
        timeout=60,
        cwd=root,
        label="COHN 状态 worker",
        error_cls=OpenGoProError,
    )
    credentials = payload.get("credentials")
    if payload.get("error"):
        raise OpenGoProError(
            f"COHN 状态读取失败: {payload['error']} "
            f"worker={root / 'ble_worker.py'} python={sys.executable}"
        )
    if not isinstance(credentials, dict):
        raise OpenGoProError(f"COHN 状态 helper 未返回 credentials: {payload}")
    return credentials


async def _optional_json(request: web.Request) -> dict[str, Any]:
    if request.can_read_body:
        return await request.json()
    return {}


def _preset_inventory(payload: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    groups = payload.get("presetGroupArray") or payload.get("preset_groups") or payload.get("groups") or payload.get("presets") or []
    result = []
    for group in groups:
        if not isinstance(group, dict):
            continue
        group_id = str(group.get("id", group.get("group_id", group.get("preset_group", ""))))
        modes = {"1000": "video", "1001": "photo", "1002": "timelapse",
                 "PRESET_GROUP_ID_VIDEO": "video", "PRESET_GROUP_ID_PHOTO": "photo",
                 "PRESET_GROUP_ID_TIMELAPSE": "timelapse"}
        mode = modes.get(group_id)
        if mode is None:
            title = (group.get("customName") or group.get("title") or group.get("name") or
                     group.get("display_name") or group.get("label") or group.get("titleId") or "")
            title = str(title).lower().replace("_", " ")
            mode = next((value for token, value in (("video", "video"), ("photo", "photo"), ("time", "timelapse"))
                         if token in title), "")
        presets = group.get("presetArray") or group.get("presets") or group.get("preset") or group.get("items") or []
        for preset in presets:
            if isinstance(preset, dict):
                result.append((mode, preset))
    return result


def _preset_id(preset: dict[str, Any]) -> str:
    return str(preset.get("id", preset.get("preset_id", preset.get("preset", ""))))


def _preset_identity(preset: dict[str, Any]) -> str:
    title = preset.get("titleId", preset.get("title", preset.get("name", "")))
    custom = preset.get("customName", "")
    return f"{title}|{custom}" if custom else str(title if title is not None else "")


def _find_schedule_preset(payload: dict[str, Any], schedule: dict[str, Any]) -> dict[str, Any]:
    for mode, preset in _preset_inventory(payload):
        if mode == schedule["mode"] and _preset_id(preset) == schedule["preset"]:
            identity = _preset_identity(preset)
            if schedule.get("preset_identity") and identity != schedule["preset_identity"]:
                raise ValueError("Preset identity changed; edit the schedule")
            available = preset.get("settingArray", preset.get("settings", preset.get("setting_values", [])))
            ids = {str(s.get("id", s.get("setting_id", s.get("setting", "")))) for s in available if isinstance(s, dict)}
            if schedule["settings"] and not set(schedule["settings"]).issubset(ids):
                raise ValueError("A requested setting is not available in the selected preset")
            return preset
    raise ValueError("Preset is unavailable for the selected mode")


def _schedule_public(app: web.Application, item: dict[str, Any]) -> dict[str, Any]:
    result = dict(item)
    result.pop("processed_dates", None)
    result.pop("cron_cursor", None)
    candidate = next_occurrence(item, now_local()) if item["enabled"] else None
    result["next_at"] = candidate[1].isoformat() if candidate and candidate[1] else None
    result["next_unavailable_date"] = candidate[0].isoformat() if candidate and candidate[1] is None else None
    records = [r for r in app["schedule_store"].data["history"] if r["schedule_id"] == item["id"]]
    result["last_run"] = records[-1] if records else None
    result["wake_guard"] = app["schedule_store"].data.get("wake_guards", {}).get(item["camera_id"])
    return result


async def schedules_list(request: web.Request) -> web.Response:
    return json_response({"schedules": [_schedule_public(request.app, s) for s in request.app["schedule_store"].data["schedules"]],
                          "timezone": str(local_zone())})


async def schedule_history(request: web.Request) -> web.Response:
    store = request.app["schedule_store"]
    if not store.get(request.match_info["schedule_id"]):
        raise web.HTTPNotFound(text="schedule not found")
    return json_response({"history": [r for r in reversed(store.data["history"]) if r["schedule_id"] == request.match_info["schedule_id"]]})


def _schedule_running(store: ScheduleStore, schedule_id: str) -> bool:
    return any(r["schedule_id"] == schedule_id and r["status"] in ("preparing", "capturing") for r in store.data["history"])


async def _stop_unused_wake_guard(app: web.Application, camera_id: str) -> None:
    store: ScheduleStore = app["schedule_store"]
    if any(s.get("enabled") and s.get("camera_id") == camera_id for s in store.data["schedules"]):
        return
    task = app.get("guard_tasks", {}).get(camera_id)
    if task and not task.done():
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
    guard = store.data.get("wake_guards", {}).get(camera_id)
    if guard:
        guard.update(status="disabled", next_at=None)
        store.save()


async def schedule_write(request: web.Request) -> web.Response:
    app = request.app
    store: ScheduleStore = app["schedule_store"]
    item = store.get(request.match_info.get("schedule_id", ""))
    if request.method != "POST" and not item:
        raise web.HTTPNotFound(text="schedule not found")
    if item and _schedule_running(store, item["id"]):
        return json_response({"error": "Schedule is currently running"}, status=409)
    payload = await request.json()
    if item and _schedule_running(store, item["id"]):
        return json_response({"error": "Schedule is currently running"}, status=409)
    if request.method == "PATCH":
        if not isinstance(payload, dict) or set(payload) != {"enabled"} or not isinstance(payload["enabled"], bool):
            return json_response({"error": "Expected enabled boolean"}, status=400)
        if payload["enabled"] and item["repeat"] == "once":
            probe = {**item, "created_at": now_local().isoformat(), "processed_dates": []}
            if not next_occurrence(probe, now_local()):
                return json_response({"error": "The scheduled time must be in the future"}, status=400)
        item["enabled"] = payload["enabled"]
        # Re-enabling never catches up on occurrences while disabled.
        if item["enabled"]:
            item["created_at"] = now_local().isoformat()
            item["processed_dates"] = []
            item.pop("cron_cursor", None)
        store.save()
        if not item["enabled"]:
            await _stop_unused_wake_guard(app, item["camera_id"])
        return json_response({"schedule": _schedule_public(app, item)})
    camera = app["store"].get(str(payload.get("camera_id", ""))) if isinstance(payload, dict) else None
    try:
        values = validate_schedule(payload, bool(camera))
        client = create_client(app["session"], camera)
        inventory = await client.async_get_preset_status()
        preset = _find_schedule_preset(inventory, values)
        values["preset_identity"] = _preset_identity(preset)
        if not values["preset_identity"]:
            raise ValueError("Camera did not provide a stable preset identity")
        probe = {**values, "created_at": now_local().isoformat(), "processed_dates": []}
        if not next_occurrence(probe, now_local()):
            raise ValueError("The scheduled time must be in the future")
    except (ValueError, OpenGoProError) as err:
        return json_response({"error": str(err)}, status=400 if isinstance(err, ValueError) else 502)
    if item:
        if not store.get(item["id"]):
            raise web.HTTPNotFound(text="schedule not found")
        if _schedule_running(store, item["id"]):
            return json_response({"error": "Schedule is currently running"}, status=409)
        previous_camera = item["camera_id"]
        store.update(item, values)
        await _stop_unused_wake_guard(app, previous_camera)
    else:
        item = store.create(values)
    return json_response({"schedule": _schedule_public(app, item)}, status=201 if request.method == "POST" else 200)


async def schedule_delete(request: web.Request) -> web.Response:
    store = request.app["schedule_store"]
    item = store.get(request.match_info["schedule_id"])
    if not item:
        raise web.HTTPNotFound(text="schedule not found")
    if _schedule_running(store, item["id"]):
        return json_response({"error": "Schedule is currently running"}, status=409)
    store.data["schedules"].remove(item)
    store.data["history"] = [r for r in store.data["history"] if r["schedule_id"] != item["id"]]
    store.save()
    await _stop_unused_wake_guard(request.app, item["camera_id"])
    return json_response({"ok": True})


async def _schedule_connect(app: web.Application, camera: dict[str, Any]):
    client = create_client(app["session"], camera)
    try:
        snapshot = await client.async_get_state()
    except OpenGoProError:
        await run_ble_wake_helper(camera, OpenGoProError, enable_wifi=not _is_cohn_camera(camera))
        try:
            snapshot = await _wait_http_ready_short(client)
        except OpenGoProError:
            if not _is_cohn_camera(camera):
                raise
            camera = await _recover_cohn_camera(app["store"], camera)
            client = create_client(app["session"], camera)
            snapshot = await _wait_http_ready_short(client)
    return camera, client, snapshot


def _snapshot_busy(snapshot: Any) -> bool:
    status = snapshot.raw_state.get("status", {})
    if "10" not in status and "recording" not in status:
        raise RuntimeError("Camera did not report its capture state")
    value = status.get("8", status.get("busy", 0))
    return bool(snapshot.recording or value not in (None, False, 0, "0", "false"))


async def _schedule_idle(client: Any, timeout: float = 15) -> Any:
    deadline = asyncio.get_running_loop().time() + timeout
    while True:
        snapshot = await client.async_get_state()
        if not _snapshot_busy(snapshot):
            return snapshot
        if asyncio.get_running_loop().time() >= deadline:
            raise RuntimeError("Camera did not become idle")
        await asyncio.sleep(1)


async def _schedule_sleep(app: web.Application, camera_id: str, client: Any) -> None:
    _stop_keep_alive(app, camera_id)
    await app["preview_manager"].stop(camera_id)
    await client.async_sleep()


async def _execute_schedule(app: web.Application, item: dict[str, Any], record: dict[str, Any], target: datetime) -> None:
    store: ScheduleStore = app["schedule_store"]
    camera_id = item["camera_id"]
    lock = _camera_lock(app, camera_id)
    client = None
    controlled = False
    shutter_uncertain = False
    if lock.locked():
        record.update(status="skipped", error="Camera is busy with another operation", finished_at=now_local().isoformat())
        store.save()
        return
    async with lock:
        try:
            camera = app["store"].get(camera_id)
            if not camera:
                raise RuntimeError("Camera no longer exists")
            camera, client, snapshot = await _schedule_connect(app, camera)
            if _snapshot_busy(snapshot):
                record.update(status="skipped", error="Camera is already recording or busy", finished_at=now_local().isoformat())
                return
            controlled = True
            record["camera_prepared"] = True
            store.save()
            _ensure_keep_alive(app, camera_id)
            _find_schedule_preset(await client.async_get_preset_status(), item)
            await client.async_set_preset(item["preset"])
            await _schedule_idle(client)
            for setting, option in item["settings"].items():
                await client.async_set_setting(setting, option)
                snapshot = await _schedule_idle(client)
                actual = snapshot.settings.get(setting, snapshot.settings.get(int(setting)))
                if actual is None or str(actual) != option:
                    raise RuntimeError(f"Camera did not confirm setting {setting}={option}")
            delay = target.timestamp() - now_local().timestamp()
            if delay < -5:
                raise RuntimeError("Camera preparation missed the scheduled time")
            if delay > 0:
                await asyncio.sleep(delay)
            if _snapshot_busy(await client.async_get_state()):
                controlled = False
                record.update(status="skipped", error="Camera became busy before capture", finished_at=now_local().isoformat())
                _stop_keep_alive(app, camera_id)
                return
            record.update(status="capturing", shutter_sent=True, started_at=now_local().isoformat())
            store.save()  # Persist before the non-idempotent shutter command.
            shutter_uncertain = True
            started = asyncio.get_running_loop().time()
            await client.async_shutter(True)
            if item["mode"] == "photo":
                await asyncio.sleep(2)
                await _schedule_idle(client, timeout=30)
                shutter_uncertain = False
            else:
                deadline = started + min(10, item["duration_seconds"])
                while True:
                    snapshot = await client.async_get_state()
                    _snapshot_busy(snapshot)  # Reject an unknown capture state.
                    if snapshot.recording:
                        break
                    if asyncio.get_running_loop().time() >= deadline:
                        raise RuntimeError("Camera did not confirm that capture started")
                    await asyncio.sleep(0.5)
                await asyncio.sleep(max(0, started + item["duration_seconds"] - asyncio.get_running_loop().time()))
                await client.async_shutter(False)
                await _schedule_idle(client, timeout=30)
                shutter_uncertain = False
            await _schedule_sleep(app, camera_id, client)
            controlled = False
            record.update(status="success", finished_at=now_local().isoformat())
        except asyncio.CancelledError:
            # Keep the durable in-progress state for restart recovery.
            raise
        except Exception as err:
            record.update(status="uncertain" if shutter_uncertain else "failed", error=str(err), finished_at=now_local().isoformat())
            if controlled and client and not shutter_uncertain:
                try:
                    await _schedule_sleep(app, camera_id, client)
                except Exception as sleep_error:
                    record["error"] += f"; sleep failed: {sleep_error}"
            elif shutter_uncertain:
                _stop_keep_alive(app, camera_id)
                record["needs_recovery"] = item["mode"] != "photo"
                record["error"] += "; check the camera: capture may still be active"
        finally:
            store.save()


async def _recover_interrupted_schedule(app: web.Application, record: dict[str, Any]) -> None:
    store: ScheduleStore = app["schedule_store"]
    camera = app["store"].get(record["camera_id"])
    lock = _camera_lock(app, record["camera_id"])
    async with lock:
        try:
            if record.get("shutter_sent") and record.get("mode") != "photo":
                if not camera:
                    raise RuntimeError("Camera no longer exists")
                _, client, _ = await _schedule_connect(app, camera)
                await client.async_shutter(False)
                await _schedule_idle(client, timeout=30)
                await _schedule_sleep(app, camera["id"], client)
                record["error"] = "Service restarted during capture; camera stopped"
            elif record.get("camera_prepared") and not record.get("shutter_sent") and camera:
                client = create_client(app["session"], camera)
                try:
                    snapshot = await client.async_get_state()
                except OpenGoProError:
                    record["error"] = "Service restarted during preparation; camera is unreachable"
                else:
                    if _snapshot_busy(snapshot):
                        raise RuntimeError("Camera is busy; it was not put to sleep")
                    await _schedule_sleep(app, camera["id"], client)
                    record["error"] = "Service restarted during preparation; camera put to sleep"
            else:
                record["error"] = "Service restarted; capture outcome may be unknown"
            record["status"] = "interrupted"
        except Exception as err:
            record.update(status="uncertain", error=f"Recovery failed; check camera: {err}")
        record["finished_at"] = now_local().isoformat()
        record["needs_recovery"] = record["status"] == "uncertain"
        store.save()


WAKE_GUARD_INTERVAL = timedelta(hours=6)
WAKE_GUARD_RETRY = timedelta(minutes=15)
WAKE_GUARD_DEFER = timedelta(minutes=5)


def _guard_deadline(now: datetime, delay: timedelta) -> datetime:
    return datetime.fromtimestamp(now.timestamp() + delay.total_seconds(), tz=now.tzinfo)


def _guard_has_capture_conflict(store: ScheduleStore, camera_id: str, now: datetime) -> bool:
    if any(r.get("camera_id") == camera_id and
           (r.get("status") in ("preparing", "capturing") or r.get("needs_recovery"))
           for r in store.data["history"]):
        return True
    for item in store.data["schedules"]:
        if item.get("enabled") and item.get("camera_id") == camera_id:
            candidate = next_occurrence(item, now)
            if candidate and candidate[1] and candidate[1].timestamp() <= _guard_deadline(now, WAKE_GUARD_DEFER).timestamp():
                return True
    return False


async def _execute_wake_guard(app: web.Application, camera_id: str) -> None:
    store: ScheduleStore = app["schedule_store"]
    guard = store.data["wake_guards"][camera_id]
    now = now_local()
    lock = _camera_lock(app, camera_id)
    if lock.locked() or _guard_has_capture_conflict(store, camera_id, now):
        guard.update(status="deferred", next_at=_guard_deadline(now, WAKE_GUARD_DEFER).isoformat())
        store.save()
        return
    async with lock:
        if not any(item.get("enabled") and item.get("camera_id") == camera_id
                   for item in store.data["schedules"]):
            guard.update(status="disabled", next_at=None)
            store.save()
            return
        if _guard_has_capture_conflict(store, camera_id, now_local()):
            guard.update(status="deferred", next_at=_guard_deadline(now_local(), WAKE_GUARD_DEFER).isoformat())
            store.save()
            return
        try:
            camera = app["store"].get(camera_id)
            if not camera:
                raise OpenGoProError("Camera not found")
            result = await run_ble_worker(
                {"command": "refresh_wake_window", "ble_address": camera["ble_address"]},
                timeout=80, cwd=Path(__file__).resolve().parent,
                label="BLE 定期唤醒 worker", error_cls=OpenGoProError,
            )
            status = result.get("status", "failed")
            error = result.get("error")
            finished = now_local()
            guard.update(status=status, last_attempt=finished.isoformat(), error=error,
                         next_at=_guard_deadline(finished, WAKE_GUARD_INTERVAL if status == "success" else WAKE_GUARD_RETRY).isoformat())
            if status == "success":
                guard["last_success"] = finished.isoformat()
        except asyncio.CancelledError:
            guard.update(status="deferred", next_at=_guard_deadline(now_local(), WAKE_GUARD_DEFER).isoformat())
            raise
        except Exception as err:
            finished = now_local()
            guard.update(status="failed", last_attempt=finished.isoformat(),
                         error=_error_trace(err), next_at=_guard_deadline(finished, WAKE_GUARD_RETRY).isoformat())
        finally:
            store.save()
            if app.get("status_hub"):
                app["status_hub"].refresh(camera_id)


async def _wake_guard_cycle(app: web.Application, now: datetime) -> None:
    store: ScheduleStore = app["schedule_store"]
    guards = store.data["wake_guards"]
    tasks = app["guard_tasks"]
    enabled = {item["camera_id"] for item in store.data["schedules"] if item.get("enabled")}
    for camera_id in enabled:
        if camera_id in tasks and not tasks[camera_id].done():
            continue
        guard = guards.setdefault(camera_id, {})
        next_at = guard.get("next_at")
        try:
            due = not next_at or datetime.fromisoformat(next_at).timestamp() <= now.timestamp()
        except (ValueError, TypeError, OverflowError):
            due = True
        if not due:
            continue
        # Persist a retry deadline before launching so restart cannot cause a tight retry loop.
        guard.update(status="pending", next_at=_guard_deadline(now, WAKE_GUARD_RETRY).isoformat())
        store.save()
        task = asyncio.create_task(_execute_wake_guard(app, camera_id))
        tasks[camera_id] = task
        task.add_done_callback(lambda completed, key=camera_id: tasks.pop(key, None) if tasks.get(key) is completed else None)


async def _wake_guard_loop(app: web.Application) -> None:
    while True:
        try:
            await _wake_guard_cycle(app, now_local())
        except asyncio.CancelledError:
            raise
        except Exception:
            import logging
            logging.exception("Periodic wake guard failed")
        await asyncio.sleep(60)


async def _capture_schedule_loop(app: web.Application) -> None:
    store: ScheduleStore = app["schedule_store"]
    # Recovery completes before new tasks are dispatched.
    for record in list(store.data["history"]):
        if record["status"] in ("preparing", "capturing") or record.get("needs_recovery"):
            await _recover_interrupted_schedule(app, record)
    while True:
        try:
            now = now_local()
            for item in list(store.data["schedules"]):
                if not item["enabled"]:
                    continue
                if item.get("repeat") == "cron":
                    cutoff = datetime.fromtimestamp(now.timestamp() - CRON_LOOKBACK.total_seconds(), tz=now.tzinfo)
                    skipped = cron_missed_before(item, cutoff)
                    if skipped:
                        store.history(item, skipped.date(), skipped, "missed",
                                      "Older missed cron occurrences were skipped after downtime")
                for _ in range(371):
                    candidate = next_occurrence(item, now)
                    if not candidate or not item["enabled"]:
                        break
                    day, target = candidate
                    marker = target or datetime.combine(day, time(23, 59), tzinfo=local_zone())
                    delta = marker.timestamp() - now.timestamp()
                    if target is None and delta <= 0:
                        store.history(item, day, None, "skipped", "No sunset or local time does not exist")
                    elif target and delta < -5:
                        store.history(item, day, target, "missed", "Scheduled time was missed")
                    elif target and delta <= 120:
                        guard_task = app.get("guard_tasks", {}).get(item["camera_id"])
                        if guard_task and not guard_task.done():
                            guard_task.cancel()
                            await asyncio.gather(guard_task, return_exceptions=True)
                        camera_lock = app.get("camera_locks", {}).get(item["camera_id"])
                        if delta > 0 and camera_lock and camera_lock.locked():
                            # Another operation may finish before the target time.
                            break
                        record = store.history(item, day, target, "preparing")
                        task = asyncio.create_task(_execute_schedule(app, dict(item), record, target))
                        app["capture_tasks"].add(task)
                        task.add_done_callback(app["capture_tasks"].discard)
                        break
                    else:
                        break
        except asyncio.CancelledError:
            raise
        except Exception:
            import logging
            logging.exception("Capture scheduler failed")
        await asyncio.sleep(1)


async def create_app(data_path: Path) -> web.Application:
    app = web.Application()
    app["store"] = CameraStore(data_path)
    app["session"] = ClientSession()
    app["keepalive_tasks"] = {}
    app["keepalive_interval"] = 3.0
    app["camera_locks"] = {}
    app["status_hub"] = CameraStatusHub(lambda camera_id: _sample_camera_status(app, camera_id))
    app["schedule_store"] = ScheduleStore(data_path.with_name("capture-schedules.json"))
    app["capture_tasks"] = set()
    app["guard_tasks"] = {}
    app["preview_manager"] = PreviewManager(OpenGoProError)
    app["capture_schedule_task"] = asyncio.create_task(_capture_schedule_loop(app))
    app["guard_task"] = asyncio.create_task(_wake_guard_loop(app))
    app["wake_schedule_task"] = asyncio.create_task(_wake_schedule_loop(app))
    app.router.add_get("/", index)
    app.router.add_get("/assets/opengopro-console.js", console_asset)
    app.router.add_get("/assets/opengopro-console-styles.js", console_styles_asset)
    app.router.add_get("/assets/mpegts.min.js", mpegts_asset)
    app.router.add_get("/api/health", health)
    app.router.add_get("/api/cameras", list_cameras)
    app.router.add_get("/api/schedules", schedules_list)
    app.router.add_post("/api/schedules", schedule_write)
    app.router.add_put("/api/schedules/{schedule_id}", schedule_write)
    app.router.add_patch("/api/schedules/{schedule_id}", schedule_write)
    app.router.add_delete("/api/schedules/{schedule_id}", schedule_delete)
    app.router.add_get("/api/schedules/{schedule_id}/history", schedule_history)
    app.router.add_post("/api/cameras", add_camera)
    app.router.add_post("/api/scan", scan_ble)
    app.router.add_post("/api/cohn/access-points", guarded_scan_access_points)
    app.router.add_post("/api/cohn/provision", guarded_provision_cohn)
    app.router.add_post("/api/cohn/provision/stream", guarded_provision_cohn_stream)
    app.router.add_get("/api/cameras/{camera_id}/state", camera_state)
    app.router.add_get("/api/cameras/{camera_id}/status", camera_status_snapshot)
    app.router.add_get("/api/cameras/{camera_id}/events", camera_status_stream)
    app.router.add_get("/api/cameras/{camera_id}/presence", camera_presence)
    app.router.add_post("/api/cameras/{camera_id}/wake-schedule", camera_wake_schedule)
    app.router.add_get("/api/cameras/{camera_id}/media", camera_media)
    app.router.add_delete("/api/cameras/{camera_id}/media", camera_media_delete)
    app.router.add_get("/api/cameras/{camera_id}/presets", camera_presets)
    app.router.add_get("/api/cameras/{camera_id}/media/file/{path:.+}", camera_media_file)
    app.router.add_get(
        "/api/cameras/{camera_id}/media/thumbnail/{path:.+}",
        camera_media_thumbnail,
    )
    app.router.add_get("/api/cameras/{camera_id}/preview/status", camera_preview_status)
    app.router.add_get("/api/cameras/{camera_id}/preview.ts", camera_preview_stream)
    app.router.add_post("/api/cameras/{camera_id}/command", camera_command)

    async def close_session(app: web.Application) -> None:
        await app["status_hub"].close()
        app["capture_schedule_task"].cancel()
        app["guard_task"].cancel()
        app["wake_schedule_task"].cancel()
        for task in list(app["capture_tasks"]):
            task.cancel()
        for task in list(app["guard_tasks"].values()):
            task.cancel()
        await asyncio.gather(app["capture_schedule_task"], app["wake_schedule_task"], app["guard_task"],
                             *app["capture_tasks"], *app["guard_tasks"].values(), return_exceptions=True)
        for task in list(app["keepalive_tasks"].values()):
            task.cancel()
        if app["keepalive_tasks"]:
            await asyncio.gather(*app["keepalive_tasks"].values(), return_exceptions=True)
        await app["preview_manager"].close()
        await app["session"].close()

    app.on_cleanup.append(close_session)
    return app


def main() -> None:
    parser = argparse.ArgumentParser(description="gopro-ctl service")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--data", type=Path, default=Path("data/cameras.json"))
    args = parser.parse_args()
    web.run_app(create_app(args.data), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
