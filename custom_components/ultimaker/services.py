"""Services for the Ultimaker integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SERVICE_PAUSE_PRINT = "pause_print"
SERVICE_RESUME_PRINT = "resume_print"
SERVICE_STOP_PRINT = "stop_print"
SERVICE_SET_BED_TEMP = "set_bed_temperature"
SERVICE_SET_HOTEND_TEMP = "set_hotend_temperature"

SERVICE_SCHEMA = vol.Schema(
    {
        vol.Required("entity_id"): cv.entity_id,
    }
)

SERVICE_TEMP_SCHEMA = SERVICE_SCHEMA.extend(
    {
        vol.Required("temperature"): vol.All(vol.Coerce(float), vol.Range(min=0, max=300)),
    }
)

async def async_setup_services(hass: HomeAssistant, config: ConfigType) -> None:
    """Set up services for Ultimaker integration."""

    async def async_pause_print(call: ServiceCall) -> None:
        """Pause the current print job."""
        coordinator = await _get_coordinator(hass, call)
        if coordinator:
            await coordinator.async_pause_print()

    async def async_resume_print(call: ServiceCall) -> None:
        """Resume the current print job."""
        coordinator = await _get_coordinator(hass, call)
        if coordinator:
            await coordinator.async_resume_print()

    async def async_stop_print(call: ServiceCall) -> None:
        """Stop the current print job."""
        coordinator = await _get_coordinator(hass, call)
        if coordinator:
            await coordinator.async_stop_print()

    async def async_set_bed_temp(call: ServiceCall) -> None:
        """Set the bed temperature."""
        coordinator = await _get_coordinator(hass, call)
        if coordinator:
            await coordinator.async_set_bed_temperature(call.data["temperature"])

    async def async_set_hotend_temp(call: ServiceCall) -> None:
        """Set the hotend temperature."""
        coordinator = await _get_coordinator(hass, call)
        if coordinator:
            await coordinator.async_set_hotend_temperature(call.data["temperature"])

    hass.services.async_register(
        DOMAIN, SERVICE_PAUSE_PRINT, async_pause_print, schema=SERVICE_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_RESUME_PRINT, async_resume_print, schema=SERVICE_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_STOP_PRINT, async_stop_print, schema=SERVICE_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_SET_BED_TEMP, async_set_bed_temp, schema=SERVICE_TEMP_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_SET_HOTEND_TEMP, async_set_hotend_temp, schema=SERVICE_TEMP_SCHEMA
    )

async def _get_coordinator(hass: HomeAssistant, call: ServiceCall) -> Any:
    """Get the coordinator for the service call."""
    entity_id = call.data["entity_id"]
    entry_id = entity_id.split(".")[1].split("_")[0]
    
    if entry_id not in hass.data[DOMAIN]:
        _LOGGER.error("Invalid entity_id: %s", entity_id)
        return None
        
    return hass.data[DOMAIN][entry_id] 