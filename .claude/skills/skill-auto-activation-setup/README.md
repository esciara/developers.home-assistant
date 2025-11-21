# Skill Auto-Activation Setup

This skill helps you set up automatic skill activation in Claude Code using hooks.

## Problem

Skills in Claude Code don't activate automatically - you have to manually invoke them. This skill provides a hook-based solution that automatically suggests relevant skills based on your prompts.

## Quick Start

### 1. Invoke the Skill

When you need help setting up skill auto-activation, use:

```
/skill skill-auto-activation-setup
```

Or reference it directly in your prompt:
```
Help me set up skill auto-activation
```

### 2. Files Provided

This skill includes template files you can use:

- `hook-template.sh` - Bash wrapper for the hook
- `hook-handler-template.ts` - TypeScript implementation
- `skill-rules-template.json` - Example skill rules configuration

### 3. Installation Steps

The skill will guide you through:

1. Creating `.claude/hooks/` directory
2. Copying hook files from templates
3. Creating `.claude/skills/skill-rules.json`
4. Configuring hook in Claude Code settings
5. Testing the setup

## How It Works

```
User submits prompt
    ↓
Hook analyzes prompt
    ↓
Checks skill-rules.json for matches
    ↓
Suggests relevant skills
    ↓
Claude loads skill (if needed)
    ↓
Claude responds with skill knowledge
```

## Configuration

Edit `.claude/skills/skill-rules.json` to define when skills should activate:

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

## Example

When you type "write a python function", the hook will:
1. Detect the keyword "python"
2. Check skill-rules.json for matching skills
3. Suggest the "python-development" skill
4. Claude loads the skill before responding

## Reference

For a complete production example, see:
https://github.com/diet103/claude-code-infrastructure-showcase

## Support

Invoke this skill for detailed setup instructions, troubleshooting, and best practices.
