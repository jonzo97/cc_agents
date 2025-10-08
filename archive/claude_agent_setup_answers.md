# Claude Agent System Setup Answers

## 1. Immediate Priority
Jon’s immediate priority is to implement the **full Scout–Plan–Build workflow**, with a callable **Research agent** that can be triggered manually or automatically when deeper analysis is required. The goal is to test full orchestration early while keeping the system lean.

## 2. Gemini Setup
The **Gemini Deep Research MCP integration** will be added **later**. For now, Jon will start with a **Claude-only research setup** to simplify development and focus on orchestrator logic. Once the core system is stable, Gemini will be reintroduced for parallel deep research tasks and offloading.

## 3. Primary Use Cases
Jon will use this agent system for:
- Building **internal team utilities** and FAE tooling integrations.
- **Learning new frameworks and agent architectures** for professional development.
- **Personal creative projects**, such as building **VST plugins** and **Ableton Max for Live plugins**.
- Experimenting with **agentic orchestration and AI infrastructure** for both brownfield and greenfield projects.

## 4. Complexity Preference
Start with **Option A** — a minimal, modular system of 2–3 agents (Scout, Planner, Builder) plus a callable Research agent. Once the foundation is validated and useful, expand toward the full architecture including the Context Manager, Orchestrator, and optional Gemini integrations.

## 5. Existing Tools & Workflows
Jon currently uses **Claude Code in the terminal** as his main development environment. He’s experimented with **Warp** and **BMAD**, but found BMAD overly complex. This project is his **first real attempt at orchestrating multiple agents** in Claude to maximize productivity. He’s also open to **exploring new tools and standards** in the orchestration ecosystem and plans to run research prompts to identify **current best practices** and popular frameworks.

## 6. Storage Location
The system will be installed at the **user level** under `~/.claude/agents/` so that agents are accessible across all projects. Once refined, Jon plans to **publish it on GitHub** for feedback and to easily sync between his **home desktop** and **work computer**.

## 7. Additional Design Notes
- The **Research agent** will remain separate for modularity but callable on demand.
- An **Orchestrator agent** (a.k.a. Root Orchestrator) will handle coordination, sequencing, and agent handoffs.
- The architecture will follow the **Scout → Plan → Build** flow, with optional Research integration when deeper analysis is required.
- A **lightweight architectural reference guide** will be created to standardize how agents reference architecture documents and templates.
- **Checkpointing**: Plan milestone reviews for when to revisit Gemini integration after a few successful Claude-only orchestrations.

## 8. Next Steps
1. Create the base `.claude/agents/` directory with Scout, Planner, and Builder configurations.
2. Implement structured JSON handoffs between agents.
3. Add the callable Research agent with minimal integration points.
4. Build out the Orchestrator to manage sequencing and handoffs.
5. Once stable, integrate the Context Manager and prepare for Gemini MCP support.
6. Publish the setup on GitHub with a `README.md` quick start guide.

---

### Usage Note
Place this file in your Claude Code directory and instruct the system:

```
read this, then execute setup
```

This document serves as your unified reference for system setup, architecture alignment, and next actions.

