# Testing Complete Guide

Testing is mandatory for Home Assistant integrations. This guide covers test structure, config flow testing (100% coverage required), mocking, and best practices.

## Test Requirements by Quality Tier

**Bronze** (minimum):
- ✅ 100% config flow test coverage (MANDATORY)
- ✅ Basic setup/unload tests
- ✅ Entity creation tests

**Silver**:
- ✅ Above + 80% overall test coverage
- ✅ Error path testing
- ✅ Service action tests

**Gold**:
- ✅ Above + 90% overall test coverage
- ✅ Snapshot testing for complex outputs
- ✅ Integration tests

**Platinum**:
- ✅ Above + 95% overall test coverage
- ✅ Comprehensive edge case testing
- ✅ Performance tests

## Test Directory Structure

```
tests/components/my_device/
├── __init__.py          # Required, simple docstring
├── conftest.py          # Test fixtures
├── test_init.py         # Test __init__.py (setup/unload)
├── test_config_flow.py  # Config flow tests (100% coverage REQUIRED)
├── test_sensor.py       # Sensor platform tests
├── test_light.py        # Light platform tests
└── snapshots/           # Snapshot test files (.ambr)
```

### __init__.py

**Required** but can be minimal:
```python
"""Tests for the My Device integration."""
```

### conftest.py

Test fixtures shared across all tests:
```python
"""Fixtures for My Device tests."""
import pytest
from unittest.mock import AsyncMock, patch

from homeassistant.const import CONF_HOST, CONF_API_KEY

from tests.common import MockConfigEntry

from custom_components.my_device.const import DOMAIN


@pytest.fixture
def mock_config_entry():
    """Return a mock config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_HOST: "192.168.1.100",
            CONF_API_KEY: "test-key",
        },
        unique_id="device123",
    )


@pytest.fixture
def mock_api():
    """Return a mock API."""
    api = AsyncMock()
    api.async_test_connection.return_value = True
    api.async_get_device_id.return_value = "device123"
    api.async_get_data.return_value = {
        "temperature": 22.5,
        "humidity": 60,
    }
    return api


@pytest.fixture
def mock_setup_entry():
    """Mock setup entry."""
    with patch(
        "custom_components.my_device.async_setup_entry",
        return_value=True,
    ) as mock_setup:
        yield mock_setup
```

## Config Flow Testing (100% Coverage REQUIRED)

**CRITICAL**: 100% config flow test coverage is MANDATORY for Bronze tier.

### Test User Flow Success

```python
"""Test config flow for My Device."""
from unittest.mock import AsyncMock, patch

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_API_KEY
from homeassistant.core import HomeAssistant

from custom_components.my_device.const import DOMAIN


async def test_user_flow_success(hass: HomeAssistant):
    """Test successful user flow."""
    # Start flow
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    # Verify form shown
    assert result["type"] == "form"
    assert result["step_id"] == "user"
    assert result["errors"] == {}

    # Mock API calls
    with patch(
        "custom_components.my_device.config_flow.MyDeviceAPI"
    ) as mock_api_class:
        mock_api = AsyncMock()
        mock_api.async_test_connection.return_value = True
        mock_api.async_get_device_id.return_value = "device123"
        mock_api_class.return_value = mock_api

        # Submit form
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_HOST: "192.168.1.100",
                CONF_API_KEY: "test-key",
            },
        )

    # Verify entry created
    assert result["type"] == "create_entry"
    assert result["title"] == "192.168.1.100"
    assert result["data"] == {
        CONF_HOST: "192.168.1.100",
        CONF_API_KEY: "test-key",
    }
```

### Test Error Handling

**Connection errors**:
```python
async def test_user_flow_cannot_connect(hass: HomeAssistant):
    """Test connection error handling."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    # Mock connection failure
    with patch(
        "custom_components.my_device.config_flow.MyDeviceAPI"
    ) as mock_api_class:
        mock_api = AsyncMock()
        mock_api.async_test_connection.side_effect = ConnectionError
        mock_api_class.return_value = mock_api

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOST: "192.168.1.100", CONF_API_KEY: "test-key"},
        )

    # Verify error shown
    assert result["type"] == "form"
    assert result["errors"] == {"base": "cannot_connect"}
```

