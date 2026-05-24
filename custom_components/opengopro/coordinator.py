"""Data update coordinator for OpenGoPro."""

from __future__ import annotations

import asyncio
from dataclasses import replace
from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .client import CameraMediaItem, CameraSnapshot, OpenGoProClient, OpenGoProError
from .const import (
    CONF_BLE_ADDRESS,
    CONF_HTTP_HOST,
    CONF_HTTP_PASSWORD,
    CONF_HTTP_PORT,
    CONF_HTTP_SCHEME,
    CONF_HTTP_USERNAME,
    CONF_VERIFY_SSL,
    DEFAULT_HTTP_HOST,
    DEFAULT_HTTP_PORT,
    DEFAULT_HTTP_SCHEME,
    DEFAULT_KEEP_ALIVE_INTERVAL,
    DEFAULT_POLL_INTERVAL,
    DOMAIN,
    PREVIEW_MANAGER_KEY,
)
from .models import ConnectionPhase
from .preview import OpenGoProPreviewManager

_LOGGER = logging.getLogger(__name__)


class OpenGoProCoordinator(DataUpdateCoordinator[CameraSnapshot]):
    """Own camera lifecycle, polling, Keep Alive, and media cache."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        client: OpenGoProClient,
        preview_manager: OpenGoProPreviewManager,
    ) -> None:
        self.client = client
        self.preview_manager = preview_manager
        self.media: list[CameraMediaItem] = []
        self._keep_alive_task: asyncio.Task[None] | None = None
        poll_interval = entry.options.get("poll_interval", DEFAULT_POLL_INTERVAL)
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            config_entry=entry,
            update_interval=timedelta(seconds=poll_interval),
        )

    @classmethod
    def from_entry(
        cls,
        hass: HomeAssistant,
        entry: ConfigEntry,
        session: Any,
    ) -> OpenGoProCoordinator:
        """Create a coordinator from config entry data."""
        ble_address = entry.data[CONF_BLE_ADDRESS]
        ble_device_callback = _ble_device_callback(hass, ble_address)
        client = OpenGoProClient(
            session,
            ble_address,
            name=entry.title,
            http_host=entry.data.get(CONF_HTTP_HOST, DEFAULT_HTTP_HOST),
            http_port=entry.data.get(CONF_HTTP_PORT, DEFAULT_HTTP_PORT),
            http_scheme=entry.data.get(CONF_HTTP_SCHEME, DEFAULT_HTTP_SCHEME),
            http_username=entry.data.get(CONF_HTTP_USERNAME),
            http_password=entry.data.get(CONF_HTTP_PASSWORD),
            verify_ssl=entry.data.get(CONF_VERIFY_SSL, True),
            ble_device=ble_device_callback(),
            ble_device_callback=ble_device_callback,
        )
        return cls(hass, entry, client, hass.data[PREVIEW_MANAGER_KEY])

    async def _async_update_data(self) -> CameraSnapshot:
        """Fetch camera state."""
        try:
            return await self.client.async_get_state()
        except OpenGoProError as err:
            raise UpdateFailed(str(err)) from err

    async def async_wake(self) -> None:
        """Wake and connect the camera."""
        await self.client.async_wake()
        self._ensure_keep_alive()
        await self.async_request_refresh()

    async def async_sleep(self) -> None:
        """Sleep and disconnect the camera."""
        self._stop_keep_alive()
        await self.preview_manager.stop(self.config_entry.entry_id)
        await self.client.async_sleep()
        current = self.data or CameraSnapshot()
        self.async_set_updated_data(
            replace(
                current,
                phase=ConnectionPhase.DISCONNECTED,
                wifi_enabled=False,
                ble_connected=False,
                preview_active=False,
                recording=False,
            )
        )

    async def async_guard_wake(self, *, hold: float = 3) -> None:
        """Refresh the BLE wake window and put the camera back to sleep."""
        self._stop_keep_alive()
        await self.client.async_ble_connect()
        await asyncio.sleep(hold)
        await self.client.async_ble_sleep()
        current = self.data or CameraSnapshot()
        self.async_set_updated_data(
            replace(
                current,
                phase=ConnectionPhase.DISCONNECTED,
                wifi_enabled=False,
                ble_connected=False,
                preview_active=False,
                recording=False,
            )
        )

    async def async_refresh_media(self) -> list[CameraMediaItem]:
        """Refresh cached media list."""
        self.media = await self.client.async_list_media()
        return self.media

    async def async_shutter(self, active: bool) -> None:
        """Start or stop recording/capture."""
        await self.client.async_shutter(active)
        await self.async_request_refresh()

    async def async_set_mode(self, mode: str) -> None:
        """Set camera mode."""
        await self.client.async_set_mode(mode)
        await self.async_request_refresh()

    async def async_set_preset(self, preset: str) -> None:
        """Set camera preset."""
        await self.client.async_set_preset(preset)
        await self.async_request_refresh()

    async def async_get_preset_status(self) -> dict[str, Any]:
        """Fetch the camera preset hierarchy."""
        return await self.client.async_get_preset_status()

    async def async_scan_access_points(self, *, timeout: float = 30) -> list[Any]:
        """Scan Wi-Fi access points visible to the camera over BLE."""
        return await self.client.async_scan_access_points(timeout=timeout)

    async def async_set_setting(self, setting: str, option: str) -> None:
        """Set camera setting."""
        await self.client.async_set_setting(setting, option)
        await self.async_request_refresh()

    async def async_start_preview(self) -> None:
        """Start preview state and the local MPEG-TS relay."""
        entry_id = self.config_entry.entry_id
        preview = await self.preview_manager.start(entry_id, port=8554)
        try:
            await self.client.async_start_preview(port=preview.port)
        except Exception:
            await self.preview_manager.stop(entry_id)
            preview = await self.preview_manager.start(entry_id)
            await self.client.async_start_preview(port=preview.port)
        await self.preview_manager.wait_for_datagram(entry_id, timeout=5)
        await self.async_request_refresh()

    async def async_stop_preview(self) -> None:
        """Stop preview state on the camera."""
        try:
            await self.client.async_stop_preview()
            await self.async_request_refresh()
        finally:
            await self.preview_manager.stop(self.config_entry.entry_id)

    def preview_status(self) -> dict[str, Any]:
        """Return the local preview relay status."""
        return self.preview_manager.status(self.config_entry.entry_id)

    async def async_shutdown(self) -> None:
        """Stop background tasks."""
        self._stop_keep_alive()
        await self.preview_manager.stop(self.config_entry.entry_id)

    def _ensure_keep_alive(self) -> None:
        """Start Keep Alive loop if enabled."""
        if self.config_entry.options.get("keep_alive", True) is False:
            return
        if self._keep_alive_task and not self._keep_alive_task.done():
            return
        self._keep_alive_task = self.hass.loop.create_task(self._keep_alive_loop())

    def _stop_keep_alive(self) -> None:
        """Cancel Keep Alive loop."""
        if self._keep_alive_task:
            self._keep_alive_task.cancel()
            self._keep_alive_task = None

    async def _keep_alive_loop(self) -> None:
        """Send periodic Keep Alive requests."""
        interval = self.config_entry.options.get(
            "keep_alive_interval", DEFAULT_KEEP_ALIVE_INTERVAL
        )
        while True:
            try:
                await asyncio.sleep(interval)
                await self.client.async_keep_alive()
            except asyncio.CancelledError:
                raise
            except Exception as err:  # noqa: BLE/HTTP libraries raise broad errors
                _LOGGER.debug("Keep Alive failed: %s", err)


def _ble_device_callback(hass: HomeAssistant, address: str):
    """Return a callback that resolves the latest HA BLEDevice for an address."""

    def resolve() -> Any | None:
        try:
            from homeassistant.components import bluetooth
        except Exception:
            return None
        return bluetooth.async_ble_device_from_address(hass, address, connectable=True)

    return resolve
