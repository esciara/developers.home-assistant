# Home Assistant Config Flow Knowledge Skill Implementation Plan

## Overview

Create the `ha-config-flow-knowledge` Claude Code Skill as a comprehensive, self-contained, composable skill that provides complete guidance for both creating new Home Assistant config flows and refactoring existing ones. This skill will eliminate the need for external documentation lookups during config flow development.

## Current State Analysis

**What Exists:**
- ✅ Comprehensive research document with ~3000 lines covering all config flow patterns
  - File: `thoughts/shared/research/2025-11-21-ha-config-flow-skill-implementation-research.md`
- ✅ Clear increment plan with defined deliverables and success criteria
  - File: `plans/increments/increment-01-config-flow-skill.md`
- ✅ Existing skill example for structure reference
  - File: `.claude/skills/python-development/SKILL.md`
- ✅ Skill authoring best practices documentation
  - Files: `claude-skills-docs/overview.md`, `claude-skills-docs/authoring-best-practices.md`

**What's Missing:**
- ❌ Skill directory structure and files
- ❌ SKILL.md with navigation and activation description
- ❌ Domain-organized content files (new-implementation/, refactoring/, shared/)
- ❌ Code templates and examples
- ❌ Testing patterns and coverage guidance
- ❌ Validation with real integration work

### Key Discoveries:

- **Progressive Disclosure Pattern**: Skills use filesystem-based architecture where only referenced files are loaded (zero token cost until read)
- **Composability via Domain Organization**: BigQuery skill pattern demonstrates how to organize content by domain for selective loading
- **SKILL.md Constraints**: Must be < 500 lines, written in third person, one-level deep references only
- **Auto-Activation**: Description field must include both what the skill does AND when to use it with key trigger terms

## Desired End State

A fully functional Claude Code Skill that:

1. **Auto-activates** when developers work on Home Assistant config flows (create or refactor)
2. **Provides complete guidance** without external documentation lookups
3. **Loads only relevant content** via domain-based organization (new-implementation/ vs refactoring/)
4. **Includes working templates** ready to copy and customize
5. **Achieves 100% coverage** of config flow patterns from research

### Verification:

**Automated:**
- [ ] Skill directory structure exists: `.claude/skills/ha-config-flow-knowledge/`
- [ ] SKILL.md passes frontmatter validation (name, description fields)
- [ ] All referenced files exist and are readable
- [ ] No broken internal links
- [ ] File structure matches increment plan

**Manual:**
- [ ] Skill activates on prompt "How do I create a config flow?"
- [ ] Skill activates when working on `config_flow.py` files
- [ ] Can complete new config flow creation without external docs
- [ ] Can identify and fix anti-patterns without external docs
- [ ] Real integration trial completed successfully (zero external doc lookups)

## What We're NOT Doing

**Out of Scope for This Implementation:**
- ❌ Other Skills (ha-entity-knowledge, ha-coordinator-knowledge, etc.)
- ❌ Slash Commands (/research_ha_integration, etc.)
- ❌ Sub-agents (ha-integration-validator)
- ❌ Content beyond config flows (entities, coordinators belong in separate skills)
- ❌ Custom hooks or advanced activation logic
- ❌ Live examples from actual integration repositories (links are fine, but not cloning repos)
- ❌ Executable Python scripts (.py files) - only markdown documentation with code examples

## Implementation Approach

### Strategy: Composable Skill with Domain Organization

Following the BigQuery skill pattern from the docs, we'll create a single skill with domain-based organization:

```
.claude/skills/ha-config-flow-knowledge/
├── SKILL.md                           # Navigation hub (<500 lines)
│
├── new-implementation/                # Only loaded for "create flow" tasks
│   ├── overview.md
│   ├── user-flows.md
│   ├── discovery-flows.md
│   ├── authentication-flows.md
│   ├── options-flows.md
│   ├── multi-step-flows.md
│   └── templates/
│       ├── basic-user-flow.md
│       ├── discovery-flow.md
│       ├── reauth-flow.md
│       └── options-flow.md
│
├── refactoring/                       # Only loaded for "refactor flow" tasks
│   ├── overview.md
│   ├── anti-patterns.md
│   ├── migration-guides.md
│   └── before-after-examples.md
│
└── shared/                            # Loaded by both domains
    ├── error-handling.md
    ├── schema-definitions.md
    ├── testing-patterns.md
    ├── coverage-guide.md
    └── requirements-checklist.md
```

