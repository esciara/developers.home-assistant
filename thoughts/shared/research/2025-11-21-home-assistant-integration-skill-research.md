---
date: 2025-11-21T00:09:45+00:00
researcher: Claude
git_commit: 2da5fccdc337939271b10113aa04a5ee6808d904
branch: claude/home-assistant-skill-013vGYJPRZfj56zuq2CZSHVi
repository: developers.home-assistant
topic: "Research for Creating Home Assistant Integration Development Skill"
tags: [research, codebase, home-assistant, integrations, claude-skills, documentation]
status: complete
last_updated: 2025-11-21
last_updated_by: Claude
---

# Research: Home Assistant Integration Development Skill

**Date**: 2025-11-21T00:09:45+00:00
**Researcher**: Claude
**Git Commit**: 2da5fccdc337939271b10113aa04a5ee6808d904
**Branch**: claude/home-assistant-skill-013vGYJPRZfj56zuq2CZSHVi
**Repository**: developers.home-assistant

## Research Question

Identify the parts of the Home Assistant developer documentation that will allow creation of a Claude Code skill to help create or refactor Home Assistant integrations following all best practices, and identify good practices for creating Claude Code skills.

## Summary

The Home Assistant developers repository contains comprehensive documentation for integration development in the `docs/` directory, organized into 76 root-level files and 10 major subdirectories. The documentation is structured around a **5-tier Integration Quality Scale** (Bronze, Silver, Gold, Platinum, No Score) with **56 detailed quality rules** that define best practices.

The research identified key documentation areas essential for a Claude Code skill:
1. **Integration Quality Scale** - 56 rules across 5 tiers defining all requirements
2. **Integration Structure** - File organization, manifest.json, and setup patterns
3. **Entity Platforms** - 41+ platform types (sensor, switch, climate, etc.)
4. **Config Flows** - UI configuration and authentication patterns
5. **Data Coordinators** - Data fetching and update patterns
6. **Testing Requirements** - 95%+ coverage requirements with pytest patterns
7. **Code Style** - Ruff formatting, strict typing, import organization

For Claude Code skill development, the `skills.md` file provides comprehensive guidelines including YAML frontmatter requirements, description best practices, tool restrictions, and progressive disclosure patterns.

## Detailed Findings

### 1. Home Assistant Documentation Structure

The `/home/user/developers.home-assistant/docs/` directory is well-organized with clear entry points:

**Primary Entry Points:**
- `creating_component_index.md` - Main starting point for integration development
- `development_index.md` - Hub for all development documentation
- `core/integration-quality-scale/index.md` - Quality framework overview

**Major Documentation Categories:**
- **Core Integration Files**: Structure, manifest, file organization
- **Config Entry System**: Config flows, options flows, authentication
- **Entity Platforms**: 41 platform types with individual documentation
- **Quality Scale**: 56 rules organized by tier (Bronze → Platinum)
- **Testing & QA**: Coverage requirements, pytest patterns, CI/CD
- **Code Standards**: Style guidelines, typing, formatting

### 2. Integration Quality Scale Framework

**Location**: `docs/core/integration-quality-scale/`

The quality scale is the most critical documentation for best practices:

#### Quality Tiers

| Tier | Requirements | Key Rules |
|------|-------------|-----------|
| **Bronze** (Minimum) | Config flow UI, unique entity IDs, device classes | 15+ foundational rules |
| **Silver** | Config entry unloading, entity unavailable handling, diagnostics | 20+ operational excellence rules |
| **Gold** | 95%+ test coverage, comprehensive documentation, entity naming | 30+ quality rules |
| **Platinum** | Strict typing, optimal patterns, advanced features | Full type coverage |

#### Key Quality Rules for the Skill

**Essential Bronze Rules** (`docs/core/integration-quality-scale/rules/`):
- `config-flow.md` - UI configuration requirement
- `entity-unique-id.md` - Entity identification
- `entity-device-class.md` - Device classification
- `entity-category.md` - Entity categorization

**Critical Silver Rules**:
- `config-entry-unloading.md` - Resource cleanup patterns
- `entity-unavailable.md` - Handling unavailable devices
- `diagnostics.md` - Diagnostic data support
- `discovery.md` - Device discovery capability

**Important Gold Rules**:
- `test-coverage.md` - 95%+ coverage requirement
- `has-entity-name.md` - Entity naming conventions
- `docs-*.md` (12 files) - Documentation requirements

