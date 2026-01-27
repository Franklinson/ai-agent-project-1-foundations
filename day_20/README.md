# Day 20: Reasoning System

## Overview

An integrated reasoning system that combines reasoning, planning, and decision-making to process user inputs and generate actionable plans.

## Components

### 1. Reasoner (`reasoner.py`)
Analyzes processed input and identifies goals and actions.

**Features:**
- Intent-to-goal mapping
- Action identification
- Confidence scoring
- Handles 3+ intent types: query, command, greeting

**Usage:**
```python
from reasoner import Reasoner

reasoner = Reasoner()
result = reasoner.reason({
    'intent': 'query',
    'entities': {'keywords': ['weather']},
    'text': 'What is the weather?'
})
```

### 2. Planner (`planner.py`)
Decomposes goals into actionable steps with dependency ordering.

**Features:**
- Goal decomposition into sub-goals
- Dependency tracking
- Step ordering (topological sort)
- Structured Plan objects

**Usage:**
```python
from planner import Planner

planner = Planner()
plan = planner.decompose_goal('retrieve_information')
print(plan.to_dict())
```

### 3. Decision Maker (`decision_maker.py`)
Selects appropriate tools for actions based on intent and entities.

**Features:**
- Tool registry with 5+ tools
- Intent and entity matching
- Parameter building
- Handles multiple tool candidates

**Usage:**
```python
from decision_maker import DecisionMaker

decision_maker = DecisionMaker()
selection = decision_maker.select_tool('query', 'search_knowledge_base', {'keywords': ['test']})
```

### 4. Reasoning System (`reasoning_system.py`)
Integrated system combining all components.

**Features:**
- Full pipeline processing
- Integrates with Day 19 input processor
- End-to-end reasoning flow
- Structured action plans

**Usage:**
```python
from reasoning_system import ReasoningSystem

system = ReasoningSystem()
result = system.process({
    'intent': 'command',
    'entities': {'keywords': ['Create']},
    'text': 'Create a project'
})
```

## Pipeline Flow

```
Input → Reasoner → Planner → Decision Maker → Action Plan
         ↓           ↓            ↓
       Goal      Sub-goals    Tool Selection
```

## Running the Demo

```bash
cd day_20
python3 demo.py
```

The demo tests:
- Query intent: "What is the weather today?"
- Command intent: "Create a new project called MyApp"
- Greeting intent: "Hello there!"

## Output Structure

```json
{
  "success": true,
  "reasoning": "Detected intent: query...",
  "goal": "retrieve_information",
  "confidence": 0.9,
  "plan": {
    "goal": "retrieve_information",
    "sub_goals": ["identify_query", "search_data", "synthesize_results"],
    "steps": [...],
    "total_steps": 3
  },
  "action_plan": [
    {
      "step_id": 1,
      "action": "identify_query",
      "tool": "search_tool",
      "parameters": {"query": "weather"},
      "dependencies": []
    }
  ]
}
```

## Integration with Day 19

The system integrates seamlessly with Day 19's input processor:

```python
from input_processor import InputHandler
from reasoning_system import ReasoningSystem

input_handler = InputHandler()
reasoning_system = ReasoningSystem()

# Process raw input
processed = input_handler.process("What is the weather?", "user_001")

# Generate action plan
result = reasoning_system.process(processed['data'])
```

## Supported Intents

- **query**: Information retrieval requests
- **command**: Action execution requests
- **greeting**: Conversation initiation

## Supported Tools

- `search_tool`: Knowledge base search
- `text_formatter`: Response formatting
- `command_executor`: Command execution
- `validator`: Input validation
- `response_generator`: Response generation

## Testing

### Running Tests

```bash
cd day_20
python3 -m unittest tests.test_reasoning -v
```

### Test Coverage

- **35 total tests** - All passing ✅
- **Reasoner**: 6 tests
- **Planner**: 8 tests
- **Decision Maker**: 8 tests
- **Integration**: 8 tests
- **Edge Cases**: 5 tests

### Test Categories

1. **Unit Tests**: Individual component testing
2. **Integration Tests**: Full pipeline testing
3. **Edge Cases**: Error handling and boundary conditions

See [TEST_SUMMARY.md](TEST_SUMMARY.md) for detailed test documentation.

## Project Structure

```
day_20/
├── reasoner.py              # Reasoning component
├── planner.py               # Planning component
├── decision_maker.py        # Decision-making component
├── reasoning_system.py      # Integrated system
├── demo.py                  # Demonstration script
├── test_reasoning_system.py # Quick validation tests
├── tests/
│   ├── __init__.py
│   └── test_reasoning.py    # Comprehensive unit tests
├── README.md                # This file
└── TEST_SUMMARY.md          # Detailed test documentation
```
