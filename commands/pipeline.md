---
name: pipeline
description: Orchestrate the full agent pipeline (scout → research → plan → build → review)
---

# /pipeline — Full Agent Pipeline

Orchestrate a complete agent pipeline for a task. Creates a team, spawns agents in phases, and manages the full lifecycle.

## Usage

```
/pipeline <task description>
/pipeline plan-only <task description>
/pipeline build-only <task description>
```

## Instructions

When the user invokes `/pipeline <task>`, execute the following orchestration:

### 1. Setup

- Create a team: `TeamCreate` with team_name `pipeline-<short-task-slug>`
- Announce: "Starting pipeline for: <task>"

### 2. Pre-Flight (before spawning any agents)

Run the pre-flight protocol from the [Orchestrator Guide](../docs/orchestrator-guide.md):

1. **Scout the project** — Quick-scan CLAUDE.md, package.json/pyproject.toml, test config, CI config. Infer language, framework, test runner, existing patterns.

2. **Check tool availability** — Consult the [Tool Catalog](../docs/tool-catalog.md). If a high-impact tool (Playwright, jq, etc.) would unlock autonomous operation for this task, suggest it now. Example:
   > "This is a web project. Playwright would let me verify visually without asking you to check. Want me to set it up?"

3. **Ask 2-3 targeted questions** — Only ask what you couldn't infer from code inspection. Use structured options:
   - Scope: "This touches X, Y, Z. Should I include all of them, or focus on [specific area]?"
   - Acceptance criteria: "What does 'done' look like? [Option A] [Option B] [Other]"
   - Research need: "This involves [specialized domain]. Research first? [Yes - ~5min] [No - I know this]"

4. **Flag research needs** — Apply the research decision tree. If the domain is specialized (math, physics, protocols, crypto) or involves post-cutoff libraries, research is mandatory. Otherwise, flag and let the user decide.

**Max 2-3 questions total.** Don't front-load a questionnaire. If in doubt, proceed and interrupt at Tier 2 checkpoints later.

### 3. Determine Scope

- **Full pipeline** (default): All phases
- **plan-only**: Phases 1-2 only (discovery + planning). Stop after plan is created.
- **build-only**: Phases 3-4 only (build + review). Assumes plan already exists in TodoWrite.

### 4. Phase 1: Discovery (parallel)

Create and run in parallel:

```
TaskCreate: "Scout the codebase for <relevant area>"
TaskCreate: "Research best practices/approach for <task>"
```

Spawn both agents simultaneously:
```
Task with team_name, subagent_type "scout", name "scout-1", model "haiku"
Task with team_name, subagent_type "research", name "researcher-1", model "sonnet"
```

Wait for both to complete. Collect findings.

### 5. Phase 2: Planning

Create planning task (blocked by discovery):
```
TaskCreate: "Create implementation plan from scout and research findings"
```

Spawn planner:
```
Task with team_name, subagent_type "planner", name "planner-1", model "opus"
```

**CHECKPOINT: Present the plan to the user for approval before proceeding.**

If `plan-only` scope: stop here, show plan summary, clean up team.

### 6. Phase 3: Build + Test (Inner Loop)

After plan approval, spawn builder and tester concurrently:
```
Task with team_name, subagent_type "builder", name "builder-1", model "sonnet"
Task with team_name, subagent_type "general-purpose", name "tester-1", model "sonnet"
```

The tester uses `agents/tester.md` prompt. Inner loop per task:
1. Builder completes an implementation task
2. Tester picks up the corresponding test task, runs tests, analyzes output
3. **PASS** — builder moves to next task
4. **FAIL** — tester creates fix tasks with root cause analysis, builder picks them up
5. Max 3 fix cycles per task. If still failing, escalate to human.

Monitor via TaskList. The inner loop runs automatically through task dependencies.

### 7. Phase 4: Review (Outer Gate)

After ALL tasks pass the inner loop, spawn reviewer:
```
Task with team_name, subagent_type "general-purpose", name "reviewer-1", model "haiku"
```

Handle review results:
- **PASS**: Report success, clean up team
- **FAIL with fix tasks**: Builder picks them up, tester re-validates
- **FAIL with architecture flag**: Re-plan via planner (max 1 re-plan cycle, then escalate to human)

### 8. Completion

- Summarize what was done: files changed, tests passing, key decisions
- Send shutdown_request to all teammates
- Clean up team with TeamDelete
- Report final status

## Progress Reporting

After each phase transition, report:
```
Pipeline: <task>
Phase 1/4: Discovery ✓ (scout: done, research: done)
Phase 2/4: Planning ✓ (plan approved)
Phase 3/4: Building... (3/7 tasks complete)
Phase 4/4: Pending
```

## Error Handling

- If any agent fails or gets stuck, report the issue and ask the user what to do
- If the review cycle exceeds 3 iterations, stop and escalate to human
- If the user cancels at any checkpoint, shut down the team gracefully
