"""Camera platform for Ultimaker integration."""
from __future__ import annotations

import logging
import aiohttp

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

    camera = UltimakerCamera(
        name=f"{entry.data['name']} Camera",
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

    _attr_supported_features = CameraEntityFeature(0)

    def __init__(
        self,
        name: str,
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
        self.coordinator = coordinator
        self._camera_feed_url = None

        _LOGGER.debug("Initialized camera component")

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self._update_camera_url()

        # S'abonner aux mises à jour du coordinator
        if self.coordinator:
            self.async_on_remove(
                self.coordinator.async_add_listener(self._update_camera_url)
            )

    def _update_camera_url(self):
        """Update camera URL from coordinator data."""
        if self.coordinator:
            feed = self.coordinator.data.get("printer", {}).get("camera", {}).get("feed")
            if isinstance(feed, str) and feed.startswith("http"):
                self._camera_feed_url = feed
                _LOGGER.debug("Updated camera feed URL: %s", self._camera_feed_url)

    async def stream_source(self) -> str | None:
        """Return the source of the stream."""
        return self._camera_feed_url

    async def async_camera_image(self, width: int | None = None, height: int | None = None) -> bytes | None:
        """Return a still image from the camera feed."""
        if self._camera_feed_url:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(self._camera_feed_url) as resp:
                        if resp.status == 200:
                            return await resp.read()
                        _LOGGER.warning("Failed to get camera image, status: %s", resp.status)
            except Exception as err:
                _LOGGER.error("Error getting camera image: %s", err)
        return None