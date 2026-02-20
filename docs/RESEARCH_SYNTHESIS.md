# Research Synthesis — Opus 4.6 Ecosystem (Feb 2026)

Deep research findings from 4 parallel research agents, 60+ sources. Distilled into what matters for cc_agents.

---

## 1. Agent Teams — The Game Changer

Native multi-agent coordination in Claude Code. Multiple Claude instances work in parallel with independent context windows, shared task lists, and direct peer messaging.

### Architecture
| Component | Role |
|-----------|------|
| Team Lead | Main Claude instance — coordinates, delegates, synthesizes |
| Teammates | Separate Claude instances with independent context windows |
| Task List | Shared work queue with dependency tracking |
| Mailbox | Structured messaging system for coordination |

**Key difference from subagents:** Teammates communicate directly with each other, not just back to the spawner.

### Enable
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

### Best Use Cases
- **Strong:** Research/review (parallel investigation), new modules (clear file ownership), debugging (competing hypotheses), cross-layer work (frontend/backend/tests)
- **Avoid:** Sequential tasks (single session better), same-file edits (merge conflicts), heavy dependencies between tasks

### Real-World: $20K C Compiler
[anthropics/claudes-c-compiler](https://github.com/anthropics/claudes-c-compiler) — 16 agents, ~2000 sessions over 2 weeks, 2B input tokens, 140M output tokens. Built a 100K-line Rust C compiler that compiles Linux 6.9 on x86/ARM/RISC-V. 100% of code written by Claude.

### Known Limitations
- 32K subagent output limit (Issue #10738)
- Delegate Mode breaks teammate tools (Issue #24073)
- Bash subagent may fabricate output (Issue #21585)
- No `/resume` or `/rewind` with in-process teammates

### Orchestration Patterns
1. **Parallel Specialists** — Each agent has a focus (security, performance, tests). Findings aggregated by lead.
2. **Pipeline** — Tasks auto-unblock when dependencies complete via `addBlockedBy`.
3. **Self-Organizing Swarm** — Workers independently claim tasks from pool, natural load balancing.
4. **Competing Hypotheses** — Multiple agents investigate different theories, debate and disprove each other.

**Sources:** [TechCrunch](https://techcrunch.com/2026/02/05/anthropic-releases-opus-4-6-with-new-agent-teams/), [Claude Code Docs](https://code.claude.com/docs/en/agent-teams), [Swarm Orchestration Skill](https://gist.github.com/kieranklaassen/4f2aba89594a4aea4ad64d753984b2ea)

---

## 2. Effort Parameter — Cost/Quality Control

Four-level control replacing manual `budget_tokens`:

| Effort | Thinking Behavior | Use Case |
|--------|------------------|----------|
| `max` | Always thinks, no depth constraints (Opus 4.6 only) | Deepest reasoning |
| `high` | Almost always thinks, deep reasoning | Complex problems, agents |
| `medium` | Moderate thinking, may skip simple queries | Balanced speed/quality |
| `low` | Minimal thinking, skips simple tasks | Speed optimization |

**Key finding:** At `medium` effort, Opus 4.6 matches Sonnet 4.5's SWE-bench score while using **76% fewer output tokens**.

### Agent Hierarchy Pattern
```
Main Orchestrator: high effort (quality decisions)
├── Scout Agent: medium effort (balance speed/thoroughness)
├── Research Agent: high effort (thorough findings)
├── Planner Agent: high effort (reliable plans)
└── Builder Subagents: low effort (speed for focused tasks)
```

**Dynamic escalation:** Start at `low`, auto-escalate to `high` on test failures or detected ambiguity.

**Source:** [Effort Parameter Docs](https://platform.claude.com/docs/en/build-with-claude/effort)

---

## 3. Ralph Wiggum — Advanced Patterns

### Three-Phase Architecture (Evolution from Simple Loops)
1. **Requirements** — Specifications and acceptance criteria
2. **Planning** — Gap analysis, task decomposition
3. **Building** — One task per iteration, fresh context

**Philosophy:** "Backpressure beats direction" — engineer environments where wrong outputs get rejected automatically (tests, linters, formatters).

### Agent Teams + Ralph (Hybrid Pattern)
| Use Case | Best Tool | Why |
|----------|-----------|-----|
| Creative work (docs, API design) | **Agent Teams** | Parallel specialists, human review |
| Mechanical work (bug fixes, tests) | **Ralph Loops** | Autonomous iteration, cost-effective |

**The 2026 Standard:** Agent teams for "what" and "why," Ralph loops for "do it until it works."

### Parallel Worktree Execution
Multiple Ralph loops run simultaneously using **git worktrees** for isolated branches:
- **L-thread**: Single Ralph loop
- **P-thread**: Multiple parallel loops
- **B-thread**: Orchestrated chains of loops

### Fresh Context Pattern
Critical for cost and quality:
- Spawns fresh Claude session per iteration
- State persists via files and git commits only
- Prevents context rot over long sessions
- Each iteration gets ~176K usable tokens from 200K window

### Cost Reality
- 50-iteration loop on medium codebase: **$50-100+ API costs**
- `--max-iterations` is cost control, not just safety
- Geoffrey Huntley's 3-month loop built complete programming language
- YC teams shipped 6+ repos overnight for $297

### Exit Detection (frankbria/ralph-claude-code)
- **Dual-condition gate:** Completion indicators AND explicit EXIT_SIGNAL
- **Semantic response analyzer:** Beyond simple pattern matching
- **Circuit breaker:** Error detection, auto-recovery, rate limiting

**Sources:** [Ralph Wiggum Playbook](https://paddo.dev/blog/ralph-wiggum-playbook/), [Agent Teams + Ralph](https://medium.com/@himeag/when-agent-teams-meet-the-ralph-wiggum-loop-4bbcc783db23), [frankbria/ralph-claude-code](https://github.com/frankbria/ralph-claude-code)

---

## 4. Progressive Tool Discovery

See [docs/PROGRESSIVE_TOOL_DISCOVERY.md](PROGRESSIVE_TOOL_DISCOVERY.md) for the full guide.

**Summary:**
| Pattern | Savings | When |
|---------|---------|------|
| Tool Search (`defer_loading`) | 85% | 20-100 tools |
| Code Execution with MCP | 98.7% | 100+ tools |
| Agent Skills (3-level) | Variable | Custom workflows |
| Programmatic Tool Calling | 37% | Multi-tool workflows |
| Tool Use Examples | 72%->90% accuracy | Complex parameters |

---

## 5. Stop Hooks as Quality Gates

Beyond Ralph's iteration loop, stop hooks enable quality enforcement:

### Patterns
1. **Linting/type checks** — Block completion on style violations
2. **Test suite validation** — Prevent PR if tests fail
3. **Output verification** — Ensure files exist, build succeeds
4. **Auto-review** — Architecture/security checks that linters can't express

### Multi-Phase Workflows
```
Phase 1: Requirements → Stop hook validates spec completeness
Phase 2: Implementation → Stop hook runs tests
Phase 3: Documentation → Stop hook validates docs
```

### CI/CD Integration
- **PreToolUse hooks** for PR gating — run tests before allowing PR creation
- Async execution for long-running checks
- Event-driven workflows via git operation hooks

**Sources:** [Quality Gates](https://blog.devgenius.io/claude-code-use-hooks-to-enforce-end-of-turn-quality-gates-5bed84e89a0d), [Auto-Reviewing](https://www.oreilly.com/radar/auto-reviewing-claudes-code/), [Hooks Reference](https://code.claude.com/docs/en/hooks)

---

## 6. Context Compaction (API Feature)

Automatic server-side summarization when approaching context limits.

- Triggers at configurable threshold (default 150K tokens)
- Generates summary, inserts compaction block
- Future requests drop content before compaction block
- Supports custom summarization instructions
- Combined with 1M token window = effectively infinite conversations
- **Prompt caching integration:** Add cache breakpoint to system prompt so it survives compaction

**Source:** [Compaction Docs](https://platform.claude.com/docs/en/build-with-claude/compaction)

---

## 7. Community Frameworks

### Claude Flow v3 (ruvnet/claude-flow)
28 enhancement proposals for Opus 4.6, organized into 6 categories:
- Agent Teams Integration (5 proposals including memory bridge, verification sidecar)
- Adaptive Effort Routing (5 proposals including effort-level router, dynamic escalation)
- Trust & Verification (5 proposals including hash-chained audit, hallucination detection)
- Memory & Learning (5 proposals including semantic curator, cross-session playbooks)
- Security & Safety (3 proposals including security swarm-on-commit)
- Developer Experience (5 proposals including live dashboard, replay & debug)

### Autonomous Loop Convergence
Industry converging on hybrid pattern across Cursor, Devin, Windsurf:
```
Interactive Phase (architecture decisions, creative exploration)
    ↓
Autonomous Phase (mechanical implementation, parallel execution)
    ↓
Review & Refine (quality assessment, course correction)
```

No single tool wins. Teams combine tools for different phases.

---

## 8. DeerFlow Assessment

ByteDance's multi-agent research framework (LangGraph-based):
- Actively maintained, modular architecture
- Adds Python/LangGraph dependency overhead
- Claude Code's native WebSearch + research agent already covers most use cases
- **Verdict:** Track but don't integrate. Marginal value vs. complexity cost.

---

## Emerging "Standard Stack" (Feb 2026)

```
Human: Architecture & Creativity
    ↓
Agent Teams: Planning & Decomposition (with Skills for custom workflows)
    ↓
Ralph Loops: Mechanical Execution (Fresh Context, Stop Hooks)
    ↓
Tools: Progressive Discovery (Code Exec / Tool Search / Direct)
```

---

*Research completed: 2026-02-15*
*4 parallel agents, 60+ sources, confidence: 0.89-0.92*
