# Increment 01: ha-config-flow-knowledge Skill

**Status:** Ready to Execute
**Priority:** High
**Estimated Effort:** 12-16 hours
**Target Completion:** 1-2 weeks (calendar time)

---

## Executive Summary

This first incremental round focuses on creating the `ha-config-flow-knowledge` Claude Code Skill as a proof-of-concept and foundation for the broader extension system workflow optimization.

**Why Start Here:**
- Config flow development is a critical, high-complexity task in HA integration development
- Provides immediate value for contributors working on config flow overhauls
- Acts as MVP to validate the self-contained Skill approach
- Lowest risk, highest learning opportunity

**Expected Outcomes:**
- One fully functional, self-contained Claude Code Skill with comprehensive config flow knowledge
- Validated approach for creating additional self-contained Skills
- Improved workflow for config flow development with all necessary information embedded
- Foundation for expanding to other Skills and Commands

---

## Objectives

### Primary Objective
Create the `ha-config-flow-knowledge` Skill that automatically activates when developers work on Home Assistant configuration flows, providing comprehensive, self-contained guidance including patterns, templates, examples, and best practices.

### Secondary Objectives
1. Validate Claude's native Skill activation system
2. Prove value of self-contained, embedded knowledge approach
3. Establish content extraction and organization patterns for subsequent Skill creation
4. Document lessons learned for next increments

---

## Scope

### In Scope

**Skill Creation:**
- Create `.claude/skills/ha-config-flow-knowledge/` directory structure
- Write comprehensive SKILL.md with clear activation description
- Extract and organize relevant content from research documents:
  - `thoughts/shared/research/2025-11-20-home-assistant-integration-skill-research.md` (Section 2: Configuration Flows)
  - `thoughts/shared/research/2025-11-21-home-assistant-integration-refactoring-patterns.md` (Sections 1, 7: Config Flow Refactoring, Authentication)

**Skill Content (Self-Contained):**
- Comprehensive patterns and implementation guides for all config flow types
- Code templates for common scenarios (basic flow, discovery flow, options flow, multi-step)
- Complete decision trees for flow patterns (user, discovery, options)
- Detailed error handling strategies and examples
- Schema definition patterns and validators
- Testing patterns and requirements (100% coverage guidance)
- Authentication flow patterns (reauthentication, reconfiguration)
- Real-world examples from HA core integrations
- Key requirements checklists
- Common pitfalls and solutions
- Activation triggers (prompts and file patterns)

**Testing:**
- Activation tests (prompt-based and file-based)
- Content completeness verification
- Real integration trial (apply to actual config flow work)
- Validation that skill provides all necessary information without external references

**Documentation:**
- Usage notes in the Skill directory
- Activation validation report
- Lessons learned document

### Out of Scope

**Not in This Increment:**
- Other Skills (ha-entity-knowledge, ha-coordinator-knowledge, etc.)
- Slash Commands (/research_ha_integration, etc.)
- Sub-agents (ha-integration-validator)
- Content beyond config flows (entities, coordinators, etc. - those belong in other Skills)
- Custom hooks or advanced activation logic
- Live examples from actual integration repositories (links to examples are fine, but not full repository clones)

---

## Deliverables

### 1. Skill Directory Structure

```
.claude/skills/ha-config-flow-knowledge/
├── SKILL.md                          # Main skill descriptor with activation info
├── patterns/
│   ├── flow-types.md                 # User, discovery, options flow patterns
│   ├── step-patterns.md              # async_step_* implementation patterns
│   ├── error-handling.md             # Error handling strategies and examples
│   ├── schema-definitions.md         # vol.Schema patterns and validators
│   └── authentication.md             # Reauthentication and reconfiguration
├── templates/
│   ├── basic-config-flow.py          # Single-step user flow template
│   ├── discovery-flow.py             # Discovery with zeroconf/ssdp template
│   ├── options-flow.py               # Options flow template
│   └── multi-step-flow.py            # Multi-step flow with data passing
├── examples/
│   ├── real-world-examples.md        # Annotated examples from HA core
│   └── common-scenarios.md           # Solutions to frequent use cases
├── testing/
│   ├── test-patterns.md              # Config flow testing patterns
│   ├── test-templates.py             # Test templates for different flows
│   └── coverage-guide.md             # Achieving 100% coverage
└── requirements-checklist.md         # Complete requirements reference
```

### 2. SKILL.md Content

**YAML Frontmatter (Required):**
```yaml
---
name: ha-config-flow-knowledge
description: Provides comprehensive Home Assistant config flow implementation guidance including patterns, templates, and testing strategies. Use when creating or refactoring config flows, implementing async_step methods, handling user/discovery/options flows, or working with config_flow.py files.
---
```

**Frontmatter Requirements:**
- `name`: Must use lowercase, numbers, hyphens only (max 64 chars)
- `description`: Max 1024 chars, written in **third person** (not "I help" or "You can")
- `description` must include: what the skill does + when to use it + key trigger terms

