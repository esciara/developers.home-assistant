"""The My Device integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_API_KEY, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady, ConfigEntryAuthFailed

from .const import DOMAIN

# List platforms that your integration supports
PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up My Device from a config entry."""
    # Create API instance from external library
    from my_device_lib import MyDeviceAPI, ConnectionError, AuthenticationError

    api = MyDeviceAPI(
        entry.data[CONF_HOST],
        entry.data[CONF_API_KEY]
    )

    # Test connection
    try:
        await api.async_test_connection()
    except ConnectionError as err:
        raise ConfigEntryNotReady(f"Cannot connect to {api.host}") from err
    except AuthenticationError as err:
        raise ConfigEntryAuthFailed("Invalid credentials") from err

    # Store API instance for platforms to use
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = api

    # Forward setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS
    )

    # Remove stored data
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
