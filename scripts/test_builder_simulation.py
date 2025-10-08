#!/usr/bin/env python3
"""
Builder Agent Test Simulation
Tests TDD workflow, checkpointing, progress reporting, and error recovery.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
import uuid

# Test configuration
DB_PATH = Path.home() / ".claude" / "memory.db"
SCHEMA_PATH = Path.home() / ".claude" / "schemas" / "builder_data.json"

def load_schema():
    """Load builder data JSON schema."""
    with open(SCHEMA_PATH, 'r') as f:
        return json.load(f)

def validate_builder_data(data, schema):
    """Validate builder data against schema."""
    required_fields = schema.get('required', [])
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    # Validate types
    props = schema.get('properties', {})
    for key, value in data.items():
        if key in props:
            expected_type = props[key].get('type')
            if expected_type == 'integer' and not isinstance(value, int):
                return False, f"Field {key} should be integer"
            elif expected_type == 'boolean' and not isinstance(value, bool):
                return False, f"Field {key} should be boolean"
            elif expected_type == 'string' and not isinstance(value, str):
                return False, f"Field {key} should be string"

    return True, "Valid"

def create_test_workflow(conn, scenario_name):
    """Create a test workflow in the database."""
    workflow_id = f"wf_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"

    conn.execute("""
        INSERT INTO workflows (id, status, current_agent, user_request, created_at)
        VALUES (?, 'in_progress', 'builder', ?, CURRENT_TIMESTAMP)
    """, (workflow_id, f"Test scenario: {scenario_name}"))
    conn.commit()

    return workflow_id

def simulate_builder_workflow(scenario_name, task_count, should_fail=False, fail_at_task=None):
    """Simulate a Builder workflow execution."""

    print(f"\n{'='*60}")
    print(f"Testing Builder: {scenario_name}")
    print(f"{'='*60}")

    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    workflow_id = create_test_workflow(conn, scenario_name)

    # Simulate builder execution
    builder_data = {
        "tasks_completed": 0,
        "total_tasks": task_count,
        "tasks": [],
        "tests_passing": True,
        "checkpoints_created": 0,
        "rollbacks_needed": 0,
        "completion_status": "success",
        "progress_updates": []
    }

    # Simulate task execution
    for i in range(1, task_count + 1):
        task_name = f"Task {i}: Implement feature {i}"

        # Check if this task should fail
        if should_fail and fail_at_task == i:
            # Simulate failure
            builder_data["tasks"].append({
                "task_id": i,
                "name": task_name,
                "status": "failed",
                "test_result": "failed"
            })
            builder_data["tests_passing"] = False
            builder_data["rollbacks_needed"] += 1
            builder_data["blocker"] = {
                "type": "test_failure",
                "description": "Test failure: expected output mismatch",
                "task": task_name,
                "attempts": 1,
                "last_error": "AssertionError: expected 42, got 0"
            }
            builder_data["completion_status"] = "blocked"
            print(f"  ❌ {task_name} - FAILED (simulated failure)")
            break
        else:
            # Successful task
            builder_data["tasks"].append({
                "task_id": i,
                "name": task_name,
                "status": "completed",
                "test_result": "passed"
            })
            builder_data["tasks_completed"] += 1
            print(f"  ✓ {task_name}")

        # Create checkpoint every 3 tasks
        if i % 3 == 0:
            checkpoint_id = f"cp_{workflow_id}_{i}"
            builder_data["checkpoints_created"] += 1
            print(f"    📸 Checkpoint created: {checkpoint_id}")

        # Progress update every 5 tasks
        if i % 5 == 0:
            progress_update = {
                "timestamp": datetime.now().isoformat(),
                "tasks_completed": i,
                "message": f"Completed {i}/{task_count} tasks"
            }
            builder_data["progress_updates"].append(progress_update)
            print(f"    📊 Progress: {i}/{task_count} tasks")

    # Mark as success if all tasks succeeded
    if builder_data["tasks_completed"] == task_count:
        builder_data["completion_status"] = "success"
        builder_data["test_results"] = {
            "total_tests": task_count,
            "passing": task_count,
            "failing": 0,
            "skipped": 0
        }
    elif builder_data["tasks_completed"] == 0:
        builder_data["completion_status"] = "failed"
    elif builder_data["tasks_completed"] < task_count:
        if "blocker" in builder_data:
            builder_data["completion_status"] = "blocked"
        else:
            builder_data["completion_status"] = "partial"

    # Validate against schema
    schema = load_schema()
    is_valid, message = validate_builder_data(builder_data, schema)

    # Log handoff
    handoff_data = {
        "from": "builder",
        "to": "orchestrator",
        "workflow_id": workflow_id,
        "phase": "build",
        "summary": f"{scenario_name}: {builder_data['tasks_completed']}/{task_count} tasks completed",
        "data": builder_data,
        "confidence": 0.95 if builder_data["completion_status"] == "completed" else 0.5,
        "timestamp": datetime.now().isoformat()
    }

    conn.execute("""
        INSERT INTO handoffs (id, workflow_id, from_agent, to_agent, phase, summary, handoff_data, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (
        f"ho_{uuid.uuid4().hex[:12]}",
        workflow_id,
        "builder",
        "orchestrator",
        "build",
        handoff_data["summary"],
        json.dumps(handoff_data)
    ))

    # Update workflow status
    status = "completed" if builder_data["completion_status"] == "completed" else "failed"
    conn.execute("""
        UPDATE workflows SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?
    """, (status, workflow_id))

    conn.commit()
    conn.close()

    # Print results
    print(f"\n  Schema Validation: {'✅ PASS' if is_valid else '❌ FAIL'} - {message}")
    print(f"  Status: {builder_data['completion_status']}")
    print(f"  Tasks: {builder_data['tasks_completed']}/{builder_data['total_tasks']}")
    print(f"  Tests Passing: {builder_data['tests_passing']}")
    print(f"  Checkpoints: {builder_data['checkpoints_created']}")
    print(f"  Rollbacks: {builder_data['rollbacks_needed']}")
    print(f"  Progress Updates: {len(builder_data['progress_updates'])}")

    return {
        "scenario": scenario_name,
        "valid": is_valid,
        "completed": builder_data["completion_status"] == "success",
        "tasks_completed": builder_data["tasks_completed"],
        "workflow_id": workflow_id
    }

