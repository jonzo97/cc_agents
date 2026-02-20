# Future TODOs

Captured improvements and research tasks for future sessions.

---

## Recipes

- [ ] **Fill out recipe book** — Docker Compose, lighthouse, npm/pip audit, act
- [ ] **Add recipes for common RAG patterns** — chunking strategies, embedding selection, retrieval patterns

## Deep Research

- [ ] **Research deep-research automation** — Investigate DeerFlow, LangChain, and other frameworks for automating the Gemini Deep Research handoff. Goal: reduce the manual copy-paste step. Check if Gemini has programmatic access yet, or if DeerFlow/LangChain can orchestrate multi-model research pipelines.
- [x] ~~**Build `research-liaison` agent**~~ — Done. See `agents/research-liaison.md`.
- [ ] **Build `/deep-research` command** — Agent exists (`research-liaison`), command TBD. Slash command that generates the prompt, sets up the directory, and after user pastes the output, runs squeeze → PRD → pipeline.

## Cross-Project

- [ ] **Research cross-project delegation patterns** — How to spawn work across projects more formally. Handoff prompts, shared directory conventions, status tracking. Consider whether this needs a lightweight framework or if shared mailbox + peek is sufficient.

## Dashboard

- [ ] **Update dashboard** — Add recipes section, cross-project patterns, deep research workflow. Reflect current file structure.

## Context Estimator

- [ ] **Fix or replace context estimator status line** — Previously attempted a context usage estimator in the Claude Code status line. Currently broken. Options: (a) find an existing community solution, (b) fix our implementation, (c) build from scratch. Could be a standalone shareable plugin repo eventually, but lives in cc_agents for now.

## README

- [ ] **Update README** — Add recipes, new docs, future todos reference. Keep it share-worthy.
