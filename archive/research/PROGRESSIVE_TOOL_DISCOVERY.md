# Progressive Tool Discovery vs MCP: A Practical Guide

**Context:** How to efficiently manage tools in Claude Code agents without drowning in tokens.

**Sources:** [Advanced Tool Use (Anthropic)](https://www.anthropic.com/engineering/advanced-tool-use) | [Code Execution with MCP (Anthropic)](https://www.anthropic.com/engineering/code-execution-with-mcp)

---

## The Problem

Loading all tool definitions upfront consumes massive context before work begins:

| Scenario | Token Cost |
|----------|-----------|
| 5 MCP servers, 58 tools | ~55K tokens |
| Add Jira integration | +17K tokens |
| Full enterprise stack | 100K+ tokens |

That's half the 200K context window burned on tool definitions alone.

---

## Three Solutions (Choose by Scale)

### 1. Tool Search Tool (`defer_loading`) — For 20-100 Tools

Mark rarely-used tools as discoverable on-demand instead of loading upfront.

**How it works:**
```json
{
  "tools": [
    {
      "name": "core_file_operations",
      "defer_loading": false
    },
    {
      "name": "github.createPullRequest",
      "description": "Create a pull request",
      "defer_loading": true
    }
  ]
}
```

- Keep 3-5 most-used tools always loaded
- Defer specialized/rarely-used tools
- Claude discovers deferred tools via regex or BM25 search when needed
- **Result: 85% token reduction** (77K -> 8.7K tokens)
- Accuracy improvement: Opus 4 (49% -> 74%), Opus 4.5 (79.5% -> 88.1%)

**MCP integration:**
```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "google-drive",
  "default_config": {"defer_loading": true},
  "configs": {
    "search_files": {"defer_loading": false}
  }
}
```

### 2. Code Execution with MCP — For 100+ Tools

Treat MCP servers as code APIs. Agent writes code that calls tools, processes data locally, returns only final results.

**Architecture:**
```
servers/
├── google-drive/
│   ├── getDocument.ts
│   ├── createDocument.ts
│   └── index.ts
├── salesforce/
│   ├── updateRecord.ts
│   └── index.ts
```

**Agent workflow:**
1. Explore filesystem to find available servers
2. Read only needed tool definition files
3. Write TypeScript/Python to call tools
4. Process/filter data in execution environment
5. Return only summarized results to context

**Example — agent writes this code:**
```python
team = await get_team_members("engineering")
expenses = await asyncio.gather(*[
    get_expenses(m["id"], "Q3") for m in team
])

# Filter locally — only exceeded budgets enter context
exceeded = [
    {"name": m["name"], "spent": total}
    for m, exp in zip(team, expenses)
    if (total := sum(e["amount"] for e in exp)) > budget_limit
]
print(json.dumps(exceeded))  # Only 2-3 results, not 2000+ line items
```

- **Result: 98.7% token reduction** (150K -> 2K tokens)
- Intermediate data never enters model context
- Parallel execution via async patterns
- Error handling in code, not via re-prompting

**Trade-off:** Requires secure sandboxing infrastructure.

### 3. Agent Skills (Progressive Disclosure) — For Custom Workflows

Three-level system matching how Claude naturally navigates information:

**Level 1: Table of Contents (YAML frontmatter)** — Always loaded
```yaml
---
name: api-design
description: Design RESTful APIs following project conventions
---
```
- Metadata only, minimal tokens
- Claude uses this to decide if skill is relevant

**Level 2: Chapter (SKILL.md body)** — Loaded when relevant
- Full instructions and workflow guidance
- **Keep under 500 lines** for optimal performance
- Claude reads via `cat ~/.claude/skills/api-design/SKILL.md`

**Level 3: Appendix (linked files)** — Loaded on demand
- Reference docs, schemas, examples in separate files
- Claude discovers via filesystem navigation
- Unbounded capacity

**Result:** Context-efficient, scalable, natural filesystem interaction.

---

## Decision Matrix

| Tool Set Size | Pattern | Token Savings | Complexity |
|---------------|---------|--------------|------------|
| <20 tools | Direct tool calls | N/A | None |
| 20-100 tools | **Tool Search Tool** | 85% | Low (config only) |
| 100+ tools | **Code Execution** | 98.7% | High (sandboxing) |
| Custom workflows | **Agent Skills** | Variable | Low (markdown files) |

---

## Programmatic Tool Calling (Complementary)

Orthogonal to discovery — instead of N separate tool calls (N inference passes), Claude writes code that orchestrates multiple tools in a single execution.

```python
# Traditional: 5 tool calls = 5 inference passes, all results in context
# Programmatic: 1 code execution, intermediate results stay local

tools = ["get_team", "get_budget", "get_expenses"]
# Claude writes code using all 3, returns only final analysis
```

- **Result: 37% token reduction** on multi-tool workflows
- Opt-in per tool via `allowed_callers: ["code_execution_20250825"]`

---

## Tool Use Examples (Complementary)

JSON schemas define structure but can't express conventions. Provide realistic examples alongside schemas:

```json
{
  "name": "create_ticket",
  "input_schema": { "..." },
  "input_examples": [
    {
      "title": "Login page returns 500 error",
      "priority": "critical",
      "labels": ["bug", "authentication", "production"],
      "escalation": {"level": 2, "notify_manager": true, "sla_hours": 4}
    }
  ]
}
```

- Shows parameter correlations (critical -> escalation required)
- Demonstrates format conventions (date formats, ID patterns)
- **Result: 72% -> 90% accuracy** on complex parameter handling
- Use realistic data (not "example@example.com")
- Show 1-5 examples: minimal, partial, and full specification

---

## What This Means for cc_agents

### Current State
Our agents use ~20 native Claude Code tools (Read, Write, Edit, Bash, Glob, Grep, etc.) plus optional Serena LSP tools. This is well within the "direct calls" tier — no progressive discovery needed for tool definitions.

### Where Progressive Discovery Applies

1. **Agent definitions themselves** — Our agents ARE progressive disclosure. The main Claude instance loads minimal agent descriptions, spawns specialized agents only when needed. This is the right architecture.

2. **Skills integration** — If we build skills that agents use, structure them with the 3-level pattern (frontmatter -> body -> appendix). Keep SKILL.md under 500 lines.

3. **Research agent** — Could benefit from code execution pattern for processing large search result sets. Instead of dumping 100 results into context, write code to filter and summarize locally.

4. **Future MCP expansion** — If projects add many MCP servers (Serena + memory + domain-specific), use `defer_loading` for rarely-used servers.

### Not Applicable (Yet)
- We don't have 100+ tools, so code execution for tool discovery is overkill
- Tool Search Tool requires API-level configuration, not available in Claude Code's agent spawning

---

## Key Takeaways

1. **Context is the bottleneck.** Every token spent on tool definitions is a token not available for reasoning.
2. **Progressive > upfront.** Load what you need, when you need it. This applies to tools, skills, and agent definitions.
3. **Code execution is the endgame** for large tool ecosystems, but only when scale justifies complexity.
4. **Examples beat schemas** for teaching correct tool usage. Show, don't just describe.
5. **Our current architecture is already progressive** — lean agent definitions, spawned on demand, specialized per task.

---

*Last updated: 2026-02-15*
*Based on Anthropic engineering blog posts from Nov 2025 - Feb 2026*
