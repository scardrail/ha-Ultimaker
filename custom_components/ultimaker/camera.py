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

    # Vérifier si la caméra est disponible dans les données de l'imprimante
    printer_data = coordinator.data.get("printer", {})
    if "camera" in printer_data and printer_data.get("camera", {}).get("feed"):
        _LOGGER.debug("Camera feed found, setting up camera entities")
        entities = [
            UltimakerStreamCamera(coordinator, entry),
            UltimakerSnapshotCamera(coordinator, entry),
        ]
        async_add_entities(entities)
    else:
        _LOGGER.debug("No camera feed found")

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

    @property
    def available(self) -> bool:
        """Return if camera is available."""
        return (
            self.coordinator.data.get("printer", {})
            .get("camera", {})
            .get("feed") is not None
        )

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
            return None
            
        camera_feed = (
            self.coordinator.data.get("printer", {})
            .get("camera", {})
            .get("feed")
        )
        if camera_feed:
            return f"http://{self._host}{camera_feed}"
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

    @property
    def available(self) -> bool:
        """Return if camera is available."""
        return (
            self.coordinator.data.get("printer", {})
            .get("camera", {})
            .get("feed") is not None
        )

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
            return None

        try:
            async with self.coordinator.session.get(
                f"http://{self._host}/camera/0/snapshot",
                headers={"Accept": "image/jpeg"},
            ) as response:
                if response.status == 200:
                    return await response.read()
        except Exception as err:
            _LOGGER.error("Error getting camera image: %s", err)
            return None
        return None 