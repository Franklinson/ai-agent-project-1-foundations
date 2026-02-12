# API Documentation

## Overview

The Refined AI Agent provides a simple yet powerful API for processing user inputs and executing autonomous agent loops.

---

## RefinedAgent Class

### Constructor

```python
agent = RefinedAgent()
```

**Description**: Creates a new instance of the refined agent with all modules initialized.

**Parameters**: None

**Returns**: RefinedAgent instance

**Example**:
```python
from refined_agent import RefinedAgent

agent = RefinedAgent()
```

---

### run() Method

```python
result = agent.run(
    user_input: str,
    goal: str = None,
    max_iterations: int = 5
) -> Dict[str, Any]
```

**Description**: Executes the agent loop to process user input and achieve the specified goal.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `user_input` | str | Yes | - | The user's input text to process |
| `goal` | str | No | `"Process: {user_input}"` | The goal to achieve |
| `max_iterations` | int | No | 5 | Maximum number of loop iterations |

**Returns**: Dictionary with the following structure:

```python
{
    'status': str,              # 'success' or 'error'
    'iterations': int,          # Number of iterations executed
    'final_decision': str,      # 'complete', 'continue', or 'error'
    'termination_reason': str,  # Why the loop terminated
    'progress': List[Dict],     # Progress per iteration
    'errors': List[Dict],       # Any errors encountered
    'history': List[Dict]       # Complete execution history
}
```

**Example**:
```python
result = agent.run("Calculate 15 + 25")

print(f"Status: {result['status']}")
print(f"Iterations: {result['iterations']}")
print(f"Decision: {result['final_decision']}")
```

**Return Value Details**:

- **status**: Overall execution status
  - `'success'`: Loop completed successfully
  - `'error'`: Unrecoverable error occurred

- **iterations**: Number of perception-reasoning-action-observation cycles executed

- **final_decision**: Final observation decision
  - `'complete'`: Goal achieved
  - `'continue'`: More iterations needed (max reached)
  - `'error'`: Error termination

- **termination_reason**: Why the loop stopped
  - `'goal_achieved'`: Successfully completed
  - `'max_iterations_reached'`: Hit iteration limit
  - `'error_termination'`: Error detected
  - `'loop_error'`: Exception in loop

- **progress**: List of progress metrics per iteration
  ```python
  [
      {
          'iteration': 1,
          'success_rate': 1.0,
          'decision': 'complete'
      }
  ]
  ```

- **errors**: List of errors encountered
  ```python
  [
      {
          'phase': 'perception',
          'error': 'Error message'
      }
  ]
  ```

- **history**: Complete execution history
  ```python
  [
      {
          'iteration': 1,
          'perceived': {...},
          'reasoning': {...},
          'actions': [...],
          'observation': {...},
          'errors': [...]
      }
  ]
  ```

---

### get_improvements_summary() Method

```python
summary = agent.get_improvements_summary() -> str
```

**Description**: Returns a summary of improvements implemented in the refined agent.

**Parameters**: None

**Returns**: String containing improvement summary

**Example**:
```python
print(agent.get_improvements_summary())
```

---

## RefinedPerceptionModule Class

### Constructor

```python
perception = RefinedPerceptionModule()
```

**Description**: Creates a perception module instance.

**Parameters**: None

**Returns**: RefinedPerceptionModule instance

---

### process() Method

```python
result = perception.process(user_input: str) -> Dict[str, Any]
```

**Description**: Processes user input to extract intent and entities.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_input` | str | Yes | The user's input text |

**Returns**: Dictionary with perception results:

```python
{
    'text': str,           # Normalized text (lowercase, trimmed)
    'original_text': str,  # Original input text
    'intent': str,         # Detected intent
    'entities': List[Dict] # Extracted entities
}
```

**Intent Values**:
- `'greeting'`: Social interactions
- `'command'`: Action directives
- `'request'`: Information/action requests
- `'question'`: Information queries
- `'unknown'`: Unclassified

**Entity Structure**:
```python
{
    'type': str,   # 'email', 'number', 'date', 'time'
    'value': str   # Extracted value
}
```

**Example**:
```python
from refined_agent import RefinedPerceptionModule

perception = RefinedPerceptionModule()
result = perception.process("Calculate 15 + 25")

print(f"Intent: {result['intent']}")  # 'request'
print(f"Entities: {result['entities']}")  # [{'type': 'number', 'value': '15'}, ...]
```

---

## RefinedReasoningModule Class

### Constructor

```python
reasoning = RefinedReasoningModule()
```

**Description**: Creates a reasoning module instance.

**Parameters**: None

**Returns**: RefinedReasoningModule instance

---

### reason() Method

```python
result = reasoning.reason(
    processed_input: Dict[str, Any],
    context: Dict[str, Any] = None
) -> Dict[str, Any]
```

**Description**: Analyzes processed input and creates action plan.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `processed_input` | Dict | Yes | - | Output from perception module |
| `context` | Dict | No | {} | Additional context |

**Returns**: Dictionary with reasoning results:

```python
{
    'analysis': Dict,  # Analysis of input
    'plan': List[Dict] # Action plan
}
```

**Analysis Structure**:
```python
{
    'intent': str,
    'entity_count': int,
    'has_entities': bool,
    'complexity': str,  # 'high' or 'low'
    'text': str
}
```

**Plan Structure**:
```python
[
    {
        'action': str,      # 'execute', 'process_entities'
        'tool': str,        # Tool name
        'priority': int     # Execution priority
    }
]
```

**Example**:
```python
from refined_agent import RefinedReasoningModule, RefinedPerceptionModule

perception = RefinedPerceptionModule()
reasoning = RefinedReasoningModule()

