# Phase 1: Knowledge Skills Creation

**Objective:** Create five Skills that guide Claude to relevant documentation

**Duration:** 8-12 hours

**Dependencies:** None - start here

---

## Overview

Phase 1 creates five Skills that act as **navigation guides** to the research documents. These Skills don't duplicate research docs, they point Claude to the right sections and provide decision-making context.

**Key Principle:** Skills point to research doc sections (which contain precise info from docs/), NOT direct to `docs/` files

---

## Deliverables

### Five Knowledge Skills

Create these Skills in `.claude/skills/`:

**1. ha-integration-structure**
- **Purpose**: Guide file organization and manifest creation
- **Points to**:
  - New integrations doc → Section 1 (Getting Started)
  - New integrations doc → Section 7 (Development Workflow)
- **Provides**: File structure checklists, required vs optional files, manifest patterns
- **Activates on**: "integration structure", "manifest", "what files"

**2. ha-entity-knowledge** ⭐ Most Critical
- **Purpose**: Guide entity implementation with focus on unique IDs
- **Points to**:
  - New integrations doc → Section 3 (Entity Implementation)
  - Refactoring doc → Section 2 (Entity Refactoring Patterns)
- **Provides**: Decision trees for entity types, unique ID strategies, device info requirements, has_entity_name patterns
- **Activates on**: "entity", "sensor", "unique id", "device info"
- **Critical**: Unique ID stability is a common pain point

**3. ha-config-flow-knowledge**
- **Purpose**: Guide config flow implementation
- **Points to**:
  - New integrations doc → Section 2 (Configuration Flows)
  - Refactoring doc → Section 1 (Config Flow Refactoring)
  - Refactoring doc → Section 7 (Authentication Flows)
- **Provides**: Flow step patterns, error handling checklist, 100% test coverage requirement, reauthentication
- **Activates on**: "config flow", "configuration", "setup wizard"

**4. ha-coordinator-knowledge**
- **Purpose**: Guide DataUpdateCoordinator usage
- **Points to**:
  - New integrations doc → Section 6 (Core Concepts - DataUpdateCoordinator)
  - Refactoring doc → Section 9.4 (DataUpdateCoordinator async_setup)
- **Provides**: When to use coordinator, update interval guidelines, error handling patterns
- **Activates on**: "coordinator", "polling", "data update"

**5. ha-common-mistakes**
- **Purpose**: Remind about anti-patterns and quality requirements
- **Points to**:
  - New integrations doc → Section 5 (Quality Scale)
  - Refactoring doc → Section 3 (Quality Tier Upgrades)
  - Refactoring doc → Section 2.5 (Entity Availability Handling)
- **Provides**: Bronze tier checklist, async pitfalls, unique ID issues, quality upgrade paths
- **Activates on**: "error", "issue", "best practice", "quality"

---

## Skill Content Structure

Each Skill should contain:

### SKILL.md
- **Description**: Clear, specific description that triggers Claude's auto-activation
- **Purpose**: One sentence on when to use this Skill
- **Research Doc Section Map**: Bulleted list of relevant sections in the two research documents
- **Decision Trees**: "Use X when Y, use Z when W" (from research docs)
- **Key Requirements**: Must-have items (e.g., "100% config flow test coverage" from research doc section 2)
- **Common Questions**: Quick answers with pointers to research doc sections

### Supporting Files (Optional)
- Quick reference checklists
- Decision flowcharts
- Link collections

**What NOT to include:**
- ❌ Direct docs/ file references (point to research doc sections instead)
- ❌ Detailed code examples (those are in research docs)
- ❌ Duplicated research doc content

---

## Success Criteria

- [ ] All five Skills created with clear SKILL.md descriptions
- [ ] Skills activate automatically when relevant topics mentioned
- [ ] Each Skill points to correct research doc sections
- [ ] Navigation tests pass (user asks question → Skill guides to right research doc section)
- [ ] No duplication from research docs

---

## Creation Process

**For each Skill:**

1. **Define scope** - What questions does this Skill answer?
2. **Map research sections** - Which research doc sections are relevant?
3. **Create SKILL.md** - Clear description for auto-activation + section map
4. **Test activation** - Does it activate on relevant prompts?
5. **Validate navigation** - Does it point to the right research doc sections?

**Use Anthropic's `skill-creator` skill** to help with the actual creation process.

---

## Documentation References

**Skills reference these research documents:**

**New Integrations Doc** (595 lines): `thoughts/shared/research/2025-11-20-home-assistant-integration-skill-research.md`
- Section 1: Getting Started
- Section 2: Configuration Flows
- Section 3: Entity Implementation
- Section 4: Testing Requirements
- Section 5: Quality Scale
- Section 6: Core Concepts (async, coordinator)
- Section 7: Development Workflow

**Refactoring Doc** (1,848 lines): `thoughts/shared/research/2025-11-21-home-assistant-integration-refactoring-patterns.md`
- Section 1: Config Flow Refactoring
- Section 2: Entity Refactoring Patterns
- Section 3: Quality Tier Upgrades
- Section 4: Runtime Data Migration
- Section 5: Config Entry Migration
- Section 6: Device & Discovery Patterns
- Section 7: Authentication Flows
- Section 8: Testing Modernization
- Section 9: Common API Deprecations

**Skills point to sections, not to `docs/` directly.** Research docs already reference `docs/` as needed.

---

## Estimated Effort

| Skill | Time | Rationale |
|-------|------|-----------|
| ha-integration-structure | 1-2h | Straightforward file organization |
| ha-entity-knowledge | 2-3h | Most complex, critical for quality |
| ha-config-flow-knowledge | 2-3h | Complex flows, many variations |
| ha-coordinator-knowledge | 1-2h | Focused scope |
| ha-common-mistakes | 1-2h | Checklist-focused |
| **Total** | **8-12h** | |

---

## Next Steps

After Phase 1 complete:
- Proceed to [Phase 2: Commands](phase-2-commands.md)
- Or refine Skills based on usage feedback

**See also:**
- [MVP Approach](mvp-approach.md) - Start with just one Skill first
- [System Architecture](../architecture/overview.md) - How Skills fit in the system
