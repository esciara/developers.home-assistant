# Hook-Based Activation System

**Last Updated:** 2025-11-21
**Status:** Critical Component - Must implement before Skills

---

## Problem Statement

**Claude Code Skills' built-in auto-activation doesn't work reliably.**

Skills are supposed to auto-activate based on their SKILL.md descriptions. In practice:
- ❌ Skills often "just sit there" waiting to be manually invoked
- ❌ Auto-activation dependent on Claude's description parsing (unreliable)
- ❌ No file-based triggering (only prompt-based)
- ❌ Defeats the purpose of automatic knowledge activation

**Result:** Skills become documentation that developers must manually remember to reference.

---

## Solution: Hook-Based Activation

Implement a proven hook-based system that analyzes prompts and file context to automatically suggest and activate relevant Skills.

**Reference Implementation:** [claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase/blob/main/README.md)

**Key Insight:** Use Claude Code's hook system to detect when Skills should activate, rather than relying on Claude's built-in auto-triggering.

---

## Core Components

### 1. UserPromptSubmit Hook

**File:** `skill-activation-prompt.*` (script name from reference implementation)

**Purpose:** Runs on every user prompt to determine which Skills should activate

**How It Works:**
1. User submits a prompt (e.g., "How do I create a sensor?")
2. Hook script intercepts the prompt
3. Script reads `skill-rules.json` configuration
4. Script checks prompt against trigger patterns
5. Script checks currently open/edited files against file patterns
6. Script automatically suggests relevant Skills to Claude
7. Claude loads Skills and has them in context

**Trigger Methods:**
- **Keyword matching:** Prompt contains words like "entity", "sensor", "unique id"
- **File context:** User is editing files like `sensor.py`, `manifest.json`
- **Combined:** Both prompt AND file match (highest confidence)

**Example:**
```bash
# User prompt: "How do I create a sensor entity?"
# Hook detects: "sensor", "entity"
# Hook suggests: ha-entity-knowledge Skill
# Result: Claude has entity patterns in context
```

### 2. PostToolUse Hook

**File:** `post-tool-use-tracker.sh` (script name from reference implementation)

**Purpose:** Tracks which tools are used during session

**How It Works:**
1. Monitors tools Claude uses (Read, Write, Edit, etc.)
2. Maintains context about active Skills
3. Enables progressive Skill engagement
4. Helps hooks understand session context

**Use Case:**
- If Claude reads `sensor.py`, hook knows entity context is relevant
- If Claude writes to `config_flow.py`, hook knows config flow context matters
- Progressive activation as work evolves

### 3. Configuration File

**File:** `skill-rules.json` (location: root or `.claude/` directory)

**Purpose:** Defines trigger patterns for each Skill without modifying hook scripts

**Format:**
```json
{
  "skill-name": {
    "prompt_patterns": ["keyword1", "keyword2", "phrase"],
    "file_patterns": ["**/path/pattern/*.py", "specific-file.json"],
    "contexts": ["context description"]
  }
}
```

**Benefits:**
- Declarative configuration (no code changes)
- Easy to tune trigger sensitivity
- Can be version controlled
- Team can contribute patterns

---

## Implementation Details

### skill-rules.json Structure

**Full example for HA integration development:**

```json
{
  "ha-entity-knowledge": {
    "prompt_patterns": [
      "entity",
      "sensor",
      "switch",
      "climate",
      "light",
      "binary sensor",
      "unique id",
      "unique_id",
      "device info",
      "device_info",
      "entity state",
      "entity attribute"
    ],
    "file_patterns": [
      "**/homeassistant/components/**/sensor.py",
      "**/homeassistant/components/**/switch.py",
      "**/homeassistant/components/**/climate.py",
      "**/homeassistant/components/**/light.py",
      "**/homeassistant/components/**/binary_sensor.py",
      "**/homeassistant/components/**/*_entity.py"
    ],
    "contexts": [
      "entity implementation",
      "platform development",
      "device integration"
    ]
  },

  "ha-integration-structure": {
    "prompt_patterns": [
      "manifest",
      "integration structure",
      "required files",
      "__init__.py",
      "manifest.json",
      "integration setup",
      "what files"
    ],
    "file_patterns": [
      "**/homeassistant/components/**/manifest.json",
      "**/homeassistant/components/**/__init__.py"
    ],
    "contexts": [
      "integration setup",
      "file organization",
      "new integration"
    ]
  },

  "ha-config-flow-knowledge": {
    "prompt_patterns": [
      "config flow",
      "config_flow",
      "configuration",
      "setup wizard",
      "user input",
      "config entry",
      "options flow"
    ],
    "file_patterns": [
      "**/homeassistant/components/**/config_flow.py"
    ],
    "contexts": [
      "configuration flow",
      "user setup",
      "integration configuration"
    ]
  },

  "ha-coordinator-knowledge": {
    "prompt_patterns": [
      "coordinator",
      "DataUpdateCoordinator",
      "update coordinator",
      "polling",
      "data update",
      "refresh data"
    ],
    "file_patterns": [
      "**/homeassistant/components/**/coordinator.py",
      "**/homeassistant/components/**/__init__.py"
    ],
    "contexts": [
      "data polling",
      "coordinator pattern",
      "data refresh"
    ]
  },

  "ha-common-mistakes": {
    "prompt_patterns": [
      "error",
      "issue",
      "problem",
      "not working",
      "best practice",
      "avoid",
      "anti-pattern"
    ],
    "file_patterns": [
      "**/homeassistant/components/**/*.py"
    ],
    "contexts": [
      "debugging",
      "troubleshooting",
      "code review"
    ]
  }
}
```

