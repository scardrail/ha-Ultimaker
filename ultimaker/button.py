"""Support for Ultimaker buttons."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from homeassistant.components.button import (
    ButtonDeviceClass,
    ButtonEntity,
    ButtonEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import UltimakerDataUpdateCoordinator
from .const import DOMAIN

@dataclass
class UltimakerButtonEntityDescription(ButtonEntityDescription):
    """Class describing Ultimaker button entities."""

    press_fn: Callable[[dict[str, Any]], None] = None

BUTTONS: tuple[UltimakerButtonEntityDescription, ...] = (
    UltimakerButtonEntityDescription(
        key="pause",
        name="Pause",
        icon="mdi:pause",
        press_fn=lambda api, data: api.send_printer_command(
            data["cluster_info"]["cluster_id"],
            data["status"]["printers"][0]["uuid"],
            "pause",
        ),
    ),
    UltimakerButtonEntityDescription(
        key="resume",
        name="Resume",
        icon="mdi:play",
        press_fn=lambda api, data: api.send_printer_command(
            data["cluster_info"]["cluster_id"],
            data["status"]["printers"][0]["uuid"],
            "resume",
        ),
    ),
    UltimakerButtonEntityDescription(
        key="abort",
        name="Abort",
        icon="mdi:stop",
        device_class=ButtonDeviceClass.RESTART,
        press_fn=lambda api, data: api.send_printer_command(
            data["cluster_info"]["cluster_id"],
            data["status"]["printers"][0]["uuid"],
            "abort",
        ),
    ),
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ultimaker button based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    api = hass.data[DOMAIN][entry.entry_id]["api"]

    async_add_entities(
        UltimakerButton(
            coordinator=coordinator,
            api=api,
            description=description,
        )
        for description in BUTTONS
    )

class UltimakerButton(CoordinatorEntity, ButtonEntity):
    """Representation of a Ultimaker button."""

    entity_description: UltimakerButtonEntityDescription

    def __init__(
        self,
        coordinator: UltimakerDataUpdateCoordinator,
        api: Any,
        description: UltimakerButtonEntityDescription,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self._api = api
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.data['cluster_info']['cluster_id']}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.data["cluster_info"]["cluster_id"])},
            "name": coordinator.data["cluster_info"]["friendly_name"],
            "manufacturer": "Ultimaker",
            "model": coordinator.data["cluster_info"]["printer_type"],
            "sw_version": coordinator.data["cluster_info"].get("host_version", "Unknown"),
        }

    async def async_press(self) -> None:
        """Press the button."""
        if self.coordinator.data and self.entity_description.press_fn:
            await self.hass.async_add_executor_job(
                self.entity_description.press_fn,
                self._api,
                self.coordinator.data,
            ) 