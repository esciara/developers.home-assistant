---
date: 2025-11-21T23:30:00Z
researcher: Claude (emmanuelsciara)
git_commit: e6af12d4131098bc5d35dcca1ffb754a2782c4d3
branch: claude/review-config-flow-research-01P8pdcfWdXLLnbDeQWegejg
repository: developers.home-assistant
topic: "Config Flow Refactoring Quick Reference"
tags: [research, refactoring, config-flows, migration, anti-patterns, best-practices]
status: complete
last_updated: 2025-11-21
last_updated_by: Claude
related_research:
  - "2025-11-21-ha-config-flow-skill-implementation-research.md"
  - "2025-11-21-home-assistant-integration-refactoring-patterns.md"
purpose: "Quick reference for refactoring existing config flows - companion to main implementation research"
---

# Config Flow Refactoring Quick Reference

**Date**: 2025-11-21T23:30:00Z
**Researcher**: Claude (emmanuelsciara)
**Git Commit**: e6af12d4131098bc5d35dcca1ffb754a2782c4d3
**Branch**: claude/review-config-flow-research-01P8pdcfWdXLLnbDeQWegejg
**Repository**: developers.home-assistant

## Purpose

Quick reference guide for identifying and fixing anti-patterns in existing Home Assistant config flows. Use this for rapid assessment and migration planning.

---

## Quick Assessment Checklist

Run through this checklist to identify issues in existing config flows:

- [ ] ❌ **No connection testing** - Creates entry without validating connectivity
- [ ] ❌ **No unique ID** - Missing `async_set_unique_id()` call
- [ ] ❌ **IP as unique ID** - Using changeable values (IP, name, URL) as unique ID
- [ ] ❌ **No duplicate check** - Missing `_abort_if_unique_id_configured()`
- [ ] ❌ **Discovery without confirmation** - Creating entry directly in discovery step
- [ ] ❌ **No error handling** - Missing try/except blocks
- [ ] ❌ **No reauth flow** - Missing `async_step_reauth`
- [ ] ❌ **Direct entry mutation** - Using `entry.data = ...` instead of `async_update_entry()`
- [ ] ❌ **Manual single-instance check** - Code checking `_async_current_entries()`
- [ ] ❌ **Old imports** - Using `from homeassistant.components.zeroconf`

---

## Critical Deadlines (Breaking Changes)

| Deadline | Issue | Fix |
|----------|-------|-----|
| **NOW (2024.8)** | `async_show_progress` missing `progress_task` | Add `progress_task` parameter |
| **NOW (2024.9)** | Direct `entry.data` mutation | Use `hass.config_entries.async_update_entry()` |
| **2025.12** | Reauth without entry link | Use `entry.async_start_reauth(hass)` |
| **2025.12** | Manual `OptionsFlow.config_entry` setting | Remove `__init__` parameter |
| **2025.12** | OAuth2 no error handling | Catch `ImplementationUnavailableError` |
| **2026.2** | Old ServiceInfo imports | Update to `homeassistant.helpers.service_info.*` |

---

## Top 10 Fixes (Priority Order)

### 1. Fix Direct Entry Mutation (FAILS NOW)

```python
# ❌ BROKEN (fails since 2024.9)
entry.data["field"] = value

# ✅ FIX
hass.config_entries.async_update_entry(
    entry,
    data={**entry.data, "field": value}
)
```

### 2. Fix async_show_progress (FAILS NOW)

```python
# ❌ BROKEN (fails since 2024.8)
return self.async_show_progress(
    step_id="progress",
    progress_action="connecting"
)

# ✅ FIX
return self.async_show_progress(
    step_id="progress",
    progress_action="connecting",
    progress_task=self._task  # Required!
)
```

### 3. Update ServiceInfo Imports (Deadline: 2026.2)

```python
# ❌ OLD (removed in 2026.2)
from homeassistant.components.zeroconf import ZeroconfServiceInfo

# ✅ NEW
from homeassistant.helpers.service_info.zeroconf import ZeroconfServiceInfo
```

### 4. Fix Reauth Trigger (Deadline: 2025.12)

```python
# ❌ OLD (fails in 2025.12)
self.hass.async_create_task(
    hass.config_entries.flow.async_init(DOMAIN, context={"source": SOURCE_REAUTH})
)

# ✅ NEW
self.entry.async_start_reauth(self.hass)
```

### 5. Add Connection Testing (Bronze Tier Requirement)

```python
# ❌ BAD
async def async_step_user(self, user_input=None):
    if user_input:
        return self.async_create_entry(...)  # No validation!

# ✅ GOOD
async def async_step_user(self, user_input=None):
    errors = {}
    if user_input:
        try:
            client = MyClient(user_input[CONF_HOST])
            await client.test_connection()  # Validate!
        except ConnectionError:
            errors["base"] = "cannot_connect"
        else:
            return self.async_create_entry(...)
    return self.async_show_form(..., errors=errors)
```

### 6. Add Unique ID Handling (Bronze Tier Requirement)

