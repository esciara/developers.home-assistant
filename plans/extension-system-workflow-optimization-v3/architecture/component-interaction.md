# Component Interaction Model

**Last Updated:** 2025-11-21

---

## Overview

This document details how Skills, Commands, and Sub-agents interact during the complete workflow from research → plan → implement → validate.

---

## Complete Workflow Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INITIATES                           │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
        │  RESEARCH    │ │   PLANNING   │ │ IMPLEMENT    │
        │   PHASE      │ │    PHASE     │ │   PHASE      │
        └──────────────┘ └──────────────┘ └──────────────┘
                │               │               │
                │               │               │
                ▼               ▼               ▼
┌───────────────────────────────────────────────────────────────────┐
│                    SKILLS (Auto-activated via hooks)               │
│  • ha-integration-structure (research phase)                       │
│  • ha-entity-knowledge (planning + implementation)                 │
│  • ha-config-flow-knowledge (planning + implementation)            │
│  • ha-coordinator-knowledge (planning + implementation)            │
│  • ha-common-mistakes (all phases)                                │
└───────────────────────────────────────────────────────────────────┘
                                │
                                │ (implementation phase)
                                ▼
                ┌─────────────────────────────────┐
                │   VALIDATION SUB-AGENT          │
                │  (Launched via Task tool)       │
                └─────────────────────────────────┘
```

---

## Phase 1: Research Phase

### User Action
```
User: /research_ha_integration mqtt
```

### Command Activation
```
research_ha_integration.md command expands with:
  1. HA-specific research protocol
  2. File discovery checklist
  3. Pattern recognition guidance
  4. Structured output format
```

### Automatic Skill Activation (via hooks)

**Trigger 1: Command prompt mentions "integration"**
→ Hook activates: `ha-integration-structure`

**Trigger 2: User opens manifest.json during research**
→ Hook activates: `ha-integration-structure` (if not already active)

**Trigger 3: User asks "How do entities work in this integration?"**
→ Hook activates: `ha-entity-knowledge`

### Skills Provide Context

**ha-integration-structure contributes:**
- Required files checklist (manifest.json, __init__.py, etc.)
- manifest.json structure and required fields
- __init__.py setup patterns
- Platform file expectations

**ha-entity-knowledge contributes (if activated):**
- Entity base class patterns
- Device info expectations
- State and attribute conventions

### Command Output

Structured research document:
```markdown
# MQTT Integration Research

## File Structure
- ✅ manifest.json (reviewed)
- ✅ __init__.py (reviewed)
- ✅ sensor.py (platform file)
- ✅ config_flow.py (UI configuration)
...

## Key Patterns Identified
- Uses DataUpdateCoordinator
- Device-based entities
- Unique ID: based on MQTT topic + entity type
...
```

### Data Flow
```
User Prompt
    ↓
research_ha_integration Command
    ↓
Hook System (analyzes prompt + files)
    ↓
Activates: ha-integration-structure Skill
    ↓
Claude uses Skill's checklists and patterns
    ↓
Outputs: Structured research document
```

---

## Phase 2: Planning Phase

### User Action
```
User: /create_plan_ha_integration mqtt
```

### Command Activation
```
create_plan_ha_integration.md command expands with:
  1. HA-specific plan template
  2. Architecture decision framework
  3. Pattern selection guidance
  4. Success criteria checklist
