"""Constants for the Ultimaker integration."""
from typing import Final

DOMAIN: Final = "ultimaker"

PLATFORMS: Final = ["sensor", "binary_sensor", "button"]

# Configuration
CONF_HOST = "host"
CONF_NAME = "name"

# API endpoints
API_PRINTER = "/api/v1/printer"
API_PRINT_JOB = "/api/v1/print_job"
API_SYSTEM = "/api/v1/system"

# Update interval
UPDATE_INTERVAL = 10  # seconds

# Printer states
PRINTER_STATE_IDLE = "idle"
PRINTER_STATE_PRINTING = "printing"
PRINTER_STATE_PAUSED = "paused"
PRINTER_STATE_ERROR = "error"
PRINTER_STATE_OFFLINE = "offline"

# Attributes
ATTR_BED_TEMPERATURE = "bed_temperature"
ATTR_BED_TARGET = "bed_target"
ATTR_HOTEND_TEMPERATURE = "hotend_temperature"
ATTR_HOTEND_TARGET = "hotend_target"
ATTR_PROGRESS = "progress"
ATTR_PRINT_TIME = "print_time"
ATTR_ESTIMATED_TIME = "estimated_time"
ATTR_FILAMENT_USED = "filament_used"
ATTR_LAYER = "layer"
ATTR_LAYER_COUNT = "layer_count" 