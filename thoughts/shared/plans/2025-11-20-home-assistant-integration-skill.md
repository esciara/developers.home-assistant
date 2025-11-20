---
date: 2025-11-20T23:30:00+00:00
author: Claude
git_commit: 427544d
branch: claude/home-assistant-integration-skill-01T9LctSUCa3AjQpfkMro4yC
repository: developers.home-assistant
topic: "Home Assistant Integration Development Skill - Implementation Plan"
tags: [plan, claude-skills, home-assistant, integration-development, progressive-disclosure]
status: complete
related_research: thoughts/shared/research/2025-11-20-home-assistant-integration-development.md
---

# Implementation Plan: Home Assistant Integration Development Skill

**Date**: 2025-11-20T23:30:00+00:00
**Author**: Claude
**Related Research**: `thoughts/shared/research/2025-11-20-home-assistant-integration-development.md`

## Executive Summary

Create a comprehensive Claude Code Skill for Home Assistant integration development following official best practices. The Skill will use a **hybrid progressive disclosure architecture**: all three phases (MVP, Advanced, Quality) will be implemented, but structured so beginners can naturally progress while having access to advanced features when needed.

**Key Decisions**:
- **Location**: Project skill in `.claude/skills/home-assistant-integration/`
- **Architecture**: Progressive disclosure with main SKILL.md + supporting guides
- **Scope**: All 3 phases covered, MVP-first presentation
- **Target Quality**: Bronze tier baseline, with Silver/Gold/Platinum guidance
- **Activation**: Model-invoked via description triggers

## Phasing Approach: Hybrid Strategy

After analyzing the pros/cons of single-phase vs. multi-phase approaches, we're implementing a **hybrid progressive disclosure architecture**:

### Design Rationale

**Why Hybrid?**
1. **Complete from day one**: All knowledge accessible immediately
2. **Beginner-friendly**: SKILL.md focuses on Phase 1 MVP workflow
3. **Natural progression**: Users follow Phase 1 → 2 → 3 as they gain experience
4. **On-demand context**: Supporting files load only when needed
5. **Maintainable**: Changes to one phase don't cascade unnecessarily

### Progressive Disclosure Structure

```
SKILL.md (Focus: Phase 1 MVP)
├── Quick Start → Basic workflow
├── Phase 1 Instructions → Scaffold → Config Flow → Basic Entity → Tests
├── "Next Steps" Section → Points to Phase 2/3
└── References to supporting files

Supporting Files (Load on demand)
├── MANIFEST_GUIDE.md (All phases)
├── CONFIG_FLOW_GUIDE.md (All phases)
├── ENTITY_GUIDE.md (All phases, heavy Phase 2/3)
├── COORDINATOR_GUIDE.md (Phase 2 focus)
├── TESTING_GUIDE.md (All phases, progressive)
├── QUALITY_SCALE.md (Phase 3 focus)
└── templates/ (All phases)
```

## File Structure

```
.claude/skills/home-assistant-integration/
├── SKILL.md                    # Main workflow, Phase 1 focus, ~500 lines
├── MANIFEST_GUIDE.md           # manifest.json reference, ~400 lines
├── CONFIG_FLOW_GUIDE.md        # Config flow patterns, ~600 lines
├── ENTITY_GUIDE.md             # Entity development, ~500 lines
├── COORDINATOR_GUIDE.md        # DataUpdateCoordinator patterns, ~400 lines
├── TESTING_GUIDE.md            # Testing requirements, ~500 lines
├── QUALITY_SCALE.md            # Quality tiers checklist, ~400 lines
└── templates/
    ├── manifest.json           # Complete manifest template
    ├── __init__.py             # Basic __init__ (Phase 1)
    ├── __init__-coordinator.py # With coordinator (Phase 2)
    ├── config_flow.py          # Full config flow with reauth/reconfigure
    ├── coordinator.py          # DataUpdateCoordinator implementation
    ├── const.py                # Constants template
    ├── light.py                # Example light entity
    ├── sensor.py               # Example sensor entity
    └── test_config_flow.py     # 100% coverage test template
```

