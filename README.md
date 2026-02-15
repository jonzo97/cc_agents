# cc_agents — Claude Code Agent R&D

Agent definitions for Claude Code's Task tool system. This is the development/experimentation repo — tested agents get deployed to `~/.claude/agents/` via `./deploy.sh`.

## Architecture (Opus 4.6 Era)

The main Claude instance IS the orchestrator. No separate orchestrator agent needed. The Task tool handles agent spawning natively.

**4 agents:**

| Agent | Model | Purpose | Lines |
|-------|-------|---------|-------|
| **scout** | Sonnet | Codebase exploration, architecture discovery | ~60 |
| **research** | Sonnet | Technical research with citations | ~55 |
| **planner** | Opus | Strategic planning, task decomposition | ~55 |
| **builder** | Sonnet | Implementation with TDD workflow | ~60 |

**Removed from v2 (now handled natively by Claude):**
- Orchestrator — Opus 4.6 does this natively
- Context Manager — `/compact` skill handles this
- SQLite coordination DB — unnecessary overhead
- Handoff protocol schemas — Task tool handles communication

## Usage

### In any Claude Code session:
```
"Scout this project and tell me about the architecture"
→ Claude spawns scout agent via Task tool

"Research React Server Components best practices"
→ Claude spawns research agent via Task tool

"Plan the implementation for adding auth"
→ Claude spawns planner agent via Task tool

"Build the auth feature following the approved plan"
→ Claude spawns builder agent via Task tool
```

Claude decides when to use which agent based on the request. No explicit orchestration needed.

### Deploy to production:
```bash
./deploy.sh --dry-run  # Preview changes
./deploy.sh            # Copy agents to ~/.claude/agents/
```

## Development

Edit agents in `agents/`. Test by running Claude Code sessions. When satisfied, deploy.

### Testing
The `test_scenarios/` directory has 5 sample codebases for validation:
- `simple_cli` — Node.js CLI
- `react_library` — React + TypeScript
- `max_plugin` — Max for Live MIDI plugin
- `legacy_codebase` — AngularJS 1.5
- `empty_project` — Greenfield

### History
The `archive/v2/` directory contains the full v2 system (6 agents, 5,697 lines, SQLite coordination, 7,700+ lines of docs) for reference.

## Repo Relationship

```
cc_agents (this repo)     →  R&D, experimentation, testing
    ↓ deploy.sh
~/.claude/agents/ (.claude repo)  →  Production runtime
```
