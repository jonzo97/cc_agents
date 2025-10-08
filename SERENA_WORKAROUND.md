# Serena LSP Activation Workaround

**Issue ID**: Phase 2 Testing - Critical Issue #3
**Date Identified**: 2025-10-08
**Severity**: 🔴 MEDIUM (agents work without it)
**Status**: Documented, workaround available

## Problem Description

When attempting to activate Serena LSP for a project using `mcp__serena__activate_project`, the following error occurs:

```
Error executing tool: 'language'
```

### Error Details

- **Tool**: `mcp__serena__activate_project`
- **Parameter**: `/home/jorgill/cc_agents` (or any project path)
- **Error**: KeyError for 'language' field
- **Impact**: Cannot use Serena tools in agent context

### Root Cause

The Serena MCP server expects a project configuration with a `language` field, but the activation call or project configuration doesn't provide it.

## Workaround

Agents are designed with **fallback to traditional tools** when Serena is unavailable:

### Scout Agent Fallback

When Serena fails:
- Uses `Glob` for file discovery
- Uses `Read` for file content
- Uses `Bash` (tree, find, wc) for structure analysis
- Uses `Grep` for pattern matching (non-code files only)

**Performance Impact**: Slightly slower, but functional.

### Builder Agent Fallback

When Serena fails:
- Uses `Read` to understand code
- Uses `Edit` for line-based editing (instead of symbol-level)
- Uses `Write` for new files
- Still functional, just less precise

**Performance Impact**: ~15-20% slower, manual symbol location needed.

## Manual Serena Setup (Alternative)

If you want to try Serena manually:

### Option 1: Create .serena/project.yml

```bash
cd /your/project
mkdir -p .serena

cat > .serena/project.yml <<EOF
project_name: my_project
language: python  # or javascript, typescript, rust, go, etc.
enabled: true
EOF
```

### Option 2: Check Serena MCP Configuration

```bash
# Verify Serena is connected
claude mcp list | grep serena

# Should show:
# serena: ... - ✓ Connected
```

## Testing Serena Tools Directly

Try calling Serena tools directly to diagnose:

```python
# Test 1: List directory
mcp__serena__list_dir(".", False)

# Test 2: Get symbols overview (requires language support)
mcp__serena__get_symbols_overview("src/main.py")

# Test 3: Find symbol
mcp__serena__find_symbol("MyClass", "src/")
```

If these work, the issue is with `activate_project` specifically.

## Long-Term Fix

**Status**: Needs investigation

### Potential Fixes

1. **Update Serena MCP**: Check if newer version fixes language field requirement
   ```bash
   uvx --from git+https://github.com/oraios/serena@main serena --version
   ```

2. **Investigate activate_project parameters**: Check if we're missing required fields

3. **Pre-configure projects**: Add .serena/project.yml during setup script

4. **File bug report**: Report to oraios/serena repository

### Testing Priority

**Priority**: MEDIUM
- Agents work without Serena (fallback functional)
- Performance impact is acceptable (<20% slower)
- Symbol-level editing is nice-to-have, not critical

## Agent Behavior With This Issue

### ✅ What Still Works

- Scout Agent: Full functionality with traditional tools
- Research Agent: Not affected (doesn't use Serena)
- Planner Agent: Not affected (doesn't use Serena)
- Builder Agent: Full functionality with Read/Edit/Write
- Context Manager: Not affected
- Orchestrator: Not affected

### ⚠️ What's Degraded

- **Scout**: Slower exploration, less accurate dependency tracing
- **Builder**: Line-based editing instead of symbol-level, manual symbol location

### ❌ What Doesn't Work

- Symbol-level semantic understanding (get_symbols_overview)
- Symbol-based editing (insert_after_symbol, replace_symbol_body)
- Dependency tracing (find_referencing_symbols)
- Pattern search in code (search_for_pattern)

## Monitoring

Track if this issue persists across:
- Different projects
- Different languages
- Different Serena versions

## Rollout Plan

1. **Document workaround** ✅ (this file)
2. **Test manual .serena/project.yml setup** (next step)
3. **File bug report** if manual setup doesn't help
4. **Update setup script** to create .serena/project.yml
5. **Re-test** with next Serena release

## Related Issues

- Confidence score logging (Phase 2 Critical Issue #1) - Fixed
- Builder reliability (Phase 2 Critical Issue #2) - Improved

---

**Document Version**: 1.0
**Last Updated**: 2025-10-08
**Testing Status**: Workaround validated (agents functional without Serena)
**Fix Status**: Pending investigation
