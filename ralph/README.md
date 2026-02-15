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

## References

- [snarktank/ralph](https://github.com/snarktank/ralph) — Original community implementation
- [frankbria/ralph-claude-code](https://github.com/frankbria/ralph-claude-code) — Enhanced version with smart exit detection
- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks) — Official docs
