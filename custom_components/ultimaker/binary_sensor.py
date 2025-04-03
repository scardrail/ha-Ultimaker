"""Binary sensor platform for Ultimaker integration."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import UltimakerDataUpdateCoordinator

@dataclass
class UltimakerBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes Ultimaker binary sensor entity."""

    value_fn: Any = None

BINARY_SENSOR_TYPES: tuple[UltimakerBinarySensorEntityDescription, ...] = (
    UltimakerBinarySensorEntityDescription(
        key="printing",
        name="Printing",
        device_class=BinarySensorDeviceClass.RUNNING,
        value_fn=lambda data: data["printer"].get("status") == "printing",
    ),
    UltimakerBinarySensorEntityDescription(
        key="paused",
        name="Paused",
        device_class=BinarySensorDeviceClass.RUNNING,
        value_fn=lambda data: data["printer"].get("status") == "paused",
    ),
    UltimakerBinarySensorEntityDescription(
        key="error",
        name="Error",
        device_class=BinarySensorDeviceClass.PROBLEM,
        value_fn=lambda data: data["printer"].get("status") == "error",
    ),
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ultimaker binary sensors based on a config entry."""
    coordinator: UltimakerDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        UltimakerBinarySensor(coordinator, description, entry)
        for description in BINARY_SENSOR_TYPES
    )

class UltimakerBinarySensor(CoordinatorEntity[UltimakerDataUpdateCoordinator], BinarySensorEntity):
    """Representation of an Ultimaker binary sensor."""

    entity_description: UltimakerBinarySensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: UltimakerDataUpdateCoordinator,
        description: UltimakerBinarySensorEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data["name"],
            manufacturer="Ultimaker",
        )

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        return self.entity_description.value_fn(self.coordinator.data) 