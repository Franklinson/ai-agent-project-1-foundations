"""Example iteration workflow with automated prompt refinement."""

from iteration_workflow import IterationWorkflow
from typing import Dict
import json


def evaluator(prompt: str, test_input: str, expected: dict) -> dict:
    """Evaluator that simulates LLM responses."""
    # Simulate improvement based on prompt characteristics
    has_examples = "example" in prompt.lower()
    has_constraints = "must" in prompt.lower()
    has_tools = "tools" in prompt.lower()
    is_detailed = len(prompt) > 80
    
    # Base quality
    quality = 7.0
    if has_examples:
        quality += 1.0
    if has_constraints:
        quality += 0.5
    if has_tools:
        quality += 1.0
    if is_detailed:
        quality += 0.5
    
    # Simulate responses
    if "search" in test_input.lower():
        response = "Found information"
        tool_used = "search"
        success = True
    elif "calculate" in test_input.lower():
        response = "42"
        tool_used = "calculator"
        # Calculator improves with constraints
        success = has_constraints or has_examples
    elif "api" in test_input.lower():
        response = "API data"
        tool_used = "api_call"
        success = has_tools
    else:
        response = "Response"
        tool_used = None
        success = is_detailed
    
    # Validate
    if "contains" in expected:
        success = success and expected["contains"].lower() in response.lower()
    
    return {
        "success": success,
        "tool_used": tool_used,
        "quality_score": min(quality, 10.0)
    }


def simple_refiner(prompt: str, iteration: Dict) -> str:
    """Simple prompt refiner based on iteration results."""
    analysis = iteration["analysis"]
    metrics = iteration["metrics"]
    
    # Start with current prompt
    refined = prompt
    
    # Add improvements based on issues
    if "failed" in str(analysis["issues"]):
        if "example" not in refined.lower():
            refined += "\nExample: For calculations, show your work."
    
    if metrics["success_rate"] < 80:
        if "must" not in refined.lower():
            refined += "\nYou must verify all responses before returning them."
    
    if "tool" in str(analysis["issues"]).lower():
        if "tools" not in refined.lower():
            refined += "\nUse appropriate tools for each task type."
    
    # Add detail if too short
    if len(refined) < 100:
        refined += " Provide clear and accurate responses."
    
    return refined


# Test cases
test_cases = [
    {"input": "Search for Python docs", "expected": {"contains": "information"}},
    {"input": "Calculate 10 + 5", "expected": {"contains": "15"}},
    {"input": "Search for tutorials", "expected": {"contains": "information"}},
    {"input": "Get API data", "expected": {"contains": "data"}},
    {"input": "Calculate 20 * 3", "expected": {"contains": "60"}},
    {"input": "General question", "expected": {"contains": "response"}},
]


if __name__ == "__main__":
    # Initialize workflow
    workflow = IterationWorkflow()
    
    # Initial prompt (intentionally basic)
    initial_prompt = "You are an AI assistant."
    
    print("="*60)
    print("AUTOMATED PROMPT ITERATION WORKFLOW")
    print("="*60 + "\n")
    
    # Run automated workflow
    summary = workflow.run_workflow(
        initial_prompt=initial_prompt,
        test_cases=test_cases,
        evaluator=evaluator,
        refiner=simple_refiner,
        max_iterations=5,
        target_score=90.0
    )
    
    print("\n" + "="*60)
    print("WORKFLOW COMPLETE")
    print("="*60 + "\n")
    
    # Generate report
    report = workflow.generate_iteration_report("iteration_report.txt")
    print(report)
    
    # Save workflow
    workflow.save_workflow("workflow_history.json")
    
    # Show best version
    best = workflow.get_best_version()
    print("\n" + "="*60)
    print("BEST VERSION")
    print("="*60)
    print(f"\nIteration: {best['iteration']}")
    print(f"Success Rate: {best['success_rate']}%")
    print(f"Quality Score: {best['quality_score']}%")
    print(f"\nPrompt:\n{best['prompt']}")
    
    # Compare first and last
    if len(workflow.iteration_history) > 1:
        comparison = workflow.compare_iterations(1, len(workflow.iteration_history))
        print("\n" + "="*60)
        print("FIRST vs LAST COMPARISON")
        print("="*60)
        print(f"Success Rate Change: {comparison['success_rate_change']:+.2f}%")
        print(f"Quality Score Change: {comparison['quality_score_change']:+.2f}%")
        print(f"Improved: {comparison['improvement']}")
    
    print("\n✓ All results saved to iteration_report.txt and workflow_history.json")
