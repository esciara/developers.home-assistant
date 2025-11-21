# Phase 3: Validation Sub-agent

**Objective:** Create specialized sub-agent for HA integration validation

**Duration:** 4-6 hours

**Dependencies:** Phases 1-2 (Skills and Commands exist)

---

## Overview

Phase 3 creates a validation sub-agent that performs comprehensive checks on HA integrations. The sub-agent uses all five Skills to validate against HA requirements.

**Key Features:**
- Automated validation using hassfest, mypy, pylint
- Pattern validation using Skills' documentation maps
- Quality scale compliance checking
- Detailed, actionable reports

---

## Deliverables

### ha-integration-validator Agent

Located in `.claude/agents/ha-integration-validator.md`

**What it validates:**
- **Structure**: Manifest completeness, file organization
- **Code Quality**: Async patterns, blocking I/O, type hints
- **Entity Patterns**: Unique ID stability, device info, has_entity_name
- **Config Flow**: Test coverage, error handling, connection testing
- **Quality Scale**: Bronze/Silver/Gold/Platinum tier requirements
- **Testing**: Coverage thresholds, test structure

**Points to:**
- All five Skills for validation rules
- `docs/core/integration-quality-scale/` for quality requirements
- Research docs for patterns

**Automated tools:**
- `python3 -m script.hassfest` - Manifest and structure validation
- `pytest` with coverage - Test validation
- Type checking - If strict typing enabled

**Output structure:**
- **Summary**: Pass/fail with tier level
- **Issues**: Categorized by severity (error/warning/info)
- **Recommendations**: With pointers to docs/
- **Quality tier**: Current tier and next steps

---

## Integration Points

**Called from:**
- `implement_plan_ha_integration` command (automatic)
- Manual: Use Task tool with sub-agent name
- CI/CD: Can be integrated into workflows

**Usage example:**
```
User: "Validate the example integration"
Claude: *Uses Task tool to launch ha-integration-validator*
Agent: *Performs comprehensive checks, returns report*
```

---

## Success Criteria

- [ ] Validator agent created
- [ ] Uses all five Skills for validation rules
- [ ] Runs automated tools (hassfest, pytest)
- [ ] Provides actionable feedback
- [ ] Tested on known-good and known-bad integrations
- [ ] False positive rate acceptable (<10%)
- [ ] Performance acceptable (<2 min for typical integration)

---

## Testing Strategy

**Test on:**
1. **Known-good integrations** - Should validate successfully with minimal warnings
2. **Known-issue integrations** - Should catch specific issues
3. **Various quality tiers** - Bronze, Silver, Gold examples

**Tune for:**
- False positive rate (target: <10%)
- Clear,actionable messages
- Appropriate severity levels

---

## Estimated Effort

| Task | Time | Rationale |
|------|------|-----------|
| Agent structure | 1h | Basic sub-agent setup |
| Validation logic | 2-3h | Implement checks using Skills |
| Tool integration | 1-2h | hassfest, pytest integration |
| Testing & tuning | 1-2h | Test and refine |
| **Total** | **4-6h** | |

---

## Next Steps

After Phase 3 complete:
- Full workflow available (Skills → Commands → Validator)
- Measure impact vs generic workflow
- Document usage patterns
- Train team

**See also:**
- [Phase 1](phase-1-skills.md) - Skills the validator uses
- [Phase 2](phase-2-commands.md) - Commands that call the validator
- [Success Metrics](../reference/success-metrics.md) - How to measure impact
