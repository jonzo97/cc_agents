# Ralph Builder — Autonomous Iteration Loop

Ralph is an autonomous development pattern that uses Claude Code's **Stop Hook** to keep the builder agent working until all tasks are complete or safety limits are reached.

Named after the [Ralph Wiggum pattern](https://github.com/snarktank/ralph) popularized in the Claude Code community.

## How It Works

1. You give Claude a plan with tasks and acceptance criteria
2. Claude works through tasks, attempting to complete them
3. When Claude tries to stop, the **Stop Hook** fires
4. The hook checks: are all tasks done? Did Claude make progress?
5. If not done and still making progress, it forces Claude to continue
6. Safety limits prevent infinite loops (max iterations, no-progress circuit breaker)

## Quick Start

### 1. Copy the hook script

```bash
cp ralph/ralph-builder.sh /path/to/your-project/.claude/hooks/
chmod +x /path/to/your-project/.claude/hooks/ralph-builder.sh
```

### 2. Configure the Stop Hook

Add to your project's `.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/ralph-builder.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### 3. Run Claude with a plan

```bash
claude "Implement the tasks in the approved plan. Work through each task sequentially. When all tasks are complete and tests pass, say RALPH_COMPLETE."
```

## Configuration

Environment variables control behavior:

| Variable | Default | Description |
|----------|---------|-------------|
| `RALPH_MAX_ITERATIONS` | 15 | Maximum loop iterations before forced stop |
| `RALPH_NO_PROGRESS_LIMIT` | 3 | Stop after N iterations with no git commits |
| `RALPH_PROGRESS_FILE` | `.ralph-progress.log` | Log file for iteration history |
| `RALPH_STATE_FILE` | `.ralph-state.json` | State tracking between iterations |

## Safety Features

- **Max iterations:** Hard cap prevents runaway loops (default: 15)
- **No-progress circuit breaker:** Stops if no git commits for 3 consecutive iterations
- **Blocker detection:** Stops if Claude reports an escalation or blocker
- **Completion signal:** Stops when Claude outputs "RALPH_COMPLETE" or "all tasks complete"

## State Files

Ralph creates two files in your project root (add to `.gitignore`):

- `.ralph-state.json` — Current iteration count, progress tracking
- `.ralph-progress.log` — Timestamped log of each iteration

## Completion Signals

The hook stops the loop when it detects any of these in Claude's output:

- `RALPH_COMPLETE` — explicit completion marker
- `all tasks complete` — natural language completion
- `all acceptance criteria met` — criteria-based completion
- `escalat` / `blocker` / `cannot proceed` — builder escalating a problem

## Integration with cc_agents

Ralph works best with the **builder agent**:

1. Use the **planner agent** to create a detailed plan with acceptance criteria
2. Start Ralph with the builder agent working through the plan
3. The builder's checkpoint protocol (every 3 tasks) ensures quality
4. The builder's error recovery protocol (2 retries then escalate) triggers Ralph's blocker detection

## Limitations

- Each iteration is a fresh Claude context — state persists only through files and git
- Token consumption scales with iterations (monitor your usage)
- Not suitable for tasks that require human decision points mid-execution
- Stop Hook mechanism may vary across Claude Code versions

## Ralph v2

Ralph v2 is an enhanced version with production-grade safety features and heuristic validation.

### What's New vs v1

**Dual-Condition Exit Gate:**
- v1: Stops when Claude says "complete" (trusted signal only)
- v2: Requires BOTH completion signal AND heuristic verification
  - Heuristics: tests pass, git clean, all tasks marked done
  - If signal detected but heuristics fail, forces continue with explanation

**Cost Tracking:**
- Track cumulative cost per iteration
- Budget enforcement (stop when limit exceeded)
- Cost visibility in progress logs

**Repeated-Error Circuit Breaker:**
- Detects when same error appears 2x consecutively
- Uses error message hashing for comparison
- Different from generic no-progress check (targets error loops)

**Task-Aware Progress:**
- Parses TodoWrite task lists from Claude's output
- Tracks completed vs total tasks in state
- Reports task progress in logs and continue prompts

**Configurable Signals:**
- Exit signals via `RALPH_EXIT_SIGNALS` env var
- Blocker signals via `RALPH_BLOCKER_SIGNALS` env var
- Customizable per project needs

### Configuration (v2-specific)

| Variable | Default | Description |
|----------|---------|-------------|
| `RALPH_COST_BUDGET` | (empty = unlimited) | Stop when cumulative cost exceeds budget |
| `RALPH_COST_PER_ITERATION` | 0.50 | Estimated cost per iteration in dollars |
| `RALPH_EXIT_SIGNALS` | (see below) | Comma-separated completion signals |
| `RALPH_BLOCKER_SIGNALS` | (see below) | Comma-separated blocker signals |
| `RALPH_PROGRESS_FILE` | `.ralph-v2-progress.log` | v2 progress log (separate from v1) |
| `RALPH_STATE_FILE` | `.ralph-v2-state.json` | v2 state file (separate from v1) |

**Default exit signals:** `RALPH_COMPLETE,all tasks complete,all acceptance criteria met`

**Default blocker signals:** `escalat,blocker,cannot proceed,giving up`

### Quick Start (v2)

```bash
# Copy v2 script
cp ralph/ralph-v2.sh /path/to/your-project/.claude/hooks/
chmod +x /path/to/your-project/.claude/hooks/ralph-v2.sh

# Configure Stop Hook with v2 script
# Edit .claude/settings.json:
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/ralph-v2.sh",
        "timeout": 30
      }]
    }]
  }
}

# Set cost budget (optional)
export RALPH_COST_BUDGET=5.00

# Run with plan
claude "Implement tasks in plan. Say RALPH_COMPLETE when done and all tests pass."
```

### Ralph Planner — Three-Phase Orchestration

The `ralph-planner.sh` script orchestrates the full development lifecycle:

**Phase 1: Requirements Refinement**
- Claude asks clarifying questions
- Explores edge cases and constraints
- Outputs `.ralph-requirements.md`
- Max 5 iterations (configurable)

**Phase 2: Planning**
- Reads requirements
- Creates detailed implementation plan
- Breaks down into TodoWrite tasks
- Outputs `.ralph-plan.md`
- Max 5 iterations (configurable)

**Phase 3: Building**
- Delegates to `ralph-v2.sh` autonomous loop
- All v2 safety features apply
- Implements plan tasks sequentially

### Quick Start (Planner)

```bash
# Run all phases sequentially
./ralph/ralph-planner.sh --phase all "Build a REST API for user management"

# Or run phases individually
./ralph/ralph-planner.sh --phase 1 "Build a REST API"  # Requirements
./ralph/ralph-planner.sh --phase 2                      # Planning (reads requirements)
./ralph/ralph-planner.sh --phase 3                      # Building (reads plan)

# Configure max iterations per phase
export RALPH_PHASE1_MAX_ITERATIONS=3
export RALPH_PHASE2_MAX_ITERATIONS=5
```

### State Files (v2)

Ralph v2 creates separate state files to avoid conflicts with v1:

- `.ralph-v2-state.json` — Iteration, cost, error tracking, task counts
- `.ralph-v2-progress.log` — Timestamped iteration log with cost/tasks
- `.ralph-planner-state.json` — Phase tracking (if using planner)
- `.ralph-requirements.md` — Requirements doc (phase 1 output)
- `.ralph-plan.md` — Implementation plan (phase 2 output)

Add to `.gitignore`:
```
.ralph*.json
.ralph*.log
.ralph-requirements.md
.ralph-plan.md
```

### Dual-Condition Gate Example

```
Claude outputs: "All tasks complete! Tests passing. Ready to ship."

Ralph v2 checks:
  ✓ Completion signal detected ("all tasks complete")
  Running heuristics...
    ✓ Tests pass (pytest)
    ✗ Git has uncommitted changes
    ✓ All tasks marked complete (5/5)

Gate: FAILED (git dirty)
Decision: Force continue with explanation

Output:
{
  "decision": "block",
  "reason": "You said you're complete, but verification failed.
             Tests: PASS, Git: dirty, Tasks: 5/5.
             Commit your changes before stopping."
}
```

## References

- [snarktank/ralph](https://github.com/snarktank/ralph) — Original community implementation
- [frankbria/ralph-claude-code](https://github.com/frankbria/ralph-claude-code) — Enhanced version with smart exit detection
- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks) — Official docs
