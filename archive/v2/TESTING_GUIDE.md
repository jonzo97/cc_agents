# Testing Guide - v2.2.0-alpha/beta

**Purpose**: Validate Phase 1 fixes and prepare for beta release

**Target**: All 6 agents tested, confidence logging verified, builder reliability confirmed

---

## Quick Validation (15 minutes)

**Goal**: Verify Phase 1 critical fixes work

### Test 1: Confidence Logging (5 min)

```bash
cd ~/mcu-competitive-analysis

# Run a simple Scout exploration
/scout-explore

# After Scout completes, check database
python3 << 'EOF'
import sqlite3, os
db = sqlite3.connect(os.path.expanduser("~/.claude/memory.db"))
cursor = db.cursor()
cursor.execute("SELECT confidence FROM handoffs WHERE confidence IS NOT NULL ORDER BY timestamp DESC LIMIT 1")
result = cursor.fetchone()
if result and result[0] is not None:
    print(f"✅ SUCCESS: Confidence logged: {result[0]}")
else:
    print("❌ FAILED: No confidence score found")
db.close()
EOF
```

**Expected**: ✅ SUCCESS message with confidence score (0.0-1.0)

### Test 2: Builder Error Handling (5 min)

```bash
# Trigger a simple build task that might fail
# (or manually test builder timeout handling)

# After build completes (or fails), check for graceful error handling
/workflow-status

# Look for:
# - Builder status (completed or failed with reason)
# - No hung/timeout workflows
```

**Expected**: Builder completes or fails gracefully (no hangs)

### Test 3: Feedback Analysis (5 min)

```bash
# After running 2-3 workflows above
/feedback

# Look for:
# - Confidence scores present (not NULL)
# - Success rates calculated
# - Recommendations provided
```

**Expected**: Feedback shows confidence scores, not "Missing confidence: 100%"

---

## Comprehensive Testing (2-3 hours)

### Test Suite 1: Scout Agent (30 min)

#### Test 1.1: Basic Exploration

```bash
cd ~/mcu-competitive-analysis
/scout-explore
```

**Expected Output**:
- Project type identified
- Tech stack listed
- Architecture pattern described
- Confidence score calculated
- Handoff message with confidence

**Validation**:
- [ ] Exploration completes in <3 minutes
- [ ] Confidence score ≥0.7
- [ ] Database handoff logged (check with query)
- [ ] No Serena errors (or graceful fallback)

#### Test 1.2: Unknown Technology Trigger

```bash
# Explore a project with unfamiliar tech
cd /path/to/unfamiliar/project
/scout-explore
```

**Expected**:
- Lower confidence (<0.7)
- Recommends Research Agent
- Handoff to "research" not "planner"

**Validation**:
- [ ] Confidence reflects unknowns
- [ ] Research recommendation present
- [ ] Handoff decision logic works

### Test Suite 2: Research Agent (45 min)

#### Test 2.1: Technical Research

```bash
/research ARM Cortex-M MCU comparative analysis 2024
```

**Expected Output**:
- 3-5 research questions generated
- Multiple authoritative sources
- Confidence score ≥0.7
- Handoff to planner with confidence

**Validation**:
- [ ] Research completes in <10 minutes
- [ ] Sources include recent (2024) information
- [ ] Confidence score logged to database
- [ ] Report comprehensive and actionable

#### Test 2.2: Research Quality (With vs Without Perplexity)

**Part A: Without Perplexity** (baseline)
```bash
/research TypeScript 5.4 new features
```
- Note confidence score, source quality, time

**Part B: With Perplexity** (if installed)
```bash
# Install Perplexity (see PERPLEXITY_SETUP.md)
/research TypeScript 5.4 new features
```
- Compare confidence, sources, quality

**Validation**:
- [ ] Both produce good results
- [ ] Perplexity shows ~10% confidence improvement (optional)
- [ ] Confidence scores logged for both

### Test Suite 3: Planner Agent (45 min)

**Note**: Planner was UNTESTED in Phase 2 - priority for beta

#### Test 3.1: Simple Planning Task

```bash
# After Scout exploration
# Request: "Create a plan to add a new data export feature"
# (Manual invocation - no slash command)
```

**Expected Output**:
- Task breakdown (5-10 tasks)
- Dependencies identified
- Time estimates provided
- Risk assessment included
- Confidence score calculated
- User approval requested

