"""Sensor platform for My Device integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up My Device sensors from config entry."""
    api = hass.data[DOMAIN][entry.entry_id]

    # Get device info from API
    device_info = await api.async_get_device_info()

    # Create sensor entities
    async_add_entities([
        MyDeviceTemperatureSensor(api, device_info, entry),
    ])


class MyDeviceTemperatureSensor(SensorEntity):
    """Temperature sensor for My Device."""

    # Bronze tier requirements
    _attr_has_entity_name = True
    _attr_name = "Temperature"
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, api, device_info, entry):
        """Initialize the sensor."""
        self.api = api
        self._device_info = device_info
        self._attr_unique_id = f"{entry.entry_id}_temperature"

        # Device info links entity to device registry
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_info["id"])},
            name=device_info["name"],
            manufacturer=device_info.get("manufacturer"),
            model=device_info.get("model"),
            sw_version=device_info.get("sw_version"),
        )

    async def async_update(self):
        """Fetch new state data."""
        # Called periodically by Home Assistant (polling)
        data = await self.api.async_get_sensor_data()
        self._attr_native_value = data.get("temperature")
