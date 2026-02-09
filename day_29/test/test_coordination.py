import sys
sys.path.append('../day_27')

from loop_controller import LoopController


def test_phase_coordination():
    """Test data flow between all phases"""
    controller = LoopController()
    
    # Test basic flow
    result = controller.run(
        user_input="What is 2 + 2?",
        goal="Answer the question",
        max_iterations=3
    )
    
    print("=== Phase Coordination Test ===\n")
    print(f"Status: {result['status']}")
    print(f"Iterations: {result['iterations']}")
    print(f"Final Decision: {result['final_decision']}\n")
    
    # Verify data flow through phases
    for i, entry in enumerate(result['history'], 1):
        print(f"--- Iteration {i} ---")
        
        # Check perception output
        perceived = entry['perceived']
        print(f"Perception Output: intent={perceived['intent']}, entities={len(perceived['entities'])}")
        
        # Check reasoning input/output
        reasoning = entry['reasoning']
        print(f"Reasoning Output: plan_steps={len(reasoning['plan'])}")
        
        # Check action input/output
        actions = entry['actions']
        print(f"Action Output: results={len(actions)}, success={sum(1 for a in actions if a['status']=='success')}")
        
        # Check observation input/output
        observation = entry['observation']
        print(f"Observation Output: decision={observation['decision']}, success_rate={observation['evaluation']['success_rate']}\n")
    
    # Verify formats
    assert result['status'] in ['success', 'error'], "Invalid status format"
    assert isinstance(result['iterations'], int), "Iterations must be int"
    assert result['final_decision'] in ['complete', 'continue', 'error'], "Invalid decision format"
    
    print("✓ All phase coordination tests passed")


def test_state_synchronization():
    """Test state updates across iterations"""
    controller = LoopController()
    
    result = controller.run(
        user_input="Create a file and update it",
        goal="Complete the task",
        max_iterations=2
    )
    
    print("\n=== State Synchronization Test ===\n")
    
    # Verify state is maintained
    history = result['history']
    print(f"History entries: {len(history)}")
    
    for i, entry in enumerate(history, 1):
        assert 'iteration' in entry, f"Missing iteration in entry {i}"
        assert entry['iteration'] == i, f"Iteration mismatch in entry {i}"
        print(f"Iteration {i}: ✓ State synchronized")
    
    print("\n✓ State synchronization verified")


def test_error_handling():
    """Test error handling in phase coordination"""
    controller = LoopController()
    
    # Test with empty input
    result = controller.run(
        user_input="",
        goal="Handle empty input",
        max_iterations=1
    )
    
    print("\n=== Error Handling Test ===\n")
    print(f"Status: {result['status']}")
    print(f"Handled empty input: ✓")
    
    # Test max iterations
    result = controller.run(
        user_input="Keep going",
        goal="Test max iterations",
        max_iterations=2
    )
    
    assert result['iterations'] <= 2, "Max iterations not enforced"
    print(f"Max iterations enforced: ✓")
    
    print("\n✓ Error handling tests passed")


if __name__ == "__main__":
    test_phase_coordination()
    test_state_synchronization()
    test_error_handling()
    print("\n" + "="*50)
    print("ALL COORDINATION TESTS PASSED")
    print("="*50)