**Why This Works:**
- Progressive disclosure: Unread files cost zero tokens
- Clear navigation: SKILL.md directs to right domain
- Shared knowledge: Error handling, testing, schemas used by both
- Maintainable: Easy to update one domain without affecting the other

---

## Phase 1: Foundation & Core Structure

### Overview
Establish the skill directory structure, create SKILL.md with proper frontmatter and navigation, and set up the shared/ directory with foundational patterns used by both new implementation and refactoring workflows.

**Deliverable**: Skill structure exists, activates correctly, and provides navigation to domains

### Changes Required:

#### 1. Create Skill Directory Structure

**Directory**: `.claude/skills/ha-config-flow-knowledge/`

**Structure**:
```bash
mkdir -p .claude/skills/ha-config-flow-knowledge/new-implementation/templates
mkdir -p .claude/skills/ha-config-flow-knowledge/refactoring
mkdir -p .claude/skills/ha-config-flow-knowledge/shared
```

#### 2. Create SKILL.md with Frontmatter and Navigation

**File**: `.claude/skills/ha-config-flow-knowledge/SKILL.md`

**Content Structure** (complete implementation in file):
- YAML frontmatter with name and description
- Overview section
- When to Use This Skill section
- Quick Navigation by task type
- Domain overviews (one-level references)

**Key Requirements**:
- Name: `ha-config-flow-knowledge` (lowercase, hyphens only)
- Description: Third person, includes "what" and "when" with trigger terms
- Body: < 500 lines
- References: One level deep only

#### 3. Create Shared Patterns Files

**Files in `shared/` directory:**

**a) `shared/error-handling.md`**
- Standard error types (cannot_connect, invalid_auth, unknown)
- Exception handling patterns
- Translation patterns for strings.json
- Field-specific vs base errors
- Recoverable vs fatal errors

**b) `shared/schema-definitions.md`**
- Required vs optional fields
- Common validators (cv.string, cv.port, etc.)
- Modern selectors (TextSelector, EntitySelector, etc.)
- Default values and suggested values
- Sections for grouping fields
- Conditional schemas

**c) `shared/testing-patterns.md`**
- 100% coverage requirement
- Basic test structure (Given/When/Then)
- Common test fixtures
- Running coverage tests
- Mocking patterns

**d) `shared/requirements-checklist.md`**
- Bronze tier requirements (config flow, testing, unique ID)
- Silver tier requirements (unload, reauth)
- Gold tier requirements (discovery, reconfigure)
- Translation requirements

### Success Criteria:

#### Automated Verification:
- [ ] Directory structure exists: `ls .claude/skills/ha-config-flow-knowledge/`
- [ ] SKILL.md has valid YAML frontmatter: `head -10 SKILL.md | grep "name:"`
- [ ] All shared/ files exist: `ls shared/*.md | wc -l` (should be 4)
- [ ] No broken markdown syntax: Files can be rendered

#### Manual Verification:
- [ ] Skill appears in available skills list (ask Claude "What skills are available?")
- [ ] Skill activates on prompt: "How do I create a config flow?"
- [ ] Skill activates on prompt: "How do I refactor an existing config flow?"
- [ ] Navigation in SKILL.md is clear and organized
- [ ] Shared patterns are comprehensive and accurate

**Implementation Note**: After completing this phase, test activation with multiple prompts before proceeding. Verify that SKILL.md navigation is intuitive.

---

## Phase 2: New Implementation - Basic Flows

### Overview
Create comprehensive guidance for implementing basic config flows including user flows with connection testing, error handling, and unique ID management. This phase covers the most common config flow scenario.

**Deliverable**: Can create a basic user flow with connection testing using only skill content

### Changes Required:

#### 1. Create New Implementation Overview

**File**: `new-implementation/overview.md`

**Content**:
- When to use new implementation (creating flows from scratch)
- Flow types available (user, discovery, reauth, reconfigure, options)
- Bronze tier minimum requirements
- Quick start guidance
- Links to specific flow type files

#### 2. Create User Flow Patterns

**File**: `new-implementation/user-flows.md`

**Content from Research**:
- Basic user flow pattern (Section 2.1)
- User flow with connection testing (Section 2.2) - BRONZE REQUIREMENT
- Error handling integration
- Unique ID handling
- Preventing duplicates with `_abort_if_unique_id_configured()`
- Complete step-by-step implementation guide

#### 3. Create Basic User Flow Template

**File**: `new-implementation/templates/basic-user-flow.md`

