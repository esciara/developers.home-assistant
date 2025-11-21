# Comprehensive Testing Plan for `skill-auto-activation-setup`

This document outlines a structured plan to verify the skill works correctly at every level.

---

## **Phase 1: Skill Discovery & Activation Tests**

### Test 1.1: Skill is Discoverable
**Objective**: Verify Claude can find and list the skill

**Steps**:
```bash
# In a new Claude session
Ask: "What skills are available?"
```

**Expected Result**:
- `skill-auto-activation-setup` appears in the list
- Description matches the frontmatter

**Proves**: Skill is properly registered in `.claude/skills/` and has valid YAML frontmatter

---

### Test 1.2: Skill Auto-Activates on Trigger Keywords
**Objective**: Verify the skill activates based on description triggers

**Steps**:
```bash
# Test each trigger keyword from description:
1. "Skills don't activate automatically"
2. "Help me set up skill triggers"
3. "How do I configure skill-rules.json?"
4. "Set up skill auto-activation hooks"
```

**Expected Result**:
- Claude should either:
  - Automatically invoke the skill (ideal), OR
  - Mention the skill is relevant and offer to use it

**Proves**: The description field contains effective trigger words for discovery

---

## **Phase 2: Content Validation Tests**

### Test 2.1: Template Files Exist and Are Valid
**Objective**: Verify all referenced template files are present and syntactically correct

**Steps**:
```bash
ls -la .claude/skills/skill-auto-activation-setup/
cat .claude/skills/skill-auto-activation-setup/hook-template.sh
cat .claude/skills/skill-auto-activation-setup/hook-handler-template.ts
cat .claude/skills/skill-auto-activation-setup/skill-rules-template.json
```

**Expected Result**:
- All 5 files exist: SKILL.md, README.md, hook-template.sh, hook-handler-template.ts, skill-rules-template.json
- hook-template.sh has valid bash syntax
- hook-handler-template.ts has valid TypeScript syntax
- skill-rules-template.json has valid JSON

**Validation Commands**:
```bash
# Check bash syntax
bash -n .claude/skills/skill-auto-activation-setup/hook-template.sh

# Check JSON syntax
jq . .claude/skills/skill-auto-activation-setup/skill-rules-template.json

# Check TypeScript syntax (if npx available)
npx tsc --noEmit .claude/skills/skill-auto-activation-setup/hook-handler-template.ts
```

**Proves**: Template files are well-formed and won't cause syntax errors

---

### Test 2.2: Instructions Are Complete
**Objective**: Verify the skill provides actionable setup instructions

**Steps**:
```bash
# Read the skill and verify it covers:
1. grep "Setup Instructions" .claude/skills/skill-auto-activation-setup/SKILL.md
2. grep "Hook Script" .claude/skills/skill-auto-activation-setup/SKILL.md
3. grep "TypeScript Handler" .claude/skills/skill-auto-activation-setup/SKILL.md
4. grep "skill-rules.json" .claude/skills/skill-auto-activation-setup/SKILL.md
5. grep "Troubleshooting" .claude/skills/skill-auto-activation-setup/SKILL.md
```

**Expected Result**:
- All key sections exist
- Instructions are step-by-step
- Examples are provided

**Proves**: The skill provides comprehensive guidance

---

## **Phase 3: Functional Hook Tests**

### Test 3.1: Hook Script Executes Without Errors
**Objective**: Test the hook script can run in isolation

**Steps**:
```bash
# Copy templates to actual hook location
mkdir -p .claude/hooks
cp .claude/skills/skill-auto-activation-setup/hook-template.sh .claude/hooks/skill-activation-prompt.sh
cp .claude/skills/skill-auto-activation-setup/hook-handler-template.ts .claude/hooks/skill-activation-prompt.ts
chmod +x .claude/hooks/skill-activation-prompt.sh

# Test with mock input
echo '{"session_id":"test","transcript_path":"","cwd":"","permission_mode":"auto","prompt":"write a python function"}' | .claude/hooks/skill-activation-prompt.sh
```

