# Next Session Plan — cc_agents v4.3

Stashed tasks for a proper planning session. Compact-safe: this file captures everything needed to pick up where we left off.

---

## 1. Build→Test→Review Feedback Loop (Priority: HIGH) — DONE (2026-02-20)

Built: `agents/tester.md`, updated `teams/build-review-loop.md` (inner loop), `teams/full-pipeline.md` (Phase 3 tester), `commands/pipeline.md` (execution steps), `docs/orchestrator-guide.md` (testing strategy section).

---

## 2. Serena Audit (Priority: MEDIUM)

### The Problem
Serena variants exist but may not actually be in use. Need to verify:
- Is Serena configured and working in any active project?
- Are the Serena variants being deployed and selected?
- Does `deploy.sh` / `init.sh` correctly install Serena variants?

### Action Items
- [ ] Audit: check if Serena MCP is configured in any project's `.mcp.json`
- [ ] Test: run a Serena agent against a real project, verify LSP tools work
- [ ] Decide: keep, fix, or deprecate Serena variants based on findings

### Cross-Project: Research task for second-brain
Send second-brain a mailbox message requesting a Serena deep dive for NotebookLM podcast:
- What Serena actually is (LSP wrapper as MCP server)
- How it compares to native Claude Code tools
- Setup requirements and pain points
- Whether it's worth the complexity for this use case

---

## 3. Dashboard Update (Priority: LOW)

After feedback loop and Serena work are done, update the dashboard to reflect:
- [ ] Test agent card
- [ ] Feedback loop visualization (inner + outer loops)
- [ ] Ralph card (exists but not shown as a card)
- [ ] More detail on hook mechanics
- [ ] Research switchboard / cross-project flow
- [ ] Serena status (working or deprecated)

---

## 4. Also Pending (from inbox / earlier work) — DONE (2026-02-20)

- [x] Research-liaison agent (`agents/research-liaison.md`) — delivered
- [x] Google Drive recipe (`recipes/google-drive.md`) — delivered
- [x] Ingestion detection pattern — baked into research-liaison
- [x] README/dashboard updated
- [x] Committed and pushed

---

## Session Strategy

1. **Compact** after saving this file
2. **New session:** Plan v4.3 (feedback loop + test agent + Serena audit)
3. **Build** the planned changes
4. **Then:** Research-liaison agent + Google Drive recipe (separate session, may involve second-brain coordination)
