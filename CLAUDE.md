# cc_agents — Project Instructions

## What This Is
R&D repo for Claude Code agent definitions. Agents are defined in `agents/*.md` and deployed to `~/.claude/agents/` via `./deploy.sh`.

## Key Principle
With Opus 4.6, the main Claude instance IS the orchestrator. Agent definitions should be lean (50-100 lines), focused, and trust Claude's native capabilities. No ceremony, no over-engineering.

## File Structure
```
agents/          # Agent definitions (the deliverable)
deploy.sh        # Deploy to ~/.claude/agents/
test_scenarios/  # Sample codebases for testing
archive/v2/      # Historical reference (old 6-agent system)
```

## Cross-Project Inbox
If user says **"check your inbox"**, read `~/.claude/cross-project.md` for pending messages. Update status after reading/acting. See `docs/cross-project-patterns.md`.

## When Editing Agents
- Keep definitions under 100 lines
- Focus on what makes this agent different from default Claude behavior
- Don't duplicate Claude's built-in capabilities (tool selection, error handling, etc.)
- Test with real tasks before deploying
