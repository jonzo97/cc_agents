# cc_agents Modernization — Session Handoff

> Paste this into a new Claude Code session started from `~/cc_agents/`.

---

## Context

cc_agents is a template repo for Claude Code agent definitions. It was rewritten from scratch for Opus 4.6 on 2026-02-09. The old v2 system (6 agents, 5,697 lines, SQLite coordination) is archived in `archive/v2/`.

### Current State

Four lean agent definitions (~50 lines each) in `agents/`:
- `scout.md` — codebase exploration
- `research.md` — technical research with citations
- `planner.md` — strategic planning and task decomposition
- `builder.md` — implementation with TDD

Two deployment scripts:
- `init.sh <project>` — copies agents into a project's `.claude/agents/` (project-level override)
- `deploy.sh` — promotes agents to `~/.claude/agents/` (vanilla globals)

### Architecture

```
~/.claude/agents/              ← vanilla defaults (global fallback)
~/cc_agents/                   ← this repo (R&D + template)
   ├── init.sh <project>       ← install experimental agents into project
   └── deploy.sh               ← promote to vanilla globals

~/my-project/.claude/agents/   ← experimental overrides (project-level)
```

**Resolution order:** Project `.claude/agents/` > Global `~/.claude/agents/`. This is Claude Code's native behavior — verified against official docs and community patterns. No custom infrastructure needed.

**Testing workflow:**
1. Edit agents in `~/cc_agents/agents/*.md`
2. `./init.sh ~/test-project` to install into a test project
3. Run Claude Code in that project — experimental agents are active
4. `./init.sh ~/test-project --remove` to revert to vanilla
5. When satisfied, `./deploy.sh` to promote to vanilla globals

### Git Repos (TWO separate repos)

| Repo | Location | GitHub | Purpose |
|------|----------|--------|---------|
| **cc_agents** | `~/cc_agents` | `jonzo97/cc_agents` | Agent R&D, template, testing |
| **.claude** | `~/.claude` | `jonzo97/.claude` | Production runtime (vanilla agents, skills, hooks, templates) |

cc_agents is the source of truth for agent definitions. Changes flow:
`cc_agents/agents/ → init.sh → project/.claude/agents/` (testing)
`cc_agents/agents/ → deploy.sh → ~/.claude/agents/` (promote to vanilla)

### What Was Removed and Why
- **Orchestrator agent** → Opus 4.6 handles orchestration natively via Task tool
- **Context Manager agent** → `/compact` skill handles this (but skill is marked for deprecation — see below)
- **Constraint Generator agent** → moved to `/mnt/c/tcl_monster/.claude/agents/` (project-specific, FPGA only)
- **SQLite coordination DB** → over-engineered, agents communicate through Task tool results
- **Handoff protocol JSON schemas** → unnecessary ceremony

---

## Your Mission

**Research-first modernization.** The current agent definitions are lean but generic — they don't yet take advantage of what's new in Claude Code, the skills/hooks ecosystem, or community patterns. Before writing final agent definitions, you need to understand the landscape.

### Phase 1: Research (~20-30 min)

Use the **research agent** and **web search** heavily. Investigate:

1. **Claude Code's current Task tool and subagent system**
   - What subagent_types are available? (Check system prompt or docs)
   - How does the `model` field in agent frontmatter actually work?
   - What tools can each subagent_type access?
   - How do agents communicate results back to the parent?
   - What are the actual token/context limits for spawned agents?

2. **Claude Code Skills ecosystem**
   - What's the current SKILL.md format and best practices?
   - How do skills differ from agents in practice?
   - Check `~/.claude/skills/` for existing skills and patterns
   - Are there community skill repos or registries?
   - How do skills interact with hooks?
   - Check the official Anthropic skills repo: github.com/anthropics/skills

3. **Claude Code Hooks system**
   - What hook events are available? (PreToolUse, PostToolUse, etc.)
   - Check `~/.claude/hooks/` for existing hooks
   - Can hooks trigger agents or skills?
   - What's the best practice for hook → agent coordination?

4. **Community patterns**
   - Check these repos for patterns and ideas:
     - `serpro69/claude-starter-kit` — template repo + bootstrap.sh
     - `wshobson/agents` — 112 agents across 73 plugins
     - `VoltAgent/awesome-claude-code-subagents` — 100+ specialized agents
     - `davila7/claude-code-templates` — NPX installer approach
     - `hesreallyhim/awesome-claude-code` — curated resource list
   - Look for what power users are doing with multi-agent setups
   - Check if Anthropic has published guidance on agent design for Opus 4.6

5. **What's changed since October 2025**
   - The old system was built for Sonnet 3.5/4.0 era
   - What capabilities does Opus 4.6 have that make old patterns obsolete?
   - Has the Task tool API changed?
   - New tool types? New permission models?
   - How does the new Teams/TeamCreate system work?

