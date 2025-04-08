"""Camera platform for Ultimaker integration."""
from __future__ import annotations

import logging
from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, API_CAMERA_SNAPSHOT, API_CAMERA_STREAM
from .coordinator import UltimakerDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ultimaker camera based on a config entry."""
    coordinator: UltimakerDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Vérifier si la caméra est disponible dans les données de l'imprimante
    printer_data = coordinator.data.get("printer", {})
    _LOGGER.debug("Printer data for camera setup: %s", printer_data)
    
    if "camera" in printer_data and printer_data.get("camera", {}).get("feed"):
        _LOGGER.debug("Camera feed found: %s", printer_data["camera"]["feed"])
        entities = [
            UltimakerStreamCamera(coordinator, entry),
            UltimakerSnapshotCamera(coordinator, entry),
        ]
        async_add_entities(entities)
        _LOGGER.info("Added camera entities for Ultimaker")
    else:
        _LOGGER.warning("No camera feed found in printer data")

class UltimakerStreamCamera(CoordinatorEntity[UltimakerDataUpdateCoordinator], Camera):
    """Representation of an Ultimaker camera stream."""

    _attr_has_entity_name = True
    _attr_supported_features = CameraEntityFeature.STREAM
    _attr_name = "Camera Stream"
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
        
        self._attr_unique_id = f"{entry.entry_id}_camera_stream"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data["name"],
            manufacturer="Ultimaker",
        )
        self._host = entry.data["host"]
        _LOGGER.debug("Initialized stream camera for %s", self._host)

    @property
    def available(self) -> bool:
        """Return if camera is available."""
        is_available = (
            self.coordinator.data.get("printer", {})
            .get("camera", {})
            .get("feed") is not None
        )
        _LOGGER.debug("Stream camera available: %s", is_available)
        return is_available

    @property
    def is_streaming(self) -> bool:
        """Return true if the device is streaming."""
        return self.available

    @property
    def is_recording(self) -> bool:
        """Return true if the device is recording."""
        return False

    @property
    def use_stream_for_stills(self) -> bool:
        """Return true if the camera should use the stream for stills."""
        return True

    async def stream_source(self) -> str | None:
        """Return the source of the stream."""
        if not self.available:
            _LOGGER.debug("Stream not available")
            return None
        
        # Essayer d'abord l'API de flux direct si disponible
        direct_url = f"http://{self._host}{API_CAMERA_STREAM}"
        _LOGGER.debug("Trying direct stream URL: %s", direct_url)
        
        try:
            async with self.coordinator.session.head(
                direct_url, 
                timeout=5,
                allow_redirects=True
            ) as response:
                if response.status == 200:
                    _LOGGER.debug("Direct stream URL available: %s", direct_url)
                    return direct_url
                _LOGGER.debug("Direct stream unavailable (status %s), trying feed URL", response.status)
        except Exception as err:
            _LOGGER.debug("Error checking direct stream URL: %s", err)
        
        # Sinon, utiliser l'URL du flux fournie par l'API
        camera_feed = (
            self.coordinator.data.get("printer", {})
            .get("camera", {})
            .get("feed")
        )
        
        if camera_feed:
            url = f"http://{self._host}{camera_feed}"
            _LOGGER.debug("Using feed URL: %s", url)
            return url
            
        _LOGGER.debug("No camera feed URLs found")
        return None

class UltimakerSnapshotCamera(CoordinatorEntity[UltimakerDataUpdateCoordinator], Camera):
    """Representation of an Ultimaker camera snapshot."""

    _attr_has_entity_name = True
    _attr_name = "Camera Snapshot"
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
        
        self._attr_unique_id = f"{entry.entry_id}_camera_snapshot"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data["name"],
            manufacturer="Ultimaker",
        )
        self._host = entry.data["host"]
        _LOGGER.debug("Initialized snapshot camera for %s", self._host)

    @property
    def available(self) -> bool:
        """Return if camera is available."""
        is_available = (
            self.coordinator.data.get("printer", {})
            .get("camera", {})
            .get("feed") is not None
        )
        _LOGGER.debug("Snapshot camera available: %s", is_available)
        return is_available

    @property
    def is_streaming(self) -> bool:
        """Return true if the device is streaming."""
        return self.available

    @property
    def is_recording(self) -> bool:
        """Return true if the device is recording."""
        return False

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return a still image from the camera."""
        if not self.available:
            _LOGGER.debug("Snapshot not available")
            return None

        try:
            url = f"http://{self._host}{API_CAMERA_SNAPSHOT}"
            _LOGGER.debug("Getting snapshot from: %s", url)
            
            async with self.coordinator.session.get(
                url,
                headers={"Accept": "image/jpeg"},
                timeout=10,
            ) as response:
                _LOGGER.debug("Snapshot response status: %s", response.status)
                _LOGGER.debug("Snapshot response headers: %s", response.headers)
                
                if response.status == 200:
                    content_type = response.headers.get("Content-Type", "")
                    _LOGGER.debug("Snapshot content type: %s", content_type)
                    
                    if "image" in content_type:
                        image_data = await response.read()
                        _LOGGER.debug("Successfully got snapshot, size: %d bytes", len(image_data))
                        return image_data
                    else:
                        _LOGGER.error("Unexpected content type: %s", content_type)
                else:
                    _LOGGER.error("Failed to get snapshot, status: %s", response.status)
                    
                    # Essayer de lire le corps de la réponse pour le diagnostic
                    try:
                        error_text = await response.text()
                        _LOGGER.error("Error response: %s", error_text[:200])
                    except Exception as text_err:
                        _LOGGER.error("Could not read error response: %s", text_err)
        except Exception as err:
            _LOGGER.error("Error getting camera image: %s", err, exc_info=True)
        
        return None 