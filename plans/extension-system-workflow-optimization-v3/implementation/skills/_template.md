# Skill Creation Template

**Use this template when creating new Skills**

---

## Skill Directory Structure

```
.claude/skills/[skill-name]/
├── SKILL.md                    # Main Skill definition (this file)
├── [supporting-doc-1].md       # Pattern explanations
├── [supporting-doc-2].md       # Detailed guides
├── [supporting-doc-3].md       # Reference material
├── templates/                  # Code templates directory
│   ├── [template-1].py
│   ├── [template-2].py
│   └── [template-3].py
└── examples/                   # Example references (optional)
    └── examples.md
```

---

## SKILL.md Template

```markdown
# [Skill Name]

**Description:** [One-sentence description of what this Skill provides]

**When to use:** [Scenarios where this Skill is relevant]

**Activates on:**
- Prompts containing: [keywords]
- Files matching: [patterns]

---

## Overview

[2-3 paragraph overview of the Skill's purpose and scope]

**Key Capabilities:**
- [Capability 1]
- [Capability 2]
- [Capability 3]

---

## Patterns

### [Pattern Category 1]

**Pattern Name:** [Name]

**When to use:** [Scenarios]

**Implementation:**
[Code example or detailed explanation]

**Examples:**
- [Real integration example]

**See:** [reference to supporting doc or template]

### [Pattern Category 2]

[Repeat for each major pattern]

---

## Templates

### Template 1: [Name]

**Purpose:** [What this template provides]

**Use case:** [When to use this template]

**File:** `templates/[filename].py`

**Usage:**
1. Copy template
2. Replace [placeholders]
3. Customize for your use case

**Key sections to modify:**
- [Section 1]: [what to change]
- [Section 2]: [what to change]

### Template 2: [Name]

[Repeat for each template]

---

## Checklists

### [Use Case 1] Checklist

- [ ] [Step 1]
- [ ] [Step 2]
- [ ] [Step 3]
- [ ] [Step 4]

### [Use Case 2] Checklist

[Repeat for common use cases]

---

## Examples

### Example 1: [Integration Name]

**Path:** `[file path]`

**Pattern used:** [Which pattern from this Skill]

**Key implementation notes:**
- [Note 1]
- [Note 2]

**See:** [link to code if external]

### Example 2: [Integration Name]

[Repeat for 2-3 examples]

---

## Common Issues

### Issue 1: [Problem description]

**Symptom:** [How it manifests]

**Cause:** [Why it happens]

**Solution:** [How to fix]

**See:** [Reference to pattern or template]

### Issue 2: [Problem description]

[Repeat for common issues]

---

## Related Skills

- **[Related Skill 1]**: [How it relates, when to use together]
- **[Related Skill 2]**: [How it relates, when to use together]

---

## References

- [External documentation link]
- [HA developer docs link]
- [Supporting doc in this Skill]

---

**Last Updated:** [Date]
**Version:** [Version number]
```

---

## skill-rules.json Entry Template

Add to `skill-rules.json`:

```json
{
  "[skill-name]": {
    "prompt_patterns": [
      "keyword1",
      "keyword2",
      "multi word phrase",
      "related_term",
      "synonym"
    ],
    "file_patterns": [
      "**/path/to/relevant/*.py",
      "**/specific-file.json",
      "**/*pattern*.py"
    ],
    "contexts": [
      "context description 1",
      "context description 2"
    ]
  }
}
```

**Prompt Patterns:**
- Include variations (snake_case, "spaced phrase")
- Include synonyms
- Include common misspellings (if appropriate)
- Start with most specific, add broader patterns as needed

**File Patterns:**
- Use glob patterns (`**` for any directory depth)
- Include all relevant file types
- Be specific enough to avoid false positives
- Test patterns match actual file paths

**Contexts:**
- Descriptive strings for documentation
- Help team understand when Skill activates
- Used for logging/debugging

---

## Code Template Structure

**File:** `templates/[template-name].py`

