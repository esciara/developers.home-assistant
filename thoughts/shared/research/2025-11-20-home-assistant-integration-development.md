---
date: 2025-11-20T21:17:50+00:00
researcher: Claude
git_commit: cfe3dab398c272ae5271f086dc05ab2d7488bdcf
branch: claude/home-assistant-integration-skill-01T9LctSUCa3AjQpfkMro4yC
repository: developers.home-assistant
topic: "Home Assistant Integration Development - Documentation for Claude Code Skill Creation"
tags: [research, codebase, home-assistant, integration-development, best-practices, testing, quality-scale, claude-skills]
status: complete
last_updated: 2025-11-20T23:05:11+00:00
last_updated_by: Claude
last_updated_note: "Added comprehensive Claude Code Skills best practices section and updated recommendations for skill creation"
---

# Research: Home Assistant Integration Development - Documentation for Claude Code Skill Creation

**Date**: 2025-11-20T21:17:50+00:00
**Researcher**: Claude
**Git Commit**: cfe3dab398c272ae5271f086dc05ab2d7488bdcf
**Branch**: claude/home-assistant-integration-skill-01T9LctSUCa3AjQpfkMro4yC
**Repository**: developers.home-assistant

## Research Question

This repository contains all the developer documentation for the Home Assistant smart home controller. The goal is to identify the parts of the documentation that will enable creation of a Claude Code skill for building Home Assistant integrations following all documented best practices.

## Summary

Home Assistant provides comprehensive developer documentation covering the entire integration development lifecycle. This research combines that documentation with Claude Code Skills best practices to enable creation of an effective development skill.

**Home Assistant Documentation Coverage**:
1. **Getting Started & Scaffolding**: Quick-start tools and file structure requirements
2. **Core Concepts**: Architecture, asyncio patterns, events, services, states
3. **Configuration System**: Config entries, config flows, data entry flows
4. **Entity Development**: 41+ entity types, platforms, registries, naming conventions
5. **Data Management**: Coordinators, polling vs push, error handling
6. **Testing**: pytest framework, snapshot testing, 100% config flow coverage requirement
7. **Code Review & Quality**: Style guides, validation, quality scale tiers (Bronze-Platinum)
8. **Best Practices**: Development guidelines, common pitfalls, submission standards

**Claude Code Skills Best Practices**:
- Model-invoked activation via description triggers
- SKILL.md file structure with YAML frontmatter
- Progressive disclosure with supporting files
- Tool access restrictions with allowed-tools
- Focused, single-capability design
- Clear testing and debugging guidance
- Team sharing via project skills or plugins

The research provides a complete blueprint for creating a Claude Code Skill that guides developers through Home Assistant integration development following all documented best practices.

## Detailed Findings

### 1. Integration Creation Process

**Quick Start**
**File**: `docs/creating_component_index.md`

The fastest way to create a new integration:
```bash
python3 -m script.scaffold integration
```

This scaffold tool generates:
- Complete file structure with manifest.json
- Config flow implementation
- Test file structure
- Translation infrastructure (strings.json)

**8-Phase Development Cycle**:
1. Setup & Planning - Choose domain, integration type, development environment
2. Scaffolding - Run scaffold tool to generate starter files
3. Core Implementation - manifest.json, __init__.py, config_flow.py
4. Platform Implementation - Create light.py, switch.py, sensor.py etc.
5. Data Fetching - Implement polling with DataUpdateCoordinator or push subscriptions
6. Testing - Write pytest tests with proper coverage
7. Code Quality - Follow guidelines, style, validation
8. Documentation - Add strings, branding, diagnostics

### 2. File Structure & Organization

**File**: `docs/creating_integration_file_structure.md:1-50`

**Minimum Required Files**:
```
domain_name/
├── __init__.py        # Component setup entry point
└── manifest.json      # Integration metadata
```

**Common Optional Files**:
```
domain_name/
├── config_flow.py     # UI-based configuration
├── coordinator.py     # DataUpdateCoordinator for polling
├── const.py          # Constants and configuration keys
├── strings.json      # Translations and UI strings
├── services.yaml     # Custom service action documentation
├── icons.json        # Icon definitions
├── light.py          # Light platform entities
├── switch.py         # Switch platform entities
├── sensor.py         # Sensor platform entities
└── tests/            # Pytest test files
    ├── __init__.py
    ├── conftest.py
    └── test_*.py
```

### 3. Manifest.json Requirements

**File**: `docs/creating_integration_manifest.md:1-800`

**Required Fields**:
```json
{
  "domain": "unique_domain_name",
  "name": "Human Readable Name",
  "codeowners": ["@github_username"],
  "dependencies": [],
  "documentation": "https://www.home-assistant.io/integrations/domain",
  "integration_type": "hub",
  "iot_class": "cloud_polling",
  "requirements": []
}
```

**Integration Types**:
- `device` - Single device integration
- `hub` - Gateway to multiple devices/services (Philips Hue)
- `service` - Single service per config entry (DuckDNS)
- `helper` - Entity for automations (input_boolean)
- `entity` - Basic entity platform (rarely used)
- `hardware` - Hardware integration (rarely used)
- `system` - System integration (reserved)
- `virtual` - Points to another integration

**IoT Classes**:
- `local_polling` - Direct device, delayed updates
- `local_push` - Direct device, immediate updates
- `cloud_polling` - Cloud-based, delayed updates
- `cloud_push` - Cloud-based, immediate updates
- `assumed_state` - Cannot get state, assumes based on command
- `calculated` - Calculated result, no direct communication

**Critical Requirements**:
1. All Python requirements must be pinned: `"requirements": ["phue==0.8.1"]`
2. All API-specific code must be in external PyPI library
3. Config flow support required: `"config_flow": true`
4. Quality scale must be specified: `"quality_scale": "bronze"`

### 4. Config Entries & Config Flows

**Files**:
- `docs/config_entries_index.md:1-200`
- `docs/config_entries_config_flow_handler.md:1-900`
- `docs/data_entry_flow_index.md:1-700`

