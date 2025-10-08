# Research Agent Usage Guide

**Version**: 1.0
**Agent**: Research Agent v2.2.0
**Model**: Sonnet
**Status**: Production Ready

## Overview

The Research Agent is an autonomous technical investigator that fills knowledge gaps through deep, parallel research. It's designed to work seamlessly with Scout, Planner, and Builder agents—or standalone for direct research requests.

## When to Use Research Agent

### ✅ Perfect For

- **Unknown Technologies**: "What is Tauri?" "How does Max for Live work?"
- **Best Practices**: "React Server Components patterns" "VST3 plugin architecture"
- **API Documentation**: "Perplexity API reference" "Three.js latest features"
- **Framework Comparisons**: "Tauri vs Electron" "Vite vs Webpack"
- **Recent Developments**: "TypeScript 5.4 changes" "Next.js 15 features"

### ❌ Not Ideal For

- **Code debugging** (use Scout → Builder)
- **Codebase-specific questions** (use Scout)
- **Implementation details** (use Scout + Builder)
- **General knowledge** (just ask Claude directly)

## Three Ways to Trigger Research

### 1. Auto-Triggered (Scout Low Confidence)

**Happens automatically when Scout is uncertain**

```
You: "Explore this Tauri project"

System:
├─ Scout explores codebase
├─ Scout confidence: 0.58 (LOW)
└─ 🔬 Research Auto-Triggered

Research Agent:
├─ Questions:
│   1. What is Tauri's architecture?
│   2. Tauri vs Electron?
│   3. Building Tauri apps?
├─ Sources: 8 (official docs, recent articles)
└─ Confidence: 0.89

→ Planner receives Scout + Research findings
```

**No action required** - happens automatically when needed.

### 2. User Request (Direct)

**Explicitly ask for research**

```
You: "Research Max for Live MIDI processing"

Research Agent:
├─ Questions:
│   1. Max for Live MIDI API?
│   2. MIDI input/output patterns?
│   3. LiveAPI for MIDI?
│   4. Example MIDI devices?
│   5. Best practices?
├─ Perplexity: 5 queries
├─ WebFetch: 6 pages (cycling74.com, GitHub)
└─ Report: art_research_max_midi_20250106

You receive: Executive summary + detailed artifact
```

**Use this when**: You need to learn something before building.

### 3. Planner-Triggered (Unknowns Detected)

**Planner identifies knowledge gaps**

```
You: "Plan a VST3 plugin implementation"

Scout: Explores codebase
Planner: Flags unknowns - "VST3 SDK", "Audio processing"

System asks: "Run research on unknowns?"
You: "Yes"

Research Agent: Investigates VST3
Planner: Creates informed plan
```

**Use this when**: Planning reveals unknowns.

## Example Research Sessions

### Example 1: Learn New Framework

```
🎯 Goal: Understand Svelte before building

You: "Research Svelte 5 runes and reactivity"

Research Agent Output:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 RESEARCH COMPLETE: Svelte 5 Runes

Questions Researched: 5
Sources: 9 (svelte.dev, GitHub, articles)
Confidence: 0.92 ✅

Key Findings:
• Runes replace $: reactive statements in Svelte 5
• $state() creates reactive variables
• $derived() computes values automatically
• $effect() handles side effects
• Migration from Svelte 4 is straightforward

Detailed Report: art_research_svelte5_20250106
  - Complete rune reference
  - Migration guide
  - Code examples
  - Best practices

Recommended Next Steps:
1. Review official migration guide
2. Start with $state and $derived
3. Use $effect sparingly (like React useEffect)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next: Ready to implement? Use Scout→Plan→Build workflow.
```

### Example 2: API Documentation Hunt

