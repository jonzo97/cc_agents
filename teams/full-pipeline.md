# Team Preset: Full Pipeline

Complete 5-agent pipeline: Scout → Research → Plan → Build → Review.
The maximalist approach for complex features.

## When to Use

- Large features requiring exploration, research, planning, and implementation
- When you want the full agent pipeline with minimal manual coordination
- Tasks where each phase genuinely benefits from a specialized agent

## When NOT to Use

- Simple bug fixes (just use builder directly)
- Research-only tasks (use parallel-research preset instead)

## Research: Default-On

Research is **opt-out, not opt-in.** Apply this decision tree before every pipeline run:

```
Is the domain specialized (math / physics / graphics / protocols / crypto)?
├── YES → Research mandatory. Findings flow to builder tasks as constraints.
└── NO → Is the library well-known AND the task standard?
    ├── YES → Skip research. Proceed to planning.
    └── NO → Flag it:
         "This involves [X] which may have gotchas.
          Run research first? [Yes - ~5min] [No - I know this domain]"
```

**Cost math:** A 5-minute research phase costs ~10K tokens. Debugging domain knowledge gaps costs 10-50x that. When in doubt, research.

**Research findings must flow to builders.** The planner extracts specific constraints from research and attaches them to each TaskCreate call. A research report that the planner reads but doesn't propagate is wasted work. See the [Orchestrator Guide](../docs/orchestrator-guide.md#research-flagging) for the full research-to-task pipeline.

## Skipping Phases

You can skip phases, but be intentional about it:

| Phase | Skip when... | Risk of skipping |
|-------|-------------|-----------------|
| Scout | You already know the codebase well | Low — your knowledge substitutes |
| Research | Domain is trivial (CRUD, simple UI) — use decision tree above | **High for technical domains** — math, physics, protocols, graphics all have gotchas that bite builders |
| Planner | PRD is detailed enough to serve as plan | Medium — PRD describes *what*, not *how* |
| Review | Confident in builder output + good tests | Medium — untested code ships bugs |

## Team Structure

| Role | Agent | Count | Model | Phase |
|------|-------|-------|-------|-------|
| Lead | You (main Claude) | 1 | opus | All |
| Scout | scout | 1 | haiku | 1 |
| Researcher | research | 1 | sonnet | 1 |
| Planner | planner | 1 | opus | 2 |
| Builder | builder | 1-N | sonnet | 3 |
| Tester | tester | 1 | sonnet | 3 |
| Reviewer | reviewer | 1 | haiku | 4 |

### Parallel Builders

When the plan produces independent tasks (separate files, no shared state), spawn multiple builders:
- Each builder **owns specific files** — never assign the same file to two builders
- Ideal for: independent modules, separate pages/components, parallel test suites
- Avoid for: tasks that touch shared state, cross-file refactors, database migrations
- Tested: 8 parallel builders produced ~5,800 lines in ~8 minutes with zero merge conflicts

## Task Flow

```
Phase 1: Discovery (parallel, ~3-5 min)
├── Scout: Explore codebase → Scout Report
└── Research: Investigate approach → Research Report

Phase 2: Planning (sequential, ~5 min)
└── Planner: Synthesize findings → Implementation Plan + TaskCreate

Phase 3: Build + Test (inner loop, ~10-30 min)
├── Builder: Implement plan tasks → Code changes
└── Tester: Test each task as builder completes it
    ├── PASS → Builder moves to next task
    └── FAIL → Tester creates fix tasks → Builder fixes → Tester re-tests
    (max 3 fix cycles per task)

Phase 4: Review (outer gate, ~3 min)
└── Reviewer: Final acceptance check on all changes
    ├── PASS → Done, ship it
    └── FAIL (architecture) → Re-plan → restart Phase 3 (max 1 re-plan)
```

## Setup Steps

1. **Create team and all tasks upfront:**

   ```
   TeamCreate with team_name "pipeline-<feature>"

   # Phase 1 tasks (no blockers — start immediately)
   TaskCreate: "Scout codebase for <feature area>"
   TaskCreate: "Research best practices for <feature>"

   # Phase 2 task (blocked by Phase 1)
   TaskCreate: "Create implementation plan"
     → addBlockedBy: [scout-task, research-task]

   # Phase 3 task (blocked by Phase 2)
   TaskCreate: "Implement the plan"
     → addBlockedBy: [plan-task]

   # Phase 4 task (blocked by Phase 3)
   TaskCreate: "Review implementation"
     → addBlockedBy: [build-task]
   ```

2. **Spawn Phase 1 agents (parallel):**
   ```
   Task with team_name, subagent_type "scout", name "scout"
   Task with team_name, subagent_type "research", name "researcher"
   ```

3. **When Phase 1 completes, spawn Phase 2:**
   ```
   Task with team_name, subagent_type "planner", name "planner"
   ```

4. **When Phase 2 completes (plan approved), spawn Phase 3 (builder + tester):**
   ```
   Task with team_name, subagent_type "builder", name "builder"
   Task with team_name, subagent_type "general-purpose", name "tester"
   ```
   Tester uses `agents/tester.md` prompt. Both run concurrently — tester claims test tasks as builder completes implementation tasks. Inner loop: build → test → fix → test per task.

5. **When all Phase 3 tasks pass, spawn Phase 4:**
   ```
   Task with team_name, subagent_type "general-purpose", name "reviewer"
   ```

## Phase Transitions

Each phase transition is a natural checkpoint:

| Transition | Gate | Human Input |
|-----------|------|-------------|
| 1 → 2 | Both scout + research tasks completed | Optional: review findings |
| 2 → 3 | Plan created, tasks defined | **Recommended: approve plan** |
| 3 → 4 | All build tasks pass inner loop (builder + tester) | Optional: quick manual check |
| 4 → done | Review PASS | Optional: final review |

## Tips

- **Don't spawn all agents at once.** Phase dependencies exist for a reason.
- **Plan approval is the key checkpoint.** Always review the plan before Phase 3.
- For smaller features, skip Phase 1 (if you know the codebase) or skip Research (if the approach is clear).
- The `/pipeline` command automates this entire flow.

## Cost Estimate

Rough token usage per phase (varies by project size):
- Phase 1: ~15K tokens (scout: 5K, research: 10K)
- Phase 2: ~10K tokens
- Phase 3: ~30-80K tokens (depends on feature complexity)
- Phase 4: ~8K tokens
- **Total: ~60-110K tokens per pipeline run**
