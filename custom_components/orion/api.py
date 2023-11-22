"""Orion Network API"""
import aiohttp
import asyncio
import logging

_LOGGER = logging.getLogger(__name__)


class OrionNetworkApi:
    def __init__(self):
        self._url_base = "https://online.oriongroup.co.nz/loadmanagement/default.aspx"

    async def get_load(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self._url_base) as response:
                data = {}
                if response.status == 200:
                    data = await response.text()

                    if not data:
                        _LOGGER.error("Failed to fetch network load")
                        return data

                    networkLimit = data.split('lbTargetLoad">')
                    networkLimit = networkLimit[1].split(" MW</span>")
                    networkLimit = networkLimit[0]

                    networkLoad = data.split('lbTotalNetwork">')
                    networkLoad = networkLoad[1].split(" MW</span>")
                    networkLoad = networkLoad[0]

                    shedding = data.split('lbShedding">')
                    shedding = shedding[1].split(" %</span>")
                    shedding = shedding[0]

                    data = {
                        "networkLoad": int(networkLoad),
                        "networkLimit": int(networkLimit),
                        "shedding": int(shedding),
                    }
                    return data
                else:
                    _LOGGER.error("Failed to fetch appointments")
                    return {}