**Authentication errors**:
```python
async def test_user_flow_invalid_auth(hass: HomeAssistant):
    """Test authentication error handling."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.my_device.config_flow.MyDeviceAPI"
    ) as mock_api_class:
        mock_api = AsyncMock()
        mock_api.async_test_connection.side_effect = AuthenticationError
        mock_api_class.return_value = mock_api

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOST: "192.168.1.100", CONF_API_KEY: "bad-key"},
        )

    assert result["type"] == "form"
    assert result["errors"] == {"base": "invalid_auth"}
```

**Unknown errors**:
```python
async def test_user_flow_unknown_error(hass: HomeAssistant):
    """Test unknown error handling."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.my_device.config_flow.MyDeviceAPI"
    ) as mock_api_class:
        mock_api = AsyncMock()
        mock_api.async_test_connection.side_effect = Exception("Unexpected")
        mock_api_class.return_value = mock_api

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOST: "192.168.1.100", CONF_API_KEY: "test-key"},
        )

    assert result["type"] == "form"
    assert result["errors"] == {"base": "unknown"}
```

### Test Duplicate Prevention

```python
from tests.common import MockConfigEntry

async def test_duplicate_entry(hass: HomeAssistant):
    """Test duplicate entry is aborted."""
    # Create existing entry
    existing_entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="device123",
        data={CONF_HOST: "192.168.1.100", CONF_API_KEY: "test-key"},
    )
    existing_entry.add_to_hass(hass)

    # Try to add duplicate
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.my_device.config_flow.MyDeviceAPI"
    ) as mock_api_class:
        mock_api = AsyncMock()
        mock_api.async_test_connection.return_value = True
        mock_api.async_get_device_id.return_value = "device123"  # Same ID
        mock_api_class.return_value = mock_api

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_HOST: "192.168.1.200", CONF_API_KEY: "test-key"},
        )

    # Verify abort
    assert result["type"] == "abort"
    assert result["reason"] == "already_configured"
```

### Test Reauth Flow

```python
async def test_reauth_flow(hass: HomeAssistant):
    """Test reauth flow."""
    # Create existing entry
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_HOST: "192.168.1.100", CONF_API_KEY: "old-key"},
        unique_id="device123",
    )
    entry.add_to_hass(hass)

    # Start reauth
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": config_entries.SOURCE_REAUTH,
            "entry_id": entry.entry_id,
            "unique_id": entry.unique_id,
        },
        data=entry.data,
    )

    assert result["type"] == "form"
    assert result["step_id"] == "reauth_confirm"

    # Submit new credentials
    with patch(
        "custom_components.my_device.config_flow.MyDeviceAPI"
    ) as mock_api_class:
        mock_api = AsyncMock()
        mock_api.async_test_connection.return_value = True
        mock_api_class.return_value = mock_api

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_API_KEY: "new-key"},
        )

    # Verify entry updated
    assert result["type"] == "abort"
    assert result["reason"] == "reauth_successful"
    assert entry.data[CONF_API_KEY] == "new-key"
```

## Setup/Unload Testing

### Test Setup Entry

```python
"""Test __init__.py setup/unload."""
from unittest.mock import AsyncMock, patch

from homeassistant.const import CONF_HOST, CONF_API_KEY
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from tests.common import MockConfigEntry

from custom_components.my_device.const import DOMAIN


async def test_setup_entry(hass: HomeAssistant):
    """Test successful setup."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_HOST: "192.168.1.100", CONF_API_KEY: "test-key"},
    )
    entry.add_to_hass(hass)

    with patch(
        "custom_components.my_device.MyDeviceAPI"
    ) as mock_api_class:
        mock_api = AsyncMock()
        mock_api.async_test_connection.return_value = True
        mock_api.async_get_data.return_value = {"temperature": 22.5}
        mock_api_class.return_value = mock_api

        # Setup should succeed
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    # Verify entry loaded
    assert entry.state == "loaded"
    assert DOMAIN in hass.data


async def test_setup_entry_connection_error(hass: HomeAssistant):
    """Test setup fails on connection error."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_HOST: "192.168.1.100", CONF_API_KEY: "test-key"},
    )
    entry.add_to_hass(hass)

    with patch(
        "custom_components.my_device.MyDeviceAPI"
    ) as mock_api_class:
        mock_api = AsyncMock()
        mock_api.async_test_connection.side_effect = ConnectionError
        mock_api_class.return_value = mock_api

        # Setup should fail with ConfigEntryNotReady
        assert not await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    # Verify entry not loaded
    assert entry.state == "setup_retry"
```

