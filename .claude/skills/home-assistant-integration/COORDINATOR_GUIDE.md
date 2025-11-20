# DataUpdateCoordinator Complete Guide (Phase 2)

DataUpdateCoordinator is the recommended pattern for integrations that poll APIs. It centralizes data fetching, error handling, and entity updates.

## Why Use DataUpdateCoordinator?

**Without coordinator** (Phase 1 - multiple entities polling independently):
```
Entity 1 → API call → Update state
Entity 2 → API call → Update state  # Duplicate API calls!
Entity 3 → API call → Update state  # Wasteful, rate-limit risk
```

**With coordinator** (Phase 2 - single coordinated poll):
```
Coordinator → Single API call → Fetch all data
    ↓
Entity 1, Entity 2, Entity 3 → Update from cached data
```

**Benefits**:
- ✅ Single API call for all entities
- ✅ Automatic error handling (ConfigEntryNotReady, ConfigEntryAuthFailed)
- ✅ Context-aware fetching (only fetch data for active entities)
- ✅ `always_update=False` prevents duplicate state writes
- ✅ Automatic retry with backoff on failures
- ✅ Consistent update timing across all entities

## Basic Coordinator Implementation

### Step 1: Create Coordinator Class

```python
"""DataUpdateCoordinator for My Device."""
from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

_LOGGER = logging.getLogger(__name__)

class MyDeviceCoordinator(DataUpdateCoordinator):
    """Coordinator to manage data fetching."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        api: MyDeviceAPI,
    ) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="My Device",
            config_entry=entry,
            update_interval=timedelta(seconds=30),
            always_update=False,  # Only update if data changed
        )
        self.api = api

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            # Fetch data from API
            return await self.api.async_get_all_data()
        except ApiError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
```

### Step 2: Create Coordinator in __init__.py

```python
"""The My Device integration."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_API_KEY
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import MyDeviceCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from config entry."""
    # Create API instance
    api = MyDeviceAPI(
        entry.data[CONF_HOST],
        entry.data[CONF_API_KEY]
    )

    # Create coordinator
    coordinator = MyDeviceCoordinator(hass, entry, api)

    # Fetch initial data (with retry)
    await coordinator.async_config_entry_first_refresh()

    # Store coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Forward setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, ["sensor"]
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
```

### Step 3: Create CoordinatorEntity

```python
"""Sensor platform for My Device."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import MyDeviceCoordinator

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors."""
    coordinator: MyDeviceCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Create entities using coordinator
    async_add_entities([
        TemperatureSensor(coordinator),
        HumiditySensor(coordinator),
    ])

class TemperatureSensor(CoordinatorEntity, SensorEntity):
    """Temperature sensor using coordinator."""

    _attr_has_entity_name = True
    _attr_name = "Temperature"

    def __init__(self, coordinator: MyDeviceCoordinator) -> None:
        """Initialize sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_temperature"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from coordinator."""
        # Extract this sensor's data
        self._attr_native_value = self.coordinator.data["temperature"]
        self.async_write_ha_state()
```

## Advanced Coordinator Patterns

### Context-Aware Fetching

Only fetch data for entities that are actually listening.

```python
class MyDeviceCoordinator(DataUpdateCoordinator):
    """Coordinator with context-aware fetching."""

    async def _async_update_data(self):
        """Fetch data from API."""
        # Get set of device IDs being listened to
        listening_devices = set(self.async_contexts())

        if not listening_devices:
            # No entities listening, skip fetch
            return {}

        # Only fetch data for active devices
        return await self.api.async_get_devices_data(listening_devices)
```

**Entity with context**:
```python
class DeviceSensor(CoordinatorEntity, SensorEntity):
    """Sensor with context."""

    def __init__(self, coordinator, device_id):
        """Initialize with context."""
        super().__init__(coordinator, context=device_id)
        self.device_id = device_id
        self._attr_unique_id = f"{device_id}_sensor"

    @callback
    def _handle_coordinator_update(self):
        """Handle updated data."""
        # Access data by context
        data = self.coordinator.data.get(self.device_id)
        if data:
            self._attr_native_value = data["value"]
            self.async_write_ha_state()
```

### Setup Phase with _async_setup

Run one-time initialization before first data fetch.

```python
class MyDeviceCoordinator(DataUpdateCoordinator):
    """Coordinator with setup phase."""

    def __init__(self, hass, entry, api):
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="My Device",
            config_entry=entry,
            update_interval=timedelta(seconds=30),
        )
        self.api = api
        self._device_info = None

    async def _async_setup(self):
        """Set up coordinator (called once on first refresh)."""
        # Fetch device information (one-time)
        self._device_info = await self.api.async_get_device_info()

    async def _async_update_data(self):
        """Fetch data from API."""
        # _async_setup() has already been called
        return await self.api.async_get_sensor_data()
```

