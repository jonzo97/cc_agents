#!/usr/bin/env bash
# ralph-v2.sh — Enhanced stop hook with dual-condition gate, cost tracking, and circuit breakers
#
# IMPROVEMENTS OVER V1:
# - Dual-condition exit gate (signal + heuristics both must pass)
# - Cost tracking with budget enforcement
# - Repeated-error circuit breaker
# - Task-aware progress tracking
# - Configurable signals via env vars

set -euo pipefail

# --- Configuration ---
MAX_ITERATIONS="${RALPH_MAX_ITERATIONS:-15}"
NO_PROGRESS_LIMIT="${RALPH_NO_PROGRESS_LIMIT:-3}"
PROGRESS_FILE="${RALPH_PROGRESS_FILE:-.ralph-v2-progress.log}"
STATE_FILE="${RALPH_STATE_FILE:-.ralph-v2-state.json}"

# V2 additions
COST_BUDGET="${RALPH_COST_BUDGET:-}"  # Empty = unlimited
COST_PER_ITERATION="${RALPH_COST_PER_ITERATION:-0.50}"
EXIT_SIGNALS="${RALPH_EXIT_SIGNALS:-RALPH_COMPLETE,all tasks complete,all acceptance criteria met}"
BLOCKER_SIGNALS="${RALPH_BLOCKER_SIGNALS:-escalat,blocker,cannot proceed,giving up}"

# --- Utility functions ---
hash_string() {
    echo -n "$1" | md5sum | awk '{print $1}'
}

detect_test_runner() {
    # Detect test framework by checking for common files
    if [ -f "package.json" ] && grep -q '"test"' package.json 2>/dev/null; then
        echo "npm"
    elif [ -f "pytest.ini" ] || [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
        echo "pytest"
    elif [ -f "Makefile" ] && grep -q "^test:" Makefile 2>/dev/null; then
        echo "make"
    else
        echo "none"
    fi
}

run_tests() {
    local runner="$1"
    case "$runner" in
        npm)
            npm test 2>&1 | tail -5 | grep -qi "pass\|ok" && return 0 || return 1
            ;;
        pytest)
            pytest --tb=no -q 2>&1 | tail -5 | grep -qi "passed" && return 0 || return 1
            ;;
        make)
            make test 2>&1 | tail -5 | grep -qi "pass\|ok" && return 0 || return 1
            ;;
        *)
            return 0  # No tests = pass by default
            ;;
    esac
}

check_git_clean() {
    # Clean if no unstaged/uncommitted changes
    git diff --quiet && git diff --cached --quiet 2>/dev/null
}

count_tasks_from_stdin() {
    local content="$1"
    # Parse TodoWrite-style task lists or simple checkboxes
    local completed=$(echo "$content" | grep -ci "status.*completed\|✓\|✅" || echo "0")
    local total=$(echo "$content" | grep -ci "status.*\|task\|TODO" || echo "0")
    echo "$completed $total"
}

# --- Initialize state file if needed ---
if [ ! -f "$STATE_FILE" ]; then
    cat > "$STATE_FILE" << 'INIT'
{
  "iteration": 0,
  "no_progress_count": 0,
  "last_commit_hash": "",
  "cumulative_cost": 0.0,
  "last_error_hash": "",
  "error_repeat_count": 0,
  "completed_tasks": 0,
  "total_tasks": 0,
  "status": "running"
}
INIT
fi

# --- Read current state ---
ITERATION=$(jq -r '.iteration' "$STATE_FILE")
NO_PROGRESS_COUNT=$(jq -r '.no_progress_count' "$STATE_FILE")
LAST_COMMIT_HASH=$(jq -r '.last_commit_hash' "$STATE_FILE")
CUMULATIVE_COST=$(jq -r '.cumulative_cost' "$STATE_FILE")
LAST_ERROR_HASH=$(jq -r '.last_error_hash' "$STATE_FILE")
ERROR_REPEAT_COUNT=$(jq -r '.error_repeat_count' "$STATE_FILE")

# --- Increment iteration and cost ---
ITERATION=$((ITERATION + 1))
CUMULATIVE_COST=$(echo "$CUMULATIVE_COST + $COST_PER_ITERATION" | bc)

