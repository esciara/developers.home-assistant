---
date: 2025-11-20T23:03:36Z
researcher: Claude
git_commit: 17fa9427d6beb444fde8671d74fa05abba247f24
branch: create-claude-skill
repository: developers.home-assistant
topic: "Home Assistant Integration Development Documentation for Claude Code Skill Creation"
tags: [research, codebase, home-assistant, integrations, claude-code, skills]
status: complete
last_updated: 2025-11-20
last_updated_by: Claude
---

# Research: Home Assistant Integration Development Documentation for Claude Code Skill Creation

**Date**: 2025-11-20T23:03:36Z
**Researcher**: Claude
**Git Commit**: 17fa9427d6beb444fde8671d74fa05abba247f24
**Branch**: create-claude-skill
**Repository**: developers.home-assistant

## Research Question

Identify the parts of the Home Assistant developer documentation that will allow creation of a Claude Code skill to help developers create Home Assistant integrations following all best practices. The skill should guide users through the integration development process according to official Home Assistant standards.

## Summary

The Home Assistant developer documentation is comprehensive and well-organized, containing everything needed to create a Claude Code skill for integration development. The documentation is located in the `docs/` directory and covers:

1. **Integration Structure** - Manifest, file organization, naming conventions
2. **Configuration Flows** - UI-based setup, config entries, options flows
3. **Entity & Device Patterns** - Entity implementation, device registry, unique IDs
4. **Testing Requirements** - 95%+ coverage, config flow testing, validation
5. **Quality Standards** - Integration Quality Scale with Bronze/Silver/Gold/Platinum tiers
6. **Core Concepts** - State management, events, services, async patterns, data fetching
7. **Development Workflow** - Git workflow, code style, submission process

The documentation provides specific rules, code examples, and patterns that can be directly incorporated into a Claude Code skill to guide integration development.

## Key Documentation Categories for Skill Creation

### 1. Getting Started Files (Essential for Skill Introduction)

These files provide the foundational knowledge for integration development:

- `docs/creating_integration_manifest.md` - Integration manifest requirements and structure
- `docs/creating_integration_file_structure.md` - File organization and naming
- `docs/creating_component_index.md` - Component creation basics
- `docs/creating_platform_index.md` - Platform creation basics
- `docs/development_checklist.md` - Pre-submission checklist
- `docs/development_guidelines.md` - Code style and conventions

**Skill Usage**: Use these to guide initial integration setup, including scaffold usage and basic structure.

### 2. Configuration Flow Files (Critical for UI Setup)

Config flows are mandatory for all device/service integrations:

- `docs/config_entries_index.md` - Config entry lifecycle and management
- `docs/config_entries_config_flow_handler.md` - Config flow implementation (100% test coverage required)
- `docs/config_entries_options_flow_handler.md` - Options flow for settings
- `docs/data_entry_flow_index.md` - Form display, validation, user experience
- `docs/configuration_yaml_index.md` - YAML configuration (deprecated for devices/services)

**Key Requirements**:
- Must use config flows (not YAML) for device/service integrations
- 100% test coverage required for `config_flow.py`
- Must test connection before completing setup
- Must support reauthentication flow
- Unique IDs required for discoverable integrations

**Skill Usage**: Guide users through config flow creation with proper error handling, validation, and user experience patterns.

### 3. Entity Implementation Files (Core Integration Functionality)

Entities represent data points and controls:

- `docs/core/entity.md` - Base entity implementation
- `docs/entity_registry_index.md` - Entity registry and unique IDs
- `docs/device_registry_index.md` - Device registry and device info
- `docs/core/entity/*.md` - 41 entity type-specific files (sensor, switch, light, etc.)

**Mandatory Patterns**:
- `_attr_has_entity_name = True` for all new integrations
- `_attr_unique_id` using stable, unchangeable sources
- `_attr_device_info` for automatic device registration
- `_attr_device_class` when applicable
- Proper naming via `translation_key` or `None` for main features

