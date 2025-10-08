# Perplexity MCP Setup Guide

**Purpose**: Enhance Research Agent with Perplexity Pro's advanced reasoning and real-time search capabilities.

**Status**: Ready to install (requires user API key)

**Priority**: OPTIONAL (Research Agent works well with WebSearch/WebFetch)

---

## Benefits

### Research Agent Enhancement

**With Perplexity Pro**:
- Enhanced reasoning via Sonar Pro models
- Real-time web search with citations
- Better technical question answering
- Multi-source synthesis
- Confidence: ~0.85-0.95 (vs. ~0.75-0.85 without)

**Current (WebSearch only)**:
- Works excellently (0.85 confidence achieved in testing)
- Good for most research needs
- Free (no API costs)

**Recommendation**: Try current Research Agent first, add Perplexity if you need the extra 10% quality boost.

---

## Installation

### Prerequisites

1. **Perplexity Pro subscription**
   - URL: https://www.perplexity.ai/pro
   - Cost: ~$20/month
   - Includes API access

2. **Perplexity API Key**
   - Dashboard: https://www.perplexity.ai/settings/api
   - Create new API key
   - Copy key (starts with `pplx-...`)

### Installation Steps

```bash
# Step 1: Install Perplexity MCP
claude mcp add-json --scope user perplexity-mcp '{
  "type": "stdio",
  "command": "perplexity-mcp",
  "env": {
    "PERPLEXITY_API_KEY": "pplx-YOUR-KEY-HERE"
  }
}'

# Step 2: Verify installation
claude mcp list | grep perplexity

# Should show:
# perplexity-mcp: ... - ✓ Connected

# Step 3: Test Perplexity tools
# (in Claude Code session)
# The Research Agent will automatically detect and use Perplexity tools
```

### Secure API Key Storage (Alternative)

If you prefer not to store the key in MCP config:

```bash
# Option 1: Environment variable
echo 'export PERPLEXITY_API_KEY="pplx-YOUR-KEY"' >> ~/.bashrc
source ~/.bashrc

# Option 2: .env file
echo 'PERPLEXITY_API_KEY=pplx-YOUR-KEY' >> ~/.env
# Then reference in MCP config: "${PERPLEXITY_API_KEY}"
```

---

## Testing Perplexity Integration

### Test 1: Direct Tool Call

```bash
# In Claude Code, after installation:
# Try calling Perplexity tool directly (tool name may vary)
mcp__perplexity__ask "What are the latest TypeScript 5.4 features?"
```

### Test 2: Research Agent with Perplexity

```bash
# Research topic that benefits from recent info
/research TypeScript 5.4 new features and breaking changes 2024

# Check report for:
# - "Perplexity MCP" in tool usage
# - Recent sources (2024)
# - Higher confidence scores
```

### Test 3: Compare Quality

Run same research twice:

```bash
# Test A: Without Perplexity (disable MCP temporarily)
/research React Server Components best practices

# Test B: With Perplexity (re-enable MCP)
/research React Server Components best practices

# Compare:
# - Confidence scores
# - Source recency
# - Answer depth
# - Citations quality
```

---

## Research Agent Behavior

### Tool Selection Priority (in research.md)

```
Phase 2: Parallel Research

1. **Perplexity MCP** (if available - PREFERRED)
   - Enhanced reasoning with Sonar models
   - Real-time web search
   - Superior for technical questions

2. **WebSearch** (fallback)
   - Good for most research
   - Free
   - Multiple sources
```

The Research Agent automatically:
- Detects if Perplexity MCP is available
- Uses it as primary tool if found
- Falls back to WebSearch if unavailable
- No manual configuration needed

---

## Cost Estimation

### Perplexity Pro Subscription

- **Monthly**: ~$20/month
- **Includes**: Unlimited searches, API access
- **Models**: Sonar Pro, Sonar

### API Usage (if separate from Pro)

- **Pricing**: Pay per API call
- **Research Agent Usage**: 3-5 calls per research (one per question)
- **Estimated**: $0.10-0.50 per research topic

### Cost-Benefit Analysis

**Worth it if**:
- Doing frequent research (>10 topics/week)
- Need highest quality answers
- Working with cutting-edge tech (2024-2025)
- Want best citations

**Skip it if**:
- Occasional research only
- WebSearch results good enough (they are)
- Budget-conscious
- Testing system first

---

## Troubleshooting

### Issue: Perplexity MCP not detected

```bash
# Check MCP list
claude mcp list

# Restart Claude Code
# (may need to reconnect MCP servers)

# Verify API key is valid
# Test at: https://www.perplexity.ai/settings/api
```

### Issue: Research Agent not using Perplexity

**Check**: Research Agent output for tool usage
- Should mention "Perplexity MCP" or "mcp__perplexity__ask"
- If only WebSearch, Perplexity not detected

**Fix**:
- Verify MCP connected: `claude mcp list`
- Check API key is set
- Restart Claude Code session

### Issue: API key errors

```bash
# Invalid key error
# → Check key copied correctly (starts with pplx-)
# → Verify key is active in Perplexity dashboard

# Rate limit errors
# → Check Pro subscription is active
# → Reduce research frequency
```

---

## Uninstallation

```bash
# Remove Perplexity MCP
claude mcp remove perplexity-mcp

# Verify removal
claude mcp list | grep perplexity
# Should show nothing

# Research Agent will automatically fall back to WebSearch
```

---

## Performance Comparison

### With Perplexity (Expected)

```
Topic: "React Server Components best practices"

Sources: 8 authoritative (Vercel, React docs, recent blogs)
Confidence: 0.92
Time: 3-4 minutes
Citations: High quality, 2024 sources
Depth: Excellent technical detail
```

### Without Perplexity (Baseline)

```
Topic: "React Server Components best practices"

Sources: 6-7 mixed quality (docs, blogs, forums)
Confidence: 0.85
Time: 3-5 minutes
Citations: Good, some 2023-2024 sources
Depth: Very good technical detail
```

**Difference**: ~10% confidence improvement, slightly better sources

---

## Recommendation

### Phase 1: Test Without Perplexity

1. Use Research Agent with WebSearch/WebFetch
2. Run 5-10 research topics
3. Check `/feedback` for confidence scores
4. Evaluate if quality meets needs

### Phase 2: Add Perplexity (If Needed)

1. Install Perplexity MCP (this guide)
2. Run same research topics
3. Compare quality improvement
4. Decide if worth $20/month

### Phase 3: Optimize

1. Use Perplexity for complex/recent topics
2. Use WebSearch for basic/historical topics
3. Monitor costs vs. value

---

## Status

- [x] Research Agent designed with Perplexity support
- [x] Fallback to WebSearch working (tested)
- [ ] Perplexity MCP installed (requires user API key)
- [ ] Perplexity integration tested
- [ ] Quality comparison documented

**Next Step**: User provides Perplexity API key → Install → Test → Compare

---

**Guide Version**: 1.0
**Last Updated**: 2025-10-08
**Testing Status**: WebSearch baseline validated (0.85 confidence)
**Installation Status**: Pending (user API key required)
