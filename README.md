# cc_agents — Claude Code Multi-Agent Orchestration

Lean agent definitions for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Seven specialized agents, three team presets, quality gate hooks, accumulated skills, and an orchestrator guide — all designed for Opus 4.6's native orchestration capabilities.

**[View the Architecture Dashboard](docs/dashboard.html)**

## Design Principles

1. **Lean but complete.** Every line in an agent definition earns its place. Agents are 80-120 lines, not 500.
2. **Trust the model.** Opus 4.6 handles orchestration, tool selection, and error recovery natively. Agents add focused guidance, not capability.
3. **Tool-agnostic base.** Base agents work with standard Claude Code tools.
4. **Research by default.** Domain research is opt-out, not opt-in. A 5-minute research phase costs ~10K tokens; debugging domain gaps costs 10-50x that.
5. **Skills with zero context cost.** Reusable workflow skills loaded on demand via progressive disclosure. No tokens spent until the skill is needed.
6. **Test before deploy.** `init.sh` installs into a project for testing. Only promote to globals when proven.

## Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| **Scout** | Haiku | Codebase exploration, architecture discovery |
| **Research** | Sonnet | Deep technical research with citations and source hierarchy |
| **Planner** | Opus | Strategic planning, SMART task decomposition, risk assessment |
| **Builder** | Sonnet | Implementation with TDD, error recovery, checkpointing |
| **Reviewer** | Haiku | Code review against plan acceptance criteria |
| **Tester** | Sonnet | Test execution, failure analysis, fix task creation |
| **Research-Liaison** | Sonnet | Squeeze raw research output, route insights, update tracker |

## Pipeline

The full agent pipeline runs through five phases:

```
Pre-Flight → Discovery → Planning → Build → Review
(orchestrator)  (scout+research)  (planner)   (builder×N)  (reviewer)
    ~1min          ~3-5min          ~5min       ~10-30min     ~3min
                  (parallel)                   (1-8 parallel)
```

**Pre-Flight:** Before spawning agents, the orchestrator scouts the codebase, suggests tools that unlock autonomous operation, asks 2-3 targeted questions, and flags research needs.

**Proven scale:** 8 parallel builders produced ~5,800 lines in ~8 minutes with zero merge conflicts.

Run it with `/pipeline <task>` or configure manually with team presets.

## Team Presets

| Preset | Agents | Use When |
|--------|--------|----------|
| **Full Pipeline** | All 5 | Complex features requiring exploration, research, planning, and implementation |
| **Build-Review Loop** | Builder + Reviewer | Implementation with quality gates — build, review, fix until PASS |
| **Parallel Research** | Scout×N + Research×N → Planner | Discovery-heavy tasks needing multiple perspectives |

## Skills — Accumulated Expertise

Reusable workflow skills loaded on demand. Zero context cost until needed — only the skill name and description are visible until Claude loads the full instructions.

| Skill | What It Provides |
|-------|-----------------|
| **deep-research** | Orchestrate prompt → Gemini → squeeze → route pipeline |
| **chromadb** | Vector database patterns for RAG, semantic search, knowledge bases |
| **cozodb** | Knowledge graph patterns — GraphRAG, episodic memory, markdown ingestion |
| **playwright** | Browser automation for visual verification, testing, scraping |
| **google-drive** | Sync files between Google Drive and local directories via rclone |

Each skill includes install commands, common patterns, and gotchas. Bundled skills (like cozodb) include multiple linked files for progressive disclosure.

## Smarter Orchestration

Three modules that make the orchestrator proactively smarter:

| Module | What | Key Idea |
|--------|------|----------|
| **Toolbox** | [Tool catalog](docs/tool-catalog.md) for autonomous operation | Suggest Playwright, jq, Docker, etc. before starting — turns 5-min feedback loops into 25-min autonomous runs |
| **Pre-Flight Protocol** | Structured question framework | Scout code first, then ask max 2-3 questions with structured options. Three interruption tiers. |
| **Research Flagging** | Detect when research is needed | Domain complexity signals + decision tree. Research findings flow as constraints into builder tasks. |

See the [Orchestrator Guide](docs/orchestrator-guide.md) for full details.

## Cross-Project Communication

A shared mailbox pattern for coordinating between separate Claude Code instances in different projects.

- **Shared mailbox** at a known path acts as a message board between projects
- **SessionStart hook** checks for pending messages on every session start
- **Peek pattern** for read-only access to sibling project files
- **Signoff protocol** tracks message status: `pending` → `read` → `completed`

See [Cross-Project Patterns](docs/cross-project-patterns.md) for the full pattern.

## Deep Research Workflow

A structured workflow for leveraging external deep research tools (like Gemini Deep Research) and feeding results back into the agent pipeline.

```
Prompt → Ingest → Squeeze → Triage → PRD → Execute → Archive
```

Outputs route to one of four destinations: PRD for building, best practices docs, learning material, or topic files. Pre-written research prompts live in `research/prompts/`.

See [Deep Research Workflow](docs/deep-research-workflow.md) for the full pipeline.

## Quality Gates

Shell hooks that enforce quality during agent runs:

