"""Constants for the Ultimaker integration."""
from __future__ import annotations

from typing import Final

DOMAIN: Final = "ultimaker"

CONF_HOST: Final = "host"
CONF_NAME: Final = "name"

API_PRINTER: Final = "printer"
API_PRINT_JOB: Final = "print_job"
API_SYSTEM: Final = "system"

UPDATE_INTERVAL: Final = 30

PRINTER_STATE_OFFLINE: Final = "offline"

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

PLATFORMS: Final = ["sensor", "binary_sensor", "button"]