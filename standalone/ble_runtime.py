"""BLE runtime helpers for standalone OpenGoPro."""

from __future__ import annotations

import asyncio
import platform
from collections.abc import Callable
from typing import Any

from aiohttp import ClientSession
import bleak
from bleak import BleakClient, BleakScanner

try:
    from opengopro_loader import load_client_module
except ModuleNotFoundError:
    from .opengopro_loader import load_client_module

client_module = load_client_module()
OpenGoProClient = client_module.OpenGoProClient

GOPRO_BLE_SERVICE_UUID = "0000fea6-0000-1000-8000-00805f9b34fb"
GOPRO_BLE_SERVICE_UUID_SHORT = "fea6"
GOPRO_COMPANY_IDS = {0x02F2, 0xF202}
GOPRO_NAME_PREFIXES = ("gopro", "hero")


def error_payload(err: Exception) -> dict[str, str | None]:
    """Return structured error details."""
    cause = err.__cause__
    return {
        "message": str(err),
        "type": type(err).__name__,
        "repr": repr(err),
        "cause_type": type(cause).__name__ if cause else None,
        "cause_repr": repr(cause) if cause else None,
    }


async def wake(
    address: str,
    *,
    resolve_timeout: float = 10,
    connect_timeout: float = 20,
    hold: float = 2,
) -> dict[str, Any]:
    """Wake the camera with a minimal BLE connect/disconnect."""
    result: dict[str, Any] = {
        "ble_address": address,
        "resolved_device": None,
        "ble_connect": None,
        "error": None,
    }
    client = None
    try:
        device = await BleakScanner.find_device_by_address(
            address,
            timeout=resolve_timeout,
        )
        if device is None:
            result["error"] = _device_not_found()
            return result
        result["resolved_device"] = {
            "name": device.name,
            "address": device.address,
        }
        client = BleakClient(device)
        await asyncio.wait_for(client.connect(), timeout=connect_timeout)
        result["ble_connect"] = "ok"
        await asyncio.sleep(hold)
    except Exception as err:
        result["error"] = error_payload(err)
    finally:
        try:
            if client and client.is_connected:
                await client.disconnect()
        except Exception:
            pass
    return result


async def scan(
    *,
    timeout: float = 10,
    all_devices: bool = False,
) -> dict[str, Any]:
    """Scan nearby BLE devices."""
    result: dict[str, Any] = {
        "devices": [],
        "error": None,
        "diagnostics": {
            "platform": platform.platform(),
            "bleak_version": getattr(bleak, "__version__", None),
            "attempts": [],
        },
    }
    try:
        attempts = result["diagnostics"]["attempts"]
        devices = await _scan_once(
            timeout=timeout,
            all_devices=all_devices,
            service_uuids=None if all_devices else [GOPRO_BLE_SERVICE_UUID],
            attempts=attempts,
        )
        if not devices and not all_devices:
            devices = await _scan_once(
                timeout=timeout,
                all_devices=all_devices,
                service_uuids=None,
                attempts=attempts,
            )
        result["devices"] = sorted(devices, key=lambda item: item["rssi"], reverse=True)
    except Exception as err:
        result["error"] = error_payload(err)
    return result


