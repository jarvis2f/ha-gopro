"""Switch entities for OpenGoPro."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
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
    """Set up switches."""
    async_add_entities([OpenGoProRecordingSwitch(get_coordinator(hass, entry.entry_id))])


class OpenGoProRecordingSwitch(OpenGoProEntity, SwitchEntity):
    """Recording switch."""

    _attr_translation_key = "recording"
    _attr_icon = "mdi:record-rec"

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "recording")

    @property
    def is_on(self) -> bool:
        """Return if camera is recording."""
        return bool(self.coordinator.data and self.coordinator.data.recording)

    async def async_turn_on(self, **kwargs) -> None:
        """Start recording/capture."""
        await self.coordinator.async_shutter(True)

    async def async_turn_off(self, **kwargs) -> None:
        """Stop recording/capture."""
        await self.coordinator.async_shutter(False)
