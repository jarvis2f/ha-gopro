"""Diagnostics for OpenGoPro."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_HTTP_PASSWORD, DOMAIN


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = hass.data[DOMAIN].get(entry.entry_id)
    data = coordinator.data if coordinator else None
    entry_data = {**entry.data, "ble_address": "***redacted***"}
    if CONF_HTTP_PASSWORD in entry_data:
        entry_data[CONF_HTTP_PASSWORD] = "***redacted***"
    return {
        "entry": {
            "title": entry.title,
            "options": dict(entry.options),
            "data": entry_data,
        },
        "state": {
            "phase": data.phase.value if data else None,
            "model": data.model if data else None,
            "firmware": data.firmware if data else None,
            "battery": data.battery if data else None,
            "recording": data.recording if data else None,
            "sd_card_status": data.sd_card_status if data else None,
            "preview_active": data.preview_active if data else None,
        },
    }