**Config Entry Lifecycle**:
```
not loaded → setup in progress → loaded
                ↓
   setup error / setup retry (auto-retry with backoff)
                ↓
   migration error → unload in progress → failed unload
```

**Config Flow Implementation**:
```python
from homeassistant import config_entries
from .const import DOMAIN

class ExampleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle user-initiated setup."""
        if user_input is not None:
            # Validate input
            await self.async_set_unique_id(device_id)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title="Device Name",
                data=user_input  # Immutable connection data
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("host"): str,
                vol.Required("api_key"): str,
            })
        )
```

**Reserved Step Names**:
- `user` - Manual user setup
- `discovery` - Automatic discovery
- `bluetooth`, `dhcp`, `zeroconf`, `ssdp`, `usb`, `mqtt`, `homekit` - Discovery protocols
- `reauth` - Re-authentication for expired credentials
- `reconfigure` - Reconfiguration of existing entry
- `import` - YAML to config entry migration

**Unique ID Requirements**:
- Must be unique within integration domain
- Acceptable sources: serial numbers, MAC addresses, account IDs, device identifiers
- NOT acceptable: IP address, hostname, device name, user-changeable values
- Last resort: Config entry ID

### 5. Core Concepts & Architecture

**Files**:
- `docs/dev_101_hass.md:1-100`
- `docs/dev_101_states.md:1-150`
- `docs/dev_101_events.md:1-100`
- `docs/dev_101_services.md:1-400`
- `docs/architecture_components.md:1-200`

**The Hass Object** - Central hub:
```
hass (HomeAssistant instance)
├── hass.config     # Configuration (location, timezone, units)
├── hass.states     # StateMachine (entity states)
├── hass.bus        # EventBus (system events)
├── hass.services   # ServiceRegistry (actions)
├── hass.loop       # asyncio event loop
└── hass.data       # Shared data storage
```

**State Management**:
- Entity ID format: `domain.object_id` (e.g., `light.kitchen`)
- State is a string representing entity value
- Attributes are JSON-serializable metadata
- Updated via: `hass.states.set()` or `entity.async_write_ha_state()`

**Event System**:
- Event-driven architecture
- Fire events: `hass.bus.fire("event_type", {"key": "value"})`
- Listen to events: `hass.bus.listen("event_type", callback)`
- State changes broadcast as events

**Services (Actions)**:
- Registered globally in `async_setup()`: `hass.services.async_register(DOMAIN, "service_name", handler)`
- Described in `services.yaml` for UI generation
- Can return response data for advanced automations
- Entity services operate on specific entities

### 6. Asyncio Patterns

**Files**:
- `docs/asyncio_101.md:1-100`
- `docs/asyncio_working_with_async.md:1-150`
- `docs/asyncio_blocking_operations.md:1-300`
- `docs/asyncio_categorizing_functions.md:1-200`

**Function Types**:

1. **Coroutine Functions** (async):
   - Prefixed with `async_`
   - Can suspend with `await`
   - Used for I/O operations
   ```python
   async def async_setup_entry(hass, entry):
       data = await api.fetch_data()
       return True
   ```

2. **Callback Functions**:
   - Decorated with `@callback`
   - Cannot do I/O or await
   - Better performance (no suspension)
   - Can schedule coroutines: `hass.async_create_task(coro)`
   ```python
   from homeassistant.core import callback

   @callback
   def handle_event(event):
       # Quick processing only
       hass.async_create_task(async_slow_work(event))
   ```

3. **Event Loop Safe Functions**:
   - Standard computations, data transforms
   - No I/O, thread-safe
   - No special annotation needed

**Blocking Operations - CRITICAL**:
- NEVER block the event loop
- Use executor for blocking calls:
  ```python
  result = await hass.async_add_executor_job(blocking_function, arg)
  ```
- Common blocking operations: file I/O, urllib, ssl loads, `time.sleep()`
- Use async alternatives: aiohttp, `asyncio.sleep()`, pathlib async methods
- Home Assistant 2024.7+ auto-detects blocking operations

### 7. Entity Development

**Files**:
- `docs/core/entity.md:1-500`
- `docs/entity_registry_index.md:1-150`
- `docs/device_registry_index.md:1-400`
- `docs/creating_platform_index.md:1-100`

**Entity Naming Standards** (Mandatory):
- Set `_attr_has_entity_name = True`
- Device name set independently
- Main feature: `_attr_name = None` → "Dishwasher"
- Other features: `_attr_name = "Power usage"` → "Dishwasher Power usage"
- NEVER include device type in name

**Generic Entity Properties**:
```python
class MyEntity(LightEntity):
    _attr_has_entity_name = True
    _attr_unique_id = "device_serial_light"
    _attr_device_class = LightDeviceClass.LIGHT
    _attr_entity_category = EntityCategory.CONFIG
    _attr_entity_registry_enabled_default = True
    _attr_should_poll = False

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name="Device Name",
            manufacturer="Brand",
            model="Model Name",
            sw_version="1.0.0",
        )
```

**Entity Lifecycle Hooks**:
```python
async def async_added_to_hass(self):
    """Called when entity added, before first state write."""
    # Subscribe to updates, restore state, set up listeners

async def async_will_remove_from_hass(self):
    """Called before entity removal."""
    # Unsubscribe, close connections, clean up
```

**Update Strategies**:
1. **Polling** (default): `should_poll = True`, implement `async_update()`
2. **Push**: `should_poll = False`, call `async_write_ha_state()` when data arrives
3. **DataUpdateCoordinator**: Recommended for coordinated polling

### 8. Data Fetching & Coordinators

**File**: `docs/integration_fetching_data.md:1-400`

**DataUpdateCoordinator Pattern** (Recommended):
```python
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
    ConfigEntryAuthFailed,
)

class MyCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, config_entry, api):
        super().__init__(
            hass,
            _LOGGER,
            name="My Sensor",
            config_entry=config_entry,
            update_interval=timedelta(seconds=30),
            always_update=False,  # Compare data with __eq__
        )
        self.api = api

    async def _async_setup(self):
        """Setup called once during first refresh."""
        self._device = await self.api.get_device()

    async def _async_update_data(self):
        """Fetch data, called periodically."""
        try:
            async with async_timeout.timeout(10):
                listening_idx = set(self.async_contexts())
                return await self.api.fetch_data(listening_idx)
        except ApiAuthError as err:
            raise ConfigEntryAuthFailed from err
        except ApiError as err:
            raise UpdateFailed(f"Error: {err}") from err
```