# --- Safety: Cost budget ---
if [ -n "$COST_BUDGET" ]; then
    if (( $(echo "$CUMULATIVE_COST > $COST_BUDGET" | bc -l) )); then
        echo "Ralph v2: Cost budget exceeded (\$${CUMULATIVE_COST} > \$${COST_BUDGET}). Stopping."
        jq --argjson cost "$CUMULATIVE_COST" '.status = "budget_exceeded" | .cumulative_cost = $cost' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
        exit 0
    fi
fi

# --- Safety: Max iterations ---
if [ "$ITERATION" -gt "$MAX_ITERATIONS" ]; then
    echo "Ralph v2: Max iterations ($MAX_ITERATIONS) reached. Stopping."
    jq --argjson cost "$CUMULATIVE_COST" '.status = "max_iterations" | .cumulative_cost = $cost' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
    exit 0
fi

# --- Read stdin (Claude's last response context) ---
STDIN_CONTENT=""
if [ ! -t 0 ]; then
    STDIN_CONTENT=$(cat)
fi

# --- Check for repeated errors ---
ERROR_DETECTED=0
for signal in $(echo "$BLOCKER_SIGNALS" | tr ',' ' '); do
    if echo "$STDIN_CONTENT" | grep -qi "$signal"; then
        ERROR_DETECTED=1
        break
    fi
done

if [ "$ERROR_DETECTED" -eq 1 ]; then
    CURRENT_ERROR_HASH=$(hash_string "$STDIN_CONTENT")
    if [ "$CURRENT_ERROR_HASH" = "$LAST_ERROR_HASH" ]; then
        ERROR_REPEAT_COUNT=$((ERROR_REPEAT_COUNT + 1))
        if [ "$ERROR_REPEAT_COUNT" -ge 2 ]; then
            echo "Ralph v2: Same error repeated ${ERROR_REPEAT_COUNT} times. Circuit breaker triggered."
            jq --argjson cost "$CUMULATIVE_COST" '.status = "repeated_error" | .cumulative_cost = $cost' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
            exit 0
        fi
    else
        ERROR_REPEAT_COUNT=1
        LAST_ERROR_HASH="$CURRENT_ERROR_HASH"
    fi
else
    ERROR_REPEAT_COUNT=0
    LAST_ERROR_HASH=""
fi

# --- Check for completion signal ---
COMPLETION_SIGNAL_DETECTED=0
for signal in $(echo "$EXIT_SIGNALS" | tr ',' ' '); do
    if echo "$STDIN_CONTENT" | grep -qi "$signal"; then
        COMPLETION_SIGNAL_DETECTED=1
        break
    fi
done

# --- Dual-condition exit gate: Signal + Heuristics ---
if [ "$COMPLETION_SIGNAL_DETECTED" -eq 1 ]; then
    echo "Ralph v2: Completion signal detected. Verifying with heuristics..."

    # Heuristic 1: Run tests
    TEST_RUNNER=$(detect_test_runner)
    TESTS_PASS=0
    if [ "$TEST_RUNNER" != "none" ]; then
        if run_tests "$TEST_RUNNER"; then
            echo "  ✓ Tests pass ($TEST_RUNNER)"
            TESTS_PASS=1
        else
            echo "  ✗ Tests FAIL ($TEST_RUNNER)"
        fi
    else
        echo "  ⊘ No test runner detected (assuming pass)"
        TESTS_PASS=1
    fi

    # Heuristic 2: Git clean
    GIT_CLEAN=0
    if check_git_clean; then
        echo "  ✓ Git working tree clean"
        GIT_CLEAN=1
    else
        echo "  ✗ Git has uncommitted changes"
    fi

    # Heuristic 3: Task completion
    read COMPLETED TOTAL <<< $(count_tasks_from_stdin "$STDIN_CONTENT")
    TASKS_DONE=0
    if [ "$TOTAL" -gt 0 ] && [ "$COMPLETED" -eq "$TOTAL" ]; then
        echo "  ✓ All tasks marked complete ($COMPLETED/$TOTAL)"
        TASKS_DONE=1
    elif [ "$TOTAL" -eq 0 ]; then
        echo "  ⊘ No task list detected (assuming complete)"
        TASKS_DONE=1
    else
        echo "  ✗ Tasks incomplete ($COMPLETED/$TOTAL)"
    fi

    # Gate: ALL heuristics must pass
    if [ "$TESTS_PASS" -eq 1 ] && [ "$GIT_CLEAN" -eq 1 ] && [ "$TASKS_DONE" -eq 1 ]; then
        echo "Ralph v2: Dual-condition gate passed. Stopping."
        jq --argjson cost "$CUMULATIVE_COST" --argjson completed "$COMPLETED" --argjson total "$TOTAL" \
            '.status = "complete" | .cumulative_cost = $cost | .completed_tasks = $completed | .total_tasks = $total' \
            "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
        exit 0
    else
        echo "Ralph v2: Signal detected but heuristics FAILED. Forcing continue with explanation."
        cat << EOF
{
  "decision": "block",
  "reason": "Ralph v2: You said you're complete, but verification failed. Tests: $([ $TESTS_PASS -eq 1 ] && echo 'PASS' || echo 'FAIL'), Git: $([ $GIT_CLEAN -eq 1 ] && echo 'clean' || echo 'dirty'), Tasks: $COMPLETED/$TOTAL. Fix these issues before stopping."
}
EOF
        exit 0
    fi
