# System Architecture Overview

**Last Updated:** 2025-11-21

---

## Three-Layer Architecture

This workflow optimization uses a three-layer architecture pattern that leverages Claude Code's native features:

```
┌─────────────────────────────────────────────────────┐
│                    USER LAYER                        │
│  Invokes commands, reviews output, provides input   │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│              COMMAND LAYER (Orchestration)           │
│  /research_ha_integration                           │
│  /create_plan_ha_integration                        │
│  /implement_plan_ha_integration                     │
└──────────────────┬──────────────────────────────────┘
                   │
                   ├──────────► Activates Skills (auto)
                   │
                   └──────────► Launches Sub-agents (via Task tool)
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
┌──────────────────┐  ┌──────────────────┐
│  SKILL LAYER     │  │  AGENT LAYER     │
│  (Knowledge)     │  │  (Complex Tasks) │
├──────────────────┤  ├──────────────────┤
│ • ha-entity-*    │  │ • validator      │
│ • ha-integration-│  │                  │
│ • ha-config-flow-│  │                  │
│ • ha-coordinator-│  │                  │
│ • ha-common-*    │  │                  │
└──────────────────┘  └──────────────────┘
  Auto-invoked by        Invoked by commands
  Claude via SKILL.md    (Task tool)
```

---

## Layer 1: Skills (Knowledge Base)

**Purpose:** Provide patterns, templates, and checklists automatically when relevant

**Location:** `.claude/skills/`

**How They Work:**
- Stored as directories with SKILL.md files
- **Auto-activated by Claude based on SKILL.md descriptions**
- Provide context without explicit invocation
- Progressive disclosure (main Skill loads first, details on-demand)

**When They Activate:**
- Claude detects relevant keywords in prompts (e.g., "entity", "sensor")
- Claude recognizes context from file names or content
- Command explicitly activates them

**Example Flow:**
1. User types: "How do I create a sensor with unique ID?"
2. Claude detects "sensor" and "unique ID" keywords
3. Claude auto-activates `ha-entity-knowledge` Skill
4. Claude has entity patterns and unique ID strategies in context
5. Claude provides accurate, pattern-based answer

**Five Skills:**
1. `ha-integration-structure` - File organization, manifest.json, __init__.py
2. `ha-entity-knowledge` - Entity base classes, unique IDs, device info
3. `ha-config-flow-knowledge` - Config flows, step patterns, validation
4. `ha-coordinator-knowledge` - DataUpdateCoordinator patterns
5. `ha-common-mistakes` - Anti-patterns and side-by-side comparisons

**Note:** Skills activate automatically based on clear, descriptive SKILL.md files that Claude can understand

---

## Layer 2: Commands (Workflow Orchestration)

**Purpose:** Guide Claude through HA-specific workflows with structured steps

**Location:** `.claude/commands/`

**How They Work:**
- User invokes with `/command_name`
- Command prompt expands with detailed instructions
- Commands explicitly activate relevant Skills
- Commands may launch sub-agents for complex tasks
- Produce structured, consistent output

**When to Use:**
- Starting a new integration (research)
- Planning implementation approach (planning)
- Building the integration (implementation)

**Example Flow:**
1. User types: `/research_ha_integration hue`
2. Command expands to full research protocol
3. Command activates `ha-integration-structure` Skill
4. Claude follows HA-specific research checklist
5. Outputs structured research document

**Three Commands:**
1. `research_ha_integration` - HA-specific research protocol
2. `create_plan_ha_integration` - HA-specific planning template
3. `implement_plan_ha_integration` - Step-by-step implementation guide

**Enhancement Over Generic Commands:**
- HA-specific search patterns
- Automatic Skill activation
- Built-in validation checkpoints
- Reference to HA patterns and conventions

---

## Layer 3: Sub-agents (Complex Task Execution)

**Purpose:** Execute complex, multi-step validation and analysis tasks

**Location:** `.claude/agents/`

**How They Work:**
- Commands invoke via Task tool
- Run autonomously with specific instructions
- Have access to all Skills for validation rules
- Return detailed reports

**When They Activate:**
- Command launches them for validation
- User explicitly requests: "Task: ha-integration-validator"
- After implementation for quality checks

**Example Flow:**
1. Command runs: `Task: ha-integration-validator`
2. Agent reads integration files
3. Agent references all Skills for validation rules
4. Agent runs automated tools (hassfest, mypy, pylint)
5. Agent returns detailed validation report with actionable feedback

**One Sub-agent:**
1. `ha-integration-validator` - Validates manifest, file structure, unique IDs, async patterns, error handling

---

## Component Interaction Model

### Workflow 1: Research Phase

```
User: /research_ha_integration mqtt

┌─────────────────────────────────────┐
│  research_ha_integration Command     │
│  1. Activates Skills:                │
│     - ha-integration-structure       │
│  2. Follows research protocol        │
│  3. Outputs structured findings      │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Skills Provide Context:             │
│  - Required files checklist          │
│  - manifest.json patterns            │
│  - __init__.py patterns              │
└─────────────────────────────────────┘
```

### Workflow 2: Planning Phase

```
User: /create_plan_ha_integration mqtt

┌─────────────────────────────────────┐
│  create_plan_ha_integration Command  │
│  1. Activates Skills:                │
│     - ha-entity-knowledge            │
│     - ha-config-flow-knowledge       │
│     - ha-coordinator-knowledge       │
│  2. Uses planning template           │
│  3. References Skills for patterns   │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Skills Provide:                     │
│  - Entity patterns for platform      │
│  - Config flow templates             │
│  - Coordinator setup guidance        │
└─────────────────────────────────────┘
```