**Entity with Coordinator**:
```python
from homeassistant.helpers.update_coordinator import CoordinatorEntity

class MyEntity(CoordinatorEntity, LightEntity):
    def __init__(self, coordinator, idx):
        super().__init__(coordinator, context=idx)
        self.idx = idx

    @callback
    def _handle_coordinator_update(self):
        """Handle updated data from coordinator."""
        self._attr_is_on = self.coordinator.data[self.idx]["state"]
        self.async_write_ha_state()
```

**Benefits**:
- Single API poll for all entities
- Automatic error handling
- Context-aware fetching (only active entities)
- `always_update=False` avoids duplicate state writes
- `async_config_entry_first_refresh()` triggers initial fetch with retry

### 9. Error Handling & Setup Failures

**File**: `docs/integration_setup_failures.md:1-200`

**ConfigEntryNotReady** - For transient failures:
```python
async def async_setup_entry(hass, entry):
    device = MyDevice(entry.data["host"])
    try:
        await device.async_setup()
    except (asyncio.TimeoutError, TimeoutException) as ex:
        raise ConfigEntryNotReady(
            f"Timeout connecting to {device.host}"
        ) from ex
    # Continue setup...
    return True
```
- Home Assistant auto-retries with exponential backoff
- Message shown in UI
- Do NOT log yourself (framework logs it)

**ConfigEntryAuthFailed** - For authentication issues:
```python
except ApiAuthError as ex:
    raise ConfigEntryAuthFailed(
        f"Credentials expired for {device.name}"
    ) from ex
```
- Triggers reauth flow automatically
- Provides context: source="SOURCE_REAUTH", entry_id, unique_id
- Must raise from `async_setup_entry` or DataUpdateCoordinator

**PlatformNotReady** - For platform setup failures:
```python
async def async_setup_platform(hass, config, async_add_entities, discovery_info):
    if not can_connect():
        raise PlatformNotReady("Device offline")
```

### 10. Testing Requirements

**Files**:
- `docs/development_testing.md:1-350`
- `docs/creating_integration_tests_file_structure.md:1-100`

**Test Directory Structure**:
```
tests/components/<domain>/
├── __init__.py       # Required, simple docstring
├── conftest.py       # Test fixtures
├── test_init.py      # Test __init__.py functionality
├── test_config_flow.py  # Config flow tests (100% coverage required)
└── snapshots/        # Snapshot test files (.ambr)
```

**Testing Principles**:
1. Use core interfaces, NOT integration internals
2. Setup: `hass.config_entries.async_setup()` or `async_setup_component()`
3. State assertions: `hass.states.get()`
4. Service calls: `hass.services.async_call()`
5. Mock external APIs with `AsyncMock`
6. Use `MockConfigEntry` from `tests/common.py`

**Config Flow Testing** (100% Coverage Required):
```python
from tests.common import MockConfigEntry

async def test_config_flow_user(hass):
    """Test user-initiated config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}
    )
    assert result["type"] == "form"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"host": "192.168.1.1", "api_key": "test"},
    )
    assert result["type"] == "create_entry"
    assert result["title"] == "Device Name"
```

**Running Tests**:
```bash
# Run integration tests with coverage
pytest ./tests/components/<domain>/ \
  --cov=homeassistant.components.<domain> \
  --cov-report term-missing -vv

# Run pre-commit linters
pre-commit run --all-files

# Update snapshots
pytest tests/components/<domain>/ --snapshot-update
```

**Snapshot Testing**:
- Use for large outputs (entity states, diagnostics, registry entries)
- NOT a replacement for functional tests
- Snapshots stored in `snapshots/*.ambr` (human-readable)
- Must commit snapshot files to repository

### 11. Code Review & Quality Standards

**Files**:
- `docs/creating_component_code_review.md:1-300`
- `docs/creating_platform_code_review.md:1-250`
- `docs/review-process.md:1-600`
- `docs/development_guidelines.md:1-200`
- `docs/development_checklist.md:1-100`

**Component Checklist**:

0. **Common Requirements**:
   - Follow PEP8 style (enforced by Ruff)
   - Follow PEP257 docstring conventions
   - Use existing constants from `homeassistant.const`

1. **External Requirements**:
   - All requirements in `manifest.json` with pinned versions
   - All API code in external PyPI library (NOT in integration)
   - Requirements must be published on PyPI (not GitHub)

2. **Configuration**:
   - Voluptuous schema for validation
   - Default parameters in schema, not in `setup()`
   - Use generic config keys from `homeassistant.const`
   - NEVER depend on users adding to `customize`

3. **Component/Platform Communication**:
   - Share data via `hass.data[DOMAIN]`
   - Use dispatcher for update notifications

4. **Communication with Devices/Services**:
   - **CRITICAL**: All API calls via external PyPI library
   - BAD: `status = requests.get(url)`
   - GOOD: `status = bridge.get_status()`

5. **Event Names**:
   - Prefix with domain name
   - Example: `netatmo_person` not `person`

**Platform Checklist**:

1. **Setup Platform**:
   - Verify configuration works (credentials, host, etc.)
   - Group `add_entities` calls
   - Service actions format: `<domain>.<service_name>`
   - Verify permissions for service actions

2. **Entity**:
   - Extend entity from integration domain
   - Do NOT pass `hass` to constructor
   - Do NOT call `update()` in constructor (use `update_before_add=True`)
   - Do NOT do I/O in properties (cache in `update()`)
   - Use UTC timestamps, not relative time
   - Leverage lifecycle callbacks for listeners/cleanup

