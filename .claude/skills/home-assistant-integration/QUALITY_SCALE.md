# Quality Scale Complete Guide (Phase 3)

The Home Assistant Quality Scale ensures integrations meet minimum standards and provides a clear progression path from Bronze to Platinum.

## Quality Tiers Overview

- **Bronze** - Minimum for core integrations (Phase 1 target)
- **Silver** - Enhanced quality (Phase 2 target)
- **Gold** - High quality
- **Platinum** - Highest quality
- **Legacy** - No config flow (deprecated, not accepted for new integrations)

**Start with Bronze** and progressively improve over time.

## Bronze Tier (Minimum Requirements)

Target for Phase 1 (MVP). All new integrations MUST meet Bronze tier.

### Requirements

**1. Config Flow** ✅
- UI-based setup (no YAML configuration)
- `"config_flow": true` in manifest.json
- User can add integration through UI

**2. Entity Unique IDs** ✅
- All entities have `unique_id` set
- Enables entity registry
- Allows user customization

**3. Entity Naming** ✅
- `has_entity_name = True` for all entities
- Device name handled separately
- No device type in entity names

**4. Device Class Support** ✅
- Entities use appropriate device classes
- Enables proper UI rendering
- Examples: `TEMPERATURE`, `HUMIDITY`, `POWER`

**5. Entity Category** ✅
- Diagnostic entities marked with `EntityCategory.DIAGNOSTIC`
- Config entities marked with `EntityCategory.CONFIG`
- Main features have no category

**6. Config Flow Test Coverage** ✅
- 100% test coverage for config_flow.py (MANDATORY)
- Tests for all error paths
- Duplicate entry prevention tested

**7. Type Hints** ✅
- Type hints throughout integration code
- Use `from __future__ import annotations` for forward references
- Helps with IDE support and code quality

### Bronze Checklist

```
✅ Config flow implemented with UI setup
✅ Config flow has 100% test coverage
✅ All entities have unique_id
✅ All entities use has_entity_name = True
✅ Device classes used where appropriate
✅ Entity categories used for diagnostic/config entities
✅ Type hints throughout code
✅ All API code in external PyPI library
✅ Requirements pinned in manifest.json
✅ Passes hassfest validation
✅ Passes pre-commit (ruff, etc.)
✅ No blocking calls in event loop
✅ Error handling: ConfigEntryNotReady, ConfigEntryAuthFailed
```

### Manifest.json for Bronze

```json
{
  "domain": "my_device",
  "name": "My Device",
  "codeowners": ["@myusername"],
  "config_flow": true,
  "dependencies": [],
  "documentation": "https://www.home-assistant.io/integrations/my_device",
  "integration_type": "device",
  "iot_class": "cloud_polling",
  "quality_scale": "bronze",
  "requirements": ["my-device-lib==1.0.0"]
}
```

## Silver Tier (Enhanced Quality)

Target for Phase 2 (Advanced features).

### Additional Requirements

**1. Test Coverage: 80%+** ✅
- Overall test coverage above 80%
- Beyond just config flow
- Entity tests, setup tests, service tests

**2. Diagnostics** ✅
- Implement `async_get_config_entry_diagnostics()`
- Provides debug information for troubleshooting
- Redact sensitive data

**3. Exception Translations** ✅
- Error messages translated in strings.json
- Config flow errors have translations
- Helpful user-facing messages

**4. Config Entry State Handling** ✅
- Proper handling of `ConfigEntryNotReady`
- Automatic retry with backoff
- Clear error messages

**5. Reconfiguration Flow** ✅
- `async_step_reconfigure` implemented
- Users can update settings without re-adding
- Tests for reconfigure flow

### Silver Checklist

```
✅ All Bronze tier requirements
✅ Test coverage above 80%
✅ Diagnostics implemented
✅ Exception translations in strings.json
✅ Config entry state properly handled
✅ Reconfigure flow implemented and tested
✅ Reauth flow implemented and tested (if applicable)
✅ Options flow for mutable settings (if applicable)
✅ DataUpdateCoordinator for polling (if applicable)
```

### Diagnostics Implementation

```python
"""Diagnostics support."""
from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

TO_REDACT = {"api_key", "token", "password", "serial_number"}

async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> dict:
    """Return diagnostics for config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    diagnostics_data = {
        "entry": {
            "title": entry.title,
            "data": dict(entry.data),
        },
        "device_info": coordinator.api.get_device_info(),
        "data": coordinator.data,
    }

    return async_redact_data(diagnostics_data, TO_REDACT)
```

