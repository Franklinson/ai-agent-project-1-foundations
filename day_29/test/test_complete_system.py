from complete_agent import CompleteAgent


def test_component_integration():
    """Test all components are properly integrated"""
    print("=== Component Integration Test ===\n")
    
    agent = CompleteAgent()
    
    # Verify components exist
    assert agent.loop_controller is not None, "Loop controller missing"
    assert agent.tool_registry is not None, "Tool registry missing"
    assert agent.tool_executor is not None, "Tool executor missing"
    
    # Verify loop controller has all modules
    assert agent.loop_controller.perception is not None, "Perception module missing"
    assert agent.loop_controller.reasoning is not None, "Reasoning module missing"
    assert agent.loop_controller.action is not None, "Action module missing"
    assert agent.loop_controller.observation is not None, "Observation module missing"
    assert agent.loop_controller.state is not None, "State manager missing"
    
    print("✓ All components integrated")
    print("✓ Loop controller has all modules")
    print("✓ Tool system integrated\n")


def test_complete_loop_execution():
    """Test complete loop execution"""
    print("=== Complete Loop Execution Test ===\n")
    
    agent = CompleteAgent()
    result = agent.run(
        user_input="Test complete loop",
        goal="Execute full loop",
        max_iterations=3
    )
    
    # Verify result structure
    assert 'status' in result, "Missing status"
    assert 'iterations' in result, "Missing iterations"
    assert 'termination_reason' in result, "Missing termination_reason"
    assert 'progress' in result, "Missing progress"
    assert 'history' in result, "Missing history"
    assert 'available_tools' in result, "Missing available_tools"
    
    # Verify execution
    assert result['status'] == 'success', "Execution failed"
    assert result['iterations'] > 0, "No iterations executed"
    assert len(result['history']) == result['iterations'], "History mismatch"
    
    print(f"Status: {result['status']}")
    print(f"Iterations: {result['iterations']}")
    print(f"Termination: {result['termination_reason']}")
    print("✓ Complete loop executed successfully\n")


def test_all_phases_execute():
    """Test all phases execute in order"""
    print("=== All Phases Execution Test ===\n")
    
    agent = CompleteAgent()
    result = agent.run(
        user_input="Test all phases",
        goal="Verify phase execution",
        max_iterations=2
    )
    
    # Check first iteration has all phases
    first_iteration = result['history'][0]
    
    assert 'perceived' in first_iteration, "Perception not executed"
    assert 'reasoning' in first_iteration, "Reasoning not executed"
    assert 'actions' in first_iteration, "Action not executed"
    assert 'observation' in first_iteration, "Observation not executed"
    
    print("✓ Perception executed")
    print("✓ Reasoning executed")
    print("✓ Action executed")
    print("✓ Observation executed\n")


def test_tool_system_integration():
    """Test tool system is integrated"""
    print("=== Tool System Integration Test ===\n")
    
    agent = CompleteAgent()
    
    # Verify tools are registered
    tools = agent.tool_registry.list_all()
    assert len(tools) > 0, "No tools registered"
    
    tool_names = [t['name'] for t in tools]
    assert 'calculator' in tool_names, "Calculator tool missing"
    assert 'search' in tool_names, "Search tool missing"
    assert 'time' in tool_names, "Time tool missing"
    
    # Test tool execution
    calc_result = agent.tool_executor.execute('calculator', {'expression': '5+5'})
    assert calc_result['success'], "Calculator execution failed"
    assert calc_result['result']['result'] == 10, "Calculator result incorrect"
    
    print(f"Tools registered: {len(tools)}")
    print(f"Tool names: {tool_names}")
    print("✓ Tool system integrated and working\n")


def test_state_management():
    """Test state is managed across iterations"""
    print("=== State Management Test ===\n")
    
    agent = CompleteAgent()
    result = agent.run(
        user_input="Test state management",
        goal="Verify state tracking",
        max_iterations=3
    )
    
    # Verify state tracking
    assert len(result['history']) > 0, "No history recorded"
    assert len(result['progress']) > 0, "No progress tracked"
    
    # Verify iteration tracking
    for i, entry in enumerate(result['history'], 1):
        assert entry['iteration'] == i, f"Iteration {i} mismatch"
    
    print(f"History entries: {len(result['history'])}")
    print(f"Progress entries: {len(result['progress'])}")
    print("✓ State managed correctly\n")


def test_error_handling_integration():
    """Test error handling works in complete system"""
    print("=== Error Handling Integration Test ===\n")
    
    agent = CompleteAgent()
    
    # Simulate error
    original = agent.loop_controller.perception.process
    agent.loop_controller.perception.process = lambda x: (_ for _ in ()).throw(ValueError("Test error"))
    
    result = agent.run(
        user_input="Test error",
        goal="Handle error",
        max_iterations=2
    )
    
    agent.loop_controller.perception.process = original
    
    # Verify error was handled
    assert 'errors' in result, "Errors not tracked"
    assert len(result['errors']) > 0, "Error not captured"
    
    print(f"Errors captured: {len(result['errors'])}")
    print(f"Error phase: {result['errors'][0]['phase']}")
    print("✓ Error handling integrated\n")


def test_termination_conditions():
    """Test all termination conditions work"""
    print("=== Termination Conditions Test ===\n")
    
    agent = CompleteAgent()
    
    # Test goal achievement
    result1 = agent.run("Simple task", "Complete task", max_iterations=5)
    assert result1['termination_reason'] in ['goal_achieved', 'max_iterations_reached']
    print(f"Test 1 - Termination: {result1['termination_reason']}")
    
    # Test max iterations
    result2 = agent.run("Task", "Goal", max_iterations=1)
    assert result2['iterations'] <= 1
    print(f"Test 2 - Max iterations enforced: {result2['iterations']} <= 1")
    
    print("✓ All termination conditions work\n")


def test_summary_generation():
    """Test summary generation"""
    print("=== Summary Generation Test ===\n")
    
    agent = CompleteAgent()
    result = agent.run("Test summary", "Generate summary", max_iterations=2)
    
    summary = agent.get_summary(result)
    
    assert 'Status:' in summary, "Status missing from summary"
    assert 'Iterations:' in summary, "Iterations missing from summary"
    assert 'Termination:' in summary, "Termination missing from summary"
    
    print("Summary generated:")
    print(summary)
    print("\n✓ Summary generation works\n")


if __name__ == "__main__":
    test_component_integration()
    test_complete_loop_execution()
    test_all_phases_execute()
    test_tool_system_integration()
    test_state_management()
    test_error_handling_integration()
    test_termination_conditions()
    test_summary_generation()
    
    print("="*50)
    print("ALL COMPLETE SYSTEM TESTS PASSED")
    print("="*50)
