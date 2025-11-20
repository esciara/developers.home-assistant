"""The My Device integration with DataUpdateCoordinator (Phase 2)."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_API_KEY, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady, ConfigEntryAuthFailed

from .const import DOMAIN
from .coordinator import MyDeviceCoordinator

# List platforms that your integration supports
PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.LIGHT]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up My Device from a config entry with coordinator."""
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

    # Create coordinator
    # Scan interval from options or default to 30 seconds
    scan_interval = entry.options.get("scan_interval", 30)

    coordinator = MyDeviceCoordinator(
        hass,
        entry,
        api,
        update_interval=timedelta(seconds=scan_interval)
    )

    # Fetch initial data (with automatic retry)
    await coordinator.async_config_entry_first_refresh()

    # Store coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Forward setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Listen for options updates
    entry.async_on_unload(
        entry.add_update_listener(async_update_options)
    )

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


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    # Update coordinator interval
    coordinator: MyDeviceCoordinator = hass.data[DOMAIN][entry.entry_id]
    scan_interval = entry.options.get("scan_interval", 30)
    coordinator.update_interval = timedelta(seconds=scan_interval)
