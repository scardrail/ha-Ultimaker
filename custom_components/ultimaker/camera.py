"""Camera platform for Ultimaker integration."""
from __future__ import annotations

import logging
from homeassistant.components.camera import Camera
from homeassistant.components.mjpeg.camera import MjpegCamera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import UltimakerDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ultimaker camera based on a config entry."""
    coordinator: UltimakerDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    host = entry.data["host"]
    mjpeg_url = f"http://{host}:8080/?action=stream"
    
    _LOGGER.info("Setting up Ultimaker camera with MJPEG URL: %s", mjpeg_url)
    
    camera = UltimakerMjpegCamera(
        name=f"{entry.data['name']} Camera",
        mjpeg_url=mjpeg_url,
        still_image_url=None,
        unique_id=f"{entry.entry_id}_camera",
        device_info=DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data["name"],
            manufacturer="Ultimaker",
        ),
    )
    
    async_add_entities([camera])
    _LOGGER.info("Added MJPEG camera entity for Ultimaker")


class UltimakerMjpegCamera(MjpegCamera):
    """An implementation of an MJPEG IP camera for Ultimaker printers."""

    def __init__(
        self,
        name: str,
        mjpeg_url: str,
        still_image_url: str | None,
        unique_id: str,
        device_info: DeviceInfo | None = None,
    ) -> None:
        """Initialize Ultimaker MJPEG camera."""
        super().__init__(
            name=name, 
            mjpeg_url=mjpeg_url, 
            still_image_url=still_image_url, 
            authentication="basic", 
            username=None, 
            password=None, 
            verify_ssl=False
        )
        
        self._attr_unique_id = unique_id
        self._attr_device_info = device_info
        self._attr_icon = "mdi:printer-3d"
        self._attr_brand = "Ultimaker"
        self._mjpeg_url = mjpeg_url
        
        _LOGGER.debug("Initialized MJPEG camera with URL: %s", mjpeg_url)