---
name: home-assistant-integration-development
description: Create Home Assistant integrations following official best practices. Use when developing Home Assistant integrations, custom components, creating manifest.json, implementing config flows, or working with Home Assistant's integration architecture. Guides through scaffolding, config entries, coordinators, entities, testing, and quality standards.
---

# Home Assistant Integration Development

This skill guides you through creating Home Assistant integrations that follow all official best practices, from initial scaffolding through Bronze/Silver/Gold/Platinum quality tiers.

## Quick Start

The fastest way to create a new integration:

```bash
python3 -m script.scaffold integration
```

This scaffold tool generates:
- Complete file structure with manifest.json
- Config flow implementation
- Test file structure
- Translation infrastructure (strings.json)

**Follow the prompts** to specify:
- Domain name (lowercase, underscores, unique)
- Human-readable name
- Integration type (device, hub, service)
- IoT class (local_polling, local_push, cloud_polling, cloud_push)

## Phase 1: Core Workflow (MVP → Bronze Tier)

This phase gets you from zero to a working Bronze-tier integration.

### Step 1: Gather Requirements

Before running the scaffold tool, gather:

**Required Information**:
- **Domain**: Unique identifier (lowercase, underscores only, e.g., `my_device`)
- **Name**: Human-readable name (e.g., "My Device")
- **Integration Type**: Choose one:
  - `device` - Single device (smart bulb, thermostat)
  - `hub` - Gateway to multiple devices (Philips Hue bridge, Zigbee hub)
  - `service` - Single service per config entry (DuckDNS, weather service)
  - `helper` - Entity for automations (input_boolean, template sensor)
- **IoT Class**: Choose one:
  - `local_polling` - Direct device connection, delayed updates
  - `local_push` - Direct device connection, immediate updates
  - `cloud_polling` - Cloud API, delayed updates
  - `cloud_push` - Cloud API with webhooks, immediate updates
  - `assumed_state` - Cannot read state, assumes based on commands
  - `calculated` - Calculated result, no device communication
- **External Library**: PyPI package name for API calls (MUST be published to PyPI)

**Critical**: All API-specific code MUST be in an external PyPI library. The integration code only orchestrates library objects.

### Step 2: Run Scaffold Tool

```bash
# From repository root (developers.home-assistant/)
python3 -m script.scaffold integration

# Answer prompts:
# - Domain: my_device
# - Name: My Device
# - Type: device
# - IoT class: cloud_polling
```

This creates:
```
homeassistant/components/my_device/
├── __init__.py
├── manifest.json
├── config_flow.py
├── strings.json
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_config_flow.py
```

### Step 3: Customize manifest.json

See [MANIFEST_GUIDE.md](MANIFEST_GUIDE.md) for complete reference.

**Key fields to customize**:
```json
{
  "domain": "my_device",
  "name": "My Device",
  "codeowners": ["@your_github_username"],
  "config_flow": true,
  "dependencies": [],
  "documentation": "https://www.home-assistant.io/integrations/my_device",
  "integration_type": "device",
  "iot_class": "cloud_polling",
  "quality_scale": "bronze",
  "requirements": ["my-device-lib==1.2.3"]
}
```

**Critical requirements**:
- ✅ All requirements MUST be pinned: `"my-lib==1.2.3"` (NOT `"my-lib"`)
- ✅ Requirements MUST be published on PyPI (NOT GitHub URLs)
- ✅ `config_flow` MUST be `true` (Bronze tier requirement)
- ✅ `quality_scale` starts at `"bronze"`
- ✅ Add your GitHub username to `codeowners`

### Step 4: Implement Config Flow

The scaffold creates a basic config flow. Customize for your device.

See [CONFIG_FLOW_GUIDE.md](CONFIG_FLOW_GUIDE.md) for complete patterns.

