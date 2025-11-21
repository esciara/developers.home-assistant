# Extension System Workflow Optimization Plan v2

**Created:** 2025-11-21
**Target:** Home Assistant Integration Development
**Scope:** Optimize Claude Code workflow using native Skills, Commands, and Sub-agents
**Supersedes:** v1 (replaced thoughts/ approach with Skills)

---

## Executive Summary

This plan enhances the Claude Code workflow (research → plan → implement) for extension-based systems like Home Assistant integrations using **100% Claude Code native features**:

- **Skills**: Knowledge base (patterns, templates, checklists) - auto-invoked by Claude
- **Commands**: Workflow orchestration (research, plan, implement) - user-invoked
- **Sub-agents**: Complex execution tasks (validation, analysis) - tool-invoked

Benefits:
- **Auto-discovery**: Claude uses Skills automatically when context matches
- **Progressive disclosure**: Only loads what's needed
- **Git-native**: All in `.claude/` directory, version controlled
- **Team sharing**: Instant availability via git pull

---

## Architecture Overview

```
.claude/
├── skills/              # Knowledge base (auto-invoked)
│   ├── ha-integration-structure/
│   ├── ha-entity-knowledge/
│   ├── ha-config-flow-knowledge/
│   ├── ha-coordinator-knowledge/
│   └── ha-common-mistakes/
│
├── commands/            # Workflows (user-invoked)
│   ├── research_ha_integration.md
│   ├── create_plan_ha_integration.md
│   └── implement_plan_ha_integration.md
│
└── agents/              # Complex tasks (tool-invoked)
    └── ha-integration-validator.md
```

**How they work together:**

1. User invokes: `/research_ha_integration`
2. Command activates relevant Skills: `ha-integration-structure`, `ha-entity-knowledge`
3. Claude uses Skills' patterns/templates automatically
4. Command may launch sub-agents for complex analysis
5. Skills provide context throughout entire workflow

---

## Phase 1: Knowledge Skills Foundation

**Objective:** Create Skills containing patterns, templates, and checklists

**Duration:** 10-14 hours

### 1.1 Integration Structure Skill

**Location:** `.claude/skills/ha-integration-structure/`

**Files:**
```
ha-integration-structure/
├── SKILL.md                    # Main skill definition
├── required-files.md           # manifest.json, __init__.py, etc.
├── optional-files.md           # config_flow.py, strings.json, etc.
├── directory-layout.md         # File organization patterns
├── templates/
│   ├── manifest.json           # Minimal manifest template
│   ├── manifest-full.json      # Complete manifest with all fields
│   ├── __init__.py             # Basic __init__ template
│   └── __init__-platforms.py  # __init__ with platform setup
├── examples/
│   ├── template-integration.md # Simplest integration structure
│   └── met-integration.md      # Medium complexity example
└── checklists/
    ├── required-files.md       # Checklist of required files
    └── manifest-fields.md      # Manifest field checklist
```

**SKILL.md template:**
```yaml
---
name: ha-integration-structure
description: Home Assistant integration architecture, file structure, manifest.json, __init__.py patterns. Use when creating new HA integrations, planning integration structure, or understanding integration organization.
allowed-tools: Read, Grep, Glob
---

# Home Assistant Integration Structure

I provide expertise on HA integration architecture and file organization.

## What I Know

**Required Files:**
- manifest.json - Integration metadata
- __init__.py - Component initialization
- strings.json - UI text (for config flows)

**Optional Files:**
- config_flow.py - UI configuration
- {platform}.py - Entity implementations (sensor, switch, etc.)
- services.yaml - Service definitions
- const.py - Constants

See [required-files.md](required-files.md) for detailed requirements.

## File Organization Patterns

Home Assistant integrations follow strict conventions:
```
homeassistant/components/{domain}/
├── manifest.json        # REQUIRED
├── __init__.py          # REQUIRED
├── strings.json         # Required for config flows
├── config_flow.py       # For UI configuration
├── sensor.py            # Sensor platform
├── switch.py            # Switch platform
└── const.py             # Constants
```

See [directory-layout.md](directory-layout.md) for patterns.

## Templates

Use these as starting points:
- [manifest.json](templates/manifest.json) - Minimal manifest
- [manifest-full.json](templates/manifest-full.json) - All fields
- [__init__.py](templates/__init__.py) - Basic setup
- [__init__-platforms.py](templates/__init__-platforms.py) - Multi-platform

## Real Integration Examples

Study these proven structures:
- [template integration](examples/template-integration.md) - Simplest (no external deps)
- [met integration](examples/met-integration.md) - Medium (API + coordinator)

## Checklists

Before implementing:
- [ ] Review [required-files.md](checklists/required-files.md)
- [ ] Review [manifest-fields.md](checklists/manifest-fields.md)

## When to Use This Skill

- Planning a new integration
- Understanding integration organization
- Validating file structure
- Creating manifest.json
- Setting up __init__.py
```

**Key Documents:**

