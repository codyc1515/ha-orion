"""Orion Network sensors"""
from datetime import datetime, timedelta

import logging

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import OrionNetworkApi

from .const import (
    DOMAIN,
    SENSOR_NAME
)

NAME = DOMAIN
ISSUEURL = "https://github.com/codyc1515/ha-orion/issues"

STARTUP = f"""
-------------------------------------------------------------------
{NAME}
This is a custom component
If you have any issues with this you need to open an issue here:
{ISSUEURL}
-------------------------------------------------------------------
"""

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=60)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Initialize the entries."""

    api = OrionNetworkApi()

    async_add_entities([OrionNetworkLoadManagementSensor(api)], True)


class OrionNetworkLoadManagementSensor(SensorEntity):
    def __init__(self, api):
        self._name = SENSOR_NAME
        self._icon = "mdi:transmission-tower"
        self._state = None
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

    async def async_update(self) -> None:
        _LOGGER.debug('Fetching network load')

        response = self._api.get_load()
        if response:
            _LOGGER.debug(response)

            if self._state != "On" and response['shedding'] > 0:
                self._state = "On"
            elif self._state != "Off":
                self._state = "Off"

            self._state_attributes['Network Load'] = str(response['networkLoad']) + " MW"
            self._state_attributes['Network Limit'] = str(response['networkLimit']) + " MW"
            self._state_attributes['Shedding'] = str(response['shedding']) + "%"
        else:
            _LOGGER.error('Unable to fetch network load')
