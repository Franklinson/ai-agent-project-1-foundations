from execution_system import ExecutionSystem


def sample_calculator(operation, a, b):
    """Sample calculator tool."""
    if operation == 'add':
        return a + b
    elif operation == 'multiply':
        return a * b
    raise ValueError(f'Unknown operation: {operation}')


def sample_search(query):
    """Sample search tool."""
    return f'Search results for: {query}'


def main():
    # Initialize system
    system = ExecutionSystem()
    
    # Register tools
    system.tool_registry.register({
        'name': 'calculator',
        'function': sample_calculator,
        'required_parameters': ['operation', 'a', 'b']
    })
    
    system.tool_registry.register({
        'name': 'search',
        'function': sample_search,
        'required_parameters': ['query']
    })
    
    # Create action plan
    actions = [
        {
            'tool': 'calculator',
            'parameters': {'operation': 'add', 'a': 5, 'b': 3}
        },
        {
            'tool': 'calculator',
            'parameters': {'operation': 'multiply', 'a': 4, 'b': 7}
        },
        {
            'tool': 'search',
            'parameters': {'query': 'AI agents'}
        },
        {
            'tool': 'calculator',
            'parameters': {'operation': 'add', 'a': 10}  # Missing parameter
        }
    ]
    
    # Execute action plan
    print('Executing action plan...\n')
    results = system.execute_action_plan(actions)
    
    # Display results
    print(f"Total actions: {results['total_actions']}")
    print(f"Successful: {results['successful']}")
    print(f"Failed: {results['failed']}\n")
    
    for i, result in enumerate(results['results'], 1):
        print(f"Action {i}:")
        print(f"  Valid: {result['valid']}")
        print(f"  Success: {result.get('success', 'N/A')}")
        print(f"  Observation: {result['observation']}\n")


if __name__ == '__main__':
    main()
