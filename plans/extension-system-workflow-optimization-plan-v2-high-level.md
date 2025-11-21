# Extension System Workflow Optimization Plan v2 (High-Level)

**Created:** 2025-11-21
**Target:** Home Assistant Integration Development
**Scope:** Optimize Claude Code workflow using native Skills, Commands, and Sub-agents

---

## Executive Summary

This plan enhances the Claude Code workflow (research → plan → implement) for extension-based systems like Home Assistant integrations using **100% Claude Code native features**:

- **Skills**: Knowledge base (patterns, templates, checklists) - auto-invoked by Claude
- **Commands**: Workflow orchestration (research, plan, implement) - user-invoked
- **Sub-agents**: Complex execution tasks (validation, analysis) - tool-invoked

**Key Benefits:**
- **Auto-discovery**: Claude uses Skills automatically when context matches
- **Progressive disclosure**: Only loads what's needed (efficient context usage)
- **Git-native**: All in `.claude/` directory, version controlled
- **Team sharing**: Instant availability via git pull

**Expected Impact:**
- 35-45% reduction in total workflow time
- 40-50% faster research phase
- 60% fewer implementation errors
- 70% fewer validation failures

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

### How Components Work Together

1. User invokes: `/research_ha_integration`
2. Command activates relevant Skills automatically
3. Claude uses Skills' patterns/templates during work
4. Command may launch sub-agents for complex analysis
5. Skills provide context throughout entire workflow

### Why Skills Over thoughts/

| Aspect | Skills (v2) | thoughts/ (v1) |
|--------|-------------|----------------|
| Discovery | Hook-based (reliable) | Manual reference |
| Loading | Progressive | Manual reads |
| Invocation | Automatic via hooks | Explicit |
| Tool restrictions | `allowed-tools` | None |
| Context efficiency | High | Medium |

**Note on Skill Activation:** Skills' built-in auto-triggering based on descriptions doesn't work reliably in Claude Code. This plan uses a **hook-based activation system** (see "Skill Activation Hooks" section below) for reliable, context-aware Skill activation.

---

## Skill Activation Hooks

### Problem Statement

Claude Code Skills' built-in auto-activation based on SKILL.md descriptions is unreliable. Skills often "just sit there" waiting to be manually invoked, defeating the purpose of automatic knowledge activation.

### Solution: Hook-Based Activation

Implement a hook-based system that analyzes prompts and file context to automatically suggest and activate relevant Skills.

**Reference Implementation:** [claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase/blob/main/README.md)

### Core Components

**1. UserPromptSubmit Hook** (`skill-activation-prompt.*`)
- Runs on every user prompt
- Analyzes prompt text and file context
- Checks against `skill-rules.json` configuration
- Automatically suggests relevant Skills
- Works transparently without user intervention

**2. PostToolUse Hook** (`post-tool-use-tracker.sh`)
- Tracks which tools are used during session
- Maintains context about active Skills
- Enables progressive Skill engagement

**3. Configuration File** (`skill-rules.json`)
- Defines trigger patterns for each Skill
- Maps keywords, file patterns, and contexts to Skills
- Enables customization without hook modification

### Implementation in This Plan

For each Skill created in Phase 1, we'll define:

**In SKILL.md:**
- Clear description and purpose
- Detailed patterns and templates

**In skill-rules.json:**
```json
{
  "ha-entity-knowledge": {
    "prompt_patterns": [
      "entity", "sensor", "switch", "climate",
      "unique id", "unique_id", "device info"
    ],
    "file_patterns": [
      "**/homeassistant/components/**/sensor.py",
      "**/homeassistant/components/**/switch.py",
      "**/homeassistant/components/**/*_entity.py"
    ],
    "contexts": ["entity implementation", "platform development"]
  },
  "ha-integration-structure": {
    "prompt_patterns": [
      "manifest", "integration structure", "required files",
      "__init__.py", "manifest.json"
    ],
    "file_patterns": [
      "**/homeassistant/components/**/manifest.json",
      "**/homeassistant/components/**/__init__.py"
    ],
    "contexts": ["integration setup", "file organization"]
  }
}
```

