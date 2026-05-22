"""Base entity helpers for OpenGoPro."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER
from .coordinator import OpenGoProCoordinator


class OpenGoProEntity(CoordinatorEntity[OpenGoProCoordinator]):
    """Base OpenGoPro entity."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: OpenGoProCoordinator, key: str) -> None:
        super().__init__(coordinator)
        self._key = key
        address = coordinator.config_entry.unique_id or coordinator.client.ble_address
        self._attr_unique_id = f"{address}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, address)},
            name=coordinator.config_entry.title,
            manufacturer=MANUFACTURER,
            model=coordinator.data.model if coordinator.data else None,
            sw_version=coordinator.data.firmware if coordinator.data else None,
        )
