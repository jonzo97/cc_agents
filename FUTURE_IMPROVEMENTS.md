# Future Improvements — Brainstorming

Ideas for improving cc_agents, informed by deep research (Feb 2026). See `docs/RESEARCH_SYNTHESIS.md` for full findings.

## High Priority — Implement Next

### Agent Teams Integration
Native multi-agent coordination is the biggest capability unlock in Opus 4.6.
- **Team-aware agents** — Agents that can coordinate via TeamCreate/SendMessage when spawned as teammates
- **Parallel scout+research** — Scout explores codebase while research investigates technologies simultaneously
- **Builder+reviewer pipeline** — Builder implements, reviewer verifies, loop until all criteria pass
- **Competing hypotheses pattern** — Multiple agents investigate different root causes, debate findings
- **Pipeline pattern** — Tasks auto-unblock when dependencies complete via `addBlockedBy`
- **Reference:** [Agent Teams Docs](https://code.claude.com/docs/en/agent-teams), [$20K C compiler case study](https://github.com/anthropics/claudes-c-compiler)

### Ralph Enhancements
Current prototype is functional but primitive vs. what's possible.
- **Fresh Context Pattern** — Spawn fresh Claude session per iteration, state via git/files only. Prevents context rot over long sessions.
- **Smart exit detection** — Dual-condition gate (explicit signal + heuristic indicators) per [frankbria/ralph-claude-code](https://github.com/frankbria/ralph-claude-code)
- **Circuit breaker improvements** — Semantic response analysis, auto-recovery, rate limiting
- **Parallel worktree Ralph** — Multiple Ralph loops on isolated git worktrees (L-thread/P-thread/B-thread taxonomy)
- **Three-phase architecture** — Requirements → Planning → Building, not just building
- **Cost monitoring** — Track token consumption per iteration, abort if over budget (50 iterations ~$50-100)
- **Backpressure pattern** — Engineer environments where wrong outputs get rejected automatically (tests, linters, formatters)

### Effort-Based Agent Hierarchy
Opus 4.6's effort parameter enables cost optimization without model switching.
```
Main Orchestrator: high effort (quality decisions)
├── Scout: medium effort (balance speed/thoroughness)
├── Research: high effort (thorough findings)
├── Planner: high effort (reliable plans)
├── Builder: low effort (speed for focused tasks)
└── Reviewer: low effort (fast verification)
```
- **Dynamic escalation** — Start at `low`, auto-escalate to `high` on test failures or ambiguity
- **At `medium`, Opus 4.6 matches Sonnet 4.5's SWE-bench using 76% fewer tokens**
- **Reference:** [Effort Parameter Docs](https://platform.claude.com/docs/en/build-with-claude/effort)

### Research Agent Improvements
- **Context budget enforcement** — Research must specify token budget, filter before exposing to context
- **Code execution for data processing** — Write Python to filter 100 search results locally, return only top 5
- **Source quality scoring** — Automatic detection of official docs vs blog posts
- **Research templates** — Pre-built sub-question sets for common tasks (library comparison, migration guide, etc.)
- **State persistence** — Save intermediate findings between rounds, aggregate final report
- **Reference:** [Programmatic Tool Calling](https://www.anthropic.com/engineering/advanced-tool-use)

## Medium Priority — Implement When Needed

### Stop Hook Quality Gates
Beyond Ralph's iteration loop.
- **Lint/type check gate** — Block completion on style violations
- **Test suite gate** — Prevent PR creation if tests fail
- **Auto-review gate** — Architecture/security checks that linters can't express
- **Multi-phase workflows** — Requirements → Implementation → Documentation, each gated by hooks
- **CI/CD integration** — PreToolUse hooks for PR gating, async execution for long checks
- **Reference:** [Quality Gates](https://blog.devgenius.io/claude-code-use-hooks-to-enforce-end-of-turn-quality-gates-5bed84e89a0d), [Auto-Reviewing](https://www.oreilly.com/radar/auto-reviewing-claudes-code/)

### Agent Skills with Progressive Disclosure
Three-level system for context-efficient custom workflows.
- **Level 1: Frontmatter** (always loaded) — Skill name and description only
- **Level 2: SKILL.md body** (loaded when relevant) — Full instructions, keep under 500 lines
- **Level 3: Linked files** (loaded on demand) — Reference docs, schemas, unbounded capacity
- **Reference:** [Equipping Agents with Skills (Anthropic)](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

### Hook-Driven Agent Triggering
- **PreToolUse hooks** — Automatically spawn reviewer before destructive operations
- **PostToolUse hooks** — Trigger scout after new file creation to update architecture map
- **Agent hooks** — Use subagent-based hook handlers for intelligent filtering
- **SubagentStop hooks** — Quality gate checks after subagent work completes

### RAG/Knowledge Augmentation
- **rag-cli** — Local RAG using Chroma vector embeddings for Claude Code ([ItMeDiaTech/rag-cli](https://github.com/ItMeDiaTech/rag-cli))
- **Project-specific knowledge bases** — Indexed docs, past decisions, codebase patterns
- **Cross-project memory** — MCP-based knowledge graph for patterns that apply across projects

### Skill-Agent Hybrid Patterns
- **Skills that spawn agents** — A skill sets up context then delegates to an agent
- **Agent results as skill triggers** — Scout findings automatically trigger relevant skills
- **Composable agent chains** — Define pipelines: scout → research → plan → build → review

## Low Priority / Exploratory

### Progressive Tool Discovery (When Scale Demands)
Currently unnecessary (<20 tools) but future-proofed.
- **Tool Search Tool** (`defer_loading`) — 85% token savings for 20-100 tools
- **Code Execution with MCP** — 98.7% savings for 100+ tools, requires sandboxing
- **Tool Use Examples** — 72%->90% accuracy for complex parameter handling
- **See:** [docs/PROGRESSIVE_TOOL_DISCOVERY.md](docs/PROGRESSIVE_TOOL_DISCOVERY.md)

### Trust & Verification (from Claude Flow proposals)
- **Trust scoring per agent** — Track success/failure rates, adjust autonomy based on performance
- **Cross-agent test verification** — Independent verification agent validates test claims
- **Coherence engine** — Detect contradictory changes across parallel agents before merge
- **Hallucination detection** — Flag fabricated paths, impossible claims, false test results

### Cost Monitoring Agent
- Track token consumption across agents
- Budget allocation per task
- Effort-aware cost dashboard
- Alert when approaching limits
- Historical cost analysis per agent type and effort level

### Documentation Agent
- Auto-generate docs from code changes
- Keep README/CHANGELOG updated
- Generate ADRs from significant decisions

### Testing Agent
- Specialized test writing beyond builder's TDD
- Mutation testing to verify test quality
- Coverage analysis and gap identification

### Domain-Specific Agent Templates
- FPGA agents (constraint-generator already exists for tcl_monster)
- Web development agents (frontend, API, database)
- Data science agents (notebook, pipeline, model evaluation)

## Rejected / Deferred

### Orchestrator Agent
- **Why rejected:** Opus 4.6 handles orchestration natively via Task tool. Adding a separate orchestrator agent adds indirection without value.
- **Revisit if:** Native orchestration proves insufficient for complex multi-agent workflows.

### Context Manager Agent
- **Why rejected:** Hooks (PreCompact, SessionStart) handle context preservation. Memory Bank system in CLAUDE.md is more comprehensive.
- **Revisit if:** Context loss becomes a problem that hooks don't solve.

### SQLite Coordination Database
- **Why rejected:** Over-engineered. Agent results flow through Task tool return values. Was 100% broken in v2 (NULL confidence scores).
- **Revisit if:** Agent coordination becomes complex enough to need persistent state beyond files.

### DeerFlow Integration
- **Why deferred:** ByteDance's LangGraph-based multi-agent research framework. Actively maintained but adds Python/LangGraph dependency. Claude Code's native WebSearch + research agent covers most use cases.
- **Revisit if:** Research workflows become complex enough to justify external orchestration framework.

### Multi-Level Thread Orchestration
- **Why deferred:** L-thread/P-thread/B-thread taxonomy for parallel Ralph loops. Promising but taxonomy still emerging, no standardized tooling yet.
- **Revisit if:** Parallel worktree patterns mature and tooling stabilizes.

---

*Last updated: 2026-02-15 (post deep research)*