**Content**:
```markdown
# Basic Config Flow Template

## Overview
Complete, working config flow template for user-initiated setup with connection testing, error handling, and unique ID management.

## Template Code

[Include complete template from research Section 7.1]

## Customization Points

**Required Changes:**
- [ ] Replace `MyClient` with your client class
- [ ] Replace `get_device_id()` with your unique ID method
- [ ] Update exception types to match your library
- [ ] Customize CONF_* constants

**Optional Changes:**
- [ ] Add additional fields to schema
- [ ] Add custom validation logic
- [ ] Customize entry title

## Testing This Flow

[Link to shared/testing-patterns.md with specific guidance]

## Common Issues

- **Issue**: Entry created without connection test
  **Solution**: Ensure try/except wraps client call before `async_create_entry`

- **Issue**: Duplicate entries created
  **Solution**: Add `_abort_if_unique_id_configured()` after `async_set_unique_id()`
```

### Success Criteria:

#### Automated Verification:
- [ ] Files exist: `ls new-implementation/*.md new-implementation/templates/*.md`
- [ ] No broken links: All references to shared/ files are valid
- [ ] Template code is syntactically valid Python

#### Manual Verification:
- [ ] Can create a basic user flow by following overview.md
- [ ] user-flows.md explains all key concepts clearly
- [ ] Template can be copied and customized without external docs
- [ ] Error handling patterns are clear and complete
- [ ] Unique ID guidance prevents common mistakes

**Implementation Note**: Test by attempting to create a simple user flow for a fictional integration using only the skill content. Note any missing information.

---

## Phase 3: New Implementation - Discovery & Advanced Flows

### Overview
Add discovery flow patterns (zeroconf, SSDP), multi-step flows, and options flows. Enables creating advanced config flow scenarios.

**Deliverable**: Can create discovery flows and multi-step flows using only skill content

### Changes Required:

#### 1. Create Discovery Flow Patterns

**File**: `new-implementation/discovery-flows.md`

**Content from Research**:
- Zeroconf/mDNS discovery (Section 2.3)
- SSDP discovery patterns
- Unique ID from discovery info
- IP address updates on rediscovery
- Discovery confirmation requirement
- Manifest configuration
- Multiple discovery types (Section 8.1)

#### 2. Create Multi-Step Flow Patterns

**File**: `new-implementation/multi-step-flows.md`

**Content from Research**:
- Multi-step flow pattern (Section 2.7)
- Data passing between steps
- Validation between steps (Section 8.2)
- Progress dialogs (Section 2.8)
- Reserved step names (Section 2.9)

#### 3. Create Options Flow Patterns

**File**: `new-implementation/options-flows.md`

**Content from Research**:
- Options flow basics (Section 2.6)
- Registration pattern
- Suggested values
- Conditional fields (Section 8.3)
- Options vs reconfigure decision guide

#### 4. Create Discovery Flow Template

**File**: `new-implementation/templates/discovery-flow.md`

**Content**:
- Complete template from Section 7.2
- Manifest configuration example
- Customization points
- Testing guidance

#### 5. Create Options Flow Template

**File**: `new-implementation/templates/options-flow.md`

**Content**:
- Complete options flow template
- Registration in config flow
- Suggested values pattern
- Testing guidance

### Success Criteria:

#### Automated Verification:
- [ ] All files created: `ls new-implementation/*.md | wc -l` (should be 6)
- [ ] All templates created: `ls new-implementation/templates/*.md | wc -l` (should be 3)
- [ ] No broken internal links
- [ ] Template code is syntactically valid

#### Manual Verification:
- [ ] Can implement zeroconf discovery following discovery-flows.md
- [ ] Discovery template is complete and customizable
- [ ] Multi-step flow patterns are clear with examples
- [ ] Options flow guidance distinguishes from reconfigure
- [ ] Can implement options flow without external docs

**Implementation Note**: Test by creating a discovery flow for a fictional zeroconf device. Verify manifest configuration is clear.

---

## Phase 4: New Implementation - Authentication Flows

### Overview
Add comprehensive reauth and reconfigure flow patterns, including helper methods, unique ID verification, and proper triggering from integration code.

**Deliverable**: Can implement reauth and reconfigure flows using only skill content

### Changes Required:

#### 1. Create Authentication Flow Patterns

**File**: `new-implementation/authentication-flows.md`

**Content from Research**:
- When to use reauth vs reconfigure (Section 5.1)
- Reauth flow pattern (Section 2.4)
- Reconfigure flow pattern (Section 2.5)
- Helper methods (Section 5.2)
  - `_get_reauth_entry()`
  - `_get_reconfigure_entry()`
  - `async_update_reload_and_abort()`
