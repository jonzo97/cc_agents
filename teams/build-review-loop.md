# Team Preset: Build-Review Loop

Builder implements, reviewer validates, fix loop until PASS. The core quality pattern.

## When to Use

- Implementing features where quality matters (production code)
- Any task with clear acceptance criteria that can be mechanically verified
- When you want automated review without manual checking

## Team Structure

| Role | Agent | Count | Model |
|------|-------|-------|-------|
| Lead | You (main Claude) | 1 | opus |
| Builder | builder | 1 | sonnet |
| Tester | tester | 1 | sonnet |
| Reviewer | reviewer | 1 | haiku |

## Architecture: Inner Loop + Outer Gate

```
                INNER LOOP (fast, per-task)
                ┌──────────────────────────┐
                │                          │
Plan → Build task → Test → PASS → next task → ... → all tasks done
                │                          │
                └── FAIL → fix task ───────┘
                          (max 3 per task)

                OUTER GATE (once, after all tasks)
All tasks done → Review → PASS → Done
                    │
                    └── FAIL (architecture) → Re-plan → restart inner loop
                         (max 1 re-plan)
```

### Inner Loop (Builder ↔ Tester)

After each builder task completes, the tester runs immediately:
- **PASS** — builder moves to next task
- **FAIL** — tester creates fix tasks, builder picks them up
- Max 3 fix attempts per task. If still failing, escalate to human.

### Outer Gate (Reviewer)

After ALL tasks pass the inner loop, the reviewer does a final acceptance check:
- **PASS** — done, ship it
- **FAIL with fix tasks** — builder picks them up, tester re-validates
- **FAIL with architecture flag** — planner re-plans (max 1 re-plan cycle, then escalate)

## Setup Steps

1. **Create team:**
   ```
   TeamCreate with team_name "build-<feature>"
   ```

2. **Create implementation tasks** (from an approved plan):
   ```
   TaskCreate: "Implement <feature part 1>"
   TaskCreate: "Implement <feature part 2>"
   TaskCreate: "Review all implementation changes"
     → addBlockedBy: [impl-task-1, impl-task-2]
   ```

3. **Spawn builder + tester:**
   ```
   Task with team_name, subagent_type "builder", name "builder-1"
   Task with team_name, subagent_type "general-purpose", name "tester-1"
   ```
   Tester uses `agents/tester.md` prompt. Both run concurrently — tester claims test tasks as builder completes implementation tasks.

4. **Inner loop runs automatically:**
   - Builder completes task → tester picks up test task
   - PASS → builder continues; FAIL → tester creates fix tasks → builder picks them up
   - Max 3 fix cycles per task

5. **Spawn reviewer** (after all tasks pass inner loop):
   ```
   Task with team_name, subagent_type "general-purpose", name "reviewer-1"
   ```

6. **Handle review results:**
   - PASS: Merge/commit, shut down team
   - FAIL with fixes: Builder picks up fix tasks, tester re-validates
   - FAIL with architecture flag: Re-plan (max 1 cycle, then escalate to human)

## Tips

- Builder and reviewer should NOT work on the same files simultaneously.
- The reviewer is read-only — it creates fix tasks, it doesn't fix code.
- Default max 3 review cycles. For complex domains (math, graphics, protocols), allow up to 5. If still failing, escalate to human.
- For Serena-enabled projects, use serena/builder and serena/reviewer variants.
- Combine with Ralph (stop hook) for fully autonomous build loops.
- **For visual/frontend projects:** The reviewer should use Playwright (or similar headless browser) to take screenshots and verify functional output. Syntax-only review is insufficient for UI work.

## Integration with Ralph

For fully autonomous operation, install `ralph-v2.sh` as a stop hook on the builder.
The builder will keep working through tasks until Ralph's dual-condition gate confirms
both completion signal AND passing tests.

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/ralph-v2.sh",
        "timeout": 30
      }]
    }]
  }
}
```
