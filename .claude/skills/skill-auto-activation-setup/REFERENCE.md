# Technical Reference

Complete technical documentation for the skill auto-activation system.

## Architecture Overview

The auto-activation system consists of three main components:

1. **Bash Wrapper** (`.claude/hooks/skill-activation-prompt.sh`) - Entry point for the UserPromptSubmit hook
2. **TypeScript Handler** (`.claude/hooks/skill-activation-prompt.ts`) - Core logic for pattern matching
3. **Configuration File** (`.claude/skills/skill-rules.json`) - Skill trigger definitions

### Data Flow

```
Claude Code
    ↓ (UserPromptSubmit event)
skill-activation-prompt.sh
    ↓ (pipes stdin)
skill-activation-prompt.ts
    ↓ (reads)
skill-rules.json
    ↓ (matches patterns)
Output to stdout → Claude Code displays suggestions
```

## Hook Input Format

The UserPromptSubmit hook receives JSON on stdin:

```typescript
interface HookInput {
  session_id: string;           // Unique session identifier
  transcript_path: string;       // Path to conversation transcript
  cwd: string;                   // Current working directory
  permission_mode: string;       // Permission mode (e.g., "auto")
  prompt: string;                // User's prompt text
}
```

Example:
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/home/user/project",
  "permission_mode": "auto",
  "prompt": "write a python function to parse CSV files"
}
```

## Hook Output Format

The hook outputs formatted text to stdout that Claude Code displays to the user:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 SKILL ACTIVATION CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ CRITICAL SKILLS (REQUIRED):
 → skill-name-1

📚 RECOMMENDED SKILLS:
 → skill-name-2
 → skill-name-3

💡 SUGGESTED SKILLS:
 → skill-name-4

📌 OPTIONAL SKILLS:
 → skill-name-5

ACTION: Use Skill tool BEFORE responding
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Skill Rules Schema

### Complete Schema

```typescript
interface SkillRules {
  version: string;              // Schema version (currently "1.0.0")
  skills: Record<string, SkillRule>;
}

interface SkillRule {
  type: 'guardrail' | 'domain';
  enforcement: 'block' | 'suggest' | 'warn';
  priority: 'critical' | 'high' | 'medium' | 'low';
  promptTriggers?: PromptTriggers;
  fileTriggers?: FileTriggers;   // Future enhancement
  skipConditions?: SkipConditions; // Future enhancement
}

interface PromptTriggers {
  keywords?: string[];           // Case-insensitive substring matches
  intentPatterns?: string[];     // Regex patterns
}

interface FileTriggers {
  paths?: string[];              // Glob patterns for file paths
  excludePaths?: string[];       // Glob patterns to exclude
  contentPatterns?: string[];    // Regex patterns for file content
}
```

### Field Descriptions

**type**:
- `domain`: Provides domain-specific expertise (e.g., python-development)
- `guardrail`: Enforces standards and best practices (e.g., security-review)

**enforcement**:
- `suggest`: Appears in suggestion list (non-blocking)
- `warn`: Shows warning but allows continuation
- `block`: Requires skill activation before proceeding (not implemented in basic version)

**priority**:
- `critical`: Shown first with ⚠️ icon, considered required
- `high`: Shown second with 📚 icon, recommended
- `medium`: Shown third with 💡 icon, suggested
- `low`: Shown last with 📌 icon, optional

**keywords**:
- Performs case-insensitive substring matching
- Example: `"python"` matches "Python", "PYTHON", "python function"
- Multiple keywords are OR'd (any match triggers the skill)

**intentPatterns**:
- JavaScript-compatible regex patterns (case-insensitive flag automatically applied)
- Matches against the full prompt text
- Example: `"write.*python.*function"` matches "write a python function", "write Python function", etc.
- Multiple patterns are OR'd (any match triggers the skill)

## Pattern Matching Logic

### Keyword Matching

```typescript
const keywordMatch = triggers.keywords.some(kw =>
  prompt.toLowerCase().includes(kw.toLowerCase())
);
```

- Converts both prompt and keyword to lowercase
- Uses substring matching
- Fast and efficient
- Use for simple text matches

### Intent Pattern Matching

```typescript
const intentMatch = triggers.intentPatterns.some(pattern => {
  const regex = new RegExp(pattern, 'i');  // 'i' flag for case-insensitive
  return regex.test(prompt);
});
```

- Creates regex with case-insensitive flag
- Tests against full prompt
- More flexible than keywords
- Use for complex matching logic

### Matching Priority

If multiple skills match:
1. All matching skills are collected
2. Skills are grouped by priority level
3. Each priority level is displayed in order (critical → high → medium → low)
4. Within each level, skills are displayed in the order they matched

## Hook Implementation Details

### Bash Wrapper (`hook-template.sh`)

```bash
#!/bin/bash
set -e

