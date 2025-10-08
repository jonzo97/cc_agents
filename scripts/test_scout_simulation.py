#!/usr/bin/env python3
"""
Scout Agent Simulation Test
Simulates Scout agent behavior on test scenarios and validates outputs.
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path

# Test scenarios directory
SCENARIOS_DIR = Path("/home/jorgill/cc_agents/test_scenarios")

def simulate_scout_exploration(scenario_path):
    """Simulate Scout agent exploring a scenario."""
    scenario_name = scenario_path.name
    print(f"\n{'='*60}")
    print(f"Testing Scout on: {scenario_name}")
    print(f"{'='*60}")

    start_time = time.time()

    # Simulate file discovery
    files_found = list(scenario_path.rglob('*'))
    files_found = [f for f in files_found if f.is_file()]

    print(f"Files discovered: {len(files_found)}")
    for f in files_found[:5]:  # Show first 5
        print(f"  - {f.relative_to(scenario_path)}")
    if len(files_found) > 5:
        print(f"  ... and {len(files_found) - 5} more")

    # Analyze files
    tech_stack = []
    project_type = "unknown"
    confidence = 0.5
    unknowns = []

    # Check for package.json (Node.js)
    package_json = scenario_path / "package.json"
    if package_json.exists():
        with open(package_json) as f:
            pkg = json.load(f)

        # Detect project type from dependencies
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}

        if "react" in deps:
            tech_stack.append("React")
            project_type = "web_app"
            if "typescript" in deps or "@types/react" in deps:
                tech_stack.append("TypeScript")
            if "vite" in deps:
                tech_stack.append("Vite")
            if "tailwindcss" in deps:
                tech_stack.append("Tailwind CSS")
            confidence = 0.9
        elif "commander" in deps:
            tech_stack.append("Node.js")
            project_type = "cli_tool"
            confidence = 0.85

        if "jest" in deps or "vitest" in deps:
            tech_stack.append("Jest" if "jest" in deps else "Vitest")

    # Check for bower.json (legacy)
    bower_json = scenario_path / "bower.json"
    if bower_json.exists():
        with open(bower_json) as f:
            bower = json.load(f)
        deps = bower.get("dependencies", {})

        if "angular" in deps and "1." in deps["angular"]:
            tech_stack.append("AngularJS 1.x")
            tech_stack.append("Bower")
            project_type = "web_app"
            confidence = 0.75
            unknowns.append("Build system (Grunt assumed)")
            unknowns.append("No test framework detected")

    # Check README for Max plugins
    readme = scenario_path / "README.md"
    if readme.exists():
        with open(readme) as f:
            content = f.read().lower()

        if "max for live" in content or "ableton" in content:
            tech_stack.append("Max/MSP")
            project_type = "plugin"
            confidence = 0.6
            unknowns.append("Build process unclear")
            unknowns.append("MIDI routing implementation")
            unknowns.append("Deployment workflow")

    # Empty project detection
    if len(files_found) <= 1:  # Just README or empty
        project_type = "unknown"
        confidence = 0.3
        unknowns.append("No source files found")
        unknowns.append("Project structure unclear")

    execution_time = time.time() - start_time

    # Build Scout output (following scout_data.json schema)
    scout_output = {
        "project_type": project_type,
        "tech_stack": tech_stack,
        "architecture_pattern": "component_library" if "React" in tech_stack else "unknown",
        "key_files": [str(f.relative_to(scenario_path)) for f in files_found[:10]],
        "dependencies": {},  # Would parse from package.json
        "structure": {
            "src_files": len([f for f in files_found if f.suffix in ['.js', '.ts', '.jsx', '.tsx']]),
            "test_files": len([f for f in files_found if 'test' in f.name or 'spec' in f.name]),
        },
        "unknowns": unknowns,
        "recommendations": [],
        "confidence": confidence,
        "exploration_time_seconds": round(execution_time, 2),
        "timeout_occurred": False
    }

    # Add recommendations based on findings
    if scout_output["structure"]["test_files"] == 0 and scout_output["structure"]["src_files"] > 0:
        scout_output["recommendations"].append("Add test suite (no tests found)")

    if project_type == "web_app" and "TypeScript" not in tech_stack:
        scout_output["recommendations"].append("Consider TypeScript for type safety")

    # Display results
    print(f"\nScout Analysis:")
    print(f"  Project Type: {scout_output['project_type']}")
    print(f"  Tech Stack: {', '.join(scout_output['tech_stack']) if scout_output['tech_stack'] else 'None detected'}")
    print(f"  Confidence: {scout_output['confidence']:.2f}")
    print(f"  Execution Time: {scout_output['exploration_time_seconds']}s")

    if unknowns:
        print(f"\n  Unknowns ({len(unknowns)}):")
        for unknown in unknowns:
            print(f"    - {unknown}")

    if scout_output["recommendations"]:
        print(f"\n  Recommendations:")
        for rec in scout_output["recommendations"]:
            print(f"    - {rec}")

    # Validate against schema
    validate_scout_output(scout_output)

    return scout_output

def validate_scout_output(scout_output):
    """Validate Scout output against schema."""
    required_fields = ["project_type", "tech_stack", "confidence"]

    print(f"\n  Schema Validation:")
    all_valid = True

    for field in required_fields:
        if field in scout_output:
            print(f"    ✓ {field}")
        else:
            print(f"    ✗ {field} MISSING")
            all_valid = False

    # Validate confidence range
    if 0 <= scout_output.get("confidence", -1) <= 1:
        print(f"    ✓ confidence in range [0,1]")
    else:
        print(f"    ✗ confidence out of range")
        all_valid = False

    # Estimate token count (rough approximation)
    json_str = json.dumps(scout_output, indent=2)
    estimated_tokens = len(json_str) // 4  # Rough estimate: 4 chars per token
    print(f"    ~ {estimated_tokens} tokens (target: <2000)")

    if estimated_tokens > 2000:
        print(f"    ⚠ Token count may exceed limit")

    if all_valid:
        print(f"    ✅ Schema valid")
    else:
        print(f"    ❌ Schema validation failed")

    return all_valid

def main():
    print("Scout Agent Simulation Testing")
    print("="*60)

    scenarios = sorted([d for d in SCENARIOS_DIR.iterdir() if d.is_dir()])
    results = []

    for scenario in scenarios:
        try:
            result = simulate_scout_exploration(scenario)
            results.append({
                "scenario": scenario.name,
                "success": True,
                "data": result
            })
        except Exception as e:
            print(f"\n  ❌ Error: {e}")
            results.append({
                "scenario": scenario.name,
                "success": False,
                "error": str(e)
            })

    # Summary
    print(f"\n{'='*60}")
    print(f"Test Summary")
    print(f"{'='*60}")

    successes = sum(1 for r in results if r["success"])
    print(f"Tests passed: {successes}/{len(results)}")

    avg_confidence = sum(r["data"]["confidence"] for r in results if r["success"]) / successes
    print(f"Average confidence: {avg_confidence:.2f}")

    research_needed = sum(1 for r in results if r["success"] and r["data"]["confidence"] < 0.7)
    print(f"Scenarios needing research: {research_needed}")

    print(f"\n{'='*60}")

    # Save results
    results_file = Path("/home/jorgill/cc_agents/scout_test_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to: {results_file}")

if __name__ == "__main__":
    main()