1. **required-files.md**: Document what files are mandatory and why
2. **optional-files.md**: When to use config_flow, services, etc.
3. **directory-layout.md**: Naming conventions, imports, organization
4. **templates/**: Working code templates for common files
5. **examples/**: References to 2-3 real integrations with explanations
6. **checklists/**: Quick validation lists

### 1.2 Entity Knowledge Skill

**Location:** `.claude/skills/ha-entity-knowledge/`

**Files:**
```
ha-entity-knowledge/
├── SKILL.md                    # Main skill definition
├── entity-base-classes.md      # All entity types and their bases
├── unique-id-patterns.md       # Critical: stable unique ID strategies
├── device-info-patterns.md     # Device registration patterns
├── state-conventions.md        # State and attributes conventions
├── entity-naming.md            # Naming conventions (entity_id, name, etc.)
├── templates/
│   ├── sensor-basic.py         # Minimal sensor
│   ├── sensor-coordinator.py  # Sensor with coordinator
│   ├── climate-basic.py        # Climate entity
│   ├── switch-basic.py         # Switch entity
│   └── entity-platform.py      # Platform setup function
├── examples/
│   ├── template-sensor.md      # Reference: template integration
│   ├── met-sensor.md           # Reference: met integration
│   └── random-sensor.md        # Reference: random integration
└── checklists/
    ├── entity-requirements.md  # What every entity needs
    └── unique-id-validation.md # Ensuring stable unique IDs
```

**SKILL.md focus:**
- Entity base classes (SensorEntity, ClimateEntity, etc.)
- Unique ID generation (most critical!)
- Device info patterns
- State and attribute conventions
- Property overrides

**Description trigger words:** "entity", "sensor", "switch", "climate", "unique ID", "device info", "state", "attributes"

### 1.3 Config Flow Knowledge Skill

**Location:** `.claude/skills/ha-config-flow-knowledge/`

**Files:**
```
ha-config-flow-knowledge/
├── SKILL.md                    # Main skill definition
├── config-flow-basics.md       # ConfigFlow class, step methods
├── error-handling.md           # Error types and handling
├── user-flow-pattern.md        # async_step_user implementation
├── reauth-flow-pattern.md      # Re-authentication flows
├── options-flow-pattern.md     # async_get_options_flow
├── discovery-patterns.md       # DHCP, SSDP, Zeroconf discovery
├── templates/
│   ├── config_flow-basic.py    # Simple user input flow
│   ├── config_flow-auth.py     # With authentication
│   ├── config_flow-options.py  # With options flow
│   └── strings.json            # Matching strings file
├── examples/
│   ├── openweathermap-flow.md  # API key + location
│   └── met-flow.md             # Location only
└── checklists/
    ├── config-flow-steps.md    # All required methods
    └── error-handling.md       # Common errors to handle
```

**SKILL.md focus:**
- Step-based flows
- Schema definitions
- Error handling (show_form with errors)
- Options flows
- Re-authentication

**Description trigger words:** "config flow", "configuration", "UI setup", "user input", "authentication", "options", "reauth"

### 1.4 Coordinator Knowledge Skill

**Location:** `.claude/skills/ha-coordinator-knowledge/`

**Files:**
```
ha-coordinator-knowledge/
├── SKILL.md                        # Main skill definition
├── coordinator-basics.md           # DataUpdateCoordinator overview
├── update-method-pattern.md        # async _async_update_data
├── coordinator-entity-pattern.md   # CoordinatorEntity integration
├── error-handling.md               # UpdateFailed exceptions
├── auth-refresh-pattern.md         # Token refresh in coordinator
├── templates/
│   ├── coordinator-basic.py        # Simple polling coordinator
│   ├── coordinator-auth.py         # With auth refresh
│   ├── entity-coordinator.py       # CoordinatorEntity usage
│   └── __init__-coordinator.py     # Setup with coordinator
├── examples/
│   ├── met-coordinator.md          # Simple weather API
│   └── openweathermap-coordinator.md # With auth
└── checklists/
    ├── coordinator-setup.md        # Proper initialization
    └── error-handling.md           # What to catch and when
```

**SKILL.md focus:**
- When to use coordinators vs direct polling
- Update intervals
- Error handling and recovery
- CoordinatorEntity base class
- Authentication refresh

**Description trigger words:** "coordinator", "DataUpdateCoordinator", "polling", "update", "refresh", "CoordinatorEntity"

### 1.5 Common Mistakes Skill

**Location:** `.claude/skills/ha-common-mistakes/`

**Files:**
```
ha-common-mistakes/
├── SKILL.md                    # Main skill definition (anti-patterns)
├── blocking-io.md              # Async/await pitfalls
├── unique-id-instability.md    # Unstable unique IDs
├── missing-error-handling.md   # Unhandled exceptions
├── incorrect-device-info.md    # Device info issues
├── hardcoded-values.md         # Constants, intervals, etc.
├── testing-mistakes.md         # Common test issues
└── examples/
    ├── blocking-io-bad.py      # Wrong way
    ├── blocking-io-good.py     # Right way
    ├── unique-id-bad.py        # Wrong way
    └── unique-id-good.py       # Right way
```

**SKILL.md focus:**
- Common anti-patterns
- What NOT to do
- Side-by-side comparisons (bad vs good)
- How to fix common issues

**Description trigger words:** "error", "issue", "problem", "not working", "fails", "mistake", "wrong"

### Success Criteria (Phase 1)

- ✅ Five knowledge Skills created with complete SKILL.md
- ✅ Each Skill has 3-5 supporting documents
- ✅ Each Skill has 2-3 templates
- ✅ Each Skill has 2-3 real integration examples
- ✅ Descriptions trigger correctly (test with sample questions)
- ✅ All files committed to `.claude/skills/`

**Testing:** Ask Claude questions like:
- "How do I create a sensor entity?" → Should activate ha-entity-knowledge
- "I need to add a config flow" → Should activate ha-config-flow-knowledge
- "What files does an integration need?" → Should activate ha-integration-structure

### Estimated Effort: 10-14 hours

---

## Phase 2: Specialized Commands

**Objective:** Create HA-specific workflow commands that leverage Skills

**Duration:** 6-8 hours

### 2.1 Research Command

**File:** `.claude/commands/research_ha_integration.md`

**Structure:**
```yaml
---
description: Research Home Assistant integration with domain expertise
---

# Research Home Assistant Integration

[Inherits from: research_codebase_generic.md]

## Pre-Research: Activate Knowledge Skills

Before starting general research, explicitly use these Skills:
- **ha-integration-structure**: Understand overall architecture
- **ha-entity-knowledge**: If entity platforms exist
- **ha-config-flow-knowledge**: If config_flow.py exists
- **ha-coordinator-knowledge**: If coordinator pattern is used

## HA-Specific Research Protocol

### Step 1: Core Files Analysis

1. **Read manifest.json** first:
   ```bash
   Read homeassistant/components/{domain}/manifest.json
   ```
   Extract:
   - Domain name
   - Dependencies (libraries, other integrations)
   - Requirements (PyPI packages)
   - Config flow status
   - Documentation URL

2. **Read __init__.py**:
   ```bash
   Read homeassistant/components/{domain}/__init__.py
   ```
   Identify:
   - Setup type (async_setup, async_setup_entry)
   - PLATFORMS list (if present)
   - Config schema (if YAML)
   - Services registered

3. **Check for config_flow.py**:
   ```bash
   Read homeassistant/components/{domain}/config_flow.py
   ```
   If exists → UI configuration
   If not → YAML configuration

4. **List all platform files**:
   ```bash
   Glob homeassistant/components/{domain}/*.py
   ```

### Step 2: Pattern Recognition

Use Skills to identify patterns:

**For entities** (sensor.py, switch.py, etc.):
- What base class? (use ha-entity-knowledge)
- How are unique IDs generated?
- Is device info provided?
- What state attributes?

**For data updates**:
- Is DataUpdateCoordinator used? (use ha-coordinator-knowledge)
- What's the update interval?
- How are errors handled?

**For configuration**:
- Step-based flow? (use ha-config-flow-knowledge)
- What user inputs?
- What validation?

### Step 3: Find Reference Integrations

Search for similar integrations:
```bash
# By similar API/protocol
Grep "similar_library_name" homeassistant/components/*/manifest.json

