#!/usr/bin/env python3
"""
Context Manager Agent Test Simulation
Tests context monitoring, compaction triggers, artifact creation, and snapshots.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
import uuid
import hashlib

# Test configuration
DB_PATH = Path.home() / ".claude" / "memory.db"
SCHEMA_PATH = Path.home() / ".claude" / "schemas" / "context_manager_data.json"
ARTIFACT_DIR = Path.home() / ".claude" / "artifacts"

def load_schema():
    """Load context manager data JSON schema."""
    with open(SCHEMA_PATH, 'r') as f:
        return json.load(f)

def validate_context_data(data, schema):
    """Validate context manager data against schema."""
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
            elif expected_type == 'number' and not isinstance(value, (int, float)):
                return False, f"Field {key} should be number"
            elif expected_type == 'boolean' and not isinstance(value, bool):
                return False, f"Field {key} should be boolean"
            elif expected_type == 'string' and not isinstance(value, str):
                return False, f"Field {key} should be string"

    return True, "Valid"

def create_test_artifact(conn, workflow_id, artifact_type, content):
    """Create a test artifact."""
    artifact_id = f"art_{artifact_type}_{uuid.uuid4().hex[:8]}"

    # Map artifact type to directory name
    type_to_dir = {
        "research_report": "research",
        "code_block": "code_blocks",
        "dependency_graph": "diagrams",
        "architecture_diagram": "diagrams",
        "test_results": "manifests"
    }

    # Create artifact directory if needed
    dir_name = type_to_dir.get(artifact_type, artifact_type)
    artifact_subdir = ARTIFACT_DIR / dir_name
    artifact_subdir.mkdir(parents=True, exist_ok=True)

    file_path = artifact_subdir / f"{artifact_id}.txt"
    file_path.write_text(content)

    content_hash = hashlib.sha256(content.encode()).hexdigest()
    size_bytes = len(content.encode())
    token_estimate = len(content) // 4

    conn.execute("""
        INSERT INTO artifacts (id, workflow_id, artifact_type, title, content_hash, file_path, size_bytes, token_estimate, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (artifact_id, workflow_id, artifact_type, f"Test {artifact_type}", content_hash, str(file_path), size_bytes, token_estimate))

    conn.commit()

    return {
        "artifact_id": artifact_id,
        "artifact_type": artifact_type,
        "size_bytes": size_bytes,
        "token_estimate": token_estimate
    }

def create_context_snapshot(conn, workflow_id, token_count):
    """Create a context snapshot."""
    snapshot_id = f"snap_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"

    snapshot_data = {
        "messages": ["message_1", "message_2", "..."],  # Simulated
        "timestamp": datetime.now().isoformat(),
        "token_count": token_count,
        "workflow_id": workflow_id
    }

    conn.execute("""
        INSERT INTO context_snapshots (id, workflow_id, snapshot_data, token_count, compaction_type, created_at)
        VALUES (?, ?, ?, ?, 'auto_80pct', CURRENT_TIMESTAMP)
    """, (snapshot_id, workflow_id, json.dumps(snapshot_data), token_count))

    conn.commit()

    return snapshot_id