- Unique ID verification (Section 5.3)
- Triggering reauth from integration (Section 5.4)
  - From async_setup_entry
  - From DataUpdateCoordinator
  - From entity methods

#### 2. Create Reauth Flow Template

**File**: `new-implementation/templates/reauth-flow.md`

**Content**:
```markdown
# Reauthentication Flow Template

## Overview
Complete template for handling expired credentials and authentication failures automatically.

## Template Code

[Complete template from Section 7.3 - reauth portion]

## Triggering Reauth

### From async_setup_entry
[Code example from Section 5.4]

### From DataUpdateCoordinator
[Code example from Section 5.4]

### From Entity Methods
[Code example from Section 5.4]

## Customization Points

- [ ] Replace authentication method
- [ ] Update unique ID verification
- [ ] Customize error messages

## Testing

[Specific test patterns from Section 6.6]

## Common Mistakes

- **Missing unique ID verification**: Always verify same account with `_abort_if_unique_id_mismatch`
- **Using data= instead of data_updates=**: Use data_updates to merge with existing
- **Not triggering reload**: `async_update_reload_and_abort` handles this automatically
```

#### 3. Update shared/testing-patterns.md

**Changes**: Add reauth flow test patterns from Section 6.6

### Success Criteria:

#### Automated Verification:
- [ ] authentication-flows.md exists and has all sections
- [ ] Reauth template exists with complete code
- [ ] shared/testing-patterns.md updated with reauth tests
- [ ] No broken links to helper methods

#### Manual Verification:
- [ ] Reauth vs reconfigure decision guide is clear
- [ ] Can implement reauth flow from template
- [ ] Triggering reauth from different locations is explained
- [ ] Unique ID verification pattern prevents account switching
- [ ] Helper methods are documented with examples

**Implementation Note**: After this phase, verify that the distinction between reauth (automatic) and reconfigure (manual) is crystal clear.

---

## Phase 5: Refactoring Patterns

### Overview
Create comprehensive guidance for refactoring existing config flows, including anti-pattern identification, migration guides, before/after examples, and deprecation timelines.

**Deliverable**: Can identify and fix config flow anti-patterns using only skill content

### Changes Required:

#### 1. Create Refactoring Overview

**File**: `refactoring/overview.md`

**Content**:
- When to refactor (upgrading to Bronze/Silver/Gold tier)
- Quick assessment checklist (from Section 11.1)
- Red flags in code (from Section 11.1)
- Incremental refactoring strategy
- Priority-based approach (Section 11.4)

#### 2. Create Anti-Patterns Guide

**File**: `refactoring/anti-patterns.md`

**Content from Research Section 11.2**:

Each anti-pattern with:
- ❌ Problem code example
- ⚠️ Impact description
- ✅ Solution code example

**Anti-patterns to cover**:
1. No connection testing
2. Using IP address as unique ID
3. Discovery without user confirmation
4. Missing unique ID check
5. Direct config entry mutation
6. Old reauth pattern
7. Old ServiceInfo imports
8. Manual single-instance check
9. Using hass.data instead of runtime_data
10. Missing reauth unique ID verification

#### 3. Create Migration Guides

**File**: `refactoring/migration-guides.md`

**Content from Research Section 11.3**:
- OAuth2 error handling (2025.12)
- ServiceInfo imports (deadline 2026.2)
- Options flow self.config_entry (2025.12)
- Reauth/reconfigure entry linking (2025.12)
- Config entry updates (mandatory since 2024.9)
- async_show_progress requires progress_task (mandatory since 2024.8)
- Runtime data storage (best practice)
- Single config entry manifest (best practice)
- Config entry state management (2025.3.0+)

Each with:
- What changed
- Migration code examples
- Deadline
- Backwards compatibility notes

#### 4. Create Before/After Examples

**File**: `refactoring/before-after-examples.md`

**Content from Research Section 11.5**:
- Adding discovery to existing manual-only flow
- Adding reauth flow to existing config flow
- Splitting single-step into multi-step
- Updating old validators to modern selectors

Each with complete before/after code.

### Success Criteria:

#### Automated Verification:
- [ ] All refactoring/ files exist: `ls refactoring/*.md | wc -l` (should be 4)
- [ ] Anti-patterns file has all 10 patterns
- [ ] Migration guides have all 9 migrations
- [ ] Before/after examples have all 4 scenarios

