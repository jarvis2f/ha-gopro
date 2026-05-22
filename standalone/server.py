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

try:
    from .ble_process import (
        run_ble_sleep_helper,
        run_ble_wake_helper,
        run_ble_worker,
        run_ble_worker_stream,
    )
    from .opengopro_loader import load_client_module
    from .preview import PreviewManager
    from .store import CameraStore
except ImportError:  # pragma: no cover - direct script execution
    from ble_process import (
        run_ble_sleep_helper,
        run_ble_wake_helper,
        run_ble_worker,
        run_ble_worker_stream,
    )
    from opengopro_loader import load_client_module
    from preview import PreviewManager
    from store import CameraStore

client_module = load_client_module()
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
                Path(__file__).resolve().parents[1] / "standalone" / "ble_worker.py"
            ),
        }
    )


async def index(request: web.Request) -> web.FileResponse:
    return web.FileResponse(Path(__file__).parent / "static" / "index.html")


async def console_asset(request: web.Request) -> web.FileResponse:
    root = Path(__file__).resolve().parents[1]
    return web.FileResponse(
        root / "custom_components" / "opengopro" / "frontend" / "opengopro-console.js"
    )


async def console_styles_asset(request: web.Request) -> web.FileResponse:
    root = Path(__file__).resolve().parents[1]
    return web.FileResponse(
        root
        / "custom_components"
        / "opengopro"
        / "frontend"
        / "opengopro-console-styles.js"
    )


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
    root = Path(__file__).resolve().parents[1]
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
    root = Path(__file__).resolve().parents[1]
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
        root = Path(__file__).resolve().parents[1]
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

    root = Path(__file__).resolve().parents[1]
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
    root = Path(__file__).resolve().parents[1]
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


async def camera_command(request: web.Request) -> web.Response:
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
    try:
        response = await session.get(
            url,
            auth=client._http_auth(),
            ssl=client.verify_ssl,
        )
        response.raise_for_status()
        headers = {}
        if response.content_length is not None:
            headers["Content-Length"] = str(response.content_length)
        content_type = response.headers.get("Content-Type", "application/octet-stream")
        headers["Content-Type"] = content_type
        if not thumbnail:
            filename = path.rsplit("/", 1)[-1]
            headers["Content-Disposition"] = f'inline; filename="{filename}"'
        stream = web.StreamResponse(status=200, headers=headers)
        await stream.prepare(request)
        async for chunk in response.content.iter_chunked(1024 * 64):
            await stream.write(chunk)
        await stream.write_eof()
        return stream
    except Exception as err:
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
    root = Path(__file__).resolve().parents[1]
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
            f"worker={root / 'standalone' / 'ble_worker.py'} python={sys.executable}"
        )
    if not isinstance(credentials, dict):
        raise OpenGoProError(f"COHN 状态 helper 未返回 credentials: {payload}")
    return credentials


async def _optional_json(request: web.Request) -> dict[str, Any]:
    if request.can_read_body:
        return await request.json()
    return {}


async def create_app(data_path: Path) -> web.Application:
    app = web.Application()
    app["store"] = CameraStore(data_path)
    app["session"] = ClientSession()
    app["keepalive_tasks"] = {}
    app["keepalive_interval"] = 3.0
    app["wake_schedule_task"] = asyncio.create_task(_wake_schedule_loop(app))
    app["preview_manager"] = PreviewManager(OpenGoProError)
    app.router.add_get("/", index)
    app.router.add_get("/assets/opengopro-console.js", console_asset)
    app.router.add_get("/assets/opengopro-console-styles.js", console_styles_asset)
    app.router.add_get("/assets/mpegts.min.js", mpegts_asset)
    app.router.add_get("/api/health", health)
    app.router.add_get("/api/cameras", list_cameras)
    app.router.add_post("/api/cameras", add_camera)
    app.router.add_post("/api/scan", scan_ble)
    app.router.add_post("/api/cohn/access-points", scan_access_points)
    app.router.add_post("/api/cohn/provision", provision_cohn)
    app.router.add_post("/api/cohn/provision/stream", provision_cohn_stream)
    app.router.add_get("/api/cameras/{camera_id}/state", camera_state)
    app.router.add_get("/api/cameras/{camera_id}/presence", camera_presence)
    app.router.add_post("/api/cameras/{camera_id}/wake-schedule", camera_wake_schedule)
    app.router.add_get("/api/cameras/{camera_id}/media", camera_media)
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
        app["wake_schedule_task"].cancel()
        await asyncio.gather(app["wake_schedule_task"], return_exceptions=True)
        for task in list(app["keepalive_tasks"].values()):
            task.cancel()
        if app["keepalive_tasks"]:
            await asyncio.gather(*app["keepalive_tasks"].values(), return_exceptions=True)
        await app["preview_manager"].close()
        await app["session"].close()

    app.on_cleanup.append(close_session)
    return app


def main() -> None:
    parser = argparse.ArgumentParser(description="OpenGoPro standalone service")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--data", type=Path, default=Path("data/cameras.json"))
    args = parser.parse_args()
    web.run_app(create_app(args.data), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
