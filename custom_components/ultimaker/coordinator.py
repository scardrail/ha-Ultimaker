"""Data update coordinator for the Ultimaker integration."""
from __future__ import annotations

import logging
import asyncio
from datetime import datetime, timedelta
from typing import Any, Callable
import aiohttp
import async_timeout
import json
import xml.etree.ElementTree as ET

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
    API_LED_HUE,
    API_LED_SATURATION,
    API_LED_BRIGHTNESS,
    API_FILAMENTS,
    API_FILAMENT_GUID,
)

_LOGGER = logging.getLogger(__name__)

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

def parse_material_xml(xml_string: str) -> dict[str, Any]:
    """Parse le XML du matériau pour extraire les informations utiles."""
    try:
        root = ET.fromstring(xml_string)
        metadata = root.find(".//metadata")
        if metadata is not None:
            return {
                "brand": metadata.findtext("brand", "Unknown"),
                "material": metadata.findtext("material", "Unknown"),
                "color": metadata.findtext("color_name", "Unknown"),
                "density": metadata.findtext("density", "0"),
                "diameter": metadata.findtext("diameter", "0"),
            }
        return {}
    except ET.ParseError as err:
        _LOGGER.error("Failed to parse material XML: %s", err)
        return {}

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
                
                # Récupérer les données des têtes d'impression et des matériaux
                heads_data = await self._fetch_data(API_PRINTER_HEADS)
                if isinstance(heads_data, list):
                    printer_data["heads"] = heads_data
                    
                    # Pour chaque tête, récupérer les données détaillées et les matériaux
                    for i, head in enumerate(heads_data):
                        head_url = API_PRINTER_HEAD.format(head_id=i)
                        head_data = await self._fetch_data(head_url)
                        if isinstance(head_data, dict):
                            printer_data["heads"][i].update(head_data)
                            
                        # Pour chaque extrudeur de la tête
                        if "extruders" in head:
                            for j, extruder in enumerate(head["extruders"]):
                                # Récupérer la température
                                temp_url = API_HOTEND_TEMPERATURE.format(head_id=i, extruder_id=j)
                                temp_data = await self._fetch_data(temp_url)
                                if isinstance(temp_data, dict):
                                    printer_data["heads"][i]["extruders"][j]["hotend"]["temperature"] = temp_data
                                
                                # Récupérer les informations sur le matériau
                                material_guid = extruder.get("active_material", {}).get("GUID")
                                if material_guid:
                                    material_data = await self._fetch_data(API_FILAMENT_GUID.format(material_guid=material_guid))
                                    if material_data:
                                        printer_data["heads"][i]["extruders"][j]["active_material"]["data"] = material_data

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
            async with self._session.get(url, headers=HEADERS) as response:
                _LOGGER.debug("GET %s -> %s", url, response.status)
                
                if response.status == 404:
                    _LOGGER.debug("Resource not found at %s: %s", endpoint, response.status)
                    return None

                # Si c'est un appel à l'API des matériaux, on traite le XML
                if endpoint.startswith(API_FILAMENTS) and "application/json" not in response.headers.get("Content-Type", ""):
                    xml_data = await response.text()
                    return parse_material_xml(xml_data)
                    
                return await response.json()
                    
        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching data from %s: %s", url, err)
            return None
        except Exception as err:
            _LOGGER.error("Unexpected error fetching data from %s: %s", url, err, exc_info=True)
            return None

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
            # Authentification requise uniquement pour PUT/POST/DELETE
            if method in ["PUT", "POST", "DELETE"]:
                if not self._auth:
                    await self._request_auth()
                
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
                    elif method == "DELETE":
                        async with auth_session.delete(url) as response:
                            if response.status == 401:
                                await self._request_auth()
                                return await self._send_command(endpoint, method, data)
                            response.raise_for_status()
                            return await response.json() if response.status != 204 else None
            else:
                # Pour les autres méthodes, pas besoin d'authentification
                async with self._session.request(method, url, json=data) as response:
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