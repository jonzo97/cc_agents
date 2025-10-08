#!/usr/bin/env python3
"""
Planner Agent Simulation Test
Simulates Planner agent processing Scout outputs and generating plans.
"""

import json
from pathlib import Path
from datetime import datetime

def simulate_planner(scout_output, scenario_name):
    """Simulate Planner agent creating implementation plan."""
    print(f"\n{'='*60}")
    print(f"Testing Planner on: {scenario_name}")
    print(f"{'='*60}")

    # Analyze Scout findings
    project_type = scout_output["project_type"]
    confidence = scout_output["confidence"]
    unknowns = scout_output["unknowns"]
    tech_stack = scout_output["tech_stack"]

    # Determine complexity
    complexity = "low"
    if len(unknowns) > 3:
        complexity = "high"
    elif len(unknowns) > 1:
        complexity = "medium"

    if confidence < 0.6:
        complexity = "high"

    # Generate tasks based on project type
    tasks = []

    if project_type == "cli_tool":
        tasks = [
            {"task": "Review command structure", "estimate_minutes": 10},
            {"task": "Enhance argument parsing", "estimate_minutes": 20},
            {"task": "Add input validation", "estimate_minutes": 15},
            {"task": "Improve error messages", "estimate_minutes": 15},
            {"task": "Add unit tests", "estimate_minutes": 30},
            {"task": "Update documentation", "estimate_minutes": 20}
        ]
    elif project_type == "web_app" and "React" in tech_stack:
        tasks = [
            {"task": "Review component architecture", "estimate_minutes": 15},
            {"task": "Add missing test coverage", "estimate_minutes": 45},
            {"task": "Implement Storybook", "estimate_minutes": 60},
            {"task": "Configure CI/CD", "estimate_minutes": 30},
            {"task": "Optimize bundle size", "estimate_minutes": 20},
            {"task": "Document component API", "estimate_minutes": 30}
        ]
    elif "AngularJS" in tech_stack:
        tasks = [
            {"task": "Audit current architecture", "estimate_minutes": 60},
            {"task": "Document technical debt", "estimate_minutes": 30},
            {"task": "Create modernization roadmap", "estimate_minutes": 45},
            {"task": "Identify migration priorities", "estimate_minutes": 30},
            {"task": "Assess testing strategy", "estimate_minutes": 30}
        ]
    elif project_type == "unknown":
        tasks = [
            {"task": "Gather project requirements", "estimate_minutes": 15},
            {"task": "Research relevant technologies", "estimate_minutes": 30},
            {"task": "Create project structure", "estimate_minutes": 20},
            {"task": "Set up development environment", "estimate_minutes": 15}
        ]
    else:
        tasks = [
            {"task": "Analyze project requirements", "estimate_minutes": 20},
            {"task": "Design implementation approach", "estimate_minutes": 30},
            {"task": "Create development plan", "estimate_minutes": 20}
        ]

    # Generate risks
    risks = []

    if confidence < 0.7:
        risks.append({
            "id": "risk_001",
            "description": "Low confidence in project understanding",
            "category": "knowledge",
            "likelihood": "high",
            "impact": "high",
            "mitigation": "Conduct deep research before implementation",
            "owner": "planner",
            "status": "open"
        })

    if len(unknowns) > 0:
        risks.append({
            "id": f"risk_{str(len(risks)+1).zfill(3)}",
            "description": f"{len(unknowns)} unknowns identified",
            "category": "technical",
            "likelihood": "medium",
            "impact": "medium",
            "mitigation": "Address unknowns through research and experimentation",
            "owner": "planner",
            "status": "open"
        })

    if not tech_stack or len(tech_stack) == 0:
        risks.append({
            "id": f"risk_{str(len(risks)+1).zfill(3)}",
            "description": "Tech stack unclear",
            "category": "architectural",
            "likelihood": "high",
            "impact": "high",
            "mitigation": "Investigate before proceeding",
            "owner": "planner",
            "status": "open"
        })

    # Calculate estimates
    total_minutes = sum(t["estimate_minutes"] for t in tasks)
    optimistic_hours = round(total_minutes * 0.7 / 60, 1)
    realistic_hours = round(total_minutes / 60, 1)
    pessimistic_hours = round(total_minutes * 1.5 / 60, 1)

    # Build Planner output (following planner_data.json schema)
    planner_output = {
        "task_count": len(tasks),
        "total_estimate_hours": realistic_hours,
        "complexity": complexity,
        "approach": determine_approach(project_type, tech_stack),
        "risks_identified": len(risks),
        "risks": risks,
        "checkpoints": determine_checkpoints(len(tasks)),
        "checkpoint_details": generate_checkpoints(tasks),
        "resource_budget": {
            "time_estimate": {
                "optimistic": f"{optimistic_hours} hours",
                "realistic": f"{realistic_hours} hours",
                "pessimistic": f"{pessimistic_hours} hours"
            },
            "token_budget": {
                "scout": 5000,
                "planner": 8000,
                "builder": estimate_builder_tokens(len(tasks)),
                "total": 13000 + estimate_builder_tokens(len(tasks)),
                "buffer": 20000
            }
        },
        "requires_user_approval": True,
        "approval_rationale": determine_approval_rationale(complexity, len(risks))
    }

    # Display results
    print(f"\nPlanner Analysis:")
    print(f"  Tasks: {planner_output['task_count']}")
    print(f"  Complexity: {planner_output['complexity']}")
    print(f"  Approach: {planner_output['approach']}")
    print(f"  Time Estimate: {planner_output['total_estimate_hours']} hours")
    print(f"  Risks: {planner_output['risks_identified']}")

    if risks:
        print(f"\n  Risk Matrix:")
        for risk in risks:
            print(f"    [{risk['id']}] {risk['description']}")
            print(f"        Likelihood: {risk['likelihood']} | Impact: {risk['impact']}")
            print(f"        Mitigation: {risk['mitigation']}")

    print(f"\n  User Approval Required: {planner_output['requires_user_approval']}")
    print(f"  Rationale: {planner_output['approval_rationale']}")

    # Validate against schema
    validate_planner_output(planner_output)

    return planner_output

