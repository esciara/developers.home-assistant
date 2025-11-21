# ha-quality-scale Skill Implementation Spec

**Objective:** Provide the official Home Assistant Integration Quality Scale framework with tier-by-tier implementation guidance

**Priority:** CRITICAL - Quality Scale is the official HA framework for integration quality

**Estimated effort:** 2-3 hours

**Dependencies:** Used throughout integration development to guide quality improvements

---

## Why This Skill is Critical

**From HA Research:**
- **Official HA quality framework** (research: 116-141, 547-562)
- **4 tiers**: Bronze (baseline) → Silver (reliability) → Gold (UX) → Platinum (excellence)
- **50+ specific quality rules** across all tiers
- **Tier determines feature discoverability** in HA
- **Higher tiers get priority support** and visibility

**Without this Skill:**
- Developers don't know quality requirements
- Integration stuck at Bronze tier (minimal features)
- Missing features required for Silver/Gold/Platinum
- Can't achieve higher quality tiers systematically
- No clear roadmap for quality improvement

---

## Skill Structure

```
.claude/skills/ha-quality-scale/
├── SKILL.md                          # Main Skill definition
├── quality-scale-overview.md         # Framework overview
├── bronze-tier.md                    # Bronze tier requirements
├── silver-tier.md                    # Silver tier requirements
├── gold-tier.md                      # Gold tier requirements
├── platinum-tier.md                  # Platinum tier requirements
├── implementation-roadmap.md         # Tier-by-tier implementation guide
├── quality-checklist.md              # Comprehensive quality checklist
└── examples/
    └── tier-progression-examples.md  # Real integrations at each tier
```

---

## SKILL.md Content

### Overview Section

