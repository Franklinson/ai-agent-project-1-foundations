# Quick Start Guide - Complete Agent Loop

## Installation

No additional dependencies required beyond Day 27 and Day 28 modules.

## Basic Usage

```python
from complete_agent import CompleteAgent

# Create agent
agent = CompleteAgent()

# Run agent
result = agent.run(
    user_input="Your input here",
    goal="Your goal here",
    max_iterations=5
)

# Print summary
print(agent.get_summary(result))
```

## Examples

### Example 1: Simple Question
```python
agent = CompleteAgent()
result = agent.run("What is 2 + 2?", "Answer question")
print(f"Status: {result['status']}")
print(f"Iterations: {result['iterations']}")
```

### Example 2: With Error Handling
```python
agent = CompleteAgent()
result = agent.run("Complex task", "Complete task", max_iterations=10)

if result['status'] == 'error':
    print(f"Error: {result['error']}")
elif result['errors']:
    print(f"Recovered from {len(result['errors'])} errors")
```

### Example 3: Accessing History
```python
agent = CompleteAgent()
result = agent.run("Multi-step task", "Complete")

for i, entry in enumerate(result['history'], 1):
    print(f"Iteration {i}:")
    print(f"  Intent: {entry['perceived']['intent']}")
    print(f"  Decision: {entry['observation']['decision']}")
```

### Example 4: Using Tools
```python
agent = CompleteAgent()

# List available tools
result = agent.run("Test", "Test")
for tool in result['available_tools']:
    print(f"{tool['name']}: {tool['description']}")

# Execute tool directly
calc_result = agent.tool_executor.execute('calculator', {'expression': '10*5'})
print(calc_result['result'])
```

## Result Structure

```python
{
    'status': 'success' | 'error',
    'iterations': int,                    # Number of iterations executed
    'final_decision': str,                # Last observation decision
    'termination_reason': str,            # Why loop terminated
    'progress': [                         # Progress per iteration
        {
            'iteration': int,
            'success_rate': float,
            'decision': str
        }
    ],
    'errors': [                           # Errors encountered
        {
            'phase': str,
            'error': str
        }
    ],
    'history': [                          # Complete execution history
        {
            'iteration': int,
            'perceived': dict,
            'reasoning': dict,
            'actions': list,
            'observation': dict,
            'errors': list
        }
    ],
    'available_tools': list               # Registered tools
}
```

## Termination Reasons

- `'goal_achieved'` - Task completed successfully
- `'max_iterations_reached'` - Hit iteration limit
- `'error_termination'` - Critical error in observation
- `'loop_error'` - Unhandled exception

## Running Tests

```bash
# Test phase coordination
python3 test_coordination.py

# Test iteration management
python3 test_iteration_management.py

# Test error handling
python3 test_error_handling.py

# Test complete system
python3 test_complete_system.py

# Run demonstrations
python3 demo.py
```

## Adding Custom Tools

```python
agent = CompleteAgent()

# Define tool function
def my_tool(param1: str, param2: int) -> dict:
    return {"success": True, "result": f"{param1} x {param2}"}

# Register tool
agent.tool_registry.register(my_tool, "my_tool", "My custom tool")

# Use tool
result = agent.tool_executor.execute('my_tool', {'param1': 'test', 'param2': 5})
```

## Configuration

```python
# Adjust max iterations
result = agent.run(input, goal, max_iterations=10)

# Custom goal
result = agent.run(input, goal="Custom goal description")

# No goal (auto-generated)
result = agent.run(input)  # Goal: "Process: {input}"
```

## Error Handling

The agent handles errors at multiple levels:

1. **Phase Errors**: Caught and recovered automatically
2. **Loop Errors**: Caught and returned with partial results
3. **Tool Errors**: Handled by tool executor

All errors are logged in `result['errors']` for inspection.

## Best Practices

1. **Set appropriate max_iterations** - Default is 5, adjust based on task complexity
2. **Check result status** - Always verify `result['status']` before using results
3. **Review errors** - Check `result['errors']` for any issues
4. **Use clear goals** - Specific goals help with termination decisions
5. **Monitor progress** - Use `result['progress']` to track execution

## Troubleshooting

**Agent doesn't terminate:**
- Check max_iterations setting
- Review observation decisions in history
- Verify termination conditions

**Errors not being caught:**
- Check error list in result
- Review ERROR_HANDLING.md for details
- Verify phase error handlers

**Tools not working:**
- Verify tool is registered: `agent.tool_registry.list_all()`
- Check tool parameters match signature
- Review tool executor result for errors

## Documentation

- `README.md` - Complete documentation
- `COMPLETION_SUMMARY.md` - Project summary
- `COORDINATION_VERIFICATION.md` - Phase coordination details
- `ITERATION_MANAGEMENT.md` - Iteration and termination details
- `ERROR_HANDLING.md` - Error handling details
