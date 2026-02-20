# Deep Research: Claude Opus 4.6 Effort Parameter — Optimization Patterns for Multi-Agent Systems

## Context
I run a multi-agent system on Claude Code where different agents serve different roles: Scout (exploration), Research (deep investigation), Planner (task decomposition), Builder (implementation), Reviewer (quality checks). Currently each uses a fixed model (Haiku, Sonnet, or Opus). Anthropic introduced an "effort" parameter for Claude models that adjusts reasoning depth. At medium effort, Opus 4.6 reportedly matches Sonnet 4.5's SWE-bench score while using 76% fewer tokens. This could dramatically change my cost structure.

## What I Need

1. **Effort parameter mechanics** — How exactly does it work? What are the levels? How does it affect reasoning, code quality, and token consumption? Concrete benchmarks and examples.

2. **Optimal effort per task type** — What effort level is appropriate for: code exploration, technical research, planning/decomposition, straightforward implementation, code review? Evidence-based recommendations.

3. **Dynamic effort escalation** — Can I start an agent at low effort and escalate to high if it hits problems (test failures, ambiguity)? How would this work in practice? Any examples of adaptive effort systems?

4. **Single model with effort vs multi-model** — Is it better to use Opus-at-varied-effort for all agents, or keep the current Haiku/Sonnet/Opus split? Cost comparison, quality comparison, implementation complexity.

5. **Community adoption** — Are Claude Code users actively using the effort parameter? What patterns have emerged? Any gotchas or unexpected behaviors?

## Output Format

### Key Findings
### Recommended Approach
### Constraints & Gotchas
### What Others Are Doing
### Questions I Should Be Asking

## Scope Boundaries
- Claude Code multi-agent context specifically
- Focus on the 5 agent roles I use: scout, research, planner, builder, reviewer
- Cost optimization is a primary concern (I pay per token)
- Feb 2026 — latest available information