```

### Automatic Skill Activation

**Trigger 1: Command requires entity planning**
→ Hook activates: `ha-entity-knowledge`

**Trigger 2: Integration needs config flow**
→ Hook activates: `ha-config-flow-knowledge`

**Trigger 3: Integration uses coordinator**
→ Hook activates: `ha-coordinator-knowledge`

**How hooks know:**
- Command explicitly mentions these concepts
- Research document (from Phase 1) mentions them
- User asks questions containing trigger keywords

### Skills Provide Context

**ha-entity-knowledge contributes:**
- Entity architecture decision: CoordinatorEntity vs polling entity
- Unique ID strategy selection
- Device info pattern recommendations
- Templates for sensor/switch/etc.

**ha-config-flow-knowledge contributes:**
- Config flow step patterns
- Error handling approaches
- Schema definitions for user input
- Validation strategies

**ha-coordinator-knowledge contributes:**
- DataUpdateCoordinator setup pattern
- Update interval recommendations
- Error handling and recovery patterns
- Authentication refresh strategies

**ha-common-mistakes contributes:**
- Anti-patterns to avoid in plan
- Common pitfalls to note
- Best practices to follow

### Command Output

Structured implementation plan:
```markdown
# MQTT Integration Implementation Plan

## Architecture Decisions

### Entity Implementation
Pattern: CoordinatorEntity (ha-entity-knowledge recommended)
Rationale: Coordinator handles MQTT subscription, entities just read data
Unique ID Strategy: {device_id}_{entity_type}_{channel}

### Config Flow
Pattern: Single-step discovery flow (ha-config-flow-knowledge)
Steps:
  1. Auto-discover MQTT broker
  2. Validate connection
  3. Create entry

### Coordinator
Pattern: DataUpdateCoordinator with 30s update (ha-coordinator-knowledge)
Responsibilities:
  - MQTT subscription management
  - Data parsing
  - Error handling
...

## Implementation Steps
[Detailed step-by-step plan]

## Success Criteria
[Checkboxes from Skill templates]
```

### Data Flow
```
User Prompt + Research Doc
    ↓
create_plan_ha_integration Command
    ↓
Hook System (analyzes context)
    ↓
Activates: ha-entity-knowledge, ha-config-flow-knowledge, ha-coordinator-knowledge
    ↓
Claude uses Skill templates and patterns
    ↓
Outputs: Structured implementation plan
```

---

## Phase 3: Implementation Phase

### User Action
```
User: /implement_plan_ha_integration
```

### Command Activation
```
implement_plan_ha_integration.md command expands with:
  1. Step-by-step implementation protocol
  2. Continuous validation checkpoints
  3. Template usage guidance
  4. Final validation instructions
```

### Automatic Skill Activation

**Throughout implementation, hooks activate Skills based on:**
- **Files being edited:** `sensor.py` → `ha-entity-knowledge`
- **Code being written:** Config flow code → `ha-config-flow-knowledge`
- **Questions asked:** "How do I handle errors?" → `ha-coordinator-knowledge`
- **Problems encountered:** "This isn't working" → `ha-common-mistakes`

### Skills Provide Templates

**ha-entity-knowledge provides:**
```python
# Template: CoordinatorEntity-based sensor
class MQTTSensor(CoordinatorEntity, SensorEntity):
    """MQTT Sensor."""

    def __init__(self, coordinator, device_id, channel):
        super().__init__(coordinator)
        self._device_id = device_id
        self._channel = channel

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self._device_id}_sensor_{self._channel}"

    # [Additional template code]
```

**ha-config-flow-knowledge provides:**
```python
# Template: Single-step config flow
async def async_step_user(self, user_input=None):
    """Handle the initial step."""
    errors = {}

    if user_input is not None:
        # Validation logic template
        # [Additional template code]
```

### Implementation Process

**Step 1: Create manifest.json**
- Skill active: `ha-integration-structure`
- Uses template from Skill
- Validates against checklist

**Step 2: Create __init__.py**
- Skill active: `ha-integration-structure`
- Uses setup pattern from Skill
- Implements coordinator setup (from `ha-coordinator-knowledge`)

**Step 3: Create coordinator.py**
- Skill active: `ha-coordinator-knowledge`
- Uses DataUpdateCoordinator template
- Implements error handling patterns

**Step 4: Create config_flow.py**
- Skill active: `ha-config-flow-knowledge`
- Uses flow template
- Implements validation patterns

**Step 5: Create sensor.py**
- Skill active: `ha-entity-knowledge`
- Uses CoordinatorEntity template
- Implements unique ID strategy

### Sub-agent Activation

**After implementation complete:**
```
implement_plan_ha_integration Command executes:
  Task: ha-integration-validator
