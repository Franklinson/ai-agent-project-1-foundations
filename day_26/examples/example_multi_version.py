"""Advanced A/B testing with multiple metrics comparison."""

from ab_testing import ABTester
import json


def multi_metric_evaluator(prompt: str, test_input: str, expected: dict) -> dict:
    """Evaluator with multiple quality dimensions."""
    # Analyze prompt characteristics
    has_examples = "example" in prompt.lower()
    has_constraints = "must" in prompt.lower() or "should" in prompt.lower()
    is_detailed = len(prompt) > 100
    
    # Simulate responses with varying quality dimensions
    if "search" in test_input.lower():
        response = "Found information"
        tool_used = "search"
        accuracy = 9.0 if has_examples else 8.0
        speed = 7.0 if is_detailed else 9.0
        clarity = 8.5 if has_constraints else 7.5
    elif "calculate" in test_input.lower():
        response = "42"
        tool_used = "calculator"
        accuracy = 9.5
        speed = 9.0
        clarity = 8.0
    else:
        response = "General response"
        tool_used = None
        accuracy = 7.0 if has_examples else 6.0
        speed = 8.0
        clarity = 7.0 if has_constraints else 6.5
    
    # Overall quality is weighted average
    quality = (accuracy * 0.5 + speed * 0.3 + clarity * 0.2)
    
    success = True
    if "contains" in expected:
        success = expected["contains"].lower() in response.lower()
    
    return {
        "success": success,
        "tool_used": tool_used,
        "quality_score": round(quality, 2),
        "accuracy": accuracy,
        "speed": speed,
        "clarity": clarity
    }


test_cases = [
    {"input": "Search for Python docs", "expected": {"contains": "information"}},
    {"input": "Calculate 10 + 5", "expected": {"contains": "15"}},
    {"input": "Search for tutorials", "expected": {"contains": "information"}},
    {"input": "What is AI?", "expected": {"contains": "response"}},
    {"input": "Calculate 20 * 3", "expected": {"contains": "60"}},
]


if __name__ == "__main__":
    tester = ABTester()
    
    # Version A: Detailed with examples
    version_a = """You are an AI assistant with search and calculator tools.
Example: For searches, provide comprehensive results.
You must ensure accuracy in all responses."""
    
    # Version B: Concise with constraints
    version_b = """You are an AI assistant with search and calculator tools.
Keep responses brief and accurate."""
    
    # Version C: Minimal
    version_c = """AI assistant with search and calculator."""
    
    print("Running multi-version A/B/C test...\n")
    
    # Compare A vs B
    comparison_ab = tester.compare_versions(version_a, version_b, test_cases, multi_metric_evaluator)
    
    # Compare B vs C
    comparison_bc = tester.compare_versions(version_b, version_c, test_cases, multi_metric_evaluator)
    
    # Compare A vs C
    comparison_ac = tester.compare_versions(version_a, version_c, test_cases, multi_metric_evaluator)
    
    # Generate reports
    print("=== A vs B ===")
    report_ab = tester.generate_comparison_report(comparison_ab, "ab_comparison.txt")
    print(report_ab)
    
    print("\n" + "="*60 + "\n")
    
    print("=== B vs C ===")
    report_bc = tester.generate_comparison_report(comparison_bc, "bc_comparison.txt")
    print(report_bc)
    
    print("\n" + "="*60 + "\n")
    
    print("=== A vs C ===")
    report_ac = tester.generate_comparison_report(comparison_ac, "ac_comparison.txt")
    print(report_ac)
    
    # Summary
    print("\n" + "="*60)
    print("=== OVERALL SUMMARY ===")
    
    scores = {
        "A": comparison_ab["version_a"]["metrics"]["success_rate"] + 
             comparison_ab["version_a"]["metrics"]["quality_score"],
        "B": comparison_ab["version_b"]["metrics"]["success_rate"] + 
             comparison_ab["version_b"]["metrics"]["quality_score"],
        "C": comparison_bc["version_b"]["metrics"]["success_rate"] + 
             comparison_bc["version_b"]["metrics"]["quality_score"]
    }
    
    best = max(scores, key=scores.get)
    print(f"\nVersion Scores:")
    for version, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        print(f"  Version {version}: {score:.2f}")
    
    print(f"\n🏆 BEST OVERALL: Version {best}")
    
    # Save all comparisons
    with open("multi_version_results.json", "w") as f:
        json.dump({
            "ab_comparison": comparison_ab,
            "bc_comparison": comparison_bc,
            "ac_comparison": comparison_ac,
            "summary": scores
        }, f, indent=2)
    
    print("\nAll results saved to comparison files and multi_version_results.json")