### Test Unload Entry

```python
async def test_unload_entry(hass: HomeAssistant):
    """Test unloading entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_HOST: "192.168.1.100", CONF_API_KEY: "test-key"},
    )
    entry.add_to_hass(hass)

    with patch(
        "custom_components.my_device.MyDeviceAPI"
    ) as mock_api_class:
        mock_api = AsyncMock()
        mock_api.async_test_connection.return_value = True
        mock_api_class.return_value = mock_api

        # Setup
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        # Unload
        assert await hass.config_entries.async_unload(entry.entry_id)
        await hass.async_block_till_done()

    # Verify entry unloaded
    assert entry.state == "not_loaded"
    assert entry.entry_id not in hass.data[DOMAIN]
```

## Entity Testing

### Test Sensor Entity

```python
"""Test sensor platform."""
from unittest.mock import AsyncMock

from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from tests.common import MockConfigEntry

from custom_components.my_device.const import DOMAIN


async def test_sensor_entity(hass: HomeAssistant):
    """Test sensor entity creation."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_HOST: "192.168.1.100", CONF_API_KEY: "test-key"},
        unique_id="device123",
    )
    entry.add_to_hass(hass)

    with patch(
        "custom_components.my_device.MyDeviceAPI"
    ) as mock_api_class:
        mock_api = AsyncMock()
        mock_api.async_test_connection.return_value = True
        mock_api.async_get_data.return_value = {
            "temperature": 22.5,
            "humidity": 60,
        }
        mock_api_class.return_value = mock_api

        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    # Verify entities created
    entity_registry = er.async_get(hass)

    temp_entity = entity_registry.async_get("sensor.my_device_temperature")
    assert temp_entity
    assert temp_entity.unique_id == "device123_temperature"

    humidity_entity = entity_registry.async_get("sensor.my_device_humidity")
    assert humidity_entity
    assert humidity_entity.unique_id == "device123_humidity"

    # Verify states
    state = hass.states.get("sensor.my_device_temperature")
    assert state
    assert state.state == "22.5"

    state = hass.states.get("sensor.my_device_humidity")
    assert state
    assert state.state == "60"
```

### Test Entity Update

```python
async def test_sensor_update(hass: HomeAssistant):
    """Test sensor state updates."""
    entry = MockConfigEntry(...)
    entry.add_to_hass(hass)

    with patch(
        "custom_components.my_device.MyDeviceAPI"
    ) as mock_api_class:
        mock_api = AsyncMock()
        mock_api.async_get_data.return_value = {"temperature": 22.5}
        mock_api_class.return_value = mock_api

        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        # Initial state
        state = hass.states.get("sensor.my_device_temperature")
        assert state.state == "22.5"

        # Update data
        mock_api.async_get_data.return_value = {"temperature": 24.0}

        # Trigger update
        await hass.helpers.entity_component.async_update_entity(
            "sensor.my_device_temperature"
        )
        await hass.async_block_till_done()

        # Verify updated state
        state = hass.states.get("sensor.my_device_temperature")
        assert state.state == "24.0"
```

## Snapshot Testing

For complex outputs (diagnostics, entity states, etc.).

```python
from syrupy import SnapshotAssertion

async def test_entity_diagnostics(
    hass: HomeAssistant,
    snapshot: SnapshotAssertion,
):
    """Test entity diagnostics."""
    entry = MockConfigEntry(...)
    entry.add_to_hass(hass)

    with patch(
        "custom_components.my_device.MyDeviceAPI"
    ) as mock_api_class:
        mock_api = AsyncMock()
        mock_api.async_get_diagnostics.return_value = {
            "device_info": {...},
            "statistics": {...},
        }
        mock_api_class.return_value = mock_api

        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        # Get diagnostics
        diagnostics = await async_get_config_entry_diagnostics(hass, entry)

        # Compare with snapshot
        assert diagnostics == snapshot
```

**Update snapshots**:
```bash
pytest tests/components/my_device/ --snapshot-update
```

## Running Tests

### Run All Tests

```bash
# Run integration tests
pytest tests/components/my_device/

# With coverage report
pytest tests/components/my_device/ \
  --cov=homeassistant.components.my_device \
  --cov-report term-missing \
  -vv
```

### Run Specific Tests

