---
name: skill-auto-activation-setup
description: Set up hook-based auto-activation for Claude Code skills using UserPromptSubmit hooks. Use when skills don't activate automatically, when setting up skill triggers, or when configuring skill-rules.json and hook files for automatic skill suggestions.
---

# Skill Auto-Activation Setup

Set up automatic skill activation using hooks that analyze prompts and suggest relevant skills before Claude responds.

## Problem

By default, Claude Code skills are model-invoked—you must ask questions that match the skill description. This skill provides a hook-based system that proactively suggests skills based on:
- Keyword matching in prompts
- Intent pattern matching (regex)
- File context (paths, content patterns)

## Quick Start

### Step 1: Create hooks directory

```bash
mkdir -p .claude/hooks
```

### Step 2: Copy hook files from templates

```bash
cp .claude/skills/skill-auto-activation-setup/templates/hook-template.sh .claude/hooks/skill-activation-prompt.sh
cp .claude/skills/skill-auto-activation-setup/templates/hook-handler-template.ts .claude/hooks/skill-activation-prompt.ts
chmod +x .claude/hooks/skill-activation-prompt.sh
```

### Step 3: Create skill rules configuration

```bash
cp .claude/skills/skill-auto-activation-setup/templates/skill-rules-template.json .claude/skills/skill-rules.json
```

Edit `.claude/skills/skill-rules.json` to define triggers for your skills.

### Step 4: Configure hook in Claude Code settings

For Claude Code web, add to `.claude/settings.json`:

```json
{
  "hooks": {
    "userPromptSubmit": ".claude/hooks/skill-activation-prompt.sh"
  }
}
```

For CLI, check Claude Code documentation for hook configuration.

### Step 5: Test the setup

```bash
# Test the hook directly
echo '{"session_id":"test","transcript_path":"","cwd":"","permission_mode":"auto","prompt":"write a python function"}' | .claude/hooks/skill-activation-prompt.sh
```

If configured correctly, you should see a skill suggestion box with "python-development" listed.

## How It Works

```
User prompt → UserPromptSubmit hook → Analyzes prompt →
Checks skill-rules.json → Matches patterns → Suggests skills → Claude responds
```

The hook runs on every prompt, analyzes keywords and patterns, and suggests relevant skills before Claude generates a response.

## Skill Rules Configuration

Edit `.claude/skills/skill-rules.json` to define triggers:

```json
{
  "version": "1.0.0",
  "skills": {
    "your-skill-name": {
      "type": "domain",
      "enforcement": "suggest",
      "priority": "high",
      "promptTriggers": {
        "keywords": ["keyword1", "keyword2"],
        "intentPatterns": ["pattern.*regex"]
      }
    }
  }
}
```

**Field meanings**:
- `type`: "domain" (domain expertise) or "guardrail" (enforce standards)
- `enforcement`: "suggest" (recommend), "warn" (alert), or "block" (require)
- `priority`: "critical", "high", "medium", or "low"
- `keywords`: Case-insensitive substring matches
- `intentPatterns`: Regex patterns for intent detection

## Template Files

This skill provides templates in the `templates/` directory:

- **hook-template.sh** - Bash wrapper for the hook
- **hook-handler-template.ts** - TypeScript implementation
- **skill-rules-template.json** - Example configuration with python-development triggers

Copy these files to set up the system as shown in Quick Start.

## Detailed Documentation

For detailed information, see:

- **[REFERENCE.md](REFERENCE.md)** - Complete technical reference and architecture
- **[TESTING.md](TESTING.md)** - Comprehensive testing plan with 6 test phases
- **[README.md](README.md)** - Quick overview and usage guide

## Troubleshooting

### Hook doesn't run

1. Verify hook is registered in Claude Code settings
2. Check file permissions: `ls -l .claude/hooks/skill-activation-prompt.sh`
3. Ensure shebang is correct: `#!/bin/bash`
4. Test manually using the command in Step 5 above

### Skills not suggested

1. Verify skill-rules.json exists: `ls .claude/skills/skill-rules.json`
2. Check JSON syntax: `jq . .claude/skills/skill-rules.json`
3. Test keywords match your prompts (case-insensitive)
4. Add logging to TypeScript handler for debugging

### TypeScript errors

1. Ensure Node.js is installed: `node --version`
2. Try installing tsx globally: `npm install -g tsx`
3. Check TypeScript syntax: `npx tsc --noEmit .claude/hooks/skill-activation-prompt.ts`

### Performance issues

If hooks slow down responses:
1. Simplify skill-rules.json (fewer skills, simpler patterns)
2. Use keywords over complex regex patterns
3. Profile hook execution: `time echo '...' | .claude/hooks/skill-activation-prompt.sh`

## Reference Implementation

For a complete production example, see:
https://github.com/diet103/claude-code-infrastructure-showcase

The implementation is based on this proven approach.