cd "$CLAUDE_PROJECT_DIR/.claude/hooks"
cat | npx tsx skill-activation-prompt.ts
```

**Key features**:
- `set -e`: Exits on any error
- `cd $CLAUDE_PROJECT_DIR`: Ensures correct working directory
- `cat |`: Pipes stdin to TypeScript handler
- `npx tsx`: Executes TypeScript without compilation

**Environment variables**:
- `CLAUDE_PROJECT_DIR`: Set by Claude Code, points to project root

### TypeScript Handler (`hook-handler-template.ts`)

**Main function flow**:

1. Read stdin and parse JSON
2. Extract prompt and convert to lowercase
3. Resolve skill-rules.json path
4. Load and parse skill rules
5. Iterate through all skills
6. For each skill, check keyword and pattern triggers
7. Collect all matching skills
8. Sort by priority level
9. Format and output results

**Error handling**:
- Gracefully exits (code 0) if skill-rules.json doesn't exist
- Reports errors to stderr if JSON parsing fails
- Exits with code 1 on errors

**Performance considerations**:
- Reads stdin once
- Loads skill-rules.json once
- Single pass through skills
- No external dependencies beyond Node.js standard library
- Typical execution time: < 50ms

## Configuration Best Practices

### Keyword Selection

**Good keywords**:
- Specific terms unique to the skill domain
- Common variations of technical terms
- Short and memorable
- Example: `["python", "pytest", "mypy"]`

**Avoid**:
- Generic words that appear in many contexts ("code", "test", "function")
- Very long phrases (use intent patterns instead)
- Overlapping keywords between skills

### Intent Pattern Design

**Good patterns**:
- Match specific user intents
- Allow for natural language variation
- Example: `"write.*python.*function"` matches various phrasings

**Avoid**:
- Overly broad patterns (`".*python.*"` matches everything with "python")
- Very complex regex (impacts performance and maintainability)
- Patterns that match unintended prompts

### Skill Organization

**By priority**:
- `critical`: Security, compliance, breaking changes
- `high`: Core workflow skills (language development, testing)
- `medium`: Helper utilities, optional enhancements
- `low`: Experimental features, nice-to-haves

**By enforcement**:
- `suggest`: Most skills (non-intrusive)
- `warn`: Important but optional (code review, performance)
- `block`: Critical requirements (security scans, legal compliance)

## Extension Points

### Adding File Context Triggers

To extend the system with file-based triggering:

1. Modify HookInput interface to include file paths
2. Add logic to read current file paths from transcript
3. Implement glob pattern matching for `fileTriggers.paths`
4. Implement content pattern matching for `fileTriggers.contentPatterns`

Example implementation:
```typescript
if (fileTriggers?.paths) {
  const fileMatch = fileTriggers.paths.some(pattern => {
    return currentFiles.some(file => minimatch(file, pattern));
  });
}
```

### Adding Session State Tracking

To avoid repeated suggestions in the same session:

1. Add session_id to tracking
2. Store activated skills per session
3. Skip already-activated skills in current session
4. Reset on new session or user request

### Custom Enforcement Logic

To implement blocking enforcement:

1. Check if critical/high priority skills matched
2. If matched and enforcement is "block"
3. Output blocking message instead of suggestion
4. Claude Code should respect this and wait for skill activation

## Integration with Claude Code

### Hook Registration

**Web version** (`.claude/settings.json`):
```json
{
  "hooks": {
    "userPromptSubmit": ".claude/hooks/skill-activation-prompt.sh"
  }
}
```

**CLI version**:
- Configuration location varies by platform
- Check Claude Code documentation for current method
- May use global settings file or project-specific config

### Hook Execution Environment

The hook runs in a sandboxed environment with:
- Read access to project files
- Environment variables from Claude Code
- Node.js runtime (if available)
- No network access (by design)
- Limited execution time (timeout after ~5 seconds)

### Error Handling

If the hook fails:
- Claude Code logs the error
- User sees a notification (if enabled in settings)
- Claude continues normally without suggestions
- Hook failure doesn't block Claude from responding

## Performance Optimization

### For Large Projects

If you have many skills (10+):
1. Use keywords for fast initial filtering
2. Reserve intent patterns for complex cases
3. Consider lazy-loading skill-rules.json
4. Cache parsed JSON in memory (requires stateful hook)

### For Complex Patterns

If regex patterns are slow:
1. Simplify patterns where possible
2. Use keywords for broad matching, patterns for refinement
3. Profile with `time` command to identify slow patterns
4. Consider preprocessing prompts (tokenization, normalization)

### For Frequent Prompts

If users submit many prompts:
1. Optimize for common case (no matches) - fail fast
2. Use early returns in matching logic
3. Avoid unnecessary string allocations
4. Consider caching recent results (requires state)

## Security Considerations

### Input Validation

The hook receives untrusted input from users:
- Prompt text could contain special characters
- Validate JSON structure before processing
- Sanitize regex patterns to prevent ReDoS attacks
- Limit pattern complexity

### File System Access

The hook can read project files:
- Validate file paths before reading
- Avoid following symlinks outside project
- Respect `.gitignore` and similar exclusions
- Don't read sensitive files (.env, credentials)

### Code Execution

The hook executes TypeScript code:
- Review skill-rules.json before deployment
- Don't allow user-provided regex in production
- Consider CSP-style restrictions on patterns
- Audit changes to hook implementation

## Troubleshooting Guide

### Hook Not Executing

**Symptoms**: No skill suggestions appear, hook seems inactive

**Diagnostics**:
```bash
# Check hook exists
ls -l .claude/hooks/skill-activation-prompt.sh

