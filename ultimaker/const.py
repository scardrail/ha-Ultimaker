"""Constants for the Ultimaker integration."""

DOMAIN = "ultimaker"

# Printer states
STATE_IDLE = "idle"
STATE_PRINTING = "printing"
STATE_PAUSED = "paused"
STATE_ERROR = "error"
STATE_MAINTENANCE = "maintenance"
STATE_PRE_PRINT = "pre_print"
STATE_POST_PRINT = "post_print"

# Sensor types
SENSOR_TYPES = {
    "temperature_bed": {
        "name": "Bed Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
    },
    "temperature_nozzle": {
        "name": "Nozzle Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
    },
    "progress": {
        "name": "Print Progress",
        "unit": "%",
        "icon": "mdi:progress-clock",
    },
    "time_remaining": {
        "name": "Time Remaining",
        "unit": "min",
        "icon": "mdi:clock-outline",
    },
    "time_elapsed": {
        "name": "Time Elapsed",
        "unit": "min",
        "icon": "mdi:clock",
    },
}

# Configuration
CONF_PRINTER_NAME = "printer_name"
CONF_PRINTER_ID = "printer_id"

# Default values
DEFAULT_NAME = "Ultimaker"
DEFAULT_UPDATE_INTERVAL = 30  # seconds 