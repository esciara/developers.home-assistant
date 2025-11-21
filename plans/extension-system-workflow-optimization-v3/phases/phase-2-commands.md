# Phase 2: Specialized Commands

**Objective:** Create HA-specific workflow commands that leverage Skills

**Duration:** 8-12 hours (includes testing and documentation)

**Dependencies:** Phase 1 (Skills must exist)

---

## Overview

Phase 2 creates three specialized commands that orchestrate HA-specific workflows using the Skills created in Phase 1. Commands provide structured, repeatable processes for research, planning, and implementation.

**Key Enhancements Over Generic Commands:**
- Explicitly activate relevant Skills
- HA-specific search patterns and checks
- Structured output formats
- Built-in validation points
- Reference Skills throughout workflow

---

## Deliverables

Three specialized commands in `.claude/commands/`:

### 1. research_ha_integration.md

**Purpose:** HA-specific research protocol for existing integrations

**Key Features:**
- File discovery checklist (manifest.json, __init__.py, platforms, config_flow, etc.)
- Pattern recognition guidance (coordinator usage, entity types, config flow type)
- Auto-activates `ha-integration-structure` Skill
- Structured output format (file structure, patterns identified, architecture notes)
- Reference integration finder

**Output Structure:**
```markdown
# [Integration Name] Research

## File Structure
- manifest.json: [findings]
- __init__.py: [findings]
- Platforms: [list]
...

## Patterns Identified
- Coordinator: [Yes/No, details]
- Entity types: [list]
- Config flow: [type]
...

## Architecture Notes
[Key observations]
```

**See:** [research_ha_integration spec](../implementation/commands/research-ha-integration.md)

### 2. create_plan_ha_integration.md

**Purpose:** Generate HA-specific implementation plans

**Key Features:**
- HA-specific plan template structure
- Architecture decision framework (entity pattern, coordinator yes/no, etc.)
- References Skills for pattern selection
- Built-in validation checklists from Skills
- Clear success criteria

**Output Structure:**
```markdown
# [Integration Name] Implementation Plan

## Architecture Decisions
### Entity Implementation
Pattern: [CoordinatorEntity/PollingEntity]
Rationale: [why]
Unique ID Strategy: [pattern]

### Config Flow
Pattern: [type]
Steps: [list]

## Implementation Steps
[Detailed step-by-step]

## Success Criteria
[Checkboxes]
```

**See:** [create_plan_ha_integration spec](../implementation/commands/create-plan-ha-integration.md)

### 3. implement_plan_ha_integration.md

**Purpose:** Step-by-step implementation protocol with continuous validation

**Key Features:**
- Step-by-step implementation protocol
- Continuous validation at each step (after manifest, after __init__, etc.)
- Uses Skills' templates automatically
- Common mistake checks (references ha-common-mistakes Skill)
- Final validation suite (launches ha-integration-validator sub-agent)

**Workflow:**
1. Verify plan exists
2. Create manifest.json (validate)
3. Create __init__.py (validate)
4. Create coordinator (if needed, validate)
5. Create config_flow (validate)
6. Create platforms (validate each)
7. Final validation (launch sub-agent)

**See:** [implement_plan_ha_integration spec](../implementation/commands/implement-plan-ha-integration.md)

---

## Implementation Steps

### Incremental Approach

Implement and validate each command individually:

1. **Create command structure and workflow**
2. **Test command on sample integration**
3. **Verify Skills activate correctly during execution**
4. **Refine command based on test results**
5. **Document the command with examples**
6. **Move to next command**

### Per-Command Process

#### A. Create Command File

```bash
touch .claude/commands/[command-name].md
```

#### B. Write Command Content

Follow template structure:
```markdown
# [Command Name]

**Purpose:** [What this command does]

**Usage:** /[command-name] [args]

## Instructions for Claude

[Detailed step-by-step instructions]

## Skills to Activate

[List Skills this command should use]

## Output Format

[Expected output structure]

## Validation Steps

[What to check at each step]
```

**See:** [Command Creation Template](../implementation/commands/_template.md)

#### C. Test Command

**Test on simple integration:**
- Run command
- Verify Skills activate
- Check output structure
- Validate results

**Test on medium complexity integration:**
- More complex patterns
- Multiple platforms
- Config flow present
- Coordinator usage

#### D. Refine Command

Based on testing:
- Improve workflow steps
- Add missing checks
- Enhance output structure
- Ensure Skill activation reliable

#### E. Document Command

Create documentation:
- Usage instructions
- Example invocations
- Expected output
- When to use vs generic commands

---

## Testing & Validation

### Per-Command Testing

