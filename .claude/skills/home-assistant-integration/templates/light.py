"""Light platform for My Device integration (with Coordinator)."""
from __future__ import annotations

from typing import Any

from homeassistant.components.light import (
    LightEntity,
    ColorMode,
    LightEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import MyDeviceCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up My Device lights from config entry."""
    coordinator: MyDeviceCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Create light entities
    # If multiple devices, iterate over them
    async_add_entities([
        MyDeviceLight(coordinator),
    ])


class MyDeviceLight(CoordinatorEntity, LightEntity):
    """Light entity for My Device."""

    # Bronze tier requirements
    _attr_has_entity_name = True
    _attr_name = None  # Main device feature
    _attr_supported_color_modes = {ColorMode.BRIGHTNESS}
    _attr_supported_features = LightEntityFeature.EFFECT

    def __init__(self, coordinator: MyDeviceCoordinator) -> None:
        """Initialize the light."""
        super().__init__(coordinator)

        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_light"

        # Device info links entity to device registry
        device_info = coordinator.device_info
        if device_info:
            self._attr_device_info = DeviceInfo(
                identifiers={(DOMAIN, device_info["id"])},
                name=device_info["name"],
                manufacturer=device_info.get("manufacturer"),
                model=device_info.get("model"),
                sw_version=device_info.get("sw_version"),
            )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from coordinator."""
        # Extract light state from coordinator data
        data = self.coordinator.data

        self._attr_is_on = data.get("light_state") == "on"
        self._attr_brightness = data.get("brightness")

        # Write updated state
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on light."""
        # Extract brightness from kwargs if provided
        brightness = kwargs.get("brightness")

        if brightness is not None:
            await self.coordinator.api.async_set_brightness(brightness)
        else:
            await self.coordinator.api.async_turn_on()

        # Request coordinator refresh to update state
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off light."""
        await self.coordinator.api.async_turn_off()

        # Request coordinator refresh to update state
        await self.coordinator.async_request_refresh()
