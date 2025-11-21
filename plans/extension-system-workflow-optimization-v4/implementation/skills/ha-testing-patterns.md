# ha-testing-patterns Skill Implementation Spec

**Objective:** Provide comprehensive testing patterns, templates, and coverage requirements for Home Assistant integration testing

**Priority:** CRITICAL - Testing is mandatory with specific coverage thresholds

**Estimated effort:** 3-4 hours

**Dependencies:** Should be used alongside all other Skills during implementation

---

## Why This Skill is Critical

**From HA Research:**
- **95%+ overall test coverage required** (research: 76/104)
- **100% config flow coverage required** (research: 76/99-101)
- Test-before-configure pattern mandatory
- Test-before-setup pattern mandatory
- Proper fixture usage essential
- Snapshot testing for translations/strings

**Without this Skill:**
- Developers miss mandatory coverage requirements
- Tests structured incorrectly (won't pass CI)
- Missing critical test patterns (test_setup_entry, test_unload_entry)
- Fixture misuse causing flaky tests
- Integration won't be accepted in HA core

---

## Skill Structure

```
.claude/skills/ha-testing-patterns/
├── SKILL.md                           # Main Skill definition
├── test-structure.md                  # Test file organization
├── coverage-requirements.md           # Required coverage levels
├── fixture-patterns.md                # MockConfigEntry, AsyncMock, etc.
├── config-flow-testing.md             # Config flow specific tests
├── snapshot-testing.md                # Snapshot test patterns
├── templates/
│   ├── test_init.py                   # Setup/unload tests
│   ├── test_config_flow.py            # Config flow tests
│   ├── test_sensor.py                 # Platform tests
│   ├── test_coordinator.py            # Coordinator tests
│   └── conftest.py                    # Shared fixtures
└── examples/
    └── real-integration-tests.md      # Links to real test examples
```

---

## SKILL.md Content

### Overview Section

```markdown
# Home Assistant Testing Patterns

**Description:** Comprehensive testing patterns, templates, and coverage requirements for HA integration testing

**When to use:**
- Writing tests for new integration
- Adding test coverage to existing integration
- Debugging failing tests
- Understanding HA test requirements

**Activates on:**
- Prompts containing: "test", "testing", "coverage", "pytest", "fixture", "mock", "conftest"
- Files matching: `**/tests/test_*.py`, `**/tests/conftest.py`, `pytest.ini`

---

## Overview

Home Assistant has **strict testing requirements**:
- **95%+ overall coverage** (mandatory for core acceptance)
- **100% config flow coverage** (no exceptions)
- Specific test patterns (test-before-configure, test-before-setup)
- Proper fixture usage (MockConfigEntry, AsyncMock)
- Snapshot testing for translations

This Skill provides all necessary patterns, templates, and guidance to meet these requirements.

**Key Capabilities:**
- Test file structure and organization
- Coverage requirement enforcement
- Fixture patterns and best practices
- Config flow test templates (100% coverage)
- Platform test templates (sensors, switches, etc.)
- Coordinator test patterns
- Snapshot testing guidance
- Common test failures and fixes

---

## Test Structure

### Required Test Files

Every integration must have:

```
tests/
├── __init__.py                  # Empty file, marks as package
├── conftest.py                  # Shared fixtures
├── test_init.py                 # Setup/unload tests (REQUIRED)
├── test_config_flow.py          # Config flow tests (REQUIRED, 100% coverage)
├── test_sensor.py               # Platform tests (if has sensor platform)
├── test_switch.py               # Platform tests (if has switch platform)
├── test_coordinator.py          # Coordinator tests (if uses coordinator)
└── snapshots/                   # Snapshot test data
    └── test_config_flow/
        └── *.ambr               # Snapshot files
```

**See:** `test-structure.md` for detailed organization

---

## Coverage Requirements

### Mandatory Thresholds

**Overall Coverage: 95%+**
- Measured across all integration code
- Reported by pytest-cov
- CI will fail if below threshold
- No exceptions

**Config Flow Coverage: 100%**
- Every line in config_flow.py must be tested
- Every branch must be tested
- Every error condition must be tested
- No exceptions

**Platform Coverage: 90%+**
- Each platform file (sensor.py, switch.py, etc.)
- Required for quality tiers

**Coordinator Coverage: 95%+**
- If integration uses DataUpdateCoordinator
- Must test all update scenarios
- Must test error handling

**See:** `coverage-requirements.md` for complete details

---

## Core Test Patterns

### Pattern 1: Test-Before-Configure

**Purpose:** Verify integration loads before config entry is configured

**Implementation:**
```python
async def test_setup_entry(hass: HomeAssistant, mock_client: AsyncMock) -> None:
    """Test setup of config entry."""
    entry = MockConfigEntry(domain=DOMAIN, data={CONF_HOST: "192.168.1.1"})
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.LOADED
```

**See:** `templates/test_init.py` for full template

### Pattern 2: Test-Before-Setup

**Purpose:** Verify configuration before integration is set up

**Implementation:**
```python
async def test_form_user(hass: HomeAssistant) -> None:
    """Test user config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {}
```

**See:** `templates/test_config_flow.py` for full template

### Pattern 3: Fixture Usage

**MockConfigEntry:**
```python
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import MockConfigEntry

entry = MockConfigEntry(
    domain=DOMAIN,
    data={CONF_HOST: "192.168.1.1", CONF_USERNAME: "user"},
    unique_id="unique_device_id",
)
entry.add_to_hass(hass)
```

**AsyncMock for API Clients:**
```python
from unittest.mock import AsyncMock, patch

mock_client = AsyncMock()
mock_client.fetch_data.return_value = {"temperature": 20}

with patch("custom_components.myintegration.api.Client", return_value=mock_client):
    # Test code that uses Client
```

**See:** `fixture-patterns.md` for all fixture patterns

---

## Config Flow Testing (100% Coverage Required)

### Must Test Every Scenario

**User Flow:**
- [ ] Initial form display
- [ ] Successful submission
- [ ] Invalid input (each field)
- [ ] Connection errors
- [ ] Authentication errors
- [ ] Already configured check

**Discovery/Zeroconf Flow:**
- [ ] Discovery detection
- [ ] Confirmation form
- [ ] User overrides
- [ ] Duplicate detection

**Options Flow:**
- [ ] Options form display
- [ ] Successful update
- [ ] Invalid options
- [ ] Reload trigger

**Error Conditions:**
- [ ] Cannot connect
- [ ] Invalid auth
- [ ] Unknown error
- [ ] Timeout
- [ ] Already configured

**See:** `config-flow-testing.md` and `templates/test_config_flow.py`

---

## Platform Testing

### Sensor Platform

```python
async def test_sensor_state(hass: HomeAssistant, mock_entry: ConfigEntry) -> None:
    """Test sensor reports correct state."""
    await hass.config_entries.async_setup(mock_entry.entry_id)
    await hass.async_block_till_done()

    state = hass.states.get("sensor.device_temperature")
    assert state is not None
    assert state.state == "20.0"
    assert state.attributes["unit_of_measurement"] == "°C"
```

**Must Test:**
- [ ] State value
- [ ] Attributes
- [ ] Unit of measurement
- [ ] Device class
- [ ] State class
- [ ] Icon (if dynamic)
- [ ] Availability

**See:** `templates/test_sensor.py` for full template

### Switch/Binary Sensor/Other Platforms

Similar patterns apply for all platforms.

**See:** Platform-specific templates in `templates/`

---

## Coordinator Testing

```python
async def test_coordinator_update(hass: HomeAssistant, mock_client: AsyncMock) -> None:
    """Test coordinator updates data."""
    coordinator = MyCoordinator(hass, mock_client)

    mock_client.fetch_data.return_value = {"temperature": 21}
    await coordinator.async_config_entry_first_refresh()

    assert coordinator.data == {"temperature": 21}
    assert coordinator.last_update_success is True
```

**Must Test:**
- [ ] Successful update
- [ ] Update failure handling
- [ ] Authentication refresh
- [ ] Rate limiting
- [ ] Error recovery

**See:** `templates/test_coordinator.py`

---

## Snapshot Testing

For translations and strings file testing:

```python
from syrupy import SnapshotAssertion

async def test_config_flow_translations(
    hass: HomeAssistant,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config flow translations match snapshot."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result == snapshot
```

**See:** `snapshot-testing.md` for patterns

---

## Templates Provided

### 1. test_init.py
**Purpose:** Setup, unload, and reload tests
**Coverage:** Entry lifecycle
**File:** `templates/test_init.py`

### 2. test_config_flow.py
**Purpose:** Complete config flow test suite
**Coverage:** 100% config flow coverage
**File:** `templates/test_config_flow.py`

### 3. test_sensor.py
**Purpose:** Sensor platform tests
**Coverage:** State, attributes, availability
**File:** `templates/test_sensor.py`

### 4. test_coordinator.py
**Purpose:** DataUpdateCoordinator tests
**Coverage:** Update, error handling, auth refresh
**File:** `templates/test_coordinator.py`

### 5. conftest.py
**Purpose:** Shared fixtures for all tests
**Coverage:** Fixtures, mocks, common setup
**File:** `templates/conftest.py`

---

## Checklists

### New Integration Testing Checklist

**Initial Setup:**
- [ ] Create `tests/` directory with `__init__.py`
- [ ] Create `conftest.py` with shared fixtures
- [ ] Create `test_init.py` for setup/unload tests
- [ ] Create `test_config_flow.py` for config flow tests

**Coverage Goals:**
- [ ] Overall coverage ≥ 95%
- [ ] Config flow coverage = 100%
- [ ] Platform coverage ≥ 90%
- [ ] Coordinator coverage ≥ 95% (if applicable)

**Test Patterns:**
- [ ] Test-before-configure pattern implemented
- [ ] Test-before-setup pattern implemented
- [ ] All error conditions tested
- [ ] All user inputs validated
- [ ] Edge cases covered

**Fixtures:**
- [ ] MockConfigEntry used correctly
- [ ] AsyncMock used for API clients
- [ ] Fixtures shared via conftest.py
- [ ] No hardcoded test data

**Platform Tests (if applicable):**
- [ ] Sensor tests (test_sensor.py)
- [ ] Switch tests (test_switch.py)
- [ ] Binary sensor tests (test_binary_sensor.py)
- [ ] Climate tests (test_climate.py)
- [ ] Light tests (test_light.py)

**CI/CD:**
- [ ] Tests pass locally with `pytest`
- [ ] Coverage report generated with `pytest-cov`
- [ ] Pre-commit hooks pass
- [ ] No test warnings

### Config Flow 100% Coverage Checklist

**User Flow:**
- [ ] Test initial form
- [ ] Test successful submission
- [ ] Test each input field validation
- [ ] Test connection failure
- [ ] Test authentication failure
- [ ] Test already configured

**Discovery Flow (if applicable):**
- [ ] Test discovery detection
- [ ] Test confirmation
- [ ] Test duplicate detection

**Options Flow (if applicable):**
- [ ] Test options form
- [ ] Test successful update
- [ ] Test invalid options

**Error Handling:**
- [ ] Test cannot_connect error
- [ ] Test invalid_auth error
- [ ] Test unknown error
- [ ] Test timeout handling

**Edge Cases:**
- [ ] Test empty input
- [ ] Test special characters
- [ ] Test very long input
- [ ] Test concurrent setup attempts

---

## Common Issues

### Issue 1: Coverage Below 95%

**Symptom:** CI fails with coverage report below 95%

**Cause:** Missing tests for error conditions, edge cases, or unused code

**Solution:**
1. Run `pytest --cov=custom_components.DOMAIN --cov-report=html`
2. Open `htmlcov/index.html` to see uncovered lines
3. Add tests for uncovered lines or remove unused code
4. Rerun until ≥95%

### Issue 2: Config Flow Not 100%

**Symptom:** CI fails with config flow coverage < 100%

**Cause:** Missing tests for error branches or recovery logic

**Solution:**
- Test every error condition (cannot_connect, invalid_auth, unknown)
- Test every user input scenario
- Test discovery and options flows (if present)
- Use coverage report to find missing branches

### Issue 3: Flaky Tests

**Symptom:** Tests pass sometimes, fail other times

**Cause:**
- Not awaiting async operations
- Not using `hass.async_block_till_done()`
- Race conditions in mocks

**Solution:**
```python
# Always await and block
await hass.config_entries.async_setup(entry.entry_id)
await hass.async_block_till_done()

# Ensure mocks are deterministic
mock_client.fetch_data.return_value = {"data": "value"}  # Not side_effect with random
```

### Issue 4: Fixture Not Found

**Symptom:** `fixture 'hass' not found`

**Cause:** Missing pytest-homeassistant plugin or incorrect test structure

**Solution:**
- Install: `pip install pytest-homeassistant-custom-component`
- Add to `pyproject.toml`: pytest-homeassistant-custom-component
- Ensure tests directory structure is correct

### Issue 5: MockConfigEntry Not Behaving Correctly

**Symptom:** Entry not loaded or state incorrect

**Cause:** Forgot to call `entry.add_to_hass(hass)`

**Solution:**
```python
entry = MockConfigEntry(domain=DOMAIN, data={...})
entry.add_to_hass(hass)  # REQUIRED
await hass.config_entries.async_setup(entry.entry_id)
```

---

## Examples

### Example 1: MQTT Integration

**Path:** `homeassistant/components/mqtt/test_*.py`

**Coverage:** 98% overall, 100% config flow

**Key Patterns:**
- Comprehensive fixture usage in conftest.py
- Extensive config flow testing
- Snapshot testing for translations
- Platform tests for all entity types

**Notable:**
- Over 50 test files
- Excellent example of test organization

### Example 2: Shelly Integration

**Path:** `homeassistant/components/shelly/test_*.py`

**Coverage:** 96% overall, 100% config flow

**Key Patterns:**
- Discovery flow testing
- Options flow testing
- Device trigger testing
- Coordinator update testing

**Notable:**
- Good example of coordinator testing
- Complete error condition coverage

### Example 3: Template Integration

**Path:** `homeassistant/components/template/test_*.py`

**Coverage:** 97% overall

**Key Patterns:**
- Platform-specific tests
- Template rendering tests
- Reload testing

---

## Related Skills

- **ha-config-flow-knowledge**: Use together when testing config flows - this Skill provides the test patterns for config flow implementations
- **ha-entity-knowledge**: Use together when testing entities - this Skill provides test patterns for entity state and attributes
- **ha-coordinator-knowledge**: Use together when testing coordinators - this Skill provides test patterns for coordinator updates
- **ha-common-mistakes**: Reference when debugging test failures - anti-patterns often cause test issues

---

## References

- [HA Testing Documentation](https://developers.home-assistant.io/docs/development_testing)
- [pytest-homeassistant-custom-component](https://github.com/MatthewFlamm/pytest-homeassistant-custom-component)
- [HA Core Test Examples](https://github.com/home-assistant/core/tree/dev/tests/components)
- Research Document: Lines 76-104, 447-464 (coverage requirements and test patterns)

---

**Last Updated:** 2025-11-21
**Version:** 1.0
**Priority:** CRITICAL