```python
# ❌ BAD - Using IP
await self.async_set_unique_id(user_input[CONF_HOST])

# ❌ BAD - Missing check
await self.async_set_unique_id(device_id)
# Missing: self._abort_if_unique_id_configured()

# ✅ GOOD
device_id = await client.get_serial_number()  # Stable ID
await self.async_set_unique_id(device_id)
self._abort_if_unique_id_configured()
```

### 7. Fix Discovery Flow (UX Requirement)

```python
# ❌ BAD - No confirmation
async def async_step_zeroconf(self, discovery_info):
    return self.async_create_entry(...)  # Immediate!

# ✅ GOOD - Requires confirmation
async def async_step_zeroconf(self, discovery_info):
    await self.async_set_unique_id(...)
    self._abort_if_unique_id_configured(updates={CONF_HOST: ...})
    self._discovered_host = discovery_info.host
    return await self.async_step_discovery_confirm()
```

### 8. Migrate to runtime_data (Best Practice)

```python
# ❌ OLD
hass.data.setdefault(DOMAIN, {})
hass.data[DOMAIN][entry.entry_id] = client

# ✅ NEW
from dataclasses import dataclass

type MyConfigEntry = ConfigEntry[MyData]

@dataclass
class MyData:
    client: MyClient

entry.runtime_data = MyData(client=client)
```

### 9. Update Options Flow (Deadline: 2025.12)

```python
# ❌ OLD
def async_get_options_flow(config_entry):
    return OptionsFlowHandler(config_entry)

class OptionsFlowHandler(OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

# ✅ NEW
def async_get_options_flow(config_entry):
    return OptionsFlowHandler()

class OptionsFlowHandler(OptionsFlow):
    # self.config_entry available automatically!
    pass
```

### 10. Use Manifest for Single Instance (Best Practice)

```python
# ❌ OLD - Code check
async def async_step_user(self, user_input=None):
    if self._async_current_entries():
        return self.async_abort(reason="single_instance_allowed")

# ✅ NEW - Manifest
# manifest.json:
{
  "single_config_entry": true
}
# Remove code check!
```

---

## Common Refactoring Scenarios

### Scenario 1: Add Reauth Flow

**Steps:**
1. Add `async_step_reauth` and `async_step_reauth_confirm`
2. Add unique ID verification in reauth_confirm
3. Trigger from `__init__.py` with `ConfigEntryAuthFailed`

**Template:**
```python
class MyConfigFlow(ConfigFlow, domain=DOMAIN):
    async def async_step_reauth(self, entry_data):
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input=None):
        errors = {}
        if user_input:
            client = MyClient(...)
            try:
                device_id = await client.get_device_id()
            except InvalidAuthError:
                errors["base"] = "invalid_auth"
            else:
                await self.async_set_unique_id(device_id)
                self._abort_if_unique_id_mismatch(reason="wrong_account")
                return self.async_update_reload_and_abort(
                    self._get_reauth_entry(),
                    data_updates={CONF_PASSWORD: user_input[CONF_PASSWORD]}
                )
        return self.async_show_form(step_id="reauth_confirm", ...)

# In __init__.py:
async def async_setup_entry(hass, entry):
    try:
        await client.authenticate()
    except InvalidAuthError as err:
        raise ConfigEntryAuthFailed("Invalid credentials") from err
```

### Scenario 2: Add Discovery Support

**Steps:**
1. Add discovery step (zeroconf, ssdp, etc.)
2. Add discovery_confirm step
3. Update manifest.json
4. Test connection before confirming

**Template:**
```python
async def async_step_zeroconf(self, discovery_info):
    await self.async_set_unique_id(discovery_info.properties["serial"])
    self._abort_if_unique_id_configured(updates={CONF_HOST: discovery_info.host})

    try:
        client = MyClient(discovery_info.host)
        await client.test_connection()
    except Exception:
        return self.async_abort(reason="cannot_connect")

    self._discovered_host = discovery_info.host
    return await self.async_step_discovery_confirm()

async def async_step_discovery_confirm(self, user_input=None):
    if user_input is not None:
        return self.async_create_entry(
            title="Discovered Device",
            data={CONF_HOST: self._discovered_host}
        )
    self._set_confirm_only()
    return self.async_show_form(step_id="discovery_confirm")

# manifest.json:
{
  "zeroconf": ["_mydevice._tcp.local."]
}
```

### Scenario 3: Migrate hass.data to runtime_data

**Steps:**
1. Create dataclass for runtime data
2. Create type alias with ConfigEntry suffix
3. Update async_setup_entry to use runtime_data
4. Update platforms to use typed config entry
5. Remove manual cleanup from async_unload_entry

