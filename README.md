# cc_agents — Claude Code Multi-Agent Orchestration

Lean agent definitions for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Five specialized agents, three team presets, quality gate hooks, and an orchestrator guide — all designed for Opus 4.6's native orchestration capabilities.

**[View the Architecture Dashboard](docs/dashboard.html)**

## Design Principles

1. **Lean but complete.** Every line in an agent definition earns its place. Agents are 80-120 lines, not 500.
2. **Trust the model.** Opus 4.6 handles orchestration, tool selection, and error recovery natively. Agents add focused guidance, not capability.
3. **Tool-agnostic base.** Base agents work with standard Claude Code tools. Serena-enhanced variants available for LSP-enabled projects.
4. **Research by default.** Domain research is opt-out, not opt-in. A 5-minute research phase costs ~10K tokens; debugging domain gaps costs 10-50x that.
5. **Test before deploy.** `init.sh` installs into a project for testing. Only promote to globals when proven.

## Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| **Scout** | Haiku | Codebase exploration, architecture discovery |
| **Research** | Sonnet | Deep technical research with citations and source hierarchy |
| **Planner** | Opus | Strategic planning, SMART task decomposition, risk assessment |
| **Builder** | Sonnet | Implementation with TDD, error recovery, checkpointing |
| **Reviewer** | Haiku | Code review against plan acceptance criteria |

Scout, Builder, and Reviewer have **Serena variants** (`agents/serena/`) with LSP-powered semantic editing and analysis for projects with Serena configured.

## Pipeline

The full agent pipeline runs through five phases:

```
Pre-Flight → Discovery → Planning → Build → Review
(orchestrator)  (scout+research)  (planner)   (builder×N)  (reviewer)
    ~1min          ~3-5min          ~5min       ~10-30min     ~3min
                  (parallel)                   (1-8 parallel)
```

**Pre-Flight (v4.2):** Before spawning agents, the orchestrator scouts the codebase, suggests tools that unlock autonomous operation, asks 2-3 targeted questions, and flags research needs.

**Proven scale:** 8 parallel builders produced ~5,800 lines in ~8 minutes with zero merge conflicts.

Run it with `/pipeline <task>` or configure manually with team presets.

## Team Presets

| Preset | Agents | Use When |
|--------|--------|----------|
| **Full Pipeline** | All 5 | Complex features requiring exploration, research, planning, and implementation |
| **Build-Review Loop** | Builder + Reviewer | Implementation with quality gates — build, review, fix until PASS |
| **Parallel Research** | Scout×N + Research×N → Planner | Discovery-heavy tasks needing multiple perspectives |

## Quality Gates

Shell hooks that enforce quality during agent runs:

| Hook | Runs | Purpose |
|------|------|---------|
| `lint-gate.sh` | Before builder completes | Static analysis |
| `test-gate.sh` | After builder completes | Test suite validation |
| `review-gate.sh` | During review phase | Acceptance criteria check |

## v4.2 — Smarter Orchestration

Three modules that make the orchestrator proactively smarter:

| Module | What | Key Idea |
|--------|------|----------|
| **Toolbox** | [Tool catalog](docs/tool-catalog.md) for autonomous operation | Suggest Playwright, jq, Docker, etc. before starting — turns 5-min feedback loops into 25-min autonomous runs |
| **Pre-Flight Protocol** | Structured question framework | Scout code first, then ask max 2-3 questions with structured options. Three interruption tiers. |
| **Research Flagging** | Detect when research is needed | Domain complexity signals + decision tree. Research findings flow as constraints into builder tasks. |

See the [Orchestrator Guide](docs/orchestrator-guide.md) for full details.

## Quick Start

### Install agents into a project
```bash
./init.sh ~/my-project                    # Base agents
./init.sh ~/my-project --serena           # With Serena LSP variants
./init.sh ~/my-project --dry-run          # Preview changes
./init.sh ~/my-project --remove           # Revert to defaults
```

### Deploy to global defaults
```bash
./deploy.sh                    # Deploy all agents, hooks, commands, presets
./deploy.sh --dry-run --all    # Preview everything
./deploy.sh --clean            # Remove stale agents from target
```

### Run the pipeline
```
/pipeline Build a REST API with auth and tests
/pipeline plan-only Refactor the database layer
```

## Project Structure

```
cc_agents/
├── agents/                # Agent definitions (the deliverable)
│   ├── scout.md           # Codebase exploration
│   ├── research.md        # Technical research
│   ├── planner.md         # Task decomposition
│   ├── builder.md         # Implementation
│   ├── reviewer.md        # Code review
│   └── serena/            # LSP-enhanced variants
│       ├── scout.md
│       ├── builder.md
│       └── reviewer.md
├── teams/                 # Team preset configurations
│   ├── full-pipeline.md
│   ├── build-review-loop.md
│   └── parallel-research.md
├── commands/              # Slash commands
│   ├── pipeline.md        # /pipeline orchestration
│   └── team-status.md     # /team-status monitoring
├── docs/                  # Reference documentation
│   ├── orchestrator-guide.md   # How to lead agent teams
│   ├── tool-catalog.md         # Tools for autonomous operation
│   └── dashboard.html          # Visual architecture overview
├── hooks/                 # Quality gate hooks
│   ├── lint-gate.sh
│   ├── test-gate.sh
│   └── review-gate.sh
├── ralph/                 # Autonomous iteration loop (Stop Hook)
├── deploy.sh              # Deploy to ~/.claude/agents/
├── init.sh                # Install into a project for testing
└── test_scenarios/        # Sample codebases for validation
```

## How Agent Resolution Works

Claude Code resolves agents with project-level overrides:

```
~/.claude/agents/              ← global defaults (deploy.sh writes here)
~/my-project/.claude/agents/   ← project overrides (init.sh writes here)
```

Projects with `init.sh` applied use experimental agents. Without it, they fall back to global defaults.

## Version History

| Version | Date | Highlights |
|---------|------|------------|
| **v4.2** | Feb 2026 | Smarter orchestration: toolbox, pre-flight protocol, research flagging |
| **v4.1** | Feb 2026 | Field test feedback — domain knowledge, smoke tests, orchestrator guide |
| **v4.5** | Feb 2026 | Team-aware agents, presets, Ralph v2, quality gates, pipeline command |
| **v4** | Feb 2026 | Research-driven agent rewrite for Opus 4.6 |
| **v3** | Feb 2026 | 4 agents, 193 lines, lean for Opus 4.6 |
| **v2** | Oct 2025 | 6 agents, 5,697 lines, SQLite coordination, Serena LSP |