```python
"""
[Template Name]

Purpose: [What this template provides]
Use case: [When to use]

Instructions:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Placeholders to replace:
- [PLACEHOLDER1]: [Description]
- [PLACEHOLDER2]: [Description]
"""

from homeassistant.[relevant imports] import [classes]

# Template code here with [PLACEHOLDERS] and inline comments

class [CLASSNAME]:
    """[Docstring]."""

    def __init__(self, [PARAM1], [PARAM2]):
        """Initialize."""
        # Implementation with helpful comments

    def [method_name](self):
        """[Method description]."""
        # Implementation
        # Comments explaining key sections
```

**Template Requirements:**
- Must compile without errors (except placeholders)
- Must follow HA coding standards
- Must include helpful inline comments
- Must have clear placeholder naming
- Must include docstrings

---

## Supporting Document Structure

**File:** `[topic].md`

```markdown
# [Topic Name]

**Part of:** [Skill Name] Skill

---

## Overview

[Explanation of this topic]

---

## [Subtopic 1]

[Detailed explanation with code examples]

---

## [Subtopic 2]

[Detailed explanation with code examples]

---

## Best Practices

- [Practice 1]
- [Practice 2]
- [Practice 3]

---

## Common Mistakes

- [Mistake 1]: [How to avoid]
- [Mistake 2]: [How to avoid]

---

## Examples

[References to real code]

---

## See Also

- [Related section in SKILL.md]
- [Related supporting doc]
- [External reference]
```

---

## Testing Your Skill

### Activation Testing

1. **Test prompt patterns:**
   ```
   Type: "[prompt with keyword]"
   Expected: Skill activates
   Verify: Use /context command
   ```

2. **Test file patterns:**
   ```
   Open: [file matching pattern]
   Expected: Skill activates
   Verify: Use /context command
   ```

3. **Test combined:**
   ```
   Open: [file] AND type: "[prompt]"
   Expected: High-confidence activation
   ```

### Template Testing

1. Copy template to test location
2. Replace placeholders
3. Run syntax check (compile)
4. Verify follows HA patterns
5. Test in actual integration (if possible)

### Pattern Testing

1. Verify patterns are accurate
2. Check examples actually use patterns
3. Test recommendations work in practice

---

## Checklist for Skill Completion

**Structure:**
- [ ] Skill directory created
- [ ] SKILL.md created
- [ ] 3-5 supporting docs created
- [ ] templates/ directory with 2-3 templates
- [ ] examples/ directory or examples section

**Content Quality:**
- [ ] SKILL.md is clear and complete
- [ ] Patterns are accurate and current
- [ ] Templates compile without errors
- [ ] Templates follow HA patterns
- [ ] Examples reference real, current integrations
- [ ] Checklists cover common scenarios

**Activation:**
- [ ] skill-rules.json entry created
- [ ] Prompt patterns tested
- [ ] File patterns tested
- [ ] No false positives observed
- [ ] No false negatives observed

**Documentation:**
- [ ] SKILL.md documents all sections
- [ ] Supporting docs are comprehensive
- [ ] Templates include usage instructions
- [ ] Examples include notes and context
- [ ] Related Skills documented

**Testing:**
- [ ] Skill activates on expected prompts
- [ ] Skill activates on expected files
- [ ] Templates validated
- [ ] Patterns tested
- [ ] No conflicts with other Skills

---

## Tips for Success

**Start Simple:**
- Begin with core patterns
- Add detail incrementally
- Expand based on usage

**Test Early:**
- Test activation before adding all content
- Validate templates before documenting
- Get feedback on patterns quickly

**Use Real Examples:**
- Reference actual integrations
- Test patterns against real code
- Base templates on working code

**Document as You Go:**
- Write docs while creating patterns
- Capture rationale immediately
- Note edge cases as discovered

**Iterate:**
- Refine patterns based on testing
- Update templates based on usage
- Enhance docs based on questions

---

**See Also:**
- [Phase 1: Skills Foundation](../../phases/phase-1-skills.md)
- [Hook Activation Testing](../../testing/hook-activation-tests.md)
- [Skill Validation Testing](../../testing/skill-validation-tests.md)