### Pattern Matching Rules

**Prompt Patterns:**
- Case-insensitive matching
- Substring matching (pattern can appear anywhere in prompt)
- Multiple patterns = OR logic (any match triggers)
- Phrase matching for multi-word patterns

**File Patterns:**
- Glob pattern matching (e.g., `**/*.py`)
- Matches against currently open/edited files
- Multiple patterns = OR logic
- Can be specific (`config_flow.py`) or broad (`**/*.py`)

**Contexts:**
- Descriptive strings for documentation
- May be used by hooks for logging/debugging
- Help team understand when Skill should activate

---

## Setup Process

### Step 1: Install Hook Scripts (~30 min)

**From reference implementation:**

1. Clone reference repo:
```bash
git clone https://github.com/diet103/claude-code-infrastructure-showcase.git
cd claude-code-infrastructure-showcase
```

2. Copy hook scripts to your project:
```bash
# Exact file names and locations from reference implementation
cp hooks/skill-activation-prompt.* /path/to/your/project/.claude/hooks/
cp hooks/post-tool-use-tracker.sh /path/to/your/project/.claude/hooks/
```

3. Make hooks executable:
```bash
chmod +x .claude/hooks/skill-activation-prompt.*
chmod +x .claude/hooks/post-tool-use-tracker.sh
```

4. Configure Claude Code to use hooks:
```bash
# May require .claude/settings.json configuration
# Check reference implementation for exact settings
```

**Note:** Exact installation steps depend on reference implementation details. See their README for authoritative instructions.

### Step 2: Create skill-rules.json (~15 min)

1. Create file at project root or `.claude/` directory:
```bash
touch skill-rules.json
# OR
touch .claude/skill-rules.json
```

2. Start with basic configuration:
```json
{
  "ha-entity-knowledge": {
    "prompt_patterns": ["entity", "sensor", "unique id"],
    "file_patterns": ["**/components/**/sensor.py"],
    "contexts": ["entity implementation"]
  }
}
```

3. Test basic activation (see Testing section below)

4. Expand to all Skills as you create them

### Step 3: Test Hook Activation (~15 min)

**Test prompt-based activation:**
1. Type: "How do I create a sensor entity?"
2. Expected: Hook suggests `ha-entity-knowledge` Skill
3. Verify: Use `/context` command to see loaded Skills

**Test file-based activation:**
1. Open/edit a file: `homeassistant/components/mqtt/sensor.py`
2. Expected: Hook suggests `ha-entity-knowledge` Skill
3. Verify: Use `/context` to see loaded Skills

**Test combined activation:**
1. Open `sensor.py` AND type "unique id"
2. Expected: High-confidence activation of `ha-entity-knowledge`
3. Verify: Skill appears in context

### Step 4: Tune Patterns (ongoing)

As you use the system:
1. Notice when Skills **should** activate but don't → Add missing patterns
2. Notice when Skills activate **incorrectly** → Remove over-broad patterns
3. Refine file patterns based on actual file paths in your project
4. Document patterns that work well

---

## Testing Skill Activation

### Manual Testing Checklist

After implementing hooks, test each Skill:

**ha-entity-knowledge:**
- [ ] Type "How do I create a sensor?" → activates
- [ ] Open `sensor.py` file → activates
- [ ] Type "unique id strategy" → activates
- [ ] Open `switch.py` file → activates
- [ ] Use `/context` → verify Skill loaded

**ha-integration-structure:**
- [ ] Type "What files does an integration need?" → activates
- [ ] Open `manifest.json` → activates
- [ ] Type "integration structure" → activates
- [ ] Open `__init__.py` in components dir → activates

**ha-config-flow-knowledge:**
- [ ] Type "How do I create a config flow?" → activates
- [ ] Open `config_flow.py` → activates
- [ ] Type "user input validation" → activates

**ha-coordinator-knowledge:**
- [ ] Type "How do I use DataUpdateCoordinator?" → activates
- [ ] Open file with "coordinator" in path → activates
- [ ] Type "polling interval" → activates

**ha-common-mistakes:**
- [ ] Type "common mistakes" → activates
- [ ] Type "best practices" → activates
- [ ] Type "what should I avoid" → activates

### Automated Testing (Optional)

Create test scripts:
```bash
# test-hook-activation.sh
echo "Testing prompt patterns..."
# Simulate prompts and check hook responses
# (Implementation depends on hook script details)
```

---

## Benefits of Hook-Based Approach