```markdown
# Home Assistant Integration Quality Scale

**Description:** Official HA quality framework with Bronze/Silver/Gold/Platinum tier requirements and implementation guidance

**When to use:**
- Planning new integration quality targets
- Improving existing integration quality
- Understanding HA quality requirements
- Determining next quality improvement steps

**Activates on:**
- Prompts containing: "quality", "tier", "bronze", "silver", "gold", "platinum", "quality scale", "requirements"
- Files matching: `manifest.json` (quality tier specified there)

---

## Overview

Home Assistant uses a **4-tier Quality Scale** to classify integration quality:

- **Bronze** 🥉: Baseline quality (minimum for acceptance)
- **Silver** 🥈: Reliability focus (recommended for production)
- **Gold** 🥇: Enhanced UX (premium user experience)
- **Platinum** 🏆: Technical excellence (best-in-class)

**Each tier has specific, measurable requirements** covering:
- Code quality and testing
- Error handling and resilience
- User experience and configuration
- Documentation and maintainability
- Platform capabilities

**Benefits of Higher Tiers:**
- Better visibility in HA UI
- Priority support from HA team
- Featured in integrations list
- User trust and adoption
- Community recognition

**See:** `quality-scale-overview.md` for complete framework

---

## Quality Scale Tiers

### 🥉 Bronze Tier - Baseline Quality

**Purpose:** Minimum quality for core acceptance

**Requirements (12 must-haves):**

1. **Brand assets** - Logo, icon, brand colors
2. **Config flow** - UI-based configuration (no YAML)
3. **Device info** - Proper device grouping
4. **Documentation** - Basic setup guide
5. **Entity naming** - Proper naming conventions
6. **Entry unloading** - Clean unload on disable
7. **Integration quality scale** - Tier documented
8. **Lingering connections** - No leaked connections
9. **Parallel updates** - Concurrent request handling
10. **Reauthentication flow** - Token refresh support
11. **Reconfiguration flow** - Change settings without re-adding
12. **Unique config entry** - Prevent duplicate entries

**Implementation Time:** Part of initial development

**Acceptance:** Required for PR acceptance to HA core

**See:** `bronze-tier.md` for detailed requirements

---

### 🥈 Silver Tier - Reliability

**Purpose:** Production-ready reliability

**Requirements (Bronze + 10 additional):**

13. **Account linking** - OAuth2 or similar
14. **Checks before setup** - Validate before loading
15. **Diagnostics** - Debug data download
16. **Entity descriptions** - Translation keys for entities
17. **Entity unavailable** - Proper availability signaling
18. **Integration owner** - Code owner specified
19. **Raise repair issues** - UI repair notifications
20. **Runtime data** - Proper data storage patterns
21. **Test before configure** - Test config before setup
22. **Test before setup** - Test setup before running

**Additional Focus:**
- Error resilience
- Proper state management
- Diagnostic capabilities
- Test coverage improvements

**Implementation Time:** +40-60 hours beyond Bronze

**See:** `silver-tier.md` for detailed requirements

---

### 🥇 Gold Tier - Enhanced UX

**Purpose:** Premium user experience

**Requirements (Silver + 11 additional):**

23. **Action translations** - Translated action descriptions
24. **Appropriate polling** - Efficient update intervals
25. **Common modules** - Shared library usage
26. **Config entry dynamic options** - Conditional options
27. **Device remove hooks** - Cleanup on device removal
28. **Entity category** - Proper entity categorization
29. **Has entity name** - Entity-specific names
30. **Test coverage** - 95%+ coverage
31. **Translations** - Multi-language support
32. **Treatment of optional config** - Graceful optional handling
33. **Works with `async_get_config_entry_diagnostics`** - Diagnostic data structure

**Additional Focus:**
- User experience optimization
- Translation completeness
- Performance optimization
- Advanced configuration

**Implementation Time:** +60-80 hours beyond Silver

**See:** `gold-tier.md` for detailed requirements

---

### 🏆 Platinum Tier - Technical Excellence

**Purpose:** Best-in-class technical implementation

**Requirements (Gold + additional):**

34+ **Advanced entity features** - All applicable entity features
35+ **Energy management** - Energy dashboard integration
36+ **Multi-hub support** - Multiple device hubs
37+ **Virtual entities** - Helper entity support
38+ **Data privacy** - Local-only options
39+ **Advanced diagnostics** - Comprehensive debug info
40+ **Performance optimization** - Minimal resource usage
41+ **Extensive platform support** - All relevant platforms
42+ **Custom UI cards** - Advanced UI components
43+ **Documentation excellence** - Comprehensive guides

**Additional Focus:**
- Technical innovation
- Performance excellence
- Feature completeness
- Documentation mastery

**Implementation Time:** +80-100 hours beyond Gold

**Few integrations achieve Platinum** - Reserved for exceptional implementations

**See:** `platinum-tier.md` for detailed requirements

---

## Implementation Roadmap

### Phase 1: Bronze Tier Foundation

**Goal:** Achieve minimum acceptance quality

**Steps:**
1. ✅ Implement config flow (UI-based)
2. ✅ Add brand assets (logo, icon)
3. ✅ Set up device info
4. ✅ Create basic documentation
5. ✅ Implement entry unload
6. ✅ Add reauthentication flow
7. ✅ Add reconfiguration flow
8. ✅ Ensure unique config entries
9. ✅ Handle parallel updates
10. ✅ Close all connections on unload
11. ✅ Follow entity naming conventions
12. ✅ Document quality tier in manifest

**Verification:** Run `hassfest` and `python -m script.quality_scale`

**See:** `bronze-tier.md` for implementation details

---

### Phase 2: Silver Tier Reliability

**Goal:** Production-ready reliability

**Prerequisites:** Bronze tier complete

**Steps:**
1. ✅ Add diagnostics support
2. ✅ Implement test-before-configure
3. ✅ Implement test-before-setup
4. ✅ Add entity descriptions
5. ✅ Implement proper entity unavailable
6. ✅ Use runtime_data pattern
7. ✅ Add repair issue support
8. ✅ Specify integration owner
9. ✅ Add account linking (if applicable)
10. ✅ Implement checks before setup

**Verification:** Tier validation passes, all tests pass

**See:** `silver-tier.md` for implementation details

---

### Phase 3: Gold Tier UX

**Goal:** Premium user experience

**Prerequisites:** Silver tier complete

**Steps:**
1. ✅ Achieve 95%+ test coverage
2. ✅ Add full translations
3. ✅ Optimize polling intervals
4. ✅ Add entity categories
5. ✅ Implement has_entity_name
6. ✅ Add dynamic config options
7. ✅ Translate all actions
8. ✅ Add device removal hooks
9. ✅ Handle optional config gracefully
10. ✅ Use common modules
11. ✅ Implement proper diagnostics structure

**Verification:** Quality scale script confirms Gold tier

**See:** `gold-tier.md` for implementation details

---

### Phase 4: Platinum Tier Excellence (Optional)

**Goal:** Best-in-class implementation

**Prerequisites:** Gold tier complete, significant development resources

**Steps:** Custom to integration capabilities

**See:** `platinum-tier.md` for possibilities

---

## Quality Checklist

### Pre-Development Planning

**Tier Selection:**
- [ ] Determine target tier (Bronze minimum)
- [ ] Review tier requirements
- [ ] Plan implementation roadmap
- [ ] Estimate effort for target tier

**Architecture:**
- [ ] Plan for config flow
- [ ] Plan for reauthentication
- [ ] Plan for diagnostics
- [ ] Plan for testing strategy

---

### Bronze Tier Checklist

**Config & Setup:**
- [ ] Config flow implemented (no YAML)
- [ ] Reconfiguration flow implemented
- [ ] Reauthentication flow implemented
- [ ] Unique config entry enforcement
- [ ] Entry unload implemented

**Device & Entities:**
- [ ] Device info properly set
- [ ] Entity naming follows conventions
- [ ] has_entity_name = True

**Quality & Reliability:**
- [ ] No lingering connections on unload
- [ ] Parallel updates handled
- [ ] Quality tier in manifest.json

**Documentation:**
- [ ] Basic setup documentation
- [ ] README with instructions

**Branding:**
- [ ] Logo provided (icon.png)
- [ ] Brand colors defined
- [ ] Icon provided

---

### Silver Tier Checklist

**Testing:**
- [ ] Test-before-configure pattern
- [ ] Test-before-setup pattern
- [ ] Basic test coverage (70%+)

**Diagnostics:**
- [ ] Diagnostics support implemented
- [ ] Debug data includes config entry
- [ ] Debug data includes device info
- [ ] Sensitive data redacted

**Error Handling:**
- [ ] Entity unavailable properly signaled
- [ ] Repair issues raised for problems
- [ ] Checks performed before setup

**Code Quality:**
- [ ] Runtime data pattern used
- [ ] Integration owner specified
- [ ] Code follows HA standards

**Auth:**
- [ ] Account linking (if applicable)
- [ ] OAuth2 flow (if applicable)

---

### Gold Tier Checklist

**Testing:**
- [ ] 95%+ test coverage achieved
- [ ] All platforms tested
- [ ] Error conditions covered

**UX:**
- [ ] Full translations provided
- [ ] Action translations complete
- [ ] Entity categories assigned
- [ ] Dynamic config options (if applicable)

**Performance:**
- [ ] Appropriate polling intervals
- [ ] No unnecessary API calls
- [ ] Efficient data updates

**Architecture:**
- [ ] Common modules used
- [ ] Device removal hooks implemented
- [ ] Optional config handled gracefully
- [ ] Proper diagnostics structure

---

### Platinum Tier Checklist

**Features:**
- [ ] All applicable entity features
- [ ] Energy dashboard integration (if applicable)
- [ ] Multi-hub support (if applicable)
- [ ] Virtual entities (if applicable)

**Excellence:**
- [ ] Performance optimized
- [ ] Comprehensive documentation
- [ ] Advanced diagnostics
- [ ] Custom UI components (if beneficial)

**Innovation:**
- [ ] Unique features for integration type
- [ ] Technical excellence demonstrated
- [ ] Community contribution

---

## Tier Validation

### Automated Validation

**Run quality scale script:**
```bash
python -m script.quality_scale homeassistant/components/YOUR_INTEGRATION
```

**Output shows:**
- Current tier achieved
- Missing requirements for next tier
- Specific issues to fix

**Run before PR submission**

---

### Manual Validation

**Bronze Tier:**
1. Check manifest.json has quality_scale
2. Test config flow end-to-end
3. Test reauthentication
4. Test reconfiguration
5. Test unload (check connections closed)
6. Verify device info appears
7. Verify entity names follow conventions

**Silver Tier:**
1. Run diagnostics download
2. Test repair issue creation
3. Verify entity unavailable works
4. Run test suite
5. Check code owner in CODEOWNERS

**Gold Tier:**
1. Check test coverage ≥ 95%
2. Test in multiple languages
3. Verify entity categories
4. Test dynamic options
5. Verify polling intervals reasonable

---

## Common Issues

### Issue 1: Can't Achieve Target Tier

**Symptom:** Quality scale script shows lower tier than expected

**Cause:** Missing specific requirements

**Solution:**
1. Run: `python -m script.quality_scale homeassistant/components/YOUR_INTEGRATION`
2. Read missing requirements
3. Implement one requirement at a time
4. Re-run validation after each fix
5. Check `quality-checklist.md` for guidance

---

### Issue 2: Bronze Tier Blocked

**Symptom:** Can't get past Bronze despite implementing features

**Cause:** Usually missing config flow, device info, or has_entity_name

**Solution:**
- Ensure config flow is complete (no YAML)
- Set device_info on all entities
- Set has_entity_name = True
- Check manifest.json has quality_scale field

---

### Issue 3: Silver Tier Diagnostics Required

**Symptom:** Stuck at Bronze, need diagnostics for Silver

**Solution:**
```python
# Add to __init__.py
async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "entry": entry.as_dict(),
        "data": hass.data[DOMAIN][entry.entry_id].data,
        # Add other debug info
    }
