"""Comprehensive demonstration of agent with tools."""

from agent_with_tools import AgentWithTools


def print_section(title):
    """Print section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def demo_tool_discovery():
    """Demonstrate tool discovery."""
    print_section("1. TOOL DISCOVERY")
    
    agent = AgentWithTools()
    tools = agent.registry.list_all()
    
    print(f"Available Tools: {len(tools)}\n")
    for tool in tools:
        print(f"📦 {tool['name']}")
        print(f"   Description: {tool['description']}")
        print(f"   Parameters: {list(tool['parameters'].keys())}")
        print()


def demo_calculator_operations():
    """Demonstrate calculator tool."""
    print_section("2. CALCULATOR OPERATIONS")
    
    agent = AgentWithTools()
    
    operations = [
        ('add', 45, 27, 72),
        ('subtract', 100, 37, 63),
        ('multiply', 12, 8, 96),
        ('divide', 144, 12, 12),
        ('power', 3, 4, 81),
        ('modulo', 17, 5, 2)
    ]
    
    for op, a, b, expected in operations:
        result = agent.executor.execute('calculator', {
            'operation': op,
            'a': a,
            'b': b
        })
        
        if result['success']:
            actual = result['result']['result']
            status = "✓" if actual == expected else "✗"
            print(f"{status} {op.capitalize()}: {a} {op} {b} = {actual}")
        else:
            print(f"✗ {op.capitalize()}: Error - {result['error']}")


def demo_search_operations():
    """Demonstrate search tool."""
    print_section("3. SEARCH OPERATIONS")
    
    agent = AgentWithTools()
    
    queries = ['Python', 'AI', 'machine learning', 'API', 'notfound']
    
    for query in queries:
        result = agent.executor.execute('search', {'query': query})
        
        if result['success']:
            count = result['result']['count']
            print(f"🔍 '{query}': {count} matches")
            if count > 0:
                print(f"   First match: {result['result']['matches'][0][:50]}...")
        else:
            print(f"✗ '{query}': Error - {result['error']}")
        print()


def demo_time_operations():
    """Demonstrate time tool."""
    print_section("4. TIME OPERATIONS")
    
    agent = AgentWithTools()
    
    formats = ['iso', 'timestamp', 'readable']
    
    for fmt in formats:
        result = agent.executor.execute('get_time', {'format': fmt})
        
        if result['success']:
            time_value = result['result']['time']
            print(f"🕐 Format '{fmt}': {time_value}")
        else:
            print(f"✗ Format '{fmt}': Error - {result['error']}")


def demo_error_handling():
    """Demonstrate error handling."""
    print_section("5. ERROR HANDLING")
    
    agent = AgentWithTools()
    
    # Test 1: Missing tool
    result = agent.executor.execute('nonexistent_tool', {})
    print(f"Missing tool: {result['error']}")
    
    # Test 2: Missing parameters
    result = agent.executor.execute('calculator', {'operation': 'add'})
    print(f"Missing params: {result['error']}")
    
    # Test 3: Invalid operation
    result = agent.executor.execute('calculator', {
        'operation': 'invalid',
        'a': 1,
        'b': 2
    })
    print(f"Invalid operation: {result['error']}")
    
    # Test 4: Division by zero
    result = agent.executor.execute('calculator', {
        'operation': 'divide',
        'a': 10,
        'b': 0
    })
    print(f"Division by zero: {result['error']}")
    
    # Test 5: Empty search query
    result = agent.executor.execute('search', {'query': ''})
    print(f"Empty query: {result['error']}")


def demo_agent_reasoning():
    """Demonstrate agent reasoning with tools."""
    print_section("6. AGENT REASONING")
    
    agent = AgentWithTools()
    
    scenarios = [
        {
            'intent': 'calculate',
            'entities': ['multiply', 15, 4],
            'description': 'Calculate 15 * 4'
        },
        {
            'intent': 'search',
            'entities': ['Python'],
            'description': 'Search for Python'
        },
        {
            'intent': 'time',
            'entities': [],
            'description': 'Get current time'
        }
    ]
    
    for scenario in scenarios:
        print(f"Scenario: {scenario['description']}")
        
        perceived = {
            'intent': scenario['intent'],
            'entities': scenario['entities'],
            'text': scenario['description']
        }
        
        # Reasoning
        reasoning = agent.reasoning.reason(perceived, {})
        plan = reasoning['plan'][0]
        print(f"  Plan: Use '{plan['tool']}' with {plan['params']}")
        
        # Execution
        actions = agent.action.execute(reasoning['plan'])
        result = actions[0]
        
        if result['success']:
            print(f"  Result: {result['result']}")
        else:
            print(f"  Error: {result['error']}")
        print()


def demo_performance():
    """Demonstrate performance with multiple operations."""
    print_section("7. PERFORMANCE TEST")
    
    agent = AgentWithTools()
    
    import time
    
    # Test 100 calculator operations
    start = time.time()
    for i in range(100):
        agent.executor.execute('calculator', {
            'operation': 'multiply',
            'a': i,
            'b': 2
        })
    calc_time = time.time() - start
    
    print(f"✓ 100 calculator operations: {calc_time:.4f}s ({calc_time*10:.2f}ms avg)")
    
    # Test 50 search operations
    start = time.time()
    for i in range(50):
        agent.executor.execute('search', {'query': 'test'})
    search_time = time.time() - start
    
    print(f"✓ 50 search operations: {search_time:.4f}s ({search_time*20:.2f}ms avg)")
    
    # Test 50 time operations
    start = time.time()
    for i in range(50):
        agent.executor.execute('get_time', {'format': 'iso'})
    time_time = time.time() - start
    
    print(f"✓ 50 time operations: {time_time:.4f}s ({time_time*20:.2f}ms avg)")


def main():
    """Run all demonstrations."""
    print("\n" + "="*70)
    print("  AGENT WITH TOOLS - COMPREHENSIVE DEMONSTRATION")
    print("="*70)
    
    demo_tool_discovery()
    demo_calculator_operations()
    demo_search_operations()
    demo_time_operations()
    demo_error_handling()
    demo_agent_reasoning()
    demo_performance()
    
    print("\n" + "="*70)
    print("  DEMONSTRATION COMPLETE")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