#### Manual Verification:
- [ ] Can identify anti-patterns in unfamiliar config flow
- [ ] Quick assessment checklist is actionable
- [ ] Migration guides are clear with deadlines
- [ ] Before/after examples are complete and accurate
- [ ] Refactoring strategy is incremental and safe

**Implementation Note**: Test by reviewing a real HA integration config flow and identifying anti-patterns using only the skill content.

---

## Phase 6: Testing, Polish & Real Integration Trial

### Overview
Complete testing guidance for 100% coverage, conduct real integration trial, iterate based on findings, and finalize the skill.

**Deliverable**: Zero external doc lookups during real integration work

### Changes Required:

#### 1. Complete Testing Patterns

**File**: `shared/coverage-guide.md`

**Content from Research Section 6**:
- Achieving 100% coverage requirement
- Coverage tools and commands
- Test patterns for each flow type:
  - Basic user flow (Section 6.3)
  - Error handling (Section 6.4)
  - Already configured (Section 6.5)
  - Reauth flow (Section 6.6)
  - Discovery flow (if applicable)
  - Reconfigure flow (if applicable)
  - Options flow (if applicable)
- Common test fixtures (Section 6.7)
- Mocking strategies

#### 2. Update shared/testing-patterns.md

**Enhancements**:
- Add specific test patterns for discovery flows
- Add reconfigure flow test patterns
- Add options flow test patterns
- Integration with coverage-guide.md

#### 3. Identify Test Integration

**Task**: Find suitable Home Assistant integration for real trial

**Criteria for Test Integration**:
- Has config flow but needs refactoring
- Contains at least 2-3 anti-patterns from the list
- Is simple enough to refactor in reasonable time (< 2 hours)
- Ideally needs:
  - Connection testing added
  - Unique ID handling improved
  - Reauth flow added

**Document Selection**:
Create `thoughts/shared/plans/ha-config-flow-skill-test-integration.md`:
```markdown
# Config Flow Skill Test Integration

## Selected Integration
[Name of integration]

## Current State
- **Anti-patterns identified**:
  - [List 2-3 anti-patterns found]
- **Missing features**:
  - [e.g., reauth flow, connection testing]
- **Quality tier**: [Current tier]

## Refactoring Plan
1. [Step 1 - e.g., Add connection testing]
2. [Step 2 - e.g., Implement reauth flow]
3. [Step 3 - e.g., Add unique ID handling]

## Success Criteria
- [ ] All anti-patterns fixed
- [ ] 100% config flow test coverage achieved
- [ ] Zero external documentation lookups
- [ ] Config flow follows current best practices
```

#### 4. Conduct Real Integration Trial

**Process**:
1. Use skill to refactor selected integration
2. Document every time you need to look up external information
3. Note any missing patterns or unclear guidance
4. Track time spent on each refactoring step
5. Verify all changes with tests

**Deliverable**: Trial report documenting:
- External doc lookups (goal: 0)
- Missing skill content identified
- Unclear or confusing patterns
- Time spent (should be reasonable)
- Success in achieving refactoring goals

#### 5. Iterate Based on Findings

**Task**: Update skill content based on trial findings

**Process**:
- Add any missing patterns discovered
- Clarify confusing guidance
- Add examples for unclear scenarios
- Update navigation if needed
- Re-test after updates

#### 6. Final Polish

**Tasks**:
- Review all files for consistency
- Check all internal links work
- Verify SKILL.md < 500 lines
- Ensure all code examples are syntactically valid
- Proofread all content
- Verify activation with test prompts

### Success Criteria:

#### Automated Verification:
- [ ] coverage-guide.md exists with complete patterns
- [ ] Test integration selection documented
- [ ] All files under 2000 lines (progressive disclosure working)
- [ ] SKILL.md under 500 lines
- [ ] No broken internal links
- [ ] All code examples pass basic Python syntax check

#### Manual Verification:
- [ ] Test integration trial completed
- [ ] Zero external doc lookups during trial
- [ ] All identified anti-patterns successfully fixed
- [ ] 100% coverage achieved on test integration
- [ ] Trial report documents success
- [ ] Skill content updated based on findings
- [ ] Activation works on all test prompts:
  - "How do I create a config flow?"
  - "How do I refactor an existing config flow?"
  - "How do I implement reauthentication?"
  - "How do I add discovery to my integration?"
- [ ] Can complete full config flow development cycle without external docs

**Implementation Note**: This phase validates the entire skill. If trial reveals significant gaps, iterate until zero external lookups achieved.

