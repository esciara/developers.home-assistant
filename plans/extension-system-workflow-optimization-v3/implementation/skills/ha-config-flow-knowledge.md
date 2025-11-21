# ha-config-flow-knowledge Skill Implementation Spec

**Priority:** High (critical for config flow overhaul use case)

**Estimated Effort:** 3-4 hours

**Dependencies:** Hook infrastructure

---

## Purpose

Provides comprehensive patterns, templates, and best practices for implementing Home Assistant configuration flows, including user setup wizards, discovery flows, and options flows.

---

## Skill Directory Structure

```
.claude/skills/ha-config-flow-knowledge/
├── SKILL.md
├── step-patterns.md
├── error-handling.md
├── schema-definitions.md
├── validation-strategies.md
├── discovery-patterns.md
├── templates/
│   ├── basic-config-flow.py
│   ├── discovery-flow.py
│   ├── options-flow.py
│   └── multi-step-flow.py
└── examples/
    └── examples.md
```

---

## Trigger Configuration

### skill-rules.json Entry

```json
{
  "ha-config-flow-knowledge": {
    "prompt_patterns": [
      "config flow",
      "config_flow",
      "configuration",
      "setup wizard",
      "user input",
      "config entry",
      "options flow",
      "flow step",
      "async_step",
      "async_step_user",
      "async_step_discovery",
      "schema definition",
      "vol.Schema",
      "data entry flow",
      "flow handler",
      "config flow test"
    ],
    "file_patterns": [
      "**/homeassistant/components/**/config_flow.py",
      "**/homeassistant/components/**/config_flow_test.py",
      "**/tests/components/**/test_config_flow.py"
    ],
    "contexts": [
      "configuration flow",
      "user setup",
      "integration configuration",
      "discovery flow",
      "options flow"
    ]
  }
}
```

---

## SKILL.md Content Outline

### Overview Section

```markdown
# Home Assistant Config Flow Knowledge

**Description:** Comprehensive patterns and templates for implementing HA configuration flows

**When to use:**
- Creating new config flows
- Implementing user setup wizards
- Adding discovery support
- Creating options flows
- Troubleshooting config flow issues

**Activates on:**
- Prompts containing: "config flow", "setup wizard", "user input"
- Files matching: `**/config_flow.py`
```

### Patterns to Document

**1. Flow Step Patterns**
- `async_step_user` - Manual setup entry point
- `async_step_discovery` - Discovered device setup
- `async_step_zeroconf` - Zeroconf discovery
- `async_step_ssdp` - SSDP discovery
- `async_step_confirm` - Confirmation steps
- Multi-step flows with data passing

**2. Schema Definitions**
- vol.Schema basics
- Required vs Optional fields
- Validators (vol.Coerce, vol.In, etc.)
- Custom validators
- Conditional schemas
- Default values

**3. Error Handling**
- FlowResult error reporting
- User-friendly error messages
- Field-specific errors
- Recoverable vs fatal errors
- Error translation strings

**4. Data Entry Flow Lifecycle**
- Creating entries (self.async_create_entry)
- Aborting flows (self.async_abort)
- Showing forms (self.async_show_form)
- Progress dialogs
- Flow context management

**5. Options Flows**
- @staticmethod async_get_options_flow
- Inheriting from OptionsFlow
- Updating existing entries
- Options schema patterns

**6. Discovery Patterns**
- Discovery info structure
- Unique ID handling in discovery
- Conflict resolution
- Updating discovered devices

**7. Testing Patterns**
- Config flow test structure
- Mocking user input
- Testing error cases
- Testing discovery flows

### Templates to Create

**1. templates/basic-config-flow.py**
```python
"""
Basic Config Flow Template

Single-step user configuration flow with error handling.

Usage:
1. Replace [DOMAIN] with your integration domain
2. Replace [CONNECTION_PARAMS] with your connection parameters
3. Implement _test_connection method
4. Add translation strings
"""

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult
import voluptuous as vol

from .const import DOMAIN


class [DOMAIN]ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for [DOMAIN]."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate user input
            try:
                # Test connection
                await self._test_connection(user_input)
            except [EXCEPTION_TYPE]:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                errors["base"] = "unknown"
            else:
                # Create unique ID to prevent duplicates
                await self.async_set_unique_id(user_input[CONF_HOST])
                self._abort_if_unique_id_configured()

                # Create entry
                return self.async_create_entry(
                    title=user_input[CONF_HOST],
                    data=user_input,
                )

        # Show form
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors,
        )

    async def _test_connection(self, user_input: dict[str, Any]) -> None:
        """Test connection to device/service."""
        # Implement connection test
        pass
```

**2. templates/discovery-flow.py**
```python
"""
Discovery Flow Template

Config flow with automatic discovery support.
"""

# [Full implementation with discovery, zeroconf, and user steps]
```

**3. templates/options-flow.py**
```python
"""
Options Flow Template

Allows users to modify integration configuration after setup.
"""

# [Full implementation of OptionsFlowHandler]
```

**4. templates/multi-step-flow.py**
```python
"""
Multi-Step Flow Template

Config flow with multiple steps for complex setup.
"""

# [Full implementation showing data passing between steps]
```

### Checklists to Include

**Config Flow Implementation Checklist:**
- [ ] ConfigFlow class inherits from config_entries.ConfigFlow
- [ ] domain class variable set correctly
- [ ] VERSION specified
- [ ] async_step_user implemented
- [ ] Schema defined with appropriate validators
- [ ] Error handling present
- [ ] Unique ID set to prevent duplicates
- [ ] async_create_entry called with title and data
- [ ] Translation strings added (strings.json)
- [ ] Tests created