**Total Files**: 17 (1 main + 6 guides + 10 templates)

## Phase 1: MVP (Core Workflow)

**Goal**: Get developers from zero to working Bronze-tier integration with minimal friction.

### SKILL.md Content (Phase 1 Focus)

**Sections**:
1. **Quick Start** - Scaffold command and 30-second overview
2. **Phase 1: Core Workflow** - Step-by-step MVP instructions
3. **Development Workflow** - 8-step process (Scaffold → Validate)
4. **Critical Requirements** - Must-do/must-not-do checklists
5. **Common Pitfalls** - Top 10 mistakes to avoid
6. **Next Steps** - Clear path to Phase 2/3
7. **Supporting Files Reference** - When to use each guide

**Key Features**:
- Assumes no prior HA integration experience
- Copy-paste examples for common tasks
- Links to supporting files for deep dives
- Clear Bronze tier focus
- Emphasizes validation tools

### MANIFEST_GUIDE.md

**Content**:
- All required fields explained
- Integration types (device, hub, service, helper)
- IoT classes (local_polling, local_push, cloud_polling, cloud_push)
- Requirements pinning patterns
- Quality scale field
- Codeowners format
- Common validation errors

**Coverage**: All phases (Phase 1 establishes, Phase 2/3 enhance)

### CONFIG_FLOW_GUIDE.md

**Content**:
- Config flow lifecycle
- `async_step_user` implementation
- Unique ID handling (what's acceptable, what's not)
- Error handling patterns
- Reauth flow (Phase 2)
- Reconfigure flow (Phase 2)
- Options flow (Phase 2)
- Form schemas with Voluptuous
- Abort conditions
- Discovery step patterns (Phase 2)

**Coverage**: All phases (Phase 1 basic user flow, Phase 2 advanced flows)

### ENTITY_GUIDE.md

**Content**:
- Entity naming standards (`has_entity_name = True`)
- Generic entity properties
- Device info structure
- Entity lifecycle hooks
- Update strategies (polling vs push)
- 41+ entity type reference
- Entity categories
- Device classes
- Translation keys (Phase 3)

**Coverage**: All phases (Phase 1 basics, Phase 2 advanced patterns, Phase 3 translations)

### TESTING_GUIDE.md

**Content**:
- Test directory structure
- Config flow testing (100% coverage)
- MockConfigEntry usage
- Fixtures in conftest.py
- Snapshot testing
- Platform setup testing
- Running tests locally
- Coverage requirements by tier

**Coverage**: All phases (Phase 1 config flow focus, Phase 2/3 expanded coverage)

### Templates (Phase 1)

**Files to Create**:
1. `manifest.json` - Complete Bronze tier template
2. `__init__.py` - Basic setup without coordinator
3. `config_flow.py` - User flow + unique ID handling
4. `const.py` - Domain and configuration keys
5. `test_config_flow.py` - 100% coverage template

## Phase 2: Advanced Features

**Goal**: Enable production-ready integrations with DataUpdateCoordinator, multiple platforms, and advanced flows.

### COORDINATOR_GUIDE.md (New File)

**Content**:
- DataUpdateCoordinator overview
- `_async_setup` pattern
- `_async_update_data` implementation
- Error handling (ConfigEntryAuthFailed, UpdateFailed)
- Context-aware fetching
- `always_update=False` usage
- CoordinatorEntity pattern
- `_handle_coordinator_update` implementation
- Timeout handling
- Retry mechanisms

**Coverage**: Phase 2 focus

### Enhanced Supporting Files

**ENTITY_GUIDE.md additions**:
- CoordinatorEntity inheritance
- Multiple platform support patterns
- Device grouping strategies
- Entity state restoration
- Advanced lifecycle management

