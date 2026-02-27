# Cross-Project Communication Patterns

How to coordinate work between separate Claude Code instances running in different project directories.

## The Problem

You have multiple projects (`cc_agents`, `second-brain`, `fpga_project`, etc.) each with their own CC instance. They can't talk to each other directly, but sometimes need shared context: "use the research from project A to inform the build in project B."

## Pattern: Shared Mailbox File

A single file at a known path acts as a message board between projects. Every CC instance knows where it is and checks it when relevant.

### Setup

**File:** `~/.claude/cross-project.md`

**Add to global CLAUDE.md (`~/.claude/CLAUDE.md`):**
```markdown
## Cross-Project Context
When working across projects, check `~/.claude/cross-project.md` for handoff notes,
shared context, and delegation requests from other project instances.
Update it when your work produces artifacts useful to other projects.
```

### Message Format

```markdown
## [Source Project] → [Target Project]: Short Description
**Date:** YYYY-MM-DD
**Status:** pending | acknowledged | completed
**Context:** Why this matters to the target project.

### Content
The actual handoff — findings, decisions, file paths, instructions.

### Action Requested
What the target project instance should do with this.

---
```

### Example

```markdown
## cc_agents → second-brain: New skill patterns available
**Date:** 2026-02-19
**Status:** pending
**Context:** cc_agents now has a skills/ directory with reusable workflow patterns for Playwright, ChromaDB, etc.

### Content
Skills at ~/cc_agents/skills/ encode tool expertise with zero context cost until loaded.
Relevant to second-brain's RAG topic — ChromaDB skill shows how to build RAG without MCP overhead.

### Action Requested
Update topics/rag.md to reference the ChromaDB skill pattern.

---
```

### Lifecycle

1. Source project writes a message with `status: pending`
2. Target project reads it, acts on it, updates status to `read by [project] (YYYY-MM-DD)`
3. Once actioned, update status to `completed by [project] (YYYY-MM-DD)`
4. Periodically clean out completed messages (or archive them)

### Inbox Hook (Automatic)

A SessionStart hook at `~/.claude/tools/check_inbox.sh` runs on every session start across all projects. It:
- Counts pending messages in `~/.claude/cross-project.md`
- Shows message headers to the CC instance
- Tells the agent to read the full mailbox and update statuses

This means every CC instance, in any project, gets notified of pending cross-project messages the moment a session starts. No manual "check inbox" needed.

**Hook config** (in `~/.claude/settings.json` → `hooks.SessionStart`):
```json
{
  "hooks": [{ "type": "command", "command": "~/.claude/tools/check_inbox.sh" }]
}
```

## Pattern: Peek at Sibling Project

For read-only context sharing — one instance reads files from another project without modifying them.

### Setup

Add to project CLAUDE.md:
```markdown
## Sibling Projects
- `~/second-brain/topics/` — Research topics, tools to explore, bookmark collections
- `~/cc_agents/skills/` — Reusable workflow skills (chromadb, cozodb, playwright, etc.)
- `~/cc_agents/docs/` — Agent orchestration patterns and guides
```

The CC instance can `Read` these paths when the task is relevant. No write access needed.

### When to Use Which

| Scenario | Pattern |
|----------|---------|
| "Take findings from project A and use them in B" | Shared mailbox — write a handoff message |
| "What tools does project A have that are relevant here?" | Peek — just read the file |
| "Project A needs project B to do something" | Shared mailbox — write a delegation request |
| "I want to reference project A's patterns" | Peek — read on-demand |

## Future: Cross-Delegation

A more structured pattern where one CC instance spawns work in another project. This requires:
- Handoff prompts with full context
- Agreed-upon directory structure for inputs/outputs
- Status tracking across projects

**Status:** Future research. See TodoWrite for tracking.

---

## Research Findings (Prompt #05, Feb 2026)
*Source: extract_cross_project_coordination.md*

### Hard Constraints
- **Never dump full project context into another agent session.** "Lost in the Middle" causes 20-25% accuracy variance.
- **JIT context retrieval is mandatory.** Agents maintain lightweight identifiers and load data dynamically only when relevant.
- **Minimum viable handoff document** must include: (1) current task goal, (2) what was learned, (3) modified files, (4) explicit next steps.
- **WSL2 with 16GB RAM:** Multiple concurrent Claude Code instances can trigger OOM-killer. Monitor with `ps aux | grep claude`.
- **AI-to-AI doc sync MUST include human review.** Without it, hallucinated cross-project dependencies become source of truth.

### Architecture Decisions
- **Handoff vs Consultation:** Make it explicit. Most cross-project interactions are consultations (query-and-return), not ownership transfers.
- **Memory layer:** Memory Bank (flat markdown) is correct for single-developer. Migrate to Kuzu/SQLite MCP knowledge graph when flat mailbox bottlenecks.
- **Git hooks over daemons:** Integrate into existing Git + Claude Code lifecycle hooks. Deterministic, low-overhead, no extra process.
- **Blackboard pattern for async:** Central orchestrator repo with specs and state (not code). Agent A marks done; Agent B reads update. `~/second-brain` partially implements this already.

### Patterns to Formalize
1. **JIT Context Loading** — Hold pointers, load on demand only when current reasoning step requires it.
2. **Structured Handoff Document** — Auto-generate on session end: goal + learned + files + next steps. Stop hook candidate.
3. **Consultation over Handoff** — Send targeted query, receive specific answer, continue. Don't transfer ownership for queries.
4. **Merge Conflict as Feature** — When two agents write contradictory learnings, git conflict forces reconciliation. Elegant for shared topic files.
5. **Input Filters on Handoffs** — Trim conversation history before passing to specialist. Reduces token waste.

### Anti-Patterns
1. **"Kitchen-sink" context dump** — Accuracy drops to 64-67% (vs 83% with targeted loading). Hallucinates non-existent dependencies.
2. **Production infra too early** — PostgreSQL + vector DB for single-developer memory. Local markdown + SQLite gives ~90% of benefit.
3. **Polling loops** — Each poll burns tokens. Use git hooks, inotifywait, or lifecycle hooks as event triggers.
4. **Skipping the handoff doc** — Receiving agent can't reconstruct context from conversation history alone, especially after compaction.
5. **5+ concurrent Claude instances on 16GB WSL2** — Known memory leak (v2.1.21 and earlier). OOM risk.

### Tools Discovered
- inotifywait (interrupt-driven filesystem watching for WSL2)
- Context7 (MCP server for version-specific library docs)
- Agent Watch (git hook-based CLAUDE.md sync across chat sessions)
- NanoClaw (container-isolated agents for different trust levels)

---

*Updated 2026-02-24 from research squeeze. See `~/cc_agents/research/active/extracts/extract_cross_project_coordination.md` for full extract.*
