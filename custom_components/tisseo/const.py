"""Constants for the Tisséo integration."""
from __future__ import annotations

from typing import Final

DOMAIN: Final = "tisseo"

# API
API_BASE_URL: Final = "https://api.tisseo.fr/v2"
DEFAULT_TIMEOUT: Final = 30

# Polling intervals
UPDATE_INTERVAL_FAST: Final = 60  # seconds for schedules
UPDATE_INTERVAL_SLOW: Final = 300  # seconds for lines/messages

# Defaults
DEFAULT_NUMBER_SCHEDULES: Final = 5
DEFAULT_NETWORK: Final = "Tisséo"

# Config keys
CONF_STOPS: Final = "stops"
CONF_STOP_ID: Final = "stop_id"
CONF_STOP_NAME: Final = "stop_name"
CONF_LINES: Final = "lines"
CONF_LINE_ID: Final = "line_id"
CONF_LINE_SHORT_NAME: Final = "line_short_name"
CONF_LINE_NAME: Final = "line_name"
CONF_JOURNEY: Final = "journey"
CONF_JOURNEY_ORIGIN: Final = "journey_origin"
CONF_JOURNEY_DESTINATION: Final = "journey_destination"

# Services
SERVICE_CALCULATE_JOURNEY: Final = "calculate_journey"
ATTR_DEPARTURE: Final = "departure"
ATTR_ARRIVAL: Final = "arrival"
ATTR_DATETIME: Final = "datetime"
