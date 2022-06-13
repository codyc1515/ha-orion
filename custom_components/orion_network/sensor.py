"""Orion Network sensors"""
from datetime import datetime, timedelta

import logging
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity

from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .api import OrionNetworkApi

from .const import (
    DOMAIN,
    SENSOR_NAME
)

NAME = DOMAIN
ISSUEURL = "https://github.com/codyc1515/hacs_orion_network/issues"

STARTUP = f"""
-------------------------------------------------------------------
{NAME}
This is a custom component
If you have any issues with this you need to open an issue here:
{ISSUEURL}
-------------------------------------------------------------------
"""

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({

})

SCAN_INTERVAL = timedelta(seconds=60)

async def async_setup_platform(hass, config, async_add_entities,
                               discovery_info=None):
    api = OrionNetworkApi()

    _LOGGER.debug('Setting up sensor(s)...')

    sensors = []
    sensors .append(OrionNetworkLoadManagementSensor(SENSOR_NAME, api))
    async_add_entities(sensors, True)

class OrionNetworkLoadManagementSensor(Entity):
    def __init__(self, name, api):
        self._name = name
        self._icon = "mdi:transmission-tower"
        self._state = ""
        self._state_attributes = {}
        self._unit_of_measurement = None
        self._device_class = "running"
        self._unique_id = DOMAIN
        self._api = api

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the sensor."""
        return self._state_attributes

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    @property
    def unique_id(self):
        """Return the unique id."""
        return self._unique_id
    
    def update(self):
        _LOGGER.debug('Fetching network load')
        response = self._api.get_load()
        if response:
            _LOGGER.debug(response)
            if response['shedding'] > 0:
                self._state = "On"
            else:
                self._state = "Off"
                
            self._state_attributes['Network Load'] = str(response['networkLoad']) + " MW"
            self._state_attributes['Network Limit'] = str(response['networkLimit']) + " MW"
            self._state_attributes['Shedding'] = str(response['shedding']) + "%"
        else:
            _LOGGER.error('Unable to fetch network load')
