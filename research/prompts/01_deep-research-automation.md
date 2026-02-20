# Deep Research: Automating Multi-Model Research Pipelines

## Context
I'm building a personal AI development toolkit (agent orchestration, knowledge management, research workflows). I currently use Gemini Deep Research manually — I write prompts, run them in the Gemini web UI (3 at a time, unlimited), then paste outputs back into my Claude Code projects. This manual loop is my biggest workflow bottleneck. I have paid subscriptions to Gemini, Claude, and Perplexity but none provide API keys with consumer subscriptions, so I'm limited to web UIs and CLIs.

I've heard of DeerFlow (ByteDance's LangGraph-based deep research framework) and LangChain/LangGraph for orchestrating multi-model research. I also use Perplexity for daily research and would love to automate downloading their "labs" outputs.

## What I Need

Research the following, prioritizing practical solutions I can implement this month:

1. **DeerFlow** — What exactly is it? How does it work? Can it replace my manual Gemini Deep Research workflow? What models does it support? Does it require API keys or can it work with existing subscriptions? What's the setup complexity?

2. **LangChain/LangGraph for research orchestration** — Can these orchestrate research across multiple models without paid API keys? What's the minimum viable setup? Are there templates for deep research workflows?

3. **Browser automation for research** — Can tools like Playwright, Puppeteer, or Comet browser automate running Gemini Deep Research prompts? What about auto-downloading Perplexity results? Legal/ToS considerations?

4. **Google Drive as research pipeline** — Gemini can "Save to Google Docs." Can I programmatically pull those docs from Google Drive into my local projects? What APIs or tools exist for this? (I may eventually connect Google Drive to my system anyway.)

5. **Alternative deep research tools** — What open-source or free-tier tools provide deep research capabilities similar to Gemini Deep Research? Storm, Tavily, or others?

## Output Format

### Key Findings
Numbered list of the most important discoveries, each with:
- **Finding:** One sentence summary
- **Evidence:** Source/link/example
- **Implication for my workflow:** How this changes what I should do

### Recommended Approach
Based on findings, what specific approach should I take? Include:
- Immediate solution (this week)
- Medium-term solution (this month)
- Long-term architecture

### Constraints & Gotchas
Things that will break or won't work. For each:
- **Constraint:** What the limitation is
- **Why:** Root cause (API restrictions, ToS, technical limitation)
- **Workaround:** If one exists

### What Others Are Doing
3-5 examples of developers who've automated their research workflows. Links and approaches.

### Questions I Should Be Asking
Things I didn't think to ask about but should consider.

## Scope Boundaries
- Focus on solutions that work WITHOUT paid API keys (I have subscriptions, not API access)
- Prioritize open-source and self-hosted over SaaS
- I'm comfortable with Python, Docker, and CLI tools
- My experience level: EE background, strong with scripting and automation, learning SWE patterns
