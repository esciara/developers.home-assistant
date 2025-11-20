# Entity Development Complete Guide

Entities represent devices, sensors, and controls in Home Assistant. This guide covers everything from basic entity properties to advanced patterns with coordinators.

## Entity Basics

### What is an Entity?

An entity is a representation of a device feature (sensor reading, light control, switch state, etc.).

**Entity ID format**: `domain.object_id`
- `light.kitchen` - Kitchen light
- `sensor.temperature` - Temperature sensor
- `switch.outlet_1` - Power outlet switch

**Key concepts**:
- **State**: Current value (on/off, temperature, etc.)
- **Attributes**: Additional metadata (brightness, unit, etc.)
- **Unique ID**: Permanent identifier for entity registry
- **Device**: Groups related entities

## Phase 1: Basic Entity

### Minimum Entity Implementation

```python
"""Sensor platform for My Device."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up My Device sensors from config entry."""
    api = hass.data[DOMAIN][entry.entry_id]

    # Create entities
    async_add_entities([
        MyDeviceSensor(api, entry),
    ])

class MyDeviceSensor(SensorEntity):
    """My Device sensor."""

    # Bronze tier requirements
    _attr_has_entity_name = True
    _attr_unique_id = "device123_sensor"

    def __init__(self, api, entry):
        """Initialize the sensor."""
        self.api = api
        self._attr_unique_id = f"{entry.entry_id}_sensor"

    async def async_update(self):
        """Fetch new state from API."""
        data = await self.api.async_get_data()
        self._attr_native_value = data["value"]
```

### Required Properties (Bronze Tier)

**1. has_entity_name = True** (MANDATORY):
```python
_attr_has_entity_name = True
```

This enables proper entity naming. Without it, you're not Bronze tier.

**2. unique_id** (MANDATORY):
```python
_attr_unique_id = "device_serial_123_temperature"
```

Enables entity registry. Without it, users cannot customize the entity.

**Format**: `f"{device_id}_{feature}"`
- ✅ `"abc123_temperature"`
- ✅ `"sensor_789_power"`
- ✅ `f"{entry.entry_id}_main"`
- ❌ `"sensor1"` (not unique across devices)

**3. name**:
```python
# Main feature
_attr_name = None  # → "Device Name"

# Secondary feature
_attr_name = "Temperature"  # → "Device Name Temperature"
```

**Naming rules** (MANDATORY):
- Main feature: `name = None`
- Secondary features: Descriptive name WITHOUT device type
- ✅ `"Temperature"`, `"Power"`, `"Status"`
- ❌ `"Sensor Temperature"`, `"MyDevice Power"`, `"Kitchen Temperature Sensor"`

**4. device_info** (Recommended):
```python
from homeassistant.helpers.entity import DeviceInfo

@property
def device_info(self) -> DeviceInfo:
    """Return device information."""
    return DeviceInfo(
        identifiers={(DOMAIN, self._device_id)},
        name="Device Name",
        manufacturer="Brand Name",
        model="Model 123",
        sw_version="1.0.0",
    )
```

Links entity to device in device registry.

### Entity Naming Examples

**❌ WRONG (Old pattern)**:
```python
_attr_has_entity_name = False
_attr_name = "Kitchen Temperature Sensor"
# Creates: sensor.kitchen_temperature_sensor
```

**✅ CORRECT (Bronze tier)**:
```python
_attr_has_entity_name = True
_attr_name = "Temperature"  # Device name added automatically
# Device name: "Kitchen Sensor"
# Creates: sensor.kitchen_sensor_temperature
# UI shows: "Kitchen Sensor Temperature"
```

**✅ CORRECT (Main feature)**:
```python
_attr_has_entity_name = True
_attr_name = None  # Main feature
# Device name: "Kitchen Light"
# Creates: sensor.kitchen_light
# UI shows: "Kitchen Light"
```

### Device Classes

Device classes provide semantic meaning and enable proper UI rendering.

**Sensor device classes** (examples):
```python
from homeassistant.components.sensor import SensorDeviceClass

_attr_device_class = SensorDeviceClass.TEMPERATURE
_attr_device_class = SensorDeviceClass.HUMIDITY
_attr_device_class = SensorDeviceClass.POWER
_attr_device_class = SensorDeviceClass.ENERGY
_attr_device_class = SensorDeviceClass.BATTERY
```