### Manifest.json for Silver

```json
{
  "domain": "my_device",
  "name": "My Device",
  "codeowners": ["@myusername"],
  "config_flow": true,
  "dependencies": [],
  "documentation": "https://www.home-assistant.io/integrations/my_device",
  "integration_type": "device",
  "iot_class": "cloud_polling",
  "loggers": ["my_device_lib"],
  "quality_scale": "silver",
  "requirements": ["my-device-lib==1.0.0"]
}
```

## Gold Tier (High Quality)

Target for Phase 3 (Quality & Polish).

### Additional Requirements

**1. Test Coverage: 90%+** ✅
- Overall test coverage above 90%
- Comprehensive edge case testing
- Snapshot tests for complex outputs

**2. Strict Typing** ✅
- Full type hint coverage
- Listed in `.strict-typing` file
- Passes mypy strict mode

**3. Entity Translations** ✅
- Entity names translated in strings.json
- Supports internationalization
- Clear, descriptive names

**4. Device Handling** ✅
- Proper device info for all entities
- Device registry integration
- Via_device for hub-connected devices

**5. Stale Device Handling** ✅
- Removes devices no longer present
- Device removal in options/reconfigure flow
- Clean device registry

**6. Parallel Updates** ✅
- Uses `parallel_updates` semaphore if needed
- Prevents API rate limiting
- Coordinator handles this automatically

### Gold Checklist

```
✅ All Silver tier requirements
✅ Test coverage above 90%
✅ Strict typing (listed in .strict-typing)
✅ Entity translations in strings.json
✅ Device info for all entities
✅ Stale device cleanup implemented
✅ Parallel updates properly configured
✅ Comprehensive integration tests
✅ Snapshot tests for diagnostics
```

### Strict Typing Setup

**1. Add to .strict-typing file** (repository root):
```
homeassistant/components/my_device/*
```

**2. Ensure all functions/methods have type hints**:
```python
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up from config entry."""
    ...
```

**3. Run mypy**:
```bash
mypy homeassistant/components/my_device/
```

### Entity Translations

**strings.json**:
```json
{
  "config": {
    "step": {
      "user": {
        "title": "Set up My Device",
        "description": "Enter your device credentials",
        "data": {
          "host": "Host",
          "api_key": "API Key"
        }
      }
    },
    "error": {
      "cannot_connect": "Failed to connect",
      "invalid_auth": "Invalid authentication",
      "unknown": "Unexpected error occurred"
    }
  },
  "entity": {
    "sensor": {
      "temperature": {
        "name": "Temperature"
      },
      "humidity": {
        "name": "Humidity"
      },
      "battery": {
        "name": "Battery"
      }
    }
  }
}
```

### Manifest.json for Gold

```json
{
  "domain": "my_device",
  "name": "My Device",
  "codeowners": ["@myusername"],
  "config_flow": true,
  "dependencies": [],
  "documentation": "https://www.home-assistant.io/integrations/my_device",
  "integration_type": "device",
  "iot_class": "cloud_polling",
  "loggers": ["my_device_lib"],
  "quality_scale": "gold",
  "requirements": ["my-device-lib==1.0.0"]
}
```

## Platinum Tier (Highest Quality)

The pinnacle of integration quality.

### Additional Requirements

**1. Test Coverage: 95%+** ✅
- Near-complete test coverage
- All edge cases tested
- Performance tests

**2. All Quality Rules** ✅
- Every single quality scale rule satisfied
- Perfect implementation
- Exemplary code

**3. Comprehensive Documentation** ✅
- Detailed integration documentation
- Code examples
- Troubleshooting guides

**4. Best Practices Everywhere** ✅
- Follows all Home Assistant patterns
- No shortcuts or workarounds
- Clean, maintainable code

### Platinum Checklist

```
✅ All Gold tier requirements
✅ Test coverage above 95%
✅ All quality scale rules satisfied
✅ Comprehensive documentation on home-assistant.io
✅ No open quality-related issues
✅ Active maintenance and updates
✅ Responsive to bug reports
✅ Community contributions welcome
```

### Manifest.json for Platinum