**Template:**
```python
# __init__.py
from dataclasses import dataclass
from homeassistant.config_entries import ConfigEntry

type MyConfigEntry = ConfigEntry[MyData]

@dataclass
class MyData:
    client: MyClient
    coordinator: MyCoordinator | None = None

async def async_setup_entry(hass, entry: MyConfigEntry):
    client = MyClient(...)
    entry.runtime_data = MyData(client=client)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass, entry: MyConfigEntry):
    # Automatic cleanup - no manual pop needed!
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

# sensor.py
from . import MyConfigEntry

async def async_setup_entry(hass, entry: MyConfigEntry, async_add_entities):
    client = entry.runtime_data.client  # Type-safe!
    async_add_entities([MySensor(client)])
```

### Scenario 4: Update Old Validators to Modern Selectors

**Before:**
```python
data_schema = vol.Schema({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Optional(CONF_PORT, default=80): cv.port,
})
```

**After:**
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

---

## Incremental Refactoring Strategy

### Phase 1: Fix Breaking Issues (1-2 hours)
1. Update ServiceInfo imports
2. Fix direct entry mutations
3. Fix async_show_progress
4. Update reauth trigger
5. Update options flow initialization

### Phase 2: Bronze Tier Requirements (2-4 hours)
1. Add connection testing
2. Add unique ID handling
3. Add duplicate entry check
4. Add error handling
5. Achieve 100% test coverage

### Phase 3: Code Modernization (2-3 hours)
1. Migrate to runtime_data
2. Update to modern selectors
3. Add manifest options
4. Use helper methods

### Phase 4: Silver Tier (3-5 hours)
1. Implement reauth flow
2. Implement proper unload
3. Test reauth scenarios
4. Test unload behavior

### Phase 5: Gold Tier (4-8 hours)
1. Add discovery support
2. Implement reconfigure flow
3. Test discovery scenarios
4. Test reconfigure flow

---

## Testing Checklist

After refactoring, verify:

- [ ] All tests pass
- [ ] 100% config flow test coverage
- [ ] User flow tested (happy path)
- [ ] User flow tested (cannot_connect error)
- [ ] User flow tested (invalid_auth error)
- [ ] User flow tested (already_configured)
- [ ] Discovery flow tested (if applicable)
- [ ] Reauth flow tested (if implemented)
- [ ] Reconfigure flow tested (if implemented)
- [ ] Options flow tested (if exists)
- [ ] Manual testing completed
- [ ] No regressions

---

## Red Flags to Look For

**Immediate Action Required:**
- `entry.data["field"] = value` - Direct mutation (FAILS NOW)
- `async_show_progress` without `progress_task` (FAILS NOW)
- `from homeassistant.components.zeroconf import ZeroconfServiceInfo` (Fails 2026.2)

**Quality Issues:**
- No `try/except` in config flow steps
- No `async_set_unique_id()` call
- IP address used as unique ID
- No `_abort_if_unique_id_configured()` check
- Discovery step creates entry immediately
- No reauth flow for authenticated integrations

**Best Practice Violations:**
- Using `hass.data` instead of `runtime_data`
- Manual single-instance check instead of manifest
- Old `cv.string` validators instead of modern selectors
- Not using helper methods (`_get_reauth_entry()`, etc.)

---

## Quick Reference: Import Updates

### Discovery ServiceInfo (Deadline: 2026.2)

```python
# ❌ OLD
from homeassistant.components.zeroconf import ZeroconfServiceInfo
from homeassistant.components.dhcp import DhcpServiceInfo
from homeassistant.components.ssdp import SsdpServiceInfo
from homeassistant.components.usb import UsbServiceInfo

# ✅ NEW
from homeassistant.helpers.service_info.zeroconf import ZeroconfServiceInfo
from homeassistant.helpers.service_info.dhcp import DhcpServiceInfo
from homeassistant.helpers.service_info.ssdp import SsdpServiceInfo
from homeassistant.helpers.service_info.usb import UsbServiceInfo
```

---

## Related Documentation

**Main Research:**
- `thoughts/shared/research/2025-11-21-ha-config-flow-skill-implementation-research.md` - Complete implementation and refactoring patterns (Section 11)

**Refactoring Patterns:**
- `thoughts/shared/research/2025-11-21-home-assistant-integration-refactoring-patterns.md` - Detailed refactoring patterns for all integration aspects

**Blog Posts (Breaking Changes):**
- `blog/2025-11-05-config-entry-oauth2-error-handling.md`
- `blog/2025-01-15-service-info.md`
- `blog/2024-11-12-options-flow.md`
- `blog/2024-11-04-reauth-reconfigure-entry-id.md`
- `blog/2024-10-21-reauth-reconfigure-helpers.md`
- `blog/2024-02-12-async_update_entry.md`
- `blog/2024-01-11-async-show-progress-changes.md`

---

## Summary

This quick reference provides:
- ✅ Quick assessment checklist for identifying issues
- ✅ Critical deadlines for breaking changes
- ✅ Top 10 fixes in priority order
- ✅ 4 common refactoring scenarios with templates
- ✅ Phase-by-phase refactoring strategy
- ✅ Testing checklist
- ✅ Red flags to watch for

For complete details, code templates, and comprehensive patterns, see the main research document: `thoughts/shared/research/2025-11-21-ha-config-flow-skill-implementation-research.md` (Section 11).