```

**Validator sub-agent:**
1. Reads all integration files
2. References all Skills for validation rules
3. Runs automated tools (hassfest, mypy, pylint)
4. Returns detailed validation report

### Data Flow
```
User Prompt + Implementation Plan
    ↓
implement_plan_ha_integration Command
    ↓
┌─────────────────────────────────────┐
│ Iterative Implementation Steps      │
│                                     │
│ For each step:                      │
│   1. Edit files                     │
│   2. Hooks activate relevant Skills │
│   3. Claude uses Skill templates    │
│   4. Validate against checklist     │
│   5. Move to next step              │
└─────────────────────────────────────┘
    ↓
Launch: ha-integration-validator
    ↓
┌─────────────────────────────────────┐
│ Validation Sub-agent                │
│   • Check manifest completeness     │
│   • Verify file structure           │
│   • Analyze unique ID stability     │
│   • Detect blocking I/O             │
│   • Run automated tools             │
└─────────────────────────────────────┘
    ↓
Outputs: Validation report + fixes
```

---

## Skill-to-Skill Interactions

Skills can reference each other's patterns:

### Example: Entity + Coordinator Integration

**Scenario:** Implementing CoordinatorEntity

**ha-coordinator-knowledge says:**
"When entities use coordinator, see ha-entity-knowledge for CoordinatorEntity pattern"

**ha-entity-knowledge says:**
"CoordinatorEntity requires DataUpdateCoordinator from ha-coordinator-knowledge"

**Result:** Claude gets complete picture from both Skills

### Example: Config Flow + Common Mistakes

**Scenario:** User implementing config flow validation

**ha-config-flow-knowledge provides:**
Template for validation

**ha-common-mistakes warns:**
"Don't do blocking I/O in async_step_user - use async libraries"

**Result:** Implementation follows patterns AND avoids anti-patterns

---

## Command-to-Command Handoff

### Research → Plan

**Research command outputs:**
```markdown
## Patterns Identified
- Uses DataUpdateCoordinator
- Device-based entities
- Config flow with discovery
```

**Plan command uses this:**
- Activates relevant Skills (coordinator, entity, config-flow)
- Creates plan sections matching patterns
- References specific implementation approaches

### Plan → Implementation

**Plan outputs:**
```markdown
## Architecture Decisions
Entity Pattern: CoordinatorEntity
Config Flow: Single-step with discovery
Coordinator: 30s polling interval
```

**Implementation command uses this:**
- Follows plan structure
- Activates Skills for each component
- Uses templates matching plan decisions
- Validates against plan criteria

---

## Progressive Skill Engagement

Skills load progressively as work evolves:

### Early Implementation (manifest.json)
**Active Skills:**
- `ha-integration-structure` (file organization)

**Context usage:** ~15% of total Skills

### Mid Implementation (coordinator + entities)
**Active Skills:**
- `ha-integration-structure` (still active)
- `ha-coordinator-knowledge` (coordinator code)
- `ha-entity-knowledge` (entity code)

**Context usage:** ~45% of total Skills

### Late Implementation (refinement)
**Active Skills:**
- All Skills potentially active
- `ha-common-mistakes` for final review

**Context usage:** ~80% of total Skills

**Benefit:** Context usage grows naturally with implementation complexity

---

## Sub-agent Interaction with Skills

### Validator References All Skills

**For each validation rule:**

**Manifest validation:**
→ Uses `ha-integration-structure` checklist

**Entity validation:**
→ Uses `ha-entity-knowledge` patterns
→ Checks unique ID against recommended strategies

**Config flow validation:**
→ Uses `ha-config-flow-knowledge` patterns
→ Checks error handling against recommendations

**Coordinator validation:**
→ Uses `ha-coordinator-knowledge` patterns
→ Checks update interval, error handling

**Anti-pattern detection:**
→ Uses `ha-common-mistakes` checklist
→ Flags known anti-patterns

### Validator Output Format

```markdown
# Validation Report