### Reliability ✅
- **Works consistently:** Not dependent on Claude's description parsing
- **Transparent:** Works automatically without user remembering to invoke
- **Predictable:** Clear rules for when Skills activate

### Context-Awareness ✅
- **File-based triggering:** Activates when editing relevant files (not just prompts)
- **Combined signals:** High confidence when prompt + file both match
- **Progressive engagement:** Skills load as work evolves

### Configurability ✅
- **Easy to tune:** Modify `skill-rules.json` without changing hooks
- **Team contribution:** Anyone can add patterns
- **Version controlled:** Patterns evolve with codebase

### Efficiency ✅
- **Progressive loading:** Main Skill loads first, details on-demand
- **Selective activation:** Only relevant Skills load
- **Context optimization:** ~60-70% reduction vs manual loading

### Fast Setup ✅
- **~15 minutes:** Basic system functional
- **~1-2 hours:** Complete setup with all Skills
- **Proven system:** Reference implementation already works

---

## Troubleshooting

### Skills Not Activating

**Check:**
1. Hooks installed correctly: `ls -la .claude/hooks/`
2. Hooks executable: `chmod +x .claude/hooks/*`
3. `skill-rules.json` exists and is valid JSON
4. Patterns match your actual prompts/files
5. Hook scripts have correct permissions

**Debug:**
```bash
# Check hook script logs (if available)
# Verify skill-rules.json syntax
cat skill-rules.json | jq .
```

### False Positives (Skills activating incorrectly)

**Solutions:**
1. Make patterns more specific
2. Remove overly broad patterns (e.g., "error")
3. Use longer phrase patterns instead of single words
4. Tighten file patterns to specific paths

### False Negatives (Skills not activating when they should)

**Solutions:**
1. Add missing keywords to `prompt_patterns`
2. Broaden file patterns to catch more files
3. Check for typos in patterns
4. Consider case sensitivity

---

## Per-Skill Configuration Workflow

When creating each Skill:

**1. Create Skill Structure** (from template)
- SKILL.md with description and instructions
- Supporting documentation
- Templates

**2. Define Trigger Patterns** (in skill-rules.json)
```json
"new-skill-name": {
  "prompt_patterns": ["keyword1", "keyword2"],
  "file_patterns": ["**/relevant/**/*.py"],
  "contexts": ["when to use this skill"]
}
```

**3. Test Activation** (manual testing)
- Test prompt-based triggers
- Test file-based triggers
- Verify with `/context`

**4. Refine Patterns** (based on testing)
- Add missing keywords
- Remove false positives
- Tune file patterns

**5. Document** (in Skill's README)
- Document trigger patterns
- Explain when Skill activates
- Provide examples

**Time per Skill:** ~15-30 minutes for activation configuration

---

## Maintenance

### Regular Pattern Review

**Monthly:**
- Review activation logs (if available)
- Identify patterns that trigger too often/rarely
- Update `skill-rules.json` based on usage

**When HA API Changes:**
- Update patterns for new file names
- Add patterns for new concepts
- Remove patterns for deprecated features

**When Skills Change:**
- Update patterns to reflect new Skill scope
- Add patterns for new templates/patterns
- Document pattern changes in commit messages

### Team Collaboration

**Pattern Contribution:**
1. Team member discovers useful trigger pattern
2. Add to `skill-rules.json`
3. Test activation
4. Commit with description
5. Share with team via git

**Pattern Review:**
- Include `skill-rules.json` changes in code reviews
- Test patterns before merging
- Document why patterns were added/removed

---

## Comparison: Built-in vs Hook-Based Activation

| Aspect | Built-in Auto-Trigger | Hook-Based Activation |
|--------|----------------------|---------------------|
| **Reliability** | ❌ Unreliable | ✅ Consistent |
| **File-based** | ❌ No | ✅ Yes |
| **Prompt-based** | ⚠️ Sometimes | ✅ Always |
| **Configurable** | ❌ No (description only) | ✅ Yes (skill-rules.json) |
| **Transparent** | ❌ Black box | ✅ Clear rules |
| **Setup time** | ✅ 0 min | ⚠️ ~1-2 hours |
| **Maintenance** | ✅ None needed | ⚠️ Pattern tuning |
| **Team control** | ❌ Limited | ✅ Full control |

**Conclusion:** Hook-based activation requires upfront setup but provides reliable, controllable Skill activation.

---

## Next Steps

1. **Install hooks:** Follow Step 1-3 in Setup Process
2. **Create basic config:** Start with one Skill's patterns
3. **Test activation:** Verify hooks work before scaling
4. **Build first Skill:** Create Skill with hook triggers
5. **Expand:** Add patterns for each new Skill

**Critical:** Do NOT create multiple Skills until you verify hooks work for at least one Skill.

---

**See Also:**
- [System Architecture Overview](overview.md)
- [Phase 1: Skills Foundation](../phases/phase-1-skills.md) - Implementation guide
- [Hook Activation Testing](../testing/hook-activation-tests.md) - Detailed testing procedures
- [skill-rules.json Examples](../examples/skill-rules-examples.json) - Example configurations
- [Back to Main README](../README.md)