def determine_approach(project_type, tech_stack):
    """Determine development approach."""
    if project_type == "unknown":
        return "experimental"
    if "AngularJS" in tech_stack:
        return "brownfield"
    if tech_stack and len(tech_stack) > 0:
        return "greenfield"
    return "learning"

def determine_checkpoints(task_count):
    """Calculate number of checkpoints."""
    if task_count <= 3:
        return 1
    elif task_count <= 6:
        return 2
    else:
        return 3

def generate_checkpoints(tasks):
    """Generate checkpoint details."""
    checkpoints = []
    checkpoint_interval = len(tasks) // determine_checkpoints(len(tasks))

    for i in range(0, len(tasks), checkpoint_interval):
        if i + checkpoint_interval <= len(tasks):
            checkpoint = {
                "name": f"Checkpoint {len(checkpoints) + 1}",
                "after_task": tasks[min(i + checkpoint_interval - 1, len(tasks) - 1)]["task"],
                "criteria": [
                    "All tasks completed",
                    "Tests passing",
                    "No blockers"
                ]
            }
            checkpoints.append(checkpoint)

    return checkpoints

def estimate_builder_tokens(task_count):
    """Estimate Builder token usage."""
    return task_count * 5000  # Rough estimate: 5k tokens per task

def determine_approval_rationale(complexity, risk_count):
    """Determine why approval is needed."""
    if complexity == "high":
        return f"High complexity with {risk_count} risks requires careful review"
    elif risk_count > 0:
        return f"{risk_count} risks identified that need approval"
    else:
        return "Standard approval for implementation plan"

def validate_planner_output(planner_output):
    """Validate Planner output against schema."""
    required_fields = ["task_count", "complexity", "requires_user_approval"]

    print(f"\n  Schema Validation:")
    all_valid = True

    for field in required_fields:
        if field in planner_output:
            print(f"    ✓ {field}")
        else:
            print(f"    ✗ {field} MISSING")
            all_valid = False

    # Validate complexity enum
    valid_complexity = ["low", "medium", "high", "very_high"]
    if planner_output.get("complexity") in valid_complexity:
        print(f"    ✓ complexity valid")
    else:
        print(f"    ✗ complexity invalid")
        all_valid = False

    # Estimate token count
    json_str = json.dumps(planner_output, indent=2)
    estimated_tokens = len(json_str) // 4
    print(f"    ~ {estimated_tokens} tokens (target: <3000)")

    if estimated_tokens > 3000:
        print(f"    ⚠ Token count may exceed limit")

    if all_valid:
        print(f"    ✅ Schema valid")
    else:
        print(f"    ❌ Schema validation failed")

    return all_valid

def main():
    print("Planner Agent Simulation Testing")
    print("="*60)

    # Load Scout results
    scout_results_file = Path("/home/jorgill/cc_agents/scout_test_results.json")
    with open(scout_results_file) as f:
        scout_results = json.load(f)

    planner_results = []

    for result in scout_results:
        if result["success"]:
            scenario_name = result["scenario"]
            scout_data = result["data"]

            try:
                planner_output = simulate_planner(scout_data, scenario_name)
                planner_results.append({
                    "scenario": scenario_name,
                    "success": True,
                    "data": planner_output
                })
            except Exception as e:
                print(f"\n  ❌ Error: {e}")
                planner_results.append({
                    "scenario": scenario_name,
                    "success": False,
                    "error": str(e)
                })

    # Summary
    print(f"\n{'='*60}")
    print(f"Test Summary")
    print(f"{'='*60}")

    successes = sum(1 for r in planner_results if r["success"])
    print(f"Tests passed: {successes}/{len(planner_results)}")

    avg_tasks = sum(r["data"]["task_count"] for r in planner_results if r["success"]) / successes
    print(f"Average tasks per plan: {avg_tasks:.1f}")

    avg_risks = sum(r["data"]["risks_identified"] for r in planner_results if r["success"]) / successes
    print(f"Average risks identified: {avg_risks:.1f}")

    print(f"\n{'='*60}")

    # Save results
    results_file = Path("/home/jorgill/cc_agents/planner_test_results.json")
    with open(results_file, 'w') as f:
        json.dump(planner_results, f, indent=2)
    print(f"Results saved to: {results_file}")

if __name__ == "__main__":
    main()