---

## Testing Strategy

### Activation Testing

**Test Prompts** (skill should activate):
- "How do I create a config flow?"
- "How do I refactor an existing config flow?"
- "async_step_user pattern"
- "config entry validation"
- "implementing reauthentication flow"
- "100% config flow test coverage"
- "fixing config flow anti-patterns"

**Test Files** (skill should activate when working on):
- `config_flow.py`
- `test_config_flow.py`

**Negative Tests** (skill should NOT activate):
- "How do I create an entity?"
- "Data coordinator patterns"
- Working on `sensor.py`

### Content Completeness Testing

**For New Implementation:**
- [ ] Can implement basic user flow start to finish
- [ ] Can add zeroconf discovery
- [ ] Can implement reauth flow
- [ ] Can implement reconfigure flow
- [ ] Can implement options flow
- [ ] Can achieve 100% test coverage

**For Refactoring:**
- [ ] Can identify all 10 anti-patterns
- [ ] Can fix each anti-pattern with provided solution
- [ ] Can follow migration guides for deprecations
- [ ] Can apply before/after examples

### Real-World Testing

**Minimum Trial**:
- Complete one config flow refactoring task
- Document external doc lookups (goal: 0)
- Measure time to find information
- Verify all needed patterns are present

**Ideal Trial**:
- Complete 3+ config flow tasks (mix of new + refactor)
- Zero external lookups across all tasks
- Time to find info reduced by 60%+
- Team member endorses skill

## Performance Considerations

### Token Usage

**Progressive Disclosure Benefits**:
- SKILL.md only ~400-500 lines (minimal load)
- Domain files only load when relevant
- Unread files consume zero tokens
- User for new flow? Only new-implementation/ loads
- User for refactoring? Only refactoring/ loads

**Estimated Token Costs**:
- Activation metadata: ~100 tokens (frontmatter only)
- SKILL.md: ~500-800 tokens
- One domain (new or refactor): ~2000-3000 tokens
- Shared patterns: ~1000-1500 tokens
- Total for typical session: ~3500-5300 tokens

**Compare to Without Skill**:
- External doc lookups: Multiple context switches
- Web searches: Less focused, more scattered
- No progressive disclosure: All or nothing

### Maintenance

**Update Frequency**:
- Deprecations: Review quarterly for HA blog posts
- Anti-patterns: Add as discovered in community
- Examples: Update when HA core patterns change
- Testing: Update when pytest patterns evolve

**Validation**:
- Test activation after each update
- Re-run real integration trial annually
- Track external doc lookup count over time

## Migration Notes

N/A - This is a new skill, not migrating existing functionality.

## References

- **Increment Plan**: `plans/increments/increment-01-config-flow-skill.md`
- **Research Document**: `thoughts/shared/research/2025-11-21-ha-config-flow-skill-implementation-research.md`
- **Skill Best Practices**: `claude-skills-docs/authoring-best-practices.md`
- **Skill Overview**: `claude-skills-docs/overview.md`
- **Example Skill**: `.claude/skills/python-development/SKILL.md`

---

## Appendix: File Size Estimates

**To verify progressive disclosure is working:**

| File | Estimated Lines | Token Estimate |
|------|----------------|----------------|
| SKILL.md | 400-500 | 600-800 |
| new-implementation/overview.md | 100-150 | 150-250 |
| new-implementation/user-flows.md | 200-300 | 300-500 |
| new-implementation/discovery-flows.md | 200-300 | 300-500 |
| new-implementation/authentication-flows.md | 250-350 | 400-600 |
| new-implementation/options-flows.md | 150-200 | 200-350 |
| new-implementation/multi-step-flows.md | 150-200 | 200-350 |
| new-implementation/templates/* | 100-150 each | 150-250 each |
| refactoring/overview.md | 100-150 | 150-250 |
| refactoring/anti-patterns.md | 400-500 | 600-800 |
| refactoring/migration-guides.md | 300-400 | 500-650 |
| refactoring/before-after-examples.md | 300-400 | 500-650 |
| shared/error-handling.md | 150-200 | 250-350 |
| shared/schema-definitions.md | 200-250 | 350-450 |
| shared/testing-patterns.md | 200-250 | 350-450 |
| shared/coverage-guide.md | 250-350 | 400-600 |
| shared/requirements-checklist.md | 100-150 | 150-250 |

**Key Insight**: Even though total content is ~4000-5500 lines, typical usage loads only 800-1500 lines due to progressive disclosure.
