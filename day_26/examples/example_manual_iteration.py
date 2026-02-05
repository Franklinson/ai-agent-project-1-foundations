"""Advanced iteration workflow with manual control."""

from iteration_workflow import IterationWorkflow
import json


def evaluator(prompt: str, test_input: str, expected: dict) -> dict:
    """Enhanced evaluator."""
    # Analyze prompt features
    features = {
        "structured": "step" in prompt.lower() or "first" in prompt.lower(),
        "examples": "example" in prompt.lower(),
        "constraints": "must" in prompt.lower() or "always" in prompt.lower(),
        "tools": "tool" in prompt.lower(),
        "detailed": len(prompt) > 100
    }
    
    # Calculate base quality from features
    quality = 6.0 + sum([1.0 for v in features.values() if v])
    
    # Simulate task-specific responses
    success = True
    tool_used = None
    
    if "search" in test_input.lower():
        tool_used = "search"
        success = features["tools"]
    elif "calculate" in test_input.lower():
        tool_used = "calculator"
        success = features["structured"] or features["examples"]
    elif "analyze" in test_input.lower():
        success = features["detailed"] and features["structured"]
    
    if "contains" in expected:
        response = "information" if "search" in test_input.lower() else "result"
        success = success and expected["contains"].lower() in response.lower()
    
    return {
        "success": success,
        "tool_used": tool_used,
        "quality_score": min(quality, 10.0)
    }


# Complex test cases
test_cases = [
    {"input": "Search for machine learning papers", "expected": {"contains": "information"}},
    {"input": "Calculate compound interest", "expected": {"contains": "result"}},
    {"input": "Analyze this dataset", "expected": {"contains": "result"}},
    {"input": "Search for best practices", "expected": {"contains": "information"}},
    {"input": "Calculate average", "expected": {"contains": "result"}},
]


if __name__ == "__main__":
    workflow = IterationWorkflow()
    
    # Manual iteration with different prompt strategies
    prompts = {
        "v1_basic": "You are an AI assistant that helps users.",
        
        "v2_with_tools": """You are an AI assistant with search and calculator tools.
Help users with their questions.""",
        
        "v3_structured": """You are an AI assistant with search and calculator tools.
Follow these steps:
1. Understand the user's request
2. Choose the appropriate tool
3. Provide a clear answer""",
        
        "v4_with_examples": """You are an AI assistant with search and calculator tools.
Follow these steps:
1. Understand the user's request
2. Choose the appropriate tool
3. Provide a clear answer

Example: For searches, use the search tool to find relevant information.""",
        
        "v5_complete": """You are an AI assistant with search and calculator tools.
You must always follow these steps:
1. Understand the user's request
2. Choose the appropriate tool
3. Provide a clear answer

Example: For searches, use the search tool to find relevant information.
You must verify your responses before returning them."""
    }
    
    print("="*60)
    print("MANUAL ITERATION WORKFLOW")
    print("="*60 + "\n")
    
    # Run each version
    for version_name, prompt in prompts.items():
        print(f"Testing {version_name}...")
        iteration = workflow.run_iteration(prompt, test_cases, evaluator, version_name)
        print(f"  Success: {iteration['metrics']['success_rate']}% | "
              f"Quality: {iteration['metrics']['quality_score']}%")
        print(f"  Performance: {iteration['analysis']['performance']}")
        if iteration['analysis']['issues']:
            print(f"  Issues: {', '.join(iteration['analysis']['issues'])}")
        print()
    
    # Generate report
    print("="*60)
    print("ITERATION REPORT")
    print("="*60)
    report = workflow.generate_iteration_report("manual_iteration_report.txt")
    print(report)
    
    # Save workflow
    workflow.save_workflow("manual_workflow_history.json")
    
    # Best version
    best = workflow.get_best_version()
    print("\n" + "="*60)
    print("RECOMMENDED PROMPT")
    print("="*60)
    print(f"\nVersion: {best['version']}")
    print(f"Performance: {best['success_rate']}% success, {best['quality_score']}% quality")
    print(f"\nPrompt:\n{best['prompt']}")
    
    # Compare specific versions
    print("\n" + "="*60)
    print("VERSION COMPARISONS")
    print("="*60)
    
    comparisons = [
        (1, 2, "Basic vs With Tools"),
        (2, 3, "With Tools vs Structured"),
        (3, 5, "Structured vs Complete")
    ]
    
    for iter_a, iter_b, label in comparisons:
        comp = workflow.compare_iterations(iter_a, iter_b)
        print(f"\n{label}:")
        print(f"  Success Rate: {comp['success_rate_change']:+.2f}%")
        print(f"  Quality Score: {comp['quality_score_change']:+.2f}%")
        print(f"  Improved: {'✓' if comp['improvement'] else '✗'}")
    
    print("\n✓ Results saved to manual_iteration_report.txt and manual_workflow_history.json")
