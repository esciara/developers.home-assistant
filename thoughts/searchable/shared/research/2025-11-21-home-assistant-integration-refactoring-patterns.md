---
date: 2025-11-21T00:20:44Z
researcher: Claude
git_commit: 9a0290c9a05178b3779c0c0abbff5ddeba634b65
branch: create-claude-skill
repository: developers.home-assistant
topic: "Home Assistant Integration Refactoring & Migration Patterns"
tags: [research, refactoring, migration, home-assistant, integrations, patterns, quality-scale]
status: complete
last_updated: 2025-11-21
last_updated_by: Claude
related_research: ["2025-11-20-home-assistant-integration-skill-research.md"]
---

# Research: Home Assistant Integration Refactoring & Migration Patterns

**Date**: 2025-11-21T00:20:44Z
**Researcher**: Claude
**Git Commit**: 9a0290c9a05178b3779c0c0abbff5ddeba634b65
**Branch**: create-claude-skill
**Repository**: developers.home-assistant

## Research Question

Document all patterns, code examples, and procedures for refactoring and migrating existing Home Assistant integrations to modern standards. This research supports composable Claude Code skills focused on specific refactoring tasks (config flows, entities, testing, quality upgrades, etc.) that can be loaded independently to minimize context usage.

## Summary

Home Assistant provides comprehensive migration patterns and refactoring guides for updating legacy integrations to modern standards. The documentation includes specific before/after code examples, deprecation timelines, and quality tier upgrade paths. This research organizes these patterns into modular sections optimized for targeted skill loading.

## Document Organization

This document is organized into self-contained sections that can be referenced independently:

1. **Config Flow Refactoring** - Adding/updating UI-based configuration
2. **Entity Refactoring Patterns** - Modernizing entity implementations
3. **Quality Tier Upgrades** - Moving between Bronze/Silver/Gold/Platinum tiers
4. **Runtime Data Migration** - hass.data → ConfigEntry.runtime_data
5. **Config Entry Migration** - Updating config entry schemas
6. **Device & Discovery Patterns** - Adding device registry and discovery
7. **Authentication Flows** - Reauthentication and reconfiguration
8. **Testing Modernization** - Achieving 95%+ coverage
9. **Common API Deprecations** - Updating to current APIs
10. **Developer Tools** - Scripts for validation and migration

---

## 1. Config Flow Refactoring

### Adding Config Flow to YAML-Only Integration

**Reference**: `docs/config_entries_config_flow_handler.md:14-49`, `docs/configuration_yaml_index.md`

**When to use**: Legacy integration uses only YAML configuration, needs UI-based setup

**Step 1: Update manifest.json**

```json
{
  "domain": "example",
  "name": "Example",
  "config_flow": true,
  "version": "1"
}
```

**Step 2: Create config_flow.py**

```python
"""Config flow for Example integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

class ExampleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Example."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Test connection before completing
            try:
                client = MyClient(user_input[CONF_HOST], user_input[CONF_PASSWORD])
                device_id = await client.get_device_id()
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except InvalidAuthError:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Set unique ID and abort if already configured
                await self.async_set_unique_id(device_id)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input[CONF_HOST],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_PASSWORD): str,
            }),
            errors=errors,
        )
```

**Step 3: Create strings.json**

```json
{
  "config": {
    "step": {
      "user": {
        "title": "Connect to Example Device",
        "description": "Enter your device connection details",
        "data": {
          "host": "Host or IP address",
          "password": "Password"
        },
        "data_description": {
          "host": "The hostname or IP address of your Example device",
          "password": "The password configured on your Example device"
        }
      }
    },
    "error": {
      "invalid_auth": "Invalid authentication credentials",
      "cannot_connect": "Unable to connect to the device",
      "unknown": "Unexpected error occurred"
    },
    "abort": {
      "already_configured": "Device is already configured"
    }
  }
}
```

**Step 4: Update __init__.py for config entry support**

```python
"""The Example integration."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady, ConfigEntryAuthFailed

from .const import DOMAIN

PLATFORMS: list[str] = ["sensor", "switch"]

type ExampleConfigEntry = ConfigEntry[MyClient]

async def async_setup_entry(hass: HomeAssistant, entry: ExampleConfigEntry) -> bool:
    """Set up Example from a config entry."""
    client = MyClient(
        entry.data[CONF_HOST],
        entry.data[CONF_PASSWORD],
    )

    # Test setup and raise appropriate exceptions
    try:
        await client.async_setup()
    except ConnectionError as err:
        raise ConfigEntryNotReady("Device offline") from err
    except InvalidAuthError as err:
        raise ConfigEntryAuthFailed("Invalid credentials") from err

    # Store in runtime_data
    entry.runtime_data = client

    # Forward to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ExampleConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
```

**Step 5: Run validation**

```bash
python3 -m script.hassfest
```

**Step 6: Write config flow tests (100% coverage required)**

