# Agent Changes Log

This file documents changes to agent prompts in `~/.claude/agents/` which are not tracked in git (they're global config files).

## Phase 2 Critical Fixes (2025-10-08)

### Issue: Confidence Score Logging Broken

**Problem**: 100% of handoffs (11/11) had NULL confidence scores, blocking auto-research triggering and performance analysis.

**Fix**: Added comprehensive "Handoff Protocol" sections to all 4 agents that participate in workflow handoffs.

### Changes by Agent

#### 1. scout.md (v2.0 → v2.1)

**Location**: `~/.claude/agents/scout.md`

**Added**:
- `## Handoff Protocol` section (lines 471-573)
- Database logging code with confidence score (REQUIRED, never NULL)
- Handoff decision logic (research if <0.7, else planner)
- Handoff message format template
- Validation checklist (6 items)
- Common mistakes to avoid (3 items)

**Key Features**:
- Python code snippet for SQLite insert with confidence
- Determines next agent based on confidence threshold
- Includes workflow_id, from_agent, to_agent, phase, confidence, timestamp
- Confidence score must be calculated using existing formula from prompt

**Version Update**: 2.0 → 2.1 (Confidence Logging Fixed)

---

#### 2. research.md (v1.0 → v1.1)

**Location**: `~/.claude/agents/research.md`

**Added**:
- `## Handoff Protocol` section (lines 655-767)
- Database logging code with confidence score
- Handoff decision logic (always to planner, but flags low confidence)
- Handoff message format with confidence breakdown
- Validation checklist (7 items)
- Common mistakes to avoid (4 items)

**Key Features**:
- Research always hands to Planner (not conditional)
- Flags low confidence (<0.7) for Planner attention
- Includes artifact ID reference in handoff
- Executive summary requirement (<500 tokens)

**Version Update**: 1.0 → 1.1 (Confidence Logging Fixed)

---

#### 3. planner.md (v1.0 → v1.1)

**Location**: `~/.claude/agents/planner.md`

**Added**:
- `## Handoff Protocol` section (lines 639-775)
- Database logging code with confidence score
- Confidence calculation formula specific to planning
- Handoff message format with plan details
- Validation checklist (8 items)
- Common mistakes to avoid (4 items)

**Key Features**:
- Requires user approval before handoff
- Confidence based on: requirements clarity, risks, unknowns, user feedback
- Hands to Builder after approval
- Includes plan artifact reference

**Version Update**: 1.0 → 1.1 (Confidence Logging Fixed)

---

#### 4. builder.md (v2.0 → v2.1)

**Location**: `~/.claude/agents/builder.md`

**Added**:
- `## Error Handling & Recovery` section (lines 700-819)
  - Timeout management with 90% warning threshold
  - Retry logic with exponential backoff (2, 4, 8 seconds)
  - Error recovery strategy by error type
  - Validation before completion checklist
  - Recovery checklist (8 items)

- `## Handoff Protocol` section (lines 821-967)
  - Database logging code with confidence score
  - Confidence calculation based on build quality
  - Handoff message format with implementation summary
  - Validation checklist (8 items)
  - Common mistakes to avoid (5 items)

**Key Features**:
- Addresses 62.5% failure rate from Phase 2 testing
- Timeout warnings at 90% to allow graceful finalization
- Retry with backoff for transient errors
- Fallback to traditional tools if Serena fails
- Rollback on test failures
- Confidence deducted for failures, timeouts, rollbacks

**Version Update**: 2.0 → 2.1 (Confidence Logging & Error Handling Fixed)

**Special Note**: Builder received most extensive updates due to high failure rate in testing.

---

## Testing Required

All 4 updated agents need to be tested in real workflows to verify:

1. **Confidence scores are logged to database** (currently 0% → target 100%)
2. **Scores are between 0.0-1.0** (validation)
3. **Database inserts succeed** (no NULL values)
4. **Handoff logic works correctly** (research triggered at <0.7)
5. **Builder error handling reduces failures** (62.5% → target <20%)

## Rollback Information

**Backup Location**: None (agents were not versioned before)

**Rollback Instructions**:
1. Revert to git version before this commit
2. Copy agent files from git history if needed
3. Or manually remove Handoff Protocol sections

**Risk**: LOW - Additions are incremental, don't modify existing behavior

## Related Documentation

- `FEEDBACK_HISTORY.md` - Original issue identification
- `KNOWN_LIMITATIONS.md` - Updated with fix status
- `SERENA_WORKAROUND.md` - Serena activation issue (separate)

## Impact

**Before**:
- Confidence scores: 0% logged (11/11 NULL)
- Builder success rate: 37.5% (5/8 failures)
- Auto-research trigger: Not functional

**After** (Expected):
- Confidence scores: 100% logged (target)
- Builder success rate: >80% (target with error handling)
- Auto-research trigger: Functional

## Deployment

**Date**: 2025-10-08
**Method**: Direct edit of global agent files
**Verification**: Run `/feedback` after workflows to check database

---

**Change Log Version**: 1.0
**Last Updated**: 2025-10-08
**Changes**: 4 agents updated (scout, research, planner, builder)
**Lines Added**: ~500 lines across all agents
**Files Modified**: 4 (all in ~/.claude/agents/)