### Setup Requirements

**Initial Setup** (add to Phase 1, ~1-2 hours):
1. Install hook scripts from reference implementation
2. Create `skill-rules.json` configuration file
3. Define trigger patterns for each Skill
4. Test hook activation with sample prompts

**Per-Skill Configuration** (add to each Skill, ~15-30 min):
- Define prompt patterns (keywords that trigger Skill)
- Define file patterns (file paths that trigger Skill)
- Define contexts (scenarios that trigger Skill)
- Test activation rules with real examples

### Benefits of Hook-Based Approach

- ✅ **Reliable activation**: Works consistently, not dependent on Claude's description parsing
- ✅ **Context-aware**: Activates based on files being edited, not just prompts
- ✅ **Configurable**: Easy to tune trigger patterns without modifying Skills
- ✅ **Transparent**: Works automatically without user remembering to invoke Skills
- ✅ **Progressive loading**: Main Skill loads first, detailed resources on-demand
- ✅ **Fast setup**: ~15 minutes to implement basic system

### Testing Skill Activation

After implementing hooks, test activation:
1. Open relevant file (e.g., `sensor.py`) → should suggest ha-entity-knowledge
2. Type relevant prompt (e.g., "How do I create a sensor?") → should suggest ha-entity-knowledge
3. Use `/context` command to verify Skills are loaded
4. Refine `skill-rules.json` patterns based on results

---

## Phase 1: Knowledge Skills Foundation

**Objective:** Create Skills containing patterns, templates, and checklists + hook-based activation system

**Duration:** 14-20 hours (includes hook setup, testing, and documentation)

### Deliverables

**Skill Activation Infrastructure:**
1. **Hook scripts** (from reference implementation)
   - `skill-activation-prompt.*` (UserPromptSubmit hook)
   - `post-tool-use-tracker.sh` (PostToolUse hook)
   - Setup time: ~1-2 hours

2. **Configuration file** (`skill-rules.json`)
   - Trigger patterns for all Skills
   - File path patterns
   - Context definitions
   - Maintained throughout phase

**Five knowledge Skills in `.claude/skills/`:**

1. **ha-integration-structure**
   - File organization, required files
   - manifest.json patterns
   - __init__.py patterns
   - Templates and examples
   - Checklists

2. **ha-entity-knowledge** ⭐ Most Critical
   - Entity base classes and patterns
   - Unique ID generation strategies (critical!)
   - Device info patterns
   - State and attribute conventions
   - Templates for sensors, switches, climate, etc.

3. **ha-config-flow-knowledge**
   - Step-based flow patterns
   - Error handling approaches
   - Schema definitions
   - User input validation
   - Templates for common flows

4. **ha-coordinator-knowledge**
   - DataUpdateCoordinator patterns
   - Update intervals and strategies
   - Error handling and recovery
   - Authentication refresh
   - CoordinatorEntity integration

5. **ha-common-mistakes**
   - Anti-patterns to avoid
   - Blocking I/O pitfalls
   - Unique ID instability issues
   - Missing error handling
   - Side-by-side comparisons (bad vs good)

### Each Skill Contains

- **SKILL.md**: Main definition with description and instructions
- **Supporting docs**: 3-5 pattern/reference documents
- **Templates**: 2-3 working code templates
- **Examples**: 2-3 references to real integrations
- **Checklists**: Quick validation lists

### Incremental Approach

**Step 0: Setup Hook Infrastructure** (~1-2 hours, do first)
1. Install hook scripts from reference implementation
2. Create initial `skill-rules.json` file
3. Test basic hook functionality
4. Verify hooks run on prompt submit

**Per-Skill Development** (repeat for each Skill):
1. Create Skill structure and SKILL.md
2. Add trigger patterns to `skill-rules.json`
3. Test hook-based activation works
4. Add supporting docs and templates
5. Validate templates work with real code
6. Refine activation patterns based on testing
7. Document the Skill
8. Move to next Skill