```python
"""Test Example config flow."""
from unittest.mock import AsyncMock, patch

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from .const import DOMAIN

async def test_user_flow_success(hass: HomeAssistant) -> None:
    """Test successful user flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"

    with patch("custom_components.example.config_flow.MyClient") as mock_client:
        mock_client.return_value.get_device_id = AsyncMock(return_value="device123")

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOST: "192.168.1.1", CONF_PASSWORD: "test"},
        )

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "192.168.1.1"
    assert result["data"][CONF_HOST] == "192.168.1.1"

async def test_user_flow_cannot_connect(hass: HomeAssistant) -> None:
    """Test user flow with connection error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.example.config_flow.MyClient.get_device_id",
        side_effect=ConnectionError,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOST: "192.168.1.1", CONF_PASSWORD: "test"},
        )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}

async def test_user_flow_already_configured(hass: HomeAssistant) -> None:
    """Test user flow with already configured device."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="device123",
        data={CONF_HOST: "192.168.1.1"},
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.example.config_flow.MyClient.get_device_id",
        return_value="device123",
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOST: "192.168.1.2", CONF_PASSWORD: "test"},
        )

    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "already_configured"
```

---

## 2. Entity Refactoring Patterns

### 2.1 Adding has_entity_name to Entities

**Reference**: `blog/2022-07-10-entity_naming.md`, `docs/core/integration-quality-scale/rules/has-entity-name.md:17-55`

**Before (Old Pattern):**

```python
class MySwitch(SwitchEntity):
    """Representation of a switch."""

    def __init__(self, device: MyDevice):
        """Initialize the switch."""
        self._device = device

    @property
    def name(self) -> str:
        """Return the name of the switch."""
        return f"{self._device.name} Power"  # Device name + entity name

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self._device.id}_power"
```

**After (Modern Pattern):**

```python
class MySwitch(SwitchEntity):
    """Representation of a switch."""

    _attr_has_entity_name = True

    def __init__(self, device: MyDevice):
        """Initialize the switch."""
        self._device = device
        self._attr_unique_id = f"{self._device.id}_power"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device.id)},
            name=self._device.name,
            manufacturer=self._device.manufacturer,
            model=self._device.model,
        )

    @property
    def name(self) -> str | None:
        """Return the name of the entity (without device name)."""
        return "Power"  # Only entity name, HA combines with device name

# For main device entity, use None:
class MyMainSwitch(SwitchEntity):
    """Main device switch."""

    _attr_has_entity_name = True

    def __init__(self, device: MyDevice):
        self._attr_unique_id = self._device.id
        self._attr_device_info = DeviceInfo(...)
        self._attr_name = None  # Entity inherits device name
```

**Using translation_key (preferred):**

```python
class MySwitch(SwitchEntity):
    """Representation of a switch."""

    _attr_has_entity_name = True
    _attr_translation_key = "power"

    def __init__(self, device: MyDevice):
        self._attr_unique_id = f"{self._device.id}_power"
        self._attr_device_info = DeviceInfo(...)

# In strings.json:
{
  "entity": {
    "switch": {
      "power": {
        "name": "Power"
      }
    }
  }
}
```

### 2.2 Adding Unique IDs to Entities

**Reference**: `docs/core/integration-quality-scale/rules/entity-unique-id.md:21-33`

**Before:**

```python
class MySensor(SensorEntity):
    """Temperature sensor without unique ID."""

    @property
    def name(self) -> str:
        return "Temperature"
```

**After:**

```python
class MySensor(SensorEntity):
    """Temperature sensor with unique ID."""

    _attr_has_entity_name = True
    _attr_translation_key = "temperature"

    def __init__(self, device: MyDevice):
        # Use stable, unchangeable identifier
        self._attr_unique_id = f"{device.serial_number}_temperature"
        # OR use device ID + sensor type
        # self._attr_unique_id = f"{device.id}_temp"
```

**Unique ID Requirements:**
- Must be stable across restarts
- Must not change when device is reconfigured
- Should use device serial number, MAC address, or API-provided unique identifier
- Must be unique across all entities in the integration

### 2.3 Native Value Properties (Number/Sensor Entities)

**Reference**: `blog/2022-06-14-number_entity_refactoring.md`

**Before (Deprecated in 2023.1):**

```python
class MyNumber(NumberEntity):
    """Number entity without unit conversion support."""

    @property
    def value(self) -> float:
        """Current value."""
        return self._device.temperature

    @property
    def max_value(self) -> float:
        """Max value."""
        return 50.0

    @property
    def min_value(self) -> float:
        """Min value."""
        return -10.0

    @property
    def unit_of_measurement(self) -> str:
        """Unit."""
        return UnitOfTemperature.CELSIUS

    async def async_set_value(self, value: float) -> None:
        """Set value."""
        await self._device.set_temperature(value)
```

**After (Required):**

```python
class MyNumber(NumberEntity):
    """Number entity with unit conversion support."""

    _attr_device_class = NumberDeviceClass.TEMPERATURE
    _attr_has_entity_name = True
    _attr_translation_key = "target_temperature"

    @property
    def native_value(self) -> float:
        """Current native value (device's native unit)."""
        return self._device.temperature

    @property
    def native_max_value(self) -> float:
        """Max native value."""
        return 50.0

    @property
    def native_min_value(self) -> float:
        """Min native value."""
        return -10.0

    @property
    def native_unit_of_measurement(self) -> str:
        """Native unit (what device uses)."""
        return UnitOfTemperature.CELSIUS

    async def async_set_native_value(self, value: float) -> None:
        """Set native value (in device's native unit)."""
        await self._device.set_temperature(value)
```

