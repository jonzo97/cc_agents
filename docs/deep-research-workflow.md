# Deep Research Workflow

A repeatable system for writing research prompts (for Gemini Deep Research or similar), ingesting results, extracting actionable insights, and producing PRDs.

**Status:** Pattern defined. Agent and command to be built.

---

## The Flow

```
1. PROMPT       Write a structured research prompt using project context
     ↓           (CC writes it, user runs it in Gemini Deep Research)
2. INGEST       Import raw research output back into project
     ↓           (user pastes or saves file)
3. SQUEEZE      Extract every actionable insight, pattern, constraint
     ↓           (CC agent — "juice the citrus")
4. TRIAGE       Route extracted insights to the right destination
     ↓           (see Output Routing below)
5. PRD          Generate implementation-ready PRD (if building something)
     ↓           (CC agent — structured output)
6. EXECUTE      Run the PRD through the pipeline
     ↓           (/pipeline or manual build)
7. ARCHIVE      Store prompt + output + extract + PRD for reference
```

## Output Routing

Not every research output becomes a PRD. After squeezing, triage each insight:

| Destination | When | What Happens Next |
|-------------|------|-------------------|
| **PRD → build** | Research reveals something actionable to implement | Generate PRD, run `/pipeline` |
| **Best practices doc** | Research reveals patterns, constraints, or conventions | Write to `cc_agents/docs/` as reference material |
| **NotebookLM podcast** | Research covers broad concepts good for personal learning | Upload to NotebookLM, generate audio overview |
| **Topic file** | Research surfaces tools, repos, or links to explore later | Add to `second-brain/topics/` |

A single research output often routes to multiple destinations. The squeeze phase should tag each extracted insight with its destination.

## Directory Structure

```
research/
├── active/                    # Current research cycle
│   ├── prompt.md              # The prompt sent to Gemini
│   ├── output.md              # Raw Gemini deep research output
│   ├── extract.md             # Squeezed insights (the juice)
│   └── prd.md                 # Generated PRD
└── archive/                   # Completed cycles
    └── YYYY-MM-DD_topic/
        ├── prompt.md
        ├── output.md
        ├── extract.md
        └── prd.md
```

## Phase 1: Prompt Generation

The prompt should be structured to produce output the agent can efficiently process later.

### Prompt Template

```markdown
# Deep Research: [Topic]

## Context
I'm building [project description]. The current architecture is [brief summary].
I need to understand [specific area] because [why it matters to the project].

## What I Need

Research the following, prioritizing practical implementation guidance over theory:

1. [Specific question 1]
2. [Specific question 2]
3. [Specific question 3]

## Output Format

Structure your response as follows:

### Key Findings
Numbered list of the most important discoveries, each with:
- **Finding:** One sentence summary
- **Evidence:** Source/link/example
- **Implication for my project:** How this affects what I should build

### Recommended Approach
Based on findings, what specific approach should I take? Include:
- Architecture/pattern to follow
- Libraries/tools to use (with versions)
- Order of implementation

### Constraints & Gotchas
Things that will break if I get them wrong. For each:
- **Constraint:** What the rule is
- **Why:** What goes wrong if violated
- **How to verify:** How to test I got it right

### What Others Are Doing
3-5 examples of similar projects/implementations, with links. Note what they got right and wrong.

### Questions I Should Be Asking
Things I didn't think to ask about but should consider.

## Scope Boundaries
- Focus on [specific tech/framework], not [excluded alternatives]
- Prioritize [production-ready / prototype-speed / learning-oriented]
- My experience level: [EE background, familiar with Python, learning SWE patterns]
```

### Key Principles for Good Prompts

1. **Specify output format.** If you don't, you get an essay. Structured output = easier extraction.
2. **Include project context.** Generic research produces generic answers. "I'm building X with Y" gets targeted advice.
3. **Ask for constraints explicitly.** "What will break?" is more useful than "what should I do?"
4. **Request "what others are doing."** This surfaces blind spots — things you don't know to ask about.
5. **Ask for "questions I should be asking."** The meta-question that catches unknown unknowns.

## Phase 3: Squeeze (Extract)

The extraction agent reads the raw output and produces a structured extract:

### Extract Template

```markdown
# Extract: [Topic]
**Source:** research/active/output.md
**Date:** YYYY-MM-DD

## Hard Constraints
(Things that MUST be true for the implementation to work)
- [ ] Constraint 1: ...
- [ ] Constraint 2: ...

## Architecture Decisions
(Choices to make, with the research-recommended option)
- **Decision:** [what to decide]
  **Recommended:** [option] because [reason from research]
  **Alternative:** [option] — rejected because [reason]

## Patterns to Follow
(Specific code patterns, library usage, API conventions)
1. Pattern: ...
   Example: ...

## Anti-Patterns to Avoid
(Things that seem obvious but fail)
1. Don't do X because Y

## Libraries & Tools
(Specific recommendations with versions)
| Tool | Version | Purpose | Install |
|------|---------|---------|---------|

## Open Questions
(Things the research couldn't fully answer — need more investigation or user decision)
- [ ] Question 1
- [ ] Question 2

## Blind Spots Surfaced
(Things you didn't know to ask about)
- ...
```

## Phase 4: PRD Generation

The PRD agent takes the extract and produces an implementation-ready PRD following the project's standard PRD format. The extract's constraints become the PRD's technical requirements. The extract's architecture decisions become the PRD's approach.

## Future: Agent & Command

**Planned agent:** `research-liaison` — specializes in writing research prompts and squeezing outputs.

**Planned command:** `/deep-research <topic>` — generates the prompt, sets up the directory, and after user pastes the output, runs squeeze → PRD → pipeline.

**Automation gap:** Gemini Deep Research doesn't have a public API for programmatic access. The manual step (copy prompt → run in Gemini → paste output) stays manual for now. The value is in making everything around that step systematic.
