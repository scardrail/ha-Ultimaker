"""Camera platform for Ultimaker integration."""
from __future__ import annotations

from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import UltimakerDataUpdateCoordinator

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ultimaker camera based on a config entry."""
    coordinator: UltimakerDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Add both stream and snapshot cameras
    entities = [
        UltimakerStreamCamera(coordinator, entry),
        UltimakerSnapshotCamera(coordinator, entry),
    ]
    async_add_entities(entities)

class UltimakerStreamCamera(CoordinatorEntity[UltimakerDataUpdateCoordinator], Camera):
    """Representation of an Ultimaker camera stream."""

    _attr_has_entity_name = True
    _attr_supported_features = CameraEntityFeature.STREAM
    _attr_name = "Camera Stream"
    _attr_icon = "mdi:printer-3d"

    def __init__(
        self,
        coordinator: UltimakerDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the camera."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_camera_stream"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data["name"],
            manufacturer="Ultimaker",
        )
        self._host = entry.data["host"]

    @property
    def is_streaming(self) -> bool:
        """Return true if the device is streaming."""
        return True

    @property
    def is_recording(self) -> bool:
        """Return true if the device is recording."""
        return False

    async def stream_source(self) -> str | None:
        """Return the source of the stream."""
        return f"http://{self._host}/camera/0/stream"

class UltimakerSnapshotCamera(CoordinatorEntity[UltimakerDataUpdateCoordinator], Camera):
    """Representation of an Ultimaker camera snapshot."""

    _attr_has_entity_name = True
    _attr_name = "Camera Snapshot"
    _attr_icon = "mdi:printer-3d"

    def __init__(
        self,
        coordinator: UltimakerDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the camera."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_camera_snapshot"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data["name"],
            manufacturer="Ultimaker",
        )
        self._host = entry.data["host"]

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return a still image from the camera."""
        try:
            async with self.coordinator.session.get(
                f"http://{self._host}/camera/0/snapshot",
                headers={"Accept": "image/jpeg"},
            ) as response:
                if response.status == 200:
                    return await response.read()
        except Exception:
            return None
        return None 