**Platinum Rules**:
- `strict-typing.md` - Full type annotations with mypy

### 3. Integration File Structure

**Primary Documentation**: `docs/creating_integration_file_structure.md`

Standard integration structure:
```
custom_components/my_integration/
├── __init__.py           # Integration setup
├── manifest.json         # Metadata and dependencies
├── config_flow.py        # UI configuration
├── coordinator.py        # Data update coordination
├── const.py              # Constants
├── entity.py             # Base entity classes
├── sensor.py             # Sensor platform
├── switch.py             # Switch platform
├── strings.json          # Translations
└── services.yaml         # Service definitions
```

**Test Structure** (`docs/creating_integration_tests_file_structure.md`):
```
tests/components/my_integration/
├── __init__.py
├── conftest.py           # Fixtures
├── test_config_flow.py   # Config flow tests (100% coverage required)
├── test_sensor.py        # Platform tests
└── test_init.py          # Integration setup tests
```

### 4. Manifest Configuration

**Primary Documentation**: `docs/creating_integration_manifest.md`

Critical manifest.json fields:
- `domain` - Integration identifier (required)
- `name` - Human-readable name (required)
- `codeowners` - Maintainer GitHub usernames (required)
- `config_flow` - Enables UI configuration (required for Bronze tier)
- `integration_type` - hub, device, entity, service, virtual, etc.
- `requirements` - Python package dependencies with pinned versions
- `dependencies` - Other HA integrations needed
- `quality_scale` - Current tier level

### 5. Entity Platforms

**Primary Documentation**: `docs/core/entity.md` + 41 platform-specific files in `docs/core/entity/`

Most common platforms for the skill to understand:
- `sensor.md` - Read-only state and measurements
- `binary-sensor.md` - On/off state sensors
- `switch.md` - On/off controllable devices
- `light.md` - Lighting control with brightness, color
- `climate.md` - Temperature control (HVAC)
- `cover.md` - Covers, blinds, garage doors
- `lock.md` - Lock control
- `camera.md` - Camera feeds
- `media-player.md` - Media playback control

Each platform has specific requirements for:
- Device classes (e.g., temperature, humidity, battery for sensors)
- State classes (measurement, total, total_increasing)
- Supported features (capabilities bitmask)
- Unit of measurement standards

### 6. Config Flow & Authentication

**Primary Documentation**: `docs/config_entries_config_flow_handler.md` (30+ KB comprehensive guide)

Key patterns:
- User step for manual configuration
- Discovery step for automatic device detection
- Reauth flow for credential renewal
- Reconfigure flow for changing settings
- Unique ID validation to prevent duplicates
- Error handling with translated messages

**Quality Requirements**:
- 100% test coverage for config flows (`rules/config-flow-test-coverage.md`)
- User-friendly error messages
- Proper validation with ConfigValidationError

### 7. Data Update Coordinators

**Primary Documentation**: `docs/integration_fetching_data.md`

The DataUpdateCoordinator pattern is the standard approach:

```python
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

coordinator = DataUpdateCoordinator(
    hass,
    logger,
    name="my_integration",
    update_method=async_update_data,
    update_interval=timedelta(seconds=30),
)
```

**Best Practices from Blog Posts**:
- `blog/2023-07-27-avoiding-unnecessary-callbacks-with-dataupdatecoordinator.md` - Callback optimization
- `blog/2024-08-05-coordinator_async_setup.md` - Async setup patterns
- `blog/2025-11-17-retry-after-update-failed.md` - Retry mechanisms

**Quality Rule**: `rules/appropriate-polling.md` - Don't poll more frequently than necessary

### 8. Testing Requirements

**Primary Documentation**: `docs/development_testing.md`

Testing framework requirements:
- **pytest** for all tests
- **95%+ code coverage** required for Gold tier (`rules/test-coverage.md`)
- **100% config flow coverage** required (`rules/config-flow-test-coverage.md`)
- **Snapshot testing** with Syrupy for complex state validation

**Test Structure Best Practices**:
- Use fixtures in `conftest.py` for reusable test components
- Mock external API calls
- Test setup failures and error handling
- Test entity state updates
- Test device/entity registry interactions

**Quality Rule**: `rules/test-before-setup.md` - Validate setup can succeed before attempting

### 9. Code Style & Quality

