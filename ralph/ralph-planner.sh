#!/usr/bin/env bash
# ralph-planner.sh — Three-phase autonomous development orchestrator
#
# Phase 1: Requirements refinement (max iterations configurable)
#   - Claude refines requirements, asks clarifying questions
#   - Stops when requirements doc is written to .ralph-requirements.md
#
# Phase 2: Planning (max iterations configurable)
#   - Claude creates implementation plan from requirements
#   - Stops when plan is written and tasks created via TodoWrite
#
# Phase 3: Building via ralph-v2.sh loop
#   - Hands off to ralph-v2.sh for implementation
#   - All v2 safety features apply

set -euo pipefail

# --- Configuration ---
PHASE_1_MAX_ITERATIONS="${RALPH_PHASE1_MAX_ITERATIONS:-5}"
PHASE_2_MAX_ITERATIONS="${RALPH_PHASE2_MAX_ITERATIONS:-5}"
REQUIREMENTS_FILE="${RALPH_REQUIREMENTS_FILE:-.ralph-requirements.md}"
PLAN_FILE="${RALPH_PLAN_FILE:-.ralph-plan.md}"
STATE_FILE=".ralph-planner-state.json"

# --- Usage ---
usage() {
    cat << EOF
Usage: $0 --phase <1|2|3|all> [initial_prompt]

Phases:
  1     Requirements refinement (outputs $REQUIREMENTS_FILE)
  2     Planning (outputs $PLAN_FILE and TodoWrite tasks)
  3     Building (runs ralph-v2.sh loop)
  all   Sequential execution of phases 1→2→3

Environment variables:
  RALPH_PHASE1_MAX_ITERATIONS (default: 5)
  RALPH_PHASE2_MAX_ITERATIONS (default: 5)
  RALPH_REQUIREMENTS_FILE (default: .ralph-requirements.md)
  RALPH_PLAN_FILE (default: .ralph-plan.md)

Examples:
  $0 --phase 1 "Build a REST API for user management"
  $0 --phase all "Build a REST API"
  $0 --phase 2  # Assumes requirements exist
EOF
    exit 1
}

# --- Parse arguments ---
PHASE=""
INITIAL_PROMPT=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --phase)
            PHASE="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            INITIAL_PROMPT="$INITIAL_PROMPT $1"
            shift
            ;;
    esac
done

if [ -z "$PHASE" ]; then
    echo "Error: --phase argument required"
    usage
fi

INITIAL_PROMPT=$(echo "$INITIAL_PROMPT" | xargs)  # Trim whitespace

# --- Initialize state file ---
if [ ! -f "$STATE_FILE" ]; then
    cat > "$STATE_FILE" << 'INIT'
{
  "phase_1_iteration": 0,
  "phase_2_iteration": 0,
  "phase_1_status": "not_started",
  "phase_2_status": "not_started",
  "phase_3_status": "not_started"
}
INIT
fi

# --- Phase 1: Requirements Refinement ---
run_phase_1() {
    echo "=== Ralph Planner: Phase 1 - Requirements Refinement ==="

    if [ -f "$REQUIREMENTS_FILE" ] && [ -s "$REQUIREMENTS_FILE" ]; then
        echo "Requirements file already exists: $REQUIREMENTS_FILE"
        echo "Skipping Phase 1. Delete file to re-run."
        jq '.phase_1_status = "complete"' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
        return 0
    fi

    local iteration=0
    local prompt="$INITIAL_PROMPT"

    if [ -z "$prompt" ]; then
        echo "Error: Initial prompt required for Phase 1"
        exit 1
    fi

    while [ "$iteration" -lt "$PHASE_1_MAX_ITERATIONS" ]; do
        iteration=$((iteration + 1))
        echo "[Phase 1, Iteration $iteration/$PHASE_1_MAX_ITERATIONS]"

        jq --argjson iter "$iteration" '.phase_1_iteration = $iter | .phase_1_status = "running"' \
            "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"

        # Run Claude
        if [ "$iteration" -eq 1 ]; then
            claude "$prompt

You are in Phase 1 (Requirements Refinement) of a three-phase autonomous development process.

Your task: Refine requirements by asking clarifying questions, exploring edge cases, and documenting assumptions.

When requirements are clear, write them to $REQUIREMENTS_FILE using this structure:
- Project goal
- Key features
- Acceptance criteria
- Constraints
- Assumptions

Say 'REQUIREMENTS_COMPLETE' when done."
        else
            claude "Continue refining requirements. Ask any remaining clarifying questions. When complete, write to $REQUIREMENTS_FILE and say REQUIREMENTS_COMPLETE."
        fi

        # Check completion signal
        if [ -f "$REQUIREMENTS_FILE" ] && [ -s "$REQUIREMENTS_FILE" ]; then
            echo "Requirements file detected: $REQUIREMENTS_FILE"
            jq '.phase_1_status = "complete"' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
            echo "=== Phase 1 Complete ==="
            return 0
        fi

        # Safety check
        if [ "$iteration" -ge "$PHASE_1_MAX_ITERATIONS" ]; then
            echo "Phase 1: Max iterations reached without completion"
            jq '.phase_1_status = "incomplete"' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
            return 1
        fi
    done
}

