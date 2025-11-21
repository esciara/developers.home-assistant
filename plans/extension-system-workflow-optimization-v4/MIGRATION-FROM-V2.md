# Migrating from v2 to v3

**Why v3?** The v3 composable structure reduces context usage by 60-70% compared to the v2 monolithic file.

---

## What Changed

### v2 (Monolithic)
- Single 723-line file
- Load entire file for any task
- Hard to navigate
- Difficult to maintain

### v3 (Composable)
- 20+ focused documents
- Load only what you need (150-350 lines typically)
- Direct navigation to relevant info
- Easy to update individual components

---

## File Mapping

| v2 Section | v3 Location |
|------------|-------------|
| Executive Summary | `README.md` (lines 1-50) |
| Architecture Overview | `architecture/overview.md` |
| Hook System (lines 73-171) | `architecture/overview.md` |
| Component Interaction | `architecture/component-interaction.md` |
| Phase 1 (lines 174-319) | `phases/phase-1-skills.md` |
| Phase 2 (lines 322-419) | `phases/phase-2-commands.md` |
| Phase 3 (lines 422-514) | `phases/phase-3-validator.md` |
| MVP Section (lines 589-639) | `phases/mvp-approach.md` |
| Timeline (lines 517-548) | `reference/timeline.md` |
| Success Metrics (lines 551-569) | `reference/success-metrics.md` |
| Risk Mitigation (lines 572-586) | `reference/risk-mitigation.md` (to be created) |
| Future Enhancements (lines 642-670) | `reference/future-enhancements.md` (to be created) |

---

## How to Use v3

### Starting a Task

**Instead of:** Opening entire v2 file

**Do this:**
1. Start at `README.md` for navigation
2. Click to specific document you need
3. Load only that document (150-350 lines)

### Example Workflows

**Planning the project:**
```
1. Read: README.md (overview + navigation)
2. Read: architecture/overview.md (understand system)
3. Read: architecture/overview.md (critical component)
4. Read: phases/mvp-approach.md OR phases/phase-1-skills.md
```
**Context:** ~600-800 lines total (vs 723 for everything)

**Implementing Phase 1:**
```
1. Read: phases/phase-1-skills.md (your current phase)
2. Read: architecture/overview.md (setup guide)
3. Read: implementation/skills/_template.md (when creating Skills)
4. Read: implementation/skills/ha-config-flow-knowledge.md (specific Skill spec)
```
**Context:** ~500-700 lines total (vs 723 for everything)

**Creating a specific Skill:**
```
1. Read: implementation/skills/[skill-name].md (specific spec)
2. Read: implementation/skills/_template.md (template structure)
3. Reference: examples/skill-rules-examples.json (trigger patterns)
```
**Context:** ~300-400 lines total (vs 723 for everything)

**Checking progress:**
```
1. Read: README.md (status overview)
2. Read: reference/timeline.md (where you are)
```
**Context:** ~250 lines total (vs 723 for everything)

---

## Benefits

### Context Efficiency

| Task | v2 Context | v3 Context | Savings |
|------|-----------|-----------|---------|
| Planning | 723 lines | ~300 lines | 58% |
| Phase 1 setup | 723 lines | ~350 lines | 52% |
| Creating Skill | 723 lines | ~250 lines | 65% |
| Checking progress | 723 lines | ~250 lines | 65% |

**Average savings: 60-70%**

### Navigation

**v2:** Search through 723 lines to find specific section

**v3:** Direct link to exact document you need

### Maintenance

**v2:** Update means scrolling through entire file

**v3:** Update only the specific document that changed

### Collaboration

**v2:** One person editing at a time (conflicts likely)

**v3:** Multiple people can edit different documents simultaneously

---

## For Your Use Case (Config Flow Overhaul)

### v2 Approach:
1. Open v2-high-level.md (723 lines)
2. Scroll to Phase 1
3. Find config flow Skill info
4. Scroll to MVP section
5. Cross-reference hook system section

**Total context:** 723 lines

### v3 Approach:
1. Open: `README.md` → See "Trial on existing integration"
2. Click: `phases/mvp-approach.md` (see config flow option)
3. Click: `implementation/skills/ha-config-flow-knowledge.md` (detailed spec)
4. Reference: `examples/skill-rules-examples.json` (trigger patterns)

**Total context:** ~400 lines (45% savings)

**Benefit:** Directly navigate to config flow specifics without loading irrelevant information about coordinators, validators, etc.

---

## Quick Start with v3

### 1. Start Here
`README.md` - Entry point with navigation

### 2. Understand System
`architecture/overview.md` - Critical to understand first

### 3. Choose Path
- MVP trial: `phases/mvp-approach.md`
- Full implementation: `phases/phase-1-skills.md`

### 4. Implement
Follow phase guides, reference implementation specs as needed

---

## v2 is Still Available

The v2 monolithic file remains at:
`plans/extension-system-workflow-optimization-plan-v2-high-level.md`

**Keep v2 for:**
- Reference
- Searching across all content
- Getting complete overview in one file

**Use v3 for:**
- Actual implementation work
- Loading only relevant context
- Efficient navigation
- Collaborative editing

---

## Next Steps

1. **Read v3 README:** `plans/extension-system-workflow-optimization-v3/README.md`
2. **Understand hooks:** `plans/extension-system-workflow-optimization-v3/architecture/overview.md`
3. **Start MVP:** `plans/extension-system-workflow-optimization-v3/phases/mvp-approach.md`

---

**Questions?** See `README.md` for complete navigation and guidance.
