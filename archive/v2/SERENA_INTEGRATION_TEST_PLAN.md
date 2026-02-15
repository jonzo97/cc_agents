# Serena Integration Test Plan

**Version:** 2.1.0
**Date:** 2025-01-06
**Status:** Ready for Execution

---

## Prerequisites

### 1. Verify Serena MCP Server Installation

```bash
# Check uvx is installed
$HOME/.local/bin/uvx --version
# Should output: uvx 0.8.24 or similar

# Check Serena MCP config
grep -A 10 "serena" ~/.claude.json
# Should show MCP server configuration

# Verify MCP server health (requires new Claude session)
claude mcp list
# Should show: serena - ✓ Connected
```

### 2. Test Scenarios Available

```bash
ls /home/jorgill/cc_agents/test_scenarios/
# Should show: simple_cli, react_library, max_plugin, legacy_codebase, empty_project
```

---

## Test Suite 1: Serena MCP Connectivity

### Test 1.1: MCP Server Status

**Objective:** Verify Serena MCP server is running and accessible

**Steps:**
1. Start fresh Claude Code session
2. Run: `claude mcp list`
3. Verify "serena" shows as "✓ Connected"

**Expected Result:**
```
serena: /home/jorgill/.local/bin/uvx --from git+https://github.com/oraios/serena ... - ✓ Connected
```

**Pass Criteria:** Green checkmark, no errors

---

### Test 1.2: Serena Tools Available

**Objective:** Confirm all 18 Serena tools are exposed

**Steps:**
1. In Claude Code, ask: "What Serena tools are available?"
2. Verify tool list includes:
   - get_symbols_overview
   - find_symbol
   - find_referencing_symbols
   - insert_after_symbol
   - insert_before_symbol
   - replace_symbol_body
   - search_for_pattern
   - list_dir
   - find_file

**Expected Result:** All 9+ core tools listed

**Pass Criteria:** Core semantic tools available

---

## Test Suite 2: Scout Agent with Serena

### Test 2.1: React Library Exploration (Semantic)

**Objective:** Scout uses Serena tools for semantic analysis

**Steps:**
1. `cd /home/jorgill/cc_agents/test_scenarios/react_library`
2. Invoke Scout agent
3. Observe tool usage in output

**Command:**
```bash
cd /home/jorgill/cc_agents/test_scenarios/react_library
# In Claude Code: "Use the scout agent to explore this codebase"
```

**Expected Behavior:**
- ✅ Uses `get_symbols_overview` for code files
- ✅ Uses `find_symbol` to locate components
- ✅ Uses `find_referencing_symbols` for dependencies
- ❌ Avoids `grep` for code search
- ❌ Avoids reading entire files for structure

**Success Metrics:**
- Semantic analysis in output: "semantic_tools_used": true
- Token usage: <80 tokens (down from ~95)
- Confidence score: ≥0.90 (up from ~0.88)
- Accurate component count via LSP

**Pass Criteria:** Scout uses Serena tools, provides accurate semantic analysis

---

### Test 2.2: Python Project Exploration

**Objective:** Scout semantic analysis works for Python

**Test Project:** Simple CLI (Python)

**Steps:**
1. `cd /home/jorgill/cc_agents/test_scenarios/simple_cli`
2. Invoke Scout agent
3. Verify Python LSP usage

**Expected Serena Usage:**
- `get_symbols_overview main.py`
- `find_symbol "main"`
- `find_referencing_symbols` for imports

**Pass Criteria:** Python symbols correctly identified

---

### Test 2.3: Unknown Codebase (Max Plugin)

**Objective:** Scout handles language with limited/no LSP support

**Test Project:** max_plugin (JavaScript for Max)

**Steps:**
1. `cd /home/jorgill/cc_agents/test_scenarios/max_plugin`
2. Invoke Scout
3. Observe fallback behavior

**Expected Behavior:**
- Attempts Serena tools first
- Falls back to traditional tools if LSP unavailable
- Still provides analysis (lower confidence OK)

**Pass Criteria:** Graceful fallback, no errors

---

## Test Suite 3: Builder Agent with Serena

### Test 3.1: Add Method to Class (Symbol-Level Edit)

**Objective:** Builder uses `insert_after_symbol` instead of Edit

**Simulation:**
```
Task: Add getUserById method to User class

File: test_scenarios/simple_cli/src/user.py (create if needed)

Expected Builder Action:
insert_after_symbol "User.__init__" "
    def get_user_by_id(self, user_id):
        return self.users.get(user_id)
"
```