### Authentication Error Handling

Trigger reauth flow automatically when credentials expire.

```python
from homeassistant.exceptions import ConfigEntryAuthFailed

class MyDeviceCoordinator(DataUpdateCoordinator):
    """Coordinator with auth error handling."""

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            return await self.api.async_get_data()
        except ApiAuthError as err:
            # Triggers reauth flow automatically
            raise ConfigEntryAuthFailed("Credentials expired") from err
        except ApiError as err:
            # Transient error, will retry
            raise UpdateFailed(f"Error: {err}") from err
```

**Note**: Reauth flow must be implemented in config_flow.py. See [CONFIG_FLOW_GUIDE.md](CONFIG_FLOW_GUIDE.md).

### Timeout Handling

Add timeout to prevent hanging on slow API calls.

```python
import asyncio

class MyDeviceCoordinator(DataUpdateCoordinator):
    """Coordinator with timeout."""

    async def _async_update_data(self):
        """Fetch data with timeout."""
        try:
            async with asyncio.timeout(10):  # 10 second timeout
                return await self.api.async_get_data()
        except TimeoutError as err:
            raise UpdateFailed("API request timed out") from err
        except ApiError as err:
            raise UpdateFailed(f"Error: {err}") from err
```

### Partial Updates with always_update

**`always_update=False`** (recommended): Only update entities if data actually changed.

```python
class MyDeviceCoordinator(DataUpdateCoordinator):
    """Coordinator with change detection."""

    def __init__(self, hass, entry, api):
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="My Device",
            config_entry=entry,
            update_interval=timedelta(seconds=30),
            always_update=False,  # Only update if data changed
        )
        self.api = api

    async def _async_update_data(self):
        """Fetch data."""
        data = await self.api.async_get_data()

        # Return data dict
        # Framework compares with previous data using __eq__
        return {
            "temperature": data["temperature"],
            "humidity": data["humidity"],
        }
```

**How it works**:
- Framework compares new data with previous data
- If `new_data != old_data`, entities are updated
- If data identical, no entity updates (saves CPU)

**For custom comparison**:
```python
from dataclasses import dataclass

@dataclass
class DeviceData:
    """Device data with custom equality."""

    temperature: float
    humidity: float
    last_updated: str  # Not compared

    def __eq__(self, other):
        """Compare only relevant fields."""
        if not isinstance(other, DeviceData):
            return False
        return (
            self.temperature == other.temperature
            and self.humidity == other.humidity
        )
```

## Configuration Options Integration

Use coordinator with user-configurable update interval.

**Options flow** (in config_flow.py):
```python
class MyDeviceOptionsFlow(config_entries.OptionsFlow):
    """Options flow."""

    async def async_step_init(self, user_input=None):
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    "scan_interval",
                    default=self.config_entry.options.get("scan_interval", 30)
                ): cv.positive_int,
            }),
        )
```

**Using in coordinator**:
```python
async def async_setup_entry(hass, entry):
    """Set up from config entry."""
    # Get scan interval from options (or use default)
    scan_interval = entry.options.get("scan_interval", 30)

    coordinator = MyDeviceCoordinator(
        hass,
        entry,
        api,
        update_interval=timedelta(seconds=scan_interval)
    )

    # Listen for option updates
    entry.async_on_unload(
        entry.add_update_listener(async_update_options)
    )

    return True

async def async_update_options(hass, entry):
    """Handle options update."""
    # Update coordinator interval
    coordinator = hass.data[DOMAIN][entry.entry_id]
    scan_interval = entry.options.get("scan_interval", 30)
    coordinator.update_interval = timedelta(seconds=scan_interval)
```

## Multiple Coordinators

Some integrations need multiple coordinators for different data types.

```python
async def async_setup_entry(hass, entry):
    """Set up with multiple coordinators."""
    api = MyDeviceAPI(...)

    # Coordinator for device state (fast polling)
    state_coordinator = MyDeviceStateCoordinator(
        hass, entry, api,
        update_interval=timedelta(seconds=10)
    )

    # Coordinator for statistics (slow polling)
    stats_coordinator = MyDeviceStatsCoordinator(
        hass, entry, api,
        update_interval=timedelta(minutes=5)
    )

    # Initial refresh
    await state_coordinator.async_config_entry_first_refresh()
    await stats_coordinator.async_config_entry_first_refresh()

    # Store both coordinators
    hass.data[DOMAIN][entry.entry_id] = {
        "state": state_coordinator,
        "stats": stats_coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True
```

**Entity using specific coordinator**:
```python
async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensors."""
    coordinators = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        # Fast-updating sensor uses state coordinator
        TemperatureSensor(coordinators["state"]),

        # Slow-updating sensor uses stats coordinator
        DailyEnergyUseSensor(coordinators["stats"]),
    ])
```

