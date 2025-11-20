---
date: 2025-11-20T21:17:50+00:00
researcher: Claude
git_commit: cfe3dab398c272ae5271f086dc05ab2d7488bdcf
branch: claude/home-assistant-integration-skill-01T9LctSUCa3AjQpfkMro4yC
repository: developers.home-assistant
topic: "Home Assistant Integration Development - Documentation for Claude Code Skill Creation"
tags: [research, codebase, home-assistant, integration-development, best-practices, testing, quality-scale]
status: complete
last_updated: 2025-11-20
last_updated_by: Claude
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

Home Assistant provides comprehensive developer documentation covering the entire integration development lifecycle. The documentation is organized into several key areas:

1. **Getting Started & Scaffolding**: Quick-start tools and file structure requirements
2. **Core Concepts**: Architecture, asyncio patterns, events, services, states
3. **Configuration System**: Config entries, config flows, data entry flows
4. **Entity Development**: 41+ entity types, platforms, registries, naming conventions
5. **Data Management**: Coordinators, polling vs push, error handling
6. **Testing**: pytest framework, snapshot testing, 100% config flow coverage requirement
7. **Code Review & Quality**: Style guides, validation, quality scale tiers (Bronze-Platinum)
8. **Best Practices**: Development guidelines, common pitfalls, submission standards

The documentation is well-structured and provides both conceptual understanding and practical implementation patterns.

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

Based on this research, a Claude Code skill for Home Assistant integration development should:

1. **Start with Scaffold**: Leverage the existing `script.scaffold` tool as foundation
2. **Focus on Config Entries**: All new integrations use config entries, not YAML
3. **Coordinator Pattern**: Default to DataUpdateCoordinator for polling APIs
4. **Bronze Tier Minimum**: Target Bronze quality scale as baseline
5. **Testing First**: Generate test files alongside implementation files
6. **External Library Check**: Verify/remind about PyPI library requirement
7. **Validation Loop**: Run hassfest and pre-commit before completion
8. **Incremental Approach**: Start with simple integration types (service, device) before complex (hub)
9. **Best Practices Enforcement**: Embed common pitfalls as validation checks
10. **Documentation Integration**: Generate strings.json and services.yaml alongside code

**Suggested Skill Workflow**:
1. Gather requirements (domain, type, IoT class, API library)
2. Run scaffold tool
3. Customize manifest.json
4. Implement config flow with validation
5. Create coordinator (if polling)
6. Implement platform entities
7. Generate service definitions
8. Create comprehensive tests
9. Run validation tools (hassfest, pre-commit, pytest)
10. Generate documentation templates

**Key Files to Generate**:
- `manifest.json` (complete and validated)
- `__init__.py` (async_setup_entry with coordinator)
- `config_flow.py` (full flow with reauth/reconfigure)
- `coordinator.py` (if polling API)
- `const.py` (domain constants)
- Platform files (`light.py`, `sensor.py`, etc.)
- `strings.json` (i18n support)
- `services.yaml` (if custom services)
- `tests/conftest.py` (fixtures)
- `tests/test_config_flow.py` (100% coverage)
- `tests/test_init.py` (setup/unload tests)

This research provides a comprehensive foundation for creating a Claude Code skill that guides developers through creating high-quality Home Assistant integrations following all documented best practices.