### Workflow 3: Implementation Phase

```
User: /implement_plan_ha_integration

┌─────────────────────────────────────┐
│  implement_plan_ha_integration Cmd   │
│  1. Activates all relevant Skills    │
│  2. Guides step-by-step impl         │
│  3. Launches validator at end        │
└──────────────┬──────────────────────┘
               │
               ├──────► Skills provide templates & patterns
               │
               └──────► Launches sub-agent
                        │
                        ▼
               ┌─────────────────────────────┐
               │  ha-integration-validator    │
               │  - Validates manifest        │
               │  - Checks file structure     │
               │  - Analyzes unique IDs       │
               │  - Detects async issues      │
               │  - Runs automated tools      │
               └─────────────────────────────┘
```

---

## Why This Architecture?

### 1. Separation of Concerns

| Layer | Responsibility | Updates When |
|-------|---------------|--------------|
| Skills | Knowledge about HA patterns | HA API changes, new patterns discovered |
| Commands | Workflow orchestration | Process improvements, new workflow steps |
| Sub-agents | Complex validation logic | Validation rules change, new checks needed |

**Benefit:** Update one layer without affecting others

### 2. Reusability

- Skills used across all commands
- Commands reuse sub-agents
- Sub-agents reference Skills for validation rules

**Benefit:** Write once, use everywhere

### 3. Progressive Disclosure

- Start with command (high-level workflow)
- Skills load automatically when needed (Claude's auto-activation)
- Sub-agents handle complex tasks only when necessary

**Benefit:** Efficient context usage

### 4. Testability

- Each layer can be tested independently
- Skills: Test template compilation, pattern accuracy
- Commands: Test workflow produces correct structure
- Sub-agents: Test validation catches real issues

**Benefit:** Quality assurance at each layer

---

## Why Skills Over thoughts/ Directory?

| Aspect | Skills (v4) | thoughts/ (v1) |
|--------|-------------|----------------|
| Discovery | Auto by Claude | Manual reference |
| Loading | Progressive (auto) | Manual reads required |
| Invocation | Automatic | Explicit Tool calls |
| Tool restrictions | `allowed-tools` | None (can use any tool) |
| Context efficiency | High (on-demand) | Medium (manual management) |
| Version control | Git-native (`.claude/`) | Git-native (`thoughts/`) |
| Team sharing | Instant (git pull) | Instant (git pull) |

**Key Difference:** Skills' auto-activation is **automatic via Claude's built-in system**, while thoughts/ requires manual reference and loading.

**Note:** Skills activate automatically when Claude detects relevant context based on clear SKILL.md descriptions.

---

## Data Flow

### Information Flows Down (User → Commands → Skills/Agents)

```
User Request
    ↓
Command (orchestrates)
    ↓
┌───────────┬─────────────┐
↓           ↓             ↓
Skills   Sub-agents   Direct Action
(context) (complex)   (simple tasks)
```

### Knowledge Flows Up (Skills → Commands → User)

```
Skills (patterns, templates)
    ↓
Commands (use patterns in workflow)
    ↓
Structured Output
    ↓
User (receives HA-compliant results)
```

---

## File Organization

```
.claude/
├── skills/
│   ├── ha-integration-structure/
│   │   ├── SKILL.md                    # Main Skill definition
│   │   ├── file-organization.md        # Supporting doc
│   │   ├── manifest-patterns.md        # Supporting doc
│   │   └── templates/                  # Code templates
│   │       ├── manifest.json
│   │       └── __init__.py
│   │
│   ├── ha-entity-knowledge/
│   │   ├── SKILL.md
│   │   ├── entity-base-classes.md
│   │   ├── unique-id-strategies.md
│   │   ├── device-info-patterns.md
│   │   └── templates/
│   │       ├── sensor-entity.py
│   │       └── device-based-entity.py
│   │
│   └── [other skills...]
│
├── commands/
│   ├── research_ha_integration.md      # Slash command
│   ├── create_plan_ha_integration.md   # Slash command
│   └── implement_plan_ha_integration.md # Slash command
│
└── agents/
    └── ha-integration-validator.md     # Sub-agent definition

```

---

## Context Budget Management

**Problem:** Claude has a context window limit. Loading everything wastes context.

**Solution:** Progressive disclosure through Claude's auto-activation

### Context Usage Comparison

| Approach | Context Used | Efficiency |
|----------|--------------|------------|
| No optimization | Load entire codebase each time | ❌ Very Low |
| v1 (thoughts/) | Load relevant docs manually | ⚠️ Medium |
| **v4 (Native Skills)** | **Skills auto-load via Claude** | ✅ **High** |

### How Auto-Activation Optimizes Context

1. **Context-based activation:** Claude analyzes prompts and file context
2. **Selective loading:** Only load Skills relevant to current task
3. **Progressive detail:** Load main Skill first, supporting docs on-demand

**Example:**
- User edits `sensor.py`: Claude loads `ha-entity-knowledge` only
- User edits `config_flow.py`: Claude loads `ha-config-flow-knowledge` only
- User asks "How do coordinators work?": Claude loads `ha-coordinator-knowledge` only

**Benefit:** ~60-70% reduction in context usage vs loading all Skills manually

---

## Next Steps

1. **See interaction details:** Read [Component Interaction Model](component-interaction.md)
2. **Start building:** Read [Phase 1: Skills Creation](../phases/phase-1-skills.md)

---

**See Also:**
- [Component Interaction Model](component-interaction.md)
- [Back to Main README](../README.md)
