"""Select entities for OpenGoPro."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import get_coordinator
from .entity import OpenGoProEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up selects."""
    coordinator = get_coordinator(hass, entry.entry_id)
    async_add_entities([OpenGoProModeSelect(coordinator), OpenGoProPresetSelect(coordinator)])


class OpenGoProModeSelect(OpenGoProEntity, SelectEntity):
    """Camera mode select."""

    _attr_translation_key = "camera_mode"
    _attr_icon = "mdi:camera-control"

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "camera_mode")

    @property
    def options(self) -> list[str]:
        """Return available modes."""
        if self.coordinator.data:
            return self.coordinator.data.available_modes
        return ["video", "photo", "timelapse"]

    @property
    def current_option(self) -> str | None:
        """Return current mode."""
        return self.coordinator.data.current_mode if self.coordinator.data else None

    async def async_select_option(self, option: str) -> None:
        """Set mode."""
        await self.coordinator.async_set_mode(option)


class OpenGoProPresetSelect(OpenGoProEntity, SelectEntity):
    """Camera preset select."""

    _attr_translation_key = "preset"
    _attr_icon = "mdi:tune-variant"

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "preset")

    @property
    def available(self) -> bool:
        """Return availability."""
        return super().available and bool(self.options)

    @property
    def options(self) -> list[str]:
        """Return available presets."""
        if self.coordinator.data and self.coordinator.data.available_presets:
            return self.coordinator.data.available_presets
        return []

    @property
    def current_option(self) -> str | None:
        """Return current preset."""
        return self.coordinator.data.preset if self.coordinator.data else None

    async def async_select_option(self, option: str) -> None:
        """Set preset."""
        await self.coordinator.async_set_preset(option)
