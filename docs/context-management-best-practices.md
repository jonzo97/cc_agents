# Context Management Best Practices

Reference doc for managing AI agent context windows, memory persistence, and state preservation.
Synthesized from two Gemini Deep Research outputs (Feb 2026):
- Agentic AI Context Management Research (pre-queue)
- Claude Code Context Management Research (prompts #03 + #06)

---

## Hard Constraints

### Agent Context Architecture
- **Distill state, not trajectory.** Never persist raw step-by-step action logs as primary context. Compiled outcome ("what is true now") only.
- **Observation Masking on old turns.** Tool outputs older than ~5-10 turns MUST be truncated to `[Output masked: N lines]`. >50% token reduction, matches or beats summarization.
- **Drift detection must fail loudly.** If file hashes or git state on restore don't match snapshot, inject a high-priority warning before any agent action.
- **Sub-agents get scoped context only.** Never pass full parent history — construct a targeted briefing: sub-goal + constraints + relevant files + output contract.
- **State files: Markdown, not JSON.** Markdown uses 15-20% fewer tokens and yields higher accuracy (~60.7% vs 52.3%) for LLM-consumed files. JSON for machine-parsed config only.
- **Memory Bank travels with the repo.** State stored outside version control breaks portability.

### Claude Code Specifics
- **200K window has a ~45K internal buffer.** Plan around 150K "safe" limit, not 200K.
- **`used_percentage` is unreliable.** Excludes system prompt + MCP overhead. Can report 75% when "Context low" fires at 6% remaining.
- **Three token types must all be summed:** `input_tokens + cache_read_input_tokens + cache_creation_input_tokens` = total context consumed.
- **Cache tokens don't free space.** 90% price discount, identical physical consumption.
- **MEMORY.md truncates at line 200.** Content beyond line 200 silently dropped.
- **Status line scripts: 300ms budget.** Use `jq` or compiled binaries, not Python.

---

## Architecture Decisions

### State Persistence
**Recommended:** Hybrid File-Centric (Memory Bank) + Git-Native (Aider-style).
- File-Centric captures the "Why" (rationale, constraints, architecture)
- Git-Native ensures the "What" (code) is checkpointed and drift-free

**Rejected alternatives:**
- Pure Event-Sourced (OpenHands): overly complex for lightweight CLI tooling
- Pure Vector-Indexed (Cursor/RAG): structural blindness — can't reason about call graphs, type hierarchies

### Context Compression
**Recommended:** Observation Masking — preserve conversation structure, replace old tool output content with placeholders.
**Rejected:** LLM summarization — lossy for code tasks. Abstracts away file paths, error codes, variable names. Benchmarked worse than truncation (SWE-agent, Dec 2025).

### Context Estimation
**Recommended:** Hybrid model — `messages.countTokens` API for calibration, status line JSON for incremental updates, correction offset for system overhead.
```
corrected_usage = total_input_tokens + estimated_mcp_overhead
safe_remaining = context_window - corrected_usage - 45000  # safety zone
```

### CLAUDE.md Structure
**Recommended:** 5-10 purely imperative rules. Move explanatory prose to `docs/context/` or path-specific `.claude/rules/`.
**Why:** 10-15 rules = frequent silent dropping. 15+ = hallucinations. Explanatory prose interferes with instruction following MORE than random noise.

### Large Task Management
**Recommended:** Ralph Loop / Task tool sidechain delegation. Parent holds architectural plan only; code-writing delegated to clean-context subagents returning summaries.

---

## Patterns

### 1. Four-Layer Memory Architecture
- *Episodic* (what agent did): Rolling window via Observation Masking
- *Semantic* (facts about codebase): AST-based Repo Map
- *Procedural* (rules/constraints): CLAUDE.md / system_patterns.md
- *Working* (current plan): active_context.md

### 2. Priming Prompt Sequence (Cold Start)
Inject in this exact order after compaction:
1. Role definition
2. Procedural Memory (CLAUDE.md)
3. Semantic Context (Repo Map / AST summary)
4. Working Memory (active_context.md)
5. Episodic Bridge (diff of last action before compaction)

### 3. Observation Masking Implementation
For messages older than N turns, replace tool output text with `[Output masked: N lines]`. Keep tool name and call parameters. Reduces tokens >50%.

### 4. Telegraphic Semantic Compression (TSC)
Strip predictable grammar, preserve high-entropy tokens:
- Before: "The system is currently failing to meet timing closure on the PCIe interface due to a setup violation."
- After: "FAIL: timing closure PCIe interface. CAUSE: setup violation."
~40% token reduction with no meaningful loss.

### 5. MEMORY.md as Index, Not Storage
```markdown
# Project Memory Index
- **Architecture**: See arch.md for module relationships.
- **Gotchas**: See bugs.md for the Redis timeout issue.
- **Conventions**: Using the "Service Pattern" for all API routes.
```
Model reads linked files on demand — "Local RAG" within project.

### 6. Compaction Detection
Monitor turn-over-turn token count. Sudden large drop + `<summary>` tags = compaction event. On detection: re-read CLAUDE.md, re-verify project rules.

### 7. PTC (Programmatic Tool Calling)
Instead of reading 100 files (fills context), write a script to grep and return only relevant lines. 37% token reduction on research tasks.

### 8. Sub-Agent Briefing Pattern
When spawning via Task tool, include:
- Specific sub-goal (not full parent goal)
- system_patterns.md contents (constraints)
- Read-only file list from Repo Map (whitelist)
- Explicit output contract ("Return a patch file")

### 9. Git-Backed Compaction Checkpoint
```bash
git checkout -B claude/context-snapshot
git add .claude/memory/.
git commit -m "Auto-checkpoint: Context compaction at $(date)"
git checkout $current_branch
```

---

## Anti-Patterns

1. **Don't persist raw trajectory as state.** Agent fixates on stale errors ("Context Distraction").
2. **Don't use LLM summarization for compression.** Worse than truncation for code — loses specific tokens agents need most.
3. **Don't feed all ADRs into every context load.** Index only. Retrieve full text on-demand when agent proposes conflicting change.
4. **Don't rely on vector search alone for code navigation.** Structural blindness: can't answer "what calls this function?"
5. **Don't give sub-agents full parent context.** Causes noise inheritance and anchoring on irrelevant failures.
6. **Don't use JSON for LLM-read files.** 15-20% more tokens than Markdown for equivalent content.
7. **Don't trust `used_percentage` alone.** Gap between reported and actual can exceed 60 percentage points.
8. **Don't put 10+ rules in CLAUDE.md.** Middle rules silently dropped. Prose actively interferes.
9. **Don't rely on auto-compaction to preserve invariants.** Converts imperative rules to vague summaries.
10. **Don't write status line scripts in Python.** 300ms debounce budget — too tight.
11. **Don't assume cache tokens give headroom.** Same spatial cost, just cheaper financially.

---

## Blind Spots

- **"Lost in the Middle" degrades mid-session reasoning** — not just across compactions. Observation Masking mid-session may be warranted.
- **`<summary>` tag is a detectable compaction signal** — hook can auto-trigger CLAUDE.md re-injection.
- **High `cache_creation_input_tokens` = diagnostic signal** — CLAUDE.md changing too frequently, preventing cache utilization.
- **Sidechain subagents = effectively unlimited parallel context** — the mechanism for "infinite" agentic workflows within 200K constraint.
- **No external tool replaces "Context low" as ground truth** — estimator goal is "warn before the warning fires."
- **ADRs prevent "repeated exploration of rejected approaches"** — quantifiable productivity loss without a decision index.

---

*Synthesized 2026-02-24 from research extracts. See `~/cc_agents/research/active/extracts/` for full source material.*
