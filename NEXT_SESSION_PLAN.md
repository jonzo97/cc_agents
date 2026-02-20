# Next Session Plan — cc_agents v4.3

Stashed tasks for a proper planning session. Compact-safe: this file captures everything needed to pick up where we left off.

---

## 1. Build→Test→Review Feedback Loop (Priority: HIGH) — DONE (2026-02-20)

Built: `agents/tester.md`, updated `teams/build-review-loop.md` (inner loop), `teams/full-pipeline.md` (Phase 3 tester), `commands/pipeline.md` (execution steps), `docs/orchestrator-guide.md` (testing strategy section).

---

## 2. Serena Audit (Priority: MEDIUM) — DONE (2026-02-20)

Audited: zero projects have Serena in `.mcp.json`. Deprecated: variants moved to `archive/serena-variants/`, `--serena` flag removed from `deploy.sh`, Serena references stripped from team presets. Deep research prompt written at `research/prompts/11_serena-lsp-ai-coding.md`. Mailbox note to SB already sent (previous session).

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
