"""Test agent with tools integration."""

from agent_with_tools import AgentWithTools


def print_result(title: str, result: dict):
    """Print formatted result."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Intent: {result['perceived']['intent']}")
    print(f"Entities: {result['perceived']['entities']}")
    print(f"Available Tools: {result['reasoning']['analysis']['available_tools']}")
    print(f"\nPlan: {result['reasoning']['plan']}")
    print(f"\nAction Results:")
    for action in result['actions']:
        if action['success']:
            print(f"  ✓ {action['tool']}: {action['result']}")
        else:
            print(f"  ✗ {action['tool']}: {action['error']}")
    print(f"\nDecision: {result['decision']}")


def main():
    agent = AgentWithTools()
    
    # Test 1: Search
    result = agent.run("Find information about Python", "Search for Python")
    print_result("Test 1: Search Query", result)
    
    # Test 2: Calculator
    result = agent.run("Calculate 15 multiply 3", "Perform calculation")
    print_result("Test 2: Calculator", result)
    
    # Test 3: Time
    result = agent.run("What time is it?", "Get current time")
    print_result("Test 3: Time Query", result)
    
    # Test 4: Default search
    result = agent.run("Tell me about AI agents", "General query")
    print_result("Test 4: General Query", result)


if __name__ == '__main__':
    main()
