"""Button platform for Ultimaker integration."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

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

class UltimakerButton(ButtonEntity):
    """Representation of an Ultimaker button."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: UltimakerDataUpdateCoordinator,
        description: UltimakerButtonEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the button."""
        self.coordinator = coordinator
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data["name"],
            manufacturer="Ultimaker",
        )

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.entity_description.press_fn(self.coordinator)

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