### Phase 2: Audit Existing Setup (~10-15 min)

Explore what's already deployed and working:

1. **Scan `~/.claude/` thoroughly:**
   - `~/.claude/skills/*/SKILL.md` — read each skill, understand what it does
   - `~/.claude/hooks/` — read hook scripts, understand event handling
   - `~/.claude/agents/` — current vanilla agents (should match cc_agents)
   - `~/.claude/tools/` — any custom tools?
   - `~/.claude/commands/` — legacy slash commands?
   - `~/.claude/templates/` — reusable templates

2. **Check the old system for good ideas:**
   - `archive/v2/KNOWN_LIMITATIONS.md` — what problems were identified?
   - `archive/v2/FEEDBACK_HISTORY.md` — what did real-world testing reveal?
   - `archive/v2/NEXT_STEPS_ROADMAP.md` — which future ideas are still relevant?

3. **Identify redundancy:**
   - Skills vs agents — what overlaps? What should be a skill vs an agent?
   - `agent-launcher` skill vs direct Task tool usage — is the skill adding value?
   - `context-management` skill vs native `/compact` — overlap?

### Phase 3: Design Decisions (~10-15 min)

Based on research, decide:

1. **Agent scope** — Should agents be even leaner? Should they have more domain-specific knowledge? Should they reference skills they can invoke?

2. **Skill vs Agent boundary** — When should something be a skill (user-invocable, keyword-triggered) vs an agent (spawned by Task tool for autonomous work)?

3. **Hook integration** — Should agents trigger hooks? Should hooks spawn agents? What's the right coordination model?

4. **Removed agents** — Was removing orchestrator and context_manager the right call? Does the research suggest they add value that Claude can't do natively?

5. **New agents** — Based on research, are there agent types we're missing? (Reviewer? Tester? Documenter? Something domain-specific?)

6. **init.sh enhancements** — Should init.sh also copy skills or hooks? Should there be "profiles" (minimal, full, domain-specific)?

### Phase 4: Implement (~20-30 min)

Rewrite the agent definitions based on research findings. For each agent:
- Incorporate discovered best practices
- Reference available skills where relevant
- Add domain awareness if research supports it
- Keep them lean but make every line count
- Test with `./init.sh` against a real project

Update `init.sh` and `deploy.sh` if the deployment model needs changes.
Update `README.md` to reflect the final architecture.
Commit and push to `jonzo97/cc_agents`.

---

## Pending Deprecation: context-management skill

The `~/.claude/skills/context-management/` skill is marked for deprecation. It was a workaround for suboptimal `/compact` behavior. During the research phase, investigate:
- What's the current best practice for context preservation across compacts?
- Are there better hook-based approaches (PreCompact/PostCompact events)?
- Should context management be a hook rather than a skill?
- What does the community do for context continuity?

The goal is to either replace the skill with something better or confirm that native `/compact` is now sufficient. The user's `~/.claude/CLAUDE.md` has extensive context preservation instructions (Memory Bank, session snapshots, etc.) — check if the skill is redundant with what's already there.

---

## Moved: constraint-generator agent

`constraint-generator.md` was moved from `~/.claude/agents/` to `/mnt/c/tcl_monster/.claude/agents/` — it's FPGA-specific and belongs in that project, not globally. This is an example of the right pattern: domain-specific agents live in project `.claude/`, generic agents live in `~/.claude/`.

---

## Important Notes

- **Security:** Never access `~/mchp_cli_test` — restricted directory.
- **User's global CLAUDE.md** at `~/.claude/CLAUDE.md` has extensive instructions about time estimation, TodoWrite usage, memory management. Read it.
- **The user prefers action over ceremony.** Don't over-plan. Research → decide → implement.
- **Use TodoWrite** for task tracking (user checks via Ctrl+T).
- **Old system reference:** `archive/v2/` has the full v2 system. The README.md, KNOWN_LIMITATIONS.md, and FEEDBACK_HISTORY.md are the most useful files for understanding what worked and what didn't.

---

## Quick Start

```bash
# You're in ~/cc_agents/

# 1. Read current agents
cat agents/*.md

# 2. Read old system lessons
cat archive/v2/KNOWN_LIMITATIONS.md
cat archive/v2/FEEDBACK_HISTORY.md

# 3. Research the landscape (use research agent + web search)

# 4. Audit existing setup
ls ~/.claude/skills/ ~/.claude/hooks/ ~/.claude/agents/ ~/.claude/tools/

# 5. Design and implement updated agents

# 6. Test
./init.sh ~/some-test-project
# Run Claude Code session in ~/some-test-project, verify agents work
./init.sh ~/some-test-project --remove

# 7. Promote and commit
./deploy.sh                # Update vanilla globals
cd ~/cc_agents && git add -A && git commit -m "message" && git push
cd ~/.claude && git add agents/ && git commit -m "message" && git push
```
