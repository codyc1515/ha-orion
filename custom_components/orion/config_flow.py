"""Config flow for Orion Network."""
from __future__ import annotations

from collections.abc import Awaitable
from typing import Any

from homeassistant.config_entries import ConfigFlow
from homeassistant.data_entry_flow import FlowResult

from .const import SENSOR_NAME, DOMAIN


class OrionNetworkConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for Orion Network."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        return self.async_create_entry(title=SENSOR_NAME, data={})

    async def async_step_import(self, user_input: dict[str, Any]) -> FlowResult:
        """Handle import from configuration.yaml."""
        return await self.async_step_user(user_input)