```
🎯 Goal: Find Perplexity API docs before integrating

You: "Research Perplexity API authentication and usage"

Research Agent:
Questions:
  1. Perplexity API authentication methods?
  2. API endpoints available?
  3. Rate limits and pricing?
  4. Usage examples?
  5. MCP server integration?

Perplexity Used: YES ✅ (dogfooding!)
  → Used Perplexity to research itself

Output:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 PERPLEXITY API RESEARCH

Key Findings:
• Auth: Bearer token (pplx-xxx)
• Endpoints: /chat/completions (OpenAI compatible)
• Models: sonar-pro, sonar (reasoning optimized)
• Rate Limits: Pro plan - generous
• Pricing: $20/month for 600 queries/day

Code Example Found:
```python
headers = {"Authorization": f"Bearer {api_key}"}
response = requests.post(
    "https://api.perplexity.ai/chat/completions",
    json={"model": "sonar-pro", "messages": [...]}
)
```

Sources:
  - docs.perplexity.ai (official)
  - GitHub examples (community)
  - Recent blog posts (2025)

Confidence: 0.95 ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready to implement!
```

### Example 3: Framework Comparison

```
🎯 Goal: Choose between Tauri and Electron

You: "Research Tauri vs Electron for desktop apps"

Research Agent:
Questions:
  1. Architecture differences?
  2. Performance comparison?
  3. Bundle size differences?
  4. Development experience?
  5. Platform support?

Output:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 TAURI VS ELECTRON COMPARISON

Architecture:
  Tauri: Rust backend + system webview
  Electron: Chromium + Node.js bundled

Performance:
  Tauri: 3-4x faster startup
  Tauri: 10-20x smaller bundles
  Electron: More predictable (bundled Chromium)

Bundle Size:
  Tauri: 3-5 MB (uses system webview)
  Electron: 40-80 MB (bundles Chromium)

Development:
  Tauri: Learning curve (Rust)
  Electron: Easier (JavaScript/TypeScript)
  Both: Similar web frontend

Platform Support:
  Tauri: Windows, macOS, Linux (+ mobile in v2)
  Electron: Windows, macOS, Linux

Recommendation:
  ✅ Tauri if: Performance, size priority
  ✅ Electron if: Consistency, maturity priority

Sources: 12 (official docs, benchmarks, 2024 comparisons)
Confidence: 0.91 ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Perplexity Pro Integration

### Why Use Perplexity?

**Better than WebSearch alone:**
- Enhanced reasoning (Sonar Pro models)
- Real-time information
- Built-in citations
- Context-aware synthesis

### Setup Perplexity

```bash
# Install Perplexity MCP
claude mcp add-json --scope user perplexity-mcp '{
  "type": "stdio",
  "command": "perplexity-mcp",
  "env": {
    "PERPLEXITY_API_KEY": "pplx-YOUR-KEY-HERE"
  }
}'

# Verify installation
claude mcp list | grep perplexity
# Should show: perplexity - ✓ Connected
```

### With vs Without Perplexity

**With Perplexity:**
```
You: "Research Next.js 15 server actions"

Research Agent:
  ✅ Perplexity MCP detected
  → Using Sonar Pro for enhanced reasoning

Result:
  - Synthesized from 8+ sources automatically
  - Recent updates (2024-2025) prioritized
  - Official Next.js docs referenced
  - Confidence: 0.93
```

**Without Perplexity (Fallback):**
```
You: "Research Next.js 15 server actions"

Research Agent:
  ℹ️ Perplexity unavailable, using WebSearch
  → Manual source aggregation

Result:
  - Good coverage (WebSearch + WebFetch)
  - Still finds official docs
  - Confidence: 0.85 (slightly lower)
```

**Both work well**, but Perplexity is faster and more accurate.

## Tips for Effective Research

### 1. Be Specific

```
❌ "Research React"
✅ "Research React 19 Server Components"
✅ "Research React useOptimistic hook"
```

### 2. Include Version/Year

```
❌ "Research TypeScript features"
✅ "Research TypeScript 5.4 new features"
```

### 3. Focus on "How" Questions

```
✅ "How to build Max for Live plugins"
✅ "How to optimize Tauri bundle size"
✅ "How to use Perplexity API"
```

### 4. Use Before Building

```
GOOD WORKFLOW:
  Research → Scout → Plan → Build

AVOID:
  Scout → Plan → Build → "Wait, what's X?" → Research
