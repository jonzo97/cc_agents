# Deep Research: Context Window Estimation and Management for LLM Coding Agents

## Context
I use Claude Code (Anthropic's CLI coding agent) extensively. The 200K token context window is the primary constraint on session length. I previously tried building a context usage estimator in the Claude Code status line but it's broken. I want to either find an existing solution or understand what's needed to build one properly.

The problem: I can't see how much context I've used. I either hit the limit unexpectedly or compact too early and lose valuable context. A reliable estimator would let me plan sessions better — knowing "I have ~50K tokens left, enough for 2 more features" vs "I'm at 180K, should compact now."

## What I Need

1. **How Claude Code manages context internally** — What's public about how Claude Code handles the 200K window? How does conversation history, tool calls, tool results, system prompts, and file contents count toward the limit? What happens at compaction — what's preserved vs lost?

2. **Existing context estimation tools** — Has anyone in the Claude Code community built a working context estimator? Check awesome-claude-code lists, GitHub, community forums, Discord. What approaches have been tried? What worked and what didn't?

3. **Token counting approaches** — How do you estimate tokens for Claude models from the outside? tiktoken doesn't work for Claude. Is there a Claude tokenizer? Can you estimate from character count? What's the accuracy of different estimation methods?

4. **Status line plugins for Claude Code** — How does the Claude Code status line API work? What can it display? Are there examples of status line plugins that track usage metrics? What are the technical constraints?

5. **Context preservation strategies** — Beyond estimation, what strategies exist for preserving context across compactions? Memory banks, structured summaries, checkpoint files? What's the state of the art in Feb 2026?

## Output Format

### Key Findings
Numbered list, each with:
- **Finding:** One sentence summary
- **Evidence:** Source/link/example
- **Implication for my workflow:** How this changes my approach

### Recommended Approach
- Immediate: what can I do this week
- If building: architecture for a context estimator plugin
- If buying: which existing tool to use

### Constraints & Gotchas
- Technical limitations of each approach
- Why previous attempts failed (if discoverable)
- Accuracy expectations for token estimation

### What Others Are Doing
3-5 examples of developers managing context in Claude Code or similar tools.

### Questions I Should Be Asking
Things I didn't think to ask.

## Scope Boundaries
- Claude Code specifically (not generic LLM context management)
- Feb 2026 timeframe — solutions must work with current Claude Code version
- Ideally a shareable plugin/tool that others could use too
- Python/TypeScript implementation preferred
