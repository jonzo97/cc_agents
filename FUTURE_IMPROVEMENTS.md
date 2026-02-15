# Future Improvements — Brainstorming

Ideas for improving cc_agents, tracked here for future sessions. Roughly prioritized.

## High Priority

### Ralph Enhancements
- **Smart exit detection** — Dual-condition gate (explicit signal + heuristic indicators) instead of simple grep
- **Circuit breaker improvements** — Track same-error repetition, not just no-progress
- **Multi-agent Ralph** — Run ralph loops for scout→planner→builder pipeline, not just builder
- **Cost monitoring** — Track token consumption per iteration, abort if over budget
- **Reference:** [frankbria/ralph-claude-code](https://github.com/frankbria/ralph-claude-code) for enhanced patterns

### Research Agent Improvements
- **Local caching** — Cache web search results to avoid re-fetching across iterations
- **Source quality scoring** — Automatic detection of official docs vs blog posts
- **Research templates** — Pre-built sub-question sets for common research tasks (library comparison, migration guide, etc.)
- **Integration with Perplexity MCP** — Structured research via Perplexity API

### Agent Teams Integration
- **Team-aware agents** — Agents that can coordinate via TeamCreate/SendMessage when spawned as teammates
- **Parallel scout+research** — Scout explores codebase while research investigates technologies simultaneously
- **Builder+reviewer pipeline** — Builder implements, reviewer verifies, loop until all criteria pass

## Medium Priority

### DeerFlow Integration
- ByteDance's multi-agent research framework ([bytedance/deer-flow](https://github.com/bytedance/deer-flow))
- Could enhance research agent with LangGraph orchestration for complex multi-step investigations
- Worth evaluating for research-heavy workflows (technology surveys, architecture reviews)
- **Blocker:** Adds Python/LangGraph dependency, may not justify complexity vs native tools

### RAG/Knowledge Augmentation
- **rag-cli** — Local RAG using Chroma vector embeddings for Claude Code ([ItMeDiaTech/rag-cli](https://github.com/ItMeDiaTech/rag-cli))
- **Project-specific knowledge bases** — Indexed docs, past decisions, codebase patterns
- **Cross-project memory** — MCP-based knowledge graph for patterns that apply across projects

### Hook-Driven Agent Triggering
- **PreToolUse hooks** — Automatically spawn reviewer before destructive operations
- **PostToolUse hooks** — Trigger scout after new file creation to update architecture map
- **Agent hooks** — Use subagent-based hook handlers for intelligent filtering

### Skill-Agent Hybrid Patterns
- **Skills that spawn agents** — A skill could set up context then delegate to an agent
- **Agent results as skill triggers** — Scout findings automatically trigger relevant skills
- **Composable agent chains** — Define pipelines: scout → research → plan → build → review

## Low Priority / Exploratory

### Cost Monitoring Agent
- Track token consumption across agents
- Budget allocation per task
- Alert when approaching limits
- Historical cost analysis per agent type

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

---

*Last updated: 2026-02-15*