## ✅ Passed
- Manifest: All required fields present
- File structure: Follows standard layout
- Unique IDs: Use recommended {device_id}_{type} pattern

## ⚠️ Warnings
- Coordinator: Update interval (60s) higher than typical (30s)
  Reference: ha-coordinator-knowledge recommends 30s for MQTT

## ❌ Issues
- sensor.py:45: Blocking I/O call in async context
  Reference: ha-common-mistakes - "Don't use requests.get() in async"
  Fix: Use aiohttp instead
```

**Note:** Each issue references the Skill that contains the pattern/rule

---

## Error Recovery Flows

### Scenario: Implementation Error

**User:** "I'm getting an error about unique_id"

**Hook activates:** `ha-entity-knowledge` (keyword "unique_id")

**Skill provides:**
- Unique ID requirements
- Common unique ID mistakes
- Debugging guidance

**Hook may also activate:** `ha-common-mistakes`

**Result:** User gets targeted help from relevant Skills

### Scenario: Validation Failure

**Validator reports:** "Blocking I/O detected in config_flow.py"

**User opens:** `config_flow.py`

**Hook activates:**
- `ha-config-flow-knowledge` (file-based)
- `ha-common-mistakes` (error context)

**Skills provide:**
- Async patterns for config flows
- Anti-pattern examples (blocking I/O)
- Side-by-side good vs bad code

**Result:** User sees both the pattern to follow AND the mistake to avoid

---

## Context Optimization in Practice

### Without Hooks (Manual)
```
User: "How do I create a sensor?"
Claude: (has no context)
User: "@ha-entity-knowledge How do I create a sensor?"
Claude: (loads Skill, answers question)
```

**Context loaded:** Only when explicitly requested
**User friction:** Must remember Skill names

### With Hooks (Automatic)
```
User: "How do I create a sensor?"
Hook: (detects "sensor", activates ha-entity-knowledge)
Claude: (has context, answers directly using Skill patterns)
```

**Context loaded:** Automatically, transparently
**User friction:** None

### File-Based Activation Example
```
User: (opens sensor.py in editor)
Hook: (detects file pattern, activates ha-entity-knowledge)
User: "How should I structure this entity?"
Claude: (already has Skill loaded, answers immediately)
```

**Context loaded:** Proactively based on file
**User friction:** None

---

## Workflow Timing

### Research Phase
- **Duration:** 30-60 minutes typically
- **Skills activated:** 1-2 (integration-structure, maybe entity)
- **Context usage:** Low (~20%)

### Planning Phase
- **Duration:** 1-2 hours typically
- **Skills activated:** 3-4 (entity, config-flow, coordinator, common-mistakes)
- **Context usage:** Medium (~50%)

### Implementation Phase
- **Duration:** 4-8 hours typically
- **Skills activated:** All 5 progressively
- **Sub-agents launched:** 1 (validator at end)
- **Context usage:** High (~80%) but spread over time

**Total workflow:** 6-12 hours for typical integration
**Context optimization:** Never loads all Skills at once, progressive engagement

---

## Next Steps

1. **Understand architecture:** [Architecture Overview](overview.md)
2. **Understand hooks:** [Hook-Based Activation System](hook-system.md)
3. **Start implementing:** [Phase 1: Skills Foundation](../phases/phase-1-skills.md)

---

**See Also:**
- [System Architecture Overview](overview.md)
- [Hook-Based Activation System](hook-system.md)
- [Testing Integration Workflows](../testing/integration-tests.md)
- [Back to Main README](../README.md)
