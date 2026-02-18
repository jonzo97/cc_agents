# Orchestrator Guide

Guidance for the main Claude instance when leading agent teams. Add relevant sections to your project's `CLAUDE.md` or reference this document.

---

## Pre-Flight Checklist

Before spawning any agents, the orchestrator should pause and think through these questions:

### 1. Does this need research first?

Even with a detailed PRD, ask: **does the implementation involve non-trivial domain knowledge?**

Domains that almost always need research:
- Mathematical algorithms (DFT, simulations, cryptography)
- Physics/graphics (rendering, particle systems, numerical methods)
- Protocols (OAuth, WebSocket, gRPC)
- Platform-specific APIs (browser quirks, OS differences)

If yes: run research agent first, even if the user didn't ask for it. A 5-minute research phase costs ~10K tokens. Debugging domain gaps costs 100K+.

### 2. What tools would unlock autonomous operation?

Ask yourself: **if I encounter problems during build, what tool would let me diagnose and fix without asking the user?**

Common force multipliers:

| Project Type | Tool | What It Unlocks |
|-------------|------|-----------------|
| Web/frontend | Playwright | Visual verification, JS error detection, 25+ min autonomous runs |
| API/backend | curl/httpie | Endpoint testing without manual verification |
| CLI tools | Sample input files | Automated smoke testing |
| Data pipelines | Small test dataset | End-to-end validation |

**Proactively suggest these to the user.** Example:
> "This is a web project with visual output. If you enable Playwright, I can visually verify each component autonomously instead of asking you to check screenshots. Want me to set that up?"

The difference between 5-minute human feedback loops and 25-minute autonomous runs is often a single tool installation.

### 3. Should I ask the user more questions?

Before diving into implementation, consider reverse-prompting:
- "The PRD describes 8 art cards — are any of these more important than others? Should I prioritize?"
- "Some of these involve complex math (Fourier, reaction-diffusion). Want me to research best practices first, or just go?"
- "I can build these in parallel (faster) or sequentially (easier to debug). Preference?"

Users often have context they haven't shared. A 30-second question can save 30 minutes of rework.

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
