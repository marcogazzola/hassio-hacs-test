"""Component to create and remove Hass.io snapshots."""
import logging
from datetime import datetime, timedelta, timezone

import voluptuous as vol

import homeassistant.helpers.config_validation as cv

from homeassistant.components.hassio.const import X_HASSIO
from homeassistant.components.hassio.handler import HassioAPIError
from homeassistant.const import ATTR_NAME
from homeassistant.helpers.json import JSONEncoder
from homeassistant.helpers.storage import Store
from homeassistant.helpers.typing import ConfigType, HomeAssistantType, ServiceCallType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "air_quality_monitor"
SCHEMA_REFRESH_RATE = "refresh_rate"
SCHEMA_CREATE_SENSORS = "create_sensor"
SCHEMA_UNIT_OF_MEASUREMENT = "unit_of_measurement"
SCHEMA_REGIONS = "regions"
SCHEMA_URL = "url"
SCHEMA_STATION_ID = "station_id"
SCHEMA_MONITORED_PARAMS = "monitored_params"

REGION_SCHEMA = vol.Schema(
  {
      vol.Required(SCHEMA_URL): cv.url,
      vol.Required(SCHEMA_STATION_ID): cv.string,
      vol.Optional(SCHEMA_MONITORED_PARAMS, default=[]): vol.All(cv.ensure_list, [cv.string]),
  }
)
REGIONS_CONTAINER_SCHEMA = vol.Schema(
  {str: REGION_SCHEMA}
)

CONFIG_SCHEMA = vol.Schema(
  {
      DOMAIN: {
          vol.Optional(SCHEMA_REFRESH_RATE, default=6): vol.Coerce(int),
          vol.Optional(SCHEMA_CREATE_SENSORS, default=True): cv.boolean,
          vol.Optional(SCHEMA_UNIT_OF_MEASUREMENT, default=[]): vol.All(cv.ensure_list, [cv.string]),
          vol.Required(SCHEMA_REGIONS): vol.All(REGIONS_CONTAINER_SCHEMA)
      }
  },
  extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass: HomeAssistantType, config: ConfigType):
  """Setup"""
  _LOGGER.info("*********** STARTUP AIR QUALITY ***********")

  config = config[DOMAIN]
  _LOGGER.info(config)

  return True