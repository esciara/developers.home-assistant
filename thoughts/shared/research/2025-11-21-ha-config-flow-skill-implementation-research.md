---
date: 2025-11-21T22:02:17Z
researcher: Claude (emmanuelsciara)
git_commit: 1033dea7345757f94aa30f126b6c63ac32c5cb6a
branch: claude/create-increment-plan-014br6c3qFPmhiz5KBWNd9zY
repository: developers.home-assistant
topic: "Home Assistant Config Flow Implementation Patterns for Skill Creation"
tags: [research, codebase, config-flows, home-assistant, skill-creation, patterns, templates, refactoring]
status: complete
last_updated: 2025-11-21
last_updated_by: Claude
last_updated_note: "Added Section 11: Refactoring Existing Config Flows"
related_research:
  - "2025-11-20-home-assistant-integration-skill-research.md"
  - "2025-11-21-home-assistant-integration-refactoring-patterns.md"
purpose: "Support creation of ha-config-flow-knowledge skill (Increment 01)"
---

# Research: Home Assistant Config Flow Implementation Patterns for Skill Creation

**Date**: 2025-11-21T22:02:17Z
**Researcher**: Claude (emmanuelsciara)
**Git Commit**: 1033dea7345757f94aa30f126b6c63ac32c5cb6a
**Branch**: claude/create-increment-plan-014br6c3qFPmhiz5KBWNd9zY
**Repository**: developers.home-assistant

## Research Question

What are the comprehensive patterns, code examples, testing strategies, and best practices for implementing Home Assistant configuration flows? This research supports creating the `ha-config-flow-knowledge` Claude Code Skill as specified in `plans/increments/increment-01-config-flow-skill.md`.

## Executive Summary

Home Assistant configuration flows are UI-based setup systems that guide users through integration configuration. The documentation provides comprehensive patterns for both **creating new** and **refactoring existing** config flows:

1. **Flow Types**: User flows, discovery flows (zeroconf, SSDP, Bluetooth, etc.), options flows, reauthentication, and reconfiguration
2. **Schema Patterns**: Voluptuous validators, modern selectors, conditional schemas, sections, and defaults
3. **Error Handling**: Standard error types, translation patterns, recoverable vs fatal errors
4. **Authentication**: Reauth flows for expired credentials, reconfigure flows for setup changes
5. **Testing**: 100% coverage requirement with patterns for all flow types
6. **Real-World Examples**: 15+ complete patterns from official documentation
7. **Refactoring Guidance**: Anti-patterns identification, before/after migration examples, deprecation timelines, and step-by-step refactoring strategies

This research consolidates all necessary information to create a self-contained skill that eliminates the need for external documentation lookups during both new config flow development and refactoring existing flows.

## Table of Contents