### Testing & Validation (End of Phase)

After each Skill is created:
- **Hook Activation Testing**: Verify hook-based activation works
  - Type prompt: "How do I create a sensor entity?" → hook should activate ha-entity-knowledge
  - Open file: `sensor.py` → hook should suggest ha-entity-knowledge
  - Use `/context` to verify Skill loaded
- **Activation Pattern Tuning**: Refine `skill-rules.json` based on results
  - Add missing keywords that should trigger Skill
  - Remove keywords that cause false positives
  - Test file pattern matching works
- **Template Validation**: Verify each template compiles and follows HA patterns
- **Example Verification**: Confirm real integration references are accurate
- **Cross-Skill Testing**: Test that multiple Skills work together without conflicts

Final phase validation:
- ✅ Hook infrastructure installed and working
- ✅ `skill-rules.json` contains patterns for all five Skills
- ✅ All five Skills tested with hook-based activation
- ✅ Skills activate automatically via hooks (not manual invocation)
- ✅ Templates are working code (not pseudo-code)
- ✅ No conflicts between Skills
- ✅ Activation patterns tuned and reliable

### Documentation (End of Phase)

After each Skill is created:
- Document Skill purpose and usage in SKILL.md
- Add inline documentation to templates
- Create examples showing Skill in action
- Document trigger patterns in `skill-rules.json` with comments

Final phase documentation:
- **Hook Setup Guide** (`docs/hook-setup.md`)
  - How to install and configure hooks
  - Understanding `skill-rules.json` format
  - How to add/modify trigger patterns
  - Troubleshooting hook activation
- **Skills Overview Guide** (`docs/skills-overview.md`)
  - Purpose of each Skill
  - How Skills auto-activate via hooks
  - How to verify Skill loaded (`/context`)
  - When to reference Skills manually
- **Skill Contribution Guide** (`docs/contributing-skills.md`)
  - How to add patterns to existing Skills
  - How to create new Skills
  - How to define trigger patterns
  - Template structure and requirements
- **Update README** with Skills section and hook system overview

### Success Criteria

- ✅ Hook infrastructure installed and functional
- ✅ `skill-rules.json` configured for all Skills
- ✅ All five Skills created with complete SKILL.md
- ✅ Hook-based activation tested and working reliably
- ✅ Skills contain actionable templates and examples
- ✅ Team can reference Skills during development
- ✅ All files committed to `.claude/skills/`
- ✅ Skills tested and validated with hooks
- ✅ Documentation complete and reviewed
- ✅ Reference to infrastructure-showcase repo included

---

## Phase 2: Specialized Commands

**Objective:** Create HA-specific workflow commands that leverage Skills

**Duration:** 8-12 hours (includes testing and documentation)

### Deliverables

Three specialized commands in `.claude/commands/`:

1. **research_ha_integration.md**
   - Extends generic research command
   - HA-specific file analysis protocol
   - Auto-activates relevant Skills
   - Pattern recognition guidance
   - Reference integration finder
   - Structured output format

2. **create_plan_ha_integration.md**
   - HA-specific plan template
   - Architecture decision framework
   - References Skills for patterns
   - Built-in validation checklists
   - Clear success criteria

3. **implement_plan_ha_integration.md**
   - Step-by-step implementation protocol
   - Continuous validation at each step
   - Uses Skills' templates
   - Common mistake checks
   - Final validation suite

### Key Enhancements Over Generic Commands

- Explicitly activate relevant Skills
- HA-specific search patterns and checks
- Structured output formats
- Built-in validation points
- Reference Skills throughout workflow

### Incremental Approach

Implement and validate each command individually:
1. Create command structure and workflow
2. Test command on sample integration
3. Verify Skills activate correctly during execution
4. Refine command based on test results
5. Document the command with examples
6. Move to next command

### Testing & Validation (End of Phase)