**Functional Testing:**
- [ ] Command accessible via `/command-name`
- [ ] Runs on simple integration successfully
- [ ] Runs on medium complexity integration successfully
- [ ] Produces expected output structure
- [ ] Output is HA-compliant

**Skill Activation Testing:**
- [ ] Expected Skills activate during execution
- [ ] Skills provide relevant context
- [ ] No unexpected Skills activate

**Workflow Testing:**
- [ ] Command produces better results than generic version
- [ ] Workflow is clear and easy to follow
- [ ] Validation points catch issues
- [ ] Output is actionable

**Error Handling:**
- [ ] Handles missing files gracefully
- [ ] Handles unexpected structures
- [ ] Provides helpful error messages

### End of Phase Validation

**All Three Commands:**
- [ ] research_ha_integration tested on 3+ integrations
- [ ] create_plan_ha_integration produces valid plans
- [ ] implement_plan_ha_integration creates working code
- [ ] Commands work together in sequence (research → plan → implement)

**Integration Testing:**
- [ ] Run complete workflow on test integration
- [ ] research → plan → implement produces working integration
- [ ] Skills activate at appropriate points
- [ ] Validation catches real issues

**Quality Checks:**
- [ ] Commands produce HA-compliant output
- [ ] Workflow improvement measurable vs generic commands
- [ ] Commands documented with examples
- [ ] Team can use commands successfully

---

## Documentation

### Per-Command Documentation

**For each command, document:**
- Command purpose and usage
- Parameters and arguments
- Expected inputs
- Output structure
- Examples with real integrations
- When to use this command
- Troubleshooting tips

### End-of-Phase Documentation

**Commands Guide** (`docs/commands-guide.md`):
- Purpose and usage of each command
- When to use which command
- Command workflow and orchestration
- Parameters and options
- Examples for each command
- Comparison to generic commands

**Workflow Tutorial** (`docs/ha-workflow-tutorial.md`):
- Step-by-step walkthrough using commands
- Real integration example from start to finish
- How commands work together
- How Skills enhance commands
- Common patterns and tips
- Troubleshooting workflow issues

**Update README:**
Add commands section:
```markdown
## Claude Code Commands

HA-specific workflow commands:

- `/research_ha_integration <name>` - Research existing integrations
- `/create_plan_ha_integration <name>` - Create implementation plan
- `/implement_plan_ha_integration` - Implement planned integration

See [Commands Guide](docs/commands-guide.md) for details.
```

---

## Success Criteria

**Commands Created:**
- ✅ research_ha_integration command created
- ✅ create_plan_ha_integration command created
- ✅ implement_plan_ha_integration command created
- ✅ All commands accessible via `/command-name`

**Skills Integration:**
- ✅ Commands automatically leverage Skills
- ✅ Skills activate automatically during command execution
- ✅ Commands reference Skill patterns correctly
- ✅ Skill templates used in implementation command

**Testing:**
- ✅ Commands tested on sample integrations
- ✅ Produce better results than generic versions
- ✅ Workflow tested end-to-end
- ✅ Error handling works correctly

**Documentation:**
- ✅ Commands documented with examples
- ✅ Workflow tutorial complete
- ✅ README updated
- ✅ Team trained on command usage

---

## Time Estimates

| Command | Time | Notes |
|---------|------|-------|
| research_ha_integration | 2-3h | Research protocol + testing |
| create_plan_ha_integration | 3-4h | Plan template + validation |
| implement_plan_ha_integration | 3-4h | Most complex workflow |
| Testing all commands | 1-2h | End-to-end validation |
| Documentation | 1-2h | Guides and tutorial |

**Total:** 8-12 hours

---

## Next Steps

**After Phase 2 Complete:**
→ Proceed to [Phase 3: Validation Sub-agent](phase-3-validator.md)

**Can Start Early:**
Begin Phase 3 once implement_plan_ha_integration is working

---

## Resources

**Implementation:**
- [Command Creation Template](../implementation/commands/_template.md)
- [research_ha_integration spec](../implementation/commands/research-ha-integration.md)
- [create_plan_ha_integration spec](../implementation/commands/create-plan-ha-integration.md)
- [implement_plan_ha_integration spec](../implementation/commands/implement-plan-ha-integration.md)

**Testing:**
- [Command Integration Testing](../testing/command-integration-tests.md)

**Reference:**
- [Component Interaction Model](../architecture/component-interaction.md)

---

**See Also:**
- [Phase 1: Skills](phase-1-skills.md) - Previous phase
- [Phase 3: Validator](phase-3-validator.md) - Next phase
- [Back to Main README](../README.md)
