"""WebSocket API for the OpenGoPro panel."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any
from urllib.parse import quote

import voluptuous as vol

from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import OpenGoProCoordinator


def async_register_websocket_api(hass: HomeAssistant) -> None:
    """Register WebSocket commands."""
    websocket_api.async_register_command(hass, ws_list_cameras)
    websocket_api.async_register_command(hass, ws_command)
    websocket_api.async_register_command(hass, ws_presence)
    websocket_api.async_register_command(hass, ws_scan_access_points)
    websocket_api.async_register_command(hass, ws_media)
    websocket_api.async_register_command(hass, ws_presets)


@websocket_api.websocket_command({vol.Required("type"): f"{DOMAIN}/cameras"})
@websocket_api.async_response
async def ws_list_cameras(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return loaded OpenGoPro cameras."""
    connection.send_result(msg["id"], [_coordinator_payload(c) for c in _coordinators(hass)])


@websocket_api.websocket_command(
    {
        vol.Required("type"): f"{DOMAIN}/command",
        vol.Required("entry_id"): str,
        vol.Required("command"): vol.In(
            [
                "wake",
                "sleep",
                "shutter_start",
                "shutter_stop",
                "set_mode",
                "set_setting",
                "set_preset",
                "refresh_media",
                "start_preview",
                "stop_preview",
            ]
        ),
        vol.Optional("mode"): str,
        vol.Optional("setting"): str,
        vol.Optional("option"): str,
        vol.Optional("preset"): str,
    }
)
@websocket_api.async_response
async def ws_command(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Run a panel command."""
    coordinator = _coordinator(hass, msg["entry_id"])
    command = msg["command"]
    if command == "wake":
        await coordinator.async_wake()
    elif command == "sleep":
        await coordinator.async_sleep()
    elif command == "shutter_start":
        await coordinator.async_shutter(True)
    elif command == "shutter_stop":
        await coordinator.async_shutter(False)
    elif command == "set_mode":
        await coordinator.async_set_mode(msg["mode"])
    elif command == "set_setting":
        await coordinator.async_set_setting(msg["setting"], msg["option"])
    elif command == "set_preset":
        await coordinator.async_set_preset(msg["preset"])
    elif command == "refresh_media":
        await coordinator.async_refresh_media()
    elif command == "start_preview":
        await coordinator.async_start_preview()
    elif command == "stop_preview":
        await coordinator.async_stop_preview()
    connection.send_result(msg["id"], _coordinator_payload(coordinator))


@websocket_api.websocket_command(
    {
        vol.Required("type"): f"{DOMAIN}/presence",
        vol.Required("entry_id"): str,
    }
)
@websocket_api.async_response
async def ws_presence(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return non-waking Bluetooth presence from Home Assistant's discovery cache."""
    coordinator = _coordinator(hass, msg["entry_id"])
    connection.send_result(msg["id"], _presence_payload(hass, coordinator))


@websocket_api.websocket_command(
    {
        vol.Required("type"): f"{DOMAIN}/scan_access_points",
        vol.Required("entry_id"): str,
        vol.Optional("timeout", default=30): vol.All(vol.Coerce(float), vol.Range(min=5, max=120)),
    }
)
@websocket_api.async_response
async def ws_scan_access_points(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Scan Wi-Fi access points visible to the camera over BLE."""
    coordinator = _coordinator(hass, msg["entry_id"])
    entries = await coordinator.async_scan_access_points(timeout=msg["timeout"])
    connection.send_result(msg["id"], {"access_points": [asdict(entry) for entry in entries]})


@websocket_api.websocket_command(
    {
        vol.Required("type"): f"{DOMAIN}/media",
        vol.Required("entry_id"): str,
    }
)
@websocket_api.async_response
async def ws_media(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return media cache for the panel."""
    coordinator = _coordinator(hass, msg["entry_id"])
    media = await coordinator.async_refresh_media()
    connection.send_result(
        msg["id"],
        [
            {
                "path": item.path,
                "name": item.name,
                "directory": item.directory,
                "size": item.size,
                "created": item.created,
                "media_type": item.media_type,
                "url": f"/api/opengopro/media/{msg['entry_id']}/{quote(item.path, safe='')}",
                "thumbnail": (
                    f"/api/opengopro/thumbnail/{msg['entry_id']}/"
                    f"{quote(item.path, safe='')}"
                ),
            }
            for item in media
        ],
    )


@websocket_api.websocket_command(
    {vol.Required("type"): f"{DOMAIN}/presets", vol.Required("entry_id"): str}
)
@websocket_api.async_response
async def ws_presets(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return camera preset hierarchy."""
    coordinator = _coordinator(hass, msg["entry_id"])
    connection.send_result(msg["id"], await coordinator.async_get_preset_status())


def _coordinators(hass: HomeAssistant) -> list[OpenGoProCoordinator]:
    return list(hass.data.get(DOMAIN, {}).values())


def _coordinator(hass: HomeAssistant, entry_id: str) -> OpenGoProCoordinator:
    return hass.data[DOMAIN][entry_id]


def _coordinator_payload(coordinator: OpenGoProCoordinator) -> dict[str, Any]:
    data = coordinator.data
    preview = coordinator.preview_status() if hasattr(coordinator, "preview_status") else {}
    return {
        "entry_id": coordinator.config_entry.entry_id,
        "name": coordinator.config_entry.title,
        "ble_address": coordinator.client.ble_address,
        "phase": data.phase.value if data else "unknown",
        "power": "on" if data and data.phase.value == "http_ready" else "standby",
        "http_ready": bool(data and data.phase.value == "http_ready"),
        "model": data.model if data else None,
        "firmware": data.firmware if data else None,
        "battery": data.battery if data else None,
        "remaining_storage": data.remaining_storage if data else None,
        "current_mode": data.current_mode if data else None,
        "preset": data.preset if data else None,
        "temperature": data.temperature if data else None,
        "recording": data.recording if data else False,
        "sd_card_status": data.sd_card_status if data else None,
        "wifi_enabled": data.wifi_enabled if data else None,
        "ble_connected": data.ble_connected if data else False,
        "preview_active": bool(preview.get("running") or (data.preview_active if data else False)),
        "preview_url": preview.get("stream_url"),
        "preview_transport": preview.get("transport"),
        "preview_error": preview.get("error"),
        "modes": data.available_modes if data else ["video", "photo", "timelapse"],
        "presets": data.available_presets if data else [],
        "settings": data.settings if data else {},
    }


def _presence_payload(
    hass: HomeAssistant,
    coordinator: OpenGoProCoordinator,
) -> dict[str, Any]:
    """Return a panel presence payload without waking the camera."""
    try:
        discoveries = _async_discovered_service_info(hass)
    except Exception:
        discoveries = []
    return _presence_payload_from_discoveries(coordinator, discoveries)


def _presence_payload_from_discoveries(
    coordinator: OpenGoProCoordinator,
    discoveries: list[Any],
) -> dict[str, Any]:
    """Return presence payload from Bluetooth discovery objects."""
    address = coordinator.client.ble_address
    discovery = next(
        (
            discovery
            for discovery in discoveries
            if getattr(discovery, "address", None) == address
        ),
        None,
    )
    data = coordinator.data
    http_ready = bool(data and data.phase == "http_ready")
    ble_available = discovery is not None
    return {
        "power": "on" if http_ready else ("standby" if ble_available else "unknown"),
        "phase": data.phase.value if http_ready and data else ("ble_standby" if ble_available else "unknown"),
        "http_ready": http_ready,
        "ble_available": ble_available,
        "ble": _bluetooth_discovery_payload(discovery) if discovery else None,
    }


def _bluetooth_discovery_payload(discovery: Any) -> dict[str, Any]:
    advertisement = getattr(discovery, "advertisement", None)
    return {
        "name": getattr(discovery, "name", None) or getattr(advertisement, "local_name", None),
        "address": getattr(discovery, "address", None),
        "rssi": getattr(discovery, "rssi", None) or getattr(advertisement, "rssi", None),
        "service_uuids": list(
            getattr(discovery, "service_uuids", None)
            or getattr(advertisement, "service_uuids", None)
            or []
        ),
    }


def _async_discovered_service_info(hass: HomeAssistant) -> list[Any]:
    """Return Bluetooth discoveries from Home Assistant."""
    from homeassistant.components import bluetooth

    return list(bluetooth.async_discovered_service_info(hass))
