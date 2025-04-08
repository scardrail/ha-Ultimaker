"""Button platform for Ultimaker integration."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.button import (
    ButtonEntity,
    ButtonEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import UltimakerDataUpdateCoordinator

@dataclass
class UltimakerButtonEntityDescription(ButtonEntityDescription):
    """Describes Ultimaker button entity."""

    press_fn: Any = None

BUTTON_TYPES: tuple[UltimakerButtonEntityDescription, ...] = (
    UltimakerButtonEntityDescription(
        key="pause_print",
        name="Pause Print",
        icon="mdi:pause",
        press_fn=lambda coordinator: coordinator.async_pause_print(),
    ),
    UltimakerButtonEntityDescription(
        key="resume_print",
        name="Resume Print",
        icon="mdi:play",
        press_fn=lambda coordinator: coordinator.async_resume_print(),
    ),
    UltimakerButtonEntityDescription(
        key="stop_print",
        name="Stop Print",
        icon="mdi:stop",
        press_fn=lambda coordinator: coordinator.async_stop_print(),
    ),
    UltimakerButtonEntityDescription(
        key="light_on",
        name="Light On",
        icon="mdi:lightbulb-on",
        press_fn=lambda coordinator: coordinator.async_set_led({"brightness": 100, "saturation": 0, "hue": 0}),
    ),
    UltimakerButtonEntityDescription(
        key="light_off",
        name="Light Off",
        icon="mdi:lightbulb-off",
        press_fn=lambda coordinator: coordinator.async_set_led({"brightness": 0, "saturation": 0, "hue": 0}),
    ),
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ultimaker buttons based on a config entry."""
    coordinator: UltimakerDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        UltimakerButton(coordinator, description, entry)
        for description in BUTTON_TYPES
    )

class UltimakerButton(CoordinatorEntity[UltimakerDataUpdateCoordinator], ButtonEntity):
    """Representation of an Ultimaker button."""

    entity_description: UltimakerButtonEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: UltimakerDataUpdateCoordinator,
        description: UltimakerButtonEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data["name"],
            manufacturer="Ultimaker",
        )

    async def async_press(self) -> None:
        """Press the button."""
        await self.entity_description.press_fn(self.coordinator) 