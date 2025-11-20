"""DataUpdateCoordinator for My Device integration."""
from __future__ import annotations

import asyncio
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

_LOGGER = logging.getLogger(__name__)


class MyDeviceCoordinator(DataUpdateCoordinator):
    """Coordinator to manage data fetching from My Device API."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        api,
        update_interval: timedelta = timedelta(seconds=30),
    ) -> None:
        """Initialize My Device coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="My Device",
            config_entry=entry,
            update_interval=update_interval,
            always_update=False,  # Only update entities if data changed
        )
        self.api = api
        self._device_info = None

    async def _async_setup(self):
        """Set up coordinator (called once on first refresh)."""
        # Fetch device information (one-time)
        self._device_info = await self.api.async_get_device_info()
        _LOGGER.debug("Device info: %s", self._device_info)

    async def _async_update_data(self):
        """Fetch data from API."""
        from my_device_lib import ApiError, ApiAuthError

        try:
            # Add timeout to prevent hanging
            async with asyncio.timeout(10):
                # Fetch all device data
                data = await self.api.async_get_all_data()

                # Return data dict
                # Framework compares with previous data
                # Only updates entities if data changed (always_update=False)
                return data

        except ApiAuthError as err:
            # Authentication error - triggers reauth flow
            raise ConfigEntryAuthFailed("Credentials expired") from err

        except ApiError as err:
            # Temporary error - will retry on next interval
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    @property
    def device_info(self):
        """Return device information."""
        return self._device_info