# By similar entity types
Glob homeassistant/components/*/sensor.py (if sensor integration)

# By similar complexity
[Use Skills' examples/ directories for references]
```

### Step 4: Check Tests

```bash
Glob tests/components/{domain}/**/*.py
```

Look for:
- Test fixtures
- Mock patterns
- Test coverage areas

### Step 5: Document Findings

Create research document with:

#### Integration Overview
- Domain: {name}
- Type: {cloud polling/local push/hub}
- Configuration: {UI/YAML}
- Platforms: {list}

#### Architecture
- Uses coordinator: {yes/no}
- Has config flow: {yes/no}
- Device support: {yes/no}
- External dependencies: {list}

#### Reference Integration
- Most similar: {integration name}
- Why similar: {reason}
- Key patterns to reuse: {list}

#### Key Files Found
- manifest.json: {summary}
- __init__.py: {summary}
- Platform files: {list with summaries}

#### Patterns Identified
- Entity base classes: {list}
- Unique ID pattern: {describe}
- Update pattern: {coordinator/polling/push}
- Error handling: {approach}

#### Questions/Clarifications Needed
{Any unclear aspects}

## Skills Usage

Throughout research, reference:
- ha-integration-structure: For file organization questions
- ha-entity-knowledge: For entity implementation questions
- ha-config-flow-knowledge: For config flow questions
- ha-coordinator-knowledge: For update coordinator questions
- ha-common-mistakes: To identify potential issues

## Output

Save research to: `plans/{domain}-research.md`
```

**Key Enhancements:**
- Explicitly activates relevant Skills
- HA-specific search patterns
- Structured output format
- References Skills throughout

### 2.2 Planning Command

**File:** `.claude/commands/create_plan_ha_integration.md`

**Structure:**
```yaml
---
description: Create implementation plan for Home Assistant integration
---

# Create Plan for Home Assistant Integration

[Inherits from: create_plan_generic.md]

## Pre-Planning: Review Skills

Ensure you've reviewed:
- ha-integration-structure: Overall architecture
- ha-entity-knowledge: Entity patterns
- ha-config-flow-knowledge: If UI configuration needed
- ha-coordinator-knowledge: If polling/updating data

## HA Integration Plan Template

### 1. Integration Specification

**Domain:** {domain_name}

**Type:**
- [ ] Cloud API (polling)
- [ ] Local API (polling)
- [ ] Local API (push/webhook)
- [ ] Hub integration

**Configuration Method:**
- [ ] Config flow (UI)
- [ ] YAML only
- [ ] Both

**Entity Platforms:**
- [ ] sensor
- [ ] switch
- [ ] climate
- [ ] binary_sensor
- [ ] light
- [ ] Other: _____

**External Dependencies:**
- PyPI packages: {list}
- Other integrations: {list}

### 2. Architecture Decisions

**Data Update Strategy:**
- [ ] DataUpdateCoordinator (recommended for polling)
- [ ] Direct polling per entity (simple cases only)
- [ ] Push/event-based (webhooks, MQTT, etc.)

**Update Interval:** {e.g., 30 seconds}
**Justification:** {why this interval}

**Authentication:**
- [ ] API key
- [ ] Username/password
- [ ] OAuth
- [ ] Token (with refresh)
- [ ] None

**Device Model:**
- [ ] One device, multiple entities
- [ ] Multiple devices
- [ ] No devices (service-based)

**Error Handling Strategy:**
{How errors will be handled at each layer}

### 3. File Structure

List all files to create/modify:

**Required Files:**
- [ ] `manifest.json`
  - Purpose: Integration metadata
  - Key fields: domain, name, documentation, requirements, dependencies
- [ ] `__init__.py`
  - Purpose: Integration setup, coordinator initialization
  - Key functions: async_setup_entry, async_unload_entry
- [ ] `strings.json` (if config flow)
  - Purpose: UI text
  - Sections: config, options, errors

**Platform Files:**
- [ ] `sensor.py` (if sensor platform)
  - Purpose: Sensor entities
  - Entities: {list entity types}
- [ ] `{platform}.py` (for each platform)
  - Purpose: {describe}

**Optional Files:**
- [ ] `config_flow.py` (if UI configuration)
  - Purpose: Configuration UI
  - Steps: user, {other steps}
- [ ] `const.py`
  - Purpose: Constants, enums
- [ ] `coordinator.py` (if complex coordinator)
  - Purpose: Data update coordination
- [ ] `services.yaml` (if services)
  - Purpose: Service definitions

### 4. Implementation Pattern

**Reference Integration:** {name}
**Why this reference:** {similarity explanation}

**Patterns to Reuse:**
- Coordinator pattern from: {reference}
- Config flow pattern from: {reference}
- Entity structure from: {reference}

**Deviations from Standard:**
{Any non-standard approaches and why}

### 5. Detailed Design

#### 5.1 manifest.json Specification

```json
{
  "domain": "{domain}",
  "name": "{human readable name}",
  "codeowners": ["{github_username}"],
  "config_flow": {true/false},
  "documentation": "https://www.home-assistant.io/integrations/{domain}",
  "requirements": ["{package==version}"],
  "dependencies": [],
  "iot_class": "{cloud_polling/local_polling/local_push/cloud_push}"
}
```

**Validation:** Use ha-integration-structure Skill

#### 5.2 Coordinator Design (if applicable)

**Class:** `{Name}Coordinator(DataUpdateCoordinator)`

**Update Method:** `_async_update_data()`
- API calls: {describe}
- Data transformation: {describe}
- Error handling: {what exceptions to catch}

**Update Interval:** `UPDATE_INTERVAL = timedelta(seconds={value})`

**Reference:** Use ha-coordinator-knowledge Skill templates

#### 5.3 Config Flow Design (if applicable)

**Steps:**
1. `async_step_user`: {what user provides}
2. `async_step_{other}`: {if multi-step}

**Validation:**
- {what to validate}
- {how to validate}

**Errors:**
- `invalid_auth`: {when}
- `cannot_connect`: {when}
- `{custom}`: {when}

**Reference:** Use ha-config-flow-knowledge Skill templates

#### 5.4 Entity Designs

For each entity type:

**{Entity Type} Entities:**

| Entity | unique_id | Name | State | Attributes |
|--------|-----------|------|-------|------------|
| {name} | {pattern} | {display} | {state_value} | {attr_list} |

**Base Class:** {SensorEntity/SwitchEntity/etc.}

**Unique ID Pattern:** `{describe stable unique ID generation}`
- Must be stable across restarts ✓
- Must be unique per device/entity ✓

**Device Info:**
```python
{
  "identifiers": {(DOMAIN, {unique_device_id})},
  "name": {device_name},
  "manufacturer": {manufacturer},
  "model": {model},
  "sw_version": {version}
}
```

**Reference:** Use ha-entity-knowledge Skill templates

#### 5.5 Error Handling

**Coordinator Level:**
- `UpdateFailed`: {when to raise}
- `ConfigEntryAuthFailed`: {when to raise}

**Entity Level:**
- `available` property: {when False}

**Config Flow Level:**
- Error types: {list}
- User messaging: {how shown}

### 6. Testing Strategy

**Unit Tests:**
- [ ] Test coordinator update logic
- [ ] Test entity state calculations
- [ ] Test config flow steps
- [ ] Test error handling

**Integration Tests:**
- [ ] Test full setup flow
- [ ] Test coordinator refresh
- [ ] Test entity creation
- [ ] Test config flow end-to-end

**Manual Testing:**
- [ ] Add integration via UI
- [ ] Verify entities created
- [ ] Check entity states update
- [ ] Test error scenarios
- [ ] Verify logs clean

### 7. Validation Checklist

**Pre-Implementation Validation:**

Use ha-integration-structure checklist:
- [ ] All required files planned
- [ ] Manifest complete and valid
- [ ] Update strategy chosen
- [ ] Reference integration identified

Use ha-entity-knowledge checklist:
- [ ] Unique ID strategy defined and stable
- [ ] Device info planned (if applicable)
- [ ] Entity naming follows conventions
- [ ] Base classes correct

Use ha-config-flow-knowledge checklist (if config flow):
- [ ] All steps defined
- [ ] Error handling complete
- [ ] Strings file planned

Use ha-coordinator-knowledge checklist (if coordinator):
- [ ] Update method defined
- [ ] Error handling planned
- [ ] Update interval appropriate

**Post-Implementation Validation:**
- [ ] `python3 -m script.hassfest validate`
- [ ] `pytest tests/components/{domain}/`
- [ ] `mypy homeassistant/components/{domain}/`
- [ ] `pylint homeassistant/components/{domain}/`
- [ ] Manual smoke test

### 8. Success Criteria

**Functional:**
- [ ] Integration loads without errors
- [ ] Config flow works (if applicable)
- [ ] Entities appear in HA
- [ ] Entity states update correctly
- [ ] Error handling works as designed

**Quality:**
- [ ] All tests pass
- [ ] Type checking passes
- [ ] Linting passes
- [ ] No blocking I/O in async context
- [ ] Unique IDs stable across restarts

**Documentation:**
- [ ] Code comments clear
- [ ] Docstrings present
- [ ] strings.json complete

### 9. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Unstable unique IDs | High | Review pattern with ha-entity-knowledge |
| API rate limits | Medium | Appropriate update interval |
| Authentication failures | Medium | Robust error handling with reauth |
| {custom risk} | {impact} | {mitigation} |

### 10. Implementation Order

Recommended sequence:

1. **Foundation**
   - [ ] Create manifest.json
   - [ ] Create const.py (constants)
   - [ ] Create __init__.py (basic structure)

2. **Configuration**
   - [ ] Create config_flow.py (if needed)
   - [ ] Create strings.json (if config flow)
   - [ ] Test config flow

3. **Data Layer**
   - [ ] Create coordinator.py (if needed)
   - [ ] Implement update logic
   - [ ] Test coordinator

4. **Entities**
   - [ ] Create platform files (sensor.py, etc.)
   - [ ] Implement entities
   - [ ] Test entities

5. **Polish**
   - [ ] Add error handling
   - [ ] Add logging
   - [ ] Add tests
   - [ ] Run validation

## Skills Integration

Throughout planning:
- Reference Skills' templates/ for code structure
- Reference Skills' examples/ for proven patterns
- Reference Skills' checklists/ for validation
- Use ha-common-mistakes to avoid pitfalls

## Output

Save plan to: `plans/{domain}-implementation-plan.md`
```

