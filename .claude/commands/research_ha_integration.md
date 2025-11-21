# Research Home Assistant Integration

Research a Home Assistant integration thoroughly to understand its current implementation, identify issues, and plan improvements or refactoring work.

## Usage

```
/research_ha_integration <integration_name>
```

Example: `/research_ha_integration zwave_js`

---

## Research Protocol

When this command is invoked, conduct comprehensive research following this structured approach:

### 1. Integration Discovery (5-10 min)

**Locate the integration:**
- Path: `homeassistant/components/<integration_name>/`
- Verify integration exists

**Read manifest.json:**
- Integration type (device, hub, service, etc.)
- IoT class (cloud_polling, local_push, etc.)
- Config flow enabled?
- Dependencies and requirements
- Quality scale tier (if present)
- Codeowners

**Output:**
```
## Integration Overview
- **Name**: [from manifest]
- **Type**: [integration_type]
- **IoT Class**: [iot_class]
- **Config Flow**: [true/false]
- **Quality Tier**: [bronze/silver/gold/platinum/none]
- **Codeowners**: [list]
- **Dependencies**: [list]
```

---

### 2. Architecture Analysis (10-15 min)

**Read `__init__.py`:**
- Setup method (config entry vs YAML)
- Platform forwarding approach
- Runtime data structure
- Coordinator usage (if any)

**Identify platforms:**
- List all platform files (sensor.py, switch.py, etc.)
- Count entities per platform

**Check for coordinator:**
- Does it use DataUpdateCoordinator?
- Update interval
- Error handling approach

**Output:**
```
## Architecture
- **Setup Type**: [config_entry/yaml/both]
- **Platforms**: [list with entity counts]
- **Coordinator**: [yes/no - type if yes]
- **Runtime Data**: [structure description]
```

---

### 3. Config Flow Assessment (if applicable) (10-15 min)

**NOTE**: This step activates the `ha-config-flow-knowledge` Skill

If integration has config flow (`config_flow: true` in manifest):

**Read `config_flow.py`:**
- Flow steps implemented (user, zeroconf, ssdp, etc.)
- Unique ID handling
- Error handling patterns
- Reauthentication support
- Reconfiguration support
- Options flow

**Read `strings.json`:**
- Translation coverage
- Error message keys
- Step descriptions

**Reference**: ha-config-flow-knowledge Skill → Research docs section 2 (new) and section 1 (refactoring)

**Output:**
```
## Config Flow Analysis
- **Flows**: [list of async_step_* methods]
- **Unique ID**: [how it's set]
- **Error Handling**: [patterns used]
- **Reauth Support**: [yes/no]
- **Reconfig Support**: [yes/no]
- **Options Flow**: [yes/no]
- **Issues Found**:
  - [ ] [list any issues]
```

---

### 4. Entity Implementation Review (15-20 min)

**For each platform file, check:**
- `_attr_has_entity_name` usage
- Unique ID implementation
- Device info implementation
- Entity naming approach
- Update methods (polling vs coordinator)
- Availability handling

**Reference**: Research doc section 3 (Entity Implementation) and section 2 (Entity Refactoring)

**Output:**
```
## Entity Implementation
### [Platform Name]
- **Entity Count**: [approximate]
- **has_entity_name**: [yes/no/partial]
- **Unique IDs**: [yes/no - source if yes]
- **Device Info**: [yes/no]
- **Update Method**: [coordinator/polling/push]
- **Availability Handling**: [yes/no]
- **Issues Found**:
  - [ ] [list any issues]
```

---

### 5. Testing Coverage (10-15 min)

**Check `tests/components/<integration>/`:**
- Test files present
- Config flow tests (if applicable)
- Platform tests
- Coverage estimation

**Run coverage check** (if time permits):
```bash
pytest tests/components/<integration>/ --cov=homeassistant.components.<integration> --cov-report=term-missing
```

**Reference**: Research doc section 4 (Testing Requirements)

**Output:**
```
## Testing
- **Test Files**: [list]
- **Config Flow Tests**: [yes/no/partial]
- **Platform Tests**: [coverage summary]
- **Estimated Coverage**: [<90%/90-95%/>95%]
- **Issues Found**:
  - [ ] Missing config flow tests
  - [ ] Low coverage in [file]
  - [ ] [other issues]
```