async def _scan_once(
    *,
    timeout: float,
    all_devices: bool,
    service_uuids: list[str] | None,
    attempts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Run one Bleak scan and return matching device payloads."""
    discovered = await BleakScanner.discover(
        timeout=timeout,
        return_adv=True,
        service_uuids=service_uuids,
    )
    devices = []
    matched_count = 0
    for address, (device, advertisement) in discovered.items():
        name = device.name or advertisement.local_name
        matched_by = _gopro_match_reasons(device, advertisement)
        if matched_by:
            matched_count += 1
        if not all_devices and not matched_by:
            continue
        devices.append(_ble_device_payload(address, device, advertisement, name, matched_by))
    attempts.append(
        {
            "service_uuids": service_uuids or [],
            "raw_count": len(discovered),
            "matched_count": matched_count,
            "returned_count": len(devices),
        }
    )
    return devices


def _ble_device_payload(
    address: str,
    device: Any,
    advertisement: Any,
    name: str | None,
    matched_by: list[str],
) -> dict[str, Any]:
    """Return a JSON-safe BLE discovery payload."""
    manufacturer_data = getattr(advertisement, "manufacturer_data", None) or {}
    service_data = getattr(advertisement, "service_data", None) or {}
    return {
        "name": name or ("GoPro" if matched_by else None),
        "address": address,
        "rssi": advertisement.rssi,
        "service_uuids": list(advertisement.service_uuids or []),
        "service_data_uuids": [str(uuid) for uuid in service_data],
        "manufacturer_ids": sorted(int(company_id) for company_id in manufacturer_data),
        "matched_by": matched_by,
    }


def _gopro_match_reasons(device: Any, advertisement: Any) -> list[str]:
    """Return reasons why a BLE discovery looks like a GoPro camera."""
    reasons = []
    names = [
        getattr(device, "name", None),
        getattr(advertisement, "local_name", None),
    ]
    if any(name and name.lower().startswith(GOPRO_NAME_PREFIXES) for name in names):
        reasons.append("name")
    if _has_gopro_service_uuid(device, advertisement):
        reasons.append("service_uuid")
    manufacturer_data = getattr(advertisement, "manufacturer_data", None) or {}
    if any(company_id in manufacturer_data for company_id in GOPRO_COMPANY_IDS):
        reasons.append("manufacturer")
    return reasons


def _has_gopro_service_uuid(device: Any, advertisement: Any) -> bool:
    """Return whether a BLE discovery advertises GoPro's 0xFEA6 service."""
    service_uuids = (
        list(getattr(device, "service_uuids", None) or [])
        + list(getattr(advertisement, "service_uuids", None) or [])
    )
    service_data = {
        **(getattr(device, "service_data", None) or {}),
        **(getattr(advertisement, "service_data", None) or {}),
    }
    return any(_is_gopro_service_uuid(uuid) for uuid in [*service_uuids, *service_data])


def _is_gopro_service_uuid(uuid: Any) -> bool:
    """Return whether a UUID-like value is GoPro's BLE service UUID."""
    normalized = str(uuid).lower()
    compact = normalized.replace("-", "")
    return (
        normalized == GOPRO_BLE_SERVICE_UUID
        or compact == GOPRO_BLE_SERVICE_UUID.replace("-", "")
        or compact in (GOPRO_BLE_SERVICE_UUID_SHORT, f"0000{GOPRO_BLE_SERVICE_UUID_SHORT}")
    )


async def cohn_status(
    address: str,
    *,
    resolve_timeout: float = 10,
    timeout: float = 45,
) -> dict[str, Any]:
    """Read current COHN status over BLE."""
    result: dict[str, Any] = {
        "ble_address": address,
        "resolved_device": None,
        "credentials": None,
        "error": None,
    }
    client = None
    trace: list[dict[str, Any]] = []
    try:
        device = await BleakScanner.find_device_by_address(
            address,
            timeout=resolve_timeout,
        )
        if device is None:
            result["error"] = _device_not_found()
            return result
        result["resolved_device"] = {
            "name": device.name,
            "address": device.address,
        }
        async with ClientSession() as session:
            client = OpenGoProClient(session, address, ble_device=device)
            await client.async_ble_connect()
            status = await client.async_wait_cohn_status(timeout=timeout)
            result["credentials"] = {
                "ip_address": _field_string(status, 5),
                "username": _field_string(status, 3),
                "password": _field_string(status, 4),
                "ssid": _field_string(status, 7),
                "mac_address": _field_string(status, 8),
            }
    except Exception as err:
        result["error"] = error_payload(err)
    finally:
        try:
            if client:
                await client.async_ble_disconnect()
        except Exception:
            pass
    return result


async def scan_access_points(
    address: str,
    *,
    resolve_timeout: float = 10,
    timeout: float = 60,
) -> dict[str, Any]:
    """Scan Wi-Fi access points visible to the camera over BLE."""
    result: dict[str, Any] = {
        "ble_address": address,
        "resolved_device": None,
        "notification_trace": [],
        "connect_trace": [],
        "access_points": [],
        "current_ssid": None,
        "error": None,
    }
    client = None
    trace: list[dict[str, Any]] = []
    try:
        device = await BleakScanner.find_device_by_address(
            address,
            timeout=resolve_timeout,
        )
        if device is None:
            result["error"] = _device_not_found()
            return result
        result["resolved_device"] = {
            "name": device.name,
            "address": device.address,
        }
        async with ClientSession() as session:
            client = OpenGoProClient(session, address, ble_device=device)
            await client.async_ble_connect()
            result["notification_trace"] = list(
                getattr(client, "last_notification_trace", [])
            )
            current_ssid = None
            try:
                status = await client.async_wait_cohn_status(timeout=5)
                current_ssid = _field_string(status, 7)
            except Exception:
                current_ssid = None
            entries = await client.async_scan_access_points(timeout=timeout, trace=trace)
            result["connect_trace"] = trace
            result["current_ssid"] = current_ssid
            result["access_points"] = _wifi_entries_payload(entries, current_ssid=current_ssid)
    except Exception as err:
        if client is not None:
            result["connect_trace"] = trace or list(getattr(client, "last_connect_trace", []))
            result["notification_trace"] = list(
                getattr(client, "last_notification_trace", [])
            )
        result["error"] = error_payload(err)
    finally:
        try:
            if client:
                await client.async_ble_disconnect()
        except Exception:
            pass
    return result


async def provision_cohn(
    address: str,
    ssid: str,
    password: str,
    *,
    name: str = "GoPro",
    verify_ssl: bool = False,
    keep_certificate: bool = False,
    force_new_credentials: bool = True,
    resolve_timeout: float = 10,
    timeout: float = 360,
    progress: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    """Provision HERO12+ COHN over BLE."""
    result: dict[str, Any] = {
        "ble_address": address,
        "resolved_device": None,
        "stage": "resolve_ble",
        "force_new_credentials": force_new_credentials,
        "notification_trace": [],
        "connect_trace": [],
        "credentials": None,
        "certificate": None,
        "error": None,
    }
    client = None
    def update(stage: str, **extra: Any) -> None:
        result["stage"] = stage
        if client is not None:
            result["connect_trace"] = list(getattr(client, "last_connect_trace", []))
            result["notification_trace"] = list(
                getattr(client, "last_notification_trace", [])
            )
        if progress:
            progress({"stage": stage, **extra, "result": _public_progress_result(result)})

    try:
        update("resolve_ble")
        device = await BleakScanner.find_device_by_address(
            address,
            timeout=resolve_timeout,
        )
        if device is None:
            result["error"] = _device_not_found()
            update("failed", error=result["error"])
            return result
        result["resolved_device"] = {
            "name": device.name,
            "address": device.address,
        }
        async with asyncio.timeout(timeout):
            update("ble_connect", device=result["resolved_device"])
            async with ClientSession() as session:
                client = OpenGoProClient(
                    session,
                    address,
                    name=name,
                    ble_device=device,
                    verify_ssl=verify_ssl,
                )
                await client.async_ble_connect()
                result["notification_trace"] = list(
                    getattr(client, "last_notification_trace", [])
                )
                update("set_datetime")
                await client.async_set_local_datetime()
                update("scan_wifi", ssid=ssid)
                connect_trace: list[dict[str, Any]] = []
                entries = await client.async_scan_access_points(
                    timeout=timeout,
                    trace=connect_trace,
                )
                result["connect_trace"] = connect_trace
                update("scan_wifi_done", access_points=_wifi_entries_payload(entries))
                update("connect_wifi", ssid=ssid)
                await client.async_connect_to_access_point(
                    ssid,
                    password,
                    force_new_credentials=force_new_credentials,
                    timeout=timeout,
                    entries=entries,
                    trace=connect_trace,
                )
                result["connect_trace"] = list(getattr(client, "last_connect_trace", []))
                update("connect_wifi_done")
                if not keep_certificate:
                    update("clear_certificate")
                    await client.async_clear_cohn_certificate()
                update("create_certificate")
                await client.async_create_cohn_certificate()
                update("get_certificate")
                certificate = await client.async_get_cohn_certificate()
                result["certificate"] = certificate
                update("wait_cohn_status")
                status = await client.async_wait_cohn_status(timeout=timeout)
                credentials = {
                    "ip_address": _field_string(status, 5),
                    "username": _field_string(status, 3),
                    "password": _field_string(status, 4),
                    "ssid": _field_string(status, 7),
                    "mac_address": _field_string(status, 8),
                }
                update("cohn_status_done", credentials=_public_credentials(credentials))
                if (
                    not credentials["ip_address"]
                    or not credentials["username"]
                    or not credentials["password"]
                ):
                    raise client_module.OpenGoProConnectionError("COHN 配置未返回完整连接信息")
                result["credentials"] = {
                    "ip_address": credentials["ip_address"],
                    "username": credentials["username"],
                    "password": credentials["password"],
                    "ssid": credentials["ssid"],
                    "mac_address": credentials["mac_address"],
                }
                update("done", credentials=_public_credentials(result["credentials"]))
    except Exception as err:
        if client is not None:
            result["connect_trace"] = list(getattr(client, "last_connect_trace", []))
            result["notification_trace"] = list(
                getattr(client, "last_notification_trace", [])
            )
        result["error"] = error_payload(err)
        update("failed", error=result["error"])
    finally:
        try:
            if client:
                await client.async_ble_disconnect()
        except Exception:
            pass
    return result


async def presence(
    address: str,
    *,
    resolve_timeout: float = 5,
) -> dict[str, Any]:
    """Check whether the camera is advertising over BLE without connecting."""
    result: dict[str, Any] = {
        "ble_address": address,
        "resolved_device": None,
        "ble_available": False,
        "error": None,
    }
    try:
        device = await BleakScanner.find_device_by_address(
            address,
            timeout=resolve_timeout,
        )
        if device is None:
            return result
        result["ble_available"] = True
        result["resolved_device"] = {
            "name": device.name,
            "address": device.address,
        }
    except Exception as err:
        result["error"] = error_payload(err)
    return result


async def enable_wifi(
    address: str,
    *,
    resolve_timeout: float = 10,
) -> dict[str, Any]:
    """Enable GoPro AP Wi-Fi over BLE."""
    result: dict[str, Any] = {
        "ble_address": address,
        "resolved_device": None,
        "ble_connect": None,
        "enable_wifi": None,
        "error": None,
    }
    client = None
    try:
        device = await BleakScanner.find_device_by_address(
            address,
            timeout=resolve_timeout,
        )
        if device is None:
            result["error"] = _device_not_found()
            return result
        result["resolved_device"] = {
            "name": device.name,
            "address": device.address,
        }
        async with ClientSession() as session:
            client = OpenGoProClient(session, address, ble_device=device)
            await client.async_ble_connect()
            result["ble_connect"] = "ok"
            await client.async_enable_wifi()
            result["enable_wifi"] = "ok"
    except Exception as err:
        result["error"] = error_payload(err)
    finally:
        try:
            if client:
                await client.async_ble_disconnect()
        except Exception:
            pass
    return result


async def sleep(
    address: str,
    *,
    resolve_timeout: float = 10,
) -> dict[str, Any]:
    """Put the camera to sleep over BLE."""
    result: dict[str, Any] = {
        "ble_address": address,
        "resolved_device": None,
        "ble_connect": None,
        "sleep": None,
        "error": None,
    }
    client = None
    try:
        device = await BleakScanner.find_device_by_address(
            address,
            timeout=resolve_timeout,
        )
        if device is None:
            result["error"] = _device_not_found()
            return result
        result["resolved_device"] = {
            "name": device.name,
            "address": device.address,
        }
        async with ClientSession() as session:
            client = OpenGoProClient(session, address, ble_device=device)
            await client.async_ble_connect()
            result["ble_connect"] = "ok"
            await client.async_ble_sleep()
            result["sleep"] = "ok"
    except Exception as err:
        result["error"] = error_payload(err)
    finally:
        try:
            if client:
                await client.async_ble_disconnect()
        except Exception:
            pass
    return result


def _field_string(fields: dict[int, Any], key: int) -> str | None:
    value = fields.get(key)
    if isinstance(value, list):
        value = value[0] if value else None
    if isinstance(value, bytes):
        return value.decode(errors="replace")
    if value is None:
        return None
    return str(value)


def _wifi_entries_payload(
    entries: list[Any],
    *,
    current_ssid: str | None = None,
) -> list[dict[str, Any]]:
    return [
        {
            "ssid": entry.ssid,
            "signal_strength_bars": entry.signal_strength_bars,
            "signal_frequency_mhz": entry.signal_frequency_mhz,
            "flags": entry.flags,
            "configured": entry.is_configured,
            "current": bool(current_ssid and entry.ssid == current_ssid),
        }
        for entry in entries
    ]


def _public_credentials(credentials: dict[str, Any] | None) -> dict[str, Any] | None:
    if not credentials:
        return None
    return {
        "ip_address": credentials.get("ip_address"),
        "username": credentials.get("username"),
        "ssid": credentials.get("ssid"),
        "mac_address": credentials.get("mac_address"),
        "has_password": bool(credentials.get("password")),
    }


def _public_progress_result(result: dict[str, Any]) -> dict[str, Any]:
    public = dict(result)
    public["credentials"] = _public_credentials(public.get("credentials"))
    public["certificate"] = bool(public.get("certificate"))
    return public


def _device_not_found() -> dict[str, str | None]:
    return {
        "message": "扫描阶段没有再次找到该 BLE 地址",
        "type": "DeviceNotFound",
        "repr": None,
        "cause_type": None,
        "cause_repr": None,
    }
