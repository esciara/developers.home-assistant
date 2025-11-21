# Phase 3: Validation Sub-agent

**Objective:** Create specialized sub-agent for HA integration validation

**Duration:** 6-10 hours (includes testing and documentation)

**Dependencies:** Phases 1-2 (Skills and Commands must exist)

---

## Overview

Phase 3 creates a validation sub-agent that performs comprehensive quality checks on HA integrations. The validator references all Skills for validation rules and runs automated tools.

**Launched by:** implement_plan_ha_integration command (automatic) or manually via Task tool

---

## Deliverable

### ha-integration-validator Sub-agent

Located in `.claude/agents/ha-integration-validator.md`

**Validation Capabilities:**
1. **Manifest Validation**
   - All required fields present (domain, name, documentation, codeowners, etc.)
   - Valid JSON structure
   - Proper dependency declarations
   - Version constraints valid

2. **File Structure Validation**
   - Required files present (__init__.py, manifest.json)
   - Platform files properly named
   - Config flow present if required
   - Proper directory structure

3. **Unique ID Stability Analysis**
   - Unique IDs follow recommended patterns (from ha-entity-knowledge)
   - Unique IDs are stable (don't change between restarts)
   - No hardcoded values that should be configurable
   - Device ID strategy appropriate

4. **Async Pattern Validation**
   - No blocking I/O in async contexts
   - Proper use of async/await
   - No requests library in async code
   - Async libraries used correctly (aiohttp, etc.)

5. **Error Handling Checks**
   - Try/except blocks present where needed
   - Errors logged appropriately
   - User-friendly error messages
   - Recovery strategies implemented

6. **Automated Tool Integration**
   - Run hassfest (HA validation tool)
   - Run mypy (type checking)
   - Run pylint (code quality)
   - Parse and report results

7. **Pattern Compliance**
   - References all Skills for validation rules
   - Checks against ha-common-mistakes patterns
   - Validates coordinator usage (if present)
   - Validates config flow patterns (if present)

**See:** [ha-integration-validator spec](../implementation/agents/ha-integration-validator.md)

---

## Implementation Steps

### Incremental Approach

Build validator components progressively:

1. **Create basic validator agent structure**
2. **Add manifest validation** (test, refine)
3. **Add file structure validation** (test, refine)
4. **Add code quality validation** (async patterns, error handling)
5. **Integrate automated tools** (hassfest, mypy, pylint)
6. **Test complete validator on real integrations**
7. **Tune rules to reduce false positives**
8. **Document usage and interpretation**

### Step-by-Step Process

#### A. Create Agent File

```bash
touch .claude/agents/ha-integration-validator.md
```

#### B. Write Agent Definition

Structure:
```markdown
# HA Integration Validator

**Purpose:** Validate HA integrations for quality and compliance

**Invocation:** Task tool or command

## Validation Steps

[Detailed validation protocol]

## Skills to Reference

- ha-integration-structure (file/manifest validation)
- ha-entity-knowledge (unique ID validation)
- ha-config-flow-knowledge (config flow validation)
- ha-coordinator-knowledge (coordinator validation)
- ha-common-mistakes (anti-pattern detection)

## Tools to Run

- hassfest
- mypy
- pylint

## Output Format

[Structured validation report]
```

#### C. Implement Validation Rules

**For each validation type:**
1. Define what to check
2. Reference relevant Skill for patterns
3. Determine pass/warn/fail criteria
4. Create actionable feedback

**Example - Unique ID Validation:**
```markdown
### Unique ID Validation

Reference: ha-entity-knowledge Skill

Check:
- unique_id property returns string
- Follows recommended pattern: {device_id}_{entity_type}_{channel}
- No hardcoded values
- Stable across restarts

Pass: Follows recommended pattern
Warn: Works but non-standard pattern
Fail: Missing or unstable unique_id
```

#### D. Integrate Automated Tools

**hassfest:**
```bash
python -m script.hassfest --integration <name>
```

**mypy:**
```bash
mypy homeassistant/components/<name>/
```

**pylint:**
```bash
pylint homeassistant/components/<name>/
```

Parse output and integrate into report

#### E. Test on Known-Good Integrations

Test validator on established integrations:
- Should produce minimal warnings
- Should not flag valid patterns
- Should complete in reasonable time (< 30s)

Tune rules to reduce false positives

#### F. Test on Known-Issues Integrations

Test on integrations with known issues:
- Should catch blocking I/O
- Should catch unstable unique IDs
- Should catch missing error handling
- Should provide actionable feedback

Ensure detection works correctly

#### G. Tune False Positive Rate

**Goal:** < 10% false positive rate

**If too many false positives:**
- Make rules more specific
- Add exceptions for valid edge cases
- Improve pattern matching
- Provide override mechanism

#### H. Document Validator

**Create documentation:**
- How to invoke validator
- Understanding validation report
- Common issues and fixes
- How to adjust validation rules
- When to override warnings

---

## Testing & Validation

### Known-Good Testing

**Test on established integrations:**
- [ ] Demo integration: Minimal false positives
- [ ] Met.no integration: Validates correctly
- [ ] MQTT integration: No false failures

**Criteria:**
- No false failures on quality integrations
- Warnings are legitimate (not false positives)
- Completes in < 30 seconds

### Known-Issues Testing

**Test on integrations with known issues:**
- [ ] Integration with blocking I/O: Detected
- [ ] Integration with unstable unique IDs: Detected
- [ ] Integration with missing error handling: Detected

**Criteria:**
- Catches real issues reliably
- Provides actionable feedback
- References relevant Skill patterns

### False Positive Tuning

**Measure false positive rate:**
```
False Positive Rate = (False Positives / Total Warnings) × 100%
```

**Target:** < 10%

**If > 10%:**
- Review false positive cases
- Adjust validation rules
- Add exceptions where appropriate
- Improve pattern matching

### Integration Testing

**Test within command workflow:**
- [ ] implement_plan_ha_integration launches validator automatically
- [ ] Validator integrates smoothly
- [ ] Output is actionable
- [ ] Validation catches issues before commit

**Test manual invocation:**
- [ ] Can invoke via: Task: ha-integration-validator
- [ ] Works on any integration
- [ ] Produces same quality results

### Performance Testing

**Criteria:**
- [ ] Completes in < 30s for typical integration
- [ ] < 1 min for complex integration
- [ ] Doesn't block workflow excessively

---

## Documentation

### Validator Usage Guide (`docs/validator-guide.md`)

**Contents:**
- How to use validator manually
- How to interpret validation reports
- Understanding pass/warn/fail levels
- Common issues and how to fix them
- How to adjust validation rules
- When warnings can be safely ignored
- How to override validation (if needed)

### Complete Workflow Guide (`docs/claude-ha-integration-workflow.md`)

**Contents:**
- Full end-to-end workflow including validation
- Skills → Commands → Validator integration
- Real example from start to finish:
  - Research existing integration
  - Create plan
  - Implement
  - Validate
  - Fix issues
  - Final validation pass
- Troubleshooting complete workflow
- Tips and best practices

### Update README

Add validation section:
```markdown
## Validation

The `ha-integration-validator` sub-agent validates integrations:

- Manifest completeness
- File structure
- Unique ID stability
- Async patterns
- Error handling

Launched automatically by `/implement_plan_ha_integration` or manually via Task tool.

See [Validator Guide](docs/validator-guide.md).
```

### Team Training Materials

**Quick Reference Card:**
- One-page guide to validation
- Common issues quick lookup
- How to interpret reports

**FAQ Document:**
- Why did validator flag this?
- How do I fix X error?
- Can I ignore Y warning?
- How do I add custom validation?

---

## Success Criteria

**Validator Created:**
- ✅ ha-integration-validator agent created and functional
- ✅ Uses all five knowledge Skills for validation rules
- ✅ Runs automated validation tools (hassfest, mypy, pylint)
- ✅ Provides actionable, detailed feedback

**Quality:**
- ✅ False positive rate < 10%
- ✅ Catches real issues reliably (blocking I/O, unstable IDs, etc.)
- ✅ Completes in < 30s for typical integration
- ✅ References relevant Skill patterns in reports

**Integration:**
- ✅ Integrates smoothly with implementation command
- ✅ Manual invocation works correctly
- ✅ Doesn't block workflow excessively

**Testing:**
- ✅ Tested on 5+ existing integrations
- ✅ Validated on known-good integrations
- ✅ Validated on known-issues integrations
- ✅ False positive rate measured and tuned

**Documentation:**
- ✅ Validator usage guide complete
- ✅ Complete workflow guide finished
- ✅ Team training materials created
- ✅ README updated

**Team Readiness:**
- ✅ Team trained on validator usage
- ✅ Team can interpret validation reports
- ✅ Team knows how to fix common issues
- ✅ Validator integrated into team workflow

---

## Validation Report Format

### Example Output

```markdown
# Validation Report: MQTT Integration

## ✅ Passed (15)

- Manifest: All required fields present
- File structure: Follows standard layout
- Unique IDs: Use recommended {device_id}_{type} pattern
- Config flow: Proper error handling
- Coordinator: Appropriate update interval (30s)
- No blocking I/O detected
- Error handling present in async methods
- hassfest: All checks passed
- mypy: No type errors
- [... 6 more passed checks]

## ⚠️ Warnings (2)

- **Coordinator: Update interval (60s) higher than typical**
  - Reference: ha-coordinator-knowledge recommends 30s for MQTT
  - Location: coordinator.py:45
  - Suggestion: Consider reducing to 30s for better responsiveness

- **Entity: device_info missing manufacturer field**
  - Reference: ha-entity-knowledge device info pattern
  - Location: sensor.py:78
  - Suggestion: Add manufacturer field for better device registry info

## ❌ Issues (1)

- **sensor.py:125: Blocking I/O call in async context**
  - Reference: ha-common-mistakes - "Don't use requests.get() in async"
  - Code: `response = requests.get(url)`
  - Fix: Use aiohttp instead:
    ```python
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    ```
  - Impact: High - will block event loop

## Summary

- **Total checks:** 18
- **Passed:** 15 (83%)
- **Warnings:** 2 (11%)
- **Issues:** 1 (6%)

**Recommendation:** Fix blocking I/O issue before merging. Warnings are low priority.
```

---

## Time Estimates

| Activity | Time | Notes |
|----------|------|-------|
| Basic validator structure | 1h | Agent definition |
| Manifest validation | 1h | Plus testing |
| File structure validation | 1h | Plus testing |
| Code quality validation | 2-3h | Async patterns, error handling |
| Automated tool integration | 1-2h | hassfest, mypy, pylint |
| Testing on real integrations | 2-3h | Multiple integrations |
| False positive tuning | 1h | Adjust rules |
| Documentation | 1-2h | Guides and training |

**Total:** 6-10 hours

---

## Next Steps

**After Phase 3 Complete:**
→ Workflow optimization complete!
→ See [Future Enhancements](../reference/future-enhancements.md) for expansion ideas

**Team Adoption:**
→ Train team on complete workflow
→ Integrate into development process
→ Gather feedback and iterate

---

## Resources

**Implementation:**
- [ha-integration-validator spec](../implementation/agents/ha-integration-validator.md)

**Testing:**
- [Integration Tests](../testing/integration-tests.md)

**Reference:**
- [Success Metrics](../reference/success-metrics.md)
- [Timeline](../reference/timeline.md)

---

**See Also:**
- [Phase 2: Commands](phase-2-commands.md) - Previous phase
- [Future Enhancements](../reference/future-enhancements.md) - What's next
- [Back to Main README](../README.md)
