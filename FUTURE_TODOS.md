# Future TODOs

Captured improvements and research tasks for future sessions.

---

## Deep Research

- [ ] **Research deep-research automation** — Investigate DeerFlow, LangChain, and other frameworks for automating the Gemini Deep Research handoff. Goal: reduce the manual copy-paste step. Check if Gemini has programmatic access yet, or if DeerFlow/LangChain can orchestrate multi-model research pipelines.
- [x] ~~**Build `research-liaison` agent**~~ — Done. See `agents/research-liaison.md`.
- [ ] **Build `/deep-research` command** — Agent exists (`research-liaison`), command TBD. Slash command that generates the prompt, sets up the directory, and after user pastes the output, runs squeeze → PRD → pipeline.

## Cross-Project

- [ ] **Research cross-project delegation patterns** — How to spawn work across projects more formally. Handoff prompts, shared directory conventions, status tracking. Consider whether this needs a lightweight framework or if shared mailbox + peek is sufficient.

## Dashboard

- [ ] **Update dashboard** — Reflect current file structure (skills, 7 agents, no Serena variants). Add cross-project patterns, deep research workflow.

## Context Estimator

- [ ] **Fix or replace context estimator status line** — Previously attempted a context usage estimator in the Claude Code status line. Currently broken. Options: (a) find an existing community solution, (b) fix our implementation, (c) build from scratch. Could be a standalone shareable plugin repo eventually, but lives in cc_agents for now.

## README

- [x] ~~**Update README**~~ — Done (v4.3). Recipes consolidated to skills, agent count updated, Serena refs removed.