---

### 6. Quality Scale Assessment (10 min)

**Check against quality tiers:**

**Bronze Tier (baseline):**
- [ ] Config flow with UI setup
- [ ] Entity unique IDs
- [ ] `has_entity_name = True`
- [ ] Runtime data usage
- [ ] Test before configure
- [ ] Test before setup
- [ ] Appropriate polling

**Silver Tier (reliability):**
- [ ] Reauthentication flow
- [ ] Entity unavailability marking
- [ ] Config entry unloading
- [ ] 90%+ test coverage
- [ ] Codeowners

**Gold Tier (user experience):**
- [ ] Device creation
- [ ] Discovery support
- [ ] Entity translations
- [ ] Reconfiguration flow
- [ ] Diagnostics platform

**Platinum Tier (excellence):**
- [ ] Async dependency
- [ ] Strict typing
- [ ] Inject websession

**Reference**: Research doc section 5 (Quality Scale) and section 3 (Quality Tier Upgrades)

**Output:**
```
## Quality Assessment
- **Current Tier**: [bronze/silver/gold/platinum/below-bronze]
- **Bronze Requirements**: [X/Y met]
- **Silver Requirements**: [X/Y met]
- **Gold Requirements**: [X/Y met]
- **Platinum Requirements**: [X/Y met]

### Gaps to Next Tier:
- [ ] [requirement 1]
- [ ] [requirement 2]
```

---

### 7. Refactoring Opportunities (10-15 min)

**Based on findings, identify:**

**Config Flow Improvements:**
- Add config flow if YAML-only
- Add reauthentication
- Add reconfiguration
- Improve error handling
- Add discovery

**Entity Modernization:**
- Add `has_entity_name`
- Add unique IDs
- Add device info
- Migrate to coordinator
- Fix availability handling

**Code Quality:**
- Migrate to runtime_data
- Update deprecated APIs
- Improve test coverage
- Add type hints

**Reference**: Refactoring doc sections 1-9

**Output:**
```
## Refactoring Opportunities

### High Priority
1. [Most critical improvement]
2. [Second critical improvement]

### Medium Priority
1. [Important but not critical]
2. [Another improvement]

### Low Priority
1. [Nice to have]
2. [Future enhancement]

### Estimated Effort
- **Quick wins** (<2h): [list]
- **Medium tasks** (2-8h): [list]
- **Large tasks** (>8h): [list]
```

---

### 8. Research Document References

**Point researcher to relevant sections:**

**For Config Flow Work:**
- New Integrations Doc → Section 2 (Configuration Flows)
- Refactoring Doc → Section 1 (Config Flow Refactoring)
- Refactoring Doc → Section 7 (Authentication Flows)

**For Entity Work:**
- New Integrations Doc → Section 3 (Entity Implementation)
- Refactoring Doc → Section 2 (Entity Refactoring Patterns)

**For Quality Upgrades:**
- New Integrations Doc → Section 5 (Quality Scale)
- Refactoring Doc → Section 3 (Quality Tier Upgrades)

**For Testing:**
- New Integrations Doc → Section 4 (Testing Requirements)
- Refactoring Doc → Section 8 (Testing Modernization)

---

## Final Summary Template

```markdown
# Research Summary: <integration_name>

## Quick Stats
- **Quality Tier**: [current tier]
- **Config Flow**: [yes/no]
- **Test Coverage**: [estimated %]
- **Platforms**: [count]
- **Critical Issues**: [count]

## Top 3 Improvements
1. [Most impactful change]
2. [Second priority]
3. [Third priority]

## Next Steps
1. [Immediate action]
2. [Follow-up action]
3. [Future consideration]

## Research Documents to Read
- [Specific section references based on work identified]

---
*Research completed: [timestamp]*
*Total time: [estimate]*
```

---

## Notes

- **Skills activated**: This command should trigger `ha-config-flow-knowledge`, `ha-entity-knowledge`, and `ha-common-mistakes` Skills automatically based on content
- **Research docs**: Always point to research document sections, not direct `docs/` files
- **Structured output**: Use the templates above for consistency
- **Time estimate**: 60-90 minutes for thorough research
- **Depth vs breadth**: Adjust based on integration complexity and research goals
