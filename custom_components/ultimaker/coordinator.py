"""Data update coordinator for the Ultimaker integration."""
from __future__ import annotations

import logging
import asyncio
from datetime import datetime, timedelta
from typing import Any, Callable
import aiohttp
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
    API_PRINTER_HEADS,
    API_PRINTER_HEAD,
    API_PRINT_JOB_PROGRESS,
    API_PRINT_JOB_TIME_ELAPSED,
    API_PRINT_JOB_TIME_TOTAL,
    API_SYSTEM_FIRMWARE,
    API_SYSTEM_VARIANT,
    API_SYSTEM_UPTIME,
    API_AMBIENT_TEMPERATURE,
    API_LED_HUE,
    API_LED_SATURATION,
    API_LED_BRIGHTNESS,
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
            self._auth = aiohttp.auth.DigestAuth(self._auth_id, self._auth_key)

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        try:
            async with async_timeout.timeout(10):
                _LOGGER.debug("Fetching printer data from %s", self._host)
                
                # Récupérer les données de base de l'imprimante
                printer_data = await self._fetch_data(API_PRINTER)
                if not isinstance(printer_data, dict):
                    printer_data = {}
                
                # Récupérer les données des têtes d'impression
                heads_data = await self._fetch_data(API_PRINTER_HEADS)
                if isinstance(heads_data, list):
                    printer_data["heads"] = heads_data
                    
                    # Pour chaque tête, récupérer les données détaillées
                    for i, head in enumerate(heads_data):
                        head_url = API_PRINTER_HEAD.format(head_id=i)
                        head_data = await self._fetch_data(head_url)
                        if isinstance(head_data, dict):
                            printer_data["heads"][i].update(head_data)
                            
                        # Pour chaque extrudeur de la tête
                        if "extruders" in head:
                            for j, _ in enumerate(head["extruders"]):
                                temp_url = API_HOTEND_TEMPERATURE.format(head_id=i, extruder_id=j)
                                temp_data = await self._fetch_data(temp_url)
                                if isinstance(temp_data, dict):
                                    printer_data["heads"][i]["extruders"][j]["hotend"]["temperature"] = temp_data

                # Récupérer les données du lit chauffant
                bed_temp_data = await self._fetch_data(API_BED_TEMPERATURE)
                if isinstance(bed_temp_data, dict):
                    if "bed" not in printer_data:
                        printer_data["bed"] = {}
                    printer_data["bed"]["temperature"] = bed_temp_data

                # Récupérer les données du travail d'impression en cours
                print_job_data = await self._fetch_data(API_PRINT_JOB)
                if not isinstance(print_job_data, dict):
                    print_job_data = {}
                else:
                    # Ajouter les détails supplémentaires du travail d'impression
                    progress = await self._fetch_data(API_PRINT_JOB_PROGRESS)
                    if isinstance(progress, (int, float)):
                        print_job_data["progress"] = progress
                    
                    time_elapsed = await self._fetch_data(API_PRINT_JOB_TIME_ELAPSED)
                    if isinstance(time_elapsed, (int, float)):
                        print_job_data["time_elapsed"] = time_elapsed
                    
                    time_total = await self._fetch_data(API_PRINT_JOB_TIME_TOTAL)
                    if isinstance(time_total, (int, float)):
                        print_job_data["time_total"] = time_total

                # Récupérer les données système
                system_data = await self._fetch_data(API_SYSTEM)
                if not isinstance(system_data, dict):
                    system_data = {}
                else:
                    # Ajouter les détails supplémentaires du système
                    firmware = await self._fetch_data(API_SYSTEM_FIRMWARE)
                    if isinstance(firmware, str):
                        system_data["firmware"] = firmware
                    
                    variant = await self._fetch_data(API_SYSTEM_VARIANT)
                    if isinstance(variant, str):
                        system_data["variant"] = variant
                    
                    uptime = await self._fetch_data(API_SYSTEM_UPTIME)
                    if isinstance(uptime, (int, float)):
                        system_data["uptime"] = uptime

                # Récupérer les données de la caméra
                camera_data = await self._fetch_data(API_CAMERA)
                if isinstance(camera_data, dict):
                    camera_feed = await self._fetch_data(API_CAMERA_FEED)
                    if isinstance(camera_feed, str) and camera_feed.startswith("http"):
                        camera_data["feed"] = camera_feed
                    elif isinstance(camera_feed, dict):
                        if "value" in camera_feed and str(camera_feed["value"]).startswith("http"):
                            camera_data["feed"] = camera_feed["value"]
                        elif "feed" in camera_feed and str(camera_feed["feed"]).startswith("http"):
                            camera_data["feed"] = camera_feed["feed"]
                        else:
                            camera_data["feed"] = API_CAMERA_STREAM.format(index=0)
                    else:
                        camera_data["feed"] = API_CAMERA_STREAM.format(index=0)

                # Récupérer la température ambiante
                ambient_temp = await self._fetch_data(API_AMBIENT_TEMPERATURE)
                if isinstance(ambient_temp, dict):
                    printer_data["ambient_temperature"] = ambient_temp

                data = {
                    "printer": {
                        **printer_data,
                        "camera": camera_data,
                    },
                    "print_job": print_job_data,
                    "system": system_data,
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
            if self._auth:
                async with self._auth.session(self._session) as auth_session:
                    async with auth_session.get(url, headers=HEADERS) as response:
                        if response.status == 401:
                            await self._request_auth()
                            return await self._fetch_data(endpoint)
                        return await self._process_response(response, endpoint)
            else:
                async with self._session.get(url, headers=HEADERS) as response:
                    if response.status == 401:
                        await self._request_auth()
                        return await self._fetch_data(endpoint)
                    return await self._process_response(response, endpoint)
                    
        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching data from %s: %s", url, err)
            return {}
        except Exception as err:
            _LOGGER.error("Unexpected error fetching data from %s: %s", url, err, exc_info=True)
            return {}

    async def _process_response(self, response: aiohttp.ClientResponse, endpoint: str) -> Any:
        """Process the response from the printer."""
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
                "Resource not found at %s: %s", endpoint, response.status
            )
            return {}
        else:
            _LOGGER.error(
                "Error fetching data from %s: %s", endpoint, response.status
            )
            return {}

    async def _request_auth(self) -> None:
        """Request authentication from the printer."""
        url = f"http://{self._host}{API_AUTH_REQUEST}"
        data = {"application": AUTH_APP_NAME}
        
        try:
            async with self._session.post(url, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    auth_id = result.get("id")
                    auth_key = result.get("key")
                    
                    if not auth_id or not auth_key:
                        raise ConfigEntryAuthFailed("Failed to get authentication credentials")

                    # Attendre l'autorisation physique
                    authorized = await self._wait_for_auth_approval(auth_id)
                    if not authorized:
                        raise ConfigEntryAuthFailed("Authorization request timed out or was rejected")

                    # Mettre à jour les credentials
                    self._auth_id = auth_id
                    self._auth_key = auth_key
                    self._auth = aiohttp.auth.DigestAuth(self._auth_id, self._auth_key)
                    
                    # Sauvegarder les credentials
                    new_data = dict(self.config_entry.data)
                    new_data[CONF_AUTH_ID] = self._auth_id
                    new_data[CONF_AUTH_KEY] = self._auth_key
                    self.hass.config_entries.async_update_entry(
                        self.config_entry, data=new_data
                    )
                else:
                    raise ConfigEntryAuthFailed(f"Authentication request failed with status {response.status}")
        except aiohttp.ClientError as err:
            raise ConfigEntryAuthFailed(f"Error requesting authentication: {err}")

    async def _wait_for_auth_approval(self, auth_id: str) -> bool:
        """Wait for physical authorization on the printer."""
        check_url = f"http://{self._host}{API_AUTH_CHECK}/{auth_id}"
        start_time = datetime.now()
        
        while (datetime.now() - start_time).total_seconds() < AUTH_CHECK_TIMEOUT:
            try:
                async with self._session.get(check_url) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get("message") == "authorized":
                            _LOGGER.info("Authorization approved on printer")
                            return True
                        elif result.get("message") == "unauthorized":
                            _LOGGER.error("Authorization rejected on printer")
                            return False
                    
                    await asyncio.sleep(AUTH_CHECK_INTERVAL)
            except aiohttp.ClientError as err:
                _LOGGER.error("Error checking authorization status: %s", err)
                await asyncio.sleep(AUTH_CHECK_INTERVAL)
                
        _LOGGER.error("Authorization request timed out")
        return False

    async def _send_command(self, endpoint: str, method: str = "PUT", data: dict | None = None) -> Any:
        """Send command to the printer."""
        url = f"http://{self._host}{endpoint}"
        
        try:
            if self._auth:
                async with self._auth.session(self._session) as auth_session:
                    if method == "PUT":
                        async with auth_session.put(url, json=data) as response:
                            if response.status == 401:
                                await self._request_auth()
                                return await self._send_command(endpoint, method, data)
                            response.raise_for_status()
                            return await response.json() if response.status != 204 else None
                    elif method == "POST":
                        async with auth_session.post(url, json=data) as response:
                            if response.status == 401:
                                await self._request_auth()
                                return await self._send_command(endpoint, method, data)
                            response.raise_for_status()
                            return await response.json() if response.status != 204 else None
            else:
                if method == "PUT":
                    async with self._session.put(url, json=data) as response:
                        if response.status == 401:
                            await self._request_auth()
                            return await self._send_command(endpoint, method, data)
                        response.raise_for_status()
                        return await response.json() if response.status != 204 else None
                elif method == "POST":
                    async with self._session.post(url, json=data) as response:
                        if response.status == 401:
                            await self._request_auth()
                            return await self._send_command(endpoint, method, data)
                        response.raise_for_status()
                        return await response.json() if response.status != 204 else None
                        
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with printer: {err}")

    async def async_pause_print(self) -> None:
        """Pause the current print job."""
        await self._send_command(API_PRINT_JOB_STATE, "PUT", {"target": "pause"})

    async def async_resume_print(self) -> None:
        """Resume the current print job."""
        await self._send_command(API_PRINT_JOB_STATE, "PUT", {"target": "print"})

    async def async_stop_print(self) -> None:
        """Stop the current print job."""
        await self._send_command(API_PRINT_JOB_STATE, "PUT", {"target": "abort"})

    async def async_set_bed_temperature(self, temperature: float) -> None:
        """Set the bed temperature."""
        await self._send_command(API_BED_TEMPERATURE, "PUT", {"target": temperature})

    async def async_set_hotend_temperature(self, head_id: int, extruder_id: int, temperature: float) -> None:
        """Set the hotend temperature."""
        endpoint = API_HOTEND_TEMPERATURE.format(head_id=head_id, extruder_id=extruder_id)
        await self._send_command(endpoint, "PUT", {"target": temperature})

    async def async_set_led(self, hue: float = None, saturation: float = None, brightness: float = None) -> None:
        """Set the LED state."""
        if hue is not None:
            await self._send_command(API_LED_HUE, "PUT", hue)
        if saturation is not None:
            await self._send_command(API_LED_SATURATION, "PUT", saturation)
        if brightness is not None:
            await self._send_command(API_LED_BRIGHTNESS, "PUT", brightness) 