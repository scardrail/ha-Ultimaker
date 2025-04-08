"""Camera platform for Ultimaker integration."""
from __future__ import annotations

import logging
from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
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
    async_add_entities([UltimakerCamera(coordinator, entry)])
    _LOGGER.info("Added camera entity for Ultimaker")

class UltimakerCamera(CoordinatorEntity[UltimakerDataUpdateCoordinator], Camera):
    """Representation of an Ultimaker camera."""

    _attr_has_entity_name = True
    _attr_supported_features = CameraEntityFeature.STREAM
    _attr_name = "Camera"
    _attr_icon = "mdi:printer-3d"
    _attr_brand = "Ultimaker"

    def __init__(
        self,
        coordinator: UltimakerDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the camera."""
        super().__init__(coordinator)
        Camera.__init__(self)
        
        self._attr_unique_id = f"{entry.entry_id}_camera"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data["name"],
            manufacturer="Ultimaker",
        )
        self._host = entry.data["host"]
        self._mjpeg_url = f"http://{self._host}:8080/?action=stream"
        _LOGGER.debug("Initialized camera for %s with MJPEG URL: %s", self._host, self._mjpeg_url)

    @property
    def available(self) -> bool:
        """Return if camera is available."""
        return self.coordinator.last_update_success

    @property
    def is_streaming(self) -> bool:
        """Return true if the device is streaming."""
        return self.available

    @property
    def is_recording(self) -> bool:
        """Return true if the device is recording."""
        return False

    async def stream_source(self) -> str | None:
        """Return the source of the stream."""
        if not self.available:
            return None
        return self._mjpeg_url

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return a still image from the camera."""
        if not self.available:
            return None

        try:
            async with self.coordinator.session.get(
                self._mjpeg_url,
                headers={"Accept": "image/jpeg, multipart/x-mixed-replace"},
                timeout=5,
            ) as response:
                if response.status != 200:
                    _LOGGER.error("Failed to get camera image, status: %s", response.status)
                    return None

                # Pour un flux MJPEG, nous devons lire jusqu'à trouver une image complète
                content_type = response.headers.get("Content-Type", "")
                if "multipart/x-mixed-replace" in content_type:
                    # Lire le début du flux pour obtenir la première image
                    chunk = await response.content.read(100000)
                    if chunk:
                        # Chercher le début et la fin d'une image JPEG
                        start = chunk.find(b"\xff\xd8")
                        end = chunk.find(b"\xff\xd9")
                        if start != -1 and end != -1:
                            return chunk[start:end+2]
                else:
                    # Si ce n'est pas un flux multipart, essayer de lire directement
                    return await response.read()

        except Exception as err:
            _LOGGER.error("Error getting camera image: %s", err, exc_info=True)
        
        return None