```

**See:** `silver-tier.md` for complete pattern

---

### Issue 4: Gold Tier Coverage Requirements

**Symptom:** Stuck at Silver, need 95%+ coverage

**Cause:** Test coverage below 95%

**Solution:**
1. Run: `pytest --cov=custom_components.DOMAIN --cov-report=html`
2. Open htmlcov/index.html
3. Add tests for uncovered lines
4. Focus on error conditions and edge cases
5. Achieve ≥95% coverage

**See:** ha-testing-patterns Skill for test templates

---

## Examples

### Example 1: MQTT Integration (Platinum Tier) 🏆

**Path:** `homeassistant/components/mqtt/`

**Tier:** Platinum

**Key Achievements:**
- Complete feature set
- 98% test coverage
- Comprehensive diagnostics
- Multi-protocol support
- Advanced configuration
- Excellent documentation

**Progression:** Bronze → Silver (3 months) → Gold (6 months) → Platinum (12 months)

---

### Example 2: Shelly Integration (Gold Tier) 🥇

**Path:** `homeassistant/components/shelly/`

**Tier:** Gold

**Key Achievements:**
- 96% test coverage
- Full translations
- Proper entity categories
- Efficient polling
- Device removal hooks
- Diagnostics support

**Progression:** Bronze → Silver (2 months) → Gold (4 months)

---

### Example 3: Template Integration (Silver Tier) 🥈

**Path:** `homeassistant/components/template/`

**Tier:** Silver

**Key Achievements:**
- Reliable operation
- Good test coverage (85%)
- Diagnostics support
- Proper error handling
- Test patterns implemented

**Progression:** Bronze → Silver (6 weeks)

---

## Related Skills

- **ha-testing-patterns**: Required for achieving Gold tier (95%+ coverage) - use together when implementing tests
- **ha-config-flow-knowledge**: Required for Bronze tier (config flow) - foundational for any tier
- **ha-entity-knowledge**: Required for Bronze tier (entity naming, device info) - use throughout
- **ha-integration-structure**: Required for Bronze tier (manifest.json) - initial setup
- **ha-coordinator-knowledge**: Helpful for Silver tier (runtime data) - improves reliability

---

## Implementation Timeline

**Bronze Tier:**
- Included in initial development
- ~40-60 hours total development
- Required for PR acceptance

**Bronze → Silver:**
- +40-60 hours
- Focus: reliability and diagnostics
- 4-8 weeks additional work

**Silver → Gold:**
- +60-80 hours
- Focus: UX and testing
- 8-12 weeks additional work

**Gold → Platinum:**
- +80-100+ hours
- Focus: excellence and innovation
- 12-16+ weeks additional work
- Few integrations achieve this

**Total Bronze → Gold:** 140-200 hours (~4-6 months part-time)

---

## References

- [HA Integration Quality Scale](https://developers.home-assistant.io/docs/integration_quality_scale_index)
- [Quality Scale Rules](https://developers.home-assistant.io/docs/integration_quality_scale_rules)
- Quality Scale Script: `python -m script.quality_scale`
- Research Document: Lines 116-141, 547-562 (quality scale requirements)

---

**Last Updated:** 2025-11-21
**Version:** 1.0
**Priority:** CRITICAL
