# Phase 2: Specialized Commands

**Objective:** Create HA-specific workflow commands that orchestrate Skills

**Duration:** 6-8 hours

**Dependencies:** Phase 1 (Skills must exist)

---

## Overview

Phase 2 creates three commands that orchestrate HA-specific workflows using the Skills from Phase 1. Commands provide structured, repeatable processes.

**Key Enhancements Over Generic Commands:**
- Explicitly reference relevant Skills
- HA-specific checklists and patterns
- Structured output formats
- Built-in validation points

---

## Deliverables

Three commands in `.claude/commands/`:

### 1. research_ha_integration.md

**Purpose:** HA-specific research protocol

**What it does:**
- Provides file discovery checklist
- Identifies patterns (coordinator, entities, config flow type)
- Auto-references `ha-integration-structure` Skill
- Produces structured output

**Points Skills to:**
- `docs/creating_integration_manifest.md` for manifest analysis
- `docs/creating_integration_file_structure.md` for structure checks
- Research doc sections on patterns

**Effort:** 2-3 hours

### 2. create_plan_ha_integration.md

**Purpose:** Generate HA-specific implementation plans

**What it does:**
- Provides HA-specific plan template
- Decision framework (entity pattern, coordinator, config flow)
- References Skills for pattern selection
- Built-in validation checklists

**Points Skills to:**
- `docs/core/entity.md` for entity decisions
- `docs/integration_fetching_data.md` for coordinator decisions
- Quality scale docs for requirements

**Effort:** 2-3 hours

### 3. implement_plan_ha_integration.md

**Purpose:** Step-by-step implementation protocol

**What it does:**
- Guides through implementation phases
- Continuous validation at each step
- Uses Skills' documentation maps
- Common mistake checks from `ha-common-mistakes` Skill
- Final validation suite

**Points Skills to:**
- All Skills as appropriate per implementation step
- Research docs for patterns
- Testing docs for validation

**Effort:** 2-3 hours

---

## Command Structure

Each command should:
- **Define workflow**: Clear steps and checkpoints
- **Reference Skills**: Explicitly when to activate which Skill
- **Provide checklists**: What to check at each step
- **Structure output**: Consistent, parseable format
- **Point to docs**: Guide to specific `docs/` files as needed

**What NOT to include:**
- ❌ Detailed implementation code (point to Skills/docs)
- ❌ Comprehensive tutorials (guide workflow only)
- ❌ Duplicated Skill content

---

## Testing & Validation

After each command created:
- [ ] Test on simple integration
- [ ] Test on complex integration
- [ ] Verify Skills activate correctly
- [ ] Validate output structure
- [ ] Compare to generic command results

---

## Success Criteria

- [ ] Three commands created
- [ ] Commands reference appropriate Skills
- [ ] Tested on sample integrations
- [ ] Produce better, more structured results than generic commands
- [ ] Skills activate during command execution
- [ ] Documentation complete

---

## Estimated Effort

| Command | Time | Rationale |
|---------|------|-----------|
| research_ha_integration | 2-3h | Research workflow + testing |
| create_plan_ha_integration | 2-3h | Plan template + decision trees |
| implement_plan_ha_integration | 2-3h | Implementation steps + validation |
| **Total** | **6-8h** | |

---

## Next Steps

After Phase 2 complete:
- Proceed to [Phase 3: Validation Sub-agent](phase-3-validator.md)
- Or refine commands based on usage

**See also:**
- [Phase 1](phase-1-skills.md) - Skills these commands use
- [System Architecture](../architecture/overview.md) - How commands fit in the system
