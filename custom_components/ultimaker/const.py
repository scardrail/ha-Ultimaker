"""Constants for the Ultimaker integration."""
from __future__ import annotations

from typing import Final

DOMAIN: Final = "ultimaker"

# Configuration
CONF_HOST: Final = "host"
CONF_NAME: Final = "name"
CONF_AUTH_ID: Final = "auth_id"
CONF_AUTH_KEY: Final = "auth_key"

# API endpoints
API_BASE: Final = "/api/v1"

# Authentication endpoints
API_AUTH_REQUEST: Final = f"{API_BASE}/auth/request"
API_AUTH_CHECK: Final = f"{API_BASE}/auth/check"
API_AUTH_VERIFY: Final = f"{API_BASE}/auth/verify"

# Printer status endpoints
API_PRINTER: Final = f"{API_BASE}/printer"
API_PRINTER_STATUS: Final = f"{API_BASE}/printer/status"
API_PRINTER_HEADS: Final = f"{API_BASE}/printer/heads"
API_PRINTER_HEAD: Final = f"{API_BASE}/printer/heads/{{head_id}}"
API_PRINTER_HEAD_POSITION: Final = f"{API_BASE}/printer/heads/{{head_id}}/position"
API_PRINTER_HEAD_EXTRUDERS: Final = f"{API_BASE}/printer/heads/{{head_id}}/extruders"
API_PRINTER_HEAD_EXTRUDER: Final = f"{API_BASE}/printer/heads/{{head_id}}/extruders/{{extruder_id}}"

# Temperature endpoints
API_BED_TEMPERATURE: Final = f"{API_BASE}/printer/bed/temperature"
API_HOTEND_TEMPERATURE: Final = f"{API_BASE}/printer/heads/{{head_id}}/extruders/{{extruder_id}}/hotend/temperature"

# Print job endpoints
API_PRINT_JOB: Final = f"{API_BASE}/print_job"
API_PRINT_JOB_STATE: Final = f"{API_BASE}/print_job/state"
API_PRINT_JOB_PROGRESS: Final = f"{API_BASE}/print_job/progress"
API_PRINT_JOB_NAME: Final = f"{API_BASE}/print_job/name"
API_PRINT_JOB_TIME_ELAPSED: Final = f"{API_BASE}/print_job/time_elapsed"
API_PRINT_JOB_TIME_TOTAL: Final = f"{API_BASE}/print_job/time_total"
API_PRINT_JOB_SOURCE: Final = f"{API_BASE}/print_job/source"

# Camera endpoints
API_CAMERA: Final = f"{API_BASE}/camera"
API_CAMERA_FEED: Final = f"{API_BASE}/camera/feed"
API_CAMERA_STREAM: Final = f"{API_BASE}/camera/{{index}}/stream"
API_CAMERA_SNAPSHOT: Final = f"{API_BASE}/camera/{{index}}/snapshot"

# LED endpoints
API_LED: Final = f"{API_BASE}/printer/led"
API_LED_HUE: Final = f"{API_BASE}/printer/led/hue"
API_LED_SATURATION: Final = f"{API_BASE}/printer/led/saturation"
API_LED_BRIGHTNESS: Final = f"{API_BASE}/printer/led/brightness"

# System endpoints
API_SYSTEM: Final = f"{API_BASE}/system"
API_SYSTEM_NAME: Final = f"{API_BASE}/system/name"
API_SYSTEM_GUID: Final = f"{API_BASE}/system/guid"
API_SYSTEM_FIRMWARE: Final = f"{API_BASE}/system/firmware"
API_SYSTEM_VARIANT: Final = f"{API_BASE}/system/variant"
API_SYSTEM_UPTIME: Final = f"{API_BASE}/system/uptime"

# Filament endpoints
API_FILAMENTS: Final = f"{API_BASE}/materials"
API_FILAMENT_GUID: Final = f"{API_BASE}/materials/{{material_guid}}"

# Update interval
UPDATE_INTERVAL: Final = 30  # seconds

# Authentication
AUTH_APP_NAME: Final = "MyLabManager"
AUTH_USER_NAME: Final = "HDFLabCesi"
AUTH_CHECK_INTERVAL: Final = 1  # seconds
AUTH_CHECK_TIMEOUT: Final = 60  # seconds

# Printer states
PRINTER_STATE_BOOTING: Final = "booting"
PRINTER_STATE_IDLE: Final = "idle"
PRINTER_STATE_PRINTING: Final = "printing"
PRINTER_STATE_ERROR: Final = "error"
PRINTER_STATE_MAINTENANCE: Final = "maintenance"

# Print job states
PRINT_JOB_STATE_NONE: Final = "none"
PRINT_JOB_STATE_PRINTING: Final = "printing"
PRINT_JOB_STATE_PAUSED: Final = "paused"
PRINT_JOB_STATE_ABORTED: Final = "abort"
PRINT_JOB_STATE_FINISHED: Final = "finished"

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
PLATFORMS: Final = ["sensor", "binary_sensor", "button", "camera"]