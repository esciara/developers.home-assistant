---
name: "Skill Auto-Activation Setup"
description: "Set up hook-based auto-activation for Claude Code skills using UserPromptSubmit hooks"
---

# Skill Auto-Activation Setup

This skill guides you through setting up a hook-based system for automatically activating Claude Code skills based on user prompts and file context.

## Problem Statement

By default, Claude Code skills don't activate automatically - users must manually invoke them using the Skill tool. This creates friction and reduces the effectiveness of skills. The auto-activation system solves this by:

1. Analyzing user prompts for keywords and intent patterns
2. Checking file context (paths, content patterns)
3. Automatically suggesting relevant skills before Claude responds
4. Supporting different enforcement levels (suggest, warn, block)

## How Auto-Activation Works

The system uses a **UserPromptSubmit hook** that runs on every user prompt:

```
User submits prompt → Hook analyzes prompt → Checks skill-rules.json →
Matches patterns → Suggests skills → Skills load (if needed) → Claude responds
```

## Core Components

### 1. Hook Script (`.claude/hooks/skill-activation-prompt.sh`)

A bash wrapper that pipes input to a TypeScript handler:

```bash
#!/bin/bash
set -e

cd "$CLAUDE_PROJECT_DIR/.claude/hooks"
cat | npx tsx skill-activation-prompt.ts
```

### 2. TypeScript Handler (`.claude/hooks/skill-activation-prompt.ts`)

Analyzes prompts against skill rules:
- Reads stdin for hook input (JSON with prompt, session info, etc.)
- Loads `skill-rules.json` configuration
- Performs keyword matching (case-insensitive substring search)
- Performs intent pattern matching (regex patterns)
- Outputs prioritized skill suggestions

### 3. Skill Rules Configuration (`.claude/skills/skill-rules.json`)

Defines trigger patterns for each skill:

```json
{
  "version": "1.0.0",
  "skills": {
    "skill-name": {
      "type": "domain",
      "enforcement": "suggest",
      "priority": "high",
      "promptTriggers": {
        "keywords": ["keyword1", "keyword2"],
        "intentPatterns": ["pattern.*regex"]
      },
      "fileTriggers": {
        "paths": ["src/**/*.ts"],
        "excludePaths": ["**/*.test.ts"],
        "contentPatterns": ["import.*from"]
      }
    }
  }
}
```

### 4. Dependencies

The system requires:
- `tsx` - TypeScript execution engine (installed via npx, no package.json needed)
- Node.js runtime (usually available in Claude Code environments)

## Setup Instructions

### Step 1: Create Hooks Directory

```bash
mkdir -p .claude/hooks
```

### Step 2: Create Hook Script

Create `.claude/hooks/skill-activation-prompt.sh`:

```bash
#!/bin/bash
set -e

cd "$CLAUDE_PROJECT_DIR/.claude/hooks"
cat | npx tsx skill-activation-prompt.ts
```

Make it executable:

```bash
chmod +x .claude/hooks/skill-activation-prompt.sh
```

### Step 3: Create TypeScript Handler

Create `.claude/hooks/skill-activation-prompt.ts` with the full TypeScript implementation (see TypeScript Handler Implementation section below).

### Step 4: Create Skill Rules

Create `.claude/skills/skill-rules.json` with your skill definitions.

### Step 5: Configure Hook in Settings

The hook must be registered in Claude Code settings. The configuration looks like:

```json
{
  "hooks": {
    "userPromptSubmit": ".claude/hooks/skill-activation-prompt.sh"
  }
}
```

Note: Hook configuration is typically managed through Claude Code's settings UI or configuration file. The exact location depends on whether you're using CLI or web version.

## TypeScript Handler Implementation

Here's the complete TypeScript handler code:

