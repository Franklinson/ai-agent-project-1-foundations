# AI Agent Test Suite Documentation

## Overview

This comprehensive test suite evaluates the AI agent's performance across five critical areas:
- **Perception Accuracy**: How well the agent understands and processes input
- **Reasoning Quality**: The agent's ability to analyze and plan appropriate actions
- **Tool Usage**: Effectiveness of tool selection and execution
- **Observation Accuracy**: Quality of result evaluation and decision making
- **Complete Loop Operation**: End-to-end system functionality

## Test Categories

### 1. Common Use Cases (`common_use_cases`)
Tests typical user interactions that the agent should handle reliably:

- **Simple Question** (`common_001`): Basic information requests
- **Calculation Request** (`common_002`): Mathematical operations
- **Time Query** (`common_003`): Time-related requests
- **Search Request** (`common_004`): Information search tasks
- **Greeting** (`common_005`): Social interaction handling

### 2. Edge Cases (`edge_cases`)
Tests boundary conditions and unusual inputs:

- **Empty Input** (`edge_001`): Handling of empty or null input
- **Very Long Input** (`edge_002`): Processing complex, multi-part requests
- **Special Characters** (`edge_003`): Non-alphanumeric character handling
- **Mixed Language** (`edge_004`): Multi-language input processing
- **Multiple Entities** (`edge_005`): Complex entity extraction scenarios

### 3. Error Scenarios (`error_scenarios`)
Tests error handling and recovery mechanisms:

- **Invalid Calculation** (`error_001`): Mathematical error handling (division by zero)
- **Malformed Request** (`error_002`): Ambiguous or impossible requests
- **Tool Failure Simulation** (`error_003`): Tool unavailability or failure

### 4. Different Input Types (`different_input_types`)
Tests various data format handling:

- **Numeric Input** (`type_001`): Pure numerical input
- **URL Input** (`type_002`): Web address processing
- **Email Input** (`type_003`): Email address recognition
- **Date Input** (`type_004`): Date format parsing
- **Command Style** (`type_005`): SQL/command-like input

## Test Components

### Perception Testing
Evaluates the agent's ability to:
- Extract correct intent from user input
- Identify and classify entities (emails, numbers, dates)
- Normalize and preprocess text appropriately

**Success Criteria:**
- Intent classification accuracy > 80%
- Entity extraction precision > 75%
- Proper handling of edge cases

### Reasoning Testing
Assesses the agent's planning and analysis capabilities:
- Generate appropriate action plans
- Select correct tools for given intents
- Handle complex multi-step scenarios

**Success Criteria:**
- Plan generation success rate > 85%
- Tool selection accuracy > 80%
- Logical action sequencing

### Tool Usage Testing
Verifies tool integration and execution:
- Successful tool invocation
- Proper parameter passing
- Error handling for tool failures

**Success Criteria:**
- Tool execution success rate > 90%
- Appropriate fallback mechanisms
- Error recovery capabilities

### Observation Testing
Tests result evaluation and decision making:
- Accurate success/failure assessment
- Appropriate continuation decisions
- Quality reflection mechanisms

**Success Criteria:**
- Decision accuracy > 85%
- Proper termination conditions
- Meaningful progress tracking

### Complete Loop Testing
Validates end-to-end system operation:
- Full perception-reasoning-action-observation cycle
- Proper iteration management
- Termination condition handling

**Success Criteria:**
- Loop completion rate > 90%
- Reasonable iteration counts (1-5)
- Valid termination reasons

## Expected Outcomes

### Test Case Expectations

Each test case defines:
- `expected_intent`: The intent the perception module should identify
- `expected_tools`: Tools that should be selected for execution
- `expected_outcome`: Final decision the observation module should make

### Outcome Types
- **complete**: Task successfully finished
- **continue**: More iterations needed
- **error**: Unrecoverable error occurred

## Scoring System

### Individual Component Scores
- **Perception Accuracy**: Percentage of correct intent/entity extractions
- **Reasoning Quality**: Percentage of appropriate plans generated
- **Tool Usage Score**: Percentage of successful tool executions
- **Observation Accuracy**: Percentage of correct decisions made
- **Operation Score**: Percentage of successful complete loops

### Overall Grading
- **A (90-100%)**: Excellent performance across all components
- **B (80-89%)**: Good performance with minor issues
- **C (70-79%)**: Acceptable performance with some concerns
- **D (60-69%)**: Poor performance requiring attention
- **F (<60%)**: Failing performance requiring major fixes

## Running the Tests

### Prerequisites
```bash
# Ensure all dependencies are installed
pip install -r ../requirements.txt

# Verify agent modules are accessible
python -c "import sys; sys.path.append('../day_29'); from complete_agent import CompleteAgent"
```

### Execution
```bash
# Run from day_30 directory
cd day_30
python test_suite/test_scenarios.py

# Or run individual components
python -c "
from test_suite.test_scenarios import TestScenarios
runner = TestScenarios()
results = runner.run_all_tests()
runner.print_summary(results)
"
```

### Output Files
- `test_results.json`: Detailed test results with all component scores
- Console output: Summary with overall grade and category breakdowns

## Interpreting Results

### Success Indicators
- Overall score > 80%
- No category scoring below 70%
- Minimal error scenarios in details
- Reasonable iteration counts (1-3 average)

### Warning Signs
- Perception accuracy < 75%
- Tool usage score < 85%
- High error rates in common use cases
- Excessive iterations (>5 average)

### Failure Indicators
- Overall score < 60%
- Multiple categories below 50%
- System crashes or exceptions
- Complete inability to handle basic cases

## Maintenance and Updates

### Adding New Test Cases
1. Add cases to appropriate category in `test_cases.json`
2. Include all required fields: `id`, `name`, `input`, `expected_intent`, `expected_tools`, `expected_outcome`
3. Run tests to verify new cases work correctly

### Modifying Expectations
- Update expected values based on agent improvements
- Adjust scoring thresholds as system matures
- Add new test categories for new capabilities

### Performance Benchmarking
- Run tests regularly during development
- Track score trends over time
- Use results to guide optimization efforts

## Troubleshooting

### Common Issues
1. **Import Errors**: Verify all module paths are correct
2. **Missing Test Files**: Ensure `test_cases.json` exists in test_suite directory
3. **Agent Failures**: Check that base agent modules are functional
4. **Path Issues**: Run from correct directory (day_30)

### Debug Mode
Enable detailed logging by modifying test scenarios:
```python
# Add debug prints in test methods
print(f"Testing case {case['id']}: {case['input']}")
print(f"Result: {result}")
```

This test suite provides comprehensive coverage of the AI agent's capabilities and serves as both a validation tool and a benchmark for ongoing development.