def simulate_context_monitoring(scenario_name, current_tokens, max_tokens=200000):
    """Simulate context manager monitoring and compaction."""

    print(f"\n{'='*60}")
    print(f"Testing Context Manager: {scenario_name}")
    print(f"{'='*60}")

    conn = sqlite3.connect(DB_PATH)
    workflow_id = f"wf_ctx_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"

    # Calculate usage
    usage_pct = (current_tokens / max_tokens) * 100

    # Determine action
    if usage_pct >= 95:
        action = "emergency_compact"
    elif usage_pct >= 80:
        action = "compact"
    elif usage_pct >= 70:
        action = "warn"
    else:
        action = "none"

    print(f"  Current Tokens: {current_tokens:,}")
    print(f"  Max Tokens: {max_tokens:,}")
    print(f"  Usage: {usage_pct:.1f}%")
    print(f"  Action: {action}")

    # Build context manager data
    context_data = {
        "current_tokens": current_tokens,
        "max_tokens": max_tokens,
        "usage_pct": usage_pct,
        "action": action
    }

    # If compaction triggered, simulate it
    if action in ["compact", "emergency_compact"]:
        print(f"\n  🔄 Compaction triggered...")

        # Create snapshot
        snapshot_id = create_context_snapshot(conn, workflow_id, current_tokens)
        context_data["snapshot_created"] = True
        context_data["snapshot_id"] = snapshot_id
        print(f"    📸 Snapshot created: {snapshot_id}")

        # Simulate compaction
        reduction_ratio = 0.65  # Typical 65% reduction
        compacted_tokens = int(current_tokens * (1 - reduction_ratio))

        # Create artifacts for large content
        artifacts = []
        if current_tokens > 100000:
            # Simulate archiving research report
            research_content = "# Research Report\n\nDetailed findings...\n" * 100
            artifact = create_test_artifact(conn, workflow_id, "research_report", research_content)
            artifacts.append(artifact)
            print(f"    📦 Artifact created: {artifact['artifact_id']} ({artifact['token_estimate']} tokens)")

        if current_tokens > 150000:
            # Simulate archiving code block
            code_content = "// Large code block\nfunction example() {\n  // ...\n}\n" * 50
            artifact = create_test_artifact(conn, workflow_id, "code_block", code_content)
            artifacts.append(artifact)
            print(f"    📦 Artifact created: {artifact['artifact_id']} ({artifact['token_estimate']} tokens)")

        # Compaction metadata
        context_data["compaction_performed"] = True
        context_data["compaction_metadata"] = {
            "original_tokens": current_tokens,
            "compacted_tokens": compacted_tokens,
            "reduction_ratio": reduction_ratio,
            "artifacts_created": len(artifacts),
            "snapshot_id": snapshot_id,
            "duration_seconds": 2.5
        }

        # Preservation summary
        messages_total = current_tokens // 200  # Estimate ~200 tokens/message
        messages_preserved = 20
        messages_summarized = int(messages_total * 0.6)
        messages_archived = messages_total - messages_preserved - messages_summarized

        context_data["preservation_summary"] = {
            "messages_preserved": messages_preserved,
            "messages_summarized": messages_summarized,
            "messages_archived": messages_archived
        }

        context_data["artifacts"] = artifacts

        # Quality checks
        context_data["quality_check"] = {
            "critical_context_preserved": True,
            "recent_messages_intact": True,
            "handoffs_preserved": True,
            "user_prefs_preserved": True
        }

        print(f"\n    ✅ Compaction complete:")
        print(f"       {current_tokens:,} → {compacted_tokens:,} tokens ({reduction_ratio*100:.1f}% reduction)")
        print(f"       Messages: {messages_preserved} preserved, {messages_summarized} summarized, {messages_archived} archived")
        print(f"       Artifacts: {len(artifacts)} created")

    else:
        context_data["compaction_performed"] = False
        context_data["snapshot_created"] = False

        if action == "warn":
            context_data["warnings"] = [f"Context usage at {usage_pct:.1f}% - approaching compaction threshold"]
            print(f"  ⚠️  Warning logged")

    # Validate schema
    schema = load_schema()
    is_valid, message = validate_context_data(context_data, schema)

    # Log event
    conn.execute("""
        INSERT INTO events (id, workflow_id, agent, event_type, event_data, timestamp)
        VALUES (?, ?, 'context_manager', ?, ?, CURRENT_TIMESTAMP)
    """, (
        f"evt_{uuid.uuid4().hex[:12]}",
        workflow_id,
        action,
        json.dumps(context_data)
    ))

    conn.commit()
    conn.close()

    print(f"\n  Schema Validation: {'✅ PASS' if is_valid else '❌ FAIL'} - {message}")

    return {
        "scenario": scenario_name,
        "valid": is_valid,
        "action": action,
        "usage_pct": usage_pct,
        "compaction_performed": context_data.get("compaction_performed", False)
    }

def main():
    """Run all Context Manager test scenarios."""

    print("\n" + "="*60)
    print("CONTEXT MANAGER TEST SUITE")
    print("="*60)

    results = []

    # Test 1: Normal operation (50% usage)
    results.append(simulate_context_monitoring(
        "Normal Operation (50%)",
        current_tokens=100000
    ))

    # Test 2: Warning zone (75% usage)
    results.append(simulate_context_monitoring(
        "Warning Zone (75%)",
        current_tokens=150000
    ))

    # Test 3: Auto-compaction (85% usage)
    results.append(simulate_context_monitoring(
        "Auto-Compaction (85%)",
        current_tokens=170000
    ))

    # Test 4: Emergency compaction (96% usage)
    results.append(simulate_context_monitoring(
        "Emergency Compaction (96%)",
        current_tokens=192000
    ))

    # Test 5: Near limit (99% usage)
    results.append(simulate_context_monitoring(
        "Near Limit (99%)",
        current_tokens=198000
    ))

    # Summary
    print("\n" + "="*60)
    print("CONTEXT MANAGER TEST SUMMARY")
    print("="*60)

    total = len(results)
    passed = sum(1 for r in results if r["valid"])

    print(f"\nTotal Tests: {total}")
    print(f"Schema Valid: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")

    print("\nDetailed Results:")
    for r in results:
        status = "✅ PASS" if r["valid"] else "❌ FAIL"
        compaction = "🔄 Compacted" if r["compaction_performed"] else ""
        print(f"  {status} - {r['scenario']}")
        print(f"        Usage: {r['usage_pct']:.1f}% | Action: {r['action']} {compaction}")

    print("\n" + "="*60)

    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