# Check permissions
test -x .claude/hooks/skill-activation-prompt.sh && echo "Executable" || echo "Not executable"

# Test manually
echo '{"session_id":"test","transcript_path":"","cwd":"","permission_mode":"auto","prompt":"python"}' | .claude/hooks/skill-activation-prompt.sh

# Check Claude Code logs (location varies)
tail -f ~/.claude/logs/hooks.log
```

**Common causes**:
- Hook not registered in settings
- File not executable (`chmod +x`)
- Incorrect shebang line
- TypeScript handler not found

### Pattern Matching Issues

**Symptoms**: Expected skills don't appear in suggestions

**Diagnostics**:
```bash
# Check skill-rules.json syntax
jq . .claude/skills/skill-rules.json

# Test specific pattern
node -e "console.log(/'pattern'.test('your prompt text'))"

# Add debug logging to TypeScript handler
# Insert: console.error('Checking skill:', skillName, 'against prompt:', prompt);
```

**Common causes**:
- Keywords don't match (check case-sensitivity)
- Regex patterns too specific or too broad
- JSON syntax errors in skill-rules.json
- Skill name typo in configuration

### Performance Problems

**Symptoms**: Noticeable delay before Claude responds

**Diagnostics**:
```bash
# Time hook execution
time echo '{"session_id":"test","transcript_path":"","cwd":"","permission_mode":"auto","prompt":"test"}' | .claude/hooks/skill-activation-prompt.sh

# Profile TypeScript (add timing code)
# const start = Date.now();
# ... code ...
# console.error('Took:', Date.now() - start, 'ms');
```

**Common causes**:
- Too many skills in skill-rules.json
- Complex regex patterns (backtracking)
- Large skill-rules.json file
- Slow file system access

## Migration Guide

### From Manual Skill Invocation

If you currently invoke skills manually:

1. Identify which skills you use most often
2. Note what keywords/phrases you use to recognize when each skill is needed
3. Add those keywords to skill-rules.json
4. Test with typical prompts
5. Refine keywords based on false positives/negatives

### From Other Hook Systems

If you have existing hooks:

1. Review current hook for conflicts
2. Consider merging hook logic if needed
3. Ensure hook output formats are compatible
4. Test both hooks together
5. Monitor for interference or duplicate suggestions

## Appendix: Complete Examples

### Example 1: Python Development Skill

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
          "pydantic",
          "fastapi",
          "async",
          "asyncio",
          "loguru"
        ],
        "intentPatterns": [
          "write.*python",
          "create.*python",
          "fix.*python",
          "test.*python",
          "type.*check",
          "add.*type.*annotation"
        ]
      }
    }
  }
}
```

### Example 2: Security Review Skill

```json
{
  "version": "1.0.0",
  "skills": {
    "security-review": {
      "type": "guardrail",
      "enforcement": "warn",
      "priority": "critical",
      "promptTriggers": {
        "keywords": [
          "authentication",
          "authorization",
          "password",
          "token",
          "secret",
          "api key",
          "credential"
        ],
        "intentPatterns": [
          "add.*auth",
          "implement.*login",
          "store.*password",
          "handle.*secret"
        ]
      }
    }
  }
}
```

### Example 3: Multi-Skill Configuration

```json
{
  "version": "1.0.0",
  "skills": {
    "python-development": {
      "type": "domain",
      "enforcement": "suggest",
      "priority": "high",
      "promptTriggers": {
        "keywords": ["python", "pytest", "mypy"],
        "intentPatterns": ["write.*python", "test.*python"]
      }
    },
    "security-review": {
      "type": "guardrail",
      "enforcement": "warn",
      "priority": "critical",
      "promptTriggers": {
        "keywords": ["auth", "password", "secret"],
        "intentPatterns": ["implement.*security", "add.*auth"]
      }
    },
    "code-review": {
      "type": "guardrail",
      "enforcement": "suggest",
      "priority": "medium",
      "promptTriggers": {
        "keywords": ["review", "refactor", "optimize"],
        "intentPatterns": ["review.*code", "improve.*code"]
      }
    }
  }
}
```

## Related Resources

- [Claude Code Skills Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills)
- [Claude Code Hooks Documentation](https://docs.claude.com/)
- [Reference Implementation](https://github.com/diet103/claude-code-infrastructure-showcase)
- [Testing Guide](TESTING.md)
- [Quick Start Guide](README.md)
