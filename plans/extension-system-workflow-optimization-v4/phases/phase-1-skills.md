# Phase 1: Knowledge Skills Creation

**Objective:** Create five Skills that guide Claude to relevant documentation

**Duration:** 8-12 hours

**Dependencies:** None - start here

---

## Overview

Phase 1 creates five Skills that act as **navigation guides** to the Home Assistant documentation. These Skills don't duplicate docs/, they point Claude to the right places and provide decision-making context.

**Key Principle:** Skills = "Where to look" + "What to remember", NOT "How to implement"

---

## Deliverables

### Five Knowledge Skills

Create these Skills in `.claude/skills/`:

**1. ha-integration-structure**
- **Purpose**: Guide file organization and manifest creation
- **Points to**:
  - `docs/creating_integration_manifest.md`
  - `docs/creating_integration_file_structure.md`
  - `thoughts/shared/research/2025-11-20-home-assistant-integration-skill-research.md` (sections 1-2)
- **Provides**: File structure checklists, required vs optional files
- **Activates on**: "integration structure", "manifest", "what files"

**2. ha-entity-knowledge** ⭐ Most Critical
- **Purpose**: Guide entity implementation with focus on unique IDs
- **Points to**:
  - `docs/core/entity.md`
  - `docs/entity_registry_index.md`
  - `docs/device_registry_index.md`
  - Research doc sections 3.1-3.4 (entity patterns)
- **Provides**: Decision trees for entity types, unique ID strategies, device info requirements
- **Activates on**: "entity", "sensor", "unique id", "device info"
- **Critical**: Unique ID stability is a common pain point

**3. ha-config-flow-knowledge**
- **Purpose**: Guide config flow implementation
- **Points to**:
  - `docs/config_entries_config_flow_handler.md`
  - `docs/data_entry_flow_index.md`
  - Research doc section 1 (config flow patterns)
  - Refactoring doc section 1 (adding config flows)
- **Provides**: Flow step patterns, error handling checklist, 100% test coverage requirement
- **Activates on**: "config flow", "configuration", "setup wizard"

**4. ha-coordinator-knowledge**
- **Purpose**: Guide DataUpdateCoordinator usage
- **Points to**:
  - `docs/integration_fetching_data.md`
  - Research doc section 6 (coordinator patterns)
  - Refactoring doc section 9.4 (coordinator setup)
- **Provides**: When to use coordinator, update interval guidelines, error handling patterns
- **Activates on**: "coordinator", "polling", "data update"

**5. ha-common-mistakes**
- **Purpose**: Remind about anti-patterns and quality requirements
- **Points to**:
  - `docs/core/integration-quality-scale/index.md`
  - `docs/asyncio_blocking_operations.md`
  - Research doc section 5 (quality scale)
  - Refactoring doc sections 2-3 (entity and quality upgrades)
- **Provides**: Bronze tier checklist, async pitfalls, unique ID issues
- **Activates on**: "error", "issue", "best practice", "quality"

---

## Skill Content Structure

Each Skill should contain:

### SKILL.md
- **Description**: Clear, specific description that triggers Claude's auto-activation
- **Purpose**: One sentence on when to use this Skill
- **Documentation Map**: Bulleted list of relevant docs/ files with brief descriptions
- **Research Links**: Pointers to specific sections in research documents
- **Decision Trees**: "Use X when Y, use Z when W"
- **Key Requirements**: Must-have items (e.g., "100% config flow test coverage")
- **Common Questions**: Quick answers with pointers to details

### Supporting Files (Optional)
- Quick reference checklists
- Decision flowcharts
- Link collections

**What NOT to include:**
- ❌ Detailed code examples (those are in docs/)
- ❌ Comprehensive tutorials (point to docs/)
- ❌ Duplicated documentation content

---

## Success Criteria

- [ ] All five Skills created with clear SKILL.md descriptions
- [ ] Skills activate automatically when relevant topics mentioned
- [ ] Each Skill points to correct docs/ files
- [ ] Skills reference research documents appropriately
- [ ] Navigation tests pass (user asks question → Skill guides to right doc)
- [ ] No code duplication from docs/

---

## Creation Process

**For each Skill:**

1. **Define scope** - What questions does this Skill answer?
2. **Map documentation** - Which docs/ files are relevant?
3. **Create SKILL.md** - Clear description for auto-activation + navigation guide
4. **Test activation** - Does it activate on relevant prompts?
5. **Validate navigation** - Does it point to the right docs?

**Use Anthropic's `skill-creator` skill** to help with the actual creation process.

---

## Documentation References

**All details are in:**
- `thoughts/shared/research/2025-11-20-home-assistant-integration-skill-research.md` - New integration patterns
- `thoughts/shared/research/2025-11-21-home-assistant-integration-refactoring-patterns.md` - Refactoring patterns
- `docs/` directory - Source of truth for implementation

**Skills should reference these, not duplicate them.**

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