perceived = perception.process("Calculate 15 + 25")
result = reasoning.reason(perceived)

print(f"Tool: {result['plan'][0]['tool']}")  # 'calculator'
```

---

## RefinedObservationModule Class

### Constructor

```python
observation = RefinedObservationModule()
```

**Description**: Creates an observation module instance.

**Parameters**: None

**Returns**: RefinedObservationModule instance

---

### observe() Method

```python
result = observation.observe(
    results: List[Dict[str, Any]],
    goal: str
) -> Dict[str, Any]
```

**Description**: Evaluates action results and makes continuation decision.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `results` | List[Dict] | Yes | Action execution results |
| `goal` | str | Yes | Goal to achieve |

**Returns**: Dictionary with observation results:

```python
{
    'evaluation': Dict,   # Result evaluation
    'reflection': Dict,   # Quality reflection
    'decision': str       # Continuation decision
}
```

**Evaluation Structure**:
```python
{
    'total_actions': int,
    'successful': int,
    'failed': int,
    'success_rate': float
}
```

**Reflection Structure**:
```python
{
    'all_successful': bool,
    'has_errors': bool,
    'error_messages': List[str],
    'quality': str  # 'high' or 'low'
}
```

**Decision Values**:
- `'complete'`: Goal achieved
- `'continue'`: More iterations needed
- `'error'`: Error detected

**Example**:
```python
from refined_agent import RefinedObservationModule

observation = RefinedObservationModule()

action_results = [
    {'action': 'execute', 'tool': 'calculator', 'status': 'success', 'result': '40'}
]

result = observation.observe(action_results, "Calculate 15 + 25")

print(f"Decision: {result['decision']}")  # 'complete'
print(f"Success Rate: {result['evaluation']['success_rate']}")  # 1.0
```

---

## Usage Examples

### Basic Usage

```python
from refined_agent import RefinedAgent

# Create agent
agent = RefinedAgent()

# Process input
result = agent.run("What time is it?")

# Check result
if result['status'] == 'success':
    print(f"Completed in {result['iterations']} iterations")
    print(f"Decision: {result['final_decision']}")
else:
    print(f"Error: {result.get('error')}")
```

### With Custom Goal

```python
agent = RefinedAgent()

result = agent.run(
    user_input="Calculate the sum of 15 and 25",
    goal="Perform mathematical calculation",
    max_iterations=3
)

print(f"Status: {result['status']}")
print(f"Termination: {result['termination_reason']}")
```

### Accessing History

```python
agent = RefinedAgent()
result = agent.run("Search for Python tutorials")

# Access execution history
for entry in result['history']:
    print(f"Iteration {entry['iteration']}:")
    print(f"  Intent: {entry['perceived']['intent']}")
    print(f"  Tool: {entry['reasoning']['plan'][0]['tool']}")
    print(f"  Decision: {entry['observation']['decision']}")
```

### Error Handling

```python
agent = RefinedAgent()

try:
    result = agent.run("Calculate 10 / 0")
    
    if result['status'] == 'error':
        print("Agent encountered an error")
        for error in result['errors']:
            print(f"  Phase: {error['phase']}")
            print(f"  Error: {error['error']}")
    elif result['final_decision'] == 'error':
        print("Error detected in results")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Progress Monitoring

```python
agent = RefinedAgent()
result = agent.run("Complex multi-step task", max_iterations=5)

# Monitor progress
for progress in result['progress']:
    print(f"Iteration {progress['iteration']}:")
    print(f"  Success Rate: {progress['success_rate']:.1%}")
    print(f"  Decision: {progress['decision']}")
```

### Module-Level Usage

```python
from refined_agent import (
    RefinedPerceptionModule,
    RefinedReasoningModule,
    RefinedObservationModule
)

# Create modules
perception = RefinedPerceptionModule()
reasoning = RefinedReasoningModule()
observation = RefinedObservationModule()

# Process input
user_input = "Calculate 15 + 25"

# Step 1: Perception
perceived = perception.process(user_input)
print(f"Intent: {perceived['intent']}")

# Step 2: Reasoning
reasoning_result = reasoning.reason(perceived)
print(f"Tool: {reasoning_result['plan'][0]['tool']}")

# Step 3: Action (simplified)
action_results = [
    {'action': 'execute', 'tool': 'calculator', 'status': 'success', 'result': '40'}
]

# Step 4: Observation
obs_result = observation.observe(action_results, user_input)
print(f"Decision: {obs_result['decision']}")
```

---

## Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| `loop_error` | Exception in main loop | Check input format and parameters |
| `perception_error` | Perception module failed | Validate input text |
| `reasoning_error` | Reasoning module failed | Check perception output |
| `action_error` | Action execution failed | Verify tool availability |
| `observation_error` | Observation module failed | Check action results format |

---

## Best Practices

### 1. Input Validation
```python
if not user_input or not user_input.strip():
    print("Error: Empty input")
else:
    result = agent.run(user_input)
```

### 2. Iteration Limits
```python
# For simple tasks
result = agent.run(input, max_iterations=3)

# For complex tasks
result = agent.run(input, max_iterations=10)
```

### 3. Error Handling
```python
result = agent.run(input)

if result['status'] == 'error':
    # Handle error
    log_error(result)
elif result['final_decision'] == 'error':
    # Handle error decision
    retry_with_different_input()
```

### 4. Performance Monitoring
```python
import time

start = time.time()
result = agent.run(input)
duration = time.time() - start

print(f"Processed in {duration:.2f}s")
print(f"Iterations: {result['iterations']}")
```

---

## Conclusion

The Refined AI Agent API provides a simple, intuitive interface for autonomous agent operations while maintaining flexibility and extensibility for advanced use cases.