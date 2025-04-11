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
        key="ip_address",
        name="IP Address",
        icon="mdi:ip-network",
        value_fn=lambda data: data.get("system", {}).get("hostname", "unknown"),
    ),
    UltimakerSensorEntityDescription(
        key="connection_mode",
        name="Connection Mode",
        icon="mdi:connection",
        value_fn=lambda data: (
            "LAN" 
            if data.get("printer", {}).get("network", {}).get("ethernet", {}).get("connected") 
            else "WiFi" 
            if data.get("printer", {}).get("network", {}).get("wifi", {}).get("connected") 
            else "Unknown"
        ),
    ),
    UltimakerSensorEntityDescription(
        key="wifi_signal",
        name="WiFi Signal",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:wifi",
        value_fn=lambda data: (
            next(
                (
                    network["strength"] 
                    for network in data.get("printer", {}).get("network", {}).get("wifi_networks", []) 
                    if network["ssid"] == data.get("printer", {}).get("network", {}).get("wifi", {}).get("ssid")
                ), 
                0
            ) if data.get("printer", {}).get("network", {}).get("wifi", {}).get("connected") 
            else 0
        ),
    ),
    
    UltimakerSensorEntityDescription(
        key="print_start_time",
        name="Print Start Time",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda data: data.get("print_job", {}).get("datetime_started"),
    ),
    UltimakerSensorEntityDescription(
        key="print_end_time",
        name="Print End Time",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda data: data.get("print_job", {}).get("datetime_finished"),
    ),
    UltimakerSensorEntityDescription(
        key="print_speed",
        name="Print Speed",
        icon="mdi:printer-3d-nozzle",
        native_unit_of_measurement="mm/s",
        value_fn=lambda data: (
            data.get("printer", {}).get("heads", [{}])[0].get("max_speed", {}).get("x", 0)
            if data.get("printer", {}).get("heads") 
            else 0
        ),
    ),
    UltimakerSensorEntityDescription(
        key="status",
        name="Status",
        icon="mdi:printer-3d",
        value_fn=lambda data: data.get("printer", {}).get("status", "unknown"),
    ),
    UltimakerSensorEntityDescription(
        key="progress",
        name="Progress",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:progress-clock",
        value_fn=lambda data: (
            data.get("print_job", {}).get("progress", 0) * 100 
            if data.get("print_job", {}).get("progress") is not None 
            else 0
        ),
    ),
    UltimakerSensorEntityDescription(
        key="bed_temperature",
        name="Bed Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("printer", {}).get("bed", {}).get("temperature", {}).get("current", 0),
    ),
    UltimakerSensorEntityDescription(
        key="bed_target",
        name="Bed Target Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("printer", {}).get("bed", {}).get("temperature", {}).get("target", 0),
    ),
    UltimakerSensorEntityDescription(
        key="hotend_temperature",
        name="Hotend Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: (
            data.get("printer", {}).get("heads", [{}])[0]
            .get("extruders", [{}])[0]
            .get("hotend", {})
            .get("temperature", {})
            .get("current", 0)
            if data.get("printer", {}).get("heads") 
            else 0
        ),
    ),
    UltimakerSensorEntityDescription(
        key="hotend_target",
        name="Hotend Target Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: (
            data.get("printer", {}).get("heads", [{}])[0]
            .get("extruders", [{}])[0]
            .get("hotend", {})
            .get("temperature", {})
            .get("target", 0)
            if data.get("printer", {}).get("heads") 
            else 0
        ),
    ),
    UltimakerSensorEntityDescription(
        key="time_elapsed",
        name="Time Elapsed",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        icon="mdi:clock-outline",
        value_fn=lambda data: data.get("print_job", {}).get("time_elapsed", 0),
    ),
    UltimakerSensorEntityDescription(
        key="time_total",
        name="Time Total",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        icon="mdi:clock-outline",
        value_fn=lambda data: data.get("print_job", {}).get("time_total", 0),
    ),
    UltimakerSensorEntityDescription(
        key="filament_1",
        name="Filament 1",
        icon="mdi:printer-3d-nozzle",
        value_fn=lambda data: (
            f"{data.get('printer', {}).get('heads', [{}])[0].get('extruders', [{}])[0].get('active_material', {}).get('data', {}).get('brand', 'Unknown')} "
            f"{data.get('printer', {}).get('heads', [{}])[0].get('extruders', [{}])[0].get('active_material', {}).get('data', {}).get('material', 'Unknown')}"
            if isinstance(data.get('printer', {}).get('heads', [{}])[0].get('extruders', [{}])[0].get('active_material', {}).get('data'), dict)
            else "No Material"
        ),
    ),
    UltimakerSensorEntityDescription(
        key="filament_1_remaining",
        name="Filament 1 Remaining",
        icon="mdi:printer-3d-nozzle",
        native_unit_of_measurement="mm",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: (
            data.get("printer", {})
            .get("heads", [{}])[0]
            .get("extruders", [{}])[0]
            .get("active_material", {})
            .get("length_remaining", 0)
        ),
    ),
    UltimakerSensorEntityDescription(
        key="filament_2",
        name="Filament 2",
        icon="mdi:printer-3d-nozzle",
        value_fn=lambda data: (
            f"{data.get('printer', {}).get('heads', [{}])[0].get('extruders', [{}])[1].get('active_material', {}).get('data', {}).get('brand', 'Unknown')} "
            f"{data.get('printer', {}).get('heads', [{}])[0].get('extruders', [{}])[1].get('active_material', {}).get('data', {}).get('material', 'Unknown')}"
            if len(data.get("printer", {}).get("heads", [{}])[0].get("extruders", [])) > 1 and
            isinstance(data.get('printer', {}).get('heads', [{}])[0].get('extruders', [{}])[1].get('active_material', {}).get('data'), dict)
            else None
        ),
    ),
    UltimakerSensorEntityDescription(
        key="filament_2_remaining",
        name="Filament 2 Remaining",
        icon="mdi:printer-3d-nozzle",
        native_unit_of_measurement="mm",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: (
            data.get("printer", {})
            .get("heads", [{}])[0]
            .get("extruders", [{}])[1]
            .get("active_material", {})
            .get("length_remaining", 0)
            if len(data.get("printer", {}).get("heads", [{}])[0].get("extruders", [])) > 1
            else None
        ),
    ),
    UltimakerSensorEntityDescription(
        key="filament_1_color",
        name="Filament 1 Color",
        icon="mdi:palette",
        value_fn=lambda data: (
            data.get("printer", {})
            .get("heads", [{}])[0]
            .get("extruders", [{}])[0]
            .get("active_material", {})
            .get("data", {})
            .get("color", "Unknown")
            if isinstance(data.get('printer', {}).get('heads', [{}])[0].get('extruders', [{}])[0].get('active_material', {}).get('data'), dict)
            else "Unknown"
        ),
    ),
    UltimakerSensorEntityDescription(
        key="filament_2_color",
        name="Filament 2 Color",
        icon="mdi:palette",
        value_fn=lambda data: (
            data.get("printer", {})
            .get("heads", [{}])[0]
            .get("extruders", [{}])[1]
            .get("active_material", {})
            .get("data", {})
            .get("color", "Unknown")
            if len(data.get("printer", {}).get("heads", [{}])[0].get("extruders", [])) > 1 and
            isinstance(data.get('printer', {}).get('heads', [{}])[0].get('extruders', [{}])[1].get('active_material', {}).get('data'), dict)
            else None
        ),
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
        try:
            return self.entity_description.value_fn(self.coordinator.data)
        except (KeyError, IndexError, TypeError):
            return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        data = self.coordinator.data
        if not data:
            return {}

        printer_data = data.get("printer", {})
        bed_temp = printer_data.get("bed", {}).get("temperature", {})
        hotend_temp = (
            printer_data.get("heads", [{}])[0]
            .get("extruders", [{}])[0]
            .get("hotend", {})
            .get("temperature", {})
        )
        print_job = data.get("print_job", {})

        return {
            ATTR_BED_TEMPERATURE: bed_temp.get("current"),
            ATTR_BED_TARGET: bed_temp.get("target"),
            ATTR_HOTEND_TEMPERATURE: hotend_temp.get("current"),
            ATTR_HOTEND_TARGET: hotend_temp.get("target"),
            ATTR_PROGRESS: print_job.get("progress"),
            ATTR_PRINT_TIME: print_job.get("time_elapsed"),
            ATTR_ESTIMATED_TIME: print_job.get("time_total"),
            ATTR_FILAMENT_USED: None,  # Non disponible dans l'API actuelle
            ATTR_LAYER: None,  # Non disponible dans l'API actuelle
            ATTR_LAYER_COUNT: None,  # Non disponible dans l'API actuelle
        }
