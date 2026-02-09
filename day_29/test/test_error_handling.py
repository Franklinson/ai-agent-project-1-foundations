import sys
sys.path.append('../day_27')

from loop_controller import LoopController


def test_perception_error_handling():
    """Test perception phase error handling"""
    controller = LoopController()
    
    # Break perception
    original_process = controller.perception.process
    def failing_process(user_input):
        raise ValueError("Perception failed")
    
    controller.perception.process = failing_process
    
    result = controller.run(
        user_input="Test input",
        goal="Test perception error",
        max_iterations=2
    )
    
    controller.perception.process = original_process
    
    print("=== Perception Error Handling Test ===\n")
    print(f"Status: {result['status']}")
    print(f"Errors: {len(result['errors'])}")
    print(f"Error phase: {result['errors'][0]['phase'] if result['errors'] else 'none'}")
    
    assert len(result['errors']) > 0, "Should capture perception error"
    assert result['errors'][0]['phase'] == 'perception', "Should identify perception phase"
    assert result['status'] == 'success', "Should recover from perception error"
    
    print("✓ Perception error handled and recovered\n")


def test_reasoning_error_handling():
    """Test reasoning phase error handling"""
    controller = LoopController()
    
    # Break reasoning
    original_reason = controller.reasoning.reason
    def failing_reason(processed_input, context):
        raise RuntimeError("Reasoning failed")
    
    controller.reasoning.reason = failing_reason
    
    result = controller.run(
        user_input="Test input",
        goal="Test reasoning error",
        max_iterations=2
    )
    
    controller.reasoning.reason = original_reason
    
    print("=== Reasoning Error Handling Test ===\n")
    print(f"Status: {result['status']}")
    print(f"Errors: {len(result['errors'])}")
    print(f"Error phase: {result['errors'][0]['phase'] if result['errors'] else 'none'}")
    
    assert len(result['errors']) > 0, "Should capture reasoning error"
    assert result['errors'][0]['phase'] == 'reasoning', "Should identify reasoning phase"
    assert result['status'] == 'success', "Should recover from reasoning error"
    
    print("✓ Reasoning error handled and recovered\n")


def test_action_error_handling():
    """Test action phase error handling"""
    controller = LoopController()
    
    # Break action
    original_execute = controller.action.execute
    def failing_execute(actions):
        raise Exception("Action execution failed")
    
    controller.action.execute = failing_execute
    
    result = controller.run(
        user_input="Test input",
        goal="Test action error",
        max_iterations=2
    )
    
    controller.action.execute = original_execute
    
    print("=== Action Error Handling Test ===\n")
    print(f"Status: {result['status']}")
    print(f"Errors: {len(result['errors'])}")
    print(f"Error phase: {result['errors'][0]['phase'] if result['errors'] else 'none'}")
    
    assert len(result['errors']) > 0, "Should capture action error"
    assert result['errors'][0]['phase'] == 'action', "Should identify action phase"
    assert result['status'] == 'success', "Should recover from action error"
    
    print("✓ Action error handled and recovered\n")


def test_observation_error_handling():
    """Test observation phase error handling"""
    controller = LoopController()
    
    # Break observation
    original_observe = controller.observation.observe
    def failing_observe(results, goal):
        raise KeyError("Observation failed")
    
    controller.observation.observe = failing_observe
    
    result = controller.run(
        user_input="Test input",
        goal="Test observation error",
        max_iterations=2
    )
    
    controller.observation.observe = original_observe
    
    print("=== Observation Error Handling Test ===\n")
    print(f"Status: {result['status']}")
    print(f"Errors: {len(result['errors'])}")
    print(f"Error phase: {result['errors'][0]['phase'] if result['errors'] else 'none'}")
    
    assert len(result['errors']) > 0, "Should capture observation error"
    assert result['errors'][0]['phase'] == 'observation', "Should identify observation phase"
    assert result['status'] == 'success', "Should recover from observation error"
    
    print("✓ Observation error handled and recovered\n")