**Validation**:
- [ ] Plan is clear and actionable
- [ ] User prompted for approval
- [ ] Confidence score ≥0.7
- [ ] Handoff to builder logged after approval

#### Test 3.2: Complex Planning with Research

```bash
# After Research Agent provides findings
# Request: "Create implementation plan for [research topic]"
```

**Expected**:
- Integrates research findings
- Higher confidence (research backing)
- References research artifact

**Validation**:
- [ ] Plan incorporates research insights
- [ ] Confidence reflects research quality
- [ ] Research artifact referenced

### Test Suite 4: Builder Agent (60 min)

**Note**: Builder had 62.5% failure rate - priority for validation

#### Test 4.1: Simple Implementation

```bash
# After Planner creates approved plan
# Builder should execute TodoWrite tasks
```

**Expected**:
- Tasks completed in order
- Tests written (if applicable)
- Checkpoints created
- Confidence score calculated
- Handoff to orchestrator

**Validation**:
- [ ] All tasks completed OR failures documented
- [ ] No timeouts (or graceful handling)
- [ ] Error recovery works (if errors occur)
- [ ] Confidence score logged
- [ ] Success rate >80%

#### Test 4.2: Error Recovery

```bash
# Manually trigger an error scenario:
# - Permission denied file
# - Timeout simulation
# - Test failure
```

**Expected**:
- Retry with backoff (for retryable errors)
- Checkpoint created before risky operations
- Rollback on failures
- Graceful escalation on blockers

**Validation**:
- [ ] Errors handled gracefully (no crashes)
- [ ] Retry logic works (max 3 attempts)
- [ ] Timeout warnings work (90% threshold)
- [ ] User notified of blockers

### Test Suite 5: Context Manager (30 min)

#### Test 5.1: Manual Compaction

```bash
# When context usage >70%
/compact-status

# Review recommendations
# Trigger manual compaction if needed
```

**Expected**:
- Current usage displayed
- Recommendations provided
- Compaction successful (if triggered)
- No loss of critical context

**Validation**:
- [ ] Status command works
- [ ] Recommendations accurate
- [ ] Compaction reduces tokens >40%
- [ ] Critical context preserved

#### Test 5.2: Auto-Compaction

```bash
# Continue working until context reaches 80%
# Auto-compaction should trigger
```

**Expected**:
- Auto-trigger at 80%
- Emergency compact at 95%
- Graceful handling
- No data loss

**Validation**:
- [ ] Auto-trigger works
- [ ] Emergency handling works
- [ ] Database events logged

### Test Suite 6: Orchestrator (45 min)

#### Test 6.1: Intent Detection

Test each intent pattern:

```bash
# Intent: Explore
"Explore this codebase and suggest improvements"

# Intent: Research
"Research React Server Components best practices"

# Intent: Plan
"Create a plan to implement feature X"

# Intent: Build
"Build the approved feature plan"
```

**Expected**:
- Correct agent invoked for each intent
- Workflow coordinated properly
- Handoffs logged

**Validation**:
- [ ] Intent detection accuracy >80%
- [ ] Correct agent triggered each time
- [ ] Workflow state managed

#### Test 6.2: Auto-Research Trigger

```bash
# Scout should trigger research if confidence <0.7
/scout-explore /unfamiliar/tech/project
```

**Expected**:
- Scout completes with low confidence
- Orchestrator auto-triggers Research
- Research investigates unknowns
- Planner receives both Scout + Research

**Validation**:
- [ ] Low confidence detected
- [ ] Research auto-triggered
- [ ] Workflow continues to Planner

---

## Test Scenarios by User Story

### Scenario 1: Complete Workflow (Scout → Research → Plan → Build)

```bash
cd ~/new-project
User: "Explore this codebase, research any unfamiliar technologies, create an implementation plan for feature X, and build it"
```

**Steps**:
1. Orchestrator detects multi-step intent
2. Scout explores codebase
3. Research investigates unknowns (if confidence <0.7)
4. Planner creates plan
5. User approves plan
6. Builder implements
7. All handoffs logged with confidence

**Validation**:
- [ ] Full workflow completes
- [ ] All handoffs logged
- [ ] Confidence scores present
- [ ] Success rate >70%

### Scenario 2: Research-Only