**Style Guidelines** (`docs/development_guidelines.md:1-200`):
- PEP8 strictly enforced
- Ruff for formatting (auto-checked in CI)
- Comments are full sentences with periods
- Imports ordered alphabetically
- Constants in alphabetical order
- Prefer f-strings (except logging uses % formatting)
- Type hints encouraged and checked in CI
- Log messages: no platform name (auto-added), no period at end
- **CRITICAL**: Do NOT log API keys, tokens, passwords

**Configuration Validation** (`docs/development_validation.md:1-150`):
```python
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

DEFAULT_NAME = "Sensor Name"
DEFAULT_PORT = 993

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
    vol.Optional(CONF_METHOD, default="GET"): vol.In(["GET", "POST"]),
})
```

**Development Checklist** (Before Committing):
1. All API code in external PyPI library
2. Run `python3 -m script.gen_requirements_all` (updates requirements_all.txt)
3. Run `python3 -m script.hassfest` (validates manifest, codeowners)
4. Update `.strict-typing` if fully type hinted
5. Run `ruff format` for code formatting
6. Run `pre-commit run --all-files` for linting
7. Run `pytest tests` for testing
8. Documentation developed for home-assistant.io

### 12. Quality Scale & Tiers

**Files**: `docs/core/integration-quality-scale/rules/*`

**Quality Tiers**:
- **Bronze** (minimum for core integrations)
- **Silver**
- **Gold**
- **Platinum**
- **Legacy** (non-UI-configurable, deprecated)

**Bronze Tier Requirements**:
- Config flow support (UI setup)
- Entity unique IDs
- `has_entity_name = True`
- Device class and entity category support
- Basic test coverage
- Type hints

**Silver Tier Requirements**:
- Above 80% test coverage
- Diagnostics implementation
- Exception translations
- Config entry state handling
- Reconfiguration flow support

**Gold Tier Requirements**:
- Above 90% test coverage
- Strict typing
- Entity translations
- Device/stale device handling
- Proper parallel updates

**Platinum Tier Requirements**:
- Above 95% test coverage
- All above requirements
- Perfect implementation
- Highest code quality

**Key Quality Rules**:
1. Config flow required (Bronze+)
2. Entity unique IDs (Bronze+)
3. has_entity_name = True (Bronze+)
4. Device class support (Bronze+)
5. Entity category (Bronze+)
6. 100% config flow test coverage (Bronze+)
7. Diagnostics (Silver+)
8. Strict typing (Gold+)
9. Entity translations (Gold+)
10. Reauthentication flow (Silver+)

### 13. Pull Request & Submission Process

**File**: `docs/review-process.md:1-600`, `docs/development_submitting.md:1-150`

**Before Creating PR**:
1. Base off `dev` branch (NOT `master`)
2. Test locally (run pytest, pre-commit)
3. Comply with all architectural decisions (ADRs)
4. Ensure latest upstream version

**Creating Perfect PR**:
1. **Small PRs** - Single feature/fix/platform
   - Limit to single platform for new integrations
   - No feature mixing or unrelated changes
   - No PRs depending on unmerged work
   - Large code dumps will be closed

2. **One thing at a time** - Focused changes only

3. **Clear title** - Capital letter, no period at end

4. **Extensive description**:
   - Motivation and use case
   - Links to relevant code/docs
   - Test plan for reviewers

5. **Dependency updates** - Separate PRs with:
   - Links to release notes/changelog
   - Git diff/compare view

**Commit Messages**:
- Meaningful messages (not "Update" or "Fix")
- Capital letter, no period
- Imperative voice: "Add feature" not "Adds feature"
- No prefixes like `[domain]` or `platform:`

**What NOT to Do**:
- Contact reviewers directly or ping them
- Ask for review in PR description
- Submit PRs you won't work on
- Open more than 5 PRs at once
- Force push to main/master

**Review Process**:
- Review comments help improve code (not personal)
- Ask questions for clarification
- PR marked draft when changes requested
- Mark ready when changes complete
- Keep PR updated with latest `dev`

### 14. Common Pitfalls to Avoid

Based on all documentation:

1. **API calls directly in code** - Use external PyPI library
2. **Logging sensitive info** - No API keys, tokens, passwords
3. **I/O in properties** - Cache in `update()` instead
4. **Calling `update()` in constructor** - Use `update_before_add=True`
5. **Depending on `customize`** - Use proper schema
6. **Passing `hass` to entity** - HA sets it automatically
7. **Mixed features in PR** - Keep focused
8. **Unmerged dependencies** - Create sequential PRs
9. **>5 PRs at once** - Follow guidelines
10. **Skipping pre-commit** - Always run linters
11. **Huge PRs** - Won't be prioritized
12. **Relative time** - Use UTC timestamps
13. **Missing unique IDs** - All entities need them
14. **No validation** - Always validate input
15. **Unneeded features** - Keep to MVP
16. **None defaults** - Use sensible defaults
17. **No tests** - Minimize regressions
18. **Sync blocking** - Use async/await
19. **Device type in name** - Use `has_entity_name = True`
20. **Blocking event loop** - Use executor for blocking calls

## Code References

**Key Documentation Files**:

### Getting Started
- `docs/creating_component_index.md` - Integration creation overview
- `docs/creating_integration_file_structure.md` - File structure requirements
- `docs/creating_integration_manifest.md` - Manifest.json specification
- `docs/creating_integration_brand.md` - Brand configuration
- `docs/development_environment.mdx` - Development setup

### Core Concepts
- `docs/dev_101_hass.md` - Hass object overview
- `docs/dev_101_states.md` - State management
- `docs/dev_101_events.md` - Event system
- `docs/dev_101_services.md` - Service actions
- `docs/architecture_index.md` - Architecture overview
- `docs/architecture_components.md` - Component architecture

### Asyncio
- `docs/asyncio_101.md` - Asyncio fundamentals
- `docs/asyncio_working_with_async.md` - Working with async
- `docs/asyncio_blocking_operations.md` - Blocking operations
- `docs/asyncio_categorizing_functions.md` - Function types
- `docs/asyncio_thread_safety.md` - Thread safety
- `docs/asyncio_imports.md` - Import best practices