**Applies to:**
- `SensorEntity`: `native_value`, `native_unit_of_measurement`
- `NumberEntity`: `native_value`, `native_min_value`, `native_max_value`, `native_step`, `native_unit_of_measurement`
- `WeatherEntity`: `native_temperature`, `native_pressure`, etc.

### 2.4 Frozen EntityDescription

**Reference**: `blog/2023-12-11-entity-description-changes.md`

**Before (Deprecated in 2025.1):**

```python
from dataclasses import dataclass
from homeassistant.components.sensor import SensorEntityDescription

@dataclass
class MySensorDescription(SensorEntityDescription):
    """Custom sensor description."""
    custom_field: str = ""
```

**After (Required):**

```python
from dataclasses import dataclass
from homeassistant.components.sensor import SensorEntityDescription

@dataclass(frozen=True, kw_only=True)
class MySensorDescription(SensorEntityDescription):
    """Custom sensor description (frozen and keyword-only)."""
    custom_field: str = ""

# Usage
SENSOR_DESCRIPTIONS: tuple[MySensorDescription, ...] = (
    MySensorDescription(
        key="temperature",
        translation_key="temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        custom_field="example",
    ),
)
```

**Why:**
- `frozen=True`: Makes instances immutable, prevents accidental modification
- `kw_only=True`: Requires keyword arguments, protects against field order changes

### 2.5 Entity Availability Handling

**Reference**: `docs/core/integration-quality-scale/rules/entity-unavailable.md:14-76`

**Using DataUpdateCoordinator (Recommended):**

```python
from homeassistant.helpers.update_coordinator import CoordinatorEntity

class MySensor(CoordinatorEntity[MyCoordinator], SensorEntity):
    """Sensor with automatic availability from coordinator."""

    def __init__(self, coordinator: MyCoordinator, device_id: str):
        """Initialize sensor."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._attr_unique_id = f"{device_id}_temperature"

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        # Coordinator handles base availability, check if device exists in data
        return (
            super().available
            and self._device_id in self.coordinator.data
        )

    @property
    def native_value(self) -> float | None:
        """Return sensor value."""
        if device_data := self.coordinator.data.get(self._device_id):
            return device_data.temperature
        return None
```

**Direct async_update Pattern:**

```python
class MySensor(SensorEntity):
    """Sensor with manual availability tracking."""

    async def async_update(self) -> None:
        """Update sensor data."""
        try:
            data = await self._client.get_data()
        except ConnectionError:
            # Mark unavailable on connection errors
            if self._attr_available:
                _LOGGER.warning("Device became unavailable")
                self._attr_available = False
        except Exception:
            _LOGGER.exception("Unexpected error updating sensor")
            self._attr_available = False
        else:
            # Mark available on successful update
            if not self._attr_available:
                _LOGGER.info("Device is now available")
            self._attr_available = True
            self._attr_native_value = data.temperature
```

---

## 3. Quality Tier Upgrades

### Quality Scale Overview

**Reference**: `docs/core/integration-quality-scale/index.md`, `docs/core/integration-quality-scale/_includes/tiers.json`

Quality tiers are cumulative: Platinum requires Gold + Silver + Bronze requirements.

### 3.1 No Score/Legacy → Bronze

**Bronze Requirements (17 rules):**

1. ✅ Config flow with UI setup
2. ✅ Config flow test coverage
3. ✅ Entity unique IDs
4. ✅ `has_entity_name = True`
5. ✅ Runtime data in ConfigEntry
6. ✅ Test before configure
7. ✅ Test before setup
8. ✅ Appropriate polling intervals
9. ✅ Common modules usage
10. ✅ Branding information
11. ✅ Documentation (high-level description, installation, removal, actions)
12. ✅ Unique config entry handling

**Migration Checklist:**

```yaml
# Create quality_scale.yaml in integration root
rules:
  config-flow: done
  config-flow-test-coverage: done
  entity-unique-id: done
  has-entity-name: done
  runtime-data: done
  test-before-configure: done
  test-before-setup: done
  appropriate-polling: done
  brands: done
  docs-high-level-description: done
  docs-installation-instructions: done
  docs-removal-instructions: done
  docs-actions: done
  unique-config-entry: done
```

**Code Changes Required:**

1. **Add config flow** (see section 1)
2. **Update all entities:**
   ```python
   class MyEntity(SensorEntity):
       _attr_has_entity_name = True

       def __init__(self, device_id: str):
           self._attr_unique_id = f"{device_id}_sensor"
   ```
3. **Use runtime_data** (see section 4)
4. **Test connection in config flow** (see section 1, step 2)
5. **Test setup in async_setup_entry**:
   ```python
   try:
       await client.async_setup()
   except ConnectionError as err:
       raise ConfigEntryNotReady("Device offline") from err
   except AuthError as err:
       raise ConfigEntryAuthFailed("Invalid credentials") from err
   ```

### 3.2 Bronze → Silver

**Additional Silver Requirements (10 rules):**

1. ✅ Action exceptions handling
2. ✅ Config entry unloading
3. ✅ Entity unavailable marking
4. ✅ Integration owner (codeowners)
5. ✅ Log when unavailable
6. ✅ Parallel updates
7. ✅ Reauthentication flow
8. ✅ 90%+ test coverage
9. ✅ Configuration parameters documentation
10. ✅ Installation parameters documentation