## Manual Refresh

Trigger coordinator refresh manually (e.g., from service call).

```python
async def async_setup_entry(hass, entry):
    """Set up with manual refresh service."""
    coordinator = MyDeviceCoordinator(...)

    # Register service to force refresh
    async def async_force_refresh(call):
        """Force coordinator refresh."""
        await coordinator.async_request_refresh()

    hass.services.async_register(
        DOMAIN,
        "force_refresh",
        async_force_refresh,
    )

    return True
```

## Error Recovery

### Transient Errors (UpdateFailed)

```python
async def _async_update_data(self):
    """Fetch data."""
    try:
        return await self.api.async_get_data()
    except ApiTemporaryError as err:
        # Will retry on next interval
        raise UpdateFailed(f"Temporary error: {err}") from err
```

**Behavior**:
- Coordinator sets `last_update_success = False`
- Entities retain last known state
- Next update retry happens on schedule
- No user intervention needed

### Permanent Errors (ConfigEntryNotReady)

Raise `ConfigEntryNotReady` from `async_setup_entry()`, not coordinator:

```python
async def async_setup_entry(hass, entry):
    """Set up from config entry."""
    api = MyDeviceAPI(...)

    try:
        # Test connection before creating coordinator
        await api.async_test_connection()
    except ConnectionError as err:
        raise ConfigEntryNotReady(f"Cannot connect to {api.host}") from err

    # Connection OK, create coordinator
    coordinator = MyDeviceCoordinator(hass, entry, api)
    await coordinator.async_config_entry_first_refresh()

    return True
```

### Authentication Errors (ConfigEntryAuthFailed)

```python
from homeassistant.exceptions import ConfigEntryAuthFailed

async def _async_update_data(self):
    """Fetch data."""
    try:
        return await self.api.async_get_data()
    except ApiAuthError as err:
        # Triggers reauth flow
        raise ConfigEntryAuthFailed("Credentials expired") from err
```

**Requires reauth flow** in config_flow.py.

## Testing with Coordinator

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for complete testing patterns.

**Mock coordinator in tests**:
```python
from unittest.mock import AsyncMock, MagicMock

async def test_sensor_with_coordinator(hass):
    """Test sensor using coordinator."""
    # Create mock coordinator
    coordinator = MagicMock()
    coordinator.data = {"temperature": 22.5}
    coordinator.last_update_success = True

    # Create entity
    sensor = TemperatureSensor(coordinator)

    # Test state
    assert sensor.native_value == 22.5
```

## Best Practices

### ✅ Do

1. **Use coordinator for multiple entities** - Single API call
2. **Set `always_update=False`** - Avoid unnecessary updates
3. **Use context for device-specific data** - Efficient fetching
4. **Handle auth errors with ConfigEntryAuthFailed** - Automatic reauth
5. **Use `_async_setup()` for one-time init** - Efficient startup
6. **Add timeouts to API calls** - Prevent hanging
7. **Raise UpdateFailed for transient errors** - Automatic retry
8. **Test coordinator error paths** - Complete coverage

### ❌ Don't

1. **Don't use coordinator for single entity** - Overhead not worth it
2. **Don't set `should_poll = True` on CoordinatorEntity** - Coordinator handles it
3. **Don't raise ConfigEntryNotReady from coordinator** - Use in setup instead
4. **Don't forget `async_config_entry_first_refresh()`** - Initial data fetch
5. **Don't poll too frequently** - Respect API rate limits
6. **Don't catch all exceptions** - Let framework handle coordinator errors
7. **Don't do I/O in entity properties** - Coordinator provides data
8. **Don't forget to unload coordinator** - Clean up properly

## Migration from Polling to Coordinator

**Before (Phase 1 - polling)**:
```python
class MySensor(SensorEntity):
    """Polling sensor."""

    _attr_should_poll = True

    async def async_update(self):
        """Fetch new state."""
        self._attr_native_value = await self.api.async_get_temperature()
```

**After (Phase 2 - coordinator)**:
```python
class MySensor(CoordinatorEntity, SensorEntity):
    """Coordinator-based sensor."""

    _attr_should_poll = False  # Coordinator handles updates

    def __init__(self, coordinator):
        """Initialize."""
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self):
        """Handle updated data."""
        self._attr_native_value = self.coordinator.data["temperature"]
        self.async_write_ha_state()
```

## Complete Example

See `templates/coordinator.py` and `templates/__init__-coordinator.py` for complete working examples.

## Next Steps

- See [TESTING_GUIDE.md](TESTING_GUIDE.md) for coordinator testing patterns
- See [ENTITY_GUIDE.md](ENTITY_GUIDE.md) for entity development
- See [QUALITY_SCALE.md](QUALITY_SCALE.md) for Silver tier requirements
