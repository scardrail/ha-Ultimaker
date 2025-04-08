"""Data update coordinator for the Ultimaker integration."""
from __future__ import annotations

import logging
import asyncio
from datetime import datetime, timedelta
from typing import Any, Callable
import aiohttp
from aiohttp_digest import DigestAuth
import async_timeout
import json

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.exceptions import ConfigEntryAuthFailed

from .const import (
    API_PRINTER,
    API_PRINT_JOB,
    API_SYSTEM,
    API_BED_TEMPERATURE,
    API_HOTEND_TEMPERATURE,
    API_PRINT_JOB_STATE,
    API_CAMERA,
    API_CAMERA_FEED,
    API_LED,
    API_AUTH_REQUEST,
    API_AUTH_CHECK,
    API_AUTH_VERIFY,
    PRINT_JOB_STATE_PAUSED,
    PRINT_JOB_STATE_PRINTING,
    PRINT_JOB_STATE_ABORTED,
    UPDATE_INTERVAL,
    DOMAIN,
    API_CAMERA_STREAM,
    AUTH_APP_NAME,
    AUTH_USER_NAME,
    AUTH_CHECK_INTERVAL,
    AUTH_CHECK_TIMEOUT,
    CONF_AUTH_ID,
    CONF_AUTH_KEY,
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
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self.config_entry = config_entry
        self._host = config_entry.data["host"]
        self._auth_id = config_entry.data.get(CONF_AUTH_ID)
        self._auth_key = config_entry.data.get(CONF_AUTH_KEY)
        self._session = async_get_clientsession(hass)
        self._auth = None
        if self._auth_id and self._auth_key:
            self._auth = DigestAuth(self._auth_id, self._auth_key)

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        try:
            async with async_timeout.timeout(10):
                _LOGGER.debug("Fetching printer data from %s", self._host)
                
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

                # Traitement des données de caméra
                if camera_data:
                    _LOGGER.debug("Camera data found: %s", camera_data)
                    camera_feed = await self._fetch_data(API_CAMERA_FEED)
                    _LOGGER.debug("Camera feed data: %s", camera_feed)
                    
                    # Gestion propre du feed
                    if isinstance(camera_feed, str) and camera_feed.startswith("http"):
                        camera_data["feed"] = camera_feed
                        _LOGGER.info("Camera feed URL found (string): %s", camera_feed)

                    elif isinstance(camera_feed, dict):
                        # Cas: réponse sous {"value": "http://..."}
                        if "value" in camera_feed and str(camera_feed["value"]).startswith("http"):
                            camera_data["feed"] = camera_feed["value"]
                            _LOGGER.info("Camera feed URL found in 'value': %s", camera_data["feed"])
                        elif "feed" in camera_feed and str(camera_feed["feed"]).startswith("http"):
                            camera_data["feed"] = camera_feed["feed"]
                            _LOGGER.info("Camera feed URL found in 'feed': %s", camera_data["feed"])
                        else:
                            camera_data["feed"] = API_CAMERA_STREAM
                            _LOGGER.warning("Fallback to default stream path: %s", API_CAMERA_STREAM)

                    else:
                        camera_data["feed"] = API_CAMERA_STREAM
                        _LOGGER.warning("Fallback to default stream path: %s", API_CAMERA_STREAM)
                else:
                    _LOGGER.debug("No camera data available from API")

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

    async def _fetch_data(self, endpoint: str) -> Any:
        """Fetch data from the printer."""
        url = f"http://{self._host}{endpoint}"
        
        try:
            async with self._session.get(url, headers=HEADERS) as response:
                _LOGGER.debug("GET %s -> %s", url, response.status)
                
                if response.status == 200:
                    content_type = response.headers.get("Content-Type", "")
                    text = await response.text()
                    _LOGGER.debug("Response text from %s: %s", endpoint, text)
                    
                    if not text:
                        _LOGGER.warning("Empty response from %s", endpoint)
                        return {}

                    # Si le contenu est du JSON
                    if "application/json" in content_type:
                        try:
                            data = json.loads(text)
                            if isinstance(data, dict):
                                return data
                            elif isinstance(data, (int, float, str, bool)):
                                return {"value": data}
                            return {}
                        except json.JSONDecodeError as err:
                            _LOGGER.error(
                                "Failed to decode JSON from %s: %s (text: %s)", endpoint, err, text
                            )
                            return {}
                    
                    # Si c'est du texte brut (comme l'URL de la caméra)
                    elif "text/plain" in content_type or "text/html" in content_type:
                        if text.strip().startswith("http"):
                            return text.strip()
                        return {"value": text.strip()}
                    
                    # Pour tout autre type de contenu, on essaie d'abord de parser comme JSON
                    try:
                        data = json.loads(text)
                        if isinstance(data, dict):
                            return data
                        elif isinstance(data, (int, float, str, bool)):
                            return {"value": data}
                    except json.JSONDecodeError:
                        # Si ce n'est pas du JSON et que ça ressemble à une URL
                        if text.strip().startswith("http"):
                            return text.strip()
                        return {"value": text.strip()}
                            
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

    async def _request_auth(self) -> None:
        """Request authentication from the printer."""
        url = f"http://{self._host}{API_AUTH_REQUEST}"
        data = {"application": AUTH_APP_NAME}
        
        try:
            async with self._session.post(url, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    self._auth_id = result.get("id")
                    self._auth_key = result.get("key")
                    
                    if self._auth_id and self._auth_key:
                        self._auth = DigestAuth(self._auth_id, self._auth_key)
                        
                        # Save the credentials
                        new_data = dict(self.config_entry.data)
                        new_data[CONF_AUTH_ID] = self._auth_id
                        new_data[CONF_AUTH_KEY] = self._auth_key
                        self.hass.config_entries.async_update_entry(
                            self.config_entry, data=new_data
                        )
                    else:
                        raise ConfigEntryAuthFailed("Failed to get authentication credentials")
                else:
                    raise ConfigEntryAuthFailed(f"Authentication request failed with status {response.status}")
        except aiohttp.ClientError as err:
            raise ConfigEntryAuthFailed(f"Error requesting authentication: {err}")

    async def _send_command(self, endpoint: str, method: str = "GET", data: dict | None = None) -> Any:
        """Send command to the printer."""
        url = f"http://{self._host}{endpoint}"
        
        try:
            if method == "GET":
                if self._auth:
                    async with self._auth.session(self._session) as auth_session:
                        async with auth_session.get(url) as response:
                            if response.status == 401:
                                await self._request_auth()
                                return await self._send_command(endpoint, method, data)
                            response.raise_for_status()
                            return await response.json()
                else:
                    async with self._session.get(url) as response:
                        if response.status == 401:
                            await self._request_auth()
                            return await self._send_command(endpoint, method, data)
                        response.raise_for_status()
                        return await response.json()
            else:
                if self._auth:
                    async with self._auth.session(self._session) as auth_session:
                        async with auth_session.put(url, json=data) as response:
                            if response.status == 401:
                                await self._request_auth()
                                return await self._send_command(endpoint, method, data)
                            response.raise_for_status()
                            return await response.json()
                else:
                    async with self._session.put(url, json=data) as response:
                        if response.status == 401:
                            await self._request_auth()
                            return await self._send_command(endpoint, method, data)
                        response.raise_for_status()
                        return await response.json()
                        
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with printer: {err}")

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

    async def async_set_led(self, led_data: dict[str, Any]) -> bool:
        """Set the LED state."""
        return await self._send_command(
            API_LED,
            data=led_data
        ) 