# cc_agents v4 — Session Handoff

> Paste this into a new Claude Code session started from `~/cc_agents/`.

---

## Context

cc_agents is a template repo for Claude Code agent definitions. v4 was rewritten on 2026-02-15 based on comprehensive research into the Opus 4.6 ecosystem, community patterns, and lessons from the v2 system.

### Current State (v4)

**5 base agents** in `agents/` (~73-78 lines each, tool-agnostic):
- `scout.md` — codebase exploration (haiku, fast and cheap)
- `research.md` — technical research with citations (sonnet)
- `planner.md` — strategic planning with SMART tasks (opus)
- `builder.md` — implementation with TDD and error recovery (sonnet)
- `reviewer.md` — code review against acceptance criteria (haiku, read-only)

**3 Serena variants** in `agents/serena/` (for LSP-enabled projects):
- `scout.md` — adds `get_symbols_overview`, `find_symbol` for semantic analysis
- `builder.md` — adds `replace_symbol_body`, `insert_after_symbol` for precise edits
- `reviewer.md` — adds `find_symbol` for targeted review

**Ralph prototype** in `ralph/`:
- `ralph-builder.sh` — Stop Hook script for autonomous builder iteration
- Based on community Ralph Wiggum pattern (snarktank/ralph, frankbria/ralph-claude-code)

**Two deployment scripts:**
- `init.sh <project> [--serena]` — copies agents into project's `.claude/agents/`
- `deploy.sh [--serena] [--clean]` — promotes agents to `~/.claude/agents/`

### Architecture

```
~/.claude/agents/              <- vanilla defaults (global fallback)
~/cc_agents/                   <- this repo (R&D + template)
   ├── init.sh <project>       <- install experimental agents
   └── deploy.sh               <- promote to vanilla globals

~/my-project/.claude/agents/   <- experimental overrides (project-level)
```

### Design Decisions Made

1. **Base agents are tool-agnostic** — Serena LSP is a separate variant, not baked in
2. **Haiku for read-only agents** (scout, reviewer) — fast, cheap, sufficient
3. **No SQLite, no handoff JSON, no research_tools.py** — all removed as dead code from v2
4. **Ralph uses Stop Hook** — not a formal plugin, just a bash script
5. **Skills to deprecate** — agent-launcher and context-management overlap with native features

### Git Repos (TWO separate repos)

| Repo | Location | GitHub | Purpose |
|------|----------|--------|---------|
| **cc_agents** | `~/cc_agents` | `jonzo97/cc_agents` | Agent R&D, template, testing |
| **.claude** | `~/.claude` | `jonzo97/.claude` | Production runtime (vanilla agents, skills, hooks) |

---

## Continue Working

Check `FUTURE_IMPROVEMENTS.md` for the current improvement backlog. Key next steps:

### Testing and Validation
1. Test base agents with `init.sh` against real projects
2. Test Serena variants in a project with Serena configured
3. Test Ralph builder loop with a real build task
4. Validate reviewer catches issues the builder misses

### Ralph Enhancements
- Add dual-condition exit gate (explicit signal + heuristics)
- Add circuit breaker for same-error repetition
- Add cost monitoring per iteration
- Test with multi-step build tasks

### Research Agent as Foundation
- Once research agent is solid, use it to investigate improvements listed in FUTURE_IMPROVEMENTS.md
- Key topics: DeerFlow integration, Agent Teams patterns, hook-driven agent triggering

### Skills Cleanup (in ~/.claude/ repo)
- Deprecate agent-launcher skill
- Deprecate context-management skill
- Evaluate remaining skills for v4 compatibility

---

## Important Notes

- **Security:** Never access `~/mchp_cli_test` — restricted directory.
- **User's global CLAUDE.md** at `~/.claude/CLAUDE.md` has extensive instructions. Read it.
- **The user prefers action over ceremony.** Research -> decide -> implement.
- **Old system reference:** `archive/v2/` has lessons learned (KNOWN_LIMITATIONS.md, FEEDBACK_HISTORY.md).