**Skill Usage**: Provide entity implementation templates based on entity type, ensuring proper unique ID, device info, and naming patterns.

### 4. Testing Requirements (Quality Assurance)

Testing is mandatory with specific coverage thresholds:

- `docs/development_testing.md` - Testing framework and pytest usage
- `docs/development_validation.md` - Configuration validation
- `docs/core/integration-quality-scale/rules/test-coverage.md` - 95%+ coverage requirement
- `docs/core/integration-quality-scale/rules/config-flow-test-coverage.md` - 100% config flow coverage
- `docs/core/integration-quality-scale/rules/test-before-configure.md` - Connection testing in config flow
- `docs/core/integration-quality-scale/rules/test-before-setup.md` - Setup validation

**Critical Requirements**:
- 95% overall integration test coverage
- 100% config flow test coverage
- Tests must use core interfaces (not integration internals)
- Must test connection in config flow
- Must validate setup with proper exceptions (ConfigEntryNotReady, ConfigEntryAuthFailed, ConfigEntryError)
- Snapshot testing for large outputs

**Skill Usage**: Generate test templates with proper structure, fixtures, and coverage patterns.

### 5. Integration Quality Scale (Best Practices Framework)

The quality scale defines four tiers with specific requirements:

- `docs/core/integration-quality-scale/index.md` - Quality scale overview
- `docs/core/integration-quality-scale/checklist.md` - Quality checklist
- `docs/core/integration-quality-scale/_includes/tiers.json` - Rule mapping by tier
- `docs/core/integration-quality-scale/rules/*.md` - 50+ individual rule files

**Tier Structure**:
- **Bronze** (16 rules): Baseline for new integrations - config flow, entity patterns, basic testing
- **Silver** (10 rules): Reliability - error handling, reauthentication, code ownership
- **Gold** (21 rules): User experience - discovery, translations, full test coverage
- **Platinum** (3 rules): Technical excellence - async libraries, strict typing

**Key Rules for All Integrations**:
- `config-flow` - UI-based setup required
- `runtime-data` - Use ConfigEntry.runtime_data for non-persisted data
- `test-before-configure` - Test connection in config flow
- `test-before-setup` - Validate setup in async_setup_entry
- `entity-unique-id` - Provide unique IDs for all entities
- `has-entity-name` - Set _attr_has_entity_name = True
- `appropriate-polling` - Use reasonable polling intervals
- `action-exceptions` - Raise exceptions for service failures
- `entity-unavailable` - Mark entities unavailable on failures
- `reauthentication-flow` - Support credential updates
- `async-dependency` (Platinum) - Use asyncio-native libraries
- `strict-typing` (Platinum) - Full type annotations

**Skill Usage**: Use quality scale rules to guide best practices, providing specific implementation patterns for each requirement.

### 6. Core Concepts (Foundational Knowledge)

Understanding Home Assistant architecture is essential:

- `docs/dev_101_hass.md` - The hass object and core components
- `docs/dev_101_states.md` - State management
- `docs/dev_101_events.md` - Event system
- `docs/dev_101_services.md` - Service registration and handling
- `docs/asyncio_index.md` - Async programming overview
- `docs/asyncio_working_with_async.md` - Async implementation patterns
- `docs/integration_fetching_data.md` - DataUpdateCoordinator and data fetching

**Essential Patterns**:
- **hass object**: Central access to states, events, services, config
- **Async-first**: Use async_ prefixed methods within coroutines
- **State management**: domain.object_id format with JSON-serializable attributes
- **Event system**: Fire and listen with component-prefixed event names
- **Services**: Register in async_setup, use ServiceCall.data
- **DataUpdateCoordinator**: For single API serving multiple entities
- **Error handling**: ConfigEntryAuthFailed for auth, UpdateFailed for transient errors

**Skill Usage**: Provide architectural context and patterns for proper integration implementation.

### 7. Development Workflow (Submission Process)