```json
{
  "domain": "my_device",
  "name": "My Device",
  "codeowners": ["@myusername", "@contributor"],
  "config_flow": true,
  "dependencies": [],
  "documentation": "https://www.home-assistant.io/integrations/my_device",
  "integration_type": "device",
  "iot_class": "cloud_polling",
  "loggers": ["my_device_lib"],
  "quality_scale": "platinum",
  "requirements": ["my-device-lib==1.0.0"]
}
```

## Progression Path

### Phase 1 → Bronze

1. Implement basic config flow
2. Add unique IDs to entities
3. Use `has_entity_name = True`
4. Add type hints
5. Write config flow tests (100% coverage)
6. Pass all validation (hassfest, pre-commit)

**Estimated time**: 1-2 weeks for new integration

### Bronze → Silver

1. Implement diagnostics
2. Add reconfigure flow
3. Add reauth flow (if applicable)
4. Expand test coverage to 80%+
5. Translate error messages

**Estimated time**: 1 week

### Silver → Gold

1. Add entity translations
2. Expand test coverage to 90%+
3. Add strict typing
4. Implement stale device cleanup
5. Add snapshot tests

**Estimated time**: 1-2 weeks

### Gold → Platinum

1. Expand test coverage to 95%+
2. Write comprehensive documentation
3. Address all quality issues
4. Add performance optimizations
5. Engage with community

**Estimated time**: 2-4 weeks

## Quality Scale Rules Reference

See official documentation for complete list:
- https://developers.home-assistant.io/docs/core/integration-quality-scale

**Key rules**:
1. Config flow (Bronze+)
2. Unique IDs (Bronze+)
3. has_entity_name (Bronze+)
4. Device class (Bronze+)
5. Entity category (Bronze+)
6. 100% config flow coverage (Bronze+)
7. Type hints (Bronze+)
8. 80%+ coverage (Silver+)
9. Diagnostics (Silver+)
10. Reconfigure flow (Silver+)
11. 90%+ coverage (Gold+)
12. Strict typing (Gold+)
13. Entity translations (Gold+)
14. 95%+ coverage (Platinum+)

## Verification Commands

```bash
# Run hassfest (validates manifest, codeowners)
python3 -m script.hassfest

# Run code formatting
ruff format homeassistant/components/my_device/

# Run all linters
pre-commit run --all-files

# Run tests with coverage
pytest tests/components/my_device/ \
  --cov=homeassistant.components.my_device \
  --cov-report term-missing \
  -vv

# Verify 100% config flow coverage (Bronze requirement)
pytest tests/components/my_device/test_config_flow.py \
  --cov=homeassistant.components.my_device.config_flow \
  --cov-report term-missing

# Run type checking (Gold requirement)
mypy homeassistant/components/my_device/
```

## Common Upgrade Blockers

### Bronze → Silver

**Issue**: Test coverage below 80%
**Solution**: Add tests for:
- Entity state updates
- Service actions
- Options flow
- Error recovery

**Issue**: No diagnostics
**Solution**: Implement `async_get_config_entry_diagnostics()`

### Silver → Gold

**Issue**: Test coverage below 90%
**Solution**: Add tests for:
- Edge cases
- State restoration
- Device removal
- All entity types

**Issue**: Type hints incomplete
**Solution**:
- Add type hints to all functions/methods
- Add to `.strict-typing`
- Fix mypy errors

### Gold → Platinum

**Issue**: Test coverage below 95%
**Solution**: Test every code path, including:
- Exception handlers
- Rare edge cases
- Performance scenarios

**Issue**: Quality rules not satisfied
**Solution**: Review quality scale docs and address each rule

## Tips for Quality Progression

1. **Start with Bronze**: Get working integration first
2. **Iterate incrementally**: Don't jump tiers
3. **Test as you go**: Write tests alongside features
4. **Use templates**: Copy patterns from high-quality integrations
5. **Ask for reviews**: Get feedback from community
6. **Monitor coverage**: Use coverage reports to find gaps
7. **Read quality docs**: Stay updated on requirements
8. **Be patient**: Quality takes time

## Next Steps

- See [TESTING_GUIDE.md](TESTING_GUIDE.md) for test coverage strategies
- See [CONFIG_FLOW_GUIDE.md](CONFIG_FLOW_GUIDE.md) for reauth/reconfigure flows
- See [ENTITY_GUIDE.md](ENTITY_GUIDE.md) for entity translations
- See [COORDINATOR_GUIDE.md](COORDINATOR_GUIDE.md) for DataUpdateCoordinator patterns
