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
├── requirements-checklist.md         # Complete requirements reference
└── README.md                         # Usage and activation guide
```

### 2. SKILL.md Content

**Required Sections:**
- **Description**: Clear, specific description triggering auto-activation
- **Purpose**: One-sentence use case statement
- **What This Skill Provides**: Complete list of embedded content
- **Quick Start Guide**: How to use the skill effectively
- **Content Organization**: Overview of directory structure and what's in each file
- **Common Workflows**: Step-by-step guides for common tasks
- **When to Use What**: Decision tree for navigating skill content

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
- [ ] Activation on prompt "How do I create a config flow?"
- [ ] Activation on prompt "async_step_user pattern"
- [ ] Activation on prompt "config entry validation"
- [ ] Activation when opening `config_flow.py`
- [ ] Activation when opening `test_config_flow.py`
- [ ] No false positives (doesn't activate inappropriately)

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

**README.md in Skill directory:**
- What this Skill provides
- Complete table of contents for all embedded content
- When it activates
- How to navigate and use the skill effectively
- Quick start guide for common tasks
- Examples of activation

**Lessons Learned Document:**
- What worked well
- What content gaps were identified
- Content organization effectiveness
- Recommendations for next Skills
- Activation refinements needed
- Optimal content structure insights

---

## Implementation Plan

### Phase 1: Preparation & Content Extraction (3-4 hours)

**Activities:**
1. Review existing research documents thoroughly
2. Extract all config flow-related content from research docs
3. Review HA core integration examples for real-world patterns
4. Review v3 ha-config-flow-knowledge spec for reference
5. Set up `.claude/skills/` directory structure
6. Plan content organization and file structure

**Deliverables:**
- Extracted content organized by topic
- List of HA core integrations to use as examples
- Directory structure created
- Content organization plan

### Phase 2: Core Skill Documents (4-5 hours)

**Activities:**
1. Write SKILL.md with clear activation description and navigation guide
2. Create all pattern documents (flow-types, step-patterns, error-handling, schema-definitions, authentication)
3. Build comprehensive requirements checklist
4. Write README with content overview and navigation guide

**Deliverables:**
- Complete SKILL.md with activation criteria
- All 5 pattern documents in patterns/ directory
- requirements-checklist.md
- README.md

**Key Decisions:**
- Activation trigger specificity (balance false positives vs false negatives)
- Content depth (how detailed to make each pattern)
- Organization structure (how to group related content)

### Phase 3: Code Templates & Examples (4-5 hours)

**Activities:**
1. Create 4 complete code templates (basic, discovery, options, multi-step)
2. Write detailed inline comments and guidance in each template
3. Extract and annotate real-world examples from HA core integrations
4. Create common scenarios document with solutions
5. Verify all templates are syntactically correct and follow current HA patterns

**Deliverables:**
- 4 working Python templates in templates/ directory
- real-world-examples.md with annotated examples
- common-scenarios.md with solutions

### Phase 4: Testing Content & Guides (2-3 hours)

**Activities:**
1. Create testing pattern documents
2. Write test templates matching flow templates
3. Create coverage achievement guide
4. Document mocking strategies for external APIs

**Deliverables:**
- Complete testing/ directory with all documents
- Test templates for each flow type
- Comprehensive testing guidance

### Phase 5: Validation & Refinement (2-3 hours)

**Activities:**
1. Run activation tests with various prompts
2. Test file-based activation
3. Verify content completeness (can implement without external docs)
4. Test templates compile and work correctly
5. Refine SKILL.md description if needed
6. Check all cross-references are accurate

**Deliverables:**
- Test results documentation
- Refined SKILL.md (if adjustments needed)
- Validation report
- Content completeness verification

### Phase 6: Real-World Trial (2-3 hours)

**Activities:**
1. Apply Skill to actual config flow development work
2. Document activation behavior
3. Verify all needed info is available within skill
4. Identify any content gaps requiring external docs
5. Measure effectiveness (time to info, workflow smoothness)
6. Gather qualitative feedback

**Deliverables:**
- Trial report with gap analysis
- Effectiveness metrics
- User experience notes
- Content improvement recommendations

### Phase 7: Documentation & Handoff (1-2 hours)

**Activities:**
1. Document lessons learned
2. Document optimal content organization patterns
3. Create recommendations for next increments
4. Update main plan if needed
5. Prepare for increment 02 planning

**Deliverables:**
- Lessons learned document
- Content organization best practices
- Recommendations for subsequent Skills
- Updated timeline estimates for remaining work

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

## Timeline

### Condensed Timeline (3-4 days full-time)

| Day | Activities | Hours |
|-----|------------|-------|
| 1 | Phase 1: Preparation & Content Extraction | 3-4 |
| 2 | Phase 2: Core Documents + Start Phase 3: Templates | 4-5 |
| 3 | Complete Phase 3 + Phase 4: Testing Content | 4-5 |
| 4 | Phase 5: Validation + Phase 6: Trial + Phase 7: Documentation | 4-5 |

**Total:** 15-19 hours over 3-4 days

### Extended Timeline (2 weeks part-time)

| Week | Day | Activities | Hours |
|------|-----|------------|-------|
| 1 | Mon | Phase 1: Preparation & Content Extraction | 3-4 |
| 1 | Tue | Phase 2: Start Core Documents | 2-3 |
| 1 | Wed | Phase 2: Complete Core Documents | 2-3 |
| 1 | Thu | Phase 3: Start Templates | 2-3 |
| 1 | Fri | Phase 3: Complete Templates & Examples | 2-3 |
| 2 | Mon | Phase 4: Testing Content | 2-3 |
| 2 | Tue | Phase 5: Validation & Refinement | 2-3 |
| 2 | Wed | Phase 6: Real-World Trial | 2-3 |
| 2 | Thu | Phase 7: Documentation & Handoff | 1-2 |

**Total:** 18-25 hours over 2 weeks

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

## Next Increments Preview

### Increment 02: ha-entity-knowledge Skill
**Estimated:** 12-16 hours
**Focus:** Self-contained entity implementation guidance, unique ID strategies, device info patterns
**Content:** Entity patterns, templates for different entity types, testing guidance, real-world examples

### Increment 03: ha-coordinator-knowledge Skill
**Estimated:** 10-14 hours
**Focus:** Self-contained DataUpdateCoordinator usage guidance
**Content:** Coordinator patterns, templates, update interval strategies, error handling

### Increment 04: ha-integration-structure Skill
**Estimated:** 8-12 hours
**Focus:** Self-contained integration file structure and manifest guidance
**Content:** Required files checklist, manifest patterns, directory structure templates

### Increment 05: ha-common-mistakes Skill
**Estimated:** 8-12 hours
**Focus:** Self-contained anti-patterns and best practices
**Content:** Common pitfalls, quality scale requirements, async patterns, unique ID issues

### Increment 06+: Commands & Sub-agents
**Focus:** Workflow orchestration commands that leverage the self-contained Skills

---

## References

### Planning Documents
- [Extension System Workflow Optimization Plan v4](../extension-system-workflow-optimization-v4/README.md) - Overall system vision
- [v3 ha-config-flow-knowledge Spec](../extension-system-workflow-optimization-v3/implementation/skills/ha-config-flow-knowledge.md) - Original concept (now adapted for self-contained approach)

### Research Documents (Source Material for Content Extraction)
- New Integrations: `thoughts/shared/research/2025-11-20-home-assistant-integration-skill-research.md` (Section 2: Configuration Flows)
- Refactoring Patterns: `thoughts/shared/research/2025-11-21-home-assistant-integration-refactoring-patterns.md` (Sections 1, 7: Config Flow Refactoring, Authentication)

### Home Assistant Documentation (Reference for Pattern Verification)
- Config Entry Documentation: `docs/creating_integration_config_entries.md`
- Data Entry Flow Architecture: `docs/data_entry_flow_index.md`
- Config Flow Testing: `docs/development_testing.md`

### Related Files
- `.claude/skills/` - Skills directory location
- `plans/increments/` - This document's location

---

## Approval & Sign-off

**Created:** 2025-11-21
**Author:** Claude Code Workflow Optimization Team
**Status:** Ready for Execution

**Review Checklist:**
- [ ] Scope is clear and focused
- [ ] Deliverables are well-defined
- [ ] Timeline is realistic
- [ ] Success criteria are measurable
- [ ] Risks are identified and mitigated
- [ ] Dependencies are documented
- [ ] Next steps are clear

**Approved by:** [Pending]
**Date:** [Pending]

---

## Execution Notes

This section will be updated during execution with:
- Actual time spent per phase
- Deviations from plan
- Unexpected challenges
- Quick wins
- Recommendations for next increment

**[To be filled during execution]**
