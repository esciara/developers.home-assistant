# Home Assistant Config Flow Knowledge

This skill provides guidance for implementing, refactoring, and troubleshooting Home Assistant configuration flows. It helps developers create UI-based setup wizards that meet Home Assistant's quality standards, including 100% test coverage requirements.

## When to Use This Skill

Use this skill when working on:
- Creating new config flows for integrations
- Refactoring YAML-only integrations to use UI-based configuration
- Adding reauthentication or reconfiguration flows
- Debugging config flow issues
- Ensuring config flow test coverage requirements are met

**Activates on**: "config flow", "configuration", "setup wizard", "config entry", "reauthentication", "reconfiguration"

---

## Research Document Section Map

This skill guides you to relevant sections in the comprehensive research documents:

### For New Config Flow Implementation
**Research Doc**: `thoughts/shared/research/2025-11-20-home-assistant-integration-skill-research.md`
- **Section 2: Configuration Flow Files** - Core patterns and requirements
  - Config flow basics (lines 55-73)
  - Key requirements: 100% test coverage, connection testing, unique IDs
  - Config entry lifecycle management
  - Form display and validation patterns

### For Refactoring Existing Integrations
**Research Doc**: `thoughts/shared/research/2025-11-21-home-assistant-integration-refactoring-patterns.md`
- **Section 1: Config Flow Refactoring** (lines 48-279) - Complete migration guide
  - Adding config flow to YAML-only integrations
  - Step-by-step implementation with code examples
  - Strings.json and error handling patterns
  - Test templates for 100% coverage

### For Authentication Flows
**Research Doc**: `thoughts/shared/research/2025-11-21-home-assistant-integration-refactoring-patterns.md`
- **Section 7: Authentication Flows** (lines 1167-1341)
  - Section 7.1: Reauthentication flow (expired credentials)
  - Section 7.2: Reconfiguration flow (non-credential updates)

---

## Key Requirements

### Bronze Tier (Mandatory)
✅ **UI-based config flow required** - No YAML for device/service integrations
✅ **100% config flow test coverage** - Every code path must be tested
✅ **Test connection before completing** - Validate credentials/connectivity in config flow
✅ **Set unique ID** - Call `async_set_unique_id()` and check for duplicates
✅ **Proper exception handling** - Use ConfigEntryNotReady, ConfigEntryAuthFailed

### Testing Requirements
- Test success path
- Test connection errors
- Test invalid authentication
- Test already configured
- Test each error case in strings.json

---

## Decision Trees

### When to Use Which Flow Type

**User Flow** (`async_step_user`)
- Use when: Manual setup by user
- Required for: All integrations supporting manual configuration

**Discovery Flow** (`async_step_zeroconf`, `async_step_ssdp`, etc.)
- Use when: Integration supports automatic discovery
- Requires: Unique ID from discovered device
- Must call: `_abort_if_unique_id_configured()`

**Reauthentication Flow** (`async_step_reauth`)
- Use when: Credentials expire or become invalid
- Trigger via: `ConfigEntryAuthFailed` exception in setup
- Must: Use `async_update_reload_and_abort()` to update and reload

**Reconfiguration Flow** (`async_step_reconfigure`)
- Use when: Non-credential settings need updating (host, port, etc.)
- Must: Verify unique ID matches to ensure same device
- Must: Use `async_update_reload_and_abort()`

### Error Handling Strategy

**Connection Errors** → Return `errors["base"] = "cannot_connect"`
**Authentication Errors** → Return `errors["base"] = "invalid_auth"`
**Unknown Errors** → Log exception, return `errors["base"] = "unknown"`

---

## Common Questions

### Q: How do I ensure 100% config flow test coverage?
**A**: See **Refactoring Doc Section 1, lines 204-278** for complete test templates covering:
- Success flow
- Connection errors
- Invalid auth
- Already configured
- All error cases

### Q: What's the difference between reauthentication and reconfiguration?
**A**: See **Refactoring Doc Section 7**:
- **Reauthentication** (7.1): For expired credentials - triggers on `ConfigEntryAuthFailed`
- **Reconfiguration** (7.2): For non-credential settings - user-initiated updates

### Q: How do I add a config flow to a YAML-only integration?
**A**: Follow **Refactoring Doc Section 1** complete migration guide:
1. Add `"config_flow": true` to manifest.json
2. Create config_flow.py with user flow
3. Create strings.json with translations
4. Update __init__.py for config entry support
5. Write tests for 100% coverage
6. Run `python3 -m script.hassfest` to validate

### Q: What exceptions should I raise during setup?
**A**: See **New Integrations Doc Section 2**:
- `ConfigEntryNotReady`: Device offline/temporary failures (will retry)
- `ConfigEntryAuthFailed`: Invalid credentials (triggers reauth flow)
- `ConfigEntryError`: Permanent configuration issues

### Q: How do I handle unique IDs correctly?
**A**: Best practices from **New Integrations Doc Section 2**:
- Use stable identifiers (serial number, MAC address, device ID from API)
- Call `await self.async_set_unique_id(device_id)` before creating entry
- Call `self._abort_if_unique_id_configured()` to prevent duplicates
- For discovery: `self._abort_if_unique_id_configured(updates={CONF_HOST: host})`

---

## Quick Reference Checklist

Before submitting config flow implementation:

- [ ] manifest.json has `"config_flow": true`
- [ ] config_flow.py implements at least `async_step_user`
- [ ] Connection tested before `async_create_entry`
- [ ] Unique ID set via `async_set_unique_id()`
- [ ] Duplicate check via `_abort_if_unique_id_configured()`
- [ ] strings.json created with all steps and errors
- [ ] All error paths return appropriate error keys
- [ ] ConfigEntryNotReady raised for temporary failures
- [ ] ConfigEntryAuthFailed raised for auth failures
- [ ] 100% test coverage in test_config_flow.py
- [ ] Tests cover: success, connection error, invalid auth, already configured
- [ ] Reauthentication flow implemented (if credentials can expire)
- [ ] `python3 -m script.hassfest` passes

---

## Pattern Examples

### Minimal Config Flow Structure
```python
class ExampleConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Test connection
            try:
                device_id = await test_connection(user_input[CONF_HOST])
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except InvalidAuthError:
                errors["base"] = "invalid_auth"
            else:
                # Set unique ID and check duplicates
                await self.async_set_unique_id(device_id)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input[CONF_HOST],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_HOST): str}),
            errors=errors,
        )
```

For complete implementation examples, see research documents.

---

## Navigation Summary

**Quick access to research doc sections:**

| Topic | Research Doc | Section |
|-------|-------------|---------|
| Config flow basics | New Integrations (2025-11-20) | Section 2 |
| Adding config flow to YAML integration | Refactoring (2025-11-21) | Section 1 |
| Reauthentication | Refactoring (2025-11-21) | Section 7.1 |
| Reconfiguration | Refactoring (2025-11-21) | Section 7.2 |
| Test coverage requirements | New Integrations (2025-11-20) | Section 4 |
| Quality scale requirements | New Integrations (2025-11-20) | Section 5 |

**These research documents reference official Home Assistant docs as needed.**