**Manual Test:**
1. Create simple Python class in test scenario
2. Ask Builder to add a method
3. Verify uses `insert_after_symbol`

**Pass Criteria:**
- Uses symbol-level editing
- Correct indentation automatically
- No line number counting

---

### Test 3.2: Modify Function Body (replace_symbol_body)

**Objective:** Builder modifies function implementation semantically

**Simulation:**
```
Task: Update handleClick function to log event

Expected Builder Action:
replace_symbol_body "handleClick" "
  console.log('Button clicked:', event);
  onClick?.(event);
"
```

**Manual Test:**
1. Use React component from react_library scenario
2. Ask Builder to modify existing function
3. Verify uses `replace_symbol_body`

**Pass Criteria:**
- Uses semantic replacement
- Maintains syntax
- Faster than traditional Edit

---

### Test 3.3: Add Import Statement (insert_before_symbol)

**Objective:** Builder adds imports precisely

**Simulation:**
```
Task: Add lodash import to utils.ts

Expected Builder Action:
insert_before_symbol "export" "import _ from 'lodash';"
```

**Manual Test:**
1. Pick TypeScript file from react_library
2. Ask Builder to add import
3. Verify uses `insert_before_symbol`

**Pass Criteria:**
- Correct placement (before first export/function)
- No manual line counting
- Proper syntax

---

## Test Suite 4: End-to-End Integration

### Test 4.1: Full Scout → Plan → Build (Serena-Enhanced)

**Objective:** Entire workflow uses Serena appropriately

**Steps:**
1. `cd /home/jorgill/cc_agents/test_scenarios/react_library`
2. Full orchestration: "Explore this codebase and add a new Card component"
3. Observe tool usage throughout

**Expected Flow:**
```
Orchestrator → Scout (Serena-enhanced exploration)
           ↓
         Planner (creates task list)
           ↓
         Builder (Serena symbol-level edits)
           ↓
         Complete
```

**Scout Phase Verification:**
- Uses `get_symbols_overview` for existing components
- Uses `find_symbol` to understand structure
- Token usage <80 (semantic analysis)

**Builder Phase Verification:**
- Uses `insert_after_symbol` to add Card component
- Uses `insert_before_symbol` for imports
- No line-based Edit for code

**Pass Criteria:**
- All agents use appropriate tools
- No redundant grep/Edit for code
- Workflow completes successfully

---

## Test Suite 5: Performance Comparison

### Test 5.1: Token Usage Comparison

**Objective:** Measure token reduction from Serena

**Baseline (Phase 2, no Serena):**
- Scout: ~95 tokens/scenario
- Builder: ~512 tokens/workflow

**Target (Phase 2.5, with Serena):**
- Scout: <80 tokens (15% reduction)
- Builder: <400 tokens (20% reduction)

**Test Method:**
1. Run Scout on react_library with Serena
2. Count tokens in JSON output
3. Compare to baseline

**Success:** ≥10% token reduction

---

### Test 5.2: Accuracy Comparison

**Objective:** Verify semantic analysis is more accurate

**Metrics:**
- Component count accuracy
- Dependency mapping accuracy
- Architecture pattern detection

**Test:**
1. Scout react_library with Serena
2. Manually verify:
   - Components counted correctly (LSP-based)
   - Dependencies traced accurately
   - Architecture pattern precise

**Baseline Accuracy:** ~80% (grep-based estimates)
**Target Accuracy:** >95% (LSP semantic understanding)

**Success:** Measurably more accurate

---

### Test 5.3: Speed Comparison

**Objective:** Verify Serena is faster (after initialization)

**Operations to Time:**

| Operation | Traditional | Serena | Expected Speedup |
|-----------|-------------|--------|------------------|
| Find class definition | grep + verify | find_symbol | 5x faster |
| Get file structure | Read full file | get_symbols_overview | 3x faster |
| Add method to class | Read + Find + Edit | insert_after_symbol | 7x faster |

**Test:** Time each operation

**Success:** Serena operations faster after LSP warmup

---

## Test Suite 6: Edge Cases

### Test 6.1: Unsupported Language Fallback

**Objective:** Verify graceful fallback for unsupported languages

**Test File:** Create `.xyz` file (unsupported)

**Expected:**
- Serena attempts LSP
- Falls back to traditional tools
- No errors, operation completes

**Pass Criteria:** Graceful degradation

---

### Test 6.2: Large File Handling

**Objective:** Verify Serena handles large files efficiently

**Test:**
1. Create 1000-line TypeScript file
2. Use `get_symbols_overview`
3. Verify performance