```

## Research Output

### What You Get

1. **Executive Summary** (<500 tokens)
   - 3-5 key bullet points
   - Immediately actionable insights
   - Confidence score

2. **Detailed Report** (Artifact)
   - All questions answered
   - Full source citations
   - Code examples (if found)
   - Unknowns/gaps flagged

3. **Recommended Actions**
   - Next steps for implementation
   - Areas to focus on
   - Warnings/gotchas

### Confidence Scores

| Score | Meaning | Action |
|-------|---------|--------|
| **0.9-1.0** | Excellent - comprehensive findings | ✅ Proceed with confidence |
| **0.7-0.89** | Good - solid information | ✅ Minor gaps acceptable |
| **0.5-0.69** | Fair - partial answers | ⚠️ May need follow-up |
| **<0.5** | Poor - insufficient info | ❌ Manual research recommended |

## Troubleshooting

### "Research Agent not triggering automatically"

**Check Scout confidence**:
```
Scout should report confidence < 0.7 for auto-trigger.
If confidence is higher, manual research needed.
```

**Workaround**: Request research directly
```
You: "Research [topic] before planning"
```

### "Perplexity MCP not working"

**Verify setup**:
```bash
claude mcp list | grep perplexity
```

**If not connected**:
```bash
# Re-add with correct API key
claude mcp add-json --scope user perplexity-mcp '{
  "type": "stdio",
  "command": "perplexity-mcp",
  "env": {
    "PERPLEXITY_API_KEY": "pplx-YOUR-ACTUAL-KEY"
  }
}'
```

**Fallback**: Research Agent will use WebSearch automatically

### "Low confidence scores"

**Common causes**:
- Niche/uncommon technology (limited documentation)
- Very recent releases (docs not yet comprehensive)
- Proprietary systems (limited public info)

**Solutions**:
1. Accept lower confidence and proceed carefully
2. Supplement with manual research
3. Ask specific sub-questions for better coverage

### "Research taking too long"

**Expected duration**: 3-5 minutes

**If exceeds 10 minutes**:
- Agent will timeout (Orchestrator enforces)
- Partial results will be returned
- Re-run with more specific questions

## Integration with Other Agents

### Research → Planner

```
Research provides context
  ↓
Planner creates informed implementation plan
  ↓
Example: "Based on research, use Tauri v2 with..."
```

### Scout → Research → Planner

```
Scout explores codebase (confidence: 0.62)
  ↓
Research fills knowledge gaps (confidence: 0.88)
  ↓
Planner combines both contexts
  ↓
Better plans with full context
```

### Research Only (Learning Mode)

```
Just want to learn? Use Research directly:

You: "Research GraphQL best practices 2025"
Research Agent: Comprehensive report
You: Read and learn (no implementation needed)
```

## Best Practices

### ✅ DO

- Use Research before building unfamiliar features
- Request research on specific versions/years
- Let auto-trigger work (don't disable)
- Read executive summaries first
- Check confidence scores before proceeding
- Use Perplexity MCP if available

### ❌ DON'T

- Research generic topics (just ask Claude)
- Skip research when Scout confidence is low
- Ignore unknowns flagged by Research
- Research without specific questions
- Disable Perplexity fallback unnecessarily

## Command Reference

| Command | Purpose | Example |
|---------|---------|---------|
| Direct request | Standalone research | "Research Tauri desktop apps" |
| Auto-trigger | (No command needed) | Scout confidence < 0.7 |
| With Scout | Explore + research | "Explore and research this Svelte project" |
| With Planner | Research before plan | "Research and plan VST3 plugin" |

## Next Steps

1. **Try a research query**: "Research [your favorite framework] best practices"
2. **Set up Perplexity**: See Setup section above
3. **Test with Scout**: Let Research auto-trigger on unknown codebase
4. **Read artifacts**: Check `~/.claude/artifacts/research/` for reports

---

**Need Help?**
- Research Agent Config: `~/.claude/agents/research.md`
- Architecture Docs: `~/.claude/AGENT_SYSTEM_ARCHITECTURE.md`
- Main README: `/home/jorgill/cc_agents/README.md`

**Version**: 1.0
**Last Updated**: 2025-01-06
**Agent**: Research v2.2.0

🤖 Generated with [Claude Code](https://claude.com/claude-code)