**Code Changes Required:**

1. **Add reauthentication flow** (see section 7.1)
2. **Mark entities unavailable** (see section 2.5)
3. **Add codeowners to manifest.json:**
   ```json
   {
     "codeowners": ["@github_username"]
   }
   ```
4. **Implement proper unloading:**
   ```python
   async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
       """Unload config entry."""
       return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
   ```
5. **Reach 90%+ test coverage** (see section 8)

### 3.3 Silver → Gold

**Additional Gold Requirements (21 rules):**

1. ✅ Device creation and management
2. ✅ Discovery support
3. ✅ Entity translations
4. ✅ Reconfiguration flow
5. ✅ Diagnostics platform
6. ✅ Entity categories
7. ✅ Device classes
8. ✅ Disable non-critical entities by default
9. ✅ Comprehensive documentation (examples, troubleshooting, limitations, supported devices)
10. ✅ Dynamic device handling
11. ✅ Stale device cleanup

**Code Changes Required:**

1. **Add device info to entities** (see section 6.1)
2. **Implement discovery** (see section 6.2)
3. **Add entity translations** (see section 2.1)
4. **Add reconfiguration flow** (see section 7.2)
5. **Create diagnostics.py:**
   ```python
   from homeassistant.config_entries import ConfigEntry
   from homeassistant.core import HomeAssistant
   from homeassistant.helpers import device_registry as dr, entity_registry as er

   async def async_get_config_entry_diagnostics(
       hass: HomeAssistant, entry: ConfigEntry
   ) -> dict[str, Any]:
       """Return diagnostics for a config entry."""
       return {
           "entry": {
               "title": entry.title,
               "version": entry.version,
           },
           "data": entry.runtime_data.get_diagnostics(),
       }
   ```

### 3.4 Gold → Platinum

**Additional Platinum Requirements (3 rules):**

1. ✅ Async dependency (library uses asyncio)
2. ✅ Inject websession
3. ✅ Strict typing

**Code Changes Required:**

1. **Use async library** - Ensure PyPI dependency is asyncio-native
2. **Inject websession:**
   ```python
   from homeassistant.helpers.aiohttp_client import async_get_clientsession

   async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
       session = async_get_clientsession(hass)
       client = MyClient(session, entry.data[CONF_HOST])
   ```
3. **Add strict typing:**
   - Add integration to `.strict-typing` file in HA core
   - Add `py.typed` marker file to integration
   - Add type hints to all functions:
     ```python
     type MyConfigEntry = ConfigEntry[MyClient]

     async def async_setup_entry(
         hass: HomeAssistant,
         entry: MyConfigEntry,
     ) -> bool:
         """Set up from config entry."""
         ...
     ```

---

## 4. Runtime Data Migration

### Migrating from hass.data to ConfigEntry.runtime_data

**Reference**: `blog/2024-04-30-store-runtime-data-inside-config-entry.md`, `docs/core/integration-quality-scale/rules/runtime-data.md:22-37`

**Before (Old Pattern):**

```python
# __init__.py
DOMAIN = "example"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from config entry."""
    client = MyClient(entry.data[CONF_HOST])

    # Store in hass.data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = client

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload entry."""
    # Manual cleanup required
    hass.data[DOMAIN].pop(entry.entry_id)

    if not hass.data[DOMAIN]:
        hass.data.pop(DOMAIN)

    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

# sensor.py
async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors."""
    # Access from hass.data - error prone, no typing
    client = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([MySensor(client)])
```

**After (Modern Pattern):**

```python
# __init__.py
from dataclasses import dataclass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "example"

# Define type alias with "ConfigEntry" suffix
type ExampleConfigEntry = ConfigEntry[ExampleData]

@dataclass
class ExampleData:
    """Runtime data for Example integration."""
    client: MyClient
    coordinator: MyCoordinator | None = None

async def async_setup_entry(hass: HomeAssistant, entry: ExampleConfigEntry) -> bool:
    """Set up from config entry."""
    client = MyClient(entry.data[CONF_HOST])

    # Store in runtime_data - typed and auto-cleaned
    entry.runtime_data = ExampleData(client=client)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ExampleConfigEntry) -> bool:
    """Unload entry."""
    # No manual cleanup needed - runtime_data is auto-cleared
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

# sensor.py
from . import ExampleConfigEntry

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ExampleConfigEntry,  # Use typed config entry
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors."""
    # Access runtime_data with full typing support
    data = entry.runtime_data
    async_add_entities([MySensor(data.client)])
```

**Benefits:**
- ✅ Type-safe access to runtime data
- ✅ Automatic cleanup on unload
- ✅ No manual hass.data management
- ✅ Better IDE support and autocomplete
- ✅ Prevents memory leaks from forgotten cleanup

---

## 5. Config Entry Migration

### Updating Config Entry Schema

**Reference**: `docs/config_entries_config_flow_handler.md:237-270`, `docs/config_entries_index.md`

**When to use**: Config entry data structure needs to change (rename fields, add fields, change format)

**Version Management:**
- **Major version bump**: Breaking change, requires migration handler
- **Minor version bump**: Backward compatible, optional migration handler

