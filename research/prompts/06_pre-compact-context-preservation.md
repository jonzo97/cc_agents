# Deep Research: Context Preservation Across Compaction in Claude Code

## Context
I use Claude Code heavily and frequently hit the 200K context limit. When I compact, I lose context and the agent experiences "amnesia" — forgetting what we were working on, re-exploring files it already read, and making decisions that contradict earlier ones. I previously built a pre-compact hook system that saved state to markdown files, but it was overcomplicated and fragile.

Claude Code's built-in compaction has improved (it summarizes the conversation), but I still notice quality drops after compaction, especially for multi-step tasks. I want to find the most token-efficient way to preserve critical context.

## What I Need

1. **How Claude Code compaction works in Feb 2026** — What does the built-in compaction actually preserve? What's lost? Has it improved recently? Are there settings or flags that affect compaction quality?

2. **Community approaches to context preservation** — What are Claude Code power users doing? Pre-compact hooks, memory bank patterns, checkpoint files, session logs. What's working in practice vs theory?

3. **Token-efficient context restoration** — After compaction, what's the minimum context needed to resume effectively? Is it better to restore a structured summary (500 tokens) or detailed state (5000 tokens)? What information has the highest "context value per token"?

4. **Memory Bank patterns** — Structured markdown files (active_context.md, learnings.md, decisions.md) that persist across compactions. Best practices for what to store, how to format for LLM consumption, and how to keep them updated without overhead.

5. **Hook-based automation** — PreCompact hooks that automatically snapshot state. PostCompact/SessionStart hooks that restore context. What's the right level of automation vs manual checkpointing?

6. **Alternative approaches** — Git-based state (commit before compact, restore after), file-based memory, MCP memory servers, external state stores. What works for a single developer workflow?

## Output Format

### Key Findings
Numbered list, each with:
- **Finding:** One sentence summary
- **Evidence:** Source/link
- **Implication for my workflow:** What I should change

### Recommended Approach
- Minimal viable preservation (what to do right now)
- Optimal preservation (if I invest time to build it)
- What NOT to preserve (common mistakes, over-preservation)

### Constraints & Gotchas
### What Others Are Doing
### Questions I Should Be Asking

## Scope Boundaries
- Claude Code specifically
- Token efficiency is critical — the preservation system shouldn't eat the context it's trying to save
- Must work with hooks (shell scripts triggered by Claude Code events)
- Current setup: Memory Bank markdown files + git-based snapshots
