"""Diagnostics support for My Device integration (Silver tier)."""
from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

# Keys to redact from diagnostics
TO_REDACT = {
    "api_key",
    "token",
    "password",
    "serial_number",
    "mac_address",
}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    diagnostics_data = {
        "entry": {
            "title": entry.title,
            "data": dict(entry.data),
            "options": dict(entry.options),
        },
        "device_info": coordinator.device_info,
        "coordinator_data": coordinator.data,
        "last_update_success": coordinator.last_update_success,
        "last_update_time": coordinator.last_update_time.isoformat()
        if coordinator.last_update_time
        else None,
    }

    # Redact sensitive data
    return async_redact_data(diagnostics_data, TO_REDACT)