**Binary sensor device classes**:
```python
from homeassistant.components.binary_sensor import BinarySensorDeviceClass

_attr_device_class = BinarySensorDeviceClass.MOTION
_attr_device_class = BinarySensorDeviceClass.DOOR
_attr_device_class = BinarySensorDeviceClass.WINDOW
_attr_device_class = BinarySensorDeviceClass.MOISTURE
```

**See entity-specific docs for complete list**.

### Entity Categories

Categorize entities by purpose.

```python
from homeassistant.helpers.entity import EntityCategory

# Diagnostic entity (hidden by default)
_attr_entity_category = EntityCategory.DIAGNOSTIC

# Configuration entity (settings)
_attr_entity_category = EntityCategory.CONFIG

# No category (main features, shown by default)
# Don't set _attr_entity_category
```

**When to use**:
- `EntityCategory.DIAGNOSTIC` - Diagnostic info (signal strength, uptime, error counts)
- `EntityCategory.CONFIG` - Configuration settings
- No category - Main features users care about

### State Class (Sensors)

For sensors, specify how values should be treated.

```python
from homeassistant.components.sensor import SensorStateClass

# Measurement (current value)
_attr_state_class = SensorStateClass.MEASUREMENT

# Total (ever-increasing counter)
_attr_state_class = SensorStateClass.TOTAL

# Total increasing (can reset to zero)
_attr_state_class = SensorStateClass.TOTAL_INCREASING
```

**Examples**:
- `MEASUREMENT` - Temperature, humidity, power
- `TOTAL` - Total energy consumed (never resets)
- `TOTAL_INCREASING` - Session data usage (resets)

### Units

Specify native units for sensor values.

```python
from homeassistant.const import (
    UnitOfTemperature,
    UnitOfPower,
    UnitOfEnergy,
    PERCENTAGE,
)

_attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
_attr_native_unit_of_measurement = UnitOfPower.WATT
_attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
_attr_native_unit_of_measurement = PERCENTAGE
```

**Always use constants** from `homeassistant.const`.

## Update Strategies

### Strategy 1: Polling (Default)

Entity polls for updates periodically.

```python
class MyEntity(SensorEntity):
    """Polling entity."""

    _attr_should_poll = True  # Default, can be omitted

    async def async_update(self):
        """Fetch new state from API."""
        data = await self.api.async_get_sensor_data()
        self._attr_native_value = data["temperature"]
        self._attr_extra_state_attributes = {
            "last_updated": data["timestamp"],
        }
```

**Polling interval**: Default 30 seconds (configurable in platform setup).

**When to use**:
- Simple integrations
- No push notifications available
- Few entities (polling is inefficient for many entities)

### Strategy 2: Push

Device pushes updates, entity doesn't poll.

```python
class MyEntity(SensorEntity):
    """Push-based entity."""

    _attr_should_poll = False  # Disable polling

    def __init__(self, api):
        """Initialize."""
        self.api = api

    async def async_added_to_hass(self):
        """Entity added to Home Assistant."""
        # Subscribe to push updates
        self.async_on_remove(
            self.api.subscribe(
                self._device_id,
                self._handle_update
            )
        )

    @callback
    def _handle_update(self, data):
        """Handle pushed update."""
        self._attr_native_value = data["temperature"]
        self.async_write_ha_state()  # Trigger state write
```

**When to use**:
- Devices with push notifications (webhooks, websockets, MQTT)
- Real-time updates required
- IoT class: `local_push` or `cloud_push`

### Strategy 3: DataUpdateCoordinator (Recommended)

Centralized polling for all entities. See [COORDINATOR_GUIDE.md](COORDINATOR_GUIDE.md) for complete guide.

```python
from homeassistant.helpers.update_coordinator import CoordinatorEntity

class MyEntity(CoordinatorEntity, SensorEntity):
    """Coordinator-based entity."""

    _attr_should_poll = False  # Coordinator handles polling

    def __init__(self, coordinator, device_id):
        """Initialize."""
        super().__init__(coordinator, context=device_id)
        self.device_id = device_id
        self._attr_unique_id = f"{device_id}_temperature"

    @callback
    def _handle_coordinator_update(self):
        """Handle updated data from coordinator."""
        # Extract this entity's data
        data = self.coordinator.data[self.device_id]
        self._attr_native_value = data["temperature"]
        self.async_write_ha_state()
```

**Benefits**:
- Single API call for all entities
- Automatic error handling
- Context-aware fetching (only active entities)
- Required for Phase 2

## Entity Lifecycle

### Lifecycle Hooks

