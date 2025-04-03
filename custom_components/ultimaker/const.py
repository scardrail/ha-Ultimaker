"""Constants for the Ultimaker integration."""
from __future__ import annotations

from typing import Final

DOMAIN: Final = "ultimaker"

# Configuration
CONF_HOST: Final = "host"
CONF_NAME: Final = "name"

# API endpoints
API_PREFIX: Final = "/api/v1"
API_PRINTER: Final = f"{API_PREFIX}/printer"
API_PRINT_JOB: Final = f"{API_PREFIX}/print_job"
API_SYSTEM: Final = f"{API_PREFIX}/system"
API_BED_TEMPERATURE: Final = f"{API_PREFIX}/printer/bed/temperature"
API_HOTEND_TEMPERATURE: Final = f"{API_PREFIX}/printer/heads/0/extruders/0/hotend/temperature"
API_PRINT_JOB_STATE: Final = f"{API_PREFIX}/print_job/state"

# Update interval
UPDATE_INTERVAL: Final = 30  # seconds

# Printer states
PRINTER_STATE_IDLE: Final = "idle"
PRINTER_STATE_PRINTING: Final = "printing"
PRINTER_STATE_PAUSED: Final = "paused"
PRINTER_STATE_ERROR: Final = "error"
PRINTER_STATE_OFFLINE: Final = "offline"

# Print job states
PRINT_JOB_STATE_NONE: Final = "none"
PRINT_JOB_STATE_PRINTING: Final = "print"
PRINT_JOB_STATE_PAUSED: Final = "pause"
PRINT_JOB_STATE_ABORTED: Final = "abort"

# Attributes
ATTR_BED_TEMPERATURE: Final = "bed_temperature"
ATTR_BED_TARGET: Final = "bed_target"
ATTR_HOTEND_TEMPERATURE: Final = "hotend_temperature"
ATTR_HOTEND_TARGET: Final = "hotend_target"
ATTR_PROGRESS: Final = "progress"
ATTR_PRINT_TIME: Final = "print_time"
ATTR_ESTIMATED_TIME: Final = "estimated_time"
ATTR_FILAMENT_USED: Final = "filament_used"
ATTR_LAYER: Final = "layer"
ATTR_LAYER_COUNT: Final = "layer_count"

# Platforms
PLATFORMS: Final = ["sensor", "binary_sensor", "button"]