**Migration Implementation:**

```python
# __init__.py
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate old entry to new format."""
    _LOGGER.debug(
        "Migrating configuration from version %s.%s",
        config_entry.version,
        config_entry.minor_version,
    )

    # Reject downgrades
    if config_entry.version > 2:
        _LOGGER.error("Cannot downgrade from version %s", config_entry.version)
        return False

    # Migrate from version 1 to 2
    if config_entry.version == 1:
        new_data = {**config_entry.data}

        # Example: Rename field
        if "host" in new_data:
            new_data["hostname"] = new_data.pop("host")

        # Example: Add new required field with default
        if "port" not in new_data:
            new_data["port"] = 80

        # Update to version 2
        hass.config_entries.async_update_entry(
            config_entry,
            data=new_data,
            version=2,
            minor_version=0,
        )

        _LOGGER.debug("Migration to version 2.0 successful")

    # Migrate minor versions within version 2
    if config_entry.version == 2:
        new_data = {**config_entry.data}

        if config_entry.minor_version < 2:
            # Minor version 1 → 2: Add optional field
            if "timeout" not in new_data:
                new_data["timeout"] = 10

        if config_entry.minor_version < 3:
            # Minor version 2 → 3: Convert string to int
            if isinstance(new_data.get("port"), str):
                new_data["port"] = int(new_data["port"])

        if config_entry.minor_version < 3:
            hass.config_entries.async_update_entry(
                config_entry,
                data=new_data,
                minor_version=3,
            )

    _LOGGER.debug(
        "Migration to configuration version %s.%s successful",
        config_entry.version,
        config_entry.minor_version,
    )
    return True
```

**Update config_flow.py VERSION:**

```python
class ExampleConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow."""

    VERSION = 2  # Increment when schema changes
    MINOR_VERSION = 3  # Increment for backward-compatible changes
```

**Testing Migration:**

```python
# tests/test_init.py
async def test_migrate_v1_to_v2(hass: HomeAssistant) -> None:
    """Test migration from version 1 to 2."""
    # Create old version config entry
    old_entry = MockConfigEntry(
        domain=DOMAIN,
        version=1,
        minor_version=0,
        data={
            "host": "192.168.1.1",  # Old field name
            "password": "test",
        },
    )
    old_entry.add_to_hass(hass)

    # Trigger migration
    assert await async_migrate_entry(hass, old_entry)

    # Verify migration
    assert old_entry.version == 2
    assert old_entry.minor_version == 0
    assert old_entry.data["hostname"] == "192.168.1.1"  # Renamed
    assert old_entry.data["port"] == 80  # Added default
    assert "host" not in old_entry.data  # Old field removed
```

---

## 6. Device & Discovery Patterns

### 6.1 Adding Device Registry Support

**Reference**: `docs/core/integration-quality-scale/rules/devices.md:15-40`, `docs/device_registry_index.md`

**Before (No devices):**

```python
class MySensor(SensorEntity):
    """Sensor without device."""

    _attr_has_entity_name = True
    _attr_unique_id = "sensor_123"
```

**After (With device):**

```python
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import DeviceInfo

class MySensor(SensorEntity):
    """Sensor with device information."""

    _attr_has_entity_name = True

    def __init__(self, device: MyDevice):
        """Initialize sensor."""
        self._attr_unique_id = f"{device.id}_temperature"

        # Add device info for automatic device registry
        self._attr_device_info = DeviceInfo(
            # Identifiers: unique set of IDs for this device
            identifiers={(DOMAIN, device.id)},

            # Connections: network identifiers (MAC, etc.)
            connections={(dr.CONNECTION_NETWORK_MAC, device.mac_address)},

            # Basic device info
            name=device.name,
            manufacturer=device.manufacturer,
            model=device.model,
            model_id="ABC-123",  # Specific model variant

            # Version information
            hw_version=device.hardware_version,
            sw_version=device.firmware_version,

            # Serial number
            serial_number=device.serial,

            # Configuration URL (device web interface)
            configuration_url=f"http://{device.ip_address}",

            # Hub device (if this device connects through a hub)
            via_device=(DOMAIN, device.hub_id),
        )
```

**Device Info Requirements:**
- `identifiers` (required): Unique identifier tuple(s)
- `connections` (optional): Network identifiers (MAC, etc.)
- `name` (required): Device name
- `manufacturer` (recommended): Manufacturer name
- `model` (recommended): Model name

### 6.2 Adding Discovery Support

**Reference**: `docs/core/integration-quality-scale/rules/discovery.md:30-111`

**Supported Discovery Types:**
- Zeroconf (mDNS)
- SSDP
- Bluetooth
- HomeKit
- MQTT
- DHCP
- USB

**Example: Zeroconf Discovery**

**Step 1: Add to manifest.json**

```json
{
  "domain": "example",
  "name": "Example",
  "zeroconf": [
    {
      "type": "_example._tcp.local.",
      "name": "example*"
    }
  ]
}
```

**Step 2: Implement discovery step in config_flow.py**