**CONFIG_FLOW_GUIDE.md additions**:
- Reauth flow complete implementation
- Reconfigure flow patterns
- Options flow for runtime config
- Discovery step implementations (Bluetooth, Zeroconf, DHCP, etc.)

**TESTING_GUIDE.md additions**:
- Testing with coordinator
- Mocking API responses
- Testing reauth/reconfigure flows
- Platform setup tests
- Integration tests with multiple entities

### Templates (Phase 2)

**Additional Files**:
1. `__init__-coordinator.py` - With DataUpdateCoordinator
2. `coordinator.py` - Complete coordinator implementation
3. `light.py` - CoordinatorEntity example
4. `sensor.py` - Multiple sensor types example
5. Updated `config_flow.py` - With reauth/reconfigure

## Phase 3: Quality & Polish

**Goal**: Guide developers to Silver/Gold/Platinum tiers with strict typing, diagnostics, and advanced testing.

### QUALITY_SCALE.md (New File)

**Content**:
- Bronze tier checklist (minimum requirements)
- Silver tier requirements:
  - 80%+ test coverage
  - Diagnostics implementation
  - Exception translations
  - Config entry state handling
  - Reconfiguration flow
- Gold tier requirements:
  - 90%+ test coverage
  - Strict typing (`.strict-typing` file)
  - Entity translations
  - Device/stale device handling
  - Proper parallel updates
- Platinum tier requirements:
  - 95%+ test coverage
  - Perfect implementation
  - All quality rules satisfied
- Quality rules reference with links

**Coverage**: Phase 3 focus, references all phases

### Enhanced Supporting Files

**ENTITY_GUIDE.md additions**:
- Entity translations structure
- Translation keys by entity type
- Device handling patterns
- Stale device cleanup

**TESTING_GUIDE.md additions**:
- Coverage analysis tools
- Snapshot testing advanced usage
- Type checking integration
- Pre-commit hook setup
- CI/CD patterns

**MANIFEST_GUIDE.md additions**:
- Quality scale progression
- When to upgrade tiers
- Diagnostic config

### Templates (Phase 3)

**Additional Files**:
1. `strings.json` - Complete translation structure
2. `diagnostics.py` - Diagnostics implementation
3. `.strict-typing` - Entry for integration
4. `services.yaml` - Custom service documentation
5. Advanced test examples

## Testing Strategy

### Validation Queries

Test the Skill with these queries to ensure proper activation:

**Phase 1 (MVP)**:
1. "Help me create a Home Assistant integration"
2. "I need to implement a config flow for my HA integration"
3. "How do I structure a Home Assistant custom component?"
4. "Create a manifest.json for a new integration"
5. "What are the testing requirements for Home Assistant integrations?"

**Phase 2 (Advanced)**:
1. "How do I use DataUpdateCoordinator in Home Assistant?"
2. "Implement reauth flow for my integration"
3. "How do I add multiple platforms to my HA integration?"
4. "Help me set up discovery for my integration"

**Phase 3 (Quality)**:
1. "How do I get to Silver tier quality for my HA integration?"
2. "Implement diagnostics for Home Assistant integration"
3. "Add strict typing to my integration"
4. "What are the Gold tier requirements?"

### Success Criteria

**Skill activates when**:
- User mentions "Home Assistant integration"
- User mentions "HA integration" or "custom component"
- User works with `manifest.json` in HA context
- User implements "config flow" or "config entry"
- User asks about HA integration testing

**Skill provides**:
- Clear phase-appropriate guidance
- References to relevant supporting files
- Template files for copy-paste
- Validation command sequences
- Quality tier awareness

### Testing Process

1. **Unit Testing**: Verify each template is valid Python/JSON
2. **Activation Testing**: Test with all validation queries
3. **Flow Testing**: Walk through complete Phase 1 → 2 → 3 progression
4. **Integration Testing**: Use Skill to create a real integration
5. **Documentation Review**: Ensure all links resolve correctly

## Implementation Steps

### Step 1: Create Skill Directory Structure

```bash
mkdir -p .claude/skills/home-assistant-integration/templates
```

