# cc_agents — Claude Code Agent R&D

Template repo for Claude Code agent definitions. Experimental agents are developed here, tested via `init.sh`, then promoted to vanilla globals via `deploy.sh`.

## Design Principles

1. **Lean but complete.** Every line in an agent definition earns its place. No ceremony, no dead code, no over-engineering.
2. **Tool-agnostic base.** Base agents work with standard Claude Code tools. Serena-enhanced variants available for LSP-enabled projects.
3. **Trust the model.** Opus 4.6 handles orchestration, tool selection, and error recovery natively. Agents add focused guidance, not capability.
4. **Test before deploy.** init.sh installs into a project for testing. Only promote to vanilla globals when proven.

## Agents (v4 — Feb 2026)

### Base Agents (`agents/`)

| Agent | Model | Purpose | Lines |
|-------|-------|---------|-------|
| **scout** | Haiku | Codebase exploration, architecture discovery | ~73 |
| **research** | Sonnet | Technical research with citations and source hierarchy | ~73 |
| **planner** | Opus | Strategic planning, SMART task decomposition, risk assessment | ~78 |
| **builder** | Sonnet | Implementation with TDD, error recovery, checkpointing | ~77 |
| **reviewer** | Haiku | Code review against plan acceptance criteria (read-only) | ~72 |

### Serena Variants (`agents/serena/`)

Enhanced versions for projects with Serena LSP configured. These override the base agents for code-heavy work:

| Agent | Additions over base |
|-------|-------------------|
| **scout** | `get_symbols_overview`, `find_symbol` for semantic code analysis |
| **builder** | `replace_symbol_body`, `insert_after_symbol`, `find_referencing_symbols` for precise edits |
| **reviewer** | `find_symbol` for targeted review, `find_referencing_symbols` for impact checking |

### Ralph Builder (`ralph/`)

Autonomous iteration loop using Claude Code's Stop Hook. Keeps the builder working until all tasks pass or safety limits are reached. See [ralph/README.md](ralph/README.md).

## Architecture

```
~/.claude/agents/              <- vanilla defaults (global fallback)
~/cc_agents/                   <- this repo (R&D + template)
   ├── init.sh <project>       <- install experimental agents into project
   ├── init.sh <project> --serena  <- install Serena variants
   └── deploy.sh               <- promote to vanilla globals

~/my-project/.claude/agents/   <- experimental overrides (project-level)
```

**How it works:** Claude Code resolves agents with project-level `.claude/agents/` overriding global `~/.claude/agents/`. So:

- Projects WITHOUT `init.sh` applied -> use vanilla global agents
- Projects WITH `init.sh` applied -> use experimental agents from this repo
- To revert -> `init.sh <project> --remove` (falls back to vanilla)

## Usage

### Initialize a project with experimental agents
```bash
./init.sh ~/some-project                  # Install base agents
./init.sh ~/some-project --serena         # Install Serena-enhanced variants
./init.sh ~/some-project --dry-run        # Preview
./init.sh ~/some-project --remove         # Revert to vanilla
```

### Promote experimental -> vanilla globals
```bash
./deploy.sh                    # Deploy base agents
./deploy.sh --serena           # Deploy with Serena variants
./deploy.sh --clean            # Remove stale agents from target
./deploy.sh --dry-run          # Preview
```

### Workflow
```
1. Edit agents in cc_agents/agents/*.md
2. Test: ./init.sh ~/test-project -> run Claude Code there
3. Iterate until satisfied
4. Promote: ./deploy.sh -> updates vanilla globals
5. Commit both repos (cc_agents + ~/.claude)
```

## Git Repositories

| Repo | Location | GitHub | Purpose |
|------|----------|--------|---------|
| **cc_agents** | `~/cc_agents` | `jonzo97/cc_agents` | Agent R&D, template, testing |
| **.claude** | `~/.claude` | `jonzo97/.claude` | Production runtime (vanilla agents, skills, hooks) |

## File Structure

```
cc_agents/
├── agents/               # Base agent definitions
│   ├── scout.md
│   ├── research.md
│   ├── planner.md
│   ├── builder.md
│   ├── reviewer.md
│   └── serena/           # Serena LSP-enhanced variants
│       ├── scout.md
│       ├── builder.md
│       └── reviewer.md
├── ralph/                # Autonomous iteration loop
│   ├── ralph-builder.sh
│   └── README.md
├── init.sh               # Install agents into a project
├── deploy.sh             # Promote agents to vanilla globals
├── FUTURE_IMPROVEMENTS.md # Brainstorming and roadmap
├── HANDOFF_PROMPT.md     # Session handoff for continuing R&D
├── test_scenarios/       # 5 sample codebases for validation
└── archive/v2/           # Historical reference (old 6-agent system)
```

## Skills Deprecation Notes

These skills at `~/.claude/skills/` overlap with native Claude Code features:

| Skill | Status | Reason |
|-------|--------|--------|
| **agent-launcher** | DEPRECATE | Task tool is native — no need for a skill to spawn agents |
| **context-management** | DEPRECATE | PreCompact/SessionStart hooks handle this; Memory Bank in CLAUDE.md is more comprehensive |
| **skill-builder** | KEEP | Still useful for creating new skills |

## History

- **v1** (2024) — Initial agent system
- **v2** (Oct 2025) — 6 agents, 5,697 lines, SQLite coordination, Serena LSP
- **v3** (Feb 2026) — 4 agents, 193 lines, lean for Opus 4.6
- **v4** (Feb 2026) — 5 base + 3 Serena variants + Ralph, ~370 lines base, research-driven rewrite