```bash
# Config flow tests only
pytest tests/components/my_device/test_config_flow.py

# Single test
pytest tests/components/my_device/test_config_flow.py::test_user_flow_success
```

### Verify 100% Config Flow Coverage

```bash
pytest tests/components/my_device/test_config_flow.py \
  --cov=homeassistant.components.my_device.config_flow \
  --cov-report term-missing \
  -vv
```

**Required**: Must show 100% coverage for `config_flow.py`.

## Mocking Best Practices

### Mock External Libraries

```python
# ✅ GOOD - Mock at import location
with patch(
    "custom_components.my_device.config_flow.MyDeviceAPI"
) as mock_api_class:
    mock_api = AsyncMock()
    mock_api_class.return_value = mock_api
    ...

# ❌ BAD - Mock at library location (doesn't work)
with patch("my_device_lib.MyDeviceAPI") as mock:
    ...
```

### Use AsyncMock for Async Functions

```python
from unittest.mock import AsyncMock

# ✅ GOOD - AsyncMock for async functions
mock_api = AsyncMock()
mock_api.async_get_data.return_value = {"temperature": 22.5}

# ❌ BAD - Regular Mock for async (won't work)
mock_api = Mock()
mock_api.async_get_data.return_value = {"temperature": 22.5}
```

### Mock Side Effects

```python
# Exception on first call, success on second
mock_api.async_test_connection.side_effect = [
    ConnectionError("Offline"),
    True,
]

# Different return values
mock_api.async_get_data.side_effect = [
    {"temperature": 22.5},
    {"temperature": 24.0},
]
```

## Testing Checklist

**Bronze Tier (Minimum)**:
- ✅ 100% config flow test coverage (MANDATORY)
  - User flow success
  - Connection error
  - Authentication error
  - Unknown error
  - Duplicate entry
- ✅ Setup entry success
- ✅ Setup entry connection error
- ✅ Unload entry
- ✅ Entity creation
- ✅ Entity state correct

**Silver Tier**:
- ✅ Above +reauth flow
- ✅ Options flow
- ✅ Service action tests
- ✅ Error recovery tests
- ✅ 80%+ overall coverage

**Gold Tier**:
- ✅ Above + reconfigure flow
- ✅ Discovery flow tests
- ✅ Coordinator error handling
- ✅ Snapshot tests for diagnostics
- ✅ 90%+ overall coverage

**Platinum Tier**:
- ✅ Above + all edge cases
- ✅ Performance tests
- ✅ State restoration tests
- ✅ 95%+ overall coverage

## Common Testing Mistakes

1. **Not testing error paths**:
   ```python
   # ❌ BAD - Only tests success
   async def test_config_flow(hass):
       result = await setup_flow(hass)
       assert result["type"] == "create_entry"

   # ✅ GOOD - Tests all paths
   async def test_user_flow_success(hass): ...
   async def test_user_flow_cannot_connect(hass): ...
   async def test_user_flow_invalid_auth(hass): ...
   ```

2. **Using real API calls in tests**:
   ```python
   # ❌ BAD - Real API call
   api = MyDeviceAPI("192.168.1.100", "key")
   data = await api.async_get_data()

   # ✅ GOOD - Mocked API
   with patch(...) as mock_api_class:
       mock_api = AsyncMock()
       mock_api.async_get_data.return_value = {"temperature": 22.5}
   ```

3. **Not using MockConfigEntry**:
   ```python
   # ❌ BAD - Manual config entry creation
   entry = ConfigEntry(...)

   # ✅ GOOD - MockConfigEntry
   from tests.common import MockConfigEntry
   entry = MockConfigEntry(domain=DOMAIN, data={...})
   ```

4. **Forgetting async_block_till_done()**:
   ```python
   # ❌ BAD - State not updated yet
   await hass.config_entries.async_setup(entry.entry_id)
   state = hass.states.get("sensor.my_device")

   # ✅ GOOD - Wait for completion
   await hass.config_entries.async_setup(entry.entry_id)
   await hass.async_block_till_done()
   state = hass.states.get("sensor.my_device")
   ```

## Next Steps

- See [QUALITY_SCALE.md](QUALITY_SCALE.md) for coverage requirements by tier
- See [CONFIG_FLOW_GUIDE.md](CONFIG_FLOW_GUIDE.md) for config flow patterns
- See [COORDINATOR_GUIDE.md](COORDINATOR_GUIDE.md) for coordinator testing