**Minimum config flow** (templates/__init__.py and templates/config_flow.py):
```python
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_API_KEY
import voluptuous as vol

from .const import DOMAIN

class MyDeviceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow for My Device."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle user-initiated setup."""
        errors = {}

        if user_input is not None:
            # Validate credentials
            try:
                # Use your external library here
                device = MyDeviceAPI(
                    user_input[CONF_HOST],
                    user_input[CONF_API_KEY]
                )
                await device.async_test_connection()

                # Set unique ID (prevents duplicate config entries)
                device_id = await device.async_get_device_id()
                await self.async_set_unique_id(device_id)
                self._abort_if_unique_id_configured()

                # Create config entry
                return self.async_create_entry(
                    title=f"My Device ({user_input[CONF_HOST]})",
                    data=user_input  # Stored immutably
                )
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except AuthenticationError:
                errors["base"] = "invalid_auth"
            except Exception:
                errors["base"] = "unknown"

        # Show form
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_API_KEY): str,
            }),
            errors=errors,
        )
```

**Unique ID requirements** (CRITICAL):
- ✅ Use: Serial number, MAC address, device ID, account ID
- ❌ Don't use: IP address, hostname, device name, user-changeable values
- Must be stable across reboots and network changes

### Step 5: Implement Basic __init__.py

For Phase 1 (without DataUpdateCoordinator):

```python
"""The My Device integration."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_API_KEY
from homeassistant.core import HomeAssistant

from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up My Device from a config entry."""
    # Create API instance from external library
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
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, ["sensor"]
    )

    # Remove stored data
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
```

**Error handling**:
- `ConfigEntryNotReady` - Transient failures (network timeout, device offline). Home Assistant retries automatically.
- `ConfigEntryAuthFailed` - Authentication failures. Triggers reauth flow automatically.
- Do NOT log these yourself (framework logs them)

### Step 6: Create Platform Entity (Example: Sensor)

See [ENTITY_GUIDE.md](ENTITY_GUIDE.md) for complete patterns.

Create `sensor.py`:
```python
"""Sensor platform for My Device."""
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
    """Set up My Device sensors."""
    api = hass.data[DOMAIN][entry.entry_id]

    # Get device info from API
    device_info = await api.async_get_device_info()

    # Create sensor entities
    async_add_entities([
        MyDeviceTemperatureSensor(api, device_info, entry),
    ])

class MyDeviceTemperatureSensor(SensorEntity):
    """Temperature sensor for My Device."""

    # Required for Bronze tier
    _attr_has_entity_name = True
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, api, device_info, entry):
        """Initialize the sensor."""
        self.api = api
        self._attr_unique_id = f"{device_info['id']}_temperature"
        self._attr_name = "Temperature"  # → "Device Temperature"

        # Device info links entity to device registry
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_info["id"])},
            name=device_info["name"],
            manufacturer=device_info["manufacturer"],
            model=device_info["model"],
            sw_version=device_info["sw_version"],
        )

    async def async_update(self):
        """Fetch new state data."""
        # Called periodically by Home Assistant
        data = await self.api.async_get_sensor_data()
        self._attr_native_value = data["temperature"]
```

**Naming requirements** (Bronze tier):
- ✅ `_attr_has_entity_name = True` (mandatory)
- ✅ Main feature: `_attr_name = None` → "Device Name"
- ✅ Other features: `_attr_name = "Temperature"` → "Device Name Temperature"
- ❌ NEVER include device type in name

**Unique ID requirements**:
- ✅ Must be set for entity registry
- ✅ Format: `f"{device_id}_{feature}"` (e.g., `"abc123_temperature"`)
- ✅ Must be stable (same across restarts)

### Step 7: Write Config Flow Tests (100% Coverage Required)

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for complete patterns.