1. [Config Flow Documentation Files](#1-config-flow-documentation-files)
2. [Flow Type Patterns](#2-flow-type-patterns)
3. [Schema Definition Patterns](#3-schema-definition-patterns)
4. [Error Handling Patterns](#4-error-handling-patterns)
5. [Authentication Flow Patterns](#5-authentication-flow-patterns)
6. [Testing Patterns](#6-testing-patterns)
7. [Complete Code Templates](#7-complete-code-templates)
8. [Common Scenarios and Solutions](#8-common-scenarios-and-solutions)
9. [Requirements Checklist](#9-requirements-checklist)
10. [References](#10-references)
11. [Refactoring Existing Config Flows](#11-refactoring-existing-config-flows)

---

## 1. Config Flow Documentation Files

### Core Documentation (4 files)

**Primary Config Flow Documentation:**
- `docs/config_entries_config_flow_handler.md` - Main config flow handler documentation with step methods, form handling, and entry creation
- `docs/config_entries_options_flow_handler.md` - Options flow handlers for modifying existing config entries
- `docs/config_entries_index.md` - Config entries system overview and architecture
- `docs/data_entry_flow_index.md` - Core data entry flow framework documentation

### Integration Quality Scale Rules (10 files)

**Config Flow Requirements:**
- `docs/core/integration-quality-scale/rules/config-flow.md` - Quality scale rule requiring config flow implementation (Bronze tier)
- `docs/core/integration-quality-scale/rules/config-flow-test-coverage.md` - 100% testing requirements (Bronze tier)
- `docs/core/integration-quality-scale/rules/test-before-configure.md` - Connection testing requirement (Bronze tier)
- `docs/core/integration-quality-scale/rules/reauthentication-flow.md` - Reauth flow requirements (Silver tier)
- `docs/core/integration-quality-scale/rules/reconfiguration-flow.md` - Reconfigure flow requirements (Gold tier)
- `docs/core/integration-quality-scale/rules/unique-config-entry.md` - Unique config entry identification
- `docs/core/integration-quality-scale/rules/config-entry-unloading.md` - Proper unloading requirements
- `docs/core/integration-quality-scale/rules/discovery.md` - Discovery integration with config flows (Gold tier)
- `docs/core/integration-quality-scale/rules/discovery-update-info.md` - Updating discovered device information

### Blog Posts - Evolution and Patterns (22 files)

**Recent Changes (2025):**
- `blog/2025-11-05-config-entry-oauth2-error-handling.md` - OAuth2 error handling
- `blog/2025-07-31-result-removed-from-flowresult.md` - FlowResult return value changes
- `blog/2025-03-24-config-subentry-flow-changes.md` - Config subentry flow patterns
- `blog/2025-03-01-config-flow-unique-id.md` - Unique ID handling
- `blog/2025-02-19-new-config-entry-states.md` - New config entry state management
- `blog/2025-02-16-config-subentries.md` - Config subentries feature introduction
- `blog/2025-01-15-service-info.md` - Service info usage in flows

**2024 Updates:**
- `blog/2024-11-12-options-flow.md` - Options flow pattern updates
- `blog/2024-11-04-reauth-reconfigure-entry-id.md` - Entry ID handling in reauth/reconfigure
- `blog/2024-10-21-reauth-reconfigure-helpers.md` - Helper methods for reauth and reconfigure
- `blog/2024-04-30-store-runtime-data-inside-config-entry.md` - Runtime data storage
- `blog/2024-04-25-always-reload-after-successful-reauth-flow.md` - Reload behavior after reauth
- `blog/2024-03-21-config-entry-reconfigure-step.md` - Reconfigure step introduction
- `blog/2024-02-26-single-instance-only-manifest-option.md` - Single instance config entries
- `blog/2024-02-12-async_update_entry.md` - Async update entry method
- `blog/2024-01-11-async-show-progress-changes.md` - Progress display in flows

### Supporting Documentation (8 files)

- `docs/internationalization/core.md` - Core i18n for config flow strings
- `docs/integration_setup_failures.md` - Handling setup failures
- `docs/device_registry_index.md` - Device registry integration
- `docs/development_testing.md` - General testing including config flow tests
- `docs/creating_integration_tests_file_structure.md` - Test organization

---

## 2. Flow Type Patterns

### 2.1 Basic User Flow

**Purpose**: User-initiated setup when manually adding integration
**Source**: `docs/core/integration-quality-scale/rules/config-flow.md:31-49`

```python
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
import voluptuous as vol

class MyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """My config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        errors: dict[str, str] = {}
        if user_input:
            return self.async_create_entry(
                title="MyIntegration",
                data=user_input,
            )
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_HOST): str}),
            errors=errors,
        )
```

**Key Aspects**:
- Entry point when user manually adds integration
- Returns form when `user_input` is None
- Creates entry on successful validation
- Validates user input before creating entry

### 2.2 User Flow with Connection Testing

**Purpose**: User flow with validation before creating entry
**Source**: `docs/core/integration-quality-scale/rules/test-before-configure.md:35-63`

**Required Pattern** (Bronze Tier):

```python
class MyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """My config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        errors: dict[str, str] = {}
        if user_input:
            client = MyClient(user_input[CONF_HOST])
            try:
                await client.get_data()
            except MyException:
                errors["base"] = "cannot_connect"
            except Exception:  # noqa: BLE001
                LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title="MyIntegration",
                    data=user_input,
                )
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_HOST): TextSelector()}),
            errors=errors,
        )
```

**Requirements**:
- Test connection before creating entry
- Handle specific exceptions with error codes
- Catch unexpected exceptions separately
- Return errors to form for user feedback

### 2.3 Discovery Flow - Zeroconf/mDNS

**Purpose**: Automatic discovery via mDNS/Zeroconf
**Source**: `docs/core/integration-quality-scale/rules/discovery.md:44-111`

```python
from homeassistant.components import zeroconf

class MyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """My config flow."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self.data: dict[str, Any] = {}

    async def async_step_zeroconf(
        self, discovery_info: zeroconf.ZeroconfServiceInfo
    ) -> FlowResult:
        """Handle zeroconf discovery."""
        self.data[CONF_HOST] = host = discovery_info.host

        await self.async_set_unique_id(discovery_info.properties["serialno"])
        self._abort_if_unique_id_configured(updates={CONF_HOST: host})

        client = MyClient(host)
        try:
            await client.get_data()
        except MyClientError:
            return self.async_abort(reason="cannot_connect")

        return await self.async_step_discovery_confirm()

    async def async_step_discovery_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm discovery."""
        if user_input is not None:
            return self.async_create_entry(
                title="MyIntegration",
                data={CONF_HOST: self.data[CONF_HOST]},
            )

        self._set_confirm_only()
        return self.async_show_form(step_id="discovery_confirm")
```

**Manifest Configuration**:
```json
{
  "zeroconf": ["_mydevice._tcp.local."]
}
```

**Key Aspects**:
- Sets unique ID from discovery info (serial number)
- Updates existing entry if already configured (IP changes)
- Tests connection before proceeding
- Requires user confirmation via `discovery_confirm` step

### 2.4 Reauthentication Flow

**Purpose**: Handle expired credentials/authentication failures
**Source**: `docs/core/integration-quality-scale/rules/reauthentication-flow.md:27-92`

```python
class MyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """My config flow."""

    VERSION = 1
    host: str

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> FlowResult:
        """Perform reauthentication upon an API authentication error."""
        self.host = entry_data[CONF_HOST]
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm reauthentication dialog."""
        errors: dict[str, str] = {}
        if user_input:
            client = MyClient(self.host, user_input[CONF_API_TOKEN])
            try:
                user_id = await client.check_connection()
            except MyException as exception:
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(user_id)
                self._abort_if_unique_id_mismatch(reason="wrong_account")
                return self.async_update_reload_and_abort(
                    self._get_reauth_entry(),
                    data_updates={CONF_API_TOKEN: user_input[CONF_API_TOKEN]},
                )
        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema({vol.Required(CONF_API_TOKEN): TextSelector()}),
            errors=errors,
        )
```

**Triggering Reauth from Integration**:
```python
from homeassistant.exceptions import ConfigEntryAuthFailed

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from config entry."""
    try:
        await client.authenticate()
    except InvalidAuthError as err:
        # Triggers reauth flow
        raise ConfigEntryAuthFailed("Invalid credentials") from err
```

**Key Aspects**:
- Automatically triggered by integration on auth failures
- Verifies unique ID matches to prevent account switching
- Uses `async_update_reload_and_abort()` to update and reload
- Updates existing entry, doesn't create new one

### 2.5 Reconfiguration Flow

**Purpose**: User-initiated reconfiguration of setup parameters
**Source**: `docs/core/integration-quality-scale/rules/reconfiguration-flow.md:27-88`

```python
class MyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """My config flow."""

    VERSION = 1

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle reconfiguration of the integration."""
        errors: dict[str, str] = {}
        if user_input:
            client = MyClient(user_input[CONF_HOST], user_input[CONF_API_TOKEN])
            try:
                user_id = await client.check_connection()
            except MyException as exception:
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(user_id)
                self._abort_if_unique_id_mismatch(reason="wrong_account")
                return self.async_update_reload_and_abort(
                    self._get_reconfigure_entry(),
                    data_updates=user_input,
                )
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): TextSelector(),
                    vol.Required(CONF_API_TOKEN): TextSelector(),
                }
            ),
            errors=errors,
        )
```

**Key Differences from Reauth**:
- User-initiated (not automatic)
- For non-authentication setup changes (host, port, etc.)
- Uses `_get_reconfigure_entry()` helper

### 2.6 Options Flow

**Purpose**: Updating optional configuration after setup
**Source**: `docs/config_entries_options_flow_handler.md:27-49`

```python
from homeassistant.config_entries import OptionsFlow

OPTIONS_SCHEMA = vol.Schema(
    {
        vol.Required("show_things"): bool,
    }
)

class OptionsFlowHandler(OptionsFlow):
    """Handle options flow."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                OPTIONS_SCHEMA, self.config_entry.options
            ),
        )
```

**Registration**:
```python
@staticmethod
@callback
def async_get_options_flow(
    config_entry: ConfigEntry,
) -> OptionsFlowHandler:
    """Create the options flow."""
    return OptionsFlowHandler()
```

**Key Aspects**:
- Always starts with `async_step_init`
- Access current options via `self.config_entry.options`
- Use `add_suggested_values_to_schema()` to pre-fill current values

### 2.7 Multi-Step Flow

**Purpose**: Complex setup requiring multiple steps
**Source**: `docs/data_entry_flow_index.md:376-393`

```python
class ExampleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Example multi-step config flow."""

    VERSION = 1

    async def async_step_init(self, user_input=None):
        """Handle first step."""
        errors = {}
        if user_input is not None:
            # Validate user input
            valid = await is_valid(user_input)
            if valid:
                # Store info to use in next step
                self.init_info = user_input
                # Return the form of the next step
                return await self.async_step_account()

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({vol.Required("field"): str}),
            errors=errors,
        )

    async def async_step_account(self, user_input=None):
        """Handle second step."""
        if user_input is not None:
            # Combine data from both steps
            data = {**self.init_info, **user_input}
            return self.async_create_entry(title="Title", data=data)

        return self.async_show_form(
            step_id="account",
            data_schema=vol.Schema({vol.Required("account"): str}),
        )
```

**Key Aspects**:
- Store data between steps as instance variables
- Call next step method directly with `await`
- Validate before moving to next step
- Combine data from all steps when creating entry

### 2.8 Show Progress Flow

**Purpose**: Long-running setup tasks with progress indication
**Source**: `docs/data_entry_flow_index.md:514-548`

```python
import asyncio
from homeassistant import config_entries

class TestFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Flow with progress indication."""

    VERSION = 1
    task_one: asyncio.Task | None = None
    task_two: asyncio.Task | None = None

    async def async_step_user(self, user_input=None):
        """Handle progress flow."""
        uncompleted_task: asyncio.Task[None] | None = None

        if not self.task_one:
            coro = asyncio.sleep(10)
            self.task_one = self.hass.async_create_task(coro)
        if not self.task_one.done():
            progress_action = "task_one"
            uncompleted_task = self.task_one

        if not uncompleted_task:
            if not self.task_two:
                self.async_update_progress(0.5)  # 50% done
                coro = asyncio.sleep(10)
                self.task_two = self.hass.async_create_task(coro)
            if not self.task_two.done():
                progress_action = "task_two"
                uncompleted_task = self.task_two

        if uncompleted_task:
            return self.async_show_progress(
                progress_action=progress_action,
                progress_task=uncompleted_task,
            )

        return self.async_show_progress_done(next_step_id="finish")

    async def async_step_finish(self, user_input=None):
        """Finish setup."""
        if not user_input:
            return self.async_show_form(step_id="finish")
        return self.async_create_entry(title="Some title", data={})
```

**Key Aspects**:
- Creates asyncio tasks for long operations
- Shows progress UI to user
- Step is called again when task completes
- Can update progress percentage with `async_update_progress()`

### 2.9 Reserved Step Names

**Source**: `docs/config_entries_config_flow_handler.md:66-82`

| Step name | Description |
|-----------|-------------|
| `bluetooth` | Invoked if discovered via Bluetooth |
| `dhcp` | Invoked if discovered via DHCP |
| `hassio` | Invoked if discovered via Supervisor add-on |
| `homekit` | Invoked if discovered via HomeKit |
| `mqtt` | Invoked if discovered via MQTT |
| `ssdp` | Invoked if discovered via SSDP/uPnP |
| `usb` | Invoked if discovered via USB |
| `user` | User-initiated flow or discovery fallback |
| `reconfigure` | User-initiated reconfiguration |
| `zeroconf` | Invoked if discovered via Zeroconf/mDNS |
| `reauth` | Reauthentication due to expired credentials |
| `import` | Reserved for YAML to config entry migration |

---

## 3. Schema Definition Patterns

### 3.1 Required vs Optional Fields

**Source**: `docs/data_entry_flow_index.md:129-130`, `development_validation.md:40`

```python
import voluptuous as vol

# Required fields
data_schema = vol.Schema({
    vol.Required("username"): str,
    vol.Required("password"): str,
})

# Optional fields with defaults
data_schema = vol.Schema({
    vol.Optional("field_name", default="default value"): str,
    vol.Optional(CONF_PORT, default=8080): int,
})

# Optional fields without defaults
data_schema = vol.Schema({
    vol.Optional(CONF_SOME_SETTING): TextSelector(),
})
```

### 3.2 Common Field Types and Validators

**Source**: `development_validation.md`, `docs/core/entity/siren.md:43`

```python
import homeassistant.helpers.config_validation as cv

# String fields
vol.Required(CONF_HOST): cv.string,

# Boolean fields
vol.Optional(CONF_SSL, default=True): cv.boolean,

# Integer/Number fields
vol.Required(CONF_AGE): cv.positive_int,

# Port numbers (1-65535)
vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,

# URL validation
vol.Required(CONF_URL): cv.url,

# Time period validation
vol.Required("sleep_time"): cv.time_period,

# Entity ID validation
vol.Required(CONF_ENTITY_ID): cv.entity_id,
vol.Required(CONF_ENTITIES): cv.entity_ids,

# Limited values
vol.Optional(CONF_METHOD, default="GET"): vol.In(["POST", "GET", "PUT"]),

# List validation
vol.Optional(CONF_MONITORED, default=[]): vol.All(
    cv.ensure_list, [vol.In(SENSOR_TYPES)]
),

# Multiple type acceptance
vol.Required(CONF_VALUE): vol.Any(vol.Coerce(int), cv.string),
```

### 3.3 Modern Selectors

**Source**: `docs/data_entry_flow_index.md:119-152`, `250-274`

```python
from homeassistant.helpers.selector import (
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
    EntitySelector,
    EntitySelectorConfig,
    NumberSelector,
    TemplateSelector,
)

# Text selector with types and autocomplete
data_schema = vol.Schema({
    vol.Required(CONF_USERNAME): TextSelector(
        TextSelectorConfig(type=TextSelectorType.EMAIL, autocomplete="username")
    ),
    vol.Required(CONF_PASSWORD): TextSelector(
        TextSelectorConfig(
            type=TextSelectorType.PASSWORD,
            autocomplete="current-password"
        )
    ),
    vol.Required("postal_code"): TextSelector(
        TextSelectorConfig(type=TextSelectorType.TEXT, autocomplete="postal-code")
    ),
    vol.Required("mobile_number"): TextSelector(
        TextSelectorConfig(type=TextSelectorType.TEL, autocomplete="tel")
    ),
})

# Entity selector
vol.Required(CONF_ENTITY_ID): EntitySelector(),

# Entity selector with read-only (options flow)
vol.Optional(CONF_ENTITY_ID): EntitySelector(
    EntitySelectorConfig(read_only=True)
),

# Number selector
vol.Required(CONF_SPEED): NumberSelector(
    NumberSelectorConfig(min=0, max=100)
),

# Template selector
vol.Optional(CONF_TEMPLATE): TemplateSelector(),
```

### 3.4 Default Values and Suggested Values

**Source**: `docs/data_entry_flow_index.md:281-315`

```python
# Default values (fallback if empty)
data_schema = {
    vol.Optional("field_name", default="default value"): str,
}

# Suggested values (pre-fill, can be cleared)
data_schema = {
    vol.Optional(
        "field_name",
        description={"suggested_value": "suggested value"}
    ): str,
}

# Using helper method (common in options flows)
return self.async_show_form(
    step_id="init",
    data_schema=self.add_suggested_values_to_schema(
        OPTIONS_SCHEMA, self.config_entry.options
    ),
)
```

**Note**: For `vol.In(...)` schemas without a default, the first option is selected by default.

### 3.5 Sections (Grouping Fields)

**Source**: `docs/data_entry_flow_index.md:132-141`

```python
from homeassistant.data_entry_flow import section

data_schema = {
    vol.Required("username"): str,
    vol.Required("password"): str,
    vol.Required("ssl_options"): section(
        vol.Schema({
            vol.Required("ssl", default=True): bool,
            vol.Required("verify_ssl", default=True): bool,
        }),
        {"collapsed": False},  # Whether initially collapsed
    )
}
```

**User input structure**:
```python
{
    "username": "user",
    "password": "hunter2",
    "ssl_options": {
        "ssl": True,
        "verify_ssl": False,
    },
}
```

**Icons** (defined in `icons.json`):
```json
{
  "config": {
    "step": {
      "user": {
        "sections": {
          "ssl_options": "mdi:lock"
        }
      }
    }
  }
}
```

### 3.6 Conditional Schemas

**Source**: `docs/data_entry_flow_index.md:144-149`

```python
# Build schema dynamically
data_schema = {
    vol.Required("username"): str,
    vol.Required("password"): str,
}

if self.show_advanced_options:
    data_schema[vol.Optional("allow_groups")] = selector({
        "select": {
            "options": ["all", "light", "switch"],
        }
    })

return self.async_show_form(
    step_id="init",
    data_schema=vol.Schema(data_schema)
)
```

**Conditional factors**:
- `self.show_advanced_options` flag
- Flow source (`self.source == SOURCE_REAUTH`)
- Existing config entry data
- Discovery information

---

## 4. Error Handling Patterns

### 4.1 Standard Error Types

**Source**: `docs/config_entries_config_flow_handler.md:217-233`

```python
# Standard error keys
errors = {}

# Connection errors
errors["base"] = "cannot_connect"

# Authentication errors
errors["base"] = "invalid_auth"

# Unknown/unexpected errors
errors["base"] = "unknown"

# Already configured
# (use abort instead of error)
return self.async_abort(reason="already_configured")
```

### 4.2 Exception Handling Pattern

**Source**: `docs/core/integration-quality-scale/rules/test-before-configure.md:44-57`

```python
async def async_step_user(
    self, user_input: dict[str, Any] | None = None
) -> FlowResult:
    """Handle user flow with proper error handling."""
    errors: dict[str, str] = {}

    if user_input:
        client = MyClient(user_input[CONF_HOST])
        try:
            await client.get_data()
        except MyException:
            errors["base"] = "cannot_connect"
        except Exception:  # noqa: BLE001
            LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            # Success path
            return self.async_create_entry(
                title="MyIntegration",
                data=user_input,
            )

    return self.async_show_form(
        step_id="user",
        data_schema=vol.Schema({vol.Required(CONF_HOST): TextSelector()}),
        errors=errors,
    )
```

**Key patterns**:
- Initialize `errors = {}` at start
- Use try/except with specific exception first
- Log unexpected exceptions
- Use `else` clause for success path
- Always return `async_show_form` with errors dict

### 4.3 Field-Specific Errors

```python
errors = {}

if user_input is not None:
    if not valid_host(user_input[CONF_HOST]):
        errors[CONF_HOST] = "invalid_host"  # Error on host field
    if not valid_port(user_input[CONF_PORT]):
        errors[CONF_PORT] = "invalid_port"  # Error on port field

    # Generic error not tied to a field
    if connection_failed:
        errors["base"] = "cannot_connect"
```

### 4.4 Error Translation

**Source**: `docs/internationalization/core.md:58-106`

```json
{
  "config": {
    "error": {
      "invalid_auth": "Invalid authentication credentials",
      "cannot_connect": "Unable to connect to the device",
      "unknown": "Unexpected error occurred",
      "invalid_host": "The host address is not valid",
      "invalid_port": "Port must be between 1 and 65535"
    },
    "abort": {
      "already_configured": "[%key:common::config_flow::abort::already_configured_device%]",
      "not_supported": "This device is not supported"
    }
  }
}
```

### 4.5 Recoverable vs Fatal Errors

**Recoverable** (show form with errors):
```python
# User can retry
return self.async_show_form(
    step_id="user",
    data_schema=schema,
    errors={"base": "cannot_connect"}
)
```

**Fatal** (abort flow):
```python
# Flow ends, user must start over
return self.async_abort(reason="not_supported")
```

### 4.6 Setup Exceptions

**Source**: `docs/integration_setup_failures.md:13-85`

```python
from homeassistant.exceptions import (
    ConfigEntryNotReady,
    ConfigEntryAuthFailed,
)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from config entry."""
    device = MyDevice(entry.data[CONF_HOST])

    try:
        await device.async_setup()
    except AuthFailed as ex:
        # Triggers reauth flow
        raise ConfigEntryAuthFailed(
            f"Credentials expired for {device.name}"
        ) from ex
    except (asyncio.TimeoutError, TimeoutException) as ex:
        # Triggers retry
        raise ConfigEntryNotReady(
            f"Timed out while connecting to {device.ipaddr}"
        ) from ex

    return True
```

---

## 5. Authentication Flow Patterns

### 5.1 When to Use Reauth vs Reconfigure

**Reauthentication**:
- **Trigger**: Automatic (integration raises `ConfigEntryAuthFailed`)
- **Use cases**: Expired tokens, changed passwords, revoked credentials
- **Flow**: `async_step_reauth` → `async_step_reauth_confirm`

**Reconfiguration**:
- **Trigger**: User-initiated from UI
- **Use cases**: Changed host/IP, updated port, modified non-auth settings
- **Flow**: `async_step_reconfigure`

### 5.2 Helper Methods

**Source**: `blog/2024-10-21-reauth-reconfigure-helpers.md:8-19`

```python
# Get the entry being reauthenticated or reconfigured
reauth_entry = self._get_reauth_entry()
reconfigure_entry = self._get_reconfigure_entry()

# Verify unique ID matches (prevents account switching)
await self.async_set_unique_id(user_id)
self._abort_if_unique_id_mismatch(reason="wrong_account")

# Update entry, reload integration, and abort flow
return self.async_update_reload_and_abort(
    self._get_reauth_entry(),
    data_updates={CONF_TOKEN: new_token},  # Preferred - merges with existing
    # data={...},  # Not recommended - replaces all data
    # reload_even_if_entry_is_unchanged=False,  # Optional - skip reload if no changes
)
```

### 5.3 Unique ID Verification Patterns

**Standard verification**:
```python
await self.async_set_unique_id(device_unique_id)
self._abort_if_unique_id_mismatch()
```

**With custom abort reason**:
```python
await self.async_set_unique_id(user_id)
self._abort_if_unique_id_mismatch(reason="wrong_account")
```

**Conditional verification** (shared steps):
```python
if self.source == SOURCE_REAUTH:
    self._abort_if_unique_id_mismatch()
else:
    self._abort_if_unique_id_configured()
```

### 5.4 Triggering Reauth from Integration

**From async_setup_entry**:
```python
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from config entry."""
    try:
        await device.async_setup()
    except AuthFailed as ex:
        raise ConfigEntryAuthFailed(f"Credentials expired") from ex
```

**From DataUpdateCoordinator**:
```python
async def _async_update_data(self):
    """Fetch data from API endpoint."""
    try:
        return await self.my_api.fetch_data()
    except ApiAuthError as err:
        raise ConfigEntryAuthFailed from err
```

**From entity methods**:
```python
async def async_press(self) -> None:
    """Handle button press."""
    try:
        await self.device.press_button()
    except DevicePasswordProtected as ex:
        self.entry.async_start_reauth(self.hass)
```

---

## 6. Testing Patterns

### 6.1 Coverage Requirements

**Source**: `docs/core/integration-quality-scale/rules/config-flow-test-coverage.md:18`

- **100% test coverage for config flow** (mandatory)
- Must test error recovery
- Must test uniqueness verification
- Must test all flow types (user, discovery, reauth, reconfigure, options)

### 6.2 Running Coverage Tests

```bash
# Run with coverage report
pytest tests/components/example/ \
    --cov=homeassistant.components.example \
    --cov-report=term-missing \
    -vv

# Run only config flow tests
pytest tests/components/example/test_config_flow.py -vv
```

### 6.3 Basic User Flow Test

**Source**: `docs/core/integration-quality-scale/rules/config-flow-test-coverage.md:36-59`

```python
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import SOURCE_USER
from homeassistant.data_entry_flow import FlowResultType

async def test_full_flow(
    hass: HomeAssistant,
    mock_my_client: AsyncMock,
    mock_setup_entry: AsyncMock,
) -> None:
    """Test full flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {CONF_HOST: "10.0.0.131"},
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "My integration"
    assert result["data"] == {
        CONF_HOST: "10.0.0.131",
    }
```

### 6.4 Error Handling Tests

```python
async def test_user_flow_cannot_connect(hass: HomeAssistant) -> None:
    """Test user flow with connection error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
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


async def test_user_flow_invalid_auth(hass: HomeAssistant) -> None:
    """Test user flow with invalid auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
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
```

### 6.5 Already Configured Test

```python
from tests.common import MockConfigEntry

async def test_user_flow_already_configured(hass: HomeAssistant) -> None:
    """Test user flow with already configured device."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="device123",
        data={CONF_HOST: "192.168.1.1"},
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
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

### 6.6 Reauth Flow Test

```python
async def test_reauth_flow(
    hass: HomeAssistant,
    mock_setup_entry: AsyncMock,
) -> None:
    """Test reauthentication flow."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="device123",
        data={
            CONF_HOST: "192.168.1.1",
            CONF_PASSWORD: "old_password",
        },
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": SOURCE_REAUTH,
            "entry_id": entry.entry_id,
            "unique_id": entry.unique_id,
        },
        data=entry.data,
    )

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "reauth_confirm"

    with patch(
        "custom_components.example.config_flow.MyClient.get_device_id",
        return_value="device123",
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_PASSWORD: "new_password"},
        )

    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "reauth_successful"
    assert entry.data[CONF_PASSWORD] == "new_password"
    # Verify no new entry created
    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
```

### 6.7 Common Test Fixtures

**Source**: `thoughts/shared/research/2025-11-21-home-assistant-integration-refactoring-patterns.md:1530-1567`

```python
"""Fixtures for Example tests."""
from collections.abc import Generator
from unittest.mock import AsyncMock, patch
import pytest
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

@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Mock setting up a config entry."""
    with patch(
        "homeassistant.components.example.async_setup_entry",
        return_value=True,
    ) as mock_setup:
        yield mock_setup
```

---

## 7. Complete Code Templates

### 7.1 Basic Config Flow Template

```python
"""Config flow for Example integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import TextSelector, TextSelectorConfig, TextSelectorType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ExampleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Example."""

    VERSION = 1

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
                vol.Required(CONF_HOST): TextSelector(),
                vol.Required(CONF_PASSWORD): TextSelector(
                    TextSelectorConfig(type=TextSelectorType.PASSWORD)
                ),
            }),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> OptionsFlowHandler:
        """Get options flow."""
        return OptionsFlowHandler()


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                vol.Schema({
                    vol.Optional("show_advanced"): bool,
                }),
                self.config_entry.options,
            ),
        )
```

### 7.2 Discovery Flow Template

```python
"""Config flow with discovery support."""
from __future__ import annotations

from homeassistant.components import zeroconf
from homeassistant import config_entries

class ExampleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow with discovery."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize flow."""
        self._discovered_host: str | None = None
        self._discovered_name: str | None = None

    async def async_step_zeroconf(
        self, discovery_info: zeroconf.ZeroconfServiceInfo
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

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle manual user setup."""
        # ... implementation similar to basic template
```

### 7.3 Full Reauth/Reconfigure Template

```python
"""Config flow with reauth and reconfigure support."""

class ExampleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow with reauth and reconfigure."""

    VERSION = 1

    # For reauth flow
    _reauth_host: str | None = None

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> FlowResult:
        """Perform reauth upon API authentication error."""
        self._reauth_host = entry_data[CONF_HOST]
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm reauthentication dialog."""
        errors: dict[str, str] = {}

        if user_input is not None:
            client = MyClient(self._reauth_host, user_input[CONF_PASSWORD])
            try:
                user_id = await client.check_connection()
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except InvalidAuthError:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(user_id)
                self._abort_if_unique_id_mismatch(reason="wrong_account")

                return self.async_update_reload_and_abort(
                    self._get_reauth_entry(),
                    data_updates={CONF_PASSWORD: user_input[CONF_PASSWORD]},
                )

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema({
                vol.Required(CONF_PASSWORD): TextSelector(
                    TextSelectorConfig(type=TextSelectorType.PASSWORD)
                ),
            }),
            errors=errors,
            description_placeholders={"host": self._reauth_host},
        )

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
                ): TextSelector(),
            }),
            errors=errors,
        )
```

---

## 8. Common Scenarios and Solutions

### 8.1 Handling Multiple Discovery Types

**Scenario**: Integration can be discovered via multiple methods (zeroconf, SSDP, Bluetooth)

**Solution**:
```python
class ExampleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow with multiple discovery types."""

    def __init__(self) -> None:
        """Initialize."""
        self._discovery_data: dict[str, Any] = {}

    async def async_step_zeroconf(
        self, discovery_info: zeroconf.ZeroconfServiceInfo
    ) -> FlowResult:
        """Handle zeroconf discovery."""
        self._discovery_data = {
            CONF_HOST: discovery_info.host,
            "source": "zeroconf",
        }
        return await self._async_handle_discovery()

    async def async_step_ssdp(
        self, discovery_info: ssdp.SsdpServiceInfo
    ) -> FlowResult:
        """Handle SSDP discovery."""
        self._discovery_data = {
            CONF_HOST: discovery_info.ssdp_location,
            "source": "ssdp",
        }
        return await self._async_handle_discovery()

    async def _async_handle_discovery(self) -> FlowResult:
        """Common discovery handler."""
        host = self._discovery_data[CONF_HOST]

        # Get unique ID
        try:
            client = MyClient(host)
            unique_id = await client.get_unique_id()
        except Exception:
            return self.async_abort(reason="cannot_connect")

        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured(updates={CONF_HOST: host})

        return await self.async_step_discovery_confirm()
```

### 8.2 Multi-Step with Data Validation Between Steps

**Scenario**: Validate data from step 1 before showing step 2

**Solution**:
```python
class ExampleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Multi-step flow with validation."""

    def __init__(self) -> None:
        """Initialize."""
        self._credentials: dict[str, Any] = {}
        self._available_devices: list[str] = []

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Step 1: Get credentials."""
        errors = {}

        if user_input is not None:
            # Validate credentials
            try:
                client = MyClient(user_input[CONF_API_KEY])
                # Fetch available devices for step 2
                self._available_devices = await client.get_devices()
                self._credentials = user_input
                return await self.async_step_select_device()
            except InvalidAuthError:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_API_KEY): TextSelector(),
            }),
            errors=errors,
        )

    async def async_step_select_device(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Step 2: Select device."""
        if user_input is not None:
            # Combine data from both steps
            data = {**self._credentials, **user_input}
            return self.async_create_entry(title=user_input["device"], data=data)

        return self.async_show_form(
            step_id="select_device",
            data_schema=vol.Schema({
                vol.Required("device"): vol.In(self._available_devices),
            }),
        )
```

### 8.3 Options Flow with Conditional Fields

**Scenario**: Show advanced options only when advanced mode is enabled

**Solution**:
```python
class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options with conditional fields."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        # Build schema dynamically
        schema = {
            vol.Optional("advanced_mode", default=False): bool,
        }

        # Add advanced options if enabled
        if self.config_entry.options.get("advanced_mode"):
            schema[vol.Optional("polling_interval", default=30)] = vol.All(
                vol.Coerce(int), vol.Range(min=10, max=300)
            )
            schema[vol.Optional("timeout", default=10)] = vol.All(
                vol.Coerce(int), vol.Range(min=1, max=60)
            )

        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                vol.Schema(schema),
                self.config_entry.options,
            ),
        )
```

### 8.4 Handling IP Address Changes via Discovery

**Scenario**: Device's IP address changes, discovery should update existing entry

**Solution**:
```python
async def async_step_zeroconf(
    self, discovery_info: zeroconf.ZeroconfServiceInfo
) -> FlowResult:
    """Handle zeroconf discovery."""
    host = discovery_info.host
    unique_id = discovery_info.properties["serial"]

    # Set unique ID and update host if already configured
    await self.async_set_unique_id(unique_id)
    self._abort_if_unique_id_configured(updates={CONF_HOST: host})

    # If we reach here, it's a new device
    # ... continue with discovery confirmation
```

**Key**: The `updates` parameter in `_abort_if_unique_id_configured()` automatically updates the existing entry's data.

---

## 9. Requirements Checklist

### Bronze Tier (Minimum Requirements)

- [ ] **Config flow implemented** (`config-flow` rule)
  - UI-based setup (not YAML)
  - 100% test coverage for config flow
  - Connection testing in config flow before entry creation

- [ ] **Unique IDs for config entries** (`unique-config-entry` rule)
  - Using stable identifiers (serial number, MAC, etc.)
  - Not using changeable values (IP, name, etc.)

- [ ] **Test before configure** (`test-before-configure` rule)
  - Validates connection/credentials before creating entry
  - Returns appropriate errors to user

- [ ] **Test before setup** (`test-before-setup` rule)
  - Validates setup in `async_setup_entry`
  - Raises `ConfigEntryNotReady` for temporary failures
  - Raises `ConfigEntryAuthFailed` for auth failures

### Silver Tier

- [ ] **Config entry unloading** (`config-entry-unloading` rule)
  - Implements `async_unload_entry`
  - Returns True on successful unload

- [ ] **Reauthentication flow** (`reauthentication-flow` rule)
  - Implements `async_step_reauth` and `async_step_reauth_confirm`
  - Triggers on `ConfigEntryAuthFailed` exception
  - Updates existing entry (doesn't create new)

### Gold Tier

- [ ] **Discovery support** (`discovery` rule)
  - Implements discovery step(s) (zeroconf, SSDP, etc.)
  - Manifest includes discovery matchers
  - Updates IP on rediscovery

- [ ] **Reconfiguration flow** (`reconfiguration-flow` rule)
  - Implements `async_step_reconfigure`
  - Allows updating non-optional setup parameters

### Testing Requirements

- [ ] **100% config flow test coverage** (`config-flow-test-coverage` rule)
  - User flow with success
  - User flow with errors (cannot_connect, invalid_auth, unknown)
  - Already configured check
  - Discovery flow (if applicable)
  - Reauth flow (if applicable)
  - Reconfigure flow (if applicable)
  - Options flow (if applicable)

### Translation Requirements

- [ ] **strings.json complete**
  - All step titles and descriptions
  - All field labels and descriptions
  - All error messages
  - All abort reasons

---

## 10. References

### Primary Documentation Files

**Core Config Flow:**
- `docs/config_entries_config_flow_handler.md` - Main config flow implementation guide
- `docs/data_entry_flow_index.md` - Foundation framework documentation
- `docs/config_entries_options_flow_handler.md` - Options flow patterns
- `docs/config_entries_index.md` - Overall system architecture

**Quality Scale Rules:**
- `docs/core/integration-quality-scale/rules/config-flow.md`
- `docs/core/integration-quality-scale/rules/config-flow-test-coverage.md`
- `docs/core/integration-quality-scale/rules/test-before-configure.md`
- `docs/core/integration-quality-scale/rules/reauthentication-flow.md`
- `docs/core/integration-quality-scale/rules/reconfiguration-flow.md`
- `docs/core/integration-quality-scale/rules/discovery.md`

**Testing:**
- `docs/development_testing.md`
- `docs/creating_integration_tests_file_structure.md`

**Supporting:**
- `docs/internationalization/core.md`
- `docs/integration_setup_failures.md`
- `docs/development_validation.md`

### Blog Posts (Key Pattern Updates)

- `blog/2024-10-21-reauth-reconfigure-helpers.md` - Helper methods
- `blog/2024-04-25-always-reload-after-successful-reauth-flow.md` - Reload behavior
- `blog/2024-03-21-config-entry-reconfigure-step.md` - Reconfigure introduction
- `blog/2025-11-05-config-entry-oauth2-error-handling.md` - OAuth2 error handling

### Previous Research

- `thoughts/shared/research/2025-11-20-home-assistant-integration-skill-research.md` - Integration skill research (Section 2: Configuration Flows)
- `thoughts/shared/research/2025-11-21-home-assistant-integration-refactoring-patterns.md` - Refactoring patterns (Sections 1, 7: Config Flow Refactoring, Authentication)

---

## 11. Refactoring Existing Config Flows

This section covers patterns for upgrading, migrating, and refactoring existing config flows to meet current Home Assistant standards.

### 11.1 Identifying Anti-Patterns

**How to recognize problematic config flow code:**

#### Quick Assessment Checklist

- ❌ **No connection testing** - Creates entry without validating connectivity
- ❌ **No unique ID** - Missing `async_set_unique_id()` call
- ❌ **IP as unique ID** - Using changeable values (IP, name, URL) as unique ID
- ❌ **No duplicate check** - Missing `_abort_if_unique_id_configured()` or `_async_abort_entries_match()`
- ❌ **Discovery without confirmation** - Creating entry directly in discovery step
- ❌ **No error handling** - Missing try/except blocks or only catching generic Exception
- ❌ **No reauth flow** - Missing `async_step_reauth` for auth failures
- ❌ **Direct entry mutation** - Using `entry.data = ...` instead of `async_update_entry()`
- ❌ **Manual single-instance check** - Code checking `_async_current_entries()` instead of manifest option
- ❌ **Old imports** - Using `from homeassistant.components.zeroconf` instead of `helpers.service_info`

#### Red Flags in Code

```python
# RED FLAG 1: No connection testing
async def async_step_user(self, user_input=None):
    if user_input:
        return self.async_create_entry(...)  # ❌ No validation!

# RED FLAG 2: IP address as unique ID
await self.async_set_unique_id(user_input[CONF_HOST])  # ❌ IP can change!

# RED FLAG 3: Discovery creates entry without confirmation
async def async_step_zeroconf(self, discovery_info):
    return self.async_create_entry(...)  # ❌ Must confirm with user!

# RED FLAG 4: Direct entry mutation
entry.data["new_field"] = value  # ❌ Corrupts internal state!

# RED FLAG 5: No unique ID check
await self.async_set_unique_id(device_id)
# Missing: self._abort_if_unique_id_configured()  # ❌ Allows duplicates!

# RED FLAG 6: Using hass.data instead of runtime_data
hass.data[DOMAIN][entry.entry_id] = client  # ❌ Old pattern!
```

---

### 11.2 Common Anti-Patterns and Fixes

#### Anti-Pattern 1: No Connection Testing

**❌ Problem:**
```python
async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
    """Bad: No connection testing."""
    if user_input:
        return self.async_create_entry(
            title="MyIntegration",
            data=user_input,
        )
    return self.async_show_form(step_id="user", data_schema=...)
```

**⚠️ Impact:**
- Setup fails later during `async_setup_entry`
- User doesn't know if credentials work
- Harder to debug connectivity issues

**✅ Solution:**
```python
async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
    """Good: Test connection before creating entry."""
    errors: dict[str, str] = {}

    if user_input:
        client = MyClient(user_input[CONF_HOST])
        try:
            await client.get_data()  # Test connection!
        except ConnectionError:
            errors["base"] = "cannot_connect"
        except InvalidAuthError:
            errors["base"] = "invalid_auth"
        except Exception:
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(
                title="MyIntegration",
                data=user_input,
            )

    return self.async_show_form(
        step_id="user",
        data_schema=...,
        errors=errors,
    )
```

---

#### Anti-Pattern 2: Using IP Address as Unique ID

**❌ Problem:**
```python
async def async_step_user(self, user_input=None):
    if user_input:
        await self.async_set_unique_id(user_input[CONF_HOST])  # ❌ IP can change!
        self._abort_if_unique_id_configured()
        return self.async_create_entry(...)
```

**⚠️ Impact:**
- Device with DHCP gets new IP → creates duplicate entry
- Same device appears twice in Home Assistant
- Violates unique config entry rule

**✅ Solution:**
```python
async def async_step_user(self, user_input=None):
    if user_input:
        client = MyClient(user_input[CONF_HOST])
        try:
            # Get stable identifier from device
            device_id = await client.get_serial_number()  # ✅ Stable ID
            # Or: MAC address, UUID, serial number, etc.
        except Exception:
            errors["base"] = "cannot_connect"
        else:
            await self.async_set_unique_id(device_id)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(...)
```

---

#### Anti-Pattern 3: Discovery Without User Confirmation

**❌ Problem:**
```python
async def async_step_zeroconf(self, discovery_info):
    """Bad: Creates entry immediately."""
    await self.async_set_unique_id(discovery_info.properties["serial"])
    self._abort_if_unique_id_configured()

    # ❌ BAD: Finishing flow without user confirmation!
    return self.async_create_entry(
        title="Device",
        data={CONF_HOST: discovery_info.host},
    )
```

**⚠️ Impact:**
- Violates UX guidelines
- User may not want device added automatically
- Can create unwanted entries

**✅ Solution:**
```python
async def async_step_zeroconf(self, discovery_info):
    """Good: Requires user confirmation."""
    await self.async_set_unique_id(discovery_info.properties["serial"])
    self._abort_if_unique_id_configured(updates={CONF_HOST: discovery_info.host})

    # Store discovery data
    self._discovered_host = discovery_info.host

    # ✅ GOOD: Ask user to confirm
    return await self.async_step_discovery_confirm()

async def async_step_discovery_confirm(self, user_input=None):
    """User confirms discovery."""
    if user_input is not None:
        return self.async_create_entry(
            title="Device",
            data={CONF_HOST: self._discovered_host},
        )

    self._set_confirm_only()
    return self.async_show_form(step_id="discovery_confirm")
```

---

#### Anti-Pattern 4: Missing Unique ID Check

**❌ Problem:**
```python
async def async_step_user(self, user_input=None):
    if user_input:
        device_id = await client.get_device_id()
        await self.async_set_unique_id(device_id)
        # ❌ MISSING: self._abort_if_unique_id_configured()

        # Creates duplicate entry!
        return self.async_create_entry(...)
```

**⚠️ Impact:**
- Same device can be added multiple times
- Duplicate entities
- Violates Bronze tier quality scale

**✅ Solution:**
```python
async def async_step_user(self, user_input=None):
    if user_input:
        device_id = await client.get_device_id()
        await self.async_set_unique_id(device_id)
        self._abort_if_unique_id_configured()  # ✅ Prevents duplicates!

        return self.async_create_entry(...)
```

---

#### Anti-Pattern 5: Direct Config Entry Mutation

**❌ Problem:**
```python
# In config flow or integration code
entry.data["new_field"] = value  # ❌ NEVER DO THIS!
entry.options["setting"] = new_value  # ❌ CORRUPTS STATE!
entry.title = "New Title"  # ❌ FAILS IN 2024.9+!
```

**⚠️ Impact:**
- Corrupts internal state
- Unique ID can be broken
- **Fails completely starting in 2024.9**

**✅ Solution:**
```python
# ✅ Always use async_update_entry
hass.config_entries.async_update_entry(
    entry,
    data={**entry.data, "new_field": value},
    options={**entry.options, "setting": new_value},
    title="New Title",
)
```

---

#### Anti-Pattern 6: Old Reauth Pattern

**❌ Problem:**
```python
# Entity or platform code
async def async_press(self) -> None:
    try:
        await self.device.press_button()
    except DevicePasswordProtected:
        # ❌ OLD: Manually creating flow without linking to entry
        self.hass.async_create_task(
            self.hass.config_entries.flow.async_init(
                DOMAIN,
                context={"source": SOURCE_REAUTH}
            )
        )
```

**⚠️ Impact:**
- Flow not linked to config entry
- **Fails in 2025.12**

**✅ Solution:**
```python
# ✅ NEW: Use helper method
async def async_press(self) -> None:
    try:
        await self.device.press_button()
    except DevicePasswordProtected:
        self.entry.async_start_reauth(self.hass)
```

---

#### Anti-Pattern 7: Old ServiceInfo Imports

**❌ Problem:**
```python
# ❌ OLD: Deprecated imports (removed in 2026.2)
from homeassistant.components.zeroconf import ZeroconfServiceInfo
from homeassistant.components.dhcp import DhcpServiceInfo
from homeassistant.components.ssdp import SsdpServiceInfo
from homeassistant.components.usb import UsbServiceInfo
```

**⚠️ Impact:**
- **Breaks completely in 2026.2**

**✅ Solution:**
```python
# ✅ NEW: Import from helpers
from homeassistant.helpers.service_info.zeroconf import ZeroconfServiceInfo
from homeassistant.helpers.service_info.dhcp import DhcpServiceInfo
from homeassistant.helpers.service_info.ssdp import SsdpServiceInfo
from homeassistant.helpers.service_info.usb import UsbServiceInfo
```

---

#### Anti-Pattern 8: Manual Single-Instance Check

**❌ Problem:**
```python
# config_flow.py
async def async_step_user(self, user_input=None):
    # ❌ OLD: Manual check
    if self._async_current_entries():
        return self.async_abort(reason="single_instance_allowed")

    # ... rest of flow
```

**⚠️ Impact:**
- Boilerplate code
- Must maintain manually

**✅ Solution:**
```json
// manifest.json
{
  "domain": "example",
  "name": "Example",
  "single_config_entry": true  // ✅ NEW: Automatic enforcement
}
```

Remove manual check from config flow - Home Assistant handles it automatically.

---

#### Anti-Pattern 9: Using hass.data Instead of runtime_data

**❌ Problem:**
```python
# __init__.py
async def async_setup_entry(hass, entry):
    client = MyClient(...)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = client  # ❌ OLD

async def async_unload_entry(hass, entry):
    hass.data[DOMAIN].pop(entry.entry_id)  # ❌ Manual cleanup
    if not hass.data[DOMAIN]:
        hass.data.pop(DOMAIN)
```

**⚠️ Impact:**
- No type safety
- Manual cleanup required
- Memory leaks if cleanup forgotten

**✅ Solution:**
```python
# __init__.py
from dataclasses import dataclass

type MyConfigEntry = ConfigEntry[MyData]

@dataclass
class MyData:
    client: MyClient

async def async_setup_entry(hass, entry: MyConfigEntry):
    client = MyClient(...)
    entry.runtime_data = MyData(client=client)  # ✅ NEW

async def async_unload_entry(hass, entry: MyConfigEntry):
    # ✅ Automatic cleanup - no manual pop needed!
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
```

---

#### Anti-Pattern 10: Missing Reauth Unique ID Verification

**❌ Problem:**
```python
async def async_step_reauth_confirm(self, user_input=None):
    if user_input:
        # ❌ MISSING: Verify same account
        return self.async_update_reload_and_abort(
            self._get_reauth_entry(),
            data_updates={CONF_TOKEN: user_input[CONF_TOKEN]},
        )
```

**⚠️ Impact:**
- User can switch to different account during reauth
- Breaks device/account association

**✅ Solution:**
```python
async def async_step_reauth_confirm(self, user_input=none):
    if user_input:
        client = MyClient(user_input[CONF_TOKEN])
        user_id = await client.get_user_id()

        # ✅ Verify same account
        await self.async_set_unique_id(user_id)
        self._abort_if_unique_id_mismatch(reason="wrong_account")

        return self.async_update_reload_and_abort(
            self._get_reauth_entry(),
            data_updates={CONF_TOKEN: user_input[CONF_TOKEN]},
        )
```

---

### 11.3 Migration Guides from Blog Posts (2024-2025)

#### Migration 1: OAuth2 Error Handling (2025.12)

**What Changed:** New `ImplementationUnavailableError` for OAuth2 when no internet

**Migration:**
```python
# Before: No special handling
implementation = await async_get_config_entry_implementation(hass, entry)

# After: Handle implementation unavailable
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.config_entry_oauth2_flow import ImplementationUnavailableError

try:
    implementation = await async_get_config_entry_implementation(hass, entry)
except ImplementationUnavailableError as err:
    raise ConfigEntryNotReady("OAuth2 implementation temporarily unavailable") from err
```

**Deadline:** Required for 2025.12+

---

#### Migration 2: ServiceInfo Imports (Deadline: 2026.2)

**What Changed:** ServiceInfo models moved from components to helpers

**Migration:**
```python
# Before: Old imports
from homeassistant.components.zeroconf import ZeroconfServiceInfo
from homeassistant.components.dhcp import DhcpServiceInfo
from homeassistant.components.ssdp import SsdpServiceInfo
from homeassistant.components.usb import UsbServiceInfo

# After: New imports
from homeassistant.helpers.service_info.zeroconf import ZeroconfServiceInfo
from homeassistant.helpers.service_info.dhcp import DhcpServiceInfo
from homeassistant.helpers.service_info.ssdp import SsdpServiceInfo
from homeassistant.helpers.service_info.usb import UsbServiceInfo
```

**Deadline:** Must migrate before 2026.2

---

#### Migration 3: Options Flow self.config_entry (Deadline: 2025.12)

**What Changed:** `OptionsFlow` now provides `self.config_entry` automatically

**Migration:**
```python
# Before: Manual initialization
@staticmethod
@callback
def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlowHandler:
    return OptionsFlowHandler(config_entry)  # ❌ Old

class OptionsFlowHandler(OptionsFlow):
    def __init__(self, config_entry: ConfigEntry) -> None:
        self.config_entry = config_entry  # ❌ Manual setting

# After: Use built-in property
@staticmethod
@callback
def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlowHandler:
    return OptionsFlowHandler()  # ✅ New

class OptionsFlowHandler(OptionsFlow):
    def __init__(self) -> None:
        pass  # ✅ self.config_entry available automatically
```

**Deadline:** Manual setting fails in 2025.12+

---

#### Migration 4: Reauth/Reconfigure Entry Linking (Deadline: 2025.12)

**What Changed:** Reauth flows must be linked to config entry

**Migration:**
```python
# Before: Manual flow creation
self.hass.async_create_task(
    hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_REAUTH}
    )
)

# After: Use helper method
self.entry.async_start_reauth(self.hass)

# Alternative: Raise exception
raise ConfigEntryAuthFailed("Invalid credentials")
```

**Deadline:** Old method fails in 2025.12

---

#### Migration 5: Config Entry Updates (Mandatory since 2024.9)

**What Changed:** Must use `async_update_entry` to modify ConfigEntry

**Migration:**
```python
# Before: Direct attribute setting (FAILS in 2024.9+)
entry.data = new_data  # ❌
entry.title = "New Title"  # ❌
entry.unique_id = new_id  # ❌ Fails immediately

# After: Use async_update_entry
hass.config_entries.async_update_entry(
    entry,
    data=new_data,
    title="New Title",
    unique_id=new_id,
)
```

**Deadline:** **Already mandatory** (2024.9+)

---

#### Migration 6: async_show_progress Requires progress_task (Mandatory since 2024.8)

**What Changed:** `progress_task` argument is now required

**Migration:**
```python
# Before: No progress_task (FAILS in 2024.8+)
return self.async_show_progress(
    step_id="progress",
    progress_action="connecting"
)

# After: Must provide progress_task
return self.async_show_progress(
    step_id="progress",
    progress_action="connecting",
    progress_task=self._connection_task,  # ✅ Required
)
```

**Deadline:** **Already mandatory** (2024.8+)

---

#### Migration 7: Runtime Data Storage (Best Practice)

**What Changed:** Prefer `entry.runtime_data` over `hass.data`

**Migration:**
```python
# Before: Using hass.data
hass.data.setdefault(DOMAIN, {})
hass.data[DOMAIN][entry.entry_id] = client

# After: Using runtime_data with typing
from dataclasses import dataclass

type MyConfigEntry = ConfigEntry[MyData]

@dataclass
class MyData:
    client: MyClient

async def async_setup_entry(hass, entry: MyConfigEntry):
    entry.runtime_data = MyData(client=MyClient(...))

# Access in platforms
async def async_setup_entry(hass, entry: MyConfigEntry, async_add_entities):
    client = entry.runtime_data.client  # Type-safe!
```

**Deadline:** Not mandatory, but best practice

---

#### Migration 8: Single Config Entry Manifest (Best Practice since 2024.3)

**What Changed:** Use manifest option instead of code

**Migration:**
```python
# Before: Manual check in config flow
async def async_step_user(self, user_input=None):
    if self._async_current_entries():
        return self.async_abort(reason="single_instance_allowed")
    # ...

# After: Remove code, add to manifest
# manifest.json:
{
  "single_config_entry": true
}
```

**Deadline:** Not mandatory, but cleaner

---

#### Migration 9: Config Entry State Management (2025.3.0+)

**What Changed:** New states and helper methods for entry lifecycle

**Migration:**
```python
# Before: Manual loaded entry tracking
async def async_unload_entry(hass, entry):
    loaded_entries = [
        e for e in hass.config_entries.async_entries(DOMAIN)
        if e.state is ConfigEntryState.LOADED
    ]
    if len(loaded_entries) == 1:
        # Last entry being unloaded

# After: Use helper (requires HA 2025.3.0+)
async def async_unload_entry(hass, entry):
    if not hass.config_entries.async_loaded_entries(DOMAIN):
        # Last entry being unloaded

# Backwards compatible:
async def async_unload_entry(hass, entry):
    other_loaded = [
        e for e in hass.config_entries.async_loaded_entries(DOMAIN)
        if e.entry_id != entry.entry_id
    ]
    if not other_loaded:
        # Last entry being unloaded
```

**Deadline:** Optional, available in 2025.3.0+

---

### 11.4 Incremental Refactoring Strategies

**Strategy 1: Priority-Based Approach**

**Step 1: Fix Breaking Issues First**
1. Fix mandatory migrations (deadline passed or approaching)
2. Update imports (ServiceInfo deadline 2026.2)
3. Fix direct entry mutations (fails since 2024.9)
4. Fix progress_task (fails since 2024.8)

**Step 2: Add Missing Bronze Tier Requirements**
1. Add connection testing to config flow
2. Add unique ID handling
3. Add duplicate entry checks
4. Achieve 100% test coverage

**Step 3: Add Silver Tier Features**
1. Implement reauth flow
2. Implement proper unload

**Step 4: Add Gold Tier Features**
1. Add discovery support
2. Add reconfigure flow

**Step 5: Modernize Patterns**
1. Migrate to runtime_data
2. Use modern selectors
3. Add manifest options (single_config_entry)

---

**Strategy 2: Test-Driven Refactoring**

1. **Add tests for current behavior** (even if wrong)
   - Ensures refactoring doesn't break existing functionality

2. **Add tests for desired behavior**
   - Test connection validation
   - Test unique ID handling
   - Test error scenarios

3. **Refactor incrementally**
   - Make one change at a time
   - Run tests after each change
   - Commit when tests pass

4. **Remove old behavior tests**
   - Keep only tests for correct patterns

---

**Strategy 3: Step-by-Step Migration**

**Example: Adding Connection Testing**

```python
# Step 1: Current (no testing)
async def async_step_user(self, user_input=None):
    if user_input:
        return self.async_create_entry(title="Device", data=user_input)
    return self.async_show_form(step_id="user", data_schema=...)

# Step 2: Add error dict and structure
async def async_step_user(self, user_input=None):
    errors = {}  # Added
    if user_input:
        return self.async_create_entry(title="Device", data=user_input)
    return self.async_show_form(step_id="user", data_schema=..., errors=errors)

# Step 3: Add try/except (still no actual test)
async def async_step_user(self, user_input=None):
    errors = {}
    if user_input:
        try:
            pass  # Will add test here
        except Exception:
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title="Device", data=user_input)
    return self.async_show_form(step_id="user", data_schema=..., errors=errors)

# Step 4: Add actual connection test
async def async_step_user(self, user_input=None):
    errors = {}
    if user_input:
        client = MyClient(user_input[CONF_HOST])  # Added
        try:
            await client.get_data()  # Added - actual test!
        except ConnectionError:  # Added specific exception
            errors["base"] = "cannot_connect"
        except Exception:
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title="Device", data=user_input)
    return self.async_show_form(step_id="user", data_schema=..., errors=errors)

# Step 5: Add unique ID handling
async def async_step_user(self, user_input=None):
    errors = {}
    if user_input:
        client = MyClient(user_input[CONF_HOST])
        try:
            device_id = await client.get_device_id()  # Get unique ID
        except ConnectionError:
            errors["base"] = "cannot_connect"
        except Exception:
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            await self.async_set_unique_id(device_id)  # Set unique ID
            self._abort_if_unique_id_configured()  # Check duplicates
            return self.async_create_entry(title="Device", data=user_input)
    return self.async_show_form(step_id="user", data_schema=..., errors=errors)
```

---

### 11.5 Common Refactoring Scenarios

#### Scenario 1: Adding Discovery to Existing Manual-Only Flow

**Before: Manual only**
```python
class MyConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        # Manual setup only
        if user_input:
            return self.async_create_entry(title="Device", data=user_input)
        return self.async_show_form(step_id="user", data_schema=USER_SCHEMA)
```

**After: Adding zeroconf discovery**
```python
class MyConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self) -> None:
        """Initialize."""
        self._discovered_host: str | None = None

    async def async_step_zeroconf(
        self, discovery_info: ZeroconfServiceInfo
    ) -> FlowResult:
        """Handle zeroconf discovery."""
        # Get unique ID from discovery
        await self.async_set_unique_id(discovery_info.properties["serial"])
        self._abort_if_unique_id_configured(updates={CONF_HOST: discovery_info.host})

        # Test connection
        try:
            client = MyClient(discovery_info.host)
            await client.test_connection()
        except Exception:
            return self.async_abort(reason="cannot_connect")

        self._discovered_host = discovery_info.host
        return await self.async_step_discovery_confirm()

    async def async_step_discovery_confirm(self, user_input=None):
        """Confirm discovery."""
        if user_input is not None:
            return self.async_create_entry(
                title="Discovered Device",
                data={CONF_HOST: self._discovered_host},
            )

        self._set_confirm_only()
        return self.async_show_form(step_id="discovery_confirm")

    async def async_step_user(self, user_input=None):
        # Keep existing manual setup
        if user_input:
            return self.async_create_entry(title="Device", data=user_input)
        return self.async_show_form(step_id="user", data_schema=USER_SCHEMA)
```

**Also update manifest.json:**
```json
{
  "zeroconf": ["_mydevice._tcp.local."]
}
```

---

#### Scenario 2: Adding Reauth Flow to Existing Config Flow

**Before: No reauth support**
```python
class MyConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input:
            return self.async_create_entry(title="Device", data=user_input)
        return self.async_show_form(step_id="user", data_schema=USER_SCHEMA)
```

**After: With reauth support**
```python
class MyConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1
    _reauth_entry: ConfigEntry | None = None

    async def async_step_reauth(self, entry_data: Mapping[str, Any]) -> FlowResult:
        """Handle reauthentication."""
        self._reauth_entry = self._get_reauth_entry()
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input=None):
        """Confirm reauthentication."""
        errors = {}

        if user_input:
            client = MyClient(
                self._reauth_entry.data[CONF_HOST],
                user_input[CONF_PASSWORD]
            )
            try:
                device_id = await client.get_device_id()
            except InvalidAuthError:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Verify same device
                await self.async_set_unique_id(device_id)
                self._abort_if_unique_id_mismatch(reason="wrong_account")

                return self.async_update_reload_and_abort(
                    self._reauth_entry,
                    data_updates={CONF_PASSWORD: user_input[CONF_PASSWORD]},
                )

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema({
                vol.Required(CONF_PASSWORD): TextSelector(
                    TextSelectorConfig(type=TextSelectorType.PASSWORD)
                )
            }),
            errors=errors,
        )

    async def async_step_user(self, user_input=None):
        # Existing user flow
        if user_input:
            return self.async_create_entry(title="Device", data=user_input)
        return self.async_show_form(step_id="user", data_schema=USER_SCHEMA)
```

**Trigger reauth from __init__.py:**
```python
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from config entry."""
    client = MyClient(entry.data[CONF_HOST], entry.data[CONF_PASSWORD])

    try:
        await client.authenticate()
    except InvalidAuthError as err:
        raise ConfigEntryAuthFailed("Invalid credentials") from err

    # ... rest of setup
```

---

#### Scenario 3: Splitting Single-Step Flow into Multi-Step

**Before: Single step with many fields**
```python
async def async_step_user(self, user_input=None):
    if user_input:
        # Too many fields at once, complex validation
        return self.async_create_entry(title="Device", data=user_input)

    return self.async_show_form(
        step_id="user",
        data_schema=vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_PORT): int,
            vol.Required(CONF_USERNAME): str,
            vol.Required(CONF_PASSWORD): str,
            vol.Required("device_type"): vol.In(["type1", "type2"]),
            vol.Optional("advanced_option"): bool,
        })
    )
```

**After: Multi-step for better UX**
```python
def __init__(self) -> None:
    """Initialize."""
    self._connection_info: dict[str, Any] = {}
    self._device_type: str | None = None

async def async_step_user(self, user_input=None):
    """Step 1: Connection info."""
    errors = {}

    if user_input:
        # Validate connection
        try:
            client = MyClient(user_input[CONF_HOST], user_input[CONF_PORT])
            await client.test_connection()
        except ConnectionError:
            errors["base"] = "cannot_connect"
        else:
            self._connection_info = user_input
            return await self.async_step_credentials()

    return self.async_show_form(
        step_id="user",
        data_schema=vol.Schema({
            vol.Required(CONF_HOST): TextSelector(),
            vol.Required(CONF_PORT, default=80): int,
        }),
        errors=errors,
    )

async def async_step_credentials(self, user_input=None):
    """Step 2: Credentials."""
    errors = {}

    if user_input:
        # Test auth
        client = MyClient(**self._connection_info)
        try:
            await client.authenticate(
                user_input[CONF_USERNAME],
                user_input[CONF_PASSWORD]
            )
        except InvalidAuthError:
            errors["base"] = "invalid_auth"
        else:
            self._connection_info.update(user_input)
            return await self.async_step_device_type()

    return self.async_show_form(
        step_id="credentials",
        data_schema=vol.Schema({
            vol.Required(CONF_USERNAME): TextSelector(),
            vol.Required(CONF_PASSWORD): TextSelector(
                TextSelectorConfig(type=TextSelectorType.PASSWORD)
            ),
        }),
        errors=errors,
    )

async def async_step_device_type(self, user_input=None):
    """Step 3: Device type."""
    if user_input:
        # Combine all data
        data = {**self._connection_info, **user_input}
        return self.async_create_entry(title="Device", data=data)

    return self.async_show_form(
        step_id="device_type",
        data_schema=vol.Schema({
            vol.Required("device_type"): vol.In(["type1", "type2"]),
            vol.Optional("advanced_option", default=False): bool,
        }),
    )
```

---

#### Scenario 4: Updating Old Validators to Modern Selectors

**Before: Old voluptuous validators**
```python
data_schema = vol.Schema({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Optional(CONF_PORT, default=80): cv.port,
})
```

**After: Modern selectors**
```python
from homeassistant.helpers.selector import (
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
    NumberSelector,
    NumberSelectorConfig,
)

data_schema = vol.Schema({
    vol.Required(CONF_HOST): TextSelector(),
    vol.Required(CONF_PASSWORD): TextSelector(
        TextSelectorConfig(
            type=TextSelectorType.PASSWORD,
            autocomplete="current-password"
        )
    ),
    vol.Optional(CONF_PORT, default=80): NumberSelector(
        NumberSelectorConfig(min=1, max=65535, mode="box")
    ),
})
```

**Benefits:**
- Better UI in frontend
- Autocomplete support
- Mobile keyboard optimization
- Validation in frontend

---

### 11.6 Refactoring Checklist

#### Pre-Refactoring Assessment

- [ ] Read current code thoroughly
- [ ] Document current behavior
- [ ] Identify all anti-patterns
- [ ] Check for deprecated imports/methods
- [ ] Review test coverage (if any)
- [ ] Note current quality scale tier
- [ ] List target improvements

#### Refactoring Execution

**Phase 1: Fix Breaking Issues** (Mandatory)
- [ ] Update ServiceInfo imports (deadline 2026.2)
- [ ] Fix direct entry mutations (fails since 2024.9)
- [ ] Fix async_show_progress (fails since 2024.8)
- [ ] Update reauth trigger method (fails in 2025.12)
- [ ] Update options flow initialization (fails in 2025.12)

**Phase 2: Bronze Tier Requirements**
- [ ] Add connection testing in config flow
- [ ] Add unique ID handling
- [ ] Add duplicate entry check
- [ ] Add error handling with specific exceptions
- [ ] Achieve 100% test coverage for config flow
- [ ] Update tests to cover uniqueness check
- [ ] Update tests to cover error recovery

**Phase 3: Code Modernization**
- [ ] Migrate to runtime_data (from hass.data)
- [ ] Update to modern selectors
- [ ] Add manifest options (single_config_entry if applicable)
- [ ] Use helper methods (_get_reauth_entry, etc.)
- [ ] Update schema with sections (if beneficial)

**Phase 4: Silver Tier Features**
- [ ] Implement reauth flow
- [ ] Implement proper unload
- [ ] Test reauth flow
- [ ] Test unload behavior

**Phase 5: Gold Tier Features** (if applicable)
- [ ] Add discovery support
- [ ] Implement reconfigure flow
- [ ] Test discovery scenarios
- [ ] Test reconfigure flow

#### Post-Refactoring Validation

- [ ] All tests pass
- [ ] 100% config flow test coverage verified
- [ ] Manual testing completed
- [ ] Error scenarios tested
- [ ] Documentation updated (strings.json)
- [ ] Quality scale tier improved
- [ ] No regressions in functionality
- [ ] Commit with clear message

---

### 11.7 Deprecation and Breaking Changes Timeline

| Deadline | Change | Severity | Migration Required |
|----------|--------|----------|-------------------|
| **2024.8** | `async_show_progress` requires `progress_task` | Breaking | Add progress_task parameter |
| **2024.9** | Direct ConfigEntry mutation fails | Breaking | Use async_update_entry |
| **2025.12** | Reauth without entry link fails | Breaking | Use entry.async_start_reauth() |
| **2025.12** | Manual OptionsFlow.config_entry setting fails | Breaking | Remove __init__ parameter |
| **2025.12** | OAuth2 needs ImplementationUnavailableError handling | Breaking | Catch and handle exception |
| **2026.2** | Old ServiceInfo imports removed | Breaking | Update import paths |
| TBD | Creating entry with duplicate unique_id fails | Breaking (warning now) | Add _abort_if_unique_id_configured |

**Best Practice Migrations (No Deadline):**
- Runtime data over hass.data
- Manifest single_config_entry over code checks
- Helper methods over manual entry access
- Modern selectors over old validators
- Config entry state helpers (2025.3.0+)

---

## Conclusions

This research provides comprehensive, self-contained information for implementing Home Assistant configuration flows. All patterns, examples, error handling strategies, testing requirements, and best practices are documented with concrete code examples extracted from official Home Assistant documentation.

### Key Findings

1. **Comprehensive Pattern Coverage**: 15+ complete flow patterns covering all major scenarios
2. **Testing Requirements**: 100% coverage is mandatory with specific patterns for all flow types
3. **Error Handling**: Standardized approach with specific error types and translation patterns
4. **Authentication Flows**: Clear separation between reauth (automatic) and reconfigure (manual)
5. **Refactoring Coverage**: Complete anti-pattern identification, migration guides for 16 blog post changes (2024-2025), and incremental refactoring strategies
6. **Self-Contained**: All information needed for both new implementation and refactoring is present in this document

### Skill Creation Readiness

This research fully supports creating the `ha-config-flow-knowledge` skill with:
- Complete code templates ready for copy-paste
- Decision trees for choosing flow types
- Error handling patterns with translation examples
- Testing patterns with fixtures and assertions
- Real-world examples from official documentation
- Comprehensive requirements checklist
- **NEW: Anti-pattern identification checklist**
- **NEW: 10 common before/after refactoring examples**
- **NEW: Migration guides for 16 breaking/deprecated changes (2024-2025)**
- **NEW: Deprecation timeline through 2026**
- **NEW: Step-by-step refactoring strategies**
- **NEW: 4 complete refactoring scenarios**

The skill can be created without requiring users to reference external documentation during both new config flow development and refactoring existing flows.