### Configuration
- `docs/config_entries_index.md` - Config entry lifecycle
- `docs/config_entries_config_flow_handler.md` - Config flow implementation
- `docs/config_entries_options_flow_handler.md` - Options flow
- `docs/data_entry_flow_index.md` - Data entry flow framework
- `docs/configuration_yaml_index.md` - YAML configuration (legacy)

### Entities & Platforms
- `docs/core/entity.md` - Base entity properties
- `docs/entity_registry_index.md` - Entity registry
- `docs/entity_registry_disabled_by.md` - Entity enabling/disabling
- `docs/device_registry_index.md` - Device registry
- `docs/creating_platform_index.md` - Platform creation
- `docs/core/entity/sensor.md` - Sensor entities
- `docs/core/entity/light.md` - Light entities
- `docs/core/entity/climate.md` - Climate entities

### Data Management
- `docs/integration_fetching_data.md` - Data fetching patterns
- `docs/integration_setup_failures.md` - Error handling
- `docs/integration_listen_events.md` - Event listening

### Testing
- `docs/development_testing.md` - Testing guide
- `docs/creating_integration_tests_file_structure.md` - Test structure

### Code Review & Quality
- `docs/creating_component_code_review.md` - Component checklist
- `docs/creating_platform_code_review.md` - Platform checklist
- `docs/review-process.md` - PR review process
- `docs/development_guidelines.md` - Style guidelines
- `docs/development_checklist.md` - Pre-commit checklist
- `docs/development_validation.md` - Configuration validation
- `docs/development_typing.md` - Type hints
- `docs/development_submitting.md` - Submission process
- `docs/core/integration-quality-scale/` - Quality scale rules

### Supporting Topics
- `docs/device_automation_index.md` - Device automations
- `docs/device_automation_trigger.md` - Automation triggers
- `docs/device_automation_action.md` - Automation actions
- `docs/device_automation_condition.md` - Automation conditions
- `docs/bluetooth.md` - Bluetooth integration
- `docs/network_discovery.md` - Network discovery
- `docs/translations.md` - Translation/i18n
- `docs/internationalization/` - i18n details
- `docs/documenting.md` - Documentation standards

## Architecture Insights

1. **Event-Driven Architecture**: Home Assistant is fundamentally event-driven. State changes are events, user actions are events, and integrations communicate via events.

2. **Async-First Design**: The entire platform uses asyncio. Blocking the event loop is the #1 issue to avoid. All I/O must be async or run in executor.

3. **Registry-Based Persistence**: Entity and device registries provide persistence, enabling user customizations to survive restarts and code changes.

4. **Config Entry Pattern**: Modern integrations use config entries (UI setup) instead of YAML. This is mandatory for Bronze tier and above.

5. **Coordinator Pattern**: DataUpdateCoordinator is the standard for polling APIs. It centralizes polling, error handling, and entity updates.

6. **External Library Requirement**: All API-specific code must be in external PyPI libraries. Home Assistant code only orchestrates library objects.

7. **Quality Scale System**: The tier system (Bronze-Platinum) provides clear progression for integration quality. New integrations must meet Bronze minimum.

8. **Testing Culture**: 100% config flow test coverage is mandatory. High overall coverage (80%+ Silver, 90%+ Gold, 95%+ Platinum) is expected.

9. **Type Safety**: Type hints are encouraged and checked in CI. Strict typing modules listed in `.strict-typing` file.

10. **Small PR Philosophy**: Large PRs are discouraged. Single platform per PR for new integrations. Focus beats scope.

## Claude Code Skills - Best Practices for Skill Development

### What are Agent Skills?

Agent Skills package expertise into discoverable capabilities. Each Skill consists of a `SKILL.md` file with instructions that Claude reads when relevant, plus optional supporting files like scripts and templates.

**Key Characteristics**:
- **Model-invoked**: Claude autonomously decides when to use Skills based on the user's request and the Skill's description
- **Discoverable**: Skills are automatically found from personal (`~/.claude/skills/`), project (`.claude/skills/`), and plugin locations
- **Modular**: Each Skill addresses one focused capability
- **Composable**: Multiple Skills can work together for complex tasks

**Benefits**:
- Extend Claude's capabilities for specific workflows
- Share expertise across teams via git
- Reduce repetitive prompting
- Consistent best practices enforcement

### Skill Types & Storage

**Personal Skills** (`~/.claude/skills/`):
- Available across all projects
- Individual workflows and preferences
- Experimental Skills during development
- Personal productivity tools

**Project Skills** (`.claude/skills/`):
- Shared with team via git
- Team workflows and conventions
- Project-specific expertise
- Shared utilities and scripts
- Automatically available to team members

**Plugin Skills**:
- Bundled with Claude Code plugins
- Automatically available when plugin installed
- Distributed through marketplaces
- Recommended for team sharing

### SKILL.md File Structure

**Required Format**:
```yaml
---
name: skill-name
description: Brief description of what this Skill does and when to use it
---

# Skill Name

## Instructions
Provide clear, step-by-step guidance for Claude.

## Examples
Show concrete examples of using this Skill.
```

**Field Requirements**:
- `name`: Lowercase letters, numbers, hyphens only (max 64 chars)
- `description`: What the Skill does and when to use it (max 1024 chars)

**Optional Frontmatter Fields**:
- `allowed-tools`: List of tools Claude can use without asking permission (Claude Code only)

### Description Field - Critical for Discovery

The `description` field determines when Claude uses your Skill. **It must include both what the Skill does AND when to use it.**

**Too Vague**:
```yaml
description: Helps with documents
```

**Specific and Discoverable**:
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Best Practices**:
- Include key terms users would mention
- Specify file types, operations, and use cases
- Mention specific triggers (e.g., "when working with Excel", "for PDF processing")
- Be concrete about capabilities

### Supporting Files Organization

```
skill-name/
├── SKILL.md (required)
├── reference.md (optional documentation)
├── examples.md (optional examples)
├── scripts/
│   └── helper.py (optional utility)
└── templates/
    └── template.txt (optional template)
```