After each command is created:
- **Functional Testing**: Run command on sample integration
  - Test research command on existing integration
  - Test planning command produces valid plan
  - Test implementation command creates working code
- **Skill Activation Testing**: Verify Skills auto-activate during command execution
- **Workflow Testing**: Test command produces better results than generic version
- **Error Handling**: Test command behavior with edge cases

Final phase validation:
- ✅ All three commands tested on simple integration
- ✅ Commands tested on medium complexity integration
- ✅ Skills activate automatically at appropriate points
- ✅ Commands produce HA-compliant output
- ✅ Workflow improvement measurable vs generic commands

### Documentation (End of Phase)

After each command is created:
- Document command usage and parameters
- Create command examples with real integrations
- Document expected inputs and outputs
- Add troubleshooting tips

Final phase documentation:
- **Commands Guide** (`docs/commands-guide.md`)
  - Purpose and usage of each command
  - When to use which command
  - Command workflow and orchestration
  - Examples for each command
- **Workflow Tutorial** (`docs/ha-workflow-tutorial.md`)
  - Step-by-step walkthrough using commands
  - Real integration example from start to finish
  - Common patterns and tips
- **Update README** with commands section

### Success Criteria

- ✅ Three specialized commands created
- ✅ Commands automatically leverage Skills
- ✅ Commands tested on sample integration
- ✅ Produce better results than generic versions
- ✅ Skills activate automatically during command execution
- ✅ Commands documented with examples
- ✅ Workflow tutorial complete

---

## Phase 3: Validation Sub-agent

**Objective:** Create specialized sub-agent for HA integration validation

**Duration:** 6-10 hours (includes testing and documentation)

### Deliverables

1. **ha-integration-validator** agent in `.claude/agents/`
   - Validates manifest.json completeness
   - Checks file structure and naming
   - Analyzes unique ID stability patterns
   - Detects blocking I/O in async contexts
   - Verifies error handling presence
   - Runs automated tools (hassfest, mypy, pylint)
   - References all Skills for validation rules

2. **Validation scripts** (optional helpers)
   - unique ID stability checker
   - async pattern validator
   - manifest deep validator

### Integration Points

- Called from implement_plan_ha_integration command
- Can be invoked manually: `Task: ha-integration-validator`
- Provides detailed, actionable reports

### Incremental Approach

Implement and validate validator components:
1. Create basic validator agent structure
2. Add manifest validation
3. Test on existing integrations, refine rules
4. Add code quality validation (async patterns, etc.)
5. Test and tune false positive rate
6. Add automated tool integration (hassfest, mypy, pylint)
7. Test complete validator, document usage

### Testing & Validation (End of Phase)

Validation testing on real integrations:
- **Known-Good Testing**: Run validator on established integrations
  - Should produce minimal false positives
  - Should validate without breaking existing workflows
- **Known-Issues Testing**: Run on integrations with known issues
  - Should catch common mistakes (blocking I/O, unstable unique IDs)
  - Should provide actionable feedback
- **False Positive Tuning**: Measure and tune validator rules
  - Target: < 10% false positive rate
  - Adjust thresholds and rules based on feedback
- **Integration Testing**: Test validator within command workflows
  - Called automatically from implement_plan_ha_integration
  - Manual invocation works correctly

Final phase validation:
- ✅ Validator tested on 5+ existing integrations
- ✅ False positive rate < 10%
- ✅ Catches known issues reliably
- ✅ Provides actionable, clear feedback
- ✅ Integrates smoothly with implementation command
- ✅ Performance acceptable (< 30s for typical integration)

### Documentation (End of Phase)

Documentation deliverables:
- **Validator Usage Guide** (`docs/validator-guide.md`)
  - How to use validator manually
  - Understanding validator reports
  - Common issues and fixes
  - How to adjust validation rules
- **Complete Workflow Guide** (`docs/claude-ha-integration-workflow.md`)
  - Full end-to-end workflow including validation
  - Skills → Commands → Validator integration
  - Troubleshooting complete workflow
  - Real examples from start to finish