### Step 2: Write SKILL.md

**Content priorities**:
1. YAML frontmatter with name and description
2. Quick Start section (scaffold command)
3. Phase 1 workflow (8 steps)
4. Critical requirements (must-do/must-not)
5. Common pitfalls
6. Next Steps to Phase 2/3
7. Supporting files reference

**Estimated**: ~500 lines, focus on clarity and copy-paste examples

### Step 3: Write Phase 1 Supporting Guides

**Files in order**:
1. `MANIFEST_GUIDE.md` - Foundation for all phases
2. `CONFIG_FLOW_GUIDE.md` - Phase 1 user flow + Phase 2 advanced flows
3. `ENTITY_GUIDE.md` - Phase 1 basics + Phase 2/3 patterns
4. `TESTING_GUIDE.md` - Phase 1 config flow coverage + Phase 2/3 expansion

**Estimated**: ~2000 lines total across 4 files

### Step 4: Create Phase 1 Templates

**Files**:
1. `templates/manifest.json` - Bronze tier complete
2. `templates/__init__.py` - Basic setup
3. `templates/config_flow.py` - User flow with unique ID
4. `templates/const.py` - Domain constants
5. `templates/test_config_flow.py` - 100% coverage

**Estimated**: ~600 lines total across 5 files

### Step 5: Test Phase 1 (MVP)

**Actions**:
1. Invoke Skill with Phase 1 validation queries
2. Verify Skill activates correctly
3. Walk through MVP workflow
4. Validate generated files with hassfest
5. Run template tests

### Step 6: Write Phase 2 Content

**Files**:
1. `COORDINATOR_GUIDE.md` - New comprehensive guide
2. Update `CONFIG_FLOW_GUIDE.md` - Add reauth/reconfigure/options
3. Update `ENTITY_GUIDE.md` - Add CoordinatorEntity patterns
4. Update `TESTING_GUIDE.md` - Add coordinator testing

**Templates**:
1. `templates/__init__-coordinator.py`
2. `templates/coordinator.py`
3. `templates/light.py`
4. `templates/sensor.py`

**Estimated**: ~1600 lines total (guides + templates)

### Step 7: Test Phase 2 (Advanced)

**Actions**:
1. Test Phase 2 validation queries
2. Verify coordinator guidance
3. Test reauth/reconfigure flows
4. Validate multi-platform patterns

### Step 8: Write Phase 3 Content

**Files**:
1. `QUALITY_SCALE.md` - New comprehensive guide
2. Update `ENTITY_GUIDE.md` - Add translations
3. Update `TESTING_GUIDE.md` - Add coverage analysis
4. Update `MANIFEST_GUIDE.md` - Add quality scale progression

**Templates**:
1. `templates/strings.json`
2. `templates/diagnostics.py`
3. `templates/.strict-typing`
4. `templates/services.yaml`

**Estimated**: ~1200 lines total (guides + templates)

### Step 9: Test Phase 3 (Quality)

**Actions**:
1. Test Phase 3 validation queries
2. Verify quality tier guidance
3. Test diagnostics implementation
4. Validate strict typing patterns

### Step 10: Final Integration Testing

**Actions**:
1. Use Skill to create complete integration from scratch
2. Verify all phases work in progression
3. Test supporting file references resolve
4. Run all validation tools (hassfest, pytest, pre-commit)
5. Verify templates are valid and pass linting

### Step 11: Documentation & Commit

**Actions**:
1. Add version history to SKILL.md
2. Verify all internal links work
3. Commit to project repository
4. Update plan status to "complete"

## Success Metrics

**Quantitative**:
- All 13 validation queries trigger Skill activation
- All template files pass validation (hassfest, ruff, pytest)
- Complete Phase 1 workflow takes < 30 minutes
- Supporting files stay under 600 lines each
- Total context < 10k lines across all files

**Qualitative**:
- Developers can create Bronze tier integration without external docs
- Clear progression from Phase 1 → 2 → 3
- No duplicate content across files
- Supporting files load only when referenced
- Templates are copy-paste ready