**Primary Documentation**: `docs/development_guidelines.md`

**Formatting**:
- **Ruff** for code formatting and import sorting (replaced Black)
- 120 character line length (per python-development skill)
- Google-style docstrings

**Type Hints** (`docs/development_typing.md`):
- Type annotations required for all functions
- Strict typing for core modules (`.strict-typing` file)
- mypy for static type checking
- `from __future__ import annotations` for forward references

**Import Organization**:
- Standard library imports first
- Third-party imports second
- Home Assistant imports third
- Local integration imports last
- Alphabetical within each group

**Logging Standards**:
- Use structured logging with context
- Different log levels: DEBUG, INFO, WARNING, ERROR
- Include relevant entity/device info in messages

### 10. Development Workflow

**Submission Process** (`docs/development_submitting.md`):
1. Run all tests locally
2. Ensure Ruff formatting
3. Check type hints with mypy
4. Update quality_scale.yaml if completing rules
5. Create focused, atomic commits
6. Write clear PR descriptions

**Review Process** (`docs/review-process.md`):
- Code reviews check against quality scale rules
- Checklist-based validation
- CI runs hassfest (manifest validator), pytest, mypy, Ruff

## Code References

### Essential Documentation Files

**Integration Creation**:
- `docs/creating_component_index.md` - Getting started guide
- `docs/creating_integration_file_structure.md:1-100` - File organization
- `docs/creating_integration_manifest.md:1-300` - Manifest configuration

**Quality Scale**:
- `docs/core/integration-quality-scale/index.md:1-150` - Framework overview
- `docs/core/integration-quality-scale/rules/` - 56 individual rule files
- `docs/core/integration-quality-scale/checklist.md` - Implementation tracking

**Config Flows**:
- `docs/config_entries_config_flow_handler.md:1-1000+` - Complete config flow guide
- `docs/config_entries_index.md` - Config entry lifecycle

**Data Management**:
- `docs/integration_fetching_data.md` - DataUpdateCoordinator patterns
- `docs/integration_setup_failures.md` - Error handling

**Testing**:
- `docs/development_testing.md` - Testing framework and requirements
- `docs/core/integration-quality-scale/rules/test-coverage.md` - Coverage requirements
- `docs/core/integration-quality-scale/rules/config-flow-test-coverage.md` - Config flow testing

**Code Style**:
- `docs/development_guidelines.md` - Style guide
- `docs/development_typing.md` - Type hints guide
- `docs/core/integration-quality-scale/rules/strict-typing.md` - Typing requirements

## Claude Code Skill Best Practices

**Primary Documentation**: `/home/user/developers.home-assistant/skills.md`

### Skill Structure Requirements

**YAML Frontmatter**:
```yaml
---
name: skill-name-here          # lowercase, hyphens only, max 64 chars
description: What the skill does and when to use it  # max 1024 chars
allowed-tools: Read, Grep, Glob  # optional, restricts tool usage
---
```

**Description Best Practices**:
- Include **both what and when**: "Analyze Excel spreadsheets, create pivot tables. Use when working with Excel files, .xlsx files, or tabular data."
- Use specific trigger terms users would mention
- Be concrete, not vague ("For files" is too vague)
- Include file extensions, domain terms, and use cases

### Skill Organization

**Single Skill vs Multi-file Skill**:
- Simple skills: Single `SKILL.md` file
- Complex skills: `SKILL.md` + reference docs + scripts + templates
- Use progressive disclosure - Claude reads additional files only when needed

**File Organization**:
```
my-skill/
├── SKILL.md              # Main skill (required)
├── reference.md          # Detailed API docs (loaded on demand)
├── examples.md           # Code examples (loaded on demand)
├── scripts/
│   └── helper.py         # Utility scripts
└── templates/
    └── template.txt      # File templates
```

### Tool Restrictions

**allowed-tools field**:
- Use for read-only skills: `allowed-tools: Read, Grep, Glob`
- Prevents accidental file modifications
- Good for analysis/research skills
- Omit for skills that need full tool access

### Writing Effective Instructions

**Structure**:
1. Clear step-by-step instructions
2. Concrete examples with code snippets
3. Best practices and patterns
4. Common pitfalls to avoid
5. Links to additional reference files

**Tone**:
- Imperative/instructional: "Use X when Y"
- Specific: Include code snippets, not just prose
- Focused: One skill = one capability

