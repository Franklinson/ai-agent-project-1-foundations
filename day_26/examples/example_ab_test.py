"""Example A/B testing of prompt versions."""

from ab_testing import ABTester
import json


def evaluator(prompt: str, test_input: str, expected: dict) -> dict:
    """Evaluator that simulates different responses based on prompt style."""
    # Version A (formal) vs Version B (casual) affects quality
    is_formal = "professional" in prompt.lower() or "formal" in prompt.lower()
    
    if "search" in test_input.lower():
        response = "Found relevant information"
        tool_used = "search"
        quality = 9.0 if is_formal else 8.5
    elif "calculate" in test_input.lower():
        response = "42"
        tool_used = "calculator"
        quality = 8.5 if is_formal else 9.0  # Casual better for math
    elif "api" in test_input.lower():
        response = "API data retrieved"
        tool_used = "api_call"
        quality = 8.8 if is_formal else 8.0
    else:
        response = "General response"
        tool_used = None
        quality = 7.5 if is_formal else 7.0
    
    # Validate
    success = True
    if "contains" in expected:
        success = expected["contains"].lower() in response.lower()
    
    return {
        "success": success,
        "tool_used": tool_used,
        "quality_score": quality
    }


# Test cases
test_cases = [
    {"input": "Search for Python tutorials", "expected": {"contains": "information"}},
    {"input": "Calculate 6 * 7", "expected": {"contains": "42"}},
    {"input": "Search for AI news", "expected": {"contains": "information"}},
    {"input": "Get API data for user", "expected": {"contains": "data"}},
    {"input": "Calculate square root of 16", "expected": {"contains": "4"}},
    {"input": "Search for best practices", "expected": {"contains": "information"}},
    {"input": "Get API status", "expected": {"contains": "data"}},
]


if __name__ == "__main__":
    # Initialize A/B tester
    tester = ABTester()
    
    # Define two prompt versions
    version_a = """You are a professional assistant with access to search, calculator, and API tools.
Provide formal, detailed responses."""
    
    version_b = """You are a helpful, casual assistant with search, calculator, and API tools.
Keep responses friendly and concise."""
    
    print("Running A/B test...\n")
    
    # Compare versions
    comparison = tester.compare_versions(version_a, version_b, test_cases, evaluator)
    
    # Generate and display report
    report = tester.generate_comparison_report(comparison, "ab_test_report.txt")
    print(report)
    
    # Save detailed results
    with open("ab_test_results.json", "w") as f:
        json.dump(comparison, f, indent=2)
    
    print("\nResults saved to ab_test_report.txt and ab_test_results.json")
    
    # Print recommendation
    winner = comparison["winner"]
    if winner == "tie":
        print("\n🤝 RECOMMENDATION: Both versions perform similarly. Choose based on tone preference.")
    elif winner == "version_a":
        print("\n🏆 RECOMMENDATION: Use Version A (formal prompt) for better performance.")
    else:
        print("\n🏆 RECOMMENDATION: Use Version B (casual prompt) for better performance.")
