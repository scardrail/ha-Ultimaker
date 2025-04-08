"""Data update coordinator for the Ultimaker integration."""
from __future__ import annotations

import logging
import asyncio
from datetime import datetime, timedelta
from typing import Any, Callable
import aiohttp
from aiohttp import BasicAuth, DigestAuth
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
        entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        self.host = entry.data["host"]
        self.session = async_get_clientsession(hass)
        self.auth = None
        self._auth_id = entry.data.get(CONF_AUTH_ID)
        self._auth_key = entry.data.get(CONF_AUTH_KEY)
        
        if self._auth_id and self._auth_key:
            self.auth = DigestAuth(self._auth_id, self._auth_key)

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
        url = f"http://{self.host}{endpoint}"
        
        try:
            async with self.session.get(url, headers=HEADERS) as response:
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

    async def _send_command(self, endpoint: str, method: str = "PUT", data: Any = None) -> bool:
        """Send a command to the printer."""
        url = f"http://{self.host}{endpoint}"
        
        # Vérifier si nous avons besoin d'authentification
        if method in ["PUT", "POST", "DELETE"]:
            if not self.auth:
                auth_result = await self._request_auth()
                if not auth_result:
                    _LOGGER.error("Failed to authenticate with printer")
                    return False
        
        try:
            if isinstance(data, dict):
                async with self.session.request(
                    method, 
                    url, 
                    json=data, 
                    headers=HEADERS,
                    auth=self.auth
                ) as response:
                    if response.status == 401:
                        # Essayer de renouveler l'authentification
                        auth_result = await self._request_auth()
                        if not auth_result:
                            return False
                        # Réessayer la requête avec la nouvelle authentification
                        async with self.session.request(
                            method, 
                            url, 
                            json=data, 
                            headers=HEADERS,
                            auth=self.auth
                        ) as retry_response:
                            return retry_response.status in (200, 204)
                    return response.status in (200, 204)
            else:
                # Pour les cas où data n'est pas un dict (ex: température qui est un float)
                async with self.session.request(
                    method, 
                    url, 
                    json={"temperature": data}, 
                    headers=HEADERS,
                    auth=self.auth
                ) as response:
                    if response.status == 401:
                        # Essayer de renouveler l'authentification
                        auth_result = await self._request_auth()
                        if not auth_result:
                            return False
                        # Réessayer la requête avec la nouvelle authentification
                        async with self.session.request(
                            method, 
                            url, 
                            json={"temperature": data}, 
                            headers=HEADERS,
                            auth=self.auth
                        ) as retry_response:
                            return retry_response.status in (200, 204)
                    return response.status in (200, 204)
        except aiohttp.ClientError as err:
            _LOGGER.error("Error sending command to %s: %s", url, err)
            return False

    async def _request_auth(self) -> bool:
        """Request authentication from the printer."""
        url = f"http://{self.host}{API_AUTH_REQUEST}"
        try:
            # 1. Demander l'authentification
            async with self.session.post(
                url,
                data={
                    "application": AUTH_APP_NAME,
                    "user": AUTH_USER_NAME
                },
                headers=HEADERS
            ) as response:
                if response.status != 200:
                    _LOGGER.error("Failed to request authentication: %s", response.status)
                    return False
                
                auth_data = await response.json()
                auth_id = auth_data.get("id")
                auth_key = auth_data.get("key")
                
                if not auth_id or not auth_key:
                    _LOGGER.error("Invalid authentication response: %s", auth_data)
                    return False
                
                # 2. Attendre l'autorisation
                check_url = f"http://{self.host}{API_AUTH_CHECK}/{auth_id}"
                start_time = datetime.now()
                
                while (datetime.now() - start_time).total_seconds() < AUTH_CHECK_TIMEOUT:
                    async with self.session.get(check_url, headers=HEADERS) as check_response:
                        if check_response.status != 200:
                            await asyncio.sleep(AUTH_CHECK_INTERVAL)
                            continue
                        
                        check_data = await check_response.json()
                        if check_data.get("message") == "authorized":
                            # Mettre à jour l'authentification
                            self.auth = DigestAuth(auth_id, auth_key)
                            # Sauvegarder les identifiants
                            self.hass.config_entries.async_update_entry(
                                self._entry,
                                data={
                                    **self._entry.data,
                                    CONF_AUTH_ID: auth_id,
                                    CONF_AUTH_KEY: auth_key,
                                },
                            )
                            return True
                        elif check_data.get("message") == "unauthorized":
                            _LOGGER.error("Authorization rejected by user")
                            return False
                        
                        await asyncio.sleep(AUTH_CHECK_INTERVAL)
                
                _LOGGER.error("Authorization timeout")
                return False
                
        except Exception as err:
            _LOGGER.error("Error during authentication: %s", err)
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

    async def async_set_led(self, led_data: dict[str, Any]) -> bool:
        """Set the LED state."""
        return await self._send_command(
            API_LED,
            data=led_data
        ) 