Update `tests/test_config_flow.py`:
```python
"""Test config flow for My Device."""
from unittest.mock import patch, AsyncMock

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_API_KEY
from homeassistant.core import HomeAssistant

from custom_components.my_device.const import DOMAIN

async def test_user_flow_success(hass: HomeAssistant):
    """Test successful user flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == "form"
    assert result["step_id"] == "user"

    # Mock API calls
    with patch(
        "custom_components.my_device.config_flow.MyDeviceAPI.async_test_connection",
        return_value=True,
    ), patch(
        "custom_components.my_device.config_flow.MyDeviceAPI.async_get_device_id",
        return_value="device123",
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_HOST: "192.168.1.100",
                CONF_API_KEY: "test-key",
            },
        )

    assert result["type"] == "create_entry"
    assert result["title"] == "My Device (192.168.1.100)"
    assert result["data"][CONF_HOST] == "192.168.1.100"

async def test_user_flow_cannot_connect(hass: HomeAssistant):
    """Test connection error handling."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.my_device.config_flow.MyDeviceAPI.async_test_connection",
        side_effect=ConnectionError,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOST: "192.168.1.100", CONF_API_KEY: "test-key"},
        )

    assert result["type"] == "form"
    assert result["errors"] == {"base": "cannot_connect"}

async def test_user_flow_invalid_auth(hass: HomeAssistant):
    """Test authentication error handling."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.my_device.config_flow.MyDeviceAPI.async_test_connection",
        side_effect=AuthenticationError,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOST: "192.168.1.100", CONF_API_KEY: "bad-key"},
        )

    assert result["type"] == "form"
    assert result["errors"] == {"base": "invalid_auth"}

async def test_duplicate_entry(hass: HomeAssistant):
    """Test duplicate entry is aborted."""
    # Create existing entry
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="device123",
        data={CONF_HOST: "192.168.1.100", CONF_API_KEY: "test-key"},
    )
    entry.add_to_hass(hass)

    # Try to add duplicate
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.my_device.config_flow.MyDeviceAPI.async_test_connection",
        return_value=True,
    ), patch(
        "custom_components.my_device.config_flow.MyDeviceAPI.async_get_device_id",
        return_value="device123",  # Same unique ID
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOST: "192.168.1.200", CONF_API_KEY: "test-key"},
        )

    assert result["type"] == "abort"
    assert result["reason"] == "already_configured"
```

**Critical**: 100% config flow test coverage is MANDATORY for Bronze tier.

### Step 8: Run Validation Tools

```bash
# 1. Update requirements_all.txt (if you added dependencies)
python3 -m script.gen_requirements_all

# 2. Validate manifest and codeowners
python3 -m script.hassfest

# 3. Format code
ruff format homeassistant/components/my_device/

# 4. Run all linters
pre-commit run --all-files

# 5. Run integration tests
pytest tests/components/my_device/ \
  --cov=homeassistant.components.my_device \
  --cov-report term-missing -vv

# 6. Verify 100% config flow coverage
pytest tests/components/my_device/test_config_flow.py --cov
```

All validation must pass before submission.

## Critical Requirements Checklist

### ✅ Must Do (Bronze Tier Minimum)

- ✅ All API code in external PyPI library (NOT in integration code)
- ✅ Config flow support (`"config_flow": true` in manifest)
- ✅ All requirements pinned with exact versions (`"lib==1.2.3"`)
- ✅ Entity unique IDs for all entities
- ✅ `has_entity_name = True` for all entities
- ✅ Device class and entity category support
- ✅ 100% config flow test coverage (MANDATORY)
- ✅ Async-first design (NEVER block the event loop)
- ✅ Error handling: `ConfigEntryNotReady`, `ConfigEntryAuthFailed`
- ✅ Type hints throughout code
- ✅ Pass all validation tools (hassfest, ruff, pre-commit, pytest)

### ❌ Must NOT Do

- ❌ API calls directly in integration code (use external library)
- ❌ Block the event loop (use `async`/`await` or `hass.async_add_executor_job()`)
- ❌ Log sensitive information (API keys, tokens, passwords)
- ❌ Do I/O in properties (cache in `async_update()` instead)
- ❌ Pass `hass` to entity constructor (HA sets it automatically)
- ❌ Call `update()` in constructor (use `update_before_add=True` instead)
- ❌ Skip pre-commit hooks
- ❌ Submit large PRs (single platform minimum for new integrations)
- ❌ Include device type in entity names (use `has_entity_name = True`)
- ❌ Use unpinned requirements

## Common Pitfalls

1. **Blocking the Event Loop**:
   ```python
   # ❌ BAD - Blocks event loop
   data = requests.get(url)

   # ✅ GOOD - Async
   data = await aiohttp_session.get(url)

   # ✅ GOOD - Blocking call in executor
   data = await hass.async_add_executor_job(blocking_function, arg)
   ```

