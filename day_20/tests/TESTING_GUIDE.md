# Testing Quick Reference

## Run All Tests
```bash
cd day_20
python3 -m unittest tests.test_reasoning -v
```

## Run Specific Test Classes

### Reasoner Tests Only
```bash
python3 -m unittest tests.test_reasoning.TestReasoner -v
```

### Planner Tests Only
```bash
python3 -m unittest tests.test_reasoning.TestPlanner -v
```

### Decision Maker Tests Only
```bash
python3 -m unittest tests.test_reasoning.TestDecisionMaker -v
```

### Integration Tests Only
```bash
python3 -m unittest tests.test_reasoning.TestReasoningSystem -v
```

### Edge Case Tests Only
```bash
python3 -m unittest tests.test_reasoning.TestEdgeCases -v
```

## Run Individual Tests

```bash
# Example: Run single test
python3 -m unittest tests.test_reasoning.TestReasoner.test_query_intent -v
```

## Test Output

### Success
```
Ran 35 tests in 0.001s
OK
```

### Failure Example
```
FAILED (failures=1)
```

## What Each Test Class Covers

### TestReasoner (6 tests)
- Intent classification (query, command, greeting, unknown)
- Confidence scoring
- Action mapping

### TestPlanner (8 tests)
- Goal decomposition
- Step ordering by dependencies
- Context propagation
- Plan serialization

### TestDecisionMaker (8 tests)
- Tool selection for different intents
- Parameter building
- Multiple candidate handling
- Entity-based selection

### TestReasoningSystem (8 tests)
- Full pipeline integration
- All intent types end-to-end
- Action plan structure
- Error handling

### TestEdgeCases (5 tests)
- Empty/missing data
- None values
- Large inputs
- Boundary conditions

## Quick Validation

Run the simple validation script:
```bash
python3 test_reasoning_system.py
```

## CI/CD Integration

Add to your CI pipeline:
```yaml
- name: Run Day 20 Tests
  run: |
    cd day_20
    python3 -m unittest tests.test_reasoning
```

## Test Statistics

- **Total Tests**: 35
- **Execution Time**: < 1ms
- **Success Rate**: 100%
- **Code Coverage**: All major paths
