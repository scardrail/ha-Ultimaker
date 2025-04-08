"""Camera platform for Ultimaker integration."""
from __future__ import annotations

import logging
import aiohttp
import asyncio
from typing import cast

from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.components.mjpeg.camera import MjpegCamera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import CONF_HOST

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
    host = entry.data[CONF_HOST]

    mjpeg_url = f"http://{host}:8080/?action=stream"
    still_url = f"http://{host}:8080/?action=snapshot"

    camera = UltimakerCamera(
        name=f"{entry.data['name']} Camera",
        unique_id=f"{entry.entry_id}_camera",
        device_info=DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data["name"],
            manufacturer="Ultimaker",
        ),
        mjpeg_url=mjpeg_url,
        still_url=still_url,
        coordinator=coordinator,
    )

    async_add_entities([camera])


class UltimakerCamera(MjpegCamera):
    """Camera class for Ultimaker."""

    _attr_supported_features = CameraEntityFeature.STREAM

    def __init__(
        self,
        name: str,
        unique_id: str,
        device_info: DeviceInfo | None = None,
        mjpeg_url: str | None = None,
        still_url: str | None = None,
        coordinator: UltimakerDataUpdateCoordinator | None = None,
    ) -> None:
        """Initialize Ultimaker camera component."""
        super().__init__(
            name=name,
            still_image_url=still_url,
            mjpeg_url=mjpeg_url,
            verify_ssl=False,
        )

        self._attr_unique_id = unique_id
        self._attr_device_info = device_info
        self._attr_icon = "mdi:printer-3d"
        self.coordinator = coordinator
        self._mjpeg_url = mjpeg_url
        self._still_url = still_url

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return a still image response from the camera."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self._still_url) as response:
                    if response.status != 200:
                        return None
                    image = await response.read()
                    return image
        except (asyncio.TimeoutError, aiohttp.ClientError) as err:
            _LOGGER.error("Error getting camera image: %s", err)
            return None

    async def stream_source(self) -> str | None:
        """Return the MJPEG stream source."""
        return self._mjpeg_url