### Skill Discovery

**How Claude finds skills**:
- Automatically scans `.claude/skills/` (project) and `~/.claude/skills/` (personal)
- Matches user request to skill descriptions
- Activates autonomously (model-invoked, not user-invoked)

**Testing Skills**:
- Ask questions that match the description keywords
- Check if Claude uses the skill without explicit invocation
- Refine description if skill isn't being discovered

### Best Practices Summary

1. **Focus**: One skill = one clear capability
2. **Description**: Include what, when, and trigger terms
3. **Progressive Disclosure**: Link to reference files, don't inline everything
4. **Examples**: Show concrete code, not just explanations
5. **Tool Safety**: Use allowed-tools for read-only operations
6. **Testing**: Verify skill activates automatically for matching requests

## Architecture Insights

### Documentation Organization Philosophy

Home Assistant documentation follows a layered approach:
1. **Getting Started** - Quick scaffold-based setup
2. **Core Concepts** - Integration structure, manifest, platforms
3. **Quality Scale** - Progressive improvement path (Bronze → Platinum)
4. **Reference** - Detailed platform-specific docs
5. **Advanced Topics** - Bluetooth, OAuth, diagnostics, etc.

This structure naturally maps to a skill that could:
- Guide users through initial setup (Bronze tier)
- Suggest improvements for existing integrations (Silver → Gold)
- Validate against quality scale rules
- Reference platform-specific requirements

### Common Integration Patterns

**Hub Pattern** (`integration_type: hub`):
- Single API client coordinating multiple devices
- DataUpdateCoordinator at integration level
- Entities subscribe to coordinator updates
- Example: Philips Hue hub with multiple lights

**Device Pattern** (`integration_type: device`):
- Direct device communication
- Per-device coordinators or push updates
- Example: Individual smart plugs

**Entity Pattern** (`integration_type: entity`):
- Single entity integrations
- Simple setup without devices
- Example: System monitor sensors

### Evolution & Breaking Changes

The documentation includes blog posts tracking architectural evolution:
- `blog/2019-04-12-new-integration-structure.md` - Current structure foundation
- `blog/2024-04-30-store-runtime-data-inside-config-entry.md` - Modern data storage
- `blog/2025-02-16-config-subentries.md` - Sub-entry patterns

This indicates the skill should:
- Follow current best practices (not legacy patterns)
- Be aware of modern patterns (config entry runtime data, async setup)
- Reference quality scale as the authoritative source

## Existing Claude Code Infrastructure

**Location**: `/home/user/developers.home-assistant/.claude/`

### Current Skills

**python-development** (`.claude/skills/python-development/SKILL.md`):
- Comprehensive Python guidelines
- Type checking with mypy
- Testing with pytest (90%+ coverage goal)
- Ruff for formatting
- TDD approach with Given/When/Then structure
- Logging with loguru

This skill provides general Python best practices and could be complemented by a Home Assistant-specific integration skill.

### Slash Commands (23 commands)

The repository already has extensive workflow automation:
- **Research**: `/research_codebase`, `/research_codebase_generic`
- **Planning**: `/create_plan`, `/iterate_plan`
- **Implementation**: `/implement_plan`, `/ralph_impl`
- **Git**: `/commit`, `/describe_pr`
- **Tickets**: `/linear`, `/ralph_research`, `/ralph_plan`

These commands show a mature development workflow that a Home Assistant integration skill should integrate with, not duplicate.

### Sub-agents

- `codebase-analyzer` - Implementation analysis
- `codebase-locator` - File location
- `codebase-pattern-finder` - Pattern identification
- `web-search-researcher` - Web research
- `thoughts-analyzer` - Historical context
- `thoughts-locator` - Thoughts directory search

## Skill Design Recommendations

Based on the research, a Home Assistant integration skill should:

### 1. Core Capabilities

**Integration Creation**:
- Guide through scaffold setup
- Generate manifest.json with proper fields
- Create file structure following standards
- Implement config flow with error handling
- Set up DataUpdateCoordinator pattern
- Generate entity platforms with proper device classes

**Integration Refactoring**:
- Audit against quality scale rules
- Suggest tier improvements (Bronze → Silver → Gold)
- Identify missing requirements (unique IDs, test coverage, typing)
- Update to modern patterns (config entry runtime data, async setup)