- **Update README** with complete workflow overview
- **Team Training Materials**
  - Quick reference card
  - Video walkthrough (optional)
  - FAQ document

### Success Criteria

- ✅ Validator agent created and functional
- ✅ Uses all five knowledge Skills
- ✅ Runs automated validation tools
- ✅ Provides actionable feedback
- ✅ False positive rate < 10%
- ✅ Validator tested and tuned on real integrations
- ✅ Complete workflow documentation finished
- ✅ Team trained and ready to use workflow

---

## Timeline Summary

**Integrated Testing & Documentation Approach:**
Each phase now includes its own testing and documentation, delivered incrementally as components are completed. This ensures continuous validation and knowledge capture throughout development.

**Hook-Based Activation System:**
Phase 1 includes setup of hook-based Skill activation system (adds ~1-2h) for reliable, automatic Skill triggering.

| Phase | Description | Effort (incl. hooks, test & docs) | Dependencies |
|-------|-------------|----------------------------------|--------------|
| 1 | Knowledge Skills Foundation + Hooks | 14-20h | None |
| 2 | Specialized Commands | 8-12h | Phase 1 |
| 3 | Validation Sub-agent | 6-10h | Phases 1-2 |

**Total Estimated Effort:** 28-42 hours

**Key Changes from Original Plan:**
- Testing and documentation integrated into each phase (not separate phases)
- Reduced total effort by eliminating phase boundaries and handoffs
- Faster feedback loops through incremental validation
- Documentation created alongside implementation (not after)
- Each phase delivers fully tested and documented components

**Phases can be parallelized where dependencies allow:**
- Phases 1-2 can partially overlap (start commands while finishing Skills)
- Phase 3 can start once Phase 2 complete

**Incremental Development Within Phases:**
- Each Skill/Command/Component tested individually before moving to next
- Documentation written as each component is completed
- Continuous refinement based on immediate feedback

---

## Success Metrics

### Quantitative (vs. Generic Workflow Baseline)

- **Research time:** Reduce by 40-50%
- **Planning iterations:** Reduce from 2-3 to 1
- **Implementation errors:** Reduce by 60%
- **Validation failures:** Reduce by 70%
- **Total workflow time:** Reduce by 35-45%

### Qualitative

- Skills activate automatically when context matches
- Commands produce HA-compliant plans consistently
- Implementation quality matches existing integrations
- Fewer "what pattern should I use?" questions
- New contributors successful with workflow
- Knowledge captured and reusable

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Skills don't auto-activate | High | **SOLVED**: Use hook-based activation system instead of built-in auto-triggering. Test patterns in `skill-rules.json` immediately |
| Hook configuration becomes complex | Medium | Start simple, document patterns clearly, use reference implementation as guide |
| Skill content becomes outdated | Medium | Version control, establish regular review schedule |
| Commands too rigid for edge cases | Medium | Include escape hatches, allow deviations with justification |
| Validation too strict/false positives | Medium | Tune thresholds incrementally during development, allow manual overrides |
| HA API changes break patterns | Medium | Monitor HA releases, update Skills promptly |
| Team doesn't adopt new workflow | Low | Create clear documentation incrementally, demonstrate value early, provide training |
| Testing delays development | Medium | Integrated testing approach allows parallel work, faster feedback |
| Documentation becomes stale | Low | Documentation created alongside code, easier to keep synchronized |
| Hooks break or interfere with workflow | Low | Use proven reference implementation, test thoroughly, hooks run transparently |

---

## Quick Start (MVP Approach)

For fastest value delivery, implement minimal version first:

### MVP Components (14-18 hours, includes hooks, testing & documentation)

**Hook Infrastructure Setup** (~1-2 hours, do first)
- Install `skill-activation-prompt.*` hook
- Install `post-tool-use-tracker.sh` hook
- Create basic `skill-rules.json`
- **Test**: Verify hooks run on prompt submit
- **Document**: Basic hook setup guide

