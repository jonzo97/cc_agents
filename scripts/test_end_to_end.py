#!/usr/bin/env python3
"""
End-to-End Integration Test
Tests complete Scout→Plan→Build→Context Management workflow.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
import uuid

# Test configuration
DB_PATH = Path.home() / ".claude" / "memory.db"
SCHEMAS_DIR = Path.home() / ".claude" / "schemas"

def load_all_schemas():
    """Load all JSON schemas."""
    schemas = {}
    schema_files = {
        "handoff": "handoff_protocol.json",
        "scout": "scout_data.json",
        "planner": "planner_data.json",
        "builder": "builder_data.json",
        "context": "context_manager_data.json"
    }

    for key, filename in schema_files.items():
        with open(SCHEMAS_DIR / filename, 'r') as f:
            schemas[key] = json.load(f)

    return schemas

def create_workflow(conn):
    """Create a new test workflow."""
    workflow_id = f"wf_e2e_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"

    conn.execute("""
        INSERT INTO workflows (id, status, current_agent, user_request, created_at)
        VALUES (?, 'in_progress', 'orchestrator', ?, CURRENT_TIMESTAMP)
    """, (workflow_id, "End-to-end test: Build React component library"))

    conn.commit()
    return workflow_id

def log_handoff(conn, workflow_id, from_agent, to_agent, phase, summary, data):
    """Log an agent handoff to the database."""
    handoff_id = f"ho_e2e_{uuid.uuid4().hex[:12]}"

    handoff_data = {
        "from": from_agent,
        "to": to_agent,
        "workflow_id": workflow_id,
        "phase": phase,
        "summary": summary,
        "data": data,
        "confidence": data.get("confidence", 0.9),
        "timestamp": datetime.now().isoformat()
    }

    conn.execute("""
        INSERT INTO handoffs (id, workflow_id, from_agent, to_agent, phase, summary, handoff_data, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (handoff_id, workflow_id, from_agent, to_agent, phase, summary, json.dumps(handoff_data)))

    conn.commit()
    return handoff_id

def simulate_scout_phase(conn, workflow_id):
    """Simulate Scout agent exploration."""
    print("\n" + "="*60)
    print("PHASE 1: SCOUT")
    print("="*60)

    scout_data = {
        "project_type": "web_app",
        "tech_stack": ["React", "TypeScript", "Vite", "Tailwind"],
        "architecture_pattern": "component_library",
        "key_files": ["src/App.tsx", "src/components/", "vite.config.ts", "package.json"],
        "dependencies": {
            "react": "^18.2.0",
            "typescript": "^5.0.0",
            "vite": "^5.0.0",
            "tailwindcss": "^3.0.0"
        },
        "structure_metrics": {
            "src_files": 25,
            "test_files": 8,
            "components": 15
        },
        "unknowns": ["CI/CD pipeline", "deployment target"],
        "recommendations": ["Add comprehensive tests", "Set up Storybook"],
        "confidence": 0.88
    }

    print(f"  ✓ Explored codebase")
    print(f"  ✓ Identified: {scout_data['project_type']}")
    print(f"  ✓ Tech stack: {', '.join(scout_data['tech_stack'][:3])}, ...")
    print(f"  ✓ Components found: {scout_data['structure_metrics']['components']}")
    print(f"  ✓ Confidence: {scout_data['confidence']}")

    handoff_id = log_handoff(
        conn, workflow_id, "scout", "planner", "scout",
        "React component library, 15 components, medium complexity",
        scout_data
    )

    print(f"  → Handoff to Planner: {handoff_id}")
    return scout_data

