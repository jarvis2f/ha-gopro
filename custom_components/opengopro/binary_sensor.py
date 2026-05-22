"""Binary sensor entities for OpenGoPro."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import get_coordinator
from .client import CameraSnapshot, ConnectionPhase
from .coordinator import OpenGoProCoordinator
from .entity import OpenGoProEntity


@dataclass(frozen=True, kw_only=True)
class OpenGoProBinarySensorDescription(BinarySensorEntityDescription):
    """OpenGoPro binary sensor description."""

    value_fn: Callable[[CameraSnapshot], bool | None]


BINARY_SENSORS = (
    OpenGoProBinarySensorDescription(
        key="connected",
        translation_key="connected",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        value_fn=lambda data: data.phase != ConnectionPhase.DISCONNECTED,
    ),
    OpenGoProBinarySensorDescription(
        key="http_ready",
        translation_key="http_ready",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        value_fn=lambda data: data.phase == ConnectionPhase.HTTP_READY,
    ),
    OpenGoProBinarySensorDescription(
        key="overheating",
        translation_key="overheating",
        device_class=BinarySensorDeviceClass.PROBLEM,
        value_fn=lambda data: data.overheating,
    ),
    OpenGoProBinarySensorDescription(
        key="sd_card_present",
        translation_key="sd_card_present",
        device_class=BinarySensorDeviceClass.PLUG,
        value_fn=lambda data: data.sd_card_present,
    ),
    OpenGoProBinarySensorDescription(
        key="recording",
        translation_key="recording",
        icon="mdi:record-rec",
        value_fn=lambda data: data.recording,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up binary sensors."""
    coordinator = get_coordinator(hass, entry.entry_id)
    async_add_entities(
        OpenGoProBinarySensor(coordinator, description)
        for description in BINARY_SENSORS
    )


class OpenGoProBinarySensor(OpenGoProEntity, BinarySensorEntity):
    """OpenGoPro binary sensor."""

    entity_description: OpenGoProBinarySensorDescription

    def __init__(
        self,
        coordinator: OpenGoProCoordinator,
        description: OpenGoProBinarySensorDescription,
    ) -> None:
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def is_on(self) -> bool | None:
        """Return binary sensor state."""
        if not self.coordinator.data:
            return None
        return self.entity_description.value_fn(self.coordinator.data)
