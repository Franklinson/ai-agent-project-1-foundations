from complete_agent import CompleteAgent


def demo_basic_question():
    """Demo: Basic question handling"""
    print("="*60)
    print("DEMO 1: Basic Question")
    print("="*60)
    
    agent = CompleteAgent()
    result = agent.run(
        user_input="What is 2 + 2?",
        goal="Answer the mathematical question",
        max_iterations=3
    )
    
    print(f"\nInput: What is 2 + 2?")
    print(f"\n{agent.get_summary(result)}")
    print(f"\nIteration Details:")
    for i, entry in enumerate(result['history'], 1):
        print(f"  {i}. Intent: {entry['perceived']['intent']}, "
              f"Actions: {len(entry['actions'])}, "
              f"Decision: {entry['observation']['decision']}")
    print()


def demo_command_execution():
    """Demo: Command execution"""
    print("="*60)
    print("DEMO 2: Command Execution")
    print("="*60)
    
    agent = CompleteAgent()
    result = agent.run(
        user_input="Create a new file and update it",
        goal="Execute the command",
        max_iterations=5
    )
    
    print(f"\nInput: Create a new file and update it")
    print(f"\n{agent.get_summary(result)}")
    print(f"\nProgress Tracking:")
    for progress in result['progress']:
        print(f"  Iteration {progress['iteration']}: "
              f"Success Rate: {progress['success_rate']:.0%}, "
              f"Decision: {progress['decision']}")
    print()


def demo_error_handling():
    """Demo: Error handling"""
    print("="*60)
    print("DEMO 3: Error Handling")
    print("="*60)
    
    agent = CompleteAgent()
    
    # Break a component to trigger error
    original_process = agent.loop_controller.perception.process
    call_count = [0]
    
    def sometimes_failing(user_input):
        call_count[0] += 1
        if call_count[0] == 1:
            raise ValueError("Simulated perception error")
        return original_process(user_input)
    
    agent.loop_controller.perception.process = sometimes_failing
    
    result = agent.run(
        user_input="Test error recovery",
        goal="Handle errors gracefully",
        max_iterations=3
    )
    
    agent.loop_controller.perception.process = original_process
    
    print(f"\nInput: Test error recovery")
    print(f"\n{agent.get_summary(result)}")
    
    if result['errors']:
        print(f"\nErrors Encountered:")
        for error in result['errors']:
            print(f"  Phase: {error['phase']}, Error: {error['error']}")
    print()


def demo_max_iterations():
    """Demo: Maximum iterations"""
    print("="*60)
    print("DEMO 4: Maximum Iterations")
    print("="*60)
    
    agent = CompleteAgent()
    result = agent.run(
        user_input="Complex multi-step task",
        goal="Complete complex task",
        max_iterations=2
    )
    
    print(f"\nInput: Complex multi-step task")
    print(f"Max Iterations: 2")
    print(f"\n{agent.get_summary(result)}")
    print(f"\nTermination Reason: {result['termination_reason']}")
    print()


def demo_tool_integration():
    """Demo: Tool integration"""
    print("="*60)
    print("DEMO 5: Tool Integration")
    print("="*60)
    
    agent = CompleteAgent()
    result = agent.run(
        user_input="What time is it?",
        goal="Get current time",
        max_iterations=3
    )
    
    print(f"\nInput: What time is it?")
    print(f"\n{agent.get_summary(result)}")
    print(f"\nAvailable Tools:")
    for tool in result['available_tools']:
        print(f"  - {tool['name']}: {tool['description']}")
    print()


def demo_complete_workflow():
    """Demo: Complete workflow"""
    print("="*60)
    print("DEMO 6: Complete Workflow")
    print("="*60)
    
    agent = CompleteAgent()
    
    scenarios = [
        ("Hello, how are you?", "Respond to greeting"),
        ("Calculate 10 * 5", "Perform calculation"),
        ("Search for Python tutorials", "Search information"),
    ]
    
    for user_input, goal in scenarios:
        result = agent.run(user_input, goal, max_iterations=3)
        print(f"\nInput: {user_input}")
        print(f"Goal: {goal}")
        print(f"Result: {result['status']} in {result['iterations']} iteration(s)")
        print(f"Decision: {result['final_decision']}")
    print()


def main():
    """Run all demonstrations"""
    print("\n" + "="*60)
    print("COMPLETE AGENT DEMONSTRATION")
    print("="*60 + "\n")
    
    demo_basic_question()
    demo_command_execution()
    demo_error_handling()
    demo_max_iterations()
    demo_tool_integration()
    demo_complete_workflow()
    
    print("="*60)
    print("ALL DEMONSTRATIONS COMPLETED")
    print("="*60)


if __name__ == "__main__":
    main()
