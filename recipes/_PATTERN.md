# Recipe Pattern

A recipe is a minimal reference doc that teaches the agent how to use a tool **directly via Python/Bash** — no MCP server, no tool definitions in context, zero protocol overhead.

## Why Recipes Over MCP

| Approach | Context Cost | Setup |
|----------|-------------|-------|
| MCP server | 7-17K tokens per server (tool definitions loaded upfront) | Separate terminal, running process |
| Direct recipe | 0 tokens upfront, ~50 lines read on-demand | `pip install` and go |

The agent reads the recipe, writes the code, runs it via Bash. Data processing happens in the script — only results enter context.

## Recipe Template

Every recipe follows this structure:

```markdown
# Tool Name

One-line description of what this tool does.

## Install
\`\`\`bash
pip install toolname  # or apt/brew/npm
\`\`\`

## Quick Patterns

### Pattern Name
\`\`\`python
# 3-10 lines showing the most common usage
\`\`\`

### Another Pattern
\`\`\`python
# Another common usage
\`\`\`

## Gotchas
- Things that trip people up
- Version-specific issues
- Common mistakes

## When to Use
- Trigger conditions (when should the agent reach for this?)
```

## Rules

1. **Keep recipes under 60 lines.** If you need more, the tool is too complex for a recipe — write a proper guide in `docs/`.
2. **Show real code, not pseudocode.** Agent will copy and adapt these patterns.
3. **Include install commands.** Agent needs to know how to get the tool.
4. **List gotchas.** The whole point is avoiding the 30-minute debugging loop.
5. **No MCP wrappers.** Recipes are direct library usage. If someone wants MCP, they can use the MCP server.

## How the Agent Uses Recipes

1. Orchestrator identifies project type and task
2. Checks `recipes/` for relevant tools (via tool-catalog.md cross-reference)
3. Reads the recipe (~50 lines, on-demand)
4. Writes a Python/Bash script using the patterns
5. Runs via Bash, captures output
6. Only results enter context — intermediate data stays in the script

## Adding New Recipes

When you find yourself repeatedly explaining how to use a tool to agents, write a recipe. If you catch yourself launching an MCP server just to do something a 10-line Python script could do, write a recipe.