**Progressive Disclosure**: Claude reads supporting files only when needed, managing context efficiently.

**Referencing Supporting Files**:
````markdown
For advanced usage, see [reference.md](reference.md).

Run the helper script:
```bash
python scripts/helper.py input.txt
```
````

### Tool Access Restrictions with allowed-tools

Use `allowed-tools` to limit which tools Claude can use when a Skill is active:

```yaml
---
name: safe-file-reader
description: Read files without making changes. Use when you need read-only file access.
allowed-tools: Read, Grep, Glob
---
```

**When to Use**:
- Read-only Skills that shouldn't modify files
- Skills with limited scope (e.g., only data analysis)
- Security-sensitive workflows requiring restricted capabilities

**Default Behavior**: If `allowed-tools` is not specified, Claude asks for permission to use tools following the standard permission model.

### Skill Best Practices

#### 1. Keep Skills Focused

One Skill should address one capability:

**Focused** (Good):
- "PDF form filling"
- "Excel data analysis"
- "Git commit messages"

**Too Broad** (Bad):
- "Document processing" (split into separate Skills)
- "Data tools" (split by data type or operation)

#### 2. Write Clear Instructions

**Structure**:
1. Quick start - Most common use case
2. Step-by-step guidance
3. Examples with real code
4. Best practices
5. Common pitfalls to avoid

**Example Structure**:
````markdown
# Skill Name

## Quick start
[Most common 80% use case with copy-paste example]

## Instructions
1. First step with clear action
2. Second step with expected outcome
3. Third step with validation

## Examples
```python
# Concrete, runnable example
```

## Best practices
- Do this
- Don't do that
````

#### 3. Include Specific Triggers

Help Claude discover when to use Skills:

**Clear**:
```yaml
description: Analyze Excel spreadsheets, create pivot tables, and generate charts. Use when working with Excel files, spreadsheets, or analyzing tabular data in .xlsx format.
```

**Vague**:
```yaml
description: For files
```

#### 4. Document Dependencies

List required packages in the description:

```yaml
description: Extract text, fill forms, merge PDFs. Use when working with PDF files, forms, or document extraction. Requires pypdf and pdfplumber packages.
```

**Note**: Packages must be installed in the user's environment before Claude can use them. Claude will ask for permission to install dependencies if needed.

#### 5. Version Your Skills

Track changes with version history in SKILL.md content:

```markdown
## Version History
- v2.0.0 (2025-10-01): Breaking changes to API
- v1.1.0 (2025-09-15): Added new features
- v1.0.0 (2025-09-01): Initial release
```

### Testing and Debugging Skills

#### Testing a Skill

After creating a Skill, test it by asking questions that match your description:

```
Can you help me extract text from this PDF?
```

Claude autonomously decides to use your Skill if it matches the request—you don't need to explicitly invoke it.

#### Debugging Common Issues

**1. Claude doesn't use my Skill**

Check:
- Is the description specific enough with key trigger terms?
- Is the file at the correct path (`~/.claude/skills/skill-name/SKILL.md` or `.claude/skills/skill-name/SKILL.md`)?
- Is the YAML frontmatter valid (opening/closing `---`, no tabs, correct indentation)?

Run with debug mode:
```bash
claude --debug
```

**2. Skill has errors**

Check:
- Are dependencies available/installable?
- Do scripts have execute permissions? (`chmod +x scripts/*.py`)
- Are file paths using forward slashes (Unix style)? `scripts/helper.py` not `scripts\helper.py`

**3. Multiple Skills conflict**

Use distinct trigger terms in descriptions:

Instead of:
```yaml
# Skill 1
description: For data analysis

# Skill 2
description: For analyzing data
```

Use:
```yaml
# Skill 1
description: Analyze sales data in Excel files and CRM exports. Use for sales reports, pipeline analysis, and revenue tracking.

# Skill 2
description: Analyze log files and system metrics data. Use for performance monitoring, debugging, and system diagnostics.
```

### Skill Examples

#### Simple Single-File Skill

```
commit-helper/
└── SKILL.md
```

```yaml
---
name: generating-commit-messages
description: Generates clear commit messages from git diffs. Use when writing commit messages or reviewing staged changes.
---

# Generating Commit Messages

## Instructions

1. Run `git diff --staged` to see changes
2. I'll suggest a commit message with:
   - Summary under 50 characters
   - Detailed description
   - Affected components

## Best practices

- Use present tense
- Explain what and why, not how
```

#### Skill with Tool Permissions

```
code-reviewer/
└── SKILL.md
```

```yaml
---
name: code-reviewer
description: Review code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.
allowed-tools: Read, Grep, Glob
---

# Code Reviewer

## Review checklist

1. Code organization and structure
2. Error handling
3. Performance considerations
4. Security concerns
5. Test coverage

## Instructions

1. Read the target files using Read tool
2. Search for patterns using Grep
3. Find related files using Glob
4. Provide detailed feedback on code quality
```

#### Multi-File Skill

```
pdf-processing/
├── SKILL.md
├── FORMS.md
├── REFERENCE.md
└── scripts/
    ├── fill_form.py
    └── validate.py
```

**SKILL.md**:
````yaml
---
name: pdf-processing
description: Extract text, fill forms, merge PDFs. Use when working with PDF files, forms, or document extraction. Requires pypdf and pdfplumber packages.
---

# PDF Processing

## Quick start

Extract text:
```python
import pdfplumber
with pdfplumber.open("doc.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

For form filling, see [FORMS.md](FORMS.md).
For detailed API reference, see [REFERENCE.md](REFERENCE.md).

## Requirements

Packages must be installed in your environment:
```bash
pip install pypdf pdfplumber
```
````

### Sharing Skills with Your Team

**Recommended Approach**: Distribute Skills through plugins.

**Alternative - Project Repository**:
1. Create project Skill in `.claude/skills/team-skill/`
2. Commit to git:
   ```bash
   git add .claude/skills/
   git commit -m "Add team Skill for integration development"
   git push
   ```
3. Team members automatically get Skills when they pull:
   ```bash
   git pull
   claude  # Skills are now available
   ```

### Skill Lifecycle Management

**Update a Skill**:
```bash
# Edit directly
code ~/.claude/skills/my-skill/SKILL.md  # Personal
code .claude/skills/my-skill/SKILL.md     # Project

