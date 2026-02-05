"""Example usage of MetricsCalculator."""

from metrics_calculator import MetricsCalculator
import json


# Sample test results with tool usage data
sample_results = {
    "timestamp": "2024-02-05T10:30:00",
    "total": 10,
    "passed": 7,
    "failed": 3,
    "results": [
        {"test_id": 1, "status": "PASS", "tool_used": "search", "quality_score": 8.5},
        {"test_id": 2, "status": "PASS", "tool_used": "search", "quality_score": 9.0},
        {"test_id": 3, "status": "FAIL", "tool_used": "calculator"},
        {"test_id": 4, "status": "PASS", "tool_used": "calculator", "quality_score": 7.5},
        {"test_id": 5, "status": "PASS", "tool_used": "search", "quality_score": 8.0},
        {"test_id": 6, "status": "ERROR", "tool_used": "api_call"},
        {"test_id": 7, "status": "PASS", "tool_used": "api_call", "quality_score": 9.5},
        {"test_id": 8, "status": "FAIL", "tool_used": "calculator"},
        {"test_id": 9, "status": "PASS", "tool_used": "search", "quality_score": 8.8},
        {"test_id": 10, "status": "PASS", "tool_used": "api_call", "quality_score": 9.2}
    ]
}


if __name__ == "__main__":
    # Initialize calculator
    calculator = MetricsCalculator()
    
    # Calculate individual metrics
    print("Individual Metrics:")
    print(f"Success Rate: {calculator.calculate_success_rate(sample_results)}%")
    print(f"Quality Score: {calculator.calculate_quality_score(sample_results)}%")
    print(f"Tool Accuracy: {calculator.calculate_tool_accuracy(sample_results)}")
    
    print("\n" + "="*50 + "\n")
    
    # Calculate all metrics
    metrics = calculator.calculate_all_metrics(sample_results)
    
    # Generate and print report
    report = calculator.generate_metrics_report(metrics, "metrics_report.txt")
    print(report)
    
    # Save metrics as JSON
    with open("metrics_results.json", "w") as f:
        json.dump(metrics, f, indent=2)
    
    print("\nMetrics saved to metrics_report.txt and metrics_results.json")
