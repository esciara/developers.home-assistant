"""Config flow for My Device integration."""
from __future__ import annotations

from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_API_KEY
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN


class MyDeviceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for My Device."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Import here to avoid loading external library on startup
            from my_device_lib import (
                MyDeviceAPI,
                ConnectionError,
                AuthenticationError,
            )

            try:
                # Validate by attempting connection
                api = MyDeviceAPI(
                    user_input[CONF_HOST],
                    user_input[CONF_API_KEY]
                )
                await api.async_test_connection()

                # Get unique ID to prevent duplicates
                device_id = await api.async_get_device_id()
                await self.async_set_unique_id(device_id)
                self._abort_if_unique_id_configured()

                # Create config entry
                return self.async_create_entry(
                    title=user_input[CONF_HOST],
                    data=user_input
                )

            except ConnectionError:
                errors["base"] = "cannot_connect"
            except AuthenticationError:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                errors["base"] = "unknown"

        # Show form (first time or on error)
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): cv.string,
                vol.Required(CONF_API_KEY): cv.string,
            }),
            errors=errors,
        )
