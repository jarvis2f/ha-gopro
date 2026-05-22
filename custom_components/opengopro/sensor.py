"""Sensor entities for OpenGoPro."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfInformation
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import get_coordinator
from .client import CameraSnapshot
from .coordinator import OpenGoProCoordinator
from .entity import OpenGoProEntity


@dataclass(frozen=True, kw_only=True)
class OpenGoProSensorDescription(SensorEntityDescription):
    """OpenGoPro sensor description."""

    value_fn: Callable[[CameraSnapshot], Any]


SENSORS = (
    OpenGoProSensorDescription(
        key="battery",
        translation_key="battery",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        value_fn=lambda data: data.battery,
    ),
    OpenGoProSensorDescription(
        key="remaining_storage",
        translation_key="remaining_storage",
        native_unit_of_measurement=UnitOfInformation.MEGABYTES,
        icon="mdi:sd",
        value_fn=lambda data: data.remaining_storage,
    ),
    OpenGoProSensorDescription(
        key="current_mode",
        translation_key="current_mode",
        icon="mdi:camera-control",
        value_fn=lambda data: data.current_mode,
    ),
    OpenGoProSensorDescription(
        key="temperature",
        translation_key="temperature",
        icon="mdi:thermometer",
        value_fn=lambda data: data.temperature,
    ),
    OpenGoProSensorDescription(
        key="recording_state",
        translation_key="recording_state",
        icon="mdi:record-rec",
        value_fn=lambda data: "recording" if data.recording else "idle",
    ),
    OpenGoProSensorDescription(
        key="sd_card_status",
        translation_key="sd_card_status",
        icon="mdi:sd",
        value_fn=lambda data: data.sd_card_status,
    ),
    OpenGoProSensorDescription(
        key="wifi_status",
        translation_key="wifi_status",
        icon="mdi:wifi",
        value_fn=lambda data: "on" if data.wifi_enabled else "off",
    ),
    OpenGoProSensorDescription(
        key="ble_status",
        translation_key="ble_status",
        icon="mdi:bluetooth",
        value_fn=lambda data: "connected" if data.ble_connected else "disconnected",
    ),
    OpenGoProSensorDescription(
        key="model",
        translation_key="model",
        icon="mdi:camera",
        value_fn=lambda data: data.model,
    ),
    OpenGoProSensorDescription(
        key="firmware",
        translation_key="firmware",
        icon="mdi:chip",
        value_fn=lambda data: data.firmware,
    ),
    OpenGoProSensorDescription(
        key="connection_phase",
        translation_key="connection_phase",
        icon="mdi:lan-connect",
        value_fn=lambda data: data.phase.value,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors."""
    coordinator = get_coordinator(hass, entry.entry_id)
    async_add_entities(OpenGoProSensor(coordinator, description) for description in SENSORS)


class OpenGoProSensor(OpenGoProEntity, SensorEntity):
    """OpenGoPro sensor."""

    entity_description: OpenGoProSensorDescription

    def __init__(
        self,
        coordinator: OpenGoProCoordinator,
        description: OpenGoProSensorDescription,
    ) -> None:
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def native_value(self) -> Any:
        """Return the sensor value."""
        if not self.coordinator.data:
            return None
        return self.entity_description.value_fn(self.coordinator.data)