| Hook | Runs | Purpose |
|------|------|---------|
| `lint-gate.sh` | Before builder completes | Static analysis |
| `test-gate.sh` | After builder completes | Test suite validation |
| `review-gate.sh` | During review phase | Acceptance criteria check |

## Quick Start

### Install agents into a project
```bash
./init.sh ~/my-project                    # Base agents
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

## Using This In Your Projects

This is my personal agent setup. It works well for my workflow, but yours is different — different languages, frameworks, team size, and pain points. Here's how to make it yours.

### Option 1: Cherry-pick individual agents

Browse the `agents/` directory and copy just the ones you need into your project's `.claude/agents/`. A solo developer might only want `builder.md` and `tester.md`. A team lead might grab `planner.md` and `reviewer.md`.

### Option 2: Deploy everything and customize

```bash
git clone https://github.com/jonzo97/cc_agents.git
cd cc_agents
./init.sh ~/your-project --all
```

Then edit the agents in `~/your-project/.claude/agents/` to fit your workflow. Delete what you don't need, tweak what you keep.

### Option 3: Let Claude adapt it for you

Clone the repo and run `init.sh` to install the agents into your project. Then paste the prompt below into Claude Code **while in your project directory**. It will explore your codebase, ask you a few questions, and customize the agents to fit.

```bash
git clone https://github.com/jonzo97/cc_agents.git
cd cc_agents && ./init.sh ~/your-project --all
cd ~/your-project
```

Then paste this into Claude Code:

````
I have cc_agents installed in this project (.claude/agents/). I need you to adapt these
agents to fit THIS project. Here's what to do:

1. EXPLORE this project:
   - What language(s) and frameworks are used?
   - What's the test setup (framework, coverage, where do tests live)?
   - What build tools and CI/CD are in place?
   - How big is the codebase (rough file count, key directories)?
   - Are there existing patterns in CLAUDE.md or .claude/ config?

2. ASK ME these questions (wait for my answers before proceeding):
   - Do you typically work solo or with a team of agents? How many parallel builders
     make sense for your projects?
   - What are your biggest pain points — slow reviews, flaky tests, unclear plans,
     missing research?
   - Do you use any specialized tools (databases, browser testing, external APIs)
     that agents should know about?
   - Are there project conventions agents must follow (commit style, branch naming,
     test patterns, code style)?

3. Based on my answers, CUSTOMIZE the agents:
   - Remove agents I won't use (e.g., research-liaison for small projects)
   - Edit agent definitions in .claude/agents/ to reference this project's actual
     tech stack, test commands, and patterns
   - Adjust model tiers if needed (e.g., Haiku for simple projects, Opus for
     complex ones)
   - Update team presets to match my workflow
   - Remove skills I don't need, suggest new ones I might want

4. Generate a CLAUDE.md snippet (or update the existing one) with:
   - Project-specific agent guidance
   - Which agents to use for common tasks in this project
   - Any conventions agents should follow

Show me a summary of changes before applying them.
````

## Project Structure

```
cc_agents/
├── agents/                # Agent definitions (the deliverable)
│   ├── scout.md           # Codebase exploration
│   ├── research.md        # Technical research
│   ├── planner.md         # Task decomposition
│   ├── builder.md         # Implementation
│   ├── reviewer.md        # Code review
│   ├── tester.md          # Test execution & analysis
│   └── research-liaison.md # Research squeeze & routing
├── teams/                 # Team preset configurations
│   ├── full-pipeline.md
│   ├── build-review-loop.md
│   └── parallel-research.md
├── commands/              # Slash commands
│   ├── pipeline.md        # /pipeline orchestration
│   └── team-status.md     # /team-status monitoring
├── docs/                  # Reference documentation
│   ├── orchestrator-guide.md      # How to lead agent teams
│   ├── tool-catalog.md            # Tools for autonomous operation
│   ├── cross-project-patterns.md  # Multi-project coordination
│   ├── deep-research-workflow.md  # Research pipeline
│   └── dashboard.html             # Visual architecture overview
├── skills/                # Reusable workflow skills (zero context cost)
│   ├── deep-research/     # Research pipeline orchestration
│   ├── chromadb/          # Vector DB / RAG patterns
│   ├── cozodb/            # Knowledge graph patterns (bundled)
│   ├── playwright/        # Browser automation
│   └── google-drive/      # Google Drive sync via rclone
├── research/              # Deep research prompts and outputs
│   └── prompts/           # Pre-written research prompts
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

| Version | Highlights |
|---------|------------|
| **v4.3** | Recipes consolidated to skills, 7 agents (added tester + research-liaison), FAE skills brainstorm, Serena variants removed |
| **v4.2** | Smarter orchestration, recipes, cross-project patterns, deep research workflow |
| **v4.1** | Field test feedback — domain knowledge, smoke tests, orchestrator guide |
| **v4** | Research-driven agent rewrite for Opus 4.6. Team-aware agents, presets, Ralph v2, quality gates, pipeline command. |
| **v3** | 4 agents, 193 lines, lean for Opus 4.6 |
| **v2** | 6 agents, 5,697 lines, SQLite coordination, Serena LSP |