```bash
User: "/research Max for Live MIDI plugin development best practices 2024"
```

**Steps**:
1. Research Agent triggered
2. Generates 3-5 questions
3. Parallel research via WebSearch/Perplexity
4. Report generated with confidence
5. Handoff to planner (or direct to user)

**Validation**:
- [ ] Research completes in <10 min
- [ ] Confidence ≥0.7
- [ ] Report actionable
- [ ] Handoff logged

### Scenario 3: Bug Fix (Scout → Builder)

```bash
User: "Fix the authentication timeout bug"
```

**Steps**:
1. Scout locates auth code
2. Builder creates fix with tests
3. Tests pass
4. Completion logged

**Validation**:
- [ ] Bug located quickly
- [ ] Fix implemented with tests
- [ ] No regressions
- [ ] Confidence scores logged

---

## Database Validation Queries

### Check Confidence Scores

```python
import sqlite3, os

db = sqlite3.connect(os.path.expanduser("~/.claude/memory.db"))
cursor = db.cursor()

# Total handoffs
cursor.execute("SELECT COUNT(*) FROM handoffs")
total = cursor.fetchone()[0]

# Handoffs with confidence
cursor.execute("SELECT COUNT(*) FROM handoffs WHERE confidence IS NOT NULL")
with_conf = cursor.fetchone()[0]

# Calculate percentage
percent = (with_conf / total * 100) if total > 0 else 0

print(f"Handoffs with confidence: {with_conf}/{total} ({percent:.1f}%)")
print(f"Target: 100% (was 0% in Phase 2)")

# Show recent handoffs
cursor.execute("""
    SELECT from_agent, to_agent, confidence, timestamp
    FROM handoffs
    ORDER BY timestamp DESC
    LIMIT 10
""")
print("\nRecent Handoffs:")
for row in cursor.fetchall():
    conf = row[2] if row[2] is not None else "NULL"
    print(f"{row[3]}: {row[0]} → {row[1]} | Confidence: {conf}")

db.close()
```

**Expected**: 100% confidence coverage (not NULL)

### Check Builder Success Rate

```python
import sqlite3, os

db = sqlite3.connect(os.path.expanduser("~/.claude/memory.db"))
cursor = db.cursor()

# Builder workflows
cursor.execute("""
    SELECT COUNT(*), SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END)
    FROM workflows
    WHERE current_agent='builder'
""")
total, completed = cursor.fetchone()

success_rate = (completed / total * 100) if total > 0 else 0

print(f"Builder Success Rate: {success_rate:.1f}%")
print(f"Completed: {completed}/{total}")
print(f"Target: >80% (was 37.5% in Phase 2)")

db.close()
```

**Expected**: Success rate >80%

---

## Troubleshooting Test Failures

### Issue: Confidence still NULL

**Check**:
1. Agent prompts updated? (check ~/.claude/agents/*.md version numbers)
2. Database handoff code executing? (add debug logging)
3. workflow_id available? (orchestrator must provide it)

**Fix**:
- Verify agent versions (should be v2.1 or v1.1)
- Check agent is actually using new prompt
- Restart Claude Code session

### Issue: Builder still failing >20%

**Check**:
1. Error types (timeout, permission, test failure)
2. Logs for error handling execution
3. Retry attempts (should see backoff)

**Fix**:
- Review builder.md error handling section
- Increase timeout if needed
- Add more checkpoints

### Issue: Agents not coordinating

**Check**:
1. Workflow IDs present in database?
2. Handoffs table populated?
3. Orchestrator invoking agents?

**Fix**:
- Check orchestrator.md configuration
- Verify database schema correct
- Test agents individually first

---

## Success Criteria Summary

**Beta Release Ready When**:
- [x] Phase 1 critical fixes deployed
- [ ] Confidence logging: 100% (currently 0%)
- [ ] Builder success: >80% (currently 37.5%)
- [ ] All 6 agents tested successfully
- [ ] Real-world validation: 2+ projects
- [ ] Feedback mechanism validates improvements

**Track Progress**:
```bash
# After testing sessions
/feedback

# Check specific metrics
# Run database validation queries above
```

---

**Testing Guide Version**: 1.0
**Last Updated**: 2025-10-08
**Est. Testing Time**: 3-5 hours (comprehensive)
**Quick Validation**: 15 minutes
**Status**: Ready for use
