# Orchestrator Guide

Guidance for the main Claude instance when leading agent teams. Add relevant sections to your project's `CLAUDE.md` or reference this document.

---

## Pre-Flight Protocol

Before spawning any agents, the orchestrator runs a structured pre-flight. This is not optional — skipping it is the #1 cause of wasted builds.

### Scout-Then-Ask

**Never ask questions you could answer from code inspection.** Before asking the user anything:

1. Quick-scan these files (30 seconds):
   - `CLAUDE.md` / project instructions
   - `package.json` / `pyproject.toml` / `Cargo.toml` (dependencies, scripts)
   - Test config (`jest.config`, `pytest.ini`, `vitest.config`, etc.)
   - CI config (`.github/workflows/`, `.gitlab-ci.yml`)
   - `.env.example` (environment requirements)

2. Infer from inspection:
   - Language, framework, test runner
   - Build/run commands
   - Existing patterns and conventions
   - What dependencies are already available

3. Only ask what remains **genuinely unknowable** from code alone.

### The 3-Question Limit

Research shows users disengage after 2-3 upfront questions. Prioritize by task type — ask only what you can't infer:

| Task Type | Must Ask | May Ask | Don't Ask |
|-----------|----------|---------|-----------|
| Bug fix (small) | Scope: which behavior is wrong? | — | Framework, test runner, style |
| New feature | Scope, acceptance criteria | Priority of sub-features | Tech stack (inspect it) |
| Feature with tests | Scope, acceptance criteria | Tool availability (Playwright, etc.) | Test framework (inspect it) |
| Refactor | Scope, constraints (what NOT to change) | Acceptance criteria | Current patterns (read them) |
| Infrastructure | Scope, tool availability | Constraints, rollback needs | Existing config (read it) |

**Format:** Use structured options, not open questions.

Bad: "What test runner do you use?"
Good: "I see Jest in package.json. Should I use that, or are you migrating to Vitest?"

Bad: "How should I handle errors?"
Good: "For error handling, I'll follow the pattern in `src/utils/errors.ts`. Sound right?"

### Interruption Tiers

Not all decisions need human input. Calibrate when to ask vs. proceed:

**Tier 1 — Always interrupt:**
- Irreversible actions (DB schema changes, data migrations)
- External side effects (API calls, emails, deployments)
- Scope ambiguity that could waste >30 minutes of build time
- Security-sensitive decisions (auth, crypto, access control)

**Tier 2 — Interrupt if uncertain:**
- Ambiguous requirements with multiple valid interpretations
- Unfamiliar library or framework (might need research first)
- Scope creep detected (task growing beyond original ask)
- Architectural decisions that affect future work

**Tier 3 — Proceed autonomously:**
- Read-only operations (scouting, research, code analysis)
- Standard patterns matching existing codebase style
- Reversible changes (can be rolled back with git)
- Implementation details within an approved plan

---

## Tool Suggestions

Before starting any task, check if a tool from the [Tool Catalog](tool-catalog.md) would unlock longer autonomous runs.

### The Behavior

1. Identify project type from package.json / pyproject.toml / file structure
2. Look up the recommended tool bundle in the catalog
3. Check which tools are already available (`which playwright`, `which jq`, etc.)
4. **Proactively suggest missing high-impact tools**

### Example

> "This is a web project with visual output. If you enable Playwright (`npm i -D @playwright/test && npx playwright install`), I can verify each component visually without asking you to check. Want me to set that up?"

> "I see this project uses a REST API. `jq` would let me validate JSON responses automatically. It's likely already installed — let me check."

Don't suggest tools for simple tasks where the overhead isn't worth it. A 3-line bug fix doesn't need Playwright. Match tool suggestions to task scope.

---

## Research Flagging

Research is **default-on, not opt-in.** The orchestrator detects when research is needed and flags it before building.

### Domain Complexity Signals

| Signal | Risk | Action |
|--------|------|--------|
| Library/framework released after training cutoff | High | **Mandatory research.** API may have changed, docs may differ from training data. |
| No local docs for key dependency | High | Research or ask user for docs. Don't guess at APIs. |
| Specialized domain (math, physics, graphics, protocols, crypto) | High | **Mandatory research.** Domain constraints are invisible until they cause bugs. |
| Known library, edge-case usage (auth flows, perf optimization, security hardening) | Medium | Flag for optional research. Ask: "This touches [X] which can have gotchas. Research first?" |
| Standard library, standard task (CRUD, simple UI, config changes) | Low | Proceed directly. Research would waste time. |

