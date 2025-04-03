"""Support for Ultimaker binary sensors."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import UltimakerDataUpdateCoordinator
from .const import DOMAIN

@dataclass
class UltimakerBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Class describing Ultimaker binary sensor entities."""

    is_on_fn: Callable[[dict[str, Any]], bool] = None

BINARY_SENSORS: tuple[UltimakerBinarySensorEntityDescription, ...] = (
    UltimakerBinarySensorEntityDescription(
        key="is_printing",
        name="Is Printing",
        device_class=BinarySensorDeviceClass.RUNNING,
        is_on_fn=lambda data: any(
            printer.get("status") == "printing"
            for printer in data.get("status", {}).get("printers", [])
        ),
    ),
    UltimakerBinarySensorEntityDescription(
        key="is_online",
        name="Online",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        is_on_fn=lambda data: data.get("cluster_info", {}).get("is_online", False),
    ),
    UltimakerBinarySensorEntityDescription(
        key="maintenance_required",
        name="Maintenance Required",
        device_class=BinarySensorDeviceClass.PROBLEM,
        is_on_fn=lambda data: any(
            printer.get("maintenance_required", False)
            for printer in data.get("status", {}).get("printers", [])
        ),
    ),
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ultimaker binary sensor based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    async_add_entities(
        UltimakerBinarySensor(
            coordinator=coordinator,
            description=description,
        )
        for description in BINARY_SENSORS
    )

class UltimakerBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Ultimaker binary sensor."""

    entity_description: UltimakerBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: UltimakerDataUpdateCoordinator,
        description: UltimakerBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.data['cluster_info']['cluster_id']}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.data["cluster_info"]["cluster_id"])},
            "name": coordinator.data["cluster_info"]["friendly_name"],
            "manufacturer": "Ultimaker",
            "model": coordinator.data["cluster_info"]["printer_type"],
            "sw_version": coordinator.data["cluster_info"].get("host_version", "Unknown"),
        }

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        if self.coordinator.data and self.entity_description.is_on_fn:
            return self.entity_description.is_on_fn(self.coordinator.data)
        return None 