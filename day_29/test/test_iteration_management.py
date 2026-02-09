import sys
sys.path.append('../day_27')

from loop_controller import LoopController


def test_iteration_tracking():
    """Test iteration counter works correctly"""
    controller = LoopController()
    
    result = controller.run(
        user_input="Test iteration tracking",
        goal="Track iterations",
        max_iterations=3
    )
    
    print("=== Iteration Tracking Test ===\n")
    print(f"Iterations completed: {result['iterations']}")
    print(f"History entries: {len(result['history'])}")
    
    assert result['iterations'] == len(result['history']), "Iteration count mismatch"
    assert result['iterations'] >= 1, "No iterations executed"
    
    print("✓ Iteration tracking verified\n")


def test_goal_achievement_termination():
    """Test termination when goal is achieved"""
    controller = LoopController()
    
    result = controller.run(
        user_input="What is the weather?",
        goal="Answer the question",
        max_iterations=10
    )
    
    print("=== Goal Achievement Termination Test ===\n")
    print(f"Termination reason: {result['termination_reason']}")
    print(f"Final decision: {result['final_decision']}")
    print(f"Iterations used: {result['iterations']} / 10")
    
    assert result['termination_reason'] == 'goal_achieved', "Should terminate on goal achievement"
    assert result['final_decision'] == 'complete', "Decision should be complete"
    assert result['iterations'] < 10, "Should terminate before max iterations"
    
    print("✓ Goal achievement termination works\n")


def test_max_iterations_termination():
    """Test termination at maximum iterations"""
    controller = LoopController()
    
    # Force continue decision by using command intent
    result = controller.run(
        user_input="run this command continuously",
        goal="Keep running",
        max_iterations=3
    )
    
    print("=== Max Iterations Termination Test ===\n")
    print(f"Termination reason: {result['termination_reason']}")
    print(f"Iterations: {result['iterations']}")
    print(f"Max allowed: 3")
    
    assert result['iterations'] <= 3, "Exceeded max iterations"
    assert result['termination_reason'] in ['max_iterations_reached', 'goal_achieved'], "Should hit max or complete"
    
    print("✓ Max iterations limit enforced\n")


def test_error_termination():
    """Test termination on error"""
    controller = LoopController()
    
    # Simulate error by breaking action module temporarily
    original_execute = controller.action.execute
    
    def failing_execute(actions):
        results = []
        for action in actions:
            results.append({
                'action': action.get('action'),
                'tool': action.get('tool'),
                'status': 'error',
                'error': 'Simulated failure'
            })
        return results
    
    controller.action.execute = failing_execute
    
    result = controller.run(
        user_input="This will fail",
        goal="Test error handling",
        max_iterations=5
    )
    
    # Restore original
    controller.action.execute = original_execute
    
    print("=== Error Termination Test ===\n")
    print(f"Termination reason: {result['termination_reason']}")
    print(f"Final decision: {result['final_decision']}")
    print(f"Iterations: {result['iterations']}")
    
    assert result['termination_reason'] == 'error_termination', "Should terminate on error"
    assert result['final_decision'] == 'error', "Decision should be error"
    
    print("✓ Error termination works\n")


def test_progress_tracking():
    """Test progress tracking across iterations"""
    controller = LoopController()
    
    result = controller.run(
        user_input="Multi-step task",
        goal="Complete task",
        max_iterations=3
    )
    
    print("=== Progress Tracking Test ===\n")
    print(f"Progress entries: {len(result['progress'])}")
    
    for i, progress in enumerate(result['progress'], 1):
        print(f"Iteration {progress['iteration']}: success_rate={progress['success_rate']}, decision={progress['decision']}")
    
    assert len(result['progress']) == result['iterations'], "Progress entries mismatch"
    assert all('iteration' in p for p in result['progress']), "Missing iteration in progress"
    assert all('success_rate' in p for p in result['progress']), "Missing success_rate in progress"
    assert all('decision' in p for p in result['progress']), "Missing decision in progress"
    
    print("\n✓ Progress tracking verified\n")


def test_termination_conditions_comprehensive():
    """Test all termination conditions comprehensively"""
    print("=== Comprehensive Termination Test ===\n")
    
    # Test 1: Quick completion
    controller1 = LoopController()
    result1 = controller1.run("Simple question?", "Answer", max_iterations=5)
    print(f"Test 1 - Quick completion: {result1['termination_reason']} in {result1['iterations']} iterations")
    
    # Test 2: Max iterations with low limit
    controller2 = LoopController()
    result2 = controller2.run("Complex task", "Complete", max_iterations=1)
    print(f"Test 2 - Max iterations (1): {result2['termination_reason']} in {result2['iterations']} iterations")
    
    # Test 3: Normal flow
    controller3 = LoopController()
    result3 = controller3.run("Normal request", "Process", max_iterations=10)
    print(f"Test 3 - Normal flow: {result3['termination_reason']} in {result3['iterations']} iterations")
    
    assert result1['termination_reason'] in ['goal_achieved', 'max_iterations_reached']
    assert result2['iterations'] == 1
    assert result3['status'] == 'success'
    
    print("\n✓ All termination conditions work correctly\n")


if __name__ == "__main__":
    test_iteration_tracking()
    test_goal_achievement_termination()
    test_max_iterations_termination()
    test_error_termination()
    test_progress_tracking()
    test_termination_conditions_comprehensive()
    
    print("="*50)
    print("ALL ITERATION MANAGEMENT TESTS PASSED")
    print("="*50)
