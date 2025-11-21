# Phase 1: Knowledge Skills Foundation + Hook Infrastructure

**Objective:** Create five Skills containing patterns, templates, and checklists + hook-based activation system

**Duration:** 14-20 hours (includes hook setup, testing, and documentation)

**Dependencies:** None - start here

---

## Overview

Phase 1 establishes the foundation for the entire workflow optimization by creating:
1. **Hook infrastructure** - Reliable Skill activation system
2. **Five knowledge Skills** - Patterns, templates, and checklists for HA integration development
3. **Activation configuration** - Trigger patterns in skill-rules.json
4. **Testing framework** - Validation that hooks and Skills work correctly
5. **Documentation** - Guides for using and contributing to Skills

**Critical First Step:** Hook infrastructure must work before creating multiple Skills.

---

## Deliverables

### Skill Activation Infrastructure

**1. Hook Scripts** (from reference implementation)
- `skill-activation-prompt.*` (UserPromptSubmit hook)
- `post-tool-use-tracker.sh` (PostToolUse hook)
- Setup time: ~1-2 hours

**2. Configuration File** (`skill-rules.json`)
- Trigger patterns for all Skills
- File path patterns
- Context definitions
- Maintained throughout phase

**See:** [Hook-Based Activation System](../architecture/hook-system.md) for complete details

### Five Knowledge Skills

Located in `.claude/skills/`:

**1. ha-integration-structure**
- File organization and structure
- manifest.json patterns
- __init__.py setup patterns
- Required files checklists
- Platform file organization
- Templates and examples

**2. ha-entity-knowledge** ⭐ Most Critical
- Entity base classes and patterns
- **Unique ID generation strategies** (critical pain point!)
- Device info patterns
- State and attribute conventions
- Entity lifecycle methods
- Templates for sensors, switches, climate, lights, etc.
- CoordinatorEntity vs polling patterns

**3. ha-config-flow-knowledge**
- Step-based flow patterns (async_step_user, async_step_discovery, etc.)
- Error handling approaches
- Schema definitions and validation
- User input handling
- Options flow patterns
- Discovery and zeroconf integration
- Templates for common flow types

**4. ha-coordinator-knowledge**
- DataUpdateCoordinator patterns
- Update intervals and strategies
- Error handling and recovery
- Authentication refresh patterns
- CoordinatorEntity integration
- Polling vs push strategies
- Template implementations

**5. ha-common-mistakes**
- Anti-patterns to avoid
- Blocking I/O pitfalls in async code
- Unique ID instability issues
- Missing error handling
- Coordinator misuse patterns
- Side-by-side comparisons (bad vs good code)
- Common debugging scenarios

### Each Skill Contains

- **SKILL.md**: Main definition with description and instructions
- **Supporting docs**: 3-5 pattern/reference documents
- **Templates**: 2-3 working code templates
- **Examples**: 2-3 references to real integrations
- **Checklists**: Quick validation lists

**See:** [Skill Creation Template](../implementation/skills/_template.md)

---

## Implementation Steps

### Step 0: Hook Infrastructure Setup (~1-2 hours) - DO THIS FIRST

**Critical:** Hooks must work before creating Skills

**0.1. Preparation**
Read these documents:
- [Hook-Based Activation System](../architecture/hook-system.md)
- [System Architecture Overview](../architecture/overview.md)

Clone reference implementation:
```bash
git clone https://github.com/diet103/claude-code-infrastructure-showcase.git
```

**0.2. Install hook scripts**
```bash
# Copy from reference implementation
cp claude-code-infrastructure-showcase/hooks/skill-activation-prompt.* .claude/hooks/
cp claude-code-infrastructure-showcase/hooks/post-tool-use-tracker.sh .claude/hooks/

# Make executable
chmod +x .claude/hooks/skill-activation-prompt.*
chmod +x .claude/hooks/post-tool-use-tracker.sh
```

**0.3. Create skill-rules.json**
```bash
# At project root or in .claude/
touch skill-rules.json
```

Add initial structure:
```json
{
  "ha-entity-knowledge": {
    "prompt_patterns": ["entity", "sensor", "unique id"],
    "file_patterns": ["**/components/**/sensor.py"],
    "contexts": ["entity implementation"]
  }
}
```

**0.4. Test hook activation**
1. Type in Claude: "How do I create a sensor entity?"
2. Expected: Hook suggests ha-entity-knowledge Skill
3. Verify: Use `/context` command to see if Skill would be loaded