```typescript
#!/usr/bin/env node
import { readFileSync } from 'fs';
import { join } from 'path';

interface HookInput {
  session_id: string;
  transcript_path: string;
  cwd: string;
  permission_mode: string;
  prompt: string;
}

interface PromptTriggers {
  keywords?: string[];
  intentPatterns?: string[];
}

interface SkillRule {
  type: 'guardrail' | 'domain';
  enforcement: 'block' | 'suggest' | 'warn';
  priority: 'critical' | 'high' | 'medium' | 'low';
  promptTriggers?: PromptTriggers;
}

interface SkillRules {
  version: string;
  skills: Record<string, SkillRule>;
}

interface MatchedSkill {
  name: string;
  matchType: 'keyword' | 'intent';
  config: SkillRule;
}

async function main() {
  try {
    const input = readFileSync(0, 'utf-8');
    const data: HookInput = JSON.parse(input);
    const prompt = data.prompt.toLowerCase();

    const projectDir = process.env.CLAUDE_PROJECT_DIR || '$HOME/project';
    const rulesPath = join(projectDir, '.claude', 'skills', 'skill-rules.json');
    const rules: SkillRules = JSON.parse(readFileSync(rulesPath, 'utf-8'));

    const matchedSkills: MatchedSkill[] = [];

    for (const [skillName, config] of Object.entries(rules.skills)) {
      const triggers = config.promptTriggers;
      if (!triggers) {
        continue;
      }

      if (triggers.keywords) {
        const keywordMatch = triggers.keywords.some(kw =>
          prompt.includes(kw.toLowerCase())
        );
        if (keywordMatch) {
          matchedSkills.push({ name: skillName, matchType: 'keyword', config });
          continue;
        }
      }

      if (triggers.intentPatterns) {
        const intentMatch = triggers.intentPatterns.some(pattern => {
          const regex = new RegExp(pattern, 'i');
          return regex.test(prompt);
        });
        if (intentMatch) {
          matchedSkills.push({ name: skillName, matchType: 'intent', config });
        }
      }
    }

    if (matchedSkills.length > 0) {
      let output = '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n';
      output += '🎯 SKILL ACTIVATION CHECK\n';
      output += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n';

      const critical = matchedSkills.filter(s => s.config.priority === 'critical');
      const high = matchedSkills.filter(s => s.config.priority === 'high');
      const medium = matchedSkills.filter(s => s.config.priority === 'medium');
      const low = matchedSkills.filter(s => s.config.priority === 'low');

      if (critical.length > 0) {
        output += '⚠️ CRITICAL SKILLS (REQUIRED):\n';
        critical.forEach(s => output += ` → ${s.name}\n`);
        output += '\n';
      }

      if (high.length > 0) {
        output += '📚 RECOMMENDED SKILLS:\n';
        high.forEach(s => output += ` → ${s.name}\n`);
        output += '\n';
      }

      if (medium.length > 0) {
        output += '💡 SUGGESTED SKILLS:\n';
        medium.forEach(s => output += ` → ${s.name}\n`);
        output += '\n';
      }

      if (low.length > 0) {
        output += '📌 OPTIONAL SKILLS:\n';
        low.forEach(s => output += ` → ${s.name}\n`);
        output += '\n';
      }

      output += 'ACTION: Use Skill tool BEFORE responding\n';
      output += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n';

      console.log(output);
    }

    process.exit(0);
  } catch (err) {
    console.error('Error in skill-activation-prompt hook:', err);
    process.exit(1);
  }
}

main().catch(err => {
  console.error('Uncaught error:', err);
  process.exit(1);
});
```

## Example Skill Rules Configuration

Here's a starter `skill-rules.json` template:

```json
{
  "version": "1.0.0",
  "skills": {
    "python-development": {
      "type": "domain",
      "enforcement": "suggest",
      "priority": "high",
      "promptTriggers": {
        "keywords": [
          "python",
          "pytest",
          "mypy",
          "type hint",
          "pydantic"
        ],
        "intentPatterns": [
          "write.*python.*function",
          "create.*python.*class",
          "fix.*python.*error"
        ]
      }
    }
  }
}
```

## Skill Rule Schema

### Skill Configuration Fields

- **type**: `"guardrail"` or `"domain"`
  - `guardrail`: Enforces standards/best practices
  - `domain`: Provides domain-specific knowledge

- **enforcement**: `"suggest"`, `"warn"`, or `"block"`
  - `suggest`: Appears in suggestion list
  - `warn`: Shows warning but allows continuation
  - `block`: Requires skill activation before proceeding

- **priority**: `"critical"`, `"high"`, `"medium"`, or `"low"`
  - Determines display order and emphasis

- **promptTriggers**: Prompt-based activation
  - `keywords`: Case-insensitive substring matches
  - `intentPatterns`: Regex patterns for intent detection

- **fileTriggers**: File-based activation (not implemented in basic version)
  - `paths`: Glob patterns for file paths
  - `excludePaths`: Glob patterns to exclude
  - `contentPatterns`: Regex patterns for file content

## Hook Configuration Methods

### Method 1: Web Settings (Claude Code Web)

For Claude Code on the web, hooks are configured in `.claude/settings.json`:

```json
{
  "hooks": {
    "userPromptSubmit": ".claude/hooks/skill-activation-prompt.sh"
  }
}
```

### Method 2: CLI Settings (Claude Code CLI)

For CLI users, hooks may be configured in user settings or project settings. Consult Claude Code documentation for exact path.

### Method 3: SessionStart Hook (Recommended for Web)

For Claude Code web sessions, you can use a SessionStart hook to automatically configure the system:

```bash
#!/bin/bash
# .claude/hooks/session-start.sh

# Ensure hook is registered
if command -v gh >/dev/null 2>&1; then
  echo "Skill auto-activation system ready"
  echo "skill-rules.json location: .claude/skills/skill-rules.json"
fi
```

