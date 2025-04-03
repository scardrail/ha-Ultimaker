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
        value_fn=lambda data: data["print_job"].get("state") == "printing",
    ),
    UltimakerBinarySensorEntityDescription(
        key="paused",
        name="Paused",
        device_class=BinarySensorDeviceClass.PROBLEM,
        value_fn=lambda data: data["print_job"].get("state") == "paused",
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

class UltimakerBinarySensor(BinarySensorEntity):
    """Representation of an Ultimaker binary sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: UltimakerDataUpdateCoordinator,
        description: UltimakerBinarySensorEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the binary sensor."""
        self.coordinator = coordinator
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data["name"],
            manufacturer="Ultimaker",
        )

    @property
    def is_on(self) -> bool:
        """Return the state of the binary sensor."""
        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.coordinator.async_add_listener(self.async_write_ha_state)

    async def async_will_remove_from_hass(self) -> None:
        """When entity will be removed from hass."""
        await super().async_will_remove_from_hass()
        self.coordinator.async_remove_listener(self.async_write_ha_state) 