Process for submitting integrations:

- `docs/development_submitting.md` - Git workflow and PR process
- `docs/development_checklist.md` - Pre-commit requirements
- `docs/review-process.md` - Code review expectations

**Critical Workflow Steps**:
1. Branch from `dev` (not `master`)
2. Run `python3 -m script.gen_requirements_all`
3. Run `python3 -m script.hassfest`
4. Run `ruff format`
5. Ensure 95%+ test coverage
6. Write documentation for home-assistant.io
7. Use proper commit message format (imperative, no component prefix)
8. Complete PR template

**Skill Usage**: Guide users through the complete development and submission workflow.

## Documentation Organization by File Location

### Core Integration Creation (7 files)
- `docs/creating_integration_manifest.md`
- `docs/creating_integration_file_structure.md`
- `docs/creating_integration_tests_file_structure.md`
- `docs/creating_integration_brand.md`
- `docs/creating_component_index.md`
- `docs/creating_component_code_review.md`
- `docs/creating_platform_index.md`

### Configuration System (5 files)
- `docs/config_entries_index.md`
- `docs/config_entries_config_flow_handler.md`
- `docs/config_entries_options_flow_handler.md`
- `docs/data_entry_flow_index.md`
- `docs/configuration_yaml_index.md`

### Entity & Device System (47 files)
- `docs/core/entity.md`
- `docs/entity_registry_index.md`
- `docs/device_registry_index.md`
- `docs/area_registry_index.md`
- `docs/core/entity/*.md` (41 entity type files)

### Testing & Validation (6 files)
- `docs/development_testing.md`
- `docs/development_validation.md`
- `docs/core/integration-quality-scale/rules/test-coverage.md`
- `docs/core/integration-quality-scale/rules/config-flow-test-coverage.md`
- `docs/core/integration-quality-scale/rules/test-before-configure.md`
- `docs/core/integration-quality-scale/rules/test-before-setup.md`

### Integration Quality Scale (53 files)
- `docs/core/integration-quality-scale/index.md`
- `docs/core/integration-quality-scale/checklist.md`
- `docs/core/integration-quality-scale/_includes/tiers.json`
- `docs/core/integration-quality-scale/rules/*.md` (50+ rule files)

### Core Concepts (12 files)
- `docs/dev_101_hass.md`
- `docs/dev_101_states.md`
- `docs/dev_101_events.md`
- `docs/dev_101_services.md`
- `docs/dev_101_config.md`
- `docs/asyncio_index.md`
- `docs/asyncio_working_with_async.md`
- `docs/asyncio_blocking_operations.md`
- `docs/asyncio_categorizing_functions.md`
- `docs/asyncio_thread_safety.md`
- `docs/integration_fetching_data.md`
- `docs/integration_setup_failures.md`

### Development Workflow (9 files)
- `docs/development_index.md`
- `docs/development_guidelines.md`
- `docs/development_checklist.md`
- `docs/development_submitting.md`
- `docs/development_testing.md`
- `docs/development_validation.md`
- `docs/development_typing.md`
- `docs/development_tips.md`
- `docs/review-process.md`

## Key Patterns and Requirements for Skill Implementation

### 1. Mandatory Integration Structure

Every integration must have:

```
homeassistant/components/<domain>/
├── manifest.json          # Integration metadata (REQUIRED)
├── __init__.py           # Component setup (REQUIRED)
├── config_flow.py        # Config flow handler (REQUIRED for devices/services)
├── strings.json          # Translations (REQUIRED with config_flow)
├── services.yaml         # Service definitions (if integration registers services)
├── <platform>.py         # Platform files (light.py, sensor.py, etc.)
└── coordinator.py        # DataUpdateCoordinator (recommended for polling)

tests/components/<domain>/
├── __init__.py           # Test discovery
├── conftest.py           # Pytest fixtures
├── test_init.py          # Setup/reload/unload tests
├── test_config_flow.py   # Config flow tests (100% coverage)
└── test_<platform>.py    # Platform-specific tests
```

