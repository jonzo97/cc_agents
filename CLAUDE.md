# cc_agents — Project Instructions

## What This Is
Public distribution of Claude Code agent definitions. The source of truth is `~/.claude/` (private repo). This repo is a curated snapshot published via the `publish-to-cc-agents` skill.

## Maintenance Flow
```
~/.claude/ (private, source of truth)
    ↓ publish skill
~/cc_agents/ (public, curated export)
    ↓ init.sh
~/my-project/.claude/agents/ (project overrides)
```

Edit agents in `~/.claude/agents/`. When ready to share publicly, run `/publish-to-cc-agents`.

## Key Principle
With Opus 4.6, the main Claude instance IS the orchestrator. Agent definitions should be lean (50-100 lines), focused, and trust Claude's native capabilities. No ceremony, no over-engineering.

## File Structure
```
agents/          # Agent definitions (the deliverable)
skills/          # General-purpose skills (deep-research, agent-launcher)
commands/        # Slash commands (pipeline, team-status)
hooks/           # Quality gate hooks
docs/            # Reference documentation
templates/       # ADR template, etc.
deploy.sh        # Deploy to ~/.claude/agents/ (for users who clone this repo)
init.sh          # Install into a specific project for testing
test_scenarios/  # Sample codebases for validation
```

## Cross-Project Inbox
If user says **"check your inbox"**, read `~/.claude/cross-project.md` for pending messages. Update status after reading/acting. See `docs/cross-project-patterns.md`.

## When Editing Agents
- Keep definitions under 100 lines
- Focus on what makes this agent different from default Claude behavior
- Don't duplicate Claude's built-in capabilities (tool selection, error handling, etc.)
- Test with real tasks before deploying
