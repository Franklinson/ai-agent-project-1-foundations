"""Example usage of PromptTester framework."""

from prompt_tester import PromptTester


def simple_evaluator(prompt: str, test_input: str, expected: dict) -> bool:
    """Simple evaluator that simulates prompt execution and validation."""
    # Simulate getting a response (in real use, call your LLM here)
    full_prompt = f"{prompt}\n\nUser: {test_input}"
    
    # Mock response based on input (replace with actual LLM call)
    if "2+2" in test_input:
        response = "The answer is 4"
    elif "AI" in test_input:
        response = "Artificial intelligence is computer systems that mimic human intelligence"
    elif "colors" in test_input:
        response = "Red, Blue, Green"
    else:
        response = "I don't know"
    
    # Validate response against expected criteria
    if "contains" in expected:
        if expected["contains"].lower() not in response.lower():
            return False
    
    if "max_words" in expected:
        if len(response.split()) > expected["max_words"]:
            return False
    
    if "count" in expected:
        # Simple count check (count commas + 1)
        if response.count(",") + 1 != expected["count"]:
            return False
    
    return True


if __name__ == "__main__":
    # Initialize tester
    tester = PromptTester()
    
    # Define prompt to test
    prompt = "You are a helpful assistant. Answer questions clearly and concisely."
    
    # Load test cases
    test_cases = tester.load_test_cases("test_cases.json")
    
    # Run tests
    results = tester.run_tests(prompt, test_cases, simple_evaluator)
    
    # Generate and print report
    report = tester.generate_report(results, "test_report.txt")
    print(report)
    
    # Also save as JSON
    import json
    with open("test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to test_report.txt and test_results.json")