**One Skill:** ha-entity-knowledge (most critical)
- Entity patterns and templates
- Unique ID guidance
- 2-3 templates
- 1 checklist
- Add trigger patterns to `skill-rules.json`
- **Test**: Verify hook activates Skill on entity questions and when editing sensor.py
- **Document**: Skill usage guide + activation patterns

**One Command:** research_ha_integration
- HA-specific research protocol
- References ha-entity-knowledge Skill
- Structured output
- **Test**: Run on 2-3 existing integrations
- **Document**: Command usage with examples

**No sub-agent initially** (use manual validation)

### MVP Benefits

- Immediate improvement in research phase
- Validates approach before full investment
- Provides foundation for expansion
- Team can start using immediately
- Each component tested and documented
- Faster feedback on approach viability
- **Hook-based activation proven reliable before scaling**

### Expansion Path (Incremental, with testing & docs at each step)

Once MVP proves valuable, incrementally add:
1. ha-integration-structure Skill (test + document)
2. create_plan_ha_integration Command (test + document)
3. ha-config-flow-knowledge Skill (test + document)
4. implement_plan_ha_integration Command (test + document)
5. Remaining Skills - coordinator, common-mistakes (test + document each)
6. Validation sub-agent (test + document)

---

## Future Enhancements (Post-Initial Implementation)

### Potential Phase 6+ Ideas

1. **Specialized Skills per Integration Type**
   - Climate-specific patterns
   - Light-specific patterns
   - Media player patterns

2. **Migration Skills**
   - Async migration patterns
   - Config entry migration patterns
   - Legacy integration upgrades

3. **Testing and Performance Skills**
   - Testing patterns and fixtures
   - Mocking strategies
   - Performance optimization patterns

4. **Multi-System Support**
   - Adapt for ESPHome, HACS, etc.
   - Generic extension-system patterns
   - System-specific specializations

5. **Advanced Automation**
   - Pattern mining from existing integrations
   - Auto-suggest similar integrations
   - Interactive guided wizard

---

## Recommendation

**Suggested Approach (Integrated Testing & Documentation with Hook-Based Activation):**

1. **Week 1-2**: Implement MVP (hook infrastructure + ha-entity-knowledge Skill + research command)
   - 14-18 hours (includes hook setup, testing and documentation)
   - **Day 1**: Setup hook infrastructure (~1-2h)
   - Test hook activation immediately
   - Build one Skill with hook-based activation
   - Document as you build
   - Validate approach with real integrations
   - Get team feedback early on hook reliability

2. **Week 3-4**: Complete Phase 1 & 2 (all Skills + all commands)
   - 22-32 hours total (includes incremental testing and documentation)
   - Add trigger patterns to `skill-rules.json` for each Skill
   - Test each Skill/Command individually before moving to next
   - Tune activation patterns based on real usage
   - Document each component as completed
   - Continuous refinement based on immediate feedback
   - Provides complete, tested, documented workflow
   - Major value delivered

3. **Week 5-6**: Add validation (Phase 3)
   - 6-10 hours (includes testing and documentation)
   - Test validator on existing integrations
   - Tune rules based on real-world feedback
   - Complete end-to-end workflow documentation
   - Enable team adoption
   - Establish contribution process

**Total timeline:** 4-6 weeks (depending on available time per week)

**Key Benefits of This Approach:**
- **Reliable activation**: Hook-based system proven more reliable than built-in auto-triggering
- **Faster feedback**: Testing happens immediately, not at the end
- **Better quality**: Issues caught and fixed during development
- **Reduced rework**: Documentation synchronized with code
- **Lower risk**: Each component validated before proceeding
- **Incremental value**: Team can start using components as they're completed
- **Context-aware**: Skills activate based on both prompts and files being edited

---

**Plan Version:** v2-high-level-hook-based
**Last Updated:** 2025-11-21 (Updated to use hook-based Skill activation system)
**Status:** Ready for Approval
**References:**
- [claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase) - Hook implementation reference
**Next Step:** Review and approve, then begin MVP implementation with hook infrastructure setup