```python
async def async_added_to_hass(self):
    """Called when entity is added to Home Assistant (before first state write)."""
    # Subscribe to updates
    # Restore previous state
    # Set up listeners

async def async_will_remove_from_hass(self):
    """Called before entity is removed."""
    # Unsubscribe from updates
    # Close connections
    # Clean up resources
```

**Example - Push subscription**:
```python
async def async_added_to_hass(self):
    """Subscribe to device updates."""
    self.async_on_remove(
        self.api.subscribe(self._handle_update)
    )

async def async_will_remove_from_hass(self):
    """Unsubscribe from updates."""
    self.api.unsubscribe(self._handle_update)
```

### State Restoration

Restore state after Home Assistant restart.

```python
from homeassistant.helpers.restore_state import RestoreEntity

class MyEntity(RestoreEntity, SensorEntity):
    """Entity with state restoration."""

    async def async_added_to_hass(self):
        """Restore previous state."""
        last_state = await self.async_get_last_state()
        if last_state:
            self._attr_native_value = last_state.state
            # Restore attributes if needed
            if "custom_attr" in last_state.attributes:
                self._custom_value = last_state.attributes["custom_attr"]
```

## Device Registry

### DeviceInfo

Links entities to devices in device registry.

```python
from homeassistant.helpers.entity import DeviceInfo

@property
def device_info(self) -> DeviceInfo:
    """Return device information."""
    return DeviceInfo(
        identifiers={(DOMAIN, self._device_id)},
        name="Device Name",
        manufacturer="Brand Name",
        model="Model 123",
        model_id="model-123-rev-b",  # Optional: Specific model variant
        serial_number="SN123456",  # Optional
        hw_version="2.0",  # Optional: Hardware version
        sw_version="1.0.0",  # Firmware/software version
        configuration_url="http://192.168.1.100",  # Optional: Device config UI
        suggested_area="Living Room",  # Optional: Suggested area
    )
```

**Required fields**:
- `identifiers` - Unique device identifier tuple

**Recommended fields**:
- `name` - Device name
- `manufacturer` - Brand/manufacturer
- `model` - Model name
- `sw_version` - Firmware version

### Via Device (Hubs)

For devices connected through a hub:

```python
@property
def device_info(self) -> DeviceInfo:
    """Return device information."""
    return DeviceInfo(
        identifiers={(DOMAIN, self._device_id)},
        name="Bulb 1",
        manufacturer="Philips",
        model="Hue White",
        sw_version="1.2.3",
        via_device=(DOMAIN, self._hub_id),  # Links to hub
    )
```

## Platform Setup

### async_setup_entry

```python
async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up platform from config entry."""
    # Get shared data
    api = hass.data[DOMAIN][entry.entry_id]

    # Fetch device list
    devices = await api.async_get_devices()

    # Create entities
    entities = []
    for device in devices:
        entities.extend([
            TemperatureSensor(api, device),
            HumiditySensor(api, device),
            BatterySensor(api, device),
        ])

    # Add to Home Assistant
    async_add_entities(entities)
```

### Adding Entities Dynamically

For devices discovered after initial setup:

```python
async def async_setup_entry(hass, entry, async_add_entities):
    """Set up platform."""
    api = hass.data[DOMAIN][entry.entry_id]

    # Initial devices
    devices = await api.async_get_devices()
    async_add_entities([MyEntity(api, d) for d in devices])

    # Listen for new devices
    @callback
    def async_add_device(device):
        """Add new device."""
        async_add_entities([MyEntity(api, device)])

    # Store unsubscribe function
    entry.async_on_unload(
        api.subscribe_new_devices(async_add_device)
    )
```

## Common Entity Types

### Sensor

```python
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)

class TemperatureSensor(SensorEntity):
    """Temperature sensor."""

    _attr_has_entity_name = True
    _attr_name = "Temperature"
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    @property
    def native_value(self):
        """Return sensor value."""
        return self._temperature
```

### Binary Sensor

```python
from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)

class MotionSensor(BinarySensorEntity):
    """Motion sensor."""

    _attr_has_entity_name = True
    _attr_name = "Motion"
    _attr_device_class = BinarySensorDeviceClass.MOTION

    @property
    def is_on(self):
        """Return True if motion detected."""
        return self._motion_detected
```

### Light

