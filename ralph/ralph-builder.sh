#!/usr/bin/env bash
# ralph-builder.sh — Stop Hook script for autonomous builder iteration
#
# Uses Claude Code's Stop Hook to keep the builder agent working until
# all tasks are complete or safety limits are reached.
#
# Install as a Stop Hook in .claude/settings.json:
#   "hooks": {
#     "Stop": [{
#       "hooks": [{
#         "type": "command",
#         "command": "/path/to/ralph-builder.sh",
#         "timeout": 30
#       }]
#     }]
#   }

set -euo pipefail

# --- Configuration ---
MAX_ITERATIONS="${RALPH_MAX_ITERATIONS:-15}"
NO_PROGRESS_LIMIT="${RALPH_NO_PROGRESS_LIMIT:-3}"
PROGRESS_FILE="${RALPH_PROGRESS_FILE:-.ralph-progress.log}"
STATE_FILE="${RALPH_STATE_FILE:-.ralph-state.json}"

# --- Initialize state file if needed ---
if [ ! -f "$STATE_FILE" ]; then
    cat > "$STATE_FILE" << 'INIT'
{"iteration":0,"no_progress_count":0,"last_commit_hash":"","status":"running"}
INIT
fi

# --- Read current state ---
ITERATION=$(jq -r '.iteration' "$STATE_FILE")
NO_PROGRESS_COUNT=$(jq -r '.no_progress_count' "$STATE_FILE")
LAST_COMMIT_HASH=$(jq -r '.last_commit_hash' "$STATE_FILE")

# --- Increment iteration ---
ITERATION=$((ITERATION + 1))

# --- Safety: Max iterations ---
if [ "$ITERATION" -gt "$MAX_ITERATIONS" ]; then
    echo "Ralph: Max iterations ($MAX_ITERATIONS) reached. Stopping."
    jq '.status = "max_iterations"' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
    # Exit 0 = allow Claude to stop
    exit 0
fi

# --- Check for progress (git commits) ---
CURRENT_COMMIT_HASH=$(git rev-parse HEAD 2>/dev/null || echo "no-git")

if [ "$CURRENT_COMMIT_HASH" = "$LAST_COMMIT_HASH" ]; then
    NO_PROGRESS_COUNT=$((NO_PROGRESS_COUNT + 1))
    echo "Ralph: No new commits (attempt $NO_PROGRESS_COUNT/$NO_PROGRESS_LIMIT)"
else
    NO_PROGRESS_COUNT=0
fi

# --- Safety: No progress circuit breaker ---
if [ "$NO_PROGRESS_COUNT" -ge "$NO_PROGRESS_LIMIT" ]; then
    echo "Ralph: No progress for $NO_PROGRESS_LIMIT iterations. Stopping."
    jq '.status = "no_progress"' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
    exit 0
fi

# --- Check for completion signal ---
# Read stdin (Claude's last response context)
STDIN_CONTENT=""
if [ ! -t 0 ]; then
    STDIN_CONTENT=$(cat)
fi

# Check if Claude signaled completion
if echo "$STDIN_CONTENT" | grep -qi "all tasks complete\|all acceptance criteria met\|RALPH_COMPLETE"; then
    echo "Ralph: Completion signal detected. Stopping."
    jq '.status = "complete"' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
    exit 0
fi

# --- Check for test failures that persist ---
if echo "$STDIN_CONTENT" | grep -qi "escalat\|blocker\|cannot proceed\|giving up"; then
    echo "Ralph: Builder escalated a blocker. Stopping for human review."
    jq '.status = "blocked"' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
    exit 0
fi

# --- Update state ---
jq \
    --argjson iter "$ITERATION" \
    --argjson npc "$NO_PROGRESS_COUNT" \
    --arg hash "$CURRENT_COMMIT_HASH" \
    '.iteration = $iter | .no_progress_count = $npc | .last_commit_hash = $hash' \
    "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"

# --- Log progress ---
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Iteration $ITERATION | Commits: $([ "$CURRENT_COMMIT_HASH" != "$LAST_COMMIT_HASH" ] && echo 'new' || echo 'none')" >> "$PROGRESS_FILE"

# --- Force continue ---
# Output JSON that tells Claude Code to continue with context
cat << EOF
{
  "decision": "block",
  "reason": "Ralph loop iteration $ITERATION/$MAX_ITERATIONS: Continue working on remaining tasks. Check your plan and pick up the next incomplete task."
}
EOF