## Maintenance Plan

**Version Tracking**:
```markdown
## Version History
- v1.0.0 (2025-11-20): Initial release, all 3 phases, Bronze tier focus
- v1.1.0 (TBD): Updates based on user feedback
- v2.0.0 (TBD): Home Assistant 2026.x compatibility updates
```

**Update Triggers**:
1. Home Assistant documentation changes
2. New quality scale rules
3. Scaffold tool output changes
4. New entity types or patterns
5. Breaking changes in Home Assistant core

**Review Schedule**:
- Monthly: Check for Home Assistant release notes
- Quarterly: Review validation queries effectiveness
- Annually: Complete skill refresh and restructure if needed

## Risk Mitigation

**Risk**: Supporting files become too large, consume excessive context
**Mitigation**: Progressive disclosure, keep each file < 600 lines, clear scoping

**Risk**: Skill doesn't activate for common queries
**Mitigation**: Comprehensive description with multiple triggers, validation query testing

**Risk**: Templates become outdated quickly
**Mitigation**: Version tracking, regular review schedule, scaffold tool monitoring

**Risk**: Phase 1 focus causes users to miss Phase 2/3 features
**Mitigation**: "Next Steps" sections, explicit phase progression guidance, quality tier awareness

**Risk**: Overlapping guidance across files causes confusion
**Mitigation**: Clear file boundaries, cross-references, DRY principle enforcement

## Open Questions

1. **Template Variations**: Should we provide multiple __init__.py templates (with/without coordinator) or show both patterns in one file with comments?
   - **Decision**: Separate files (`__init__.py` and `__init__-coordinator.py`) for clarity

2. **Code Generation**: Should SKILL.md instruct Claude to generate code directly or always reference templates?
   - **Recommendation**: Reference templates for complete files, generate code for small customizations

3. **External Library Guidance**: Should we add a guide for creating PyPI libraries or keep focus on integration code?
   - **Recommendation**: Phase 4 future consideration, too broad for initial release

4. **Discovery Protocols**: Should we add discovery-specific guides or keep in CONFIG_FLOW_GUIDE.md?
   - **Recommendation**: Keep in CONFIG_FLOW_GUIDE.md for now, monitor if it grows too large

5. **Platform-Specific Guides**: Should we create detailed guides for each platform type (light, sensor, climate, etc.)?
   - **Recommendation**: ENTITY_GUIDE.md covers patterns, templates show examples, avoid 41 separate files

## Conclusion

This implementation plan delivers a comprehensive Claude Code Skill that:

1. **Meets all user requirements**:
   - ✅ Covers all 3 phases (MVP, Advanced, Quality)
   - ✅ Project skill in `.claude/skills/`
   - ✅ Testing section with validation queries
   - ✅ Progressive disclosure architecture

2. **Follows Claude Skills best practices**:
   - ✅ Model-invoked with specific triggers
   - ✅ Focused on single capability
   - ✅ Progressive disclosure with supporting files
   - ✅ Clear examples and templates
   - ✅ Testable with realistic queries

3. **Embeds Home Assistant best practices**:
   - ✅ Bronze tier minimum baseline
   - ✅ Config entry pattern (not YAML)
   - ✅ DataUpdateCoordinator for polling
   - ✅ Async-first architecture
   - ✅ 100% config flow test coverage
   - ✅ External PyPI library requirement
   - ✅ Complete validation toolchain

4. **Enables natural progression**:
   - ✅ Beginner-friendly MVP workflow in SKILL.md
   - ✅ Advanced features accessible when needed
   - ✅ Clear path from Bronze → Silver → Gold → Platinum
   - ✅ Supporting files load on-demand

**Estimated Total Effort**: ~5500 lines across 17 files
**Estimated Time**: 4-6 hours for complete implementation and testing
**Target Completion**: 2025-11-20

Ready to proceed with implementation.