**Quality Validation**:
- Check manifest.json completeness
- Validate entity unique IDs
- Verify device classes and state classes
- Check test coverage against 95% requirement
- Validate type hints and strict typing
- Ensure proper config entry unloading

### 2. Key Documentation to Reference

The skill should have direct knowledge of or reference to:

**Must-Have** (inline in SKILL.md or immediate reference):
- Integration Quality Scale overview and tiers
- Bronze tier requirements (minimum for new integrations)
- Manifest.json required fields
- Config flow basic pattern
- DataUpdateCoordinator usage pattern
- Entity platform selection (which platform for which device type)
- File structure template

**Should-Have** (in reference.md or separate files):
- Complete quality scale rules (56 rules)
- Platform-specific requirements (sensor state classes, etc.)
- Testing patterns and fixtures
- Error handling patterns
- OAuth/authentication patterns

**Nice-to-Have** (link to docs/):
- Advanced features (diagnostics, discovery, repairs)
- Bluetooth/IoT-specific patterns
- Voice/LLM integration

### 3. Skill Description Example

```yaml
name: home-assistant-integration
description: Create or refactor Home Assistant integrations following quality scale best practices. Use when creating new integrations, improving integration quality, implementing config flows, adding entity platforms, or validating against Bronze/Silver/Gold/Platinum tier requirements. Understands manifest.json, DataUpdateCoordinator, entity platforms (sensor, switch, climate, etc.), and testing requirements.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
```

### 4. Progressive Disclosure Strategy

**SKILL.md** (main file, ~500-1000 lines):
- Quick start for new integrations
- Bronze tier checklist
- Common platform patterns (sensor, switch, light)
- Manifest template
- Config flow template
- Basic coordinator pattern

**REFERENCE.md** (detailed docs, ~2000-5000 lines):
- Complete quality scale rules
- All entity platforms with examples
- Advanced config flow scenarios
- Testing patterns
- Error handling patterns
- Migration guides

**PLATFORMS.md** (platform reference):
- Each platform type with requirements
- Device classes per platform
- State classes and features
- Code examples

**QUALITY-SCALE.md** (tier requirements):
- Bronze requirements checklist
- Silver requirements checklist
- Gold requirements checklist
- Platinum requirements checklist

**templates/** (code templates):
- `manifest.json` template
- `__init__.py` template
- `config_flow.py` template
- `coordinator.py` template
- Platform templates (sensor, switch, etc.)

### 5. Tool Usage Recommendations

**Read-only during planning**: Use `allowed-tools: Read, Grep, Glob` during analysis phase
**Full access during implementation**: Omit allowed-tools when creating/modifying files

Alternatively, create two skills:
- `home-assistant-integration-advisor` (read-only, analysis and recommendations)
- `home-assistant-integration-builder` (full access, implementation)

## Open Questions

1. **Skill Scope**: Should the skill cover all 41 entity platforms or focus on the most common 10-15?
   - Recommendation: Cover common platforms in SKILL.md, reference all in separate docs

2. **Testing Integration**: Should the skill include pytest test generation or just guidance?
   - Recommendation: Include test templates and patterns, generate boilerplate

3. **Quality Scale Enforcement**: Should the skill enforce Bronze tier minimum or allow any structure?
   - Recommendation: Default to Bronze minimum, allow override for experimental work

4. **Existing Integration Detection**: Should the skill analyze existing code to determine current tier?
   - Recommendation: Yes, include analysis capability to audit existing integrations

5. **Documentation Generation**: Should the skill create user-facing docs for home-assistant.io?
   - Recommendation: Yes, but as separate capability - docs have specific format requirements

## Related Research

This is the initial research for Home Assistant integration skill creation. No prior research documents exist in the thoughts/shared/research/ directory for this topic.

## Next Steps (Not Implementation - Just Research Notes)

For future reference, creating the skill would involve:

1. **Skill Structure Decision**: Single comprehensive skill vs. multiple focused skills
2. **Content Extraction**: Extract key patterns from docs into skill files
3. **Template Creation**: Create code templates for common structures
4. **Testing**: Validate skill activates for relevant prompts
5. **Documentation**: Ensure skill references are accurate and up-to-date
6. **Integration**: Ensure skill works well with existing `/commit`, `/create_plan`, etc.

---

**Research Complete**: This document provides comprehensive mapping of Home Assistant developer documentation and Claude Code skill best practices for creating an integration development skill.