**0.5. Verify hooks running**
Check that hooks execute on prompt submit (consult reference implementation for verification method)

**Checkpoint:** Do NOT proceed until hooks are working

**See:** [Hook System Setup Guide](../architecture/hook-system.md#setup-process)

### Step 1-5: Create Each Skill

**Recommended Order:**
1. ha-entity-knowledge (most critical, test hooks with this)
2. ha-integration-structure
3. ha-config-flow-knowledge
4. ha-coordinator-knowledge
5. ha-common-mistakes

**For each Skill, follow this process:**

#### A. Create Skill Structure

```bash
mkdir -p .claude/skills/[skill-name]/templates
mkdir -p .claude/skills/[skill-name]/examples
touch .claude/skills/[skill-name]/SKILL.md
```

#### B. Write SKILL.md

Follow template structure:
```markdown
# [Skill Name]

**Description:** [What this Skill provides]

**When to use:** [Scenarios where this Skill is relevant]

## Patterns

[Document key patterns]

## Templates

[Reference template files]

## Checklists

[Quick validation lists]

## Examples

[Reference real integrations]
```

**See:** Individual Skill specs in `../implementation/skills/`

#### C. Add Trigger Patterns to skill-rules.json

```json
{
  "[skill-name]": {
    "prompt_patterns": ["keyword1", "keyword2", "phrase"],
    "file_patterns": ["**/path/**/*.py"],
    "contexts": ["context description"]
  }
}
```

**Example for ha-entity-knowledge:**
```json
{
  "ha-entity-knowledge": {
    "prompt_patterns": [
      "entity", "sensor", "switch", "climate",
      "unique id", "unique_id", "device info",
      "entity state", "entity attribute"
    ],
    "file_patterns": [
      "**/homeassistant/components/**/sensor.py",
      "**/homeassistant/components/**/switch.py",
      "**/homeassistant/components/**/*_entity.py"
    ],
    "contexts": ["entity implementation", "platform development"]
  }
}
```

**See:** [skill-rules.json Examples](../examples/skill-rules-examples.json)

#### D. Test Hook-Based Activation

**Prompt-based test:**
1. Type prompt with trigger keywords
2. Hook should suggest the Skill
3. Verify with `/context`

**File-based test:**
1. Open/edit relevant file
2. Hook should suggest the Skill
3. Verify with `/context`

**Combined test:**
1. Open relevant file AND type trigger prompt
2. Should get high-confidence activation

#### E. Add Supporting Documentation

Create 3-5 supporting docs in Skill directory:
- Pattern explanations
- Detailed guides
- Reference material
- Best practices

**Example for ha-entity-knowledge:**
- `entity-base-classes.md`
- `unique-id-strategies.md`
- `device-info-patterns.md`
- `state-and-attributes.md`

#### F. Create Templates

Create 2-3 working code templates:
- Must compile without errors
- Must follow HA patterns
- Must include comments
- Must be copy-paste ready

Store in `templates/` subdirectory

**Example for ha-entity-knowledge:**
- `templates/basic-sensor-entity.py`
- `templates/coordinator-based-entity.py`
- `templates/device-based-entity.py`

#### G. Add Examples

Reference 2-3 real integrations:
- Use current, maintained integrations
- Include file paths
- Note key patterns used
- Link to GitHub (if external) or local paths

**Example for ha-entity-knowledge:**
```markdown
## Examples

1. **Demo Integration Sensor**
   - Path: `homeassistant/components/demo/sensor.py`
   - Pattern: Basic sensor with state classes

2. **Met.no Sensor**
   - Path: `homeassistant/components/met/sensor.py`
   - Pattern: CoordinatorEntity with device info
```

#### H. Create Checklists

Quick validation lists for common tasks:

**Example for ha-entity-knowledge:**
```markdown
## Entity Implementation Checklist

- [ ] Inherits from correct base class (SensorEntity, SwitchEntity, etc.)
- [ ] unique_id property returns stable, unique string
- [ ] name property returns descriptive name
- [ ] If device-based: device_info property returns DeviceInfo
- [ ] State returned from state/is_on property
- [ ] Attributes in extra_state_attributes (if any)
- [ ] No blocking I/O in property getters
- [ ] entity_category set if diagnostic/config
```

#### I. Refine Activation Patterns

Based on testing:
- Add missing keywords
- Remove over-broad patterns
- Adjust file patterns for actual paths
- Test for false positives/negatives

#### J. Document the Skill

Update SKILL.md with:
- Complete usage instructions
- When Skill activates (prompt/file patterns)
- How to use templates
- How to reference examples
- Common questions/troubleshooting

#### K. Move to Next Skill

Repeat A-J for next Skill in sequence

---

## Testing & Validation

### Per-Skill Testing (Do After Each Skill)

**Hook Activation Testing:**
- [ ] Type prompt with trigger keywords → Skill activates
- [ ] Open relevant file → Skill activates
- [ ] Use `/context` → Skill appears in context
- [ ] Activation is reliable (test 5+ times)

**Activation Pattern Tuning:**
- [ ] Test all prompt patterns trigger correctly
- [ ] Test file patterns match actual file paths
- [ ] No false positives (activating when shouldn't)
- [ ] No false negatives (not activating when should)

**Template Validation:**
- [ ] Each template compiles without errors
- [ ] Templates follow current HA patterns
- [ ] Templates include proper imports
- [ ] Templates have helpful comments

**Example Verification:**
- [ ] Example integration references exist
- [ ] File paths are accurate
- [ ] Patterns described are actually in examples
- [ ] Examples use current HA APIs (not deprecated)

**Documentation Quality:**
- [ ] SKILL.md is clear and complete
- [ ] Supporting docs are accurate
- [ ] Checklists cover common scenarios
- [ ] Usage examples are helpful

### Cross-Skill Testing (After Multiple Skills Created)

**No Conflicts:**
- [ ] Multiple Skills can activate simultaneously
- [ ] Skills don't contradict each other
- [ ] Patterns don't overlap excessively
- [ ] Context usage is reasonable when multiple active

**Complementary Patterns:**
- [ ] Skills reference each other appropriately
- [ ] E.g., entity Skill mentions coordinator Skill
- [ ] Cross-references are accurate

### End of Phase Validation

**Hook Infrastructure:**
- [ ] Hook scripts installed and executable
- [ ] skill-rules.json contains patterns for all five Skills
- [ ] skill-rules.json is valid JSON
- [ ] Hooks run on prompt submit
- [ ] Hook activation tested and working reliably

**All Five Skills:**
- [ ] ha-integration-structure complete
- [ ] ha-entity-knowledge complete
- [ ] ha-config-flow-knowledge complete
- [ ] ha-coordinator-knowledge complete
- [ ] ha-common-mistakes complete

**Quality Checks:**
- [ ] All Skills have complete SKILL.md
- [ ] Hook-based activation tested for all Skills
- [ ] All Skills contain actionable templates
- [ ] Templates are working code (not pseudo-code)
- [ ] Examples reference real, current integrations
- [ ] No conflicts between Skills
- [ ] Activation patterns tuned and reliable

**Files Committed:**
- [ ] All Skill directories in `.claude/skills/`
- [ ] skill-rules.json in project root or `.claude/`
- [ ] Hook scripts in `.claude/hooks/`
- [ ] Documentation files created

**See:** [Skill Validation Testing](../testing/skill-validation-tests.md)

---

## Documentation

### Per-Skill Documentation (Create With Each Skill)

**In SKILL.md:**
- Skill purpose and scope
- When Skill activates (trigger patterns)
- How to use templates
- How to reference patterns
- Checklist usage

**In Supporting Docs:**
- Detailed pattern explanations
- Best practices
- Common pitfalls
- Advanced usage

**In skill-rules.json:**
```json
{
  "[skill-name]": {
    // What prompts trigger this Skill
    "prompt_patterns": ["..."],

    // What files trigger this Skill
    "file_patterns": ["..."],

    // When to use this Skill (documentation)
    "contexts": ["..."]
  }
}
```

### End-of-Phase Documentation

**Hook Setup Guide** (`docs/hook-setup.md`):
- How to install and configure hooks
- Understanding skill-rules.json format
- How to add/modify trigger patterns
- Troubleshooting hook activation
- Testing activation works

**Skills Overview Guide** (`docs/skills-overview.md`):
- Purpose of each Skill
- How Skills auto-activate via hooks
- How to verify Skill loaded (use `/context`)
- When to reference Skills manually
- How Skills work together

**Skill Contribution Guide** (`docs/contributing-skills.md`):
- How to add patterns to existing Skills
- How to create new Skills
- How to define trigger patterns
- Template structure and requirements
- Testing new Skills/patterns
- Submitting changes

**Update Main README:**
Add section:
```markdown
## Claude Code Skills

This project uses Claude Code Skills for HA integration development:

- ha-integration-structure - File organization and structure
- ha-entity-knowledge - Entity patterns and unique IDs
- ha-config-flow-knowledge - Configuration flows
- ha-coordinator-knowledge - Data update coordinators
- ha-common-mistakes - Anti-patterns to avoid

Skills activate automatically via hooks. See [Skills Overview](docs/skills-overview.md).
```

**See:** Documentation templates in `../reference/`

---

## Success Criteria

**Infrastructure:**
- ✅ Hook infrastructure installed and functional
- ✅ skill-rules.json configured for all Skills
- ✅ Hooks tested and reliable
- ✅ Reference to infrastructure-showcase repo documented

**Skills:**
- ✅ All five Skills created with complete SKILL.md
- ✅ Hook-based activation tested and working reliably
- ✅ Skills contain actionable templates and examples
- ✅ Templates compile and follow HA patterns
- ✅ All files committed to `.claude/skills/`

**Testing:**
- ✅ Skills tested and validated with hooks
- ✅ No conflicts between Skills
- ✅ Activation patterns tuned for accuracy
- ✅ False positive rate < 10%

**Documentation:**
- ✅ Hook setup guide complete
- ✅ Skills overview guide complete
- ✅ Contribution guide complete
- ✅ README updated with Skills section
- ✅ Each Skill documented

**Team Readiness:**
- ✅ Team can use Skills during development
- ✅ Team can verify Skills loaded (`/context`)
- ✅ Team can contribute new patterns
- ✅ Team understands hook-based activation

---

## Common Issues & Solutions

### Hook Installation Issues

**Problem:** Hooks don't execute
**Solution:**
1. Check hooks are executable: `ls -la .claude/hooks/`
2. Run: `chmod +x .claude/hooks/*`
3. Verify hook file names match reference implementation
4. Check Claude Code settings for hook configuration

### skill-rules.json Syntax Errors

**Problem:** JSON parsing errors
**Solution:**
1. Validate JSON: `cat skill-rules.json | jq .`
2. Check for missing commas, quotes, brackets
3. Use JSON linter in editor

### Skills Not Activating

**Problem:** Hooks run but Skills don't activate
**Solution:**
1. Check patterns in skill-rules.json match actual prompts/files
2. Test with exact pattern: "sensor" if "sensor" in patterns
3. Verify Skill name in skill-rules.json matches directory name
4. Check SKILL.md exists and is valid

### False Positives

**Problem:** Skills activate when they shouldn't
**Solution:**
1. Make patterns more specific
2. Remove overly broad keywords
3. Use longer phrase patterns instead of single words
4. Tighten file patterns to specific paths

### False Negatives

**Problem:** Skills don't activate when they should
**Solution:**
1. Add missing keywords to prompt_patterns
2. Broaden file patterns
3. Check for typos in patterns
4. Test with multiple variations of prompts

---

## Time Estimates

| Activity | Time | Notes |
|----------|------|-------|
| Hook infrastructure setup | 1-2h | Critical first step |
| ha-entity-knowledge | 3-4h | Most complex, do first |
| ha-integration-structure | 2-3h | Straightforward |
| ha-config-flow-knowledge | 3-4h | Complex flows |
| ha-coordinator-knowledge | 2-3h | Focused patterns |
| ha-common-mistakes | 2-3h | Collection of anti-patterns |
| Testing & tuning | 2-3h | Across all Skills |
| Documentation | 1-2h | Guides and README |

**Total:** 14-20 hours

**Can parallelize:** Multiple people can work on different Skills simultaneously after hook infrastructure is set up

---

## Next Steps

**After Phase 1 Complete:**
→ Proceed to [Phase 2: Specialized Commands](phase-2-commands.md)

**If Doing MVP First:**
→ See [MVP Approach](mvp-approach.md) for streamlined path

---

## Resources

**Architecture:**
- [System Architecture Overview](../architecture/overview.md)
- [Hook-Based Activation System](../architecture/hook-system.md)
- [Component Interaction Model](../architecture/component-interaction.md)

**Implementation:**
- [Skill Creation Template](../implementation/skills/_template.md)
- Individual Skill specs in `../implementation/skills/`

**Testing:**
- [Hook Activation Testing](../testing/hook-activation-tests.md)
- [Skill Validation Testing](../testing/skill-validation-tests.md)

**Examples:**
- [skill-rules.json Examples](../examples/skill-rules-examples.json)

**Reference:**
- [claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase)

---

**See Also:**
- [MVP Approach](mvp-approach.md) - Start here for trial
- [Phase 2: Commands](phase-2-commands.md) - Next phase
- [Back to Main README](../README.md)
