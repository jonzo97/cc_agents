---
name: deep-research
description: Orchestrate the deep research pipeline — run existing prompts, generate new ones, or squeeze raw research output. Triggers on "deep research", "research prompt", "run prompt NN", "squeeze research", "squeeze this".
---

# Deep Research Skill

Orchestrate the prompt → Gemini → squeeze → route pipeline for deep research workflows.

## Modes

Detect which mode from user input:

### Mode A: Run Existing Prompt
**Triggers:** "run prompt 3", "deep research prompt 03", "research prompt 5"

1. Parse the prompt number from user input
2. Read matching file from `~/cc_agents/research/prompts/` (glob `NN_*.md` where NN is zero-padded)
3. Display the full prompt in a code block for easy copying
4. Create `~/cc_agents/research/active/` if it doesn't exist
5. Tell user:
   ```
   Copy the prompt above into Gemini Deep Research.
   When done, save the output and give me the file path (or paste it).
   ```
6. When user provides the file path or content → switch to Mode C

### Mode B: Generate New Prompt
**Triggers:** "deep research on [topic]", "research prompt about [topic]", "new research prompt for [topic]"

1. Read the template from `~/cc_agents/docs/deep-research-workflow.md` (Phase 1: Prompt Generation section)
2. Generate a structured prompt following the template pattern:
   - `# Deep Research: [Topic]`
   - `## Context` — infer from current project state
   - `## What I Need` — 3-5 specific research questions based on topic
   - `## Output Format` — use standard template (Key Findings, Recommended Approach, Constraints & Gotchas, What Others Are Doing, Questions I Should Be Asking)
   - `## Scope Boundaries` — infer from topic
3. Auto-increment prompt number: count existing files in `~/cc_agents/research/prompts/`, next is N+1
4. Save to `~/cc_agents/research/prompts/NN_topic-slug.md`
5. Display for user, same handoff as Mode A step 5

### Mode C: Squeeze Existing Output
**Triggers:** "squeeze this research", "squeeze [filepath]", user provides a file path after Mode A/B

1. Read the research output file
2. Spawn the research-liaison agent:
   ```
   Task(
       subagent_type="general-purpose",
       description="Squeeze research output",
       prompt="You are the research-liaison agent. Read ~/cc_agents/agents/research-liaison.md for your full instructions.

   Squeeze this research output: [filepath]

   Follow your full flow: Squeeze → Route → Update Tracker → Archive.
   Write extract to ~/cc_agents/research/active/extract.md.
   Read ~/second-brain/topics/research-switchboard.md for routing destinations.
   Report what you extracted and where you routed each insight."
   )
   ```
3. Report results to user when agent completes

## Key References

- Prompt template: `~/cc_agents/docs/deep-research-workflow.md`
- Existing prompts: `~/cc_agents/research/prompts/`
- Squeeze agent: `~/cc_agents/agents/research-liaison.md`
- Routing table: `~/second-brain/topics/research-switchboard.md`
- Active workspace: `~/cc_agents/research/active/`

## Important

- **Never run Gemini** — that's the user's manual step via web UI
- **Never auto-execute PRDs** — squeeze agent drafts only, user runs `/pipeline`
- **Always display prompts** for user to copy — no clipboard automation
- **Create `research/active/` directory** if it doesn't exist before any file operations