fi

# --- Check for explicit blockers (different from repeated errors) ---
BLOCKER_DETECTED=0
for signal in $(echo "$BLOCKER_SIGNALS" | tr ',' ' '); do
    if echo "$STDIN_CONTENT" | grep -qi "$signal"; then
        BLOCKER_DETECTED=1
        break
    fi
done

if [ "$BLOCKER_DETECTED" -eq 1 ] && [ "$ERROR_REPEAT_COUNT" -lt 2 ]; then
    echo "Ralph v2: Blocker detected (first occurrence). Stopping for review."
    jq --argjson cost "$CUMULATIVE_COST" '.status = "blocked" | .cumulative_cost = $cost' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
    exit 0
fi

# --- Check for progress (git commits) ---
CURRENT_COMMIT_HASH=$(git rev-parse HEAD 2>/dev/null || echo "no-git")

if [ "$CURRENT_COMMIT_HASH" = "$LAST_COMMIT_HASH" ]; then
    NO_PROGRESS_COUNT=$((NO_PROGRESS_COUNT + 1))
    echo "Ralph v2: No new commits (attempt $NO_PROGRESS_COUNT/$NO_PROGRESS_LIMIT)"
else
    NO_PROGRESS_COUNT=0
fi

# --- Safety: No progress circuit breaker ---
if [ "$NO_PROGRESS_COUNT" -ge "$NO_PROGRESS_LIMIT" ]; then
    echo "Ralph v2: No progress for $NO_PROGRESS_LIMIT iterations. Stopping."
    jq --argjson cost "$CUMULATIVE_COST" '.status = "no_progress" | .cumulative_cost = $cost' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
    exit 0
fi

# --- Update state with task tracking ---
read COMPLETED TOTAL <<< $(count_tasks_from_stdin "$STDIN_CONTENT")

jq \
    --argjson iter "$ITERATION" \
    --argjson npc "$NO_PROGRESS_COUNT" \
    --arg hash "$CURRENT_COMMIT_HASH" \
    --argjson cost "$CUMULATIVE_COST" \
    --arg errhash "$LAST_ERROR_HASH" \
    --argjson errcount "$ERROR_REPEAT_COUNT" \
    --argjson completed "$COMPLETED" \
    --argjson total "$TOTAL" \
    '.iteration = $iter | .no_progress_count = $npc | .last_commit_hash = $hash | .cumulative_cost = $cost | .last_error_hash = $errhash | .error_repeat_count = $errcount | .completed_tasks = $completed | .total_tasks = $total' \
    "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"

# --- Log progress with cost and tasks ---
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Iter $ITERATION/$MAX_ITERATIONS | Tasks: $COMPLETED/$TOTAL | Cost: \$${CUMULATIVE_COST} | Commits: $([ "$CURRENT_COMMIT_HASH" != "$LAST_COMMIT_HASH" ] && echo 'new' || echo 'none')" >> "$PROGRESS_FILE"

# --- Force continue ---
cat << EOF
{
  "decision": "block",
  "reason": "Ralph v2 iteration $ITERATION/$MAX_ITERATIONS (cost: \$${CUMULATIVE_COST}): Continue working. Tasks: $COMPLETED/$TOTAL complete. Check your plan and pick up the next incomplete task."
}
EOF