# Restart Claude Code to load changes
```

**Remove a Skill**:
```bash
# Personal
rm -rf ~/.claude/skills/my-skill

# Project
rm -rf .claude/skills/my-skill
git commit -m "Remove unused Skill"
```

**View Available Skills**:
Ask Claude directly:
```
What Skills are available?
```

or

```
List all available Skills
```

### Key Takeaways for Skill Development

1. **Model-Invoked**: Claude decides when to use Skills based on description
2. **Description is Critical**: Must include what it does AND when to use it
3. **Keep Focused**: One Skill = One capability
4. **Specific Triggers**: Include key terms users would mention
5. **Progressive Disclosure**: Supporting files loaded only when needed
6. **Tool Restrictions**: Use `allowed-tools` for read-only or limited-scope Skills
7. **Test with Real Queries**: Ask questions that should trigger your Skill
8. **Version History**: Document changes for team visibility
9. **Share via Git**: Project Skills or plugins for team distribution
10. **Debug Mode**: Use `claude --debug` to troubleshoot loading issues

## Open Questions

1. **Skill Scope**: Should the skill cover all integration types or focus on common patterns (hub, device, service)?

2. **Code Generation vs Guidance**: Should the skill generate complete code files or provide step-by-step guidance?

3. **Testing Integration**: Should the skill automatically create test files and run pytest?

4. **Quality Tier Target**: Should the skill target Bronze minimum or aim higher (Silver/Gold)?

5. **External Library Handling**: Should the skill guide users through creating PyPI libraries or assume they exist?

6. **Documentation Generation**: Should the skill help create home-assistant.io documentation?

7. **Validation Tooling**: Should the skill run hassfest, pre-commit, and pytest automatically?

8. **Discovery Support**: Should the skill help implement discovery protocols (Bluetooth, Zeroconf, etc.)?

9. **Advanced Patterns**: Should the skill cover advanced topics (device automations, diagnostics, translations)?

10. **Update Path**: Should the skill help with integration upgrades (new quality tiers, API changes)?

## Recommendations for Skill Creation

Based on this research combining Home Assistant integration development best practices with Claude Code Skills patterns, here are comprehensive recommendations:

### Skill Design Principles

1. **Model-Invoked Activation**: Write a description that includes specific triggers like "Home Assistant integration", "HA integration", "custom component", "manifest.json", "config flow"
2. **Keep Focused**: One Skill for the core integration development workflow
3. **Progressive Disclosure**: Reference supporting files for advanced topics (device automations, diagnostics, translations)
4. **Tool Access**: Consider using `allowed-tools` if appropriate (e.g., for read-only analysis phases)

### Recommended Skill Description

```yaml
description: Create Home Assistant integrations following official best practices. Use when developing Home Assistant integrations, custom components, creating manifest.json, implementing config flows, or working with Home Assistant's integration architecture. Guides through scaffolding, config entries, coordinators, entities, testing, and quality standards.
```

This description includes key triggers:
- "Home Assistant integrations"
- "custom components"
- "manifest.json"
- "config flows"
- Specific technical terms developers would use

### Skill Structure Recommendation

```
home-assistant-integration/
├── SKILL.md (main workflow and quick start)
├── MANIFEST_GUIDE.md (manifest.json detailed reference)
├── CONFIG_FLOW_GUIDE.md (config flow patterns)
├── ENTITY_GUIDE.md (entity development)
├── TESTING_GUIDE.md (testing requirements)
├── QUALITY_SCALE.md (quality tier checklist)
└── templates/
    ├── manifest.json
    ├── __init__.py
    ├── config_flow.py
    ├── coordinator.py
    └── test_config_flow.py
