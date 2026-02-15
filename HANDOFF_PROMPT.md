# cc_agents Modernization — Session Handoff

> Paste this into a new Claude Code session started from `~/cc_agents/` to continue the agent modernization work.

---

## Context

cc_agents has been cleaned up and given a blank-slate rewrite for Opus 4.6. The old v2 system (6 agents, 5,697 lines, SQLite coordination, handoff protocols) has been archived to `archive/v2/`. Four lean agent definitions (~50 lines each) now live in `agents/`. A `deploy.sh` script pushes them to `~/.claude/agents/` for production use.

**Current state:**
- `agents/scout.md` — codebase exploration (49 lines)
- `agents/research.md` — technical research with citations (48 lines)
- `agents/planner.md` — strategic planning and task decomposition (47 lines)
- `agents/builder.md` — implementation with TDD (49 lines)
- `deploy.sh` — deploys agents to `~/.claude/agents/` with backup
- `archive/v2/` — full old system preserved for reference
- `test_scenarios/` — 5 sample codebases for validation

**What was removed and why:**
- Orchestrator agent → Opus 4.6 handles orchestration natively via Task tool
- Context Manager agent → `/compact` skill already handles this
- SQLite coordination DB → over-engineered, agents communicate through Task tool results
- Handoff protocol JSON schemas → unnecessary ceremony

**Git repositories (TWO separate repos — important):**

| Repo | Location | GitHub | Purpose |
|------|----------|--------|---------|
| **cc_agents** | `~/cc_agents` | `jonzo97/cc_agents` | Agent R&D, experimentation, testing |
| **.claude** | `~/.claude` | `jonzo97/.claude` | Production runtime (agents, skills, hooks, templates) |

**Workflow:**
1. Edit agents in `~/cc_agents/agents/*.md` (this repo)
2. Test by running Claude Code sessions with the agents
3. Run `./deploy.sh` to copy agents to `~/.claude/agents/`
4. Commit in **both repos** when satisfied:
   - `cd ~/cc_agents && git add -A && git commit -m "message" && git push`
   - `cd ~/.claude && git add agents/ && git commit -m "message" && git push`

**Do NOT edit agents directly in `~/.claude/agents/`** — changes there get overwritten by `deploy.sh`. Always edit in cc_agents first.

The `.claude` repo also contains skills (`skills/`), hooks (`hooks/`), templates (`templates/`), and global config. Only the `agents/` directory is managed by cc_agents; everything else is edited directly in `.claude`.

---

## Your Mission

**Research-first modernization.** The agent definitions are lean but generic — they don't yet take advantage of what's new in Claude Code, the skills/hooks ecosystem, or community patterns. Before writing final agent definitions, you need to understand the landscape.

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

3. **Claude Code Hooks system**
   - What hook events are available? (PreToolUse, PostToolUse, etc.)
   - Check `~/.claude/hooks/` for existing hooks
   - Can hooks trigger agents or skills?
   - What's the best practice for hook → agent coordination?

4. **Community and ecosystem**
   - Search for Claude Code agent patterns, best practices, example repos
   - Look for what power users are doing with multi-agent setups
   - Check if Anthropic has published guidance on agent design for Opus 4.6
   - Look for MCP server patterns that complement agent workflows

5. **What's changed since October 2025**
   - The old system was built for Sonnet 3.5/4.0 era
   - What capabilities does Opus 4.6 have that make old patterns obsolete?
   - Has the Task tool API changed?
   - New tool types? New permission models?

### Phase 2: Audit Existing Setup (~10-15 min)

Explore what's already deployed and working:

1. **Scan `~/.claude/` thoroughly:**
   - `~/.claude/skills/*/SKILL.md` — read each skill, understand what it does
   - `~/.claude/hooks/` — read hook scripts, understand event handling
   - `~/.claude/agents/` — compare deployed (old) vs cc_agents (new)
   - `~/.claude/tools/` — any custom tools?
   - `~/.claude/commands/` — legacy slash commands?
   - `~/.claude/templates/` — reusable templates

2. **Check the old system for good ideas:**
   - `archive/v2/KNOWN_LIMITATIONS.md` — what problems were identified?
   - `archive/v2/FEEDBACK_HISTORY.md` — what did real-world testing reveal?
   - `archive/v2/NEXT_STEPS_ROADMAP.md` — which future ideas are still relevant?

3. **Identify redundancy:**
   - Skills vs agents — what overlaps? What should be a skill vs an agent?
   - agent-launcher skill vs direct Task tool usage — is the skill adding value?
   - context-management skill vs native /compact — overlap?

### Phase 3: Design Decisions (~10-15 min)

Based on research, decide:

1. **Agent scope** — Should agents be even leaner? Should they have more domain-specific knowledge? Should they reference skills they can invoke?

2. **Skill vs Agent boundary** — When should something be a skill (user-invocable, keyword-triggered) vs an agent (spawned by Task tool for autonomous work)?

3. **Hook integration** — Should agents trigger hooks? Should hooks spawn agents? What's the right coordination model?

4. **Removed agents** — Was removing orchestrator and context_manager the right call? Does the research suggest they add value that Claude can't do natively?

5. **New agents** — Based on research, are there agent types we're missing? (Reviewer? Tester? Documenter? Something domain-specific?)

6. **Cross-project deployment** — The user works across tcl_monster, fpga_mcp, mchp-mcp-core, tool-porting. Should agents be project-aware? Should there be project-specific agent variants?

### Phase 4: Implement (~20-30 min)

Rewrite the agent definitions based on research findings. For each agent:
- Incorporate discovered best practices
- Reference available skills where relevant
- Add domain awareness if research supports it
- Keep them lean but make every line count
- Test against at least one scenario from `test_scenarios/`

Update `deploy.sh` if the deployment model needs to change.

Update `README.md` to reflect the final architecture.

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

`constraint-generator.md` was moved from `~/.claude/agents/` to `/mnt/c/tcl_monster/.claude/agents/` — it's FPGA-specific and belongs in that project, not globally.

---

## Important Notes

- **Security:** Never access `~/mchp_cli_test` — restricted directory
- **The user's global CLAUDE.md** at `~/.claude/CLAUDE.md` has extensive instructions about time estimation, TodoWrite usage, memory management. Read it.
- **The user prefers action over ceremony.** Don't over-plan. Research → decide → implement.
- **Use TodoWrite** for task tracking (user checks via Ctrl+T)
- **The `.claude` repo** (jonzo97/.claude) is the production deployment target. Don't push to it directly — use `deploy.sh`.
- **Old system reference:** `archive/v2/` has the full v2 system. The README.md, KNOWN_LIMITATIONS.md, and FEEDBACK_HISTORY.md are the most useful files for understanding what worked and what didn't.

---

## Quick Start

```bash
# You're in ~/cc_agents/
# 1. Read the current agents
cat agents/*.md

# 2. Read the old system's lessons learned
cat archive/v2/KNOWN_LIMITATIONS.md
cat archive/v2/FEEDBACK_HISTORY.md

# 3. Launch research
# Use the research agent or web search to investigate the landscape

# 4. Audit existing setup
ls ~/.claude/skills/ ~/.claude/hooks/ ~/.claude/agents/ ~/.claude/tools/

# 5. Design and implement
# Update agents/*.md based on findings
# Test with deploy.sh --dry-run
# Deploy with deploy.sh
```
