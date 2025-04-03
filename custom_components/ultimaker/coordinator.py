"""Data update coordinator for the Ultimaker integration."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any, Callable

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import aiohttp
import async_timeout

from .const import (
    API_PRINTER,
    API_PRINT_JOB,
    API_SYSTEM,
    API_BED_TEMPERATURE,
    API_HOTEND_TEMPERATURE,
    API_PRINT_JOB_STATE,
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
        session: aiohttp.ClientSession,
        host: str,
    ) -> None:
        """Initialize."""
        self.host = host
        self.session = session
        self._data: dict[str, Any] = {}

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
                printer_data = await self._fetch_data(API_PRINTER)
                print_job_data = await self._fetch_data(API_PRINT_JOB)
                system_data = await self._fetch_data(API_SYSTEM)

                data = {
                    "printer": printer_data,
                    "print_job": print_job_data,
                    "system": system_data,
                    "last_update": datetime.now(),
                }

                return data

        except Exception as err:
            raise UpdateFailed(f"Error communicating with printer: {err}") from err

    async def _fetch_data(self, endpoint: str) -> dict[str, Any]:
        """Fetch data from the printer."""
        url = f"http://{self.host}{endpoint}"
        
        try:
            async with self.session.get(url, headers=HEADERS) as response:
                if response.status == 200:
                    return await response.json()
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