**Discovery Flow Checklist:**
- [ ] Discovery step implemented (async_step_discovery, etc.)
- [ ] Discovery info processed correctly
- [ ] Unique ID derived from discovery info
- [ ] Conflict resolution handled
- [ ] User confirmation step (if needed)

**Options Flow Checklist:**
- [ ] async_get_options_flow static method defined
- [ ] OptionsFlowHandler class created
- [ ] async_step_init implemented
- [ ] Options schema defined
- [ ] async_create_entry updates existing entry
- [ ] Options accessible in __init__.py

### Examples to Reference

**Example 1: MQTT Config Flow**
- Path: `homeassistant/components/mqtt/config_flow.py`
- Pattern: Discovery + manual setup
- Note: Good example of both discovery and manual entry

**Example 2: Demo Config Flow**
- Path: `homeassistant/components/demo/config_flow.py`
- Pattern: Minimal single-step flow
- Note: Simplest possible config flow

**Example 3: Met.no Config Flow**
- Path: `homeassistant/components/met/config_flow.py`
- Pattern: Location-based setup with validation
- Note: Good schema validation example

---

## Supporting Documents

### step-patterns.md

```markdown
# Config Flow Step Patterns

## async_step_user

Entry point for manual configuration...

[Detailed explanation with examples]

## async_step_discovery

Handling discovered devices...

[Detailed explanation]

## Flow Data Passing

Passing data between steps...

[Examples]
```

### error-handling.md

```markdown
# Config Flow Error Handling

## Error Types

### cannot_connect
[When to use, example]

### invalid_auth
[When to use, example]

### already_configured
[When to use, example]

## Custom Errors

[How to add custom error types]

## Translation Strings

[How to add error messages to strings.json]
```

### schema-definitions.md

```markdown
# Schema Definitions for Config Flows

## vol.Schema Basics

[Examples of common patterns]

## Field Types

### Text Input
```python
vol.Required(CONF_HOST): str
```

### Integer
```python
vol.Required(CONF_PORT, default=8080): int
```

### Boolean
```python
vol.Optional(CONF_VERIFY_SSL, default=True): bool
```

### Selection
```python
vol.Required(CONF_MODE): vol.In(["mode1", "mode2"])
```

## Validators

[Common validators with examples]

## Conditional Schemas

[How to show/hide fields based on other input]
```

### validation-strategies.md

```markdown
# Config Flow Validation Strategies

## Connection Testing

Best practices for testing connections...

## Input Validation

Validating user input before attempting connection...

## Error Recovery

Allowing users to correct errors without restarting flow...
```

### discovery-patterns.md

```markdown
# Discovery Flow Patterns

## Zeroconf Discovery

[How to implement zeroconf discovery]

## SSDP Discovery

[How to implement SSDP discovery]

## Unique ID from Discovery

[How to derive stable unique IDs from discovery info]
```

---

## Testing This Skill

### Activation Tests

**Prompt-based:**
- Type: "How do I create a config flow?" → Should activate
- Type: "async_step_user pattern" → Should activate
- Type: "config entry validation" → Should activate

**File-based:**
- Open: `config_flow.py` → Should activate
- Open: `test_config_flow.py` → Should activate

**Combined:**
- Open `config_flow.py` AND type "error handling" → Should activate with high confidence

### Template Validation

1. Copy `basic-config-flow.py` template
2. Replace placeholders
3. Verify compiles without errors
4. Check follows current HA config flow patterns
5. Test in actual integration (if possible)

### Pattern Accuracy

1. Verify async_step patterns match current HA API
2. Check schema examples compile
3. Validate error handling patterns work
4. Test discovery patterns with real discovery

---

## Success Criteria

- [ ] SKILL.md created and comprehensive
- [ ] All step patterns documented
- [ ] 4 templates created and validated
- [ ] 5 supporting docs created
- [ ] Examples reference current integrations
- [ ] Checklists cover common scenarios
- [ ] Activation patterns tested
- [ ] No false positives in testing
- [ ] Triggers on relevant prompts and files
- [ ] Templates follow current HA patterns

---

## Integration with Other Skills

**ha-common-mistakes:**
- References async/await pitfalls
- Links to blocking I/O warnings
- Cross-references error handling patterns

**ha-entity-knowledge:**
- Config flows create entities
- Entity unique ID strategy affects config flow unique ID

**ha-coordinator-knowledge:**
- Config flows often create coordinators
- Coordinator setup in __init__.py after config entry created

---

## Common Issues

**Issue: Config flow not showing in UI**
- Check domain in manifest.json includes "config_flow": true
- Verify ConfigFlow class domain matches integration domain

**Issue: Unique ID not preventing duplicates**
- Ensure unique_id is truly unique
- Must call self._abort_if_unique_id_configured()
- Unique ID should be based on device/service identifier

**Issue: Error messages not appearing**
- Check strings.json has error translations
- Verify error keys match strings.json keys
- Ensure errors dict keys match schema field names for field-specific errors

---

**Estimated Implementation Time:** 3-4 hours

**See Also:**
- [Skill Template](template.md)
- [Phase 1: Skills Foundation](../../phases/phase-1-skills.md)
- [Testing Guide](../../testing/skill-validation-tests.md)