**Key Enhancements:**
- HA-specific plan structure
- References all relevant Skills
- Built-in validation checklists
- Clear success criteria

### 2.3 Implementation Command

**File:** `.claude/commands/implement_plan_ha_integration.md`

**Structure:**
```yaml
---
description: Implement Home Assistant integration from plan
---

# Implement Home Assistant Integration

[Inherits from: implement_plan.md]

## Pre-Implementation Setup

### 1. Validate Plan

Load plan from: `plans/{domain}-implementation-plan.md`

Check plan completeness:
- [ ] All required sections present
- [ ] Architecture decisions made
- [ ] File structure defined
- [ ] Reference integration identified
- [ ] Validation criteria specified

### 2. Activate Knowledge Skills

Ensure these Skills are available:
- ha-integration-structure (for file organization)
- ha-entity-knowledge (for entity implementation)
- ha-config-flow-knowledge (if config flow needed)
- ha-coordinator-knowledge (if coordinator needed)
- ha-common-mistakes (to avoid issues)

### 3. Setup Workspace

```bash
cd homeassistant/components/
mkdir -p {domain}
cd {domain}
```

## Implementation Protocol

### Phase 1: Foundation Files

#### Step 1.1: Create manifest.json

Use template from ha-integration-structure Skill:
```bash
Read .claude/skills/ha-integration-structure/templates/manifest.json
```

Adapt template to plan specifications.

**Validate immediately:**
```bash
python3 -m script.hassfest validate --integration {domain}
```

If errors: Fix before proceeding.

#### Step 1.2: Create const.py

Create constants:
- DOMAIN
- UPDATE_INTERVAL (if coordinator)
- DEFAULT_NAME
- API endpoints/constants

**Reference:** ha-integration-structure patterns

#### Step 1.3: Create __init__.py

**If using coordinator:**
Use template: ha-integration-structure/templates/__init__-platforms.py

**If not using coordinator:**
Use template: ha-integration-structure/templates/__init__.py

Key functions:
- `async_setup_entry(hass, entry)`
- `async_unload_entry(hass, entry)`

**Validate:**
```bash
python3 -c "import homeassistant.components.{domain}"
```

### Phase 2: Configuration (if needed)

#### Step 2.1: Create config_flow.py

Use template from ha-config-flow-knowledge Skill:
```bash
Read .claude/skills/ha-config-flow-knowledge/templates/config_flow-basic.py
```

Implement steps from plan:
- `async_step_user`
- Error handling
- Validation

**Reference:** ha-config-flow-knowledge patterns

#### Step 2.2: Create strings.json

Use template from ha-config-flow-knowledge Skill.

Match all config flow steps and errors.

**Validate:**
```bash
python3 -m script.hassfest validate --integration {domain}
```

#### Step 2.3: Test Config Flow

Before proceeding, verify config flow works:
- Syntax is valid
- Imports resolve
- No obvious errors

### Phase 3: Data Layer (if coordinator)

#### Step 3.1: Create coordinator.py (or add to __init__.py)

Use template from ha-coordinator-knowledge Skill:
```bash
Read .claude/skills/ha-coordinator-knowledge/templates/coordinator-basic.py
```

Implement:
- `_async_update_data()` method
- Error handling
- Authentication (if needed)

**Key checks** (use ha-common-mistakes):
- [ ] No blocking I/O in async methods
- [ ] Proper exception handling
- [ ] UpdateFailed raised on errors
- [ ] ConfigEntryAuthFailed for auth errors

#### Step 3.2: Test Coordinator Logic

Create minimal test:
```python
# Verify coordinator can be instantiated
# Verify update method can be called
```

### Phase 4: Entity Platforms

For each platform (sensor, switch, etc.):

#### Step 4.1: Create {platform}.py

Use template from ha-entity-knowledge Skill:
```bash
Read .claude/skills/ha-entity-knowledge/templates/{platform}-basic.py
```

If using coordinator:
```bash
Read .claude/skills/ha-entity-knowledge/templates/{platform}-coordinator.py
```

#### Step 4.2: Implement Entities

For each entity class:

**Critical checks** (use ha-entity-knowledge):
- [ ] Unique ID is stable
- [ ] Unique ID uses coordinator data (not entity state)
- [ ] Device info is consistent
- [ ] Entity naming follows conventions
- [ ] Properties return correct types
- [ ] No blocking I/O

**Anti-patterns to avoid** (use ha-common-mistakes):
- [ ] DON'T use random/time in unique_id
- [ ] DON'T use entity state in unique_id
- [ ] DON'T call async from sync properties
- [ ] DON'T ignore exceptions silently

**Validate after each entity:**
```bash
python3 -c "from homeassistant.components.{domain}.{platform} import *"
```

### Phase 5: Testing

#### Step 5.1: Run hassfest

```bash
python3 -m script.hassfest validate --integration {domain}
```

**Fix all errors before proceeding.**

#### Step 5.2: Type Checking

```bash
mypy homeassistant/components/{domain}/
```

**Fix all type errors.**

#### Step 5.3: Linting

```bash
pylint homeassistant/components/{domain}/
```

**Fix critical issues. Document any exceptions needed.**

#### Step 5.4: Unit Tests

Create tests in `tests/components/{domain}/`:
- `test_config_flow.py` (if config flow)
- `test_init.py` (setup/unload)
- `test_{platform}.py` (for each platform)

Run tests:
```bash
pytest tests/components/{domain}/ -v
```

**All tests must pass.**

### Phase 6: Final Validation

#### Step 6.1: Integration Test

Use validation sub-agent:
```
Task: ha-integration-validator
```

Validates:
- Manifest completeness
- File structure correct
- Naming conventions followed
- Unique ID patterns stable
- No blocking I/O
- Error handling present

#### Step 6.2: Manual Smoke Test

1. Start HA in development mode
2. Add integration via UI (or YAML)
3. Verify entities created
4. Check entity states
5. Trigger error scenarios
6. Check logs for issues

#### Step 6.3: Final Checklist

Use checklists from Skills:
- [ ] ha-integration-structure/checklists/required-files.md
- [ ] ha-entity-knowledge/checklists/entity-requirements.md
- [ ] ha-config-flow-knowledge/checklists/config-flow-steps.md (if applicable)
- [ ] ha-coordinator-knowledge/checklists/coordinator-setup.md (if applicable)

#### Step 6.4: Common Mistakes Check

Review ha-common-mistakes Skill:
- [ ] No blocking I/O in async context
- [ ] Unique IDs are stable
- [ ] Error handling complete
- [ ] Device info consistent
- [ ] No hard-coded values

## Continuous Validation

After each file creation:
1. Run hassfest
2. Check imports
3. Verify against patterns from Skills

After each major section:
1. Run tests
2. Check types
3. Review against plan

## Using Skills During Implementation

**When implementing entities:**
→ Reference ha-entity-knowledge templates and patterns

**When implementing config flow:**
→ Reference ha-config-flow-knowledge templates and patterns

**When implementing coordinator:**
→ Reference ha-coordinator-knowledge templates and patterns

**When unsure about file structure:**
→ Reference ha-integration-structure patterns

**When debugging issues:**
→ Check ha-common-mistakes for known pitfalls

## Success Criteria

Implementation complete when:
- [ ] All files from plan created
- [ ] hassfest validation passes
- [ ] All tests pass (100% of written tests)
- [ ] Type checking passes (mypy)
- [ ] Linting passes (pylint)
- [ ] Manual smoke test successful
- [ ] All checklists validated
- [ ] No common mistakes present

## Output

When complete:
1. Summary of implemented files
2. Test results
3. Validation results
4. Any deviations from plan (with justification)
5. Known issues (if any)
```

