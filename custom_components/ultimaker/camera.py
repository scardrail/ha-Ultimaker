"""Camera platform for Ultimaker integration."""
from __future__ import annotations

import asyncio
import logging
import aiohttp
from typing import Optional

from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import CoordinatorEntity

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
    
    camera = UltimakerCamera(
        hass=hass,
        coordinator=coordinator,
        name=f"{entry.data['name']} Camera",
        mjpeg_url=mjpeg_url,
        unique_id=f"{entry.entry_id}_camera",
        device_info=DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data["name"],
            manufacturer="Ultimaker",
        ),
    )
    
    async_add_entities([camera])
    _LOGGER.info("Added camera entity for Ultimaker")


class UltimakerCamera(CoordinatorEntity[UltimakerDataUpdateCoordinator], Camera):
    """An implementation of an MJPEG camera for Ultimaker printers."""

    _attr_supported_features = CameraEntityFeature.STREAM

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: UltimakerDataUpdateCoordinator,
        name: str,
        mjpeg_url: str,
        unique_id: str,
        device_info: DeviceInfo | None = None,
    ) -> None:
        """Initialize Ultimaker camera."""
        super().__init__(coordinator)
        Camera.__init__(self)
        
        self.hass = hass
        self._session = async_get_clientsession(hass)
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._attr_device_info = device_info
        self._attr_icon = "mdi:printer-3d"
        self._attr_has_entity_name = True
        self._mjpeg_url = mjpeg_url
        
        _LOGGER.debug("Initialized camera with MJPEG URL: %s", mjpeg_url)
    
    @property
    def available(self) -> bool:
        """Return if camera is available."""
        return self.coordinator.last_update_success

    async def stream_source(self) -> str | None:
        """Return the source of the stream."""
        if not self.available:
            return None
        return self._mjpeg_url
        
    async def async_camera_image(
        self, width: Optional[int] = None, height: Optional[int] = None
    ) -> Optional[bytes]:
        """Return a still image from the camera."""
        if not self.available:
            return None
            
        try:
            _LOGGER.debug("Getting camera image from %s", self._mjpeg_url)
            async with self._session.get(
                self._mjpeg_url,
                timeout=10,
            ) as resp:
                if resp.status != 200:
                    _LOGGER.error(
                        "Error getting camera image, status=%d", resp.status
                    )
                    return None
                    
                headers = resp.headers
                content_type = headers.get("Content-Type", "")
                _LOGGER.debug("Camera response Content-Type: %s", content_type)
                
                # Si c'est un flux MJPEG, on doit extraire une image
                if "multipart/x-mixed-replace" in content_type:
                    # Lire suffisamment pour obtenir au moins une image
                    data = await resp.content.read(100000)
                    start_marker = b"\xff\xd8"
                    end_marker = b"\xff\xd9"
                    
                    start_pos = data.find(start_marker)
                    if start_pos != -1:
                        end_pos = data.find(end_marker, start_pos)
                        if end_pos != -1:
                            _LOGGER.debug("Found JPEG image in MJPEG stream")
                            return data[start_pos : end_pos + 2]
                else:
                    # Si c'est une simple image
                    return await resp.read()
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout getting camera image")
        except aiohttp.ClientError as error:
            _LOGGER.error("Error getting camera image: %s", error)
        except Exception as error:
            _LOGGER.exception("Unexpected error getting camera image: %s", error)
            
        return None