**Expected Result**:
- Script executes without errors
- Exits with code 0 (graceful exit when skill-rules.json doesn't exist)

**Proves**: Hook script is executable and handles missing config gracefully

---

### Test 3.2: Hook Handler Analyzes Prompts Correctly
**Objective**: Verify the TypeScript handler matches keywords and patterns

**Steps**:
```bash
# Create a test skill-rules.json in .claude/skills/
cp .claude/skills/skill-auto-activation-setup/skill-rules-template.json .claude/skills/skill-rules.json

# Test with matching prompt
echo '{"session_id":"test","transcript_path":"","cwd":"","permission_mode":"auto","prompt":"write a python function"}' | .claude/hooks/skill-activation-prompt.sh

# Test with non-matching prompt
echo '{"session_id":"test","transcript_path":"","cwd":"","permission_mode":"auto","prompt":"hello world"}' | .claude/hooks/skill-activation-prompt.sh
```

**Expected Result**:
- Matching prompt: Outputs skill suggestion box with "python-development"
- Non-matching prompt: No output (silent success)

**Proves**: Pattern matching logic works correctly (keyword and regex matching)

---

### Test 3.3: Priority Levels Display Correctly
**Objective**: Verify skills are categorized by priority

**Steps**:
```bash
# Modify skill-rules.json to have different priority levels
# Test with prompts that trigger each level
echo '{"session_id":"test","transcript_path":"","cwd":"","permission_mode":"auto","prompt":"python mypy"}' | .claude/hooks/skill-activation-prompt.sh
```

**Expected Result**:
- Output shows priority sections: "⚠️ CRITICAL SKILLS", "📚 RECOMMENDED SKILLS", etc.
- Skills appear under correct priority level

**Proves**: Priority categorization works

---

## **Phase 4: End-to-End Integration Tests**

### Test 4.1: Full Setup Workflow
**Objective**: Walk through complete setup as a new user would

**Steps**:
```bash
# Start fresh (in a test branch or separate directory)
1. Ask Claude: "Help me set up skill auto-activation"
2. Follow Claude's instructions using the skill
3. Verify Claude copies template files to correct locations
4. Verify Claude makes hook script executable
5. Create a simple skill-rules.json
6. Test with a prompt that should trigger a skill
```

**Expected Result**:
- Claude provides step-by-step guidance
- All files are created in correct locations
- Permissions are set correctly
- Test prompt triggers skill suggestion

**Proves**: The entire workflow works from a user's perspective

---

### Test 4.2: Hook Integration with Claude Code
**Objective**: Verify hooks actually run in Claude Code environment

**Steps**:
```bash
# This requires Claude Code settings configuration
# Check if hook is registered (method varies by CLI vs Web)

# For testing, manually verify:
1. Submit a prompt: "write a python function"
2. Observe if skill activation message appears BEFORE Claude responds
3. Verify the suggested skill matches the prompt
```

**Expected Result**:
- Hook runs on every prompt submission
- Skill suggestions appear before Claude's response
- No errors in Claude Code output

**Proves**: Hooks integrate correctly with Claude Code's UserPromptSubmit system

---

## **Phase 5: Edge Cases & Error Handling Tests**

### Test 5.1: Missing skill-rules.json
**Objective**: Verify graceful handling when config is missing

**Steps**:
```bash
# Remove skill-rules.json
rm .claude/skills/skill-rules.json

# Run hook
echo '{"session_id":"test","transcript_path":"","cwd":"","permission_mode":"auto","prompt":"test"}' | .claude/hooks/skill-activation-prompt.sh
```

**Expected Result**:
- No error messages
- Exits with code 0
- No output (silent success)

**Proves**: Hook doesn't break Claude Code when not configured

---

### Test 5.2: Invalid JSON in skill-rules.json
**Objective**: Verify error handling for malformed config

**Steps**:
```bash
# Create invalid JSON
echo '{"invalid json' > .claude/skills/skill-rules.json

# Run hook
echo '{"session_id":"test","transcript_path":"","cwd":"","permission_mode":"auto","prompt":"test"}' | .claude/hooks/skill-activation-prompt.sh 2>&1
```

**Expected Result**:
- Error message to stderr
- Exits with non-zero code (expected failure)
- Claude Code should handle hook failures gracefully

**Proves**: Errors are reported appropriately

---

### Test 5.3: Special Characters in Prompts
**Objective**: Verify regex patterns handle edge cases

**Steps**:
```bash
# Test with special characters
echo '{"session_id":"test","transcript_path":"","cwd":"","permission_mode":"auto","prompt":"write a python function with $variables and @decorators"}' | .claude/hooks/skill-activation-prompt.sh
```

**Expected Result**:
- No regex errors
- Pattern matching still works
- Appropriate skills suggested

**Proves**: Regex patterns are robust

---

## **Phase 6: Performance & UX Tests**

### Test 6.1: Hook Execution Time
**Objective**: Ensure hooks don't slow down Claude's responses

**Steps**:
```bash
# Time the hook execution
time echo '{"session_id":"test","transcript_path":"","cwd":"","permission_mode":"auto","prompt":"write a python function"}' | .claude/hooks/skill-activation-prompt.sh
```

**Expected Result**:
- Execution time < 200ms
- No noticeable delay in Claude Code

**Proves**: Hook is performant enough for real-time use

---

### Test 6.2: Output Formatting
**Objective**: Verify suggestions are readable and well-formatted

**Steps**:
```bash
# Run hook and check output format
echo '{"session_id":"test","transcript_path":"","cwd":"","permission_mode":"auto","prompt":"python mypy"}' | .claude/hooks/skill-activation-prompt.sh
```

**Expected Result**:
- Clear visual separators (━━━━)
- Proper emoji usage (🎯, 📚, etc.)
- Readable hierarchy
- Clear action items

**Proves**: UX is polished and professional

---

## **Summary: What This Proves**

| Test Phase | What It Proves |
|------------|----------------|
| **Phase 1** | Skill is properly configured and discoverable by Claude |
| **Phase 2** | All documentation and templates are complete and valid |
| **Phase 3** | Hook logic correctly matches prompts to skills |
| **Phase 4** | Full workflow works end-to-end as designed |
| **Phase 5** | Error handling is robust and won't break Claude Code |
| **Phase 6** | Performance and UX meet quality standards |

---

## **Quick Validation Script**

An automated test script can be created that runs most of these tests:

1. Checks all template files exist and are valid
2. Tests hook execution with various inputs
3. Validates JSON/TypeScript/Bash syntax
4. Runs performance benchmarks
5. Generates a test report

This would make it easy to verify the skill works correctly with a single command.