```python
from homeassistant import config_entries
from homeassistant.components.zeroconf import ZeroconfServiceInfo

class ExampleConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow with discovery."""

    VERSION = 1

    def __init__(self):
        """Initialize flow."""
        self._discovered_host: str | None = None
        self._discovered_name: str | None = None

    async def async_step_zeroconf(
        self, discovery_info: ZeroconfServiceInfo
    ) -> FlowResult:
        """Handle zeroconf discovery."""
        host = discovery_info.host
        name = discovery_info.name.removesuffix("._example._tcp.local.")

        # Get unique ID from device
        try:
            client = MyClient(host)
            unique_id = await client.get_serial_number()
        except Exception:
            return self.async_abort(reason="cannot_connect")

        # Set unique ID and update if already configured
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured(updates={CONF_HOST: host})

        # Store discovered info
        self._discovered_host = host
        self._discovered_name = name

        return await self.async_step_discovery_confirm()

    async def async_step_discovery_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm discovery."""
        if user_input is not None:
            return self.async_create_entry(
                title=self._discovered_name,
                data={CONF_HOST: self._discovered_host},
            )

        self._set_confirm_only()
        return self.async_show_form(
            step_id="discovery_confirm",
            description_placeholders={
                "name": self._discovered_name,
                "host": self._discovered_host,
            },
        )
```

**Step 3: Add strings for discovery**

```json
{
  "config": {
    "step": {
      "discovery_confirm": {
        "title": "Confirm discovered device",
        "description": "Found Example device '{name}' at {host}"
      }
    }
  }
}
```

---

## 7. Authentication Flows

### 7.1 Reauthentication Flow

**Reference**: `docs/core/integration-quality-scale/rules/reauthentication-flow.md:27-92`, `blog/2024-04-25-always-reload-after-successful-reauth-flow.md`

**When to use**: Handle expired credentials/tokens

**Implementation:**

```python
class ExampleConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow with reauthentication."""

    VERSION = 1

    reauth_entry: ConfigEntry | None = None

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> FlowResult:
        """Handle reauth upon credential expiration."""
        self.reauth_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm reauth dialog."""
        errors: dict[str, str] = {}

        if user_input is not None:
            assert self.reauth_entry is not None

            # Test new credentials
            try:
                client = MyClient(
                    self.reauth_entry.data[CONF_HOST],
                    user_input[CONF_PASSWORD],
                )
                await client.authenticate()
            except InvalidAuthError:
                errors["base"] = "invalid_auth"
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Update entry with new credentials
                return self.async_update_reload_and_abort(
                    self.reauth_entry,
                    data_updates={CONF_PASSWORD: user_input[CONF_PASSWORD]},
                )

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema({
                vol.Required(CONF_PASSWORD): str,
            }),
            errors=errors,
            description_placeholders={
                "host": self.reauth_entry.data[CONF_HOST],
            },
        )
```

**Trigger reauthentication from integration:**

```python
from homeassistant.exceptions import ConfigEntryAuthFailed

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from config entry."""
    client = MyClient(entry.data[CONF_HOST], entry.data[CONF_PASSWORD])

    try:
        await client.authenticate()
    except InvalidAuthError as err:
        # Trigger reauth flow
        raise ConfigEntryAuthFailed("Invalid credentials") from err
    except ConnectionError as err:
        raise ConfigEntryNotReady("Cannot connect") from err
```

**Strings:**

```json
{
  "config": {
    "step": {
      "reauth_confirm": {
        "title": "Reauthenticate",
        "description": "The credentials for {host} are no longer valid. Please enter new credentials."
      }
    }
  }
}
```

### 7.2 Reconfiguration Flow

**Reference**: `docs/core/integration-quality-scale/rules/reconfiguration-flow.md:31-58`, `blog/2024-03-21-config-entry-reconfigure-step.md`

**When to use**: Allow users to change non-credential setup data (host, port, etc.)

**Implementation:**

```python
class ExampleConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow with reconfiguration."""

    VERSION = 1

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle reconfiguration."""
        errors: dict[str, str] = {}
        reconfigure_entry = self._get_reconfigure_entry()

        if user_input is not None:
            # Validate new configuration
            try:
                client = MyClient(
                    user_input[CONF_HOST],
                    reconfigure_entry.data[CONF_PASSWORD],
                )
                device_id = await client.get_device_id()
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Verify it's the same device
                await self.async_set_unique_id(device_id)
                self._abort_if_unique_id_mismatch(reason="wrong_device")

                # Update and reload
                return self.async_update_reload_and_abort(
                    reconfigure_entry,
                    data_updates=user_input,
                )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema({
                vol.Required(
                    CONF_HOST,
                    default=reconfigure_entry.data.get(CONF_HOST),
                ): str,
            }),
            errors=errors,
        )
```

**Strings:**

```json
{
  "config": {
    "step": {
      "reconfigure": {
        "title": "Reconfigure device",
        "description": "Update the connection settings for your device."
      }
    }
  }
}
```

---

## 8. Testing Modernization

### Achieving Required Test Coverage

**Reference**: `docs/development_testing.md`, `docs/core/integration-quality-scale/rules/test-coverage.md:8-18`

**Coverage Requirements:**
- Bronze tier: Basic config flow tests
- Silver tier: 90%+ overall coverage
- Gold tier: 95%+ overall coverage
- Config flow: 100% coverage (always required)

### Test Structure