2. **Missing Unique IDs**:
   ```python
   # ❌ BAD - No unique_id
   self._attr_name = "Temperature"

   # ✅ GOOD - With unique_id
   self._attr_unique_id = f"{device_id}_temperature"
   self._attr_name = "Temperature"
   ```

3. **Incorrect Naming**:
   ```python
   # ❌ BAD
   _attr_has_entity_name = False
   _attr_name = "My Device Temperature Sensor"

   # ✅ GOOD
   _attr_has_entity_name = True
   _attr_name = "Temperature"  # → "My Device Temperature"
   ```

4. **I/O in Properties**:
   ```python
   # ❌ BAD - Network call in property
   @property
   def native_value(self):
       return self.api.get_temperature()  # Blocks event loop!

   # ✅ GOOD - Cache in async_update
   async def async_update(self):
       self._attr_native_value = await self.api.async_get_temperature()
   ```

5. **Vague Config Flow Tests**:
   ```python
   # ❌ BAD - Not testing error paths
   async def test_config_flow(hass):
       result = await setup_flow(hass)
       assert result["type"] == "create_entry"

   # ✅ GOOD - Testing all paths
   async def test_user_flow_success(hass): ...
   async def test_user_flow_cannot_connect(hass): ...
   async def test_user_flow_invalid_auth(hass): ...
   async def test_duplicate_entry(hass): ...
   ```

## Next Steps: Phase 2 & Beyond

Once your Phase 1 integration works:

### Phase 2: Advanced Features
- **DataUpdateCoordinator**: Centralized polling for all entities → See [COORDINATOR_GUIDE.md](COORDINATOR_GUIDE.md)
- **Multiple Platforms**: Add light, switch, climate entities → See [ENTITY_GUIDE.md](ENTITY_GUIDE.md)
- **Reauth Flow**: Handle expired credentials → See [CONFIG_FLOW_GUIDE.md](CONFIG_FLOW_GUIDE.md)
- **Reconfigure Flow**: Update settings without re-adding → See [CONFIG_FLOW_GUIDE.md](CONFIG_FLOW_GUIDE.md)
- **Discovery**: Auto-discover devices via Bluetooth, Zeroconf, SSDP → See [CONFIG_FLOW_GUIDE.md](CONFIG_FLOW_GUIDE.md)

### Phase 3: Quality & Polish (Silver/Gold/Platinum)
- **Silver Tier**: 80%+ coverage, diagnostics, translations → See [QUALITY_SCALE.md](QUALITY_SCALE.md)
- **Gold Tier**: 90%+ coverage, strict typing, entity translations → See [QUALITY_SCALE.md](QUALITY_SCALE.md)
- **Platinum Tier**: 95%+ coverage, perfect implementation → See [QUALITY_SCALE.md](QUALITY_SCALE.md)

## Supporting Files Reference

- **[MANIFEST_GUIDE.md](MANIFEST_GUIDE.md)** - Complete manifest.json reference with all fields, types, and classes
- **[CONFIG_FLOW_GUIDE.md](CONFIG_FLOW_GUIDE.md)** - Config flow patterns, reauth, reconfigure, discovery
- **[ENTITY_GUIDE.md](ENTITY_GUIDE.md)** - Entity development, 41+ entity types, naming, registries
- **[COORDINATOR_GUIDE.md](COORDINATOR_GUIDE.md)** - DataUpdateCoordinator patterns for Phase 2
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Testing requirements, pytest patterns, coverage
- **[QUALITY_SCALE.md](QUALITY_SCALE.md)** - Bronze/Silver/Gold/Platinum tier requirements

## Templates

The `templates/` directory contains copy-paste ready files:
- `manifest.json` - Complete Bronze tier manifest
- `__init__.py` - Basic setup without coordinator
- `__init__-coordinator.py` - Setup with DataUpdateCoordinator (Phase 2)
- `config_flow.py` - Full config flow with reauth/reconfigure
- `coordinator.py` - Complete DataUpdateCoordinator implementation (Phase 2)
- `const.py` - Domain constants template
- `light.py` - Example light entity
- `sensor.py` - Example sensor entity
- `test_config_flow.py` - 100% coverage test template

## Version History

- v1.0.0 (2025-11-20): Initial release, all 3 phases, Bronze tier focus