**SKILL.md Body (Max 500 lines):**
SKILL.md serves as navigation/overview, NOT full content dump. Points to detailed files as needed.

**Required Sections:**
- **Overview**: Brief explanation of config flow patterns (assumes Claude knows Python/HA basics)
- **Quick Start**: Most common scenario with minimal example
- **Content Organization**: Clear map to reference files (e.g., "For error handling, see [patterns/error-handling.md]")
- **Common Workflows**: High-level steps, details in separate files
- **Navigation Guide**: Decision tree for finding right content

**Progressive Disclosure Pattern:**
- Keep SKILL.md concise - under 500 lines
- Move detailed patterns to patterns/*.md
- Move code examples to templates/*.py
- Reference files one level deep only (avoid nested references)

### 3. Pattern Documents (patterns/ directory)

**flow-types.md:**
- Complete guide to user flows, discovery flows, and options flows
- When to use each type
- Implementation patterns for each
- Common combinations and variations

**step-patterns.md:**
- Detailed implementation patterns for all async_step_* methods
- Data passing between steps
- Progress dialogs and user feedback
- Flow lifecycle management

**error-handling.md:**
- Complete error handling strategies
- Standard error types (cannot_connect, invalid_auth, etc.)
- Custom error implementation
- Error translation strings
- Recoverable vs fatal errors

**schema-definitions.md:**
- Complete vol.Schema reference for config flows
- All field types with examples
- Validators and custom validation
- Conditional schemas
- Default values and optional fields

**authentication.md:**
- Reauthentication flow patterns
- Reconfiguration flow patterns
- OAuth and token-based auth
- Connection testing strategies

### 4. Code Templates (templates/ directory)

**All templates must be:**
- Complete, working Python code
- Well-commented with inline guidance
- Following current Home Assistant patterns
- Ready to copy-paste and customize
- Include placeholder markers for customization points

**Required templates:**
1. basic-config-flow.py - Single-step user configuration
2. discovery-flow.py - Discovery with automatic setup
3. options-flow.py - Post-setup configuration changes
4. multi-step-flow.py - Complex multi-step setup wizard

### 5. Examples & Testing (examples/ and testing/ directories)

**real-world-examples.md:**
- Annotated examples from actual HA core integrations
- Explanation of why certain patterns were chosen
- Links to source code in HA core repo

**common-scenarios.md:**
- Solutions to frequent config flow challenges
- Before/after code examples
- Troubleshooting guides

**testing/ directory:**
- Complete testing patterns for config flows
- Test templates matching flow templates
- Coverage guidance to achieve 100%
- Mocking strategies for external APIs

### 6. Testing & Validation

**Activation Tests:**

Note: Skills activate automatically based on context. Test by asking questions that match the description, then observe if skill activates.

- [ ] Activation on prompt "How do I create a config flow?"
- [ ] Activation on prompt "async_step_user pattern"
- [ ] Activation on prompt "config entry validation"
- [ ] Activation on prompt "implementing reauthentication flow"
- [ ] Activation on prompt "100% config flow test coverage"
- [ ] Activation when working with files named `config_flow.py`
- [ ] Activation when working with files named `test_config_flow.py`
- [ ] No false positives (doesn't activate for entity/coordinator/other topics)

**Content Completeness Tests:**
- [ ] All common config flow patterns covered
- [ ] Templates compile and run without errors
- [ ] Examples are accurate and current
- [ ] Testing guidance enables 100% coverage
- [ ] Can complete a config flow implementation without external documentation

**Real Integration Trial:**
- Apply to actual config flow development task
- Document workflow improvements
- Verify all needed information is available within skill
- Identify any gaps requiring external documentation lookup
- Capture user experience feedback

### 7. Documentation

**Lessons Learned Document** (stored outside skill directory in `plans/increments/`):
- What worked well
- What content gaps were identified
- Content organization effectiveness
- Recommendations for next Skills
- Activation refinements needed
- Optimal content structure insights

---

## Success Criteria

### Minimum Viable Success
- [ ] Skill created with all required files and directories
- [ ] SKILL.md description triggers auto-activation
- [ ] All pattern documents are comprehensive and self-contained
- [ ] All 4 code templates are complete and working
- [ ] Testing guidance enables achieving 100% coverage
- [ ] Activates on at least 80% of test prompts
- [ ] No false positives in testing
- [ ] Successfully used in one real config flow task without needing external docs

### Ideal Success
- [ ] All minimum criteria met
- [ ] Activates on 100% of test prompts
- [ ] Zero external documentation lookups needed during real trial
- [ ] All templates compile and follow current HA patterns
- [ ] Examples are accurate and helpful
- [ ] User reports improved workflow
- [ ] Time to find information reduced by 60%+ (since it's all embedded)
- [ ] Clear content organization patterns established for next Skills
- [ ] Team endorses approach for expansion

### Stretch Goals
- [ ] Used successfully in 3+ config flow tasks
- [ ] Contributed to one merged PR with config flow changes
- [ ] Community feedback gathered and incorporated
- [ ] Templates used directly in production code
- [ ] Skill becomes go-to reference for config flow development

---

## Risk Assessment

### High Risk: Skill Activation Unreliable

**Risk:** Claude's auto-activation doesn't trigger consistently

**Mitigation:**
- Test activation early and frequently
- Refine SKILL.md description based on testing
- Document activation patterns that work
- Have fallback plan to reference Skill manually

**Contingency:**
- If native activation fails, consider adding to slash command prompts explicitly
- May need to explore custom hooks approach as alternative
- Can still provide value even with manual activation

### High Risk: Content Incompleteness

**Risk:** Skill doesn't contain all necessary information, requiring external doc lookups

**Mitigation:**
- Thorough content extraction from research docs during Phase 1
- Real-world trial specifically tests for content gaps
- Include comprehensive examples and templates
- Test templates actually work
- Include troubleshooting sections

**Contingency:**
- Phase 6 trial will identify gaps
- Add missing content iteratively
- Prioritize most common use cases first
- Can release with known gaps documented

### Medium Risk: Content Becomes Outdated

**Risk:** Home Assistant patterns change, making embedded content stale

**Mitigation:**
- Focus on stable, core patterns
- Include references to HA version tested against
- Document when content was last verified
- Plan for regular review cycles

**Contingency:**
- Document maintenance schedule
- Create update process for subsequent increments
- Flag dated sections clearly

### Medium Risk: Too Much Content (Overwhelming)

**Risk:** Self-contained approach creates massive, hard-to-navigate skill

**Mitigation:**
- Strong organization with clear directory structure
- Comprehensive README with navigation guide
- Quick start section in SKILL.md
- Decision trees to guide users to right content

**Contingency:**
- Can split into multiple focused documents
- Add more navigation aids
- Create summary/quick reference documents

### Low Risk: Scope Creep

**Risk:** Attempting too much in first increment

**Mitigation:**
- Strict adherence to "one Skill only" scope
- Resist temptation to add Commands or other Skills
- Focus on config flows only, not other topics
- Save improvements for subsequent increments

**Contingency:**
- Cut stretch goals if needed
- Defer advanced scenarios
- Focus on core use cases first

---

## Dependencies

### Prerequisites
- Research documents exist and are comprehensive:
  - `thoughts/shared/research/2025-11-20-home-assistant-integration-skill-research.md`
  - `thoughts/shared/research/2025-11-21-home-assistant-integration-refactoring-patterns.md`
- Claude Code Skills feature is available
- `.claude/` directory structure is set up

### Blockers
- None identified

### External Dependencies
- Claude Code platform stability
- Access to Home Assistant integration codebase for testing
- Real config flow development work available for trial

---

## Metrics & Measurement

### Quantitative Metrics

**Activation Accuracy:**
- Target: 90%+ on test prompts
- Measure: Count successful activations / total test prompts

**Content Completeness:**
- Target: 95%+ of config flow tasks completable without external docs
- Measure: During real trial, track external doc lookups needed
- Baseline: Number of external doc lookups without skill
- With Skill: Number of external doc lookups with skill (should be near 0)

**Template Quality:**
- Target: 100% of templates compile without errors
- Target: All templates follow current HA patterns (manual verification)
- Measure: Compile tests, pattern review

**Time Savings:**
- Target: 60% reduction in time to find relevant information (higher since embedded)
- Baseline: Measure time to find info without Skill (external docs)
- With Skill: Measure time to find same info within Skill

### Qualitative Metrics

**User Experience:**
- Ease of navigation (subjective 1-5 rating)
- Content organization clarity (subjective 1-5 rating)
- Usefulness of templates (subjective 1-5 rating)
- Usefulness of examples (subjective 1-5 rating)
- Would use again (yes/no)
- Would recommend to others (yes/no)

**Quality:**
- Pattern accuracy (patterns match current HA best practices)
- Example relevance (examples are helpful and current)
- Decision tree usefulness (helped make right choice)
- Requirements checklist completeness (covered key points)
- Testing guidance effectiveness (achieved desired coverage)

---

## References

### Planning Documents
- [Extension System Workflow Optimization Plan v4](../extension-system-workflow-optimization-v4/README.md) - Overall system vision

### Research Documents (Source Material for Content Extraction)
- New Integrations: `thoughts/shared/research/2025-11-20-home-assistant-integration-skill-research.md` (Section 2: Configuration Flows)
- Refactoring Patterns: `thoughts/shared/research/2025-11-21-home-assistant-integration-refactoring-patterns.md` (Sections 1, 7: Config Flow Refactoring, Authentication)

### Home Assistant Documentation (Reference for Pattern Verification)
- Config Entry Documentation: `docs/creating_integration_config_entries.md`
- Data Entry Flow Architecture: `docs/data_entry_flow_index.md`
- Config Flow Testing: `docs/development_testing.md`

### Claude Skills Documentation
- Overview: `claude-skills-docs/overview.md`
- Authoring Best Practices: `claude-skills-docs/authoring-best-practices.md`