```python
from homeassistant.components.light import (
    LightEntity,
    ColorMode,
    LightEntityFeature,
)

class MyLight(LightEntity):
    """Light entity."""

    _attr_has_entity_name = True
    _attr_name = None  # Main device feature
    _attr_supported_color_modes = {ColorMode.BRIGHTNESS}
    _attr_supported_features = LightEntityFeature.EFFECT

    @property
    def is_on(self):
        """Return True if light is on."""
        return self._is_on

    @property
    def brightness(self):
        """Return brightness (0-255)."""
        return self._brightness

    async def async_turn_on(self, **kwargs):
        """Turn on light."""
        if "brightness" in kwargs:
            await self.api.async_set_brightness(kwargs["brightness"])
        else:
            await self.api.async_turn_on()
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn off light."""
        await self.api.async_turn_off()
        self._is_on = False
        self.async_write_ha_state()
```

### Switch

```python
from homeassistant.components.switch import SwitchEntity

class MySwitch(SwitchEntity):
    """Switch entity."""

    _attr_has_entity_name = True
    _attr_name = None

    @property
    def is_on(self):
        """Return True if switch is on."""
        return self._is_on

    async def async_turn_on(self, **kwargs):
        """Turn on switch."""
        await self.api.async_turn_on()
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn off switch."""
        await self.api.async_turn_off()
        self._is_on = False
        self.async_write_ha_state()
```

## Best Practices

### ✅ Do

1. **Set `has_entity_name = True`** (Bronze tier requirement)
2. **Provide unique_id** for all entities
3. **Use device_info** to group entities
4. **Use device classes** for semantic meaning
5. **Cache state in `async_update()`**, not in properties
6. **Use DataUpdateCoordinator** for multiple entities (Phase 2)
7. **Clean up in `async_will_remove_from_hass()`**
8. **Use `@callback` for sync event handlers**
9. **Use `async_write_ha_state()` for push updates**
10. **Restore state** if needed with `RestoreEntity`

### ❌ Don't

1. **Don't do I/O in properties** - Use `async_update()` instead
2. **Don't pass `hass`** to entity constructor - Framework sets it
3. **Don't call `update()` in constructor** - Use `update_before_add=True` instead
4. **Don't include device type in name** - Use `has_entity_name = True` instead
5. **Don't block event loop** - Use async or executor
6. **Don't log sensitive data** - API keys, tokens, passwords
7. **Don't forget cleanup** - Unsubscribe in `async_will_remove_from_hass()`
8. **Don't poll with coordinator** - Set `should_poll = False`
9. **Don't use hardcoded IDs** - Generate from device data
10. **Don't skip unique_id** - Entity registry requires it

## Common Pitfalls

**Pitfall 1: I/O in properties**
```python
# ❌ BAD - Blocks event loop
@property
def native_value(self):
    return self.api.get_temperature()  # Blocking call!

# ✅ GOOD - Cache in async_update
async def async_update(self):
    self._attr_native_value = await self.api.async_get_temperature()
```

**Pitfall 2: Wrong naming**
```python
# ❌ BAD
_attr_has_entity_name = False
_attr_name = "Kitchen Temperature Sensor"

# ✅ GOOD
_attr_has_entity_name = True
_attr_name = "Temperature"
```

**Pitfall 3: Missing unique_id**
```python
# ❌ BAD - No unique_id
class MySensor(SensorEntity):
    _attr_has_entity_name = True
    _attr_name = "Temperature"

# ✅ GOOD - With unique_id
class MySensor(SensorEntity):
    _attr_has_entity_name = True
    _attr_unique_id = "device123_temperature"
    _attr_name = "Temperature"
```

## Phase 2: Advanced Entity Patterns

See [COORDINATOR_GUIDE.md](COORDINATOR_GUIDE.md) for DataUpdateCoordinator patterns.

**Phase 2 topics**:
- CoordinatorEntity integration
- Context-aware data fetching
- Parallel entity updates
- Advanced error handling

## Phase 3: Entity Translations

See [QUALITY_SCALE.md](QUALITY_SCALE.md) for Gold tier translation requirements.

**Translation structure** (strings.json):
```json
{
  "entity": {
    "sensor": {
      "temperature": {
        "name": "Temperature"
      },
      "humidity": {
        "name": "Humidity"
      }
    }
  }
}
```

## Next Steps

- See [COORDINATOR_GUIDE.md](COORDINATOR_GUIDE.md) for Phase 2 coordinator patterns
- See [TESTING_GUIDE.md](TESTING_GUIDE.md) for entity testing
- See [QUALITY_SCALE.md](QUALITY_SCALE.md) for Silver/Gold/Platinum requirements
