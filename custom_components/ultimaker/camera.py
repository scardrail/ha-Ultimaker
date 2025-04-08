"""Camera platform for Ultimaker integration."""
from __future__ import annotations

import logging

from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, API_CAMERA_STREAM
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
    # On essaie d'abord l'API officielle
    stream_url = f"http://{host}{API_CAMERA_STREAM}"
    # URL de fallback pour le flux MJPEG direct
    fallback_url = f"http://{host}:8080/?action=stream"

    _LOGGER.info("Setting up Ultimaker camera with primary URL: %s and fallback URL: %s", stream_url, fallback_url)

    camera = UltimakerCamera(
        name=f"{entry.data['name']} Camera",
        stream_url=stream_url,
        fallback_url=fallback_url,
        unique_id=f"{entry.entry_id}_camera",
        device_info=DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data["name"],
            manufacturer="Ultimaker",
        ),
        coordinator=coordinator,
    )

    async_add_entities([camera])


class UltimakerCamera(Camera):
    """Camera class for Ultimaker."""

    _attr_supported_features = CameraEntityFeature.STREAM

    def __init__(
        self,
        name: str,
        stream_url: str,
        fallback_url: str,
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
        self._stream_url = stream_url
        self._fallback_url = fallback_url
        self._use_fallback = False
        self.coordinator = coordinator

        _LOGGER.debug("Initialized camera with stream URL: %s", self._stream_url)

    async def stream_source(self) -> str | None:
        """Return the source of the stream."""
        if self._use_fallback:
            _LOGGER.debug("Using fallback stream URL: %s", self._fallback_url)
            return self._fallback_url
            
        try:
            # Vérifie si le flux principal est accessible
            if self.coordinator and self.coordinator.data.get("printer", {}).get("camera", {}).get("feed"):
                _LOGGER.debug("Using API stream URL: %s", self._stream_url)
                return self._stream_url
            else:
                _LOGGER.debug("No camera feed in API response, switching to fallback URL")
                self._use_fallback = True
                return self._fallback_url
        except Exception as err:
            _LOGGER.warning("Error accessing camera feed, switching to fallback URL: %s", err)
            self._use_fallback = True
            return self._fallback_url

    async def async_camera_image(self, width=None, height=None):
        """Return a still image from the camera."""
        # Pour l'instant on utilise uniquement le flux MJPEG
        return None