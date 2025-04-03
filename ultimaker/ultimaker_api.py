"""API client for Ultimaker."""
import logging
import requests
from typing import Any, Dict, Optional

_LOGGER = logging.getLogger(__name__)

API_BASE_URL = "https://api.ultimaker.com/connect/v1"

class UltimakerAPI:
    """API client for Ultimaker."""

    def __init__(self, api_key: str) -> None:
        """Initialize the API client."""
        self._api_key = api_key
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

    def get_printer_status(self) -> Dict[str, Any]:
        """Get the current status of the printer."""
        try:
            response = self._session.get(f"{API_BASE_URL}/clusters")
            response.raise_for_status()
            clusters = response.json().get("data", [])
            
            if not clusters:
                return {}
            
            # Get first cluster status
            cluster = clusters[0]
            cluster_id = cluster["cluster_id"]
            
            # Get detailed status
            status_response = self._session.get(f"{API_BASE_URL}/clusters/{cluster_id}/status")
            status_response.raise_for_status()
            status_data = status_response.json().get("data", {})
            
            return {
                "cluster_info": cluster,
                "status": status_data,
            }
        except requests.RequestException as err:
            _LOGGER.error("Error fetching printer status: %s", err)
            return {}

    def send_printer_command(self, cluster_id: str, printer_id: str, action: str, data: Optional[Dict] = None) -> bool:
        """Send a command to the printer."""
        try:
            response = self._session.post(
                f"{API_BASE_URL}/clusters/{cluster_id}/printers/{printer_id}/action/{action}",
                json=data or {},
            )
            response.raise_for_status()
            return True
        except requests.RequestException as err:
            _LOGGER.error("Error sending printer command: %s", err)
            return False

    def get_print_job_status(self, cluster_id: str, job_id: str) -> Dict[str, Any]:
        """Get the status of a specific print job."""
        try:
            response = self._session.get(
                f"{API_BASE_URL}/clusters/{cluster_id}/print_jobs/{job_id}"
            )
            response.raise_for_status()
            return response.json().get("data", {})
        except requests.RequestException as err:
            _LOGGER.error("Error fetching print job status: %s", err)
            return {} 