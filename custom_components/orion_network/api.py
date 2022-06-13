"""Orion Network API"""
import logging
import requests
import json

_LOGGER = logging.getLogger(__name__)

class OrionNetworkApi:
    def __init__(self):
        self._url_base = 'https://online.oriongroup.co.nz/loadmanagement/default.aspx'
        
    def get_load(self):
        response = requests.get(self._url_base)
        
        data = {}
        if response.status_code == requests.codes.ok:
            response = response.text
            
            networkLimit = response.split('lbTargetLoad">')
            networkLimit = networkLimit[1].split(' MW</span>')
            networkLimit = networkLimit[0]

            networkLoad = response.split('lbTotalNetwork">')
            networkLoad = networkLoad[1].split(' MW</span>')
            networkLoad = networkLoad[0]

            shedding = response.split('lbShedding">')
            shedding = shedding[1].split(' %</span>')
            shedding = shedding[0]
            
            data = {
                "networkLoad": int(networkLoad),
                "networkLimit": int(networkLimit),
                "shedding": int(shedding)
            }
            return data
        else:
            _LOGGER.error('Failed to fetch network load')
            return data
