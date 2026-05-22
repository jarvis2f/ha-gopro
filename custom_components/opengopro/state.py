"""Camera state normalization helpers."""

from __future__ import annotations

from typing import Any

from .models import CameraSnapshot, ConnectionPhase
from .protocol import (
    STATUS_AP_MODE,
    STATUS_BATTERY_PERCENTAGE,
    STATUS_CAMERA_NAME,
    STATUS_COLD,
    STATUS_ENCODING,
    STATUS_FLATMODE,
    STATUS_MODEL_NAME,
    STATUS_OVERHEATING,
    STATUS_PRESET,
    STATUS_PRESET_GROUP,
    STATUS_PREVIEW_STREAM,
    STATUS_PRIMARY_STORAGE,
    STATUS_SD_CARD_ERRORS,
    STATUS_SD_CARD_REMAINING_KB,
    STATUS_SD_CARD_WRITE_ERROR,
)


def normalize_camera_state(
    payload: dict[str, Any],
    *,
    phase: ConnectionPhase,
    name: str,
    preview_active: bool,
) -> CameraSnapshot:
    """Convert raw OpenGoPro state into stable HA-facing keys."""
    status = payload.get("status", {})
    settings = payload.get("settings", {})
    remaining_storage_kb = _int_or_none(
        _first_present(status, STATUS_SD_CARD_REMAINING_KB, "remaining_storage_kb")
    )
    sd_card_present = _sd_card_present(
        _first_present(status, STATUS_PRIMARY_STORAGE, "sd_card_present")
    )
    snapshot = CameraSnapshot(
        phase=phase,
        model=_string_or_none(
            _first_present(status, STATUS_CAMERA_NAME, STATUS_MODEL_NAME, "model") or name
        ),
        firmware=_string_or_none(status.get("firmware")),
        battery=_int_or_none(_first_present(status, STATUS_BATTERY_PERCENTAGE, "battery")),
        remaining_storage=_kb_to_mb(remaining_storage_kb),
        current_mode=_mode_name(
            _first_present(status, STATUS_PRESET_GROUP, STATUS_FLATMODE, "current_mode")
        ),
        preset=_string_or_none(_first_present(status, STATUS_PRESET, "preset")),
        temperature=_temperature_state(_first_present(status, STATUS_COLD, "temperature")),
        recording=_bool(_first_present(status, STATUS_ENCODING, "recording")),
        sd_card_present=sd_card_present,
        sd_card_status=_sd_card_status(status, sd_card_present),
        wifi_enabled=(
            _bool_or_none(status.get(STATUS_AP_MODE))
            if status.get(STATUS_AP_MODE) is not None
            else phase in (ConnectionPhase.WIFI_ENABLED, ConnectionPhase.HTTP_READY)
        ),
        ble_connected=phase != ConnectionPhase.DISCONNECTED,
        overheating=_bool_or_none(_first_present(status, STATUS_OVERHEATING, "overheating")),
        preview_active=_bool(status.get(STATUS_PREVIEW_STREAM)) or preview_active,
        settings=settings if isinstance(settings, dict) else {},
        raw_state=payload,
    )
    if phase == ConnectionPhase.HTTP_READY:
        snapshot.phase = ConnectionPhase.HTTP_READY
    return snapshot


def _mode_name(value: Any) -> str | None:
    """Return a display mode name from common OpenGoPro values."""
    if value is None:
        return None
    mapping = {
        0: "video",
        1: "photo",
        2: "timelapse",
        1000: "video",
        1001: "photo",
        1002: "timelapse",
        "0": "video",
        "1": "photo",
        "2": "timelapse",
        "1000": "video",
        "1001": "photo",
        "1002": "timelapse",
        "video": "video",
        "photo": "photo",
        "timelapse": "timelapse",
    }
    return mapping.get(value, str(value))


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _bool_or_none(value: Any) -> bool | None:
    if value is None:
        return None
    return _bool(value)


def _string_or_none(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _bool(value: Any) -> bool:
    """Return bool for common OpenGoPro integer/string status values."""
    if isinstance(value, str):
        return value.lower() not in {"", "0", "false", "off", "none"}
    return bool(value)


def _kb_to_mb(value: int | None) -> int | None:
    """Convert OpenGoPro SD remaining space from KB to MB."""
    if value is None:
        return None
    return round(value / 1024)


def _sd_card_present(value: Any) -> bool | None:
    """Best-effort primary storage presence conversion."""
    if value is None:
        return None
    if value in (0, "0"):
        return True
    return _bool(value)


def _sd_card_status(status: dict[str, Any], present: bool | None) -> str | None:
    """Return a stable SD card status string."""
    if present is False:
        return "missing"
    sd_errors = _int_or_none(status.get(STATUS_SD_CARD_ERRORS)) or 0
    write_error = _int_or_none(status.get(STATUS_SD_CARD_WRITE_ERROR)) or 0
    if sd_errors > 0:
        return "error"
    if write_error > 1:
        return "write_error"
    if present is True:
        return "ok"
    return _string_or_none(status.get("sd_card_status"))


def _temperature_state(value: Any) -> str | None:
    """Return a user-facing camera temperature state."""
    if value is None:
        return None
    if isinstance(value, str) and not value.isdigit():
        return value
    return "cold" if _bool(value) else "normal"


def _first_present(source: dict[str, Any], *keys: str) -> Any:
    """Return the first present dict value, preserving falsey values."""
    for key in keys:
        if key in source:
            return source[key]
    return None