**Key Enhancements:**
- Validates after each step
- References Skills throughout
- Continuous testing
- Built-in common mistake checks

### Success Criteria (Phase 2)

- ✅ Three specialized commands created
- ✅ Commands explicitly reference and use Skills
- ✅ Commands tested on at least one integration
- ✅ Commands produce better results than generic versions
- ✅ Skills automatically activate when commands run

### Estimated Effort: 6-8 hours

---

## Phase 3: Validation Sub-agent

**Objective:** Create specialized sub-agent for HA integration validation

**Duration:** 4-6 hours

### 3.1 Validation Agent Definition

**File:** `.claude/agents/ha-integration-validator.md`

**Structure:**
```yaml
---
name: ha-integration-validator
description: Validates Home Assistant integrations for compliance with HA standards
---

# HA Integration Validator Agent

I validate Home Assistant integrations against HA standards and best practices.

## Validation Scope

I check:
- Manifest.json completeness and correctness
- Required files present
- File naming conventions
- Unique ID stability patterns
- No blocking I/O in async contexts
- Error handling presence
- Device info consistency
- Test coverage
- Type hints presence

## How I Work

When invoked with an integration domain name, I:

1. **Structural Validation**
   - Check all required files exist
   - Verify manifest.json fields
   - Validate file organization

2. **Code Quality Validation**
   - Check for blocking I/O patterns
   - Verify async/await usage
   - Check error handling
   - Verify type hints

3. **HA-Specific Validation**
   - Analyze unique ID generation
   - Check device info consistency
   - Verify entity naming conventions
   - Check coordinator usage patterns

4. **Automated Tool Validation**
   - Run hassfest
   - Run type checking (mypy)
   - Run linting (pylint)
   - Run tests

## Skills I Use

I reference these Skills for validation rules:
- ha-integration-structure (for structure requirements)
- ha-entity-knowledge (for entity patterns)
- ha-config-flow-knowledge (for config flow patterns)
- ha-coordinator-knowledge (for coordinator patterns)
- ha-common-mistakes (for anti-patterns to flag)

## Input

Provide:
- Integration domain name
- Path to integration (if not standard location)

## Output

I provide:
```markdown
# Validation Report: {domain}

