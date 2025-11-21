#!/bin/bash
# UserPromptSubmit hook for skill auto-activation
# Copy this file to .claude/hooks/skill-activation-prompt.sh
# Make it executable: chmod +x .claude/hooks/skill-activation-prompt.sh

set -e

cd "$CLAUDE_PROJECT_DIR/.claude/hooks"
cat | npx tsx skill-activation-prompt.ts
