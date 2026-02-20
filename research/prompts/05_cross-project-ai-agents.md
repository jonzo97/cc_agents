# Deep Research: Cross-Project Coordination for AI Coding Agents

## Context
I run multiple Claude Code instances across different projects (agent orchestration, knowledge management, FPGA tooling). Currently they communicate via a shared markdown "mailbox" file and can peek at each other's files. This works but is primitive — I want to understand if there are better patterns for cross-project delegation and context sharing.

The dream: I'm working in project A, need research done that relates to project B, and can seamlessly hand off the work with full context. Or: project B discovers a pattern that's useful in project A, and the insight flows automatically.

## What I Need

1. **How are developers coordinating multiple AI coding agents across projects?** — Are people running multiple Claude Code / Cursor / Copilot instances with shared context? What patterns have emerged? Monorepo approaches vs polyrepo with shared state?

2. **Shared context mechanisms** — Beyond flat files, what structures work for cross-project context? Shared databases, knowledge graphs, MCP servers that span projects? What's the token cost of loading cross-project context?

3. **Delegation patterns** — How to hand off a task from one agent instance to another with sufficient context. Handoff prompts, structured task descriptions, shared todo lists. What's the minimum viable handoff?

4. **Memory and learning across projects** — How to capture lessons learned in one project and make them available to agents in other projects. MCP memory server, shared knowledge graph, cross-project memory bank patterns.

5. **Automation opportunities** — Git hooks, file watchers, or other triggers that automatically propagate context between projects. CI/CD-style pipelines for knowledge flow.

## Output Format

### Key Findings
Numbered list, each with:
- **Finding:** One sentence summary
- **Evidence:** Source/link
- **Implication for my setup:** What I should try

### Recommended Approach
- What to do now (improve the mailbox pattern?)
- What to build next (shared knowledge layer?)
- What to avoid (over-engineering traps)

### Constraints & Gotchas
### What Others Are Doing
### Questions I Should Be Asking

## Scope Boundaries
- Claude Code specifically, but patterns from other AI coding tools are relevant
- Single developer, multiple projects on one machine (WSL2/Linux)
- Must be low-overhead — I don't want to maintain infrastructure just for coordination
- Python/Bash/Markdown preferred tooling