## Summary
- Status: PASS/FAIL
- Issues Found: {count}
- Warnings: {count}

## Structural Validation
✓ manifest.json present and valid
✓ __init__.py present
✗ strings.json missing (required for config flow)

## Code Quality
✓ No blocking I/O detected
✓ Async/await usage correct
⚠ Missing error handling in sensor.py:45

## HA-Specific
✓ Unique IDs use stable patterns
✓ Device info consistent
⚠ Entity naming could be improved (see details)

## Automated Tools
✓ hassfest: PASSED
✓ mypy: PASSED
✗ pylint: FAILED (see details)
✓ tests: PASSED (15/15)

## Detailed Issues

### Critical Issues (must fix)
1. strings.json missing for config flow integration
   - Location: homeassistant/components/{domain}/
   - Fix: Add strings.json with config flow text

### Warnings (should fix)
1. Entity naming could be clearer
   - Location: sensor.py:34
   - Current: "sensor_1"
   - Suggested: "temperature_sensor"

### Recommendations (nice to have)
1. Consider using coordinator for multiple sensors
   - Currently: Direct polling per entity
   - Benefit: Reduced API calls

## Next Steps
{prioritized list of fixes}
```

## Usage in Commands

Invoke me from implement_plan_ha_integration.md:
```
Task: ha-integration-validator
Domain: {domain_name}
```

I'll validate and provide detailed report.
```

### 3.2 Validation Scripts

Create helper scripts in `.claude/agents/scripts/`:

```
scripts/
├── validate-unique-ids.py       # Check unique ID stability
├── validate-async-patterns.py   # Check for blocking I/O
├── validate-manifest.py         # Deep manifest validation
└── run-all-validations.sh       # Run all validators
```

These scripts are called by the validator agent.

### Success Criteria (Phase 3)

- ✅ Validator agent created
- ✅ Agent uses all five knowledge Skills
- ✅ Agent runs automated tools (hassfest, mypy, pylint)
- ✅ Agent provides actionable feedback
- ✅ Agent tested on existing integration

### Estimated Effort: 4-6 hours

---

## Phase 4: Testing and Refinement

**Objective:** Validate the complete workflow on real integrations

**Duration:** 10-12 hours

### 4.1 Test on Simple Integration

**Target:** Create new minimal sensor integration

**Steps:**
1. Run `/research_ha_integration` on similar integration
2. Run `/create_plan_ha_integration` for new integration
3. Run `/implement_plan_ha_integration`
4. Verify Skills auto-activated at appropriate times
5. Document any issues

**Success Metrics:**
- Workflow completes without major issues
- Skills activate automatically when relevant
- Implementation follows HA standards
- Validation passes

### 4.2 Test on Medium Integration

**Target:** Create integration with config flow and coordinator

**Steps:**
1. Use full workflow
2. More complex patterns
3. Test error handling
4. Validate coordinator usage

**Success Metrics:**
- Config flow works correctly
- Coordinator pattern correct
- More complex validation passes
- Skills provide relevant information

### 4.3 Test on Complex Integration

**Target:** Multi-platform integration with device support

**Steps:**
1. Use full workflow
2. Multiple entity platforms
3. Device registration
4. Advanced patterns

**Success Metrics:**
- All platforms work correctly
- Device info consistent
- All validation passes
- Skills handle complexity

### 4.4 Refine Based on Feedback

Iterate on:
- Skill descriptions (improve triggering)
- Skill content (add missing patterns)
- Command workflows (streamline steps)
- Validation rules (reduce false positives)

### Success Criteria (Phase 4)

- ✅ Three test integrations completed successfully
- ✅ Skills activated automatically in all cases
- ✅ Commands produced correct structure
- ✅ Validation caught real issues
- ✅ Workflow faster than generic approach (measured)
- ✅ All feedback incorporated into Skills/Commands

### Estimated Effort: 10-12 hours

---

## Phase 5: Documentation and Rollout

**Objective:** Document the workflow and enable team adoption

**Duration:** 4-6 hours

### 5.1 Create Workflow Guide

**File:** `docs/claude-ha-integration-workflow.md`

**Contents:**
```markdown
# Claude Code HA Integration Workflow

## Overview

This workflow uses Claude Code native features to create HA integrations:
- **Skills**: Auto-activated knowledge base
- **Commands**: Guided workflows
- **Sub-agents**: Validation and analysis

## Quick Start

### 1. Research Existing Integration

```bash
/research_ha_integration
# Provide domain name when prompted
```

Claude will:
- Automatically activate relevant Skills
- Analyze integration structure
- Find similar reference integrations
- Document patterns found

### 2. Create Implementation Plan

```bash
/create_plan_ha_integration
# Provide domain name when prompted
```

Claude will:
- Use HA-specific plan template
- Reference pattern Skills
- Validate completeness
- Create detailed roadmap

### 3. Implement Integration

```bash
/implement_plan_ha_integration
# References plan from step 2
```

Claude will:
- Follow plan step-by-step
- Use Skills' templates
- Validate continuously
- Run final validation

## Available Skills

Skills auto-activate based on context:

- **ha-integration-structure**: File organization, manifest.json
- **ha-entity-knowledge**: Entity patterns, unique IDs
- **ha-config-flow-knowledge**: UI configuration flows
- **ha-coordinator-knowledge**: Data update patterns
- **ha-common-mistakes**: Anti-patterns to avoid

You don't need to explicitly invoke Skills - Claude uses them automatically.

## When to Use This Workflow

Use for:
- Creating new HA integrations
- Understanding existing integrations
- Validating integration compliance
- Learning HA patterns

Don't use for:
- Simple bug fixes (use standard workflow)
- Documentation updates
- Non-integration HA work

## Troubleshooting

### Skills Not Activating

Check Skill descriptions match your question. Try rephrasing:
- "How do I create a sensor?" → activates ha-entity-knowledge
- "I need entity patterns" → activates ha-entity-knowledge

### Command Not Found

Ensure you're in project directory with `.claude/commands/`.

### Validation Failing

Run validation agent manually:
```
Task: ha-integration-validator
Domain: {your_domain}
```

Review detailed report for issues.

## Examples

[Include 2-3 complete examples of using the workflow]
```

