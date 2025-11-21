# Extension System Workflow Optimization Plan v4

**Status:** Ready for Implementation
**Version:** v4-native-activation
**Last Updated:** 2025-11-21
**Target:** Home Assistant Integration Development
**Scope:** Optimize Claude Code workflow using native Skills, Commands, and Sub-agents

---

## What's Different in v4?

**v2 (monolithic):** Single 723-line file
**v3 (custom hooks):** 20+ focused documents with custom hook system
**v4 (native activation):** 20+ focused documents using Claude's built-in Skill activation

**Benefits:**
- **60-70% reduction in context per task** - Load only what you need
- **Faster navigation** - Direct links to relevant information
- **Easier maintenance** - Update individual components without affecting others
- **Parallel work** - Multiple people can work on different phases simultaneously
- **Simple setup** - No custom hooks, relies on Claude's native activation

---

## Executive Summary

This plan enhances the Claude Code workflow (research → plan → implement) for Home Assistant integrations using **100% Claude Code native features**:

- **Skills**: Knowledge base pointing to docs/ - auto-invoked via Claude's built-in activation
- **Commands**: Workflow orchestration - user-invoked
- **Sub-agents**: Complex validation tasks - tool-invoked

**Key Principle:** Skills don't duplicate docs/, they **guide navigation** to relevant documentation in `docs/` and leverage existing research in `thoughts/shared/research/`.

**Expected Impact:**
- 35-45% reduction in total workflow time
- 40-50% faster research phase
- 60% fewer implementation errors
- 70% fewer validation failures

---

## Quick Navigation

### 🚀 Getting Started

**Choose Your Path:**
- **Trial on existing integration?** → [MVP Approach](phases/mvp-approach.md) (8-12h)
- **Full implementation?** → Start with [Phase 1](phases/phase-1-skills.md)
- **Understanding the system first?** → [System Architecture](architecture/overview.md)

**Implementation Phases:**
1. [Phase 1: Skills Creation](phases/phase-1-skills.md) (8-12h) - **Start here**
2. [Phase 2: Specialized Commands](phases/phase-2-commands.md) (6-8h)
3. [Phase 3: Validation Sub-agent](phases/phase-3-validator.md) (4-6h)

**Total Estimated Effort:** 18-26 hours (MVP: 8-12 hours)

### 📐 Architecture & Design

- [System Architecture Overview](architecture/overview.md) - Component model and interaction
- [Component Interaction Model](architecture/component-interaction.md) - Skills → Commands → Agents flow

### 📚 Foundation Research

**All implementation details are in these research documents:**

- **Creating New Integrations**: `thoughts/shared/research/2025-11-20-home-assistant-integration-skill-research.md`
  - Integration structure, config flows, entities, testing
  - Quality scale requirements
  - Comprehensive patterns and requirements

- **Refactoring Existing Integrations**: `thoughts/shared/research/2025-11-21-home-assistant-integration-refactoring-patterns.md`
  - Config flow migration
  - Entity modernization
  - Quality tier upgrades
  - Runtime data migration

- **Home Assistant Documentation**: `docs/` directory
  - Source of truth for all patterns
  - Config flows: `docs/config_entries_*.md`
  - Entities: `docs/core/entity*.md`
  - Quality scale: `docs/core/integration-quality-scale/`
  - Testing: `docs/development_testing.md`

### 📚 Reference

- [Timeline & Effort Estimates](reference/timeline.md)
- [Success Metrics](reference/success-metrics.md)

---

## Architecture Overview

```
.claude/
├── skills/              # Knowledge navigators (point to docs/)
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

**How Components Work Together:**
1. User invokes: `/research_ha_integration`
2. Claude automatically activates relevant Skills based on SKILL.md descriptions
3. Skills guide Claude to relevant sections in `docs/` and research documents
4. Command may launch sub-agents for complex validation
5. Skills provide navigation context throughout entire workflow

**Read more:** [Component Interaction Model](architecture/component-interaction.md)

---

## What Goes in Skills

**Skills are NOT documentation duplicates.** They are:

✅ **Navigation guides** - "For config flows, see `docs/config_entries_config_flow_handler.md:14-49`"
✅ **Pattern reminders** - "Must test connection before completing config flow"
✅ **Quality requirements** - "Bronze tier requires: config-flow, entity-unique-id, has-entity-name"
✅ **Decision trees** - "Use DataUpdateCoordinator when polling multiple entities"
✅ **Checklists** - Quick validation lists

❌ **NOT detailed code examples** - Those are in `docs/` and research files
❌ **NOT skill creation how-tos** - Use Anthropic's `skill-creator` skill for that
❌ **NOT comprehensive references** - Point to `docs/` instead

**Skills answer:** "Where should I look?" and "What should I remember?"
**Docs answer:** "How do I implement this?"

---

## Recommended Path

**For config flow overhaul trial:**

1. **Preparation** (15 min)
   - Read [MVP Approach](phases/mvp-approach.md)
   - Read research: `thoughts/shared/research/2025-11-21-home-assistant-integration-refactoring-patterns.md` section 1

2. **MVP Implementation** (8-12h)
   - Create `ha-config-flow-knowledge` Skill
   - Create `research_ha_integration` Command
   - Test on real integration

3. **Expand if successful**
   - Add remaining Skills
   - Add remaining Commands
   - Add validation sub-agent

**See:** [MVP Approach](phases/mvp-approach.md) for detailed guidance

---

## Context Usage Guide

**When working on different tasks, load only these files:**

| Task | Load These Files | Lines |
|------|-----------------|-------|
| **Initial planning** | README.md + architecture/overview.md | ~250 |
| **Creating a Skill** | phase-1-skills.md + research docs | ~200 |
| **Creating a Command** | phase-2-commands.md | ~150 |
| **Checking progress** | README.md + reference/timeline.md | ~200 |

**Compare to v2:** Would load entire 723-line file for any task

---

## Quick Reference

**Total Effort:** 18-26 hours (MVP: 8-12 hours)

**Most Important Files to Read First:**
1. This README (you are here)
2. [System Architecture Overview](architecture/overview.md)
3. [Phase 1: Skills Foundation](phases/phase-1-skills.md)
4. [MVP Approach](phases/mvp-approach.md) - if doing trial first

---

**Plan Version:** v4-native-activation
**Key Difference from v3:** No custom hooks, relies on Claude's built-in Skill activation
**Status:** Ready for Implementation
**Next Step:** Read [MVP Approach](phases/mvp-approach.md) or [Phase 1](phases/phase-1-skills.md) to begin