### 2. Manifest Requirements

Minimum required fields:
- `domain` - Short name (characters and underscores, must match directory)
- `name` - Human-readable name
- `codeowners` - GitHub usernames responsible for integration
- `dependencies` - Other HA integrations required before setup
- `documentation` - Website URL with integration docs
- `integration_type` - One of: device, entity, hardware, helper, hub, service, system, virtual
- `iot_class` - One of: assumed_state, cloud_polling, cloud_push, local_polling, local_push, calculated
- `requirements` - PyPI package dependencies (pinned versions)

Optional but important:
- `config_flow: true` - Enables UI-based configuration
- `single_config_entry: true` - Limits to one config entry
- Discovery matchers (bluetooth, zeroconf, ssdp, homekit, mqtt, dhcp, usb)

### 3. Entity Implementation Template

```python
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo

class MySensor(SensorEntity):
    """Representation of a sensor."""

    _attr_has_entity_name = True  # REQUIRED for new integrations

    def __init__(self, device_id: str, device_name: str) -> None:
        """Initialize the sensor."""
        # Unique ID using stable source
        self._attr_unique_id = f"{device_id}_temperature"

        # Device info for automatic device registration
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=device_name,
            manufacturer="My Company",
            model="Model X",
            sw_version="1.0.0",
        )

        # Device class for proper representation
        self._attr_device_class = SensorDeviceClass.TEMPERATURE

        # Translation key for name
        self._attr_translation_key = "temperature"

        # For main feature, use None:
        # self._attr_name = None
```

### 4. Config Flow Template

```python
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
import voluptuous as vol

class MyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Test connection before completing
            client = MyClient(user_input[CONF_HOST])
            try:
                device_id = await client.get_device_id()
            except ConnectionError:
                errors["base"] = "cannot_connect"
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
            }),
            errors=errors,
        )
```

### 5. Setup Entry Template

```python
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady

type MyConfigEntry = ConfigEntry[MyClient]  # Custom typed config entry

async def async_setup_entry(hass: HomeAssistant, entry: MyConfigEntry) -> bool:
    """Set up from a config entry."""

    client = MyClient(entry.data[CONF_HOST])

    # Test setup and raise appropriate exceptions
    try:
        await client.async_setup()
    except OfflineException as ex:
        raise ConfigEntryNotReady("Device is offline") from ex
    except InvalidAuthException as ex:
        raise ConfigEntryAuthFailed("Invalid authentication") from ex

    # Store in runtime_data
    entry.runtime_data = client

    # Forward to platforms
    await hass.config_entries.async_forward_entry_setups(
        entry, ["sensor", "switch"]
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: MyConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(
        entry, ["sensor", "switch"]
    )
```

### 6. DataUpdateCoordinator Template

```python
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.exceptions import ConfigEntryAuthFailed
from datetime import timedelta

class MyCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator to manage data updates."""

    def __init__(self, hass: HomeAssistant, client: MyClient) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=1),
        )
        self.client = client

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API."""
        try:
            async with async_timeout.timeout(10):
                return await self.client.get_data()
        except AuthError as err:
            raise ConfigEntryAuthFailed from err
        except ApiError as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
```

### 7. Test Template

```python
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from pytest_homeassistant_custom_component.common import MockConfigEntry

async def test_setup_entry(hass: HomeAssistant, mock_client: AsyncMock) -> None:
    """Test setting up config entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_HOST: "192.168.1.1"},
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.LOADED
```

## Recommended Skill Structure

Based on the documentation analysis, the Claude Code skill should have the following structure:

### SKILL.md Sections

1. **Introduction**
   - What is a Home Assistant integration
   - Integration types (device, hub, service, etc.)
   - Quality scale overview

2. **Getting Started**
   - Using scaffold script: `python3 -m script.scaffold integration`
   - Manifest creation and required fields
   - File structure overview