### 5.2 Create Skill Contribution Guide

**File:** `docs/contributing-ha-skills.md`

**Contents:**
- How to add new patterns to existing Skills
- How to create new Skills
- How to update templates
- Review process for Skill changes
- When to update vs create new

### 5.3 Update Main README

Add section pointing to HA workflow documentation.

### Success Criteria (Phase 5)

- ✅ Complete workflow guide exists
- ✅ Contribution guide for Skills
- ✅ Examples demonstrate full workflow
- ✅ Team trained on new workflow
- ✅ README updated

### Estimated Effort: 4-6 hours

---

## Timeline Summary

| Phase | Description | Effort | Dependencies |
|-------|-------------|--------|--------------|
| 1 | Knowledge Skills | 10-14h | None |
| 2 | Specialized Commands | 6-8h | Phase 1 |
| 3 | Validation Sub-agent | 4-6h | Phases 1-2 |
| 4 | Testing & Refinement | 10-12h | Phases 1-3 |
| 5 | Documentation | 4-6h | Phase 4 |

**Total Estimated Effort:** 34-46 hours

---

## Success Metrics

### Quantitative

Measure against baseline (generic workflow):

- **Research time:** Reduce by 40-50%
- **Planning iterations:** Reduce from 2-3 to 1
- **Implementation errors:** Reduce by 60%
- **Validation failures:** Reduce by 70%
- **Total workflow time:** Reduce by 35-45%

### Qualitative

- Skills activate automatically when relevant
- Commands produce HA-compliant plans
- Implementation matches existing integration quality
- Fewer "what pattern should I use?" questions
- New contributors successful with workflow
- Knowledge captured and reusable

---

## Architecture Benefits

### Using Skills vs thoughts/

| Aspect | Skills (v2) | thoughts/ (v1) |
|--------|-------------|----------------|
| Discovery | Auto by Claude | Manual reference |
| Loading | Progressive | Manual reads |
| Version control | `.claude/` | `thoughts/` |
| Team sharing | Git native | Git native |
| Invocation | Automatic | Explicit |
| Tool restrictions | `allowed-tools` | None |
| Context efficiency | High | Medium |

### Skills + Commands + Sub-agents