### Decision Tree

```
Is the domain specialized (math / physics / graphics / protocols / crypto)?
├── YES → Research mandatory. Attach findings to builder tasks.
└── NO → Is the library well-known AND the task standard?
    ├── YES → Proceed directly.
    └── NO → Flag it:
         "This involves [X] which may have gotchas.
          Run research first? [Yes - ~5min] [No - I know this domain]"
```

### Research-to-Task Pipeline

When research runs, findings **must flow to builders as task-level constraints** — not just a report the planner reads.

**The chain:**
1. Research agent produces findings with specific technical constraints
2. Planner extracts constraints relevant to each task
3. Each `TaskCreate` call includes constraints in the task description
4. Builders implement with constraints visible in their task

**If research findings exist and constraints don't appear in task descriptions, the planner is doing it wrong.**

Bad handoff:
```
Task: "Build WebSocket server"
(research report exists somewhere, planner didn't extract anything)
```

Good handoff:
```
Task: "Build WebSocket server"
Constraints (from research):
- Use ws library v8+, not socket.io (lighter, no polling fallback needed)
- Implement ping/pong heartbeat (30s interval) — connections drop silently without it
- Buffer messages during reconnection (max 50 messages, drop oldest)
```

---

## Testing Strategy Detection

During pre-flight, detect project type and note which testing strategy applies. Pass this to the tester agent as context when spawning.

| Project Signal | Strategy | What Tester Does |
|---------------|----------|-----------------|
| `Makefile`, `.c/.h`, `CMakeLists.txt` | Compilation | Run build, parse compiler errors (file:line:col) |
| `package.json` + web framework | Web/Visual | Playwright screenshots, DOM assertions, console errors |
| `pytest.ini`, `pyproject.toml` (pytest) | Python suite | `pytest -v --tb=short`, parse tracebacks |
| `jest.config`, `vitest.config` | JS suite | Run test runner, parse assertion failures |
| `docker-compose.yml` + API routes | API/Integration | curl/httpie against endpoints, validate responses |
| Agent/pipeline output | Orchestration | Verify expected files, output schema, error logs |

**Pre-flight action:** After detecting project type, include the testing strategy in the tester's spawn prompt:
> "This is a Python project with pytest. Run `pytest -v --tb=short` and parse tracebacks for root cause."

For web projects, check Playwright availability and suggest installation if missing (see [Tool Catalog](tool-catalog.md)).

---

## During Orchestration

### Research → Planner Handoff

When research findings exist, ensure the planner attaches **specific technical constraints** to each builder task. Don't just say "see research report." Extract the gotchas:

Bad: `Task: "Build reaction-diffusion simulation"`
Good: `Task: "Build reaction-diffusion simulation" / Constraints: dt < 0.25 for stability, clamp values to [0,1], use standard Gray-Scott params f=0.055 k=0.062`

### Parallel vs Sequential Builders

Spawn parallel builders when:
- Tasks produce independent files (no shared state)
- File ownership is clear (one builder per file)
- No cross-file dependencies

Use sequential builders when:
- Tasks modify shared files (database schema, shared config)
- Later tasks depend on earlier task output
- Integration order matters

### Monitor and Intervene

Watch for:
- **Same error twice** — Builder is stuck. Don't let it spin. Intervene with context or reassign.
- **Builder asking questions** — Answer quickly or the team stalls.
- **Review FAIL on domain issues** — The builder may not have the knowledge to fix it. Consider running a targeted research query and feeding results back.

---

## Post-Build

### Verify Functional Correctness

"Passes syntax check" ≠ "works." After build completes:
- **Web:** Open in browser (Playwright if available), check for errors, verify visual output
- **API:** Hit endpoints with sample requests
- **CLI:** Run with typical inputs
- **Libraries:** Execute usage examples

### Capture Lessons

After each team run, note:
- What went right (reuse this pattern)
- What broke and why (add constraints for next time)
- Which phases were skipped and whether that was the right call
