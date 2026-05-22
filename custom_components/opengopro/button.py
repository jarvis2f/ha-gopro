"""Button entities for OpenGoPro."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Awaitable, Callable

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import get_coordinator
from .coordinator import OpenGoProCoordinator
from .entity import OpenGoProEntity


@dataclass(frozen=True, kw_only=True)
class OpenGoProButtonDescription(ButtonEntityDescription):
    """OpenGoPro button description."""

    press_fn: Callable[[OpenGoProCoordinator], Awaitable[None]]


BUTTONS = (
    OpenGoProButtonDescription(key="wake", translation_key="wake", icon="mdi:power", press_fn=lambda c: c.async_wake()),
    OpenGoProButtonDescription(key="sleep", translation_key="sleep", icon="mdi:power-sleep", press_fn=lambda c: c.async_sleep()),
    OpenGoProButtonDescription(key="reconnect", translation_key="reconnect", icon="mdi:bluetooth-connect", press_fn=lambda c: c.async_wake()),
    OpenGoProButtonDescription(key="shutter", translation_key="shutter", icon="mdi:camera-iris", press_fn=lambda c: c.async_shutter(True)),
    OpenGoProButtonDescription(key="refresh_media", translation_key="refresh_media", icon="mdi:folder-refresh", press_fn=lambda c: c.async_refresh_media()),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up OpenGoPro buttons."""
    coordinator = get_coordinator(hass, entry.entry_id)
    async_add_entities(OpenGoProButton(coordinator, description) for description in BUTTONS)


class OpenGoProButton(OpenGoProEntity, ButtonEntity):
    """OpenGoPro button."""

    entity_description: OpenGoProButtonDescription

    def __init__(
        self,
        coordinator: OpenGoProCoordinator,
        description: OpenGoProButtonDescription,
    ) -> None:
        super().__init__(coordinator, description.key)
        self.entity_description = description

    async def async_press(self) -> None:
        """Press the button."""
        await self.entity_description.press_fn(self.coordinator)