def main():
    """Run all Builder test scenarios."""

    print("\n" + "="*60)
    print("BUILDER AGENT TEST SUITE")
    print("="*60)

    results = []

    # Test 1: Simple feature (5 tasks, all pass)
    results.append(simulate_builder_workflow(
        "Simple Feature Implementation",
        task_count=5,
        should_fail=False
    ))

    # Test 2: Medium complexity (12 tasks, all pass)
    results.append(simulate_builder_workflow(
        "Medium Complexity Feature",
        task_count=12,
        should_fail=False
    ))

    # Test 3: Failure scenario (8 tasks, fail at task 5)
    results.append(simulate_builder_workflow(
        "Failure and Rollback Test",
        task_count=8,
        should_fail=True,
        fail_at_task=5
    ))

    # Test 4: Large project (20 tasks, all pass)
    results.append(simulate_builder_workflow(
        "Large Project Build",
        task_count=20,
        should_fail=False
    ))

    # Summary
    print("\n" + "="*60)
    print("BUILDER TEST SUMMARY")
    print("="*60)

    total = len(results)
    passed = sum(1 for r in results if r["valid"])

    print(f"\nTotal Tests: {total}")
    print(f"Schema Valid: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")

    print("\nDetailed Results:")
    for r in results:
        status = "✅ PASS" if r["valid"] else "❌ FAIL"
        print(f"  {status} - {r['scenario']}")
        print(f"        Tasks: {r['tasks_completed']} | Completed: {r['completed']}")

    print("\n" + "="*60)

    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
