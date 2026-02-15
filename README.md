# cc_agents — Claude Code Agent R&D

Template repo for Claude Code agent definitions. Experimental agents are developed here, then deployed into individual projects via `init.sh`.

## Architecture

```
~/.claude/agents/              ← vanilla defaults (global fallback)
~/cc_agents/                   ← this repo (R&D + template)
   └── init.sh <project>       ← copies experimental agents into project

~/my-project/.claude/agents/   ← experimental overrides (project-level)
```

**How it works:** Claude Code resolves agents with a clear precedence — project-level `.claude/agents/` overrides global `~/.claude/agents/`. So:

- Projects WITHOUT `init.sh` applied → use vanilla global agents
- Projects WITH `init.sh` applied → use experimental agents from this repo
- To revert → `init.sh <project> --remove` (falls back to vanilla)

This is the standard community pattern for sharing Claude Code configurations (see: serpro69/claude-starter-kit, davila7/claude-code-templates).

## Agents (v3 — Opus 4.6 Era)

| Agent | Model | Purpose | Lines |
|-------|-------|---------|-------|
| **scout** | Sonnet | Codebase exploration, architecture discovery | ~50 |
| **research** | Sonnet | Technical research with citations | ~50 |
| **planner** | Opus | Strategic planning, task decomposition | ~50 |
| **builder** | Sonnet | Implementation with TDD workflow | ~50 |

**Removed from v2 (now handled natively by Claude):**
- Orchestrator — Opus 4.6 does this natively via Task tool
- Context Manager — `/compact` skill handles this
- Constraint Generator — moved to tcl_monster (project-specific)

## Usage

### Initialize a project with experimental agents
```bash
./init.sh ~/some-project           # Install
./init.sh ~/some-project --dry-run # Preview
./init.sh ~/some-project --remove  # Revert to vanilla
```

### Promote experimental → vanilla globals
```bash
./deploy.sh           # Copy agents to ~/.claude/agents/
./deploy.sh --dry-run # Preview
```

### Workflow
```
1. Edit agents in cc_agents/agents/*.md
2. Test: ./init.sh ~/test-project → run Claude Code there
3. Iterate until satisfied
4. Promote: ./deploy.sh → updates vanilla globals
5. Commit both repos
```

## Git Repositories

| Repo | Location | GitHub | Purpose |
|------|----------|--------|---------|
| **cc_agents** | `~/cc_agents` | `jonzo97/cc_agents` | Agent R&D, template, testing |
| **.claude** | `~/.claude` | `jonzo97/.claude` | Production runtime (vanilla agents, skills, hooks) |

**cc_agents** is the source of truth for agent definitions. Vanilla globals in `~/.claude/agents/` are updated via `deploy.sh` when experimental agents are proven.

## File Structure

```
cc_agents/
├── agents/           # Agent definitions (the deliverable)
│   ├── scout.md
│   ├── research.md
│   ├── planner.md
│   └── builder.md
├── init.sh           # Install agents into a project's .claude/
├── deploy.sh         # Promote agents to ~/.claude/agents/ (vanilla globals)
├── HANDOFF_PROMPT.md # Session handoff for continuing R&D
├── test_scenarios/   # 5 sample codebases for validation
└── archive/v2/       # Historical reference (old 6-agent system)
```

## History

- **v1** (2024) — Initial agent system
- **v2** (Oct 2025) — 6 agents, 5,697 lines, SQLite coordination, Serena LSP
- **v3** (Feb 2026) — 4 agents, 193 lines, lean for Opus 4.6, template-based deployment