```

### SKILL.md Structure

````markdown
---
name: home-assistant-integration-development
description: Create Home Assistant integrations following official best practices. Use when developing Home Assistant integrations, custom components, creating manifest.json, implementing config flows, or working with Home Assistant's integration architecture. Guides through scaffolding, config entries, coordinators, entities, testing, and quality standards.
---

# Home Assistant Integration Development

## Quick Start

The fastest way to create a new integration:

```bash
python3 -m script.scaffold integration
```

This generates complete file structure with config flow, tests, and translations.

## Development Workflow

1. **Gather Requirements**
   - Integration domain (unique, lowercase, underscores)
   - Integration type (device, hub, service, helper)
   - IoT class (local_polling, local_push, cloud_polling, cloud_push)
   - External API library name (must be on PyPI)

2. **Run Scaffold Tool**
   ```bash
   python3 -m script.scaffold integration
   # Follow prompts for domain, name, type
   ```

3. **Customize manifest.json**
   - See [MANIFEST_GUIDE.md](MANIFEST_GUIDE.md) for all required fields
   - Must pin all requirement versions: `"requirements": ["library==1.0.0"]`
   - Set quality_scale: "bronze" minimum

4. **Implement Config Flow**
   - See [CONFIG_FLOW_GUIDE.md](CONFIG_FLOW_GUIDE.md) for patterns
   - 100% test coverage required
   - Must include unique_id handling
   - Implement reauth and reconfigure flows

5. **Create DataUpdateCoordinator** (if polling API)
   - Centralized polling for all entities
   - Automatic error handling
   - Context-aware fetching

6. **Implement Platform Entities**
   - See [ENTITY_GUIDE.md](ENTITY_GUIDE.md)
   - Must set `has_entity_name = True`
   - Must provide unique_id for registry
   - Must include device_info for device registry

7. **Write Comprehensive Tests**
   - See [TESTING_GUIDE.md](TESTING_GUIDE.md)
   - 100% config flow coverage mandatory
   - Test all flows: user, reauth, reconfigure
   - Use core interfaces, not integration internals

8. **Run Validation Tools**
   ```bash
   python3 -m script.hassfest        # Validate manifest
   ruff format                        # Code formatting
   pre-commit run --all-files         # All linters
   pytest tests/components/<domain>/  # Run tests
   ```

9. **Quality Scale Check**
   - See [QUALITY_SCALE.md](QUALITY_SCALE.md)
   - Bronze tier minimum for new integrations

## Critical Requirements

### Must Do
- ✅ All API code in external PyPI library
- ✅ Config flow support (UI setup, not YAML)
- ✅ All requirements pinned: `"library==1.0.0"`
- ✅ Entity unique IDs for registry
- ✅ `has_entity_name = True` for all entities
- ✅ 100% config flow test coverage
- ✅ Async-first design (never block event loop)
- ✅ DataUpdateCoordinator for polling
- ✅ Error handling: ConfigEntryNotReady, ConfigEntryAuthFailed

### Must NOT Do
- ❌ API calls directly in integration code
- ❌ Block the event loop (use async or executor)
- ❌ Log sensitive information (API keys, tokens)
- ❌ Do I/O in properties (cache in update())
- ❌ Pass `hass` to entity constructor
- ❌ Skip pre-commit hooks
- ❌ Large PRs (single platform minimum)

## Common Pitfalls

1. **Blocking Event Loop**: Use `await hass.async_add_executor_job()` for blocking calls
2. **Missing Unique IDs**: Every entity needs unique_id
3. **Vague Config Flow Tests**: Must test all paths and error cases
4. **No External Library**: All API code must be on PyPI
5. **Unpinned Requirements**: Must specify exact versions

## Examples

See templates/ directory for:
- Complete manifest.json
- __init__.py with coordinator
- config_flow.py with reauth/reconfigure
- coordinator.py with error handling
- test_config_flow.py with 100% coverage

## Best Practices

- Keep PRs small (single platform for new integrations)
- Base off `dev` branch, not `master`
- Follow PEP8 (enforced by Ruff)
- Type hints throughout
- Meaningful commit messages
- Test locally before PR

## Version History

- v1.0.0 (2025-11-20): Initial release
````

### Implementation Strategy

**Phase 1 - Core Workflow (MVP)**:
1. Scaffold tool execution
2. Manifest.json customization
3. Config flow implementation
4. Basic entity creation
5. Testing setup
6. Validation tools

**Phase 2 - Advanced Features**:
1. DataUpdateCoordinator patterns
2. Multiple platform support
3. Device automations
4. Diagnostics implementation
5. Translations support

**Phase 3 - Quality & Polish**:
1. Quality scale progression (Bronze → Silver → Gold)
2. Strict typing
3. Advanced testing patterns
4. PR submission guidance

### Supporting Documentation Strategy

**Separate Files for Deep Dives**:
- `MANIFEST_GUIDE.md` - All manifest fields, integration types, IoT classes
- `CONFIG_FLOW_GUIDE.md` - Step implementations, schemas, unique IDs, flows
- `ENTITY_GUIDE.md` - 41 entity types, naming, registries, coordinators
- `TESTING_GUIDE.md` - pytest patterns, fixtures, snapshots, coverage
- `QUALITY_SCALE.md` - Bronze/Silver/Gold/Platinum requirements checklist

**Progressive Disclosure Benefits**:
- Main SKILL.md stays focused on workflow
- Claude loads detailed guides only when needed
- Reduces context usage
- Easier to maintain and update

### Testing the Skill

Test with these queries:
- "Help me create a Home Assistant integration"
- "I need to implement a config flow for my HA integration"
- "How do I structure a Home Assistant custom component?"
- "Create a manifest.json for a new integration"
- "What are the testing requirements for Home Assistant integrations?"

The Skill should activate automatically for these queries based on the description triggers.

### Key Files Generated by Skill

**Minimum Required**:
- `manifest.json` (complete and validated)
- `__init__.py` (async_setup_entry with coordinator)
- `config_flow.py` (full flow with reauth/reconfigure)
- `strings.json` (i18n support)

**Common Optional**:
- `coordinator.py` (if polling API)
- `const.py` (domain constants)
- Platform files (`light.py`, `sensor.py`, etc.)
- `services.yaml` (if custom services)

**Testing Required**:
- `tests/__init__.py`
- `tests/conftest.py` (fixtures)
- `tests/test_config_flow.py` (100% coverage mandatory)
- `tests/test_init.py` (setup/unload tests)

### Skill Maintenance

**Version History in SKILL.md**:
```markdown
## Version History
- v1.0.0 (2025-11-20): Initial release with Bronze tier focus
- v1.1.0 (TBD): Add Silver tier guidance
- v2.0.0 (TBD): Add Gold/Platinum tier support
```

**Update Strategy**:
- Monitor Home Assistant documentation for changes
- Update when new quality scale rules added
- Sync with new integration patterns
- Track changes in scaffold tool output

### Distribution

**Recommended**: Create as project Skill in `.claude/skills/`
- Share via git repository
- Team automatically gets updates with `git pull`
- Can be converted to plugin later for wider distribution

**Alternative**: Package as Claude Code plugin for marketplace distribution

## Summary

This research provides a complete foundation for creating a Claude Code Skill that:

1. **Follows Claude Skills Best Practices**:
   - Model-invoked with clear triggers in description
   - Focused on one capability (HA integration development)
   - Progressive disclosure via supporting files
   - Clear examples and templates
   - Testable with realistic developer queries

2. **Embeds Home Assistant Best Practices**:
   - Bronze quality tier minimum
   - Config entry pattern (not YAML)
   - DataUpdateCoordinator for polling
   - Async-first architecture
   - 100% config flow test coverage
   - External PyPI library requirement
   - Complete validation toolchain

3. **Provides Complete Workflow**:
   - Scaffold → Customize → Implement → Test → Validate
   - Clear do's and don'ts
   - Common pitfalls called out
   - Templates for all required files
   - Quality progression path (Bronze → Platinum)

The Skill will be discovered automatically when developers ask about Home Assistant integration development, and guide them through the complete process following all documented best practices.
