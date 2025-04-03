"""Sensor platform for Ultimaker integration."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfTemperature,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_BED_TEMPERATURE,
    ATTR_BED_TARGET,
    ATTR_HOTEND_TEMPERATURE,
    ATTR_HOTEND_TARGET,
    ATTR_PROGRESS,
    ATTR_PRINT_TIME,
    ATTR_ESTIMATED_TIME,
    ATTR_FILAMENT_USED,
    ATTR_LAYER,
    ATTR_LAYER_COUNT,
    DOMAIN,
)
from .coordinator import UltimakerDataUpdateCoordinator

@dataclass
class UltimakerSensorEntityDescription(SensorEntityDescription):
    """Describes Ultimaker sensor entity."""

    value_fn: Any = None

SENSOR_TYPES: tuple[UltimakerSensorEntityDescription, ...] = (
    UltimakerSensorEntityDescription(
        key="status",
        name="Status",
        icon="mdi:printer-3d",
        value_fn=lambda data: data["printer"].get("status", "unknown"),
    ),
    UltimakerSensorEntityDescription(
        key="progress",
        name="Progress",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:progress-clock",
        value_fn=lambda data: data["print_job"].get("progress", 0),
    ),
    UltimakerSensorEntityDescription(
        key="bed_temperature",
        name="Bed Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["printer"].get("bed", {}).get("current", 0),
    ),
    UltimakerSensorEntityDescription(
        key="bed_target",
        name="Bed Target Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["printer"].get("bed", {}).get("target", 0),
    ),
    UltimakerSensorEntityDescription(
        key="hotend_temperature",
        name="Hotend Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["printer"].get("heads", [{}])[0].get("extruders", [{}])[0].get("hotend", {}).get("current", 0),
    ),
    UltimakerSensorEntityDescription(
        key="hotend_target",
        name="Hotend Target Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["printer"].get("heads", [{}])[0].get("extruders", [{}])[0].get("hotend", {}).get("target", 0),
    ),
    UltimakerSensorEntityDescription(
        key="print_time",
        name="Print Time",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        icon="mdi:clock-outline",
        value_fn=lambda data: data["print_job"].get("print_time", 0),
    ),
    UltimakerSensorEntityDescription(
        key="estimated_time",
        name="Estimated Time",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        icon="mdi:clock-outline",
        value_fn=lambda data: data["print_job"].get("estimated_time", 0),
    ),
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ultimaker sensors based on a config entry."""
    coordinator: UltimakerDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        UltimakerSensor(coordinator, description, entry)
        for description in SENSOR_TYPES
    )

class UltimakerSensor(CoordinatorEntity[UltimakerDataUpdateCoordinator], SensorEntity):
    """Representation of an Ultimaker sensor."""

    entity_description: UltimakerSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: UltimakerDataUpdateCoordinator,
        description: UltimakerSensorEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data["name"],
            manufacturer="Ultimaker",
        )

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        data = self.coordinator.data
        return {
            ATTR_BED_TEMPERATURE: data["printer"].get("bed", {}).get("current"),
            ATTR_BED_TARGET: data["printer"].get("bed", {}).get("target"),
            ATTR_HOTEND_TEMPERATURE: data["printer"].get("heads", [{}])[0].get("extruders", [{}])[0].get("hotend", {}).get("current"),
            ATTR_HOTEND_TARGET: data["printer"].get("heads", [{}])[0].get("extruders", [{}])[0].get("hotend", {}).get("target"),
            ATTR_PROGRESS: data["print_job"].get("progress"),
            ATTR_PRINT_TIME: data["print_job"].get("print_time"),
            ATTR_ESTIMATED_TIME: data["print_job"].get("estimated_time"),
            ATTR_FILAMENT_USED: data["print_job"].get("filament_used"),
            ATTR_LAYER: data["print_job"].get("layer"),
            ATTR_LAYER_COUNT: data["print_job"].get("layer_count"),
        }
