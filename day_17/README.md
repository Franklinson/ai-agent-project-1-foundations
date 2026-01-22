# Day 17: Tool Integration for AI Agents

## Overview
Implementation of reusable tools for AI agents with proper error handling, input validation, and OpenAI function calling schemas.

## Project Structure
```
day_17/
├── tools/
│   ├── calculator_tool.py    # Mathematical operations tool
│   ├── text_tool.py          # Text analysis tool
│   └── schemas.py            # OpenAI function calling schemas
├── tests/
│   ├── test_calculator_tool.py
│   └── test_text_tool.py
└── agent_with_tools.py       # Tool usage demonstration
```

## Tools Implemented

### CalculatorTool
- **Operations**: add, subtract, multiply, divide
- **Features**: Input validation, division by zero handling
- **Returns**: Consistent dict format with success/error status

### TextTool
- **word_count**: Count total words in text
- **word_search**: Count word occurrences (case-insensitive)
- **Features**: Input validation, empty string handling

## Usage

### Run Demonstration
```bash
python3 agent_with_tools.py
```

### Run Tests
```bash
python3 day_17/tests/test_calculator_tool.py
python3 day_17/tests/test_text_tool.py
```

## Example Usage

```python
from tools.calculator_tool import CalculatorTool
from tools.text_tool import TextTool

# Calculator
calc = CalculatorTool()
result = calc.calculate("add", 10, 5)
# {'success': True, 'operation': 'add', 'a': 10.0, 'b': 5.0, 'result': 15.0}

# Text Tool
text = TextTool()
result = text.word_count("Hello world")
# {'success': True, 'operation': 'word_count', 'count': 2}

result = text.word_search("hello world hello", "hello")
# {'success': True, 'operation': 'word_search', 'word': 'hello', 'count': 2}
```

## OpenAI Function Schemas
Schemas in `tools/schemas.py` follow OpenAI function calling format for LLM integration.

## Key Features
- ✓ Input validation
- ✓ Error handling
- ✓ Consistent response format
- ✓ Comprehensive test coverage
- ✓ OpenAI-compatible schemas
