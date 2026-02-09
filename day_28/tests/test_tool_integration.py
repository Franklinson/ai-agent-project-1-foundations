"""Tests for tool integration system."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../day_27'))

from tool_registry import ToolRegistry
from tool_executor import ToolExecutor
from tools import calculator, search, get_time
from agent_with_tools import AgentWithTools


def test_tool_registration():
    """Test tool registration."""
    print("=== Test 1: Tool Registration ===")
    
    registry = ToolRegistry()
    registry.register(calculator)
    registry.register(search)
    registry.register(get_time)
    
    # Verify registration
    tools = registry.list_all()
    assert len(tools) == 3, f"Expected 3 tools, got {len(tools)}"
    
    tool_names = [t['name'] for t in tools]
    assert 'calculator' in tool_names
    assert 'search' in tool_names
    assert 'get_time' in tool_names
    
    # Verify metadata
    calc = registry.get('calculator')
    assert calc is not None
    assert 'parameters' in calc
    assert 'operation' in calc['parameters']
    
    print("✓ Tool registration works")
    print(f"✓ Registered {len(tools)} tools")
    print(f"✓ Tools: {tool_names}")
    return True


def test_tool_execution():
    """Test tool execution."""
    print("\n=== Test 2: Tool Execution ===")
    
    registry = ToolRegistry()
    registry.register(calculator)
    registry.register(search)
    registry.register(get_time)
    
    executor = ToolExecutor(registry)
    
    # Test calculator
    result = executor.execute('calculator', {'operation': 'add', 'a': 10, 'b': 5})
    assert result['success'] == True
    assert result['result']['result'] == 15
    print("✓ Calculator: 10 + 5 = 15")
    
    # Test search
    result = executor.execute('search', {'query': 'Python'})
    assert result['success'] == True
    assert result['result']['count'] >= 0
    print(f"✓ Search: Found {result['result']['count']} matches for 'Python'")
    
    # Test time
    result = executor.execute('get_time', {'format': 'readable'})
    assert result['success'] == True
    assert 'time' in result['result']
    print(f"✓ Time: {result['result']['time']}")
    
    return True


def test_tool_result_handling():
    """Test tool result handling."""
    print("\n=== Test 3: Tool Result Handling ===")
    
    registry = ToolRegistry()
    registry.register(calculator)
    executor = ToolExecutor(registry)
    
    # Test missing tool
    result = executor.execute('nonexistent', {})
    assert result['success'] == False
    assert 'not found' in result['error'].lower()
    print("✓ Missing tool error handled")
    
    # Test missing parameters
    result = executor.execute('calculator', {'operation': 'add'})
    assert result['success'] == False
    assert 'missing' in result['error'].lower()
    print("✓ Missing parameters error handled")
    
    # Test invalid operation
    result = executor.execute('calculator', {'operation': 'invalid', 'a': 1, 'b': 2})
    assert result['success'] == False
    print("✓ Invalid operation error handled")
    
    # Test division by zero
    result = executor.execute('calculator', {'operation': 'divide', 'a': 10, 'b': 0})
    assert result['success'] == False
    print("✓ Division by zero error handled")
    
    return True


def test_agent_tool_usage():
    """Test agent with tools."""
    print("\n=== Test 4: Agent Tool Usage ===")
    
    agent = AgentWithTools()
    
    # Verify agent has tools
    tools = agent.registry.list_all()
    assert len(tools) == 3
    print(f"✓ Agent has {len(tools)} tools available")
    
    # Test direct execution through agent
    result = agent.executor.execute('calculator', {'operation': 'multiply', 'a': 7, 'b': 6})
    assert result['success'] == True
    assert result['result']['result'] == 42
    print("✓ Agent executor: 7 * 6 = 42")
    
    # Test reasoning module
    perceived = {'intent': 'calculate', 'entities': ['multiply', 12, 3], 'text': 'test'}
    reasoning = agent.reasoning.reason(perceived, {})
    assert len(reasoning['plan']) > 0
    assert reasoning['plan'][0]['tool'] == 'calculator'
    print("✓ Reasoning module creates tool-based plans")
    
    # Test action module
    actions = agent.action.execute(reasoning['plan'])
    assert len(actions) > 0
    assert actions[0]['success'] == True
    print("✓ Action module executes tools")
    
    return True


def test_integration_scenarios():
    """Test various integration scenarios."""
    print("\n=== Test 5: Integration Scenarios ===")
    
    agent = AgentWithTools()
    
    # Scenario 1: Calculator with multiply
    result = agent.executor.execute('calculator', {'operation': 'multiply', 'a': 8, 'b': 9})
    assert result['success'] and result['result']['result'] == 72
    print("✓ Scenario 1: Multiply 8 * 9 = 72")
    
    # Scenario 2: Search for AI
    result = agent.executor.execute('search', {'query': 'AI'})
    assert result['success'] and result['result']['count'] > 0
    print(f"✓ Scenario 2: Search 'AI' found {result['result']['count']} matches")
    
    # Scenario 3: Get time in ISO format
    result = agent.executor.execute('get_time', {'format': 'iso'})
    assert result['success'] and 'T' in result['result']['time']
    print("✓ Scenario 3: Get time in ISO format")
    
    # Scenario 4: Power operation
    result = agent.executor.execute('calculator', {'operation': 'power', 'a': 2, 'b': 8})
    assert result['success'] and result['result']['result'] == 256
    print("✓ Scenario 4: Power 2^8 = 256")
    
    # Scenario 5: Search with no matches
    result = agent.executor.execute('search', {'query': 'xyz123notfound'})
    assert result['success'] and result['result']['count'] == 0
    print("✓ Scenario 5: Search with no matches handled")
    
    return True


def run_all_tests():
    """Run all tests."""
    print("="*60)
    print("TOOL INTEGRATION TEST SUITE")
    print("="*60)
    
    tests = [
        test_tool_registration,
        test_tool_execution,
        test_tool_result_handling,
        test_agent_tool_usage,
        test_integration_scenarios
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"✗ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ Test error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