3. **Config Flow Implementation**
   - Config flow basics and requirements
   - Connection testing patterns
   - Error handling
   - Reauthentication flow
   - Options flow

4. **Entity Implementation**
   - Entity types and base classes
   - Required attributes (has_entity_name, unique_id, device_info)
   - Device class and naming patterns
   - Update strategies (polling vs push)
   - DataUpdateCoordinator pattern

5. **Testing Requirements**
   - Test structure and organization
   - Coverage requirements (95% overall, 100% config flow)
   - Config flow testing patterns
   - Fixture usage
   - Snapshot testing

6. **Quality Scale Requirements**
   - Bronze tier (baseline)
   - Silver tier (reliability)
   - Gold tier (user experience)
   - Platinum tier (technical excellence)
   - Rule-by-rule guidance

7. **Development Workflow**
   - Git workflow (branch from dev)
   - Pre-commit scripts
   - Code style (ruff format)
   - Submission process
   - Documentation requirements

8. **Common Patterns**
   - Service registration
   - Event handling
   - State management
   - Async patterns
   - Error handling

### Supporting Files

Create reference documents for:
- `MANIFEST_REFERENCE.md` - Complete manifest field reference
- `ENTITY_TYPES.md` - Entity type-specific requirements
- `QUALITY_RULES.md` - All quality scale rules with examples
- `TESTING_GUIDE.md` - Comprehensive testing patterns
- `CODE_EXAMPLES.md` - Template code for common scenarios

### Skill Behavior

The skill should:
1. **Ask clarifying questions** about integration type, entity types needed
2. **Guide through setup** step-by-step (manifest → config flow → entities → tests)
3. **Enforce quality standards** by referencing specific rules
4. **Provide code templates** based on integration type and requirements
5. **Validate patterns** against documentation requirements
6. **Reference specific docs** with file paths and line numbers when applicable
7. **Generate tests** alongside implementation
8. **Check completeness** against development checklist

## Critical Requirements Summary

### Must-Have for All Integrations
- ✅ UI-based config flow (not YAML)
- ✅ 100% config flow test coverage
- ✅ Test connection in config flow
- ✅ Test setup in async_setup_entry
- ✅ Entity unique IDs from stable sources
- ✅ has_entity_name = True
- ✅ Device info for device registry
- ✅ 95%+ overall test coverage
- ✅ Proper exception handling (ConfigEntryNotReady, ConfigEntryAuthFailed, ConfigEntryError)
- ✅ Entity unavailability marking on failures
- ✅ Reauthentication flow support
- ✅ External PyPI library for device communication
- ✅ Code style via ruff format
- ✅ Documentation for home-assistant.io

### Best Practices
- Use DataUpdateCoordinator for polling
- Use runtime_data for non-persisted data
- Set appropriate polling intervals
- Mark entities unavailable on failures
- Log once when unavailable/restored
- Raise exceptions in service actions
- Use async-native libraries (Platinum)
- Full type annotations (Platinum)
- Support reconfiguration flow
- Implement diagnostics platform
- Support discovery when possible

## Next Steps for Skill Development

1. **Create SKILL.md** with comprehensive integration development guidance
2. **Add reference files** for manifest, entity types, quality rules
3. **Include code templates** for common patterns (config flow, entities, tests, coordinator)
4. **Test skill** by having it guide creation of a sample integration
5. **Iterate based on usage** to improve guidance and completeness

## Related Documentation

All files are located in `/Users/emmanuelsciara/Development/git-repos/home-assistant/developers.home-assistant/docs/`

Key entry points:
- Start: `development_index.md`
- Integration creation: `creating_component_index.md`
- Config flows: `config_entries_index.md`
- Entity implementation: `core/entity.md`
- Quality scale: `core/integration-quality-scale/index.md`
- Testing: `development_testing.md`

## Open Questions

None - the documentation is comprehensive and provides all necessary information for skill creation.