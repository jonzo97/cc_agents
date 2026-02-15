#!/usr/bin/env python3
"""
Orchestrator Agent Simulation Test
Simulates Orchestrator coordinating Scout→Planner workflow with handoffs.
"""

import json
import uuid
from pathlib import Path
from datetime import datetime

def generate_workflow_id():
    """Generate unique workflow ID."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_suffix = uuid.uuid4().hex[:6]
    return f"wf_{timestamp}_{random_suffix}"

def simulate_orchestrator_workflow(scout_data, planner_data, scenario_name):
    """Simulate Orchestrator coordinating Scout→Planner handoff."""
    print(f"\n{'='*60}")
    print(f"Testing Orchestrator: {scenario_name}")
    print(f"{'='*60}")

    workflow_id = generate_workflow_id()
    print(f"\n[Orchestrator] Creating workflow: {workflow_id}")

    # Step 1: Invoke Scout
    print(f"[Orchestrator] Invoking Scout agent...")
    print(f"  Timeout: 180 seconds")
    print(f"  Expected output: JSON summary <2k tokens")

    # Simulate Scout completion
    print(f"[Scout] Exploration complete")
    print(f"  Project type: {scout_data['project_type']}")
    print(f"  Confidence: {scout_data['confidence']:.2f}")

    # Step 2: Evaluate Scout output
    print(f"\n[Orchestrator] Evaluating Scout results...")

    research_needed = False
    if scout_data['confidence'] < 0.7:
        print(f"  ⚠ Confidence {scout_data['confidence']:.2f} < 0.7")
        print(f"  → Research agent would be invoked (Phase 3)")
        research_needed = True

    unknowns_count = len(scout_data.get('unknowns', []))
    if unknowns_count > 3:
        print(f"  ⚠ {unknowns_count} unknowns detected")
        print(f"  → Research recommended")
        research_needed = True

    # Step 3: Create Scout→Planner handoff
    print(f"\n[Orchestrator] Creating Scout→Planner handoff...")

    handoff_scout_to_planner = {
        "from": "scout",
        "to": "planner",
        "workflow_id": workflow_id,
        "phase": "plan",
        "summary": create_handoff_summary(scout_data, scenario_name),
        "data": scout_data,
        "artifacts": [],  # Would contain artifact IDs
        "next_actions": [
            "Analyze Scout findings",
            "Create implementation plan",
            "Assess risks and complexity"
        ],
        "confidence": scout_data['confidence'],
        "warnings": [],
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "token_count": estimate_tokens(scout_data),
            "execution_time_seconds": scout_data.get('exploration_time_seconds', 0)
        }
    }

    if research_needed:
        handoff_scout_to_planner["warnings"].append("Low confidence - research recommended")

    print(f"  Handoff ID: ho_{uuid.uuid4().hex[:12]}")
    print(f"  Summary: {handoff_scout_to_planner['summary']}")
    print(f"  Token count: {handoff_scout_to_planner['metadata']['token_count']}")

    # Validate handoff
    validate_handoff(handoff_scout_to_planner)

    # Step 4: Invoke Planner
    print(f"\n[Orchestrator] Invoking Planner agent...")
    print(f"  Model: Opus (complex reasoning)")
    print(f"  Timeout: 300 seconds")

    # Simulate Planner completion
    print(f"[Planner] Planning complete")
    print(f"  Tasks: {planner_data['task_count']}")
    print(f"  Complexity: {planner_data['complexity']}")
    print(f"  Risks: {planner_data['risks_identified']}")

    # Step 5: Create Planner→Orchestrator handoff
    print(f"\n[Orchestrator] Creating Planner→Orchestrator handoff...")

    handoff_planner_to_orchestrator = {
        "from": "planner",
        "to": "orchestrator",
        "workflow_id": workflow_id,
        "phase": "plan",
        "summary": create_plan_summary(planner_data),
        "data": planner_data,
        "artifacts": [],
        "next_actions": [
            "Present plan to user for approval",
            "Address user concerns if any",
            "Hand off to Builder upon approval"
        ],
        "confidence": calculate_plan_confidence(planner_data),
        "warnings": generate_plan_warnings(planner_data),
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "token_count": estimate_tokens(planner_data)
        }
    }

    print(f"  Handoff ID: ho_{uuid.uuid4().hex[:12]}")
    print(f"  Summary: {handoff_planner_to_orchestrator['summary']}")
    print(f"  Confidence: {handoff_planner_to_orchestrator['confidence']:.2f}")

    # Validate handoff
    validate_handoff(handoff_planner_to_orchestrator)

    # Step 6: Request user approval
    print(f"\n[Orchestrator] Requesting user approval...")
    print(f"  Approval required: {planner_data['requires_user_approval']}")
    print(f"  Rationale: {planner_data['approval_rationale']}")

    # Summary
    print(f"\n[Orchestrator] Workflow status: AWAITING_APPROVAL")
    print(f"  Next step: User reviews plan")
    print(f"  If approved → Invoke Builder (Phase 2)")
    print(f"  If rejected → Return to Planner with feedback")

    return {
        "workflow_id": workflow_id,
        "status": "awaiting_approval",
        "handoffs": [handoff_scout_to_planner, handoff_planner_to_orchestrator],
        "research_triggered": research_needed,
        "approval_required": True
    }

def create_handoff_summary(scout_data, scenario_name):
    """Create Scout handoff summary."""
    tech = ", ".join(scout_data['tech_stack']) if scout_data['tech_stack'] else "unknown"
    return f"{scenario_name}: {scout_data['project_type']}, {tech}, confidence {scout_data['confidence']:.2f}"

def create_plan_summary(planner_data):
    """Create Planner handoff summary."""
    return f"Plan ready: {planner_data['task_count']} tasks, {planner_data['total_estimate_hours']}h, {planner_data['complexity']} complexity"

def calculate_plan_confidence(planner_data):
    """Calculate confidence in the plan."""
    base = 1.0
    base -= planner_data['risks_identified'] * 0.1
    if planner_data['complexity'] == 'high':
        base -= 0.2
    elif planner_data['complexity'] == 'very_high':
        base -= 0.3
    return max(0.0, min(1.0, base))

def generate_plan_warnings(planner_data):
    """Generate warnings for the plan."""
    warnings = []
    if planner_data['complexity'] in ['high', 'very_high']:
        warnings.append(f"{planner_data['complexity']} complexity requires careful execution")
    if planner_data['risks_identified'] > 0:
        warnings.append(f"{planner_data['risks_identified']} risks identified")
    return warnings

def estimate_tokens(data):
    """Estimate token count for data."""
    json_str = json.dumps(data, indent=2)
    return len(json_str) // 4

def validate_handoff(handoff):
    """Validate handoff against schema."""
    required = ["from", "to", "workflow_id", "phase", "summary", "data", "timestamp"]

    print(f"    Validating handoff schema...")
    all_valid = True

    for field in required:
        if field not in handoff:
            print(f"      ✗ Missing: {field}")
            all_valid = False

    # Check workflow_id format
    if 'workflow_id' in handoff:
        if handoff['workflow_id'].startswith('wf_'):
            print(f"      ✓ workflow_id format valid")
        else:
            print(f"      ✗ workflow_id format invalid")
            all_valid = False

    # Check confidence range
    if 'confidence' in handoff:
        if 0 <= handoff['confidence'] <= 1:
            print(f"      ✓ confidence in range")
        else:
            print(f"      ✗ confidence out of range")
            all_valid = False

    if all_valid:
        print(f"      ✅ Handoff valid")
    else:
        print(f"      ❌ Handoff validation failed")

    return all_valid

def main():
    print("Orchestrator Agent Simulation Testing")
    print("="*60)

    # Load Scout and Planner results
    scout_file = Path("/home/jorgill/cc_agents/scout_test_results.json")
    planner_file = Path("/home/jorgill/cc_agents/planner_test_results.json")

    with open(scout_file) as f:
        scout_results = json.load(f)

    with open(planner_file) as f:
        planner_results = json.load(f)

    # Combine results
    orchestrator_results = []

    for scout, planner in zip(scout_results, planner_results):
        if scout["success"] and planner["success"]:
            scenario = scout["scenario"]

            try:
                result = simulate_orchestrator_workflow(
                    scout["data"],
                    planner["data"],
                    scenario
                )
                orchestrator_results.append({
                    "scenario": scenario,
                    "success": True,
                    "data": result
                })
            except Exception as e:
                print(f"\n  ❌ Error: {e}")
                orchestrator_results.append({
                    "scenario": scenario,
                    "success": False,
                    "error": str(e)
                })

    # Summary
    print(f"\n{'='*60}")
    print(f"Test Summary")
    print(f"{'='*60}")

    successes = sum(1 for r in orchestrator_results if r["success"])
    print(f"Workflows completed: {successes}/{len(orchestrator_results)}")

    research_triggered = sum(1 for r in orchestrator_results if r["success"] and r["data"]["research_triggered"])
    print(f"Research triggers: {research_triggered}")

    all_approved = all(r["data"]["approval_required"] for r in orchestrator_results if r["success"])
    print(f"All requiring approval: {all_approved}")

    print(f"\n{'='*60}")

    # Save results
    results_file = Path("/home/jorgill/cc_agents/orchestrator_test_results.json")
    with open(results_file, 'w') as f:
        json.dump(orchestrator_results, f, indent=2)
    print(f"Results saved to: {results_file}")

if __name__ == "__main__":
    main()