**Expected:**
- Symbol overview faster than reading
- Accurate results
- No timeout

**Pass Criteria:** Handles large files well

---

## Validation Checklist

### Phase 2.5 Complete When:

- [ ] Serena MCP server connected (Test 1.1)
- [ ] All 18 tools available (Test 1.2)
- [ ] Scout uses semantic tools (Test 2.1)
- [ ] Scout semantic analysis accurate (Test 2.2)
- [ ] Scout fallback works (Test 2.3)
- [ ] Builder uses insert_after_symbol (Test 3.1)
- [ ] Builder uses replace_symbol_body (Test 3.2)
- [ ] Builder uses insert_before_symbol (Test 3.3)
- [ ] End-to-end workflow successful (Test 4.1)
- [ ] Token usage reduced ≥10% (Test 5.1)
- [ ] Accuracy improved to >95% (Test 5.2)
- [ ] Serena operations faster (Test 5.3)
- [ ] Fallback handling works (Test 6.1)
- [ ] Large files handled (Test 6.2)

---

## Regression Testing

### Ensure Phase 1 & 2 Still Work:

- [ ] Phase 1 tests still pass (15/15)
- [ ] Phase 2 tests still pass (10/10)
- [ ] End-to-end integration test passes
- [ ] No functionality broken

**Command:**
```bash
python3 /home/jorgill/cc_agents/scripts/test_scout_simulation.py
python3 /home/jorgill/cc_agents/scripts/test_planner_simulation.py
python3 /home/jorgill/cc_agents/scripts/test_builder_simulation.py
python3 /home/jorgill/cc_agents/scripts/test_context_manager_simulation.py
python3 /home/jorgill/cc_agents/scripts/test_end_to_end.py
```

**Expected:** All tests pass (26/26 total)

---

## Manual Testing Guide

### Quick Serena Validation (5 minutes)

**Test 1: Check Connection**
```bash
# New Claude session required for MCP to connect
claude mcp list
# Look for: serena - ✓ Connected
```

**Test 2: Use Serena Tool**
```
# In Claude Code:
cd test_scenarios/react_library
# Ask: "Use get_symbols_overview on src/App.tsx"
# Should show: classes, functions, exports
```

**Test 3: Scout with Serena**
```
# Ask: "Use scout agent to explore this codebase"
# Watch for semantic tool usage in output
```

**Pass if:** All 3 tests work without errors

---

## Troubleshooting

### Issue: "Serena not connected"

**Diagnosis:**
```bash
claude mcp list
# If shows: serena - ✗ Failed to connect
```

**Fixes:**
1. Check uvx installed: `$HOME/.local/bin/uvx --version`
2. Test Serena directly: `$HOME/.local/bin/uvx --from git+https://github.com/oraios/serena serena start-mcp-server --help`
3. Check logs: Claude Code console output
4. Restart Claude Code

---

### Issue: "Tool not found"

**Diagnosis:** Serena connected but tools not available

**Fix:**
1. Restart Claude Code session
2. Verify tool list with: "What tools are available?"
3. Check Serena version compatibility

---

### Issue: "LSP timeout"

**Diagnosis:** Serena operations timing out

**Common Causes:**
- First use (LSP initialization)
- Very large project
- Missing language server

**Fix:**
- Wait for initialization (one-time)
- Index project: check `.serena/cache`
- Install language servers if missing

---

## Success Criteria Summary

| Metric | Baseline (Phase 2) | Target (Phase 2.5) | Status |
|--------|-------------------|-------------------|--------|
| Scout token usage | ~95 | <80 | ⏳ Pending |
| Builder token usage | ~512 | <400 | ⏳ Pending |
| Scout accuracy | ~80% | >95% | ⏳ Pending |
| Grep usage (code files) | High | Minimal | ⏳ Pending |
| Edit usage (code files) | High | Minimal | ⏳ Pending |
| Serena tool usage | 0% | >80% | ⏳ Pending |
| All tests passing | 26/26 | 26/26 | ⏳ Pending |

---

## Next Steps After Testing

1. Document results in `PHASE_2.5_TEST_RESULTS.md`
2. Update `VALIDATION_REPORT.md` with Serena metrics
3. Update `README.md` to v2.1.0
4. Create `SERENA_INTEGRATION.md` guide
5. Mark Phase 2.5 complete

---

**Test Plan Version:** 1.0
**Created:** 2025-01-06
**Status:** Ready to Execute
**Requires:** Fresh Claude Code session with Serena MCP connected
