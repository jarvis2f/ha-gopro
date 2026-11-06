"""Shared OpenGoPro data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from protocol import PROTO_SCAN_FLAG_CONFIGURED


class OpenGoProError(Exception):
    """Base error raised by the OpenGoPro client."""


class OpenGoProConnectionError(OpenGoProError):
    """Raised when the camera cannot be reached."""


class OpenGoProHttpError(OpenGoProConnectionError):
    """Raised when the camera returns a non-success HTTP response."""

    def __init__(
        self,
        message: str,
        *,
        status: int,
        payload: dict[str, Any] | None = None,
        url: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.payload = payload or {}
        self.url = url


class OpenGoProCommandError(OpenGoProError):
    """Raised when the camera rejects a command."""


class ConnectionPhase(StrEnum):
    """Connection lifecycle phase."""

    DISCONNECTED = "disconnected"
    BLE_CONNECTED = "ble_connected"
    WIFI_ENABLED = "wifi_enabled"
    HTTP_READY = "http_ready"


@dataclass(slots=True)
class CohnCredentials:
    """Credentials returned after COHN provisioning."""

    certificate: str
    username: str
    password: str
    ip_address: str
    ssid: str | None = None
    mac_address: str | None = None


@dataclass(slots=True)
class WifiScanEntry:
    """A Wi-Fi network discovered by the camera."""

    ssid: str
    signal_strength_bars: int | None = None
    signal_frequency_mhz: int | None = None
    flags: int = 0

    @property
    def is_configured(self) -> bool:
        """Return whether the camera already has credentials for this SSID."""
        return bool(self.flags & PROTO_SCAN_FLAG_CONFIGURED)


@dataclass(slots=True)
class CameraMediaItem:
    """A media item reported by a GoPro camera."""

    directory: str
    name: str
    size: int | None = None
    created: str | None = None
    media_type: str = "video/mp4"

    @property
    def path(self) -> str:
        """Return the camera-relative path."""
        return f"{self.directory}/{self.name}".strip("/")


@dataclass(slots=True)
class CameraSnapshot:
    """Normalized camera state shown by the console."""

    phase: ConnectionPhase = ConnectionPhase.DISCONNECTED
    model: str | None = None
    firmware: str | None = None
    battery: int | None = None
    remaining_storage: int | None = None
    current_mode: str | None = None
    preset: str | None = None
    temperature: str | None = None
    recording: bool = False
    sd_card_present: bool | None = None
    sd_card_status: str | None = None
    wifi_enabled: bool | None = None
    ble_connected: bool = False
    overheating: bool | None = None
    preview_active: bool = False
    available_modes: list[str] = field(default_factory=lambda: ["video", "photo", "timelapse"])
    available_presets: list[str] = field(default_factory=list)
    settings: dict[str, Any] = field(default_factory=dict)
    raw_state: dict[str, Any] = field(default_factory=dict)
