# PRD: Self-Hosted Research Automation Pipeline
**Status:** Draft (generated from research extract)
**Source:** Gemini Deep Research -- "Automating AI Research Workflows" (2026-02-20)
**Priority:** Medium-term (Tier 2 and 3 of recommended strategy)

---

## Problem Statement

The current research workflow is: manually prompt Gemini Deep Research -> wait -> Export to Docs -> rclone sync -> manually invoke research-liaison agent to squeeze and route. This involves significant context switching and manual coordination. The research identified a clear path to automate the full cycle.

## Objective

Build a tiered research automation pipeline that progressively reduces manual steps:
1. **Tier 1 (done):** rclone cloud-sync bridge (already operational)
2. **Tier 2 (this PRD):** browser-use MCP for Claude Code + automated squeeze/route
3. **Tier 3 (future PRD):** self-hosted DeerFlow 2.0 as local research OS

---

## Tier 2: Agentic Browser + Auto-Squeeze

### What We're Building

An MCP-integrated browser automation layer that allows Claude Code to:
1. Open Gemini in a persistent Chrome session
2. Submit a research prompt
3. Wait for completion
4. Export to Google Drive
5. Trigger rclone sync
6. Auto-invoke the research-liaison squeeze/route flow

### Technical Requirements

| Requirement | Detail |
|---|---|
| **MCP Transport** | HTTP/SSE (NOT stdio). Stdio drops after 60s. |
| **Browser Profile** | Persistent Chrome profile with Google login cached |
| **Bot Mitigation** | Human-like timing delays; no high-frequency clicks |
| **State Management** | Research tracker (`.research-tracker.json`) updated at each step |
| **Error Handling** | Retry on 429; fallback to manual if bot-detected |

### Components

1. **mcp-browser-use server**
   - Source: github.com/Saik0s/mcp-browser-use
   - Runs as HTTP daemon (persistent, survives long tasks)
   - Configured with persistent Chrome profile path
   - Added to cc_agents or second-brain `.mcp.json`

2. **Research submission skill**
   - A Claude Code skill or agent instruction that:
     - Opens Gemini Deep Research URL
     - Pastes the prompt from `~/cc_agents/research/prompts/`
     - Clicks "Research" and polls for completion
     - Clicks "Export to Docs"
   - Must handle: loading delays, error states, quota exhaustion

3. **Auto-sync trigger**
   - After export, run: `rclone sync gdrive:"AI Research/pending/" ~/.research-staging/ --drive-export-formats md`
   - Detect the new file by comparing against `.research-tracker.json`
   - Update tracker status: `downloaded`

4. **Auto-squeeze trigger**
   - On new file detection, invoke research-liaison agent
   - Agent runs the squeeze template from `deep-research-workflow.md`
   - Writes extract to `cc_agents/research/active/extract.md`
   - Routes per routing table
   - Updates tracker: `squeezed` -> `routed`

### Architecture

```
User: "Run research prompt #04"
  |
  v
Claude Code (with mcp-browser-use)
  |-> Opens Gemini in persistent Chrome
  |-> Submits prompt, waits for completion
  |-> Clicks Export to Docs
  |
  v
rclone sync (triggered by Claude Code or cron)
  |-> Pulls new .md from Drive to .research-staging/
  |
  v
Research Scanner (.claude/tools/research_scanner.sh)
  |-> Detects new file, updates tracker
  |
  v
Research Liaison Agent (squeeze + route)
  |-> Reads raw output
  |-> Produces extract.md
  |-> Routes to cc_agents/docs, pipeline, second-brain/topics
  |-> Archives to research/archive/YYYY-MM-DD_topic/
  |-> Updates tracker to "routed"
```

### Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Bot detection bans Google account | Medium | High | Conservative timing, persistent profile with real history, rate-limit to 2-3 runs/day |
| Gemini UI changes break automation | High | Medium | browser-use's semantic DOM interpretation is resilient to UI changes; fall back to manual |
| Long research tasks drop MCP connection | High (if stdio) | High | Mandate HTTP/SSE transport only |
| Google API instability (429 errors) | Known issue (2026-02-20) | Medium | Retry with exponential backoff; degrade to manual export |

### Open Design Questions

- [ ] Should the browser-use MCP live in cc_agents or second-brain .mcp.json?
- [ ] How to securely store the Chrome profile path and credentials?
- [ ] Should we batch-submit prompts (risky for bot detection) or single-submit with delays?
- [ ] What's the minimum safe delay between automated Gemini interactions?

---

## Tier 3: Self-Hosted DeerFlow 2.0 (Future)

### Outline Only (Full PRD When Ready)

**What:** Deploy DeerFlow 2.0 via Docker Compose as a local research engine, replacing Gemini Deep Research entirely for most queries.

**Key decisions needed:**
- Local model selection (DeepSeek-R1:32b via Ollama? Llama 3?)
- Search provider (DuckDuckGo for free, Tavily for quality)
- Integration point (MCP server? Direct API? CLI?)
- How DeerFlow's "Skills" system maps to cc_agents agent definitions

**Prerequisites:**
- Tier 2 operational and validated
- Ollama running reliably on local hardware
- DeerFlow v2.0 stability confirmed (check GitHub issues)

---

## Success Criteria

- [ ] Can submit a research prompt from Claude Code without leaving the IDE
- [ ] Research output arrives in `.research-staging/` within 5 minutes of completion
- [ ] Squeeze/route executes automatically on new file detection
- [ ] Zero manual copy-paste in the entire chain
- [ ] Bot detection rate < 1 incident per 20 runs
- [ ] Full audit trail in `.research-tracker.json`

---

## Implementation Estimate

| Phase | Effort | Dependencies |
|---|---|---|
| Install + configure mcp-browser-use | ~30 min | npm/pip install, Chrome profile setup |
| Write research submission skill | ~1 hour | mcp-browser-use working |
| Wire auto-sync trigger | ~20 min | rclone already configured |
| Wire auto-squeeze trigger | ~30 min | research-liaison agent already built |
| End-to-end testing (3 prompts) | ~1 hour | All above working |
| **Total Tier 2** | **~3-4 hours** | |
