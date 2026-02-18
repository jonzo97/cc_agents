# cc_agents Framework — Field Test Feedback (Revised)

**Test Date:** 2026-02-17 through 2026-02-18
**Scenario:** CNY 2026 Interactive Visual Art Gallery (8 canvas-based generative art cards)
**Team Preset Used:** Custom — closest to `full-pipeline` but skipped scout/research/planner phases (PRD served as plan)
**Team Size:** 1 lead (Opus) + 8 builder agents (Sonnet)
**Build Wall-Clock Time:** ~8 minutes from team creation to all files written + validated
**Total Wall-Clock Time (including debugging):** ~90 minutes across 2 sessions

---

## Executive Summary

The build phase was impressive: 8 parallel builders produced ~5,800 lines of generative art code in ~8 minutes with zero merge conflicts. However, **2 of 8 cards were fundamentally broken** despite passing all quality gates (syntax check, API consistency). The debugging phase consumed 10x the build time. This reveals that the framework excels at parallelized code generation but lacks critical verification and domain-knowledge injection capabilities.

**Revised Grade: C+** — Excellent build orchestration, but the pipeline's quality gates are insufficient for non-trivial implementations. The skip of research/planning phases was costly.

---

## Part 1: What Worked Well

### 1. Task Dependency System
The `blockedBy` mechanism worked exactly as designed. Shell infrastructure (task #1) blocked all 8 card tasks, and they correctly unblocked when task #1 was marked complete. The integration review (task #10) was blocked by all card tasks. This is the right primitive for phased work.

### 2. Parallel Builder Spawning
Launched 4 builders simultaneously for the first batch of cards, then 3 more for the remaining cards. All produced independent, non-conflicting files. **Zero merge conflicts** because each builder owned a single file. This is the ideal parallelization pattern — embarrassingly parallel with no shared state.

### 3. Consistent API Compliance
All 8 builders independently produced files that:
- Used the correct `registerCard(N, { init, start, pause, resume, destroy })` API
- Referenced `HORSE_SVG_PATH` from utils.js consistently
- Used `COLORS` constants from the shared palette
- Followed the same naming convention (card-N.js)
- Passed `node --check` syntax validation (0 failures across 10 files)

### 4. Self-Coordination in Team Mode
Builder-3 completed Card 3 (Particle Glitch) and **proactively claimed task #6 (Card 1: Fourier Epicycles)** without being asked. This is the team-mode behavior described in the agent definition working as intended — agents check TaskList after completing a task and pick up the next available one.

### 5. Agent Definitions Are Right-Sized
The ~77-line builder definition was sufficient to guide Sonnet through substantial implementations (500-950 lines each). The "trust the model" principle was validated for structural correctness — agents didn't need micro-management for code architecture, API compliance, or file organization.

### 6. Output Volume
Each card file is substantial:
- Card 1 (Fourier): 826 lines — epicycle rendering with DFT
- Card 2 (Flow Field): 508 lines — noise-based particle system
- Card 3 (Particle Glitch): 576 lines — particle text with CRT effects
- Card 4 (Ink Wash): 570 lines — brush stroke simulation
- Card 5 (Paper Cut): 875 lines — SVG parallax with 6 layers
- Card 6 (Fireworks): 953 lines — full firework physics
- Card 7 (Reaction-Diffusion): 486 lines — Gray-Scott simulation
- Card 8 (Strange Attractor): 612 lines — Lorenz system with RK4

**Total: ~5,800 lines produced in ~8 minutes.**

---

## Part 2: Critical Issues (Post-Build Analysis)

### 1. Two Cards Were Fundamentally Broken Despite Passing All Quality Gates (Critical)

**Card 7 (Reaction-Diffusion)** had three compounding bugs:
- **Numerical instability:** Diffusion coefficients `dA=1.0, dB=0.5` with `dt=1.0` violated the stability limit (`dt < h²/(2*d*dim) = 0.25`). The simulation diverged immediately — values exploded, producing a blank/garbage canvas.
- **Missing value clamping:** No bounds checking on concentrations after each step.
- **Unguarded parameter exploration:** `mousemove` was calling `updateParamExplore` on every move without modifier key, randomly changing f/k parameters whenever the mouse was over the canvas.

**Card 1 (Fourier Epicycles)** had five compounding bugs requiring 5+ fix iterations across 2 sessions:
- **Wrong time advancement:** `speed / (N * 60)` where N=600 made the trace take 10+ minutes to complete one cycle.
- **Missing DFT frequency remapping:** Frequencies > N/2 were not remapped to negative values, making high-frequency epicycles spin hundreds of times instead of once, producing chaotic blur instead of smooth curves.
- **Non-centered path data:** Points centered at screen coordinates (960, 540) instead of origin, producing a ~1100px DC component that pushed the entire trace off-screen.
- **Broken 福 path extraction:** The canvas fallback sorted edge pixels by angle from center, which zigzags between disconnected strokes of a complex multi-stroke character. The fundamental approach was wrong.
- **Font URL 404:** The opentype.js font URL was hardcoded to a Google Fonts URL that returned 404, silently falling back to the broken canvas approach.

**Root cause analysis:** These aren't typos or edge cases — they're domain knowledge gaps. The builder agents didn't know:
- Gray-Scott stability constraints (well-documented in numerical methods literature)
- DFT frequency aliasing (standard signal processing knowledge)
- That CJK characters have multiple disconnected strokes (visual domain knowledge)
- That Google Fonts URLs change over time (web platform knowledge)

**The syntax check + API compliance review caught zero of these.** The cards passed `node --check`, used the correct `registerCard` API, and referenced shared constants correctly. Structurally perfect, functionally broken.

### 2. Debugging Cost Vastly Exceeded Build Cost (Critical)

| Phase | Wall-Clock Time | Context Tokens |
|-------|----------------|----------------|
| Team setup + build | ~8 min | ~60K |
| Integration review (syntax only) | ~2 min | ~5K |
| Card 7 debugging + fix | ~10 min | ~15K |
| Card 1 debugging (5 iterations) | ~60 min | ~150K+ |
| **Total** | **~80 min** | **~230K+** |

Card 1 alone consumed more time and tokens than the entire build phase. The debugging required:
- 5 separate hypothesis → edit → test cycles
- Reading reference material on DFT frequency handling
- Installing Playwright and creating visual test infrastructure
- Eventually extracting font glyph data using Node.js to work around the broken font URL
- Two full context windows (requiring session continuation)

**This is the most important metric in the entire test:** A pipeline that produces code 10x faster but requires 10x the debugging time has not saved time. Net productivity was negative compared to a single careful implementation.

### 3. Skipping Research Phase Was Costly (High)

We skipped the Research agent because the PRD existed. This was a mistake. The PRD described *what* to build but not *how* to build it correctly. A research phase could have:

| Research Question | What It Would Have Found | Bug It Would Have Prevented |
|-------------------|--------------------------|----------------------------|
| "DFT Fourier epicycle implementation best practices" | Frequency remapping for k > N/2 is essential | Card 1 frequency aliasing |
| "Gray-Scott reaction-diffusion numerical stability" | dt < h²/(2d·dim) constraint | Card 7 divergence |
| "Canvas-based CJK character contour extraction" | Multi-stroke characters need contour tracing, not edge detection | Card 1 broken 福 path |
| "Google Fonts URL stability for direct font file loading" | URLs are versioned and change regularly | Card 1 font loading 404 |
| "Fourier series path representation best practices" | Points must be origin-centered for stable DC component | Card 1 off-center trace |

**Cost of the research phase:** ~10K tokens, ~5 minutes.
**Cost of debugging without it:** ~150K+ tokens, ~60 minutes.

The research agent definition emphasizes citations and confidence levels. If it had produced a "Technical Notes for Builders" document with these constraints, the builders would have implemented correctly the first time.

### 4. Reviewer Agent Was Never Used (High)

The `full-pipeline` preset prescribes a Phase 4 review. We skipped it. The lead did a manual review that was limited to:
- `node --check` on all files (syntax only)
- `grep` for API consistency (structural only)

The reviewer agent definition specifies: "Run full project test suite, report specifics." But there was no test suite — the project is a visual canvas application. The reviewer definition has **no guidance for visual/UI projects**. Even if we had spawned a reviewer, it would have had no way to verify the output.

**This reveals a gap in the reviewer agent definition:** It assumes testable code with a test suite. For visual/creative/interactive projects, the acceptance criteria can't be verified with `npm test`.

### 5. No Feedback Loop to Builders (Medium)

When Cards 1 and 7 were found broken, the lead manually debugged and fixed them. The `build-review-loop` preset describes the correct pattern: reviewer creates fix tasks, builder picks them up, re-review. We didn't use this loop.

If we had:
1. Spawned a reviewer that ran Playwright screenshots
2. Reviewer identified Card 1 and Card 7 as broken, created fix tasks with specific issues
3. Builder agents picked up fix tasks with the domain context from the review
4. Re-review cycle until PASS

This would have distributed the debugging work and kept the lead focused on orchestration.

---

## Part 3: Framework Design Observations

### What the Agent Definitions Got Right
1. **Team Mode sections** are essential. Builder-3's self-claiming proves this.
2. **Tool restrictions** per agent type prevent accidents.
3. **Model selection** per agent is cost-effective.
4. **Error recovery protocol** (2 attempts then escalate) is a good pattern.
5. **Builder TDD workflow** is sound — but only effective when there's a test to run.

### What's Missing from Agent Definitions

#### Builder Definition Gaps
1. **No domain knowledge injection mechanism.** The builder gets a task description and the codebase. There's no slot for "here are technical constraints from the research phase." The planner creates tasks, but those tasks don't carry the research context.
2. **No smoke test guidance.** The builder definition emphasizes TDD but doesn't address "what if there's no automated test suite?" For visual projects, the builder should at minimum open the output and verify it's not blank/broken.
3. **"No gold-plating" can conflict with correctness.** The builder definition says "implement only what was asked." But correctness often requires things not explicitly asked for — like DFT frequency remapping or numerical stability constraints. The builder's mandate should include "implement correctly" not just "implement the spec."

#### Reviewer Definition Gaps
1. **No visual verification path.** The reviewer can run tests and read code, but can't verify visual output. For frontend/canvas/creative projects, the reviewer needs Playwright or similar.
2. **No domain-specific verification.** The reviewer checks acceptance criteria but can't verify mathematical correctness or numerical stability.
3. **Bash is listed as available** but with "read-only only" intent. The reviewer should be able to run headless browser tests.

#### Research Definition Gaps
1. **No mechanism to feed findings to builders.** The research agent produces a report, but there's no structured way for builders to consume it. The research output should include a "Builder Notes" section with specific constraints/gotchas that get attached to task descriptions.
2. **Timing is disconnected from build.** Research runs in Phase 1 and produces a report. But if a builder encounters an issue in Phase 3, there's no way to invoke a targeted research query without the lead manually mediating.

### What's Missing from Team Presets

#### Full Pipeline Preset
1. **Phase 1 should produce builder-consumable artifacts.** The current flow is: Scout → Report, Research → Report, Planner reads reports. But the reports aren't structured for builders. The planner should synthesize research findings into task-level constraints.
2. **No parallel builder pattern.** The preset shows 1 builder. Our test proved N parallel builders work well for independent tasks. The preset should document when and how to parallelize.
3. **No visual verification in Phase 4.** The review phase assumes code review + test execution. Creative/visual projects need screenshot comparison.
4. **No guidance on when to skip phases.** We skipped 3 of 5 phases. The preset should explicitly say: "Skip Scout if codebase is familiar. Skip Research if domain is well-understood. Skip Planner if PRD is detailed enough."

#### Build-Review Loop Preset
1. **Max 3 cycles may be insufficient** for complex bugs. Card 1 required 5 fix iterations. The escalation to human is correct but the limit should be configurable.
2. **No debugging agent type.** When the reviewer finds issues, the builder gets fix tasks. But the builder that wrote the buggy code may repeat the same mistakes. A specialized "debugger" agent with Playwright + domain knowledge might be more effective.

---

## Part 4: Recommendations

### Immediate (Low Effort, High Impact)

1. **Add Playwright to the reviewer toolkit.** Give the reviewer the ability to launch headless Chrome, navigate to the app, and take screenshots. Pipe screenshots through vision analysis to detect "blank screen," "error overlay," or "renders recognizable content."

2. **Add a "Technical Constraints" field to task descriptions.** When the research agent produces findings, the planner should attach relevant constraints to each task:
   ```
   Task: "Build Card 7: Reaction-Diffusion"
   Constraints:
   - Gray-Scott stability: dt < h²/(2*d*dim). With h=1, d=0.5, dim=2: dt < 0.25
   - Use standard parameters: f=0.055, k=0.062, dA=0.2097, dB=0.105
   - Clamp concentrations to [0, 1] after each step
   ```

3. **Make research phase opt-out, not opt-in.** The full-pipeline preset should strongly recommend research for any non-trivial domain (math, physics, graphics, protocols). The lead should need a reason to skip it, not a reason to include it.

4. **Add "functional smoke test" to builder workflow.** After writing code, the builder should verify the output isn't broken. For web projects: serve with python http.server, open in headless browser, check for JS errors, take screenshot. This adds ~30 seconds per builder but would have caught both broken cards.

### Medium-Term (Moderate Effort)

5. **Create a "visual reviewer" agent variant.** A reviewer specifically for frontend/visual projects that:
   - Launches headless browser with Playwright
   - Navigates to each component/page
   - Takes screenshots and analyzes them with vision
   - Checks for JS console errors
   - Verifies interactive elements respond to input
   - Reports with annotated screenshots

6. **Implement research → builder knowledge transfer.** When research produces a report, extract actionable constraints and inject them into builder task descriptions automatically. The planner is the right place to do this synthesis.

7. **Add domain-specific builder "lints"** as optional task metadata. For numerical simulation: "verify stability constraints." For DFT/signal processing: "verify frequency handling." For web: "verify no 404 resources." These would be hints in the task description that the builder checks before marking complete.

### Long-Term (Framework Architecture)

8. **On-demand research during build.** Allow builders to invoke a research sub-query when they encounter domain questions. Currently, research only runs in Phase 1. A builder working on Gray-Scott should be able to ask "what are the stability constraints?" without going through the lead.

9. **Screenshot regression for visual projects.** After the first successful build, store "golden" screenshots. On subsequent builds/reviews, diff against golden screenshots to detect regressions. This enables the build-review loop for visual projects.

10. **Builder specialization hints.** Allow task descriptions to include "this task requires knowledge of [signal processing / numerical methods / WebGL / etc.]." The lead can then assign to builders with appropriate context, or attach reference material.

---

## Part 5: Metrics (Complete)

| Metric | Value |
|--------|-------|
| **Build Phase** | |
| Team setup time (create + 10 tasks + dependencies) | ~2 min |
| Shell build time (builder-1) | ~3 min |
| Parallel card build time (7 builders) | ~5 min |
| Integration review (syntax only) | ~2 min |
| Shutdown ceremony | ~1 min |
| **Build phase total** | **~8 min** |
| | |
| **Debug Phase** | |
| Card 7 diagnosis + fix | ~10 min |
| Card 1 iteration 1 (time advancement) | ~10 min |
| Card 1 iteration 2 (frequency remapping) | ~10 min |
| Card 1 iteration 3 (origin centering) | ~10 min |
| Card 1 iteration 4 (contour ordering) | ~15 min |
| Card 1 iteration 5 (font extraction + SVG path) | ~15 min |
| Playwright setup + visual test infrastructure | ~10 min |
| **Debug phase total** | **~80 min** |
| | |
| **Overall** | |
| Total JS output | 5,863 lines across 10 files |
| Cards working on first build | 6 of 8 (75%) |
| Cards requiring manual fix | 2 of 8 (25%) |
| Fix iterations for Card 1 | 5 |
| Fix iterations for Card 7 | 1 |
| Syntax errors in build | 0 |
| Functional errors in build | 8+ (across 2 cards) |
| Merge conflicts | 0 |
| Agent self-claims | 1 (builder-3 → Fourier card) |
| Context windows consumed | 2 (required session continuation) |

---

## Part 6: What the User Should Have Done Differently

Honest assessment of prompting/orchestration choices:

1. **Should have included Playwright in the PRD requirements.** The PRD didn't mention visual testing. If it had said "each card must produce a recognizable visual output when tested with Playwright," the build and review phases would have been structured differently.

2. **Should have run research phase.** The PRD said *what* to build but not *how*. A 5-minute research phase per complex card (Fourier, Reaction-Diffusion, Strange Attractor) would have surfaced the constraints that caused the bugs.

3. **Should have specified acceptance criteria beyond syntax.** "Passes `node --check`" is a necessary but wildly insufficient acceptance criterion for visual generative art. Better: "Renders a recognizable horse shape within 15 seconds" or "Produces stable Turing patterns after 100 simulation steps."

4. **Should have used the build-review-loop pattern.** Instead of the lead manually debugging, should have spawned reviewer + Playwright → found broken cards → created fix tasks → builders fix → re-review.

---

## Verdict (Revised)

The cc_agents framework demonstrated **exceptional parallel build orchestration** — 8 builders producing 5,800 lines in 8 minutes with zero conflicts is genuinely impressive. The task dependency system, self-coordination, and API compliance were all solid.

However, the framework's quality assurance pipeline has a critical gap: **it cannot verify functional correctness**, only structural correctness. For projects where "compiles" ≠ "works" (which is most projects), this means the build phase produces code that *looks* right but may be deeply broken. The debugging phase then costs more than the build saved.

The fix is clear: integrate visual/functional verification into the reviewer role, make research opt-out rather than opt-in, and create structured knowledge transfer from research → planner → builder.

**Revised Grade: C+** — The build engine is A-tier. The verification pipeline is D-tier. The average is a C+, but the path to an A is well-defined: add visual verification, make research mandatory for domain-heavy tasks, and close the feedback loop between reviewer and builder.
