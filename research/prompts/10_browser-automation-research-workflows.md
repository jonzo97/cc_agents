# Deep Research: Browser Automation for AI Research Workflows

## Context
I have paid subscriptions to Gemini, Claude, and Perplexity but none provide API keys with consumer plans. I'm stuck using web UIs for things like Gemini Deep Research and Perplexity Labs. I want to automate repetitive browser interactions: running batches of research prompts, downloading results, exporting conversations. I've heard Comet browser might help. I also already have a Playwright recipe for general browser automation.

## What I Need

1. **Comet browser** — What is it? How does it work for AI workflow automation? Can it automate Gemini Deep Research runs? What about Perplexity? Setup complexity, cost, limitations.

2. **Playwright for AI web UIs** — Can Playwright automate interactions with Gemini, Perplexity, or Claude web interfaces? Login handling, prompt submission, result extraction. ToS considerations — which services allow browser automation of their UIs?

3. **Perplexity Labs automation** — Can I automate downloading or exporting Perplexity research outputs? Scheduled research, auto-export, RSS-like feeds of results?

4. **Gemini export workarounds** — Gemini doesn't export to .md easily but has "Save to Google Docs." Can I automate: run prompt → save to Docs → pull from Google Drive → convert to markdown? What's the pipeline?

5. **Ethical and ToS landscape** — Which of these automation approaches are explicitly allowed, in a gray area, or explicitly prohibited by the respective services' ToS? I don't want to get my accounts banned.

6. **Alternative approaches** — Are there legitimate ways to access these services programmatically that I'm missing? Academic API access, partner programs, workarounds that don't violate ToS?

## Output Format

### Key Findings
### Recommended Approach
### Constraints & Gotchas
### What Others Are Doing
### Questions I Should Be Asking

## Scope Boundaries
- Consumer subscriptions only (no enterprise/API tier budget)
- Must not violate ToS (I value my accounts)
- Python/Playwright/Node.js tooling preferred
- WSL2/Linux environment