**Skills**: Provide knowledge automatically when needed
- Auto-activated based on context
- Progressive disclosure (only loads what's needed)
- Read-only by default

**Commands**: Orchestrate workflow
- User-invoked (/command)
- Structured process
- References Skills explicitly

**Sub-agents**: Execute complex tasks
- Tool-invoked (Task tool)
- Specialized analysis
- Can use Skills too

This three-layer architecture provides:
1. **Efficiency**: Auto-activation reduces prompting
2. **Structure**: Commands guide workflow
3. **Validation**: Sub-agents ensure quality
4. **Maintainability**: All in `.claude/`, version controlled

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Skills don't activate | High | Test descriptions thoroughly, iterate |
| Skill content becomes outdated | Medium | Version control, regular review |
| Commands too rigid | Medium | Include escape hatches, allow deviations |
| Validation too strict | Medium | Tune thresholds, allow overrides |
| HA API changes | Medium | Monitor releases, update Skills promptly |
| Team doesn't adopt | Low | Clear docs, demonstrate value, training |

---

## Quick Start (MVP)

To get value quickly, implement minimal version:

### MVP Components (10-12 hours)

**One Skill:** ha-entity-knowledge (most critical)
- Entity patterns
- Unique ID patterns
- 2-3 templates
- 1 checklist

**One Command:** research_ha_integration
- HA-specific research protocol
- References ha-entity-knowledge Skill
- Structured output

**No sub-agent initially** (use manual validation)

**Result:** Immediate improvement in research phase, validate approach before expanding.

Once MVP proves valuable, incrementally add:
1. ha-integration-structure Skill
2. create_plan_ha_integration Command
3. ha-config-flow-knowledge Skill
4. implement_plan_ha_integration Command
5. Remaining Skills
6. Validation sub-agent

---

## Future Enhancements (Post-MVP)

### Phase 6+: Advanced Features

1. **Specialized Skills per Integration Type**
   - ha-climate-integration
   - ha-light-integration
   - ha-media-player-integration
   Each with type-specific patterns

2. **Migration Skills**
   - ha-migration-async
   - ha-migration-config-entry
   For upgrading legacy integrations

3. **Testing Skills**
   - ha-testing-patterns
   - ha-mocking-patterns
   - ha-fixtures-patterns

4. **Performance Skills**
   - ha-performance-optimization
   - ha-resource-management

5. **Multi-System Support**
   - Adapt pattern for ESPHome, HACS, etc.
   - Create generic extension-system-knowledge base
   - Specialize per system

6. **Advanced Validation**
   - Performance validation
   - Security validation
   - Accessibility validation

7. **Pattern Mining**
   - Auto-extract patterns from existing integrations
   - Suggest similar integrations automatically
   - Auto-update Skills from new integrations

8. **Interactive Mode**
   - Guided wizard via command
   - Real-time validation feedback
   - Suggested fixes

---

## Appendix A: Skill Description Best Practices

Good Skill descriptions are critical for auto-activation.

### Formula

```
{What it does} + {Domain keywords} + {When to use}
```

### Examples

**Good:**
```yaml
description: Home Assistant entity implementation patterns, base classes, unique IDs, device info. Use when implementing sensors, switches, climate, or any HA entities.
```
- ✓ Clear what it does
- ✓ Domain keywords (entity, sensor, switch, climate)
- ✓ Clear when to use

**Bad:**
```yaml
description: Helps with HA stuff
```
- ✗ Vague
- ✗ No keywords
- ✗ Unclear when to use

### Testing Descriptions

Ask questions that should trigger the Skill:
- "How do I create a sensor entity?" → should activate ha-entity-knowledge
- "What files does an integration need?" → should activate ha-integration-structure
- "I need to add a config flow" → should activate ha-config-flow-knowledge

If Skill doesn't activate, refine description.

---

## Appendix B: Example Skill Contents

### Minimal Entity Template

File: `.claude/skills/ha-entity-knowledge/templates/sensor-basic.py`

```python
"""Basic sensor entity template."""
from homeassistant.components.sensor import SensorEntity

class MySensorEntity(SensorEntity):
    """Representation of a sensor."""

    def __init__(self, name: str, unique_id: str) -> None:
        """Initialize the sensor."""
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._attr_native_value = None

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._attr_native_value

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        # TODO: Implement update logic
        # self._attr_native_value = await fetch_data()
        pass
```

### Minimal Manifest Template

File: `.claude/skills/ha-integration-structure/templates/manifest.json`

```json
{
  "domain": "example",
  "name": "Example Integration",
  "codeowners": ["@your-github-username"],
  "config_flow": false,
  "documentation": "https://www.home-assistant.io/integrations/example",
  "iot_class": "cloud_polling",
  "requirements": [],
  "version": "1.0.0"
}
```

---

## Appendix C: File Structure Reference

Complete `.claude/` structure after implementation:

```
.claude/
├── skills/
│   ├── ha-integration-structure/
│   │   ├── SKILL.md
│   │   ├── required-files.md
│   │   ├── optional-files.md
│   │   ├── directory-layout.md
│   │   ├── templates/
│   │   │   ├── manifest.json
│   │   │   ├── manifest-full.json
│   │   │   ├── __init__.py
│   │   │   └── __init__-platforms.py
│   │   ├── examples/
│   │   │   ├── template-integration.md
│   │   │   └── met-integration.md
│   │   └── checklists/
│   │       ├── required-files.md
│   │       └── manifest-fields.md
│   │
│   ├── ha-entity-knowledge/
│   │   ├── SKILL.md
│   │   ├── entity-base-classes.md
│   │   ├── unique-id-patterns.md
│   │   ├── device-info-patterns.md
│   │   ├── state-conventions.md
│   │   ├── entity-naming.md
│   │   ├── templates/
│   │   │   ├── sensor-basic.py
│   │   │   ├── sensor-coordinator.py
│   │   │   ├── climate-basic.py
│   │   │   ├── switch-basic.py
│   │   │   └── entity-platform.py
│   │   ├── examples/
│   │   │   ├── template-sensor.md
│   │   │   ├── met-sensor.md
│   │   │   └── random-sensor.md
│   │   └── checklists/
│   │       ├── entity-requirements.md
│   │       └── unique-id-validation.md
│   │
│   ├── ha-config-flow-knowledge/
│   │   ├── SKILL.md
│   │   ├── config-flow-basics.md
│   │   ├── error-handling.md
│   │   ├── user-flow-pattern.md
│   │   ├── reauth-flow-pattern.md
│   │   ├── options-flow-pattern.md
│   │   ├── discovery-patterns.md
│   │   ├── templates/
│   │   │   ├── config_flow-basic.py
│   │   │   ├── config_flow-auth.py
│   │   │   ├── config_flow-options.py
│   │   │   └── strings.json
│   │   ├── examples/
│   │   │   ├── openweathermap-flow.md
│   │   │   └── met-flow.md
│   │   └── checklists/
│   │       ├── config-flow-steps.md
│   │       └── error-handling.md
│   │
│   ├── ha-coordinator-knowledge/
│   │   ├── SKILL.md
│   │   ├── coordinator-basics.md
│   │   ├── update-method-pattern.md
│   │   ├── coordinator-entity-pattern.md
│   │   ├── error-handling.md
│   │   ├── auth-refresh-pattern.md
│   │   ├── templates/
│   │   │   ├── coordinator-basic.py
│   │   │   ├── coordinator-auth.py
│   │   │   ├── entity-coordinator.py
│   │   │   └── __init__-coordinator.py
│   │   ├── examples/
│   │   │   ├── met-coordinator.md
│   │   │   └── openweathermap-coordinator.md
│   │   └── checklists/
│   │       ├── coordinator-setup.md
│   │       └── error-handling.md
│   │
│   └── ha-common-mistakes/
│       ├── SKILL.md
│       ├── blocking-io.md
│       ├── unique-id-instability.md
│       ├── missing-error-handling.md
│       ├── incorrect-device-info.md
│       ├── hardcoded-values.md
│       ├── testing-mistakes.md
│       └── examples/
│           ├── blocking-io-bad.py
│           ├── blocking-io-good.py
│           ├── unique-id-bad.py
│           └── unique-id-good.py
│
├── commands/
│   ├── research_ha_integration.md
│   ├── create_plan_ha_integration.md
│   └── implement_plan_ha_integration.md
│
└── agents/
    ├── ha-integration-validator.md
    └── scripts/
        ├── validate-unique-ids.py
        ├── validate-async-patterns.py
        ├── validate-manifest.py
        └── run-all-validations.sh
```

---

## Appendix D: Migration from v1

If you started with v1 (thoughts/ approach):

### Migration Steps

1. **Convert thoughts/shared/patterns/ → Skills**
   - Each pattern document becomes a Skill
   - Add SKILL.md with frontmatter
   - Move to `.claude/skills/{skill-name}/`

2. **Convert thoughts/shared/templates/ → Skill templates/**
   - Distribute templates to relevant Skills
   - Add references from SKILL.md

3. **Convert thoughts/shared/checklists/ → Skill checklists/**
   - Distribute to relevant Skills
   - Reference from SKILL.md

4. **Update Commands**
   - Remove explicit thoughts/ reads
   - Let Skills auto-activate instead

5. **Test Migration**
   - Verify Skills activate correctly
   - Test full workflow
   - Compare to v1 performance

### V1 to V2 Mapping

| v1 Location | v2 Location |
|-------------|-------------|
| thoughts/shared/patterns/ha-integration-structure.md | .claude/skills/ha-integration-structure/SKILL.md + supporting docs |
| thoughts/shared/patterns/ha-entity-patterns.md | .claude/skills/ha-entity-knowledge/SKILL.md + patterns.md |
| thoughts/shared/templates/ha-sensor-integration.md | .claude/skills/ha-entity-knowledge/templates/sensor-basic.py |
| thoughts/shared/checklists/ha-integration-research-checklist.md | .claude/skills/ha-integration-structure/checklists/research.md |

---

**Plan Version:** v2
**Last Updated:** 2025-11-21
**Status:** Draft - Ready for Review
**Supersedes:** v1 (thoughts/ approach)