# --- Phase 2: Planning ---
run_phase_2() {
    echo "=== Ralph Planner: Phase 2 - Planning ==="

    if [ ! -f "$REQUIREMENTS_FILE" ]; then
        echo "Error: Requirements file not found. Run Phase 1 first."
        exit 1
    fi

    if [ -f "$PLAN_FILE" ] && [ -s "$PLAN_FILE" ]; then
        echo "Plan file already exists: $PLAN_FILE"
        echo "Skipping Phase 2. Delete file to re-run."
        jq '.phase_2_status = "complete"' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
        return 0
    fi

    local iteration=0

    while [ "$iteration" -lt "$PHASE_2_MAX_ITERATIONS" ]; do
        iteration=$((iteration + 1))
        echo "[Phase 2, Iteration $iteration/$PHASE_2_MAX_ITERATIONS]"

        jq --argjson iter "$iteration" '.phase_2_iteration = $iter | .phase_2_status = "running"' \
            "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"

        # Run Claude
        if [ "$iteration" -eq 1 ]; then
            claude "You are in Phase 2 (Planning) of a three-phase autonomous development process.

Requirements are documented in: $REQUIREMENTS_FILE

Your task:
1. Read the requirements
2. Create a detailed implementation plan
3. Break down into concrete, actionable tasks
4. Write plan to $PLAN_FILE
5. Create tasks using TodoWrite with time estimates
6. Say 'PLAN_COMPLETE' when done

The plan should include:
- Architecture overview
- File structure
- Implementation order
- Testing strategy
- Success criteria"
        else
            claude "Continue planning. Write the plan to $PLAN_FILE, create TodoWrite tasks, and say PLAN_COMPLETE when done."
        fi

        # Check completion signal
        if [ -f "$PLAN_FILE" ] && [ -s "$PLAN_FILE" ]; then
            echo "Plan file detected: $PLAN_FILE"
            jq '.phase_2_status = "complete"' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
            echo "=== Phase 2 Complete ==="
            return 0
        fi

        # Safety check
        if [ "$iteration" -ge "$PHASE_2_MAX_ITERATIONS" ]; then
            echo "Phase 2: Max iterations reached without completion"
            jq '.phase_2_status = "incomplete"' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
            return 1
        fi
    done
}

# --- Phase 3: Building ---
run_phase_3() {
    echo "=== Ralph Planner: Phase 3 - Building ==="

    if [ ! -f "$PLAN_FILE" ]; then
        echo "Error: Plan file not found. Run Phase 2 first."
        exit 1
    fi

    jq '.phase_3_status = "running"' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"

    # Check if ralph-v2.sh exists
    RALPH_V2_PATH="$(dirname "$0")/ralph-v2.sh"
    if [ ! -f "$RALPH_V2_PATH" ]; then
        echo "Error: ralph-v2.sh not found at $RALPH_V2_PATH"
        exit 1
    fi

    # Delegate to ralph-v2.sh via Stop Hook
    echo "Starting ralph-v2.sh autonomous loop..."
    echo "Install as Stop Hook in .claude/settings.json to enable autonomous iteration"
    echo ""
    echo "Suggested command:"
    echo "claude 'Implement the tasks in $PLAN_FILE. Work through each task sequentially, following the acceptance criteria. When all tasks are complete and tests pass, say RALPH_COMPLETE.'"

    jq '.phase_3_status = "delegated"' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
}

# --- Main orchestration ---
case "$PHASE" in
    1)
        run_phase_1
        ;;
    2)
        run_phase_2
        ;;
    3)
        run_phase_3
        ;;
    all)
        echo "=== Ralph Planner: Running all phases sequentially ==="
        run_phase_1 || exit 1
        echo ""
        echo "Phase 1 complete. Press Enter to continue to Phase 2, or Ctrl+C to stop."
        read -r

        run_phase_2 || exit 1
        echo ""
        echo "Phase 2 complete. Press Enter to continue to Phase 3, or Ctrl+C to stop."
        read -r

        run_phase_3
        ;;
    *)
        echo "Error: Invalid phase '$PHASE'. Must be 1, 2, 3, or all"
        usage
        ;;
esac
