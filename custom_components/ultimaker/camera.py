"""Camera platform for Ultimaker integration."""
from __future__ import annotations

import logging

from homeassistant.components.camera import Camera, CameraEntityFeature
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

    camera = UltimakerCamera(
        name=f"{entry.data['name']} Camera",
        mjpeg_url=mjpeg_url,
        unique_id=f"{entry.entry_id}_camera",
        device_info=DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data["name"],
            manufacturer="Ultimaker",
        ),
        coordinator=coordinator,
    )

    async_add_entities([camera])
    _LOGGER.info("Added camera entity for Ultimaker with stream URL: %s", mjpeg_url)


class UltimakerCamera(Camera):
    """Camera class for Ultimaker MJpeg stream."""

    _attr_supported_features = CameraEntityFeature.STREAM

    def __init__(
        self,
        name: str,
        mjpeg_url: str,
        unique_id: str,
        device_info: DeviceInfo | None = None,
        coordinator: UltimakerDataUpdateCoordinator | None = None,
    ) -> None:
        """Initialize Ultimaker camera component."""
        super().__init__()

        self._attr_name = name
        self._attr_unique_id = unique_id
        self._attr_device_info = device_info
        self._attr_icon = "mdi:printer-3d"
        self._mjpeg_url = mjpeg_url
        self.coordinator = coordinator  # Ajout du coordinator

        _LOGGER.debug("Initialized camera with MJPEG URL: %s", mjpeg_url)

    async def stream_source(self) -> str | None:
        """Return the source of the stream."""
        _LOGGER.debug("Returning stream source: %s", self._mjpeg_url)
        return self._mjpeg_url

    async def async_camera_image(self, width=None, height=None):
        """Return a still image from the camera."""
        # Pas d'implémentation pour l'instant, car on utilise MJPEG
        return None