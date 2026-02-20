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
## cc_agents → second-brain: New recipe pattern available
**Date:** 2026-02-19
**Status:** pending
**Context:** cc_agents now has a recipes/ directory with direct-code patterns for Playwright, ChromaDB, etc.

### Content
Recipes at ~/cc_agents/recipes/ replace MCP servers with direct Python usage.
Relevant to second-brain's RAG topic — ChromaDB recipe shows how to build RAG without MCP overhead.

### Action Requested
Update topics/rag.md to reference the ChromaDB recipe pattern.

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
- `~/cc_agents/recipes/` — Direct-code recipes for common tools
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