## Testing the Setup

### Test 1: Verify Files Exist

```bash
ls -la .claude/hooks/skill-activation-prompt.sh
ls -la .claude/hooks/skill-activation-prompt.ts
ls -la .claude/skills/skill-rules.json
```

### Test 2: Check Script Permissions

```bash
test -x .claude/hooks/skill-activation-prompt.sh && echo "Executable" || echo "Not executable"
```

### Test 3: Test TypeScript Handler Directly

```bash
echo '{"session_id":"test","transcript_path":"","cwd":"","permission_mode":"auto","prompt":"write a python function"}' | npx tsx .claude/hooks/skill-activation-prompt.ts
```

Expected output: Skill suggestions if "python" triggers match rules in skill-rules.json

### Test 4: Test in Claude Session

Submit a prompt that matches your skill rules and observe if the skill activation notification appears.

## Troubleshooting

### Hook Not Running

1. Verify hook is registered in settings
2. Check file permissions (must be executable)
3. Verify shebang line is correct (`#!/bin/bash`)
4. Check Claude Code logs for hook errors

### TypeScript Errors

1. Ensure Node.js is installed
2. Try installing tsx globally: `npm install -g tsx`
3. Check TypeScript syntax in .ts file
4. Verify skill-rules.json is valid JSON

### Skills Not Activating

1. Check skill-rules.json syntax
2. Verify keywords match your prompts (case-insensitive)
3. Test regex patterns with online regex testers
4. Add logging to TypeScript handler for debugging

### Performance Issues

If hooks slow down responses:
1. Simplify skill-rules.json (fewer skills, simpler patterns)
2. Use keywords over complex regex patterns
3. Consider lazy-loading the rules file
4. Cache parsed rules in memory

## Advanced Configuration

### File Context Triggers

To add file-based triggering, extend the TypeScript handler to read the current file context from the hook input and match against `fileTriggers` patterns.

### Session State Tracking

Track which skills have been activated in the current session to avoid repeated suggestions.

### Custom Enforcement Logic

Implement blocking enforcement by checking if required skills have been activated before allowing Claude to proceed.

### Multi-Project Support

Use different skill-rules.json files for different projects by detecting project type in the hook.

## Best Practices

1. **Start Simple**: Begin with just keyword triggers for your most important skills
2. **Test Iteratively**: Add one skill rule at a time and test thoroughly
3. **Use Specific Keywords**: Choose keywords that are unique to each skill domain
4. **Prioritize Carefully**: Reserve "critical" priority for must-have skills
5. **Document Rules**: Add comments in JSON (if supported) or maintain separate docs
6. **Monitor Performance**: Track hook execution time and optimize if needed
7. **Version Control**: Commit skill-rules.json to track changes over time
8. **Share Patterns**: Create reusable skill rule templates for common scenarios

## Integration with Existing Skills

To make your existing skills auto-activate:

1. Identify the skill's domain or purpose
2. List keywords users might type when needing this skill
3. Create intent patterns for common requests
4. Add an entry to skill-rules.json
5. Test with various prompts
6. Refine based on false positives/negatives

## Example: Auto-Activating Python Development Skill

If you have a `python-development` skill, add this to skill-rules.json:

```json
{
  "version": "1.0.0",
  "skills": {
    "python-development": {
      "type": "domain",
      "enforcement": "suggest",
      "priority": "high",
      "promptTriggers": {
        "keywords": [
          "python",
          "pytest",
          "mypy",
          "type checking",
          "pydantic",
          "fastapi",
          "async",
          "asyncio"
        ],
        "intentPatterns": [
          "write.*python",
          "create.*python",
          "fix.*python",
          "refactor.*python",
          "test.*python",
          "type.*hint"
        ]
      }
    }
  }
}
```

Now when users say "write a python function" or "fix this python error", the hook will automatically suggest the python-development skill.

## Maintenance

### Updating Rules

Edit `.claude/skills/skill-rules.json` directly. Changes take effect immediately on next prompt.

### Monitoring Usage

Add logging to the TypeScript handler to track which skills are being suggested and how often.

### Collecting Feedback

Ask users if skill suggestions are helpful and refine rules based on feedback.

## Reference Implementation

For a complete production example, see:
- Repository: https://github.com/diet103/claude-code-infrastructure-showcase
- Hook files: `.claude/hooks/skill-activation-prompt.*`
- Example rules: `.claude/skills/skill-rules.json`

## Summary

The skill auto-activation system transforms Claude Code skills from passive tools into proactive assistants. By setting up:

1. A UserPromptSubmit hook (bash + TypeScript)
2. A skill-rules.json configuration
3. Proper hook registration

You enable Claude to automatically suggest relevant skills based on user intent, making the development experience more seamless and efficient.