def test_loop_level_error_handling():
    """Test loop-level error handling"""
    controller = LoopController()
    
    # Break state manager to cause loop-level error
    original_add = controller.state.add_to_history
    def failing_add(entry):
        raise RuntimeError("State update failed")
    
    controller.state.add_to_history = failing_add
    
    result = controller.run(
        user_input="Test input",
        goal="Test loop error",
        max_iterations=2
    )
    
    controller.state.add_to_history = original_add
    
    print("=== Loop-Level Error Handling Test ===\n")
    print(f"Status: {result['status']}")
    print(f"Termination reason: {result['termination_reason']}")
    print(f"Error captured: {result.get('error', 'none')}")
    
    assert result['status'] == 'error', "Should report error status"
    assert result['termination_reason'] == 'loop_error', "Should identify loop error"
    assert 'error' in result, "Should include error message"
    
    print("✓ Loop-level error handled\n")


def test_error_recovery():
    """Test error recovery mechanisms"""
    controller = LoopController()
    
    # Simulate recoverable error in first iteration
    call_count = [0]
    original_reason = controller.reasoning.reason
    
    def sometimes_failing_reason(processed_input, context):
        call_count[0] += 1
        if call_count[0] == 1:
            raise ValueError("First call fails")
        return original_reason(processed_input, context)
    
    controller.reasoning.reason = sometimes_failing_reason
    
    result = controller.run(
        user_input="Test recovery",
        goal="Test error recovery",
        max_iterations=3
    )
    
    controller.reasoning.reason = original_reason
    
    print("=== Error Recovery Test ===\n")
    print(f"Status: {result['status']}")
    print(f"Iterations: {result['iterations']}")
    print(f"Errors encountered: {len(result['errors'])}")
    print(f"Recovered: {result['status'] == 'success'}")
    
    assert result['status'] == 'success', "Should recover and continue"
    assert len(result['errors']) > 0, "Should record the error"
    assert result['iterations'] >= 1, "Should complete iterations"
    
    print("✓ Error recovery works\n")


def test_error_propagation():
    """Test error propagation through phases"""
    controller = LoopController()
    
    # Break perception to see error propagate
    original_process = controller.perception.process
    controller.perception.process = lambda x: None  # Return None to trigger propagation
    
    result = controller.run(
        user_input="Test propagation",
        goal="Test error propagation",
        max_iterations=2
    )
    
    controller.perception.process = original_process
    
    print("=== Error Propagation Test ===\n")
    print(f"Status: {result['status']}")
    print(f"Iterations: {result['iterations']}")
    print(f"Termination: {result['termination_reason']}")
    
    # Should handle None gracefully
    assert result['status'] in ['success', 'error'], "Should handle propagation"
    
    print("✓ Error propagation handled\n")


def test_multiple_errors():
    """Test handling multiple errors across iterations"""
    controller = LoopController()
    
    # Cause errors in multiple phases
    original_reason = controller.reasoning.reason
    original_action = controller.action.execute
    
    def failing_reason(processed_input, context):
        raise ValueError("Reasoning error")
    
    def failing_action(actions):
        raise RuntimeError("Action error")
    
    controller.reasoning.reason = failing_reason
    controller.action.execute = failing_action
    
    result = controller.run(
        user_input="Test multiple errors",
        goal="Test multiple errors",
        max_iterations=2
    )
    
    controller.reasoning.reason = original_reason
    controller.action.execute = original_action
    
    print("=== Multiple Errors Test ===\n")
    print(f"Status: {result['status']}")
    print(f"Total errors: {len(result['errors'])}")
    
    for i, error in enumerate(result['errors'], 1):
        print(f"Error {i}: {error['phase']}")
    
    assert len(result['errors']) >= 2, "Should capture multiple errors"
    
    print("\n✓ Multiple errors handled\n")


if __name__ == "__main__":
    test_perception_error_handling()
    test_reasoning_error_handling()
    test_action_error_handling()
    test_observation_error_handling()
    test_loop_level_error_handling()
    test_error_recovery()
    test_error_propagation()
    test_multiple_errors()
    
    print("="*50)
    print("ALL ERROR HANDLING TESTS PASSED")
    print("="*50)