```
tests/components/example/
├── __init__.py
├── conftest.py              # Fixtures
├── test_init.py             # Setup/reload/unload tests
├── test_config_flow.py      # Config flow tests (100% coverage)
├── test_sensor.py           # Sensor platform tests
├── test_switch.py           # Switch platform tests
└── snapshots/               # Snapshot test data
    └── test_diagnostics.ambr
```

### Common Test Patterns

**Setup Entry Test:**

```python
"""Test Example integration."""
from unittest.mock import AsyncMock, patch

from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant

from tests.common import MockConfigEntry

async def test_setup_entry(hass: HomeAssistant, mock_client: AsyncMock) -> None:
    """Test setting up config entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_HOST: "192.168.1.1",
            CONF_PASSWORD: "test",
        },
    )
    entry.add_to_hass(hass)

    with patch("custom_components.example.MyClient", return_value=mock_client):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.LOADED
    assert len(mock_client.authenticate.mock_calls) == 1
```

**Unload Entry Test:**

```python
async def test_unload_entry(
    hass: HomeAssistant,
    mock_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test unloading config entry."""
    mock_config_entry.add_to_hass(hass)

    with patch("custom_components.example.MyClient", return_value=mock_client):
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED
```

**Setup Failure Test:**

```python
async def test_setup_entry_connection_error(
    hass: HomeAssistant,
    mock_client: AsyncMock,
) -> None:
    """Test setup with connection error raises ConfigEntryNotReady."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_HOST: "192.168.1.1"},
    )
    entry.add_to_hass(hass)

    mock_client.authenticate.side_effect = ConnectionError

    with patch("custom_components.example.MyClient", return_value=mock_client):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.SETUP_RETRY
```

**Config Flow Tests (100% Coverage Required):**

```python
"""Test Example config flow."""
from unittest.mock import AsyncMock, patch

import pytest

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from tests.common import MockConfigEntry

async def test_user_flow_success(hass: HomeAssistant) -> None:
    """Test successful user flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"

    with patch(
        "custom_components.example.config_flow.MyClient.get_device_id",
        return_value="device123",
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOST: "192.168.1.1", CONF_PASSWORD: "test"},
        )

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "192.168.1.1"
    assert result["data"] == {CONF_HOST: "192.168.1.1", CONF_PASSWORD: "test"}

async def test_user_flow_invalid_auth(hass: HomeAssistant) -> None:
    """Test user flow with invalid auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.example.config_flow.MyClient.get_device_id",
        side_effect=InvalidAuthError,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOST: "192.168.1.1", CONF_PASSWORD: "wrong"},
        )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {"base": "invalid_auth"}

async def test_user_flow_already_configured(hass: HomeAssistant) -> None:
    """Test user flow with already configured device."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="device123",
        data={CONF_HOST: "192.168.1.1"},
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.example.config_flow.MyClient.get_device_id",
        return_value="device123",
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOST: "192.168.1.2", CONF_PASSWORD: "test"},
        )

    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "already_configured"
```

**Fixtures (conftest.py):**

```python
"""Fixtures for Example tests."""
from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from homeassistant.const import CONF_HOST, CONF_PASSWORD

from tests.common import MockConfigEntry

@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Return a mock config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_HOST: "192.168.1.1",
            CONF_PASSWORD: "test",
        },
        unique_id="device123",
    )

@pytest.fixture
def mock_client() -> Generator[AsyncMock]:
    """Return a mocked client."""
    client = AsyncMock()
    client.authenticate = AsyncMock()
    client.get_device_id = AsyncMock(return_value="device123")
    client.get_data = AsyncMock(return_value={"temperature": 20.5})
    return client

@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(
    enable_custom_integrations: None,
) -> None:
    """Enable custom integrations."""
```

**Running Tests with Coverage:**

```bash
# Run all tests for integration
pytest tests/components/example/ -vv

# Run with coverage report
pytest tests/components/example/ \
    --cov=homeassistant.components.example \
    --cov-report=term-missing \
    -vv

# Run only config flow tests
pytest tests/components/example/test_config_flow.py -vv
```

---

## 9. Common API Deprecations

### 9.1 async_forward_entry_setup → async_forward_entry_setups

**Reference**: `blog/2024-06-12-async_forward_entry_setups.md`

**Before (Deprecated, removed in 2025.6):**

```python
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up entry."""
    # Load platforms one at a time
    await hass.config_entries.async_forward_entry_setup(entry, "sensor")
    await hass.config_entries.async_forward_entry_setup(entry, "switch")
    return True
```

**After (Required):**

```python
PLATFORMS: list[str] = ["sensor", "switch"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up entry."""
    # Load all platforms in parallel - MUST await
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
```

### 9.2 async_track_state_change → async_track_state_change_event

**Reference**: `blog/2024-04-13-deprecate_async_track_state_change.md`

**Before (Deprecated, removed in 2025.5):**

```python
from homeassistant.helpers.event import async_track_state_change

@callback
def _handle_state_change(
    entity_id: str,
    old_state: State | None,
    new_state: State | None,
) -> None:
    if new_state and new_state.state == "on":
        # Handle change

unsub = async_track_state_change(hass, "sensor.example", _handle_state_change)
```

**After (Required):**

