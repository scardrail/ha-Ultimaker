"""Data update coordinator for the Ultimaker integration."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any, Callable

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import aiohttp
import async_timeout
import json

from .const import (
    API_PRINTER,
    API_PRINT_JOB,
    API_SYSTEM,
    API_BED_TEMPERATURE,
    API_HOTEND_TEMPERATURE,
    API_PRINT_JOB_STATE,
    API_CAMERA,
    API_CAMERA_FEED,
    PRINT_JOB_STATE_PAUSED,
    PRINT_JOB_STATE_PRINTING,
    PRINT_JOB_STATE_ABORTED,
    UPDATE_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

class UltimakerDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Ultimaker data."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        self.host = entry.data["host"]
        self.session = async_get_clientsession(hass)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        try:
            async with async_timeout.timeout(10):
                _LOGGER.debug("Fetching printer data from %s", self.host)
                
                printer_data = await self._fetch_data(API_PRINTER)
                _LOGGER.debug("Printer data: %s", printer_data)
                
                if not isinstance(printer_data, dict):
                    _LOGGER.error("Invalid printer data type: %s", type(printer_data))
                    printer_data = {}

                print_job_data = await self._fetch_data(API_PRINT_JOB)
                if not isinstance(print_job_data, dict):
                    print_job_data = {}

                system_data = await self._fetch_data(API_SYSTEM)
                if not isinstance(system_data, dict):
                    system_data = {}

                bed_temp_data = await self._fetch_data(API_BED_TEMPERATURE)
                if not isinstance(bed_temp_data, dict):
                    bed_temp_data = {}

                hotend_temp_data = await self._fetch_data(API_HOTEND_TEMPERATURE)
                if not isinstance(hotend_temp_data, dict):
                    hotend_temp_data = {}

                camera_data = await self._fetch_data(API_CAMERA)
                if not isinstance(camera_data, dict):
                    camera_data = {}

                # Si nous avons des données de caméra, essayons de récupérer le flux
                if camera_data:
                    camera_feed = await self._fetch_data(API_CAMERA_FEED)
                    if isinstance(camera_feed, dict):
                        camera_data["feed"] = camera_feed.get("feed")

                data = {
                    "printer": {
                        **printer_data,
                        "camera": camera_data,
                    },
                    "print_job": print_job_data,
                    "system": system_data,
                    "bed_temperature": bed_temp_data,
                    "hotend_temperature": hotend_temp_data,
                    "last_update": datetime.now(),
                }

                _LOGGER.debug("Final data structure: %s", data)
                return data

        except Exception as err:
            _LOGGER.error("Error communicating with printer: %s", err, exc_info=True)
            raise UpdateFailed(f"Error communicating with printer: {err}") from err

    async def _fetch_data(self, endpoint: str) -> dict[str, Any]:
        """Fetch data from the printer."""
        url = f"http://{self.host}{endpoint}"
        
        try:
            async with self.session.get(url, headers=HEADERS) as response:
                _LOGGER.debug("GET %s -> %s", url, response.status)
                
                if response.status == 200:
                    text = await response.text()
                    _LOGGER.debug("Response text from %s: %s", endpoint, text)
                    
                    if not text:
                        _LOGGER.warning("Empty response from %s", endpoint)
                        return {}
                        
                    try:
                        data = json.loads(text)
                        if isinstance(data, dict):
                            return data
                        else:
                            _LOGGER.warning(
                                "Unexpected data type from %s: %s (%s)", endpoint, type(data), data
                            )
                            # Si c'est une valeur simple (nombre, chaîne), on la met dans un dict
                            if isinstance(data, (int, float, str, bool)):
                                return {"value": data}
                            return {}
                            
                    except json.JSONDecodeError as err:
                        _LOGGER.error(
                            "Failed to decode JSON from %s: %s (text: %s)", endpoint, err, text
                        )
                        return {}
                            
                elif response.status == 404:
                    _LOGGER.debug(
                        "Resource not found at %s: %s", url, response.status
                    )
                    return {}
                else:
                    _LOGGER.error(
                        "Error fetching data from %s: %s", url, response.status
                    )
                    return {}
                    
        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching data from %s: %s", url, err)
            return {}
        except Exception as err:
            _LOGGER.error("Unexpected error fetching data from %s: %s", url, err, exc_info=True)
            return {}

    async def _send_command(self, endpoint: str, method: str = "PUT", data: Any = None) -> bool:
        """Send a command to the printer."""
        url = f"http://{self.host}{endpoint}"
        
        try:
            if isinstance(data, dict):
                async with self.session.request(method, url, json=data, headers=HEADERS) as response:
                    return response.status in (200, 204)
            else:
                # Pour les cas où data n'est pas un dict (ex: température qui est un float)
                async with self.session.request(method, url, json={"temperature": data}, headers=HEADERS) as response:
                    return response.status in (200, 204)
        except aiohttp.ClientError as err:
            _LOGGER.error("Error sending command to %s: %s", url, err)
            return False

    async def async_pause_print(self) -> bool:
        """Pause the current print job."""
        return await self._send_command(API_PRINT_JOB_STATE, data=PRINT_JOB_STATE_PAUSED)

    async def async_resume_print(self) -> bool:
        """Resume the current print job."""
        return await self._send_command(API_PRINT_JOB_STATE, data=PRINT_JOB_STATE_PRINTING)

    async def async_stop_print(self) -> bool:
        """Stop the current print job."""
        return await self._send_command(API_PRINT_JOB_STATE, data=PRINT_JOB_STATE_ABORTED)

    async def async_set_bed_temperature(self, temperature: float) -> bool:
        """Set the bed temperature."""
        return await self._send_command(
            API_BED_TEMPERATURE,
            data=temperature
        )

    async def async_set_hotend_temperature(self, temperature: float) -> bool:
        """Set the hotend temperature."""
        return await self._send_command(
            API_HOTEND_TEMPERATURE,
            data=temperature
        ) 