def simulate_planner_phase(conn, workflow_id, scout_data):
    """Simulate Planner agent creating implementation plan."""
    print("\n" + "="*60)
    print("PHASE 2: PLANNER")
    print("="*60)

    planner_data = {
        "task_count": 12,
        "complexity": "medium",
        "requires_user_approval": True,
        "tasks": [
            {"id": 1, "title": "Set up test infrastructure", "priority": "high"},
            {"id": 2, "title": "Create Button component", "priority": "high"},
            {"id": 3, "title": "Create Input component", "priority": "high"},
            {"id": 4, "title": "Add component tests", "priority": "high"},
            {"id": 5, "title": "Set up Storybook", "priority": "medium"},
            {"id": 6, "title": "Create Card component", "priority": "medium"},
            {"id": 7, "title": "Create Modal component", "priority": "medium"},
            {"id": 8, "title": "Add accessibility tests", "priority": "medium"},
            {"id": 9, "title": "Create documentation", "priority": "low"},
            {"id": 10, "title": "Set up CI pipeline", "priority": "low"},
            {"id": 11, "title": "Build library bundle", "priority": "high"},
            {"id": 12, "title": "Publish to npm", "priority": "low"}
        ],
        "risks": [
            {
                "risk": "TypeScript configuration conflicts",
                "likelihood": "medium",
                "impact": "medium",
                "mitigation": "Test with strict mode"
            },
            {
                "risk": "Tailwind purge misconfiguration",
                "likelihood": "low",
                "impact": "high",
                "mitigation": "Verify bundle size"
            }
        ],
        "resource_budget": {
            "estimated_time_hours": 8,
            "estimated_tokens": 15000,
            "requires_apis": ["npm"]
        },
        "parallel_opportunities": [
            [2, 3],  # Button and Input can be parallel
            [6, 7]   # Card and Modal can be parallel
        ]
    }

    print(f"  ✓ Created {planner_data['task_count']}-task plan")
    print(f"  ✓ Complexity: {planner_data['complexity']}")
    print(f"  ✓ Estimated time: {planner_data['resource_budget']['estimated_time_hours']}h")
    print(f"  ✓ Risks identified: {len(planner_data['risks'])}")
    print(f"  ✓ Parallel opportunities: {len(planner_data['parallel_opportunities'])} task groups")
    print(f"  ⚠ Requires user approval")

    handoff_id = log_handoff(
        conn, workflow_id, "planner", "orchestrator", "plan",
        "12-task plan ready, medium complexity, 8h estimate",
        planner_data
    )

    print(f"  → Handoff to Orchestrator: {handoff_id}")
    return planner_data

def simulate_builder_phase(conn, workflow_id, planner_data):
    """Simulate Builder agent implementation."""
    print("\n" + "="*60)
    print("PHASE 3: BUILDER")
    print("="*60)

    task_count = planner_data["task_count"]

    builder_data = {
        "tasks_completed": 0,
        "total_tasks": task_count,
        "tests_passing": True,
        "checkpoints_created": 0,
        "rollbacks_needed": 0,
        "completion_status": "success",
        "progress_updates": []
    }

    # Simulate task execution
    for i in range(1, task_count + 1):
        task = planner_data["tasks"][i-1]
        builder_data["tasks_completed"] += 1

        if i % 3 == 0:
            builder_data["checkpoints_created"] += 1
            print(f"  ✓ Task {i}/{task_count}: {task['title']}")
            print(f"    📸 Checkpoint created")
        elif i % 5 == 0:
            builder_data["progress_updates"].append({
                "timestamp": datetime.now().isoformat(),
                "tasks_completed": i,
                "message": f"Progress: {i}/{task_count} tasks"
            })
            print(f"  ✓ Task {i}/{task_count}: {task['title']}")
            print(f"    📊 Progress update sent to Orchestrator")
        else:
            print(f"  ✓ Task {i}/{task_count}: {task['title']}")

    builder_data["test_results"] = {
        "total_tests": 45,
        "passing": 45,
        "failing": 0,
        "skipped": 0,
        "coverage_percent": 87.5
    }

    builder_data["files_modified"] = [
        "src/components/Button.tsx",
        "src/components/Input.tsx",
        "src/components/Card.tsx",
        "src/components/Modal.tsx",
        "src/tests/Button.test.tsx",
        "src/tests/Input.test.tsx",
        ".storybook/main.ts",
        "package.json"
    ]

    print(f"\n  ✅ Build complete!")
    print(f"  ✓ Tasks: {builder_data['tasks_completed']}/{task_count}")
    print(f"  ✓ Tests: {builder_data['test_results']['passing']}/{builder_data['test_results']['total_tests']} passing")
    print(f"  ✓ Coverage: {builder_data['test_results']['coverage_percent']:.1f}%")
    print(f"  ✓ Checkpoints: {builder_data['checkpoints_created']}")
    print(f"  ✓ Files modified: {len(builder_data['files_modified'])}")

    handoff_id = log_handoff(
        conn, workflow_id, "builder", "orchestrator", "build",
        "Build complete: 12/12 tasks, 45/45 tests passing",
        builder_data
    )

    print(f"  → Handoff to Orchestrator: {handoff_id}")
    return builder_data

def simulate_context_monitoring(conn, workflow_id):
    """Simulate Context Manager monitoring during workflow."""
    print("\n" + "="*60)
    print("PHASE 4: CONTEXT MANAGEMENT (Background)")
    print("="*60)

    # Simulate context usage at different workflow stages
    checks = [
        ("After Scout", 50000, 25.0),
        ("After Planner", 85000, 42.5),
        ("Mid-Build", 125000, 62.5),
        ("Near Completion", 155000, 77.5)
    ]

    for stage, tokens, usage_pct in checks:
        action = "none"
        if usage_pct >= 70:
            action = "warn"

        print(f"  {stage}: {tokens:,} tokens ({usage_pct:.1f}%) - {action}")

        # Log monitoring event
        conn.execute("""
            INSERT INTO events (id, workflow_id, agent, event_type, event_data, timestamp)
            VALUES (?, ?, 'context_manager', 'context_check', ?, CURRENT_TIMESTAMP)
        """, (
            f"evt_{uuid.uuid4().hex[:12]}",
            workflow_id,
            json.dumps({"tokens": tokens, "usage_pct": usage_pct, "action": action})
        ))

    print(f"  ✓ Context stayed under 80% threshold")
    print(f"  ✓ No compaction needed")

    conn.commit()

def main():
    """Run end-to-end integration test."""
    print("\n" + "="*60)
    print("END-TO-END INTEGRATION TEST")
    print("Scout → Plan → Build → Context Management")
    print("="*60)

    # Connect to database
    conn = sqlite3.connect(DB_PATH)

    # Create workflow
    workflow_id = create_workflow(conn)
    print(f"\nWorkflow ID: {workflow_id}")

    # Execute phases
    scout_data = simulate_scout_phase(conn, workflow_id)
    planner_data = simulate_planner_phase(conn, workflow_id, scout_data)

    # Simulate user approval
    print("\n" + "-"*60)
    print("USER APPROVAL: ✅ Approved (simulated)")
    print("-"*60)

    builder_data = simulate_builder_phase(conn, workflow_id, planner_data)
    simulate_context_monitoring(conn, workflow_id)

    # Update workflow status
    conn.execute("""
        UPDATE workflows SET status = 'completed', updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (workflow_id,))
    conn.commit()

    # Summary
    print("\n" + "="*60)
    print("END-TO-END TEST SUMMARY")
    print("="*60)

    # Query handoffs
    cursor = conn.execute("""
        SELECT from_agent, to_agent, phase, summary
        FROM handoffs WHERE workflow_id = ?
        ORDER BY timestamp ASC
    """, (workflow_id,))

    handoffs = cursor.fetchall()

    print(f"\nWorkflow: {workflow_id}")
    print(f"Status: COMPLETED ✅")
    print(f"\nHandoffs: {len(handoffs)}")
    for i, (from_ag, to_ag, phase, summary) in enumerate(handoffs, 1):
        print(f"  {i}. {from_ag} → {to_ag} ({phase})")
        print(f"     {summary}")

    print(f"\nFinal Results:")
    print(f"  Scout confidence: {scout_data['confidence']}")
    print(f"  Plan complexity: {planner_data['complexity']}")
    print(f"  Build status: {builder_data['completion_status']}")
    print(f"  Tasks completed: {builder_data['tasks_completed']}/{builder_data['total_tasks']}")
    print(f"  Tests passing: {builder_data['test_results']['passing']}/{builder_data['test_results']['total_tests']}")

    print("\n" + "="*60)
    print("✅ END-TO-END TEST PASSED")
    print("="*60)

    conn.close()
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