```python
from homeassistant.core import Event, EventStateChangedData, callback
from homeassistant.helpers.event import async_track_state_change_event

@callback
def _handle_state_change_event(event: Event[EventStateChangedData]) -> None:
    """Handle state change event."""
    entity_id = event.data["entity_id"]
    old_state = event.data["old_state"]
    new_state = event.data["new_state"]

    if new_state and new_state.state == "on":
        # Handle change

unsub = async_track_state_change_event(
    hass, "sensor.example", _handle_state_change_event
)
```

### 9.3 hass.helpers.X → Direct Imports

**Reference**: `blog/2024-03-30-deprecate-hass-helpers.md`

**Before (Deprecated, removed in 2024.11):**

```python
async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up component."""
    session = hass.helpers.aiohttp_client.async_get_clientsession()
    dispatcher_send = hass.helpers.dispatcher.dispatcher_send
```

**After (Required):**

```python
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.dispatcher import dispatcher_send

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up component."""
    session = async_get_clientsession(hass)
    # Use dispatcher_send directly
```

### 9.4 DataUpdateCoordinator._async_update_data → _async_setup

**Reference**: `blog/2024-08-05-coordinator_async_setup.md`

**Before (Initialization in update method):**

```python
class MyCoordinator(DataUpdateCoordinator[MyData]):

    def __init__(self, hass: HomeAssistant, client: MyClient):
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)
        self.client = client
        self.device_info: DeviceInfo | None = None

    async def _async_update_data(self) -> MyData:
        """Fetch data."""
        # Must check if initialized every update
        if self.device_info is None:
            self.device_info = await self.client.get_device_info()

        return await self.client.get_data()
```

**After (Separate setup method):**

```python
class MyCoordinator(DataUpdateCoordinator[MyData]):

    device_info: DeviceInfo

    def __init__(self, hass: HomeAssistant, client: MyClient):
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)
        self.client = client

    async def _async_setup(self) -> None:
        """One-time setup before first update."""
        self.device_info = await self.client.get_device_info()

    async def _async_update_data(self) -> MyData:
        """Fetch data (setup already done)."""
        return await self.client.get_data()

# Usage
coordinator = MyCoordinator(hass, client)
await coordinator.async_config_entry_first_refresh()  # Calls _async_setup then _async_update_data
```

---

## 10. Developer Tools

### Script Commands

**Reference**: `docs/development_checklist.md`, `blog/2020-04-16-hassfest.md`

**Essential Commands:**

```bash
# Validate integration manifest and structure
python3 -m script.hassfest

# Update requirements_all.txt after adding dependencies
python3 -m script.gen_requirements_all

# Format code with ruff
ruff format homeassistant/components/example/

# Run tests with coverage
pytest tests/components/example/ \
    --cov=homeassistant.components.example \
    --cov-report=term-missing \
    -vv

# Create new integration scaffold
python3 -m script.scaffold integration
```

### Pre-Submission Checklist

**Reference**: `docs/development_checklist.md`

Before submitting integration:

1. ✅ Run `python3 -m script.gen_requirements_all`
2. ✅ Run `python3 -m script.hassfest`
3. ✅ Run `ruff format`
4. ✅ Ensure 95%+ test coverage
5. ✅ Ensure 100% config flow test coverage
6. ✅ Create quality_scale.yaml
7. ✅ Write documentation for home-assistant.io
8. ✅ Test on actual hardware/service
9. ✅ Verify translations in strings.json
10. ✅ Update .strict-typing if applicable

### GitHub Actions

**Hassfest Validation:**

```yaml
# .github/workflows/hassfest.yml
name: Hassfest

on:
  push:
  pull_request:

jobs:
  hassfest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: home-assistant/actions/hassfest@master
```

---

## Related Research

- **Creating New Integrations**: `thoughts/shared/research/2025-11-20-home-assistant-integration-skill-research.md`

## Key Documentation References

All documentation located in: `/Users/emmanuelsciara/Development/git-repos/home-assistant/developers.home-assistant/docs/`

**Config Flows:**
- `config_entries_index.md`
- `config_entries_config_flow_handler.md`
- `config_entries_options_flow_handler.md`

**Entity Patterns:**
- `core/entity.md`
- `core/entity/*.md` (entity type-specific)
- `entity_registry_index.md`

**Quality Scale:**
- `core/integration-quality-scale/index.md`
- `core/integration-quality-scale/rules/*.md`

**Testing:**
- `development_testing.md`
- `development_validation.md`

**Blog Posts (Migration Guides):**
- `blog/2022-07-10-entity_naming.md` - has_entity_name
- `blog/2022-06-14-number_entity_refactoring.md` - native_value
- `blog/2024-04-30-store-runtime-data-inside-config-entry.md` - runtime_data
- `blog/2024-06-12-async_forward_entry_setups.md` - Platform forwarding
- `blog/2024-08-05-coordinator_async_setup.md` - Coordinator setup

## Composable Skill Design Notes

This document is organized for modular skill loading:

- **Config Flow Skill**: Load section 1, 5, 7
- **Entity Refactoring Skill**: Load section 2
- **Quality Upgrade Skill**: Load section 3
- **Testing Skill**: Load section 8
- **Device & Discovery Skill**: Load section 6
- **API Migration Skill**: Load section 9

Each section is self-contained with code examples and can be loaded independently to minimize context usage.
