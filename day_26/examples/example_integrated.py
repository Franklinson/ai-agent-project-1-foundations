"""Integrated example: PromptTester + MetricsCalculator."""

from prompt_tester import PromptTester
from metrics_calculator import MetricsCalculator
import json


def advanced_evaluator(prompt: str, test_input: str, expected: dict) -> dict:
    """Enhanced evaluator that returns detailed results including tool usage."""
    # Simulate LLM response with tool usage
    if "search" in test_input.lower():
        response = "Found relevant information"
        tool_used = "search"
        quality = 8.5
    elif "calculate" in test_input.lower():
        response = "42"
        tool_used = "calculator"
        quality = 9.0
    elif "api" in test_input.lower():
        response = "API data retrieved"
        tool_used = "api_call"
        quality = 8.0
    else:
        response = "General response"
        tool_used = None
        quality = 7.0
    
    # Validate
    success = True
    if "contains" in expected:
        success = expected["contains"].lower() in response.lower()
    
    return {
        "success": success,
        "tool_used": tool_used,
        "quality_score": quality
    }


# Enhanced test cases with tool expectations
test_cases = [
    {"input": "Search for Python tutorials", "expected": {"contains": "information"}},
    {"input": "Calculate 6 * 7", "expected": {"contains": "42"}},
    {"input": "Search for AI news", "expected": {"contains": "information"}},
    {"input": "Get API data for user", "expected": {"contains": "data"}},
    {"input": "Calculate square root of 16", "expected": {"contains": "4"}},
]


if __name__ == "__main__":
    # Initialize both systems
    tester = PromptTester()
    calculator = MetricsCalculator()
    
    prompt = "You are a helpful assistant with access to search, calculator, and API tools."
    
    # Custom test runner that captures tool usage
    results = {
        "timestamp": "",
        "total": len(test_cases),
        "passed": 0,
        "failed": 0,
        "results": []
    }
    
    for i, test_case in enumerate(test_cases):
        eval_result = advanced_evaluator(prompt, test_case["input"], test_case["expected"])
        
        if eval_result["success"]:
            results["passed"] += 1
            status = "PASS"
        else:
            results["failed"] += 1
            status = "FAIL"
        
        results["results"].append({
            "test_id": i + 1,
            "status": status,
            "input": test_case["input"],
            "tool_used": eval_result["tool_used"],
            "quality_score": eval_result["quality_score"]
        })
    
    from datetime import datetime
    results["timestamp"] = datetime.now().isoformat()
    results["pass_rate"] = f"{(results['passed']/results['total']*100):.1f}%"
    
    # Generate test report
    print("=== Test Execution ===")
    test_report = tester.generate_report(results)
    print(test_report)
    
    # Calculate and display metrics
    print("\n" + "="*50)
    metrics = calculator.calculate_all_metrics(results)
    metrics_report = calculator.generate_metrics_report(metrics, "integrated_metrics.txt")
    print(metrics_report)
    
    # Save combined results
    with open("integrated_results.json", "w") as f:
        json.dump({"test_results": results, "metrics": metrics}, f, indent=2)
    
    print("\nIntegrated results saved to integrated_results.json and integrated_metrics.txt")
