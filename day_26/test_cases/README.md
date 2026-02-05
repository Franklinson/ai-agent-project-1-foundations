# Test Suite Documentation

## Overview

Comprehensive test suite for evaluating agent prompts across multiple scenarios including common use cases, edge cases, and error handling.

## Test Suite Structure

```json
{
  "id": "unique_test_id",
  "category": "test_category",
  "scenario": "common|edge_case|error",
  "input": "test input text",
  "expected": {
    "contains": "expected text in response",
    "tool": "expected_tool_name",
    "exact_match": "exact expected value",
    "min_length": 10,
    "max_length": 100,
    "min_words": 5,
    "max_words": 50,
    "count": 5,
    "format": "json|list|text",
    "error_handling": true,
    "context_aware": true,
    "max_response_time": 5
  },
  "description": "Test case description"
}
```

## Test Categories

### 1. Search (search)
- Basic search queries
- Information retrieval
- Documentation lookup

### 2. Calculator (calculator)
- Basic arithmetic operations
- Complex calculations
- Edge cases (division by zero, large numbers)

### 3. API (api)
- Data retrieval
- API calls with various parameters
- Error handling for invalid requests

### 4. Multi-Step (multi_step)
- Tasks requiring multiple tools
- Sequential operations
- Complex reasoning

### 5. Text Generation (text_generation)
- Explanations
- Lists
- Formatted output

### 6. Edge Cases (edge_case)
- Empty input
- Single character input
- Ambiguous requests
- Unusual formatting

### 7. Error Handling (error_handling)
- Invalid input
- Special characters
- Malformed requests

### 8. Complex (complex)
- Multi-step reasoning
- Combined operations
- Context-dependent tasks

### 9. Context (context)
- Context awareness
- Follow-up questions
- Reference to previous interactions

### 10. Formatting (formatting)
- JSON output
- Structured data
- Specific format requirements

### 11. Performance (performance)
- Large calculations
- Response time requirements
- Resource-intensive operations

## Scenario Types

- **common**: Standard use cases that should work reliably
- **edge_case**: Boundary conditions and unusual inputs
- **error**: Cases that should trigger error handling

## Expected Result Fields

### Text Validation
- `contains`: Response must contain this text (case-insensitive)
- `exact_match`: Response must exactly match this value
- `min_length`: Minimum character count
- `max_length`: Maximum character count
- `min_words`: Minimum word count
- `max_words`: Maximum word count

### Tool Validation
- `tool`: Expected tool to be used (single tool)
- `tools`: Expected tools to be used (multiple tools)

### Format Validation
- `format`: Expected output format (json, list, text)
- `count`: Expected number of items in list

### Behavior Validation
- `error_handling`: Should handle error gracefully
- `context_aware`: Should reference previous context
- `max_response_time`: Maximum seconds for response

## Usage Example

```python
from prompt_tester import PromptTester
import json

# Load test suite
with open('test_cases/test_suite.json', 'r') as f:
    suite = json.load(f)

# Extract test cases
test_cases = suite['test_cases']

# Run tests
tester = PromptTester()
results = tester.run_tests(prompt, test_cases, evaluator)
```

## Test Coverage

- **Total Tests**: 20
- **Common Scenarios**: 11 (55%)
- **Edge Cases**: 6 (30%)
- **Error Scenarios**: 3 (15%)

### By Category
- Search: 2 tests
- Calculator: 4 tests
- API: 2 tests
- Multi-step: 1 test
- Text Generation: 2 tests
- Edge Cases: 3 tests
- Error Handling: 2 tests
- Complex: 1 test
- Context: 1 test
- Formatting: 1 test
- Performance: 1 test

## Adding New Test Cases

1. Choose appropriate category
2. Define scenario type (common/edge_case/error)
3. Create unique ID following pattern: `{category}_{number}`
4. Specify clear input
5. Define expected results with appropriate validation fields
6. Add descriptive text

## Best Practices

- Keep inputs clear and specific
- Use multiple validation criteria when appropriate
- Include edge cases for each category
- Test error handling explicitly
- Document expected behavior in description
- Use realistic test data
