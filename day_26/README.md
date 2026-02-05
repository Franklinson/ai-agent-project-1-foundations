# Day 26: Prompt Testing Framework

A minimal framework for evaluating agent prompts with test cases, metrics calculation, A/B testing, and automated iteration workflows.

## Features

- Load test cases from JSON files
- Execute tests with custom evaluators
- Collect and track test results
- Calculate evaluation metrics (success rate, quality score, tool accuracy)
- A/B test prompt versions with statistical comparison
- Automated iteration workflow with version tracking
- Generate reports in text and JSON formats

## Usage

### Basic Example

```python
from prompt_tester import PromptTester

# Initialize
tester = PromptTester()

# Load test cases
test_cases = tester.load_test_cases("test_cases.json")

# Define evaluator function
def evaluator(prompt, test_input, expected):
    # Your evaluation logic here
    response = call_llm(prompt, test_input)
    return validate(response, expected)

# Run tests
results = tester.run_tests(prompt, test_cases, evaluator)

# Generate report
report = tester.generate_report(results, "report.txt")
print(report)
```

### Test Case Format

```json
[
  {
    "input": "Test input text",
    "expected": {
      "contains": "expected phrase",
      "max_words": 50
    }
  }
]
```

### Running Example

```bash
cd day_26
python example_usage.py
```

## API Reference

### PromptTester

**load_test_cases(filepath: str) -> List[Dict]**
- Load test cases from JSON file

**run_tests(prompt: str, test_cases: List[Dict], evaluator: Callable) -> Dict**
- Execute tests and return results
- `evaluator`: Function with signature `(prompt, input, expected) -> bool`

**generate_report(results: Dict, output_file: str = None) -> str**
- Generate human-readable report
- Optionally save to file

## Output

- `test_report.txt`: Human-readable test report
- `test_results.json`: Structured test results
- `metrics_report.txt`: Evaluation metrics report
- `metrics_results.json`: Structured metrics data

## Test Suites

Comprehensive test suites are available in the `test_cases/` directory:

### Available Suites

1. **test_suite.json** - Comprehensive suite with 20 tests
   - 11 categories (search, calculator, API, multi-step, etc.)
   - Common scenarios, edge cases, and error handling
   - Full coverage of agent capabilities

2. **basic_suite.json** - Essential 5 tests
   - Core functionality testing
   - Quick validation suite

3. **edge_cases_suite.json** - 10 edge case and error tests
   - Boundary conditions
   - Error handling validation
   - Special input scenarios

### Using Test Suites

```python
from test_suite_loader import TestSuiteLoader

loader = TestSuiteLoader()

# List available suites
suites = loader.list_suites()

# Load specific suite
test_cases = loader.get_test_cases("test_suite")

# Filter by category
search_tests = loader.filter_by_category(test_cases, "search")

# Get suite info
info = loader.get_suite_info("test_suite")
```

See `test_cases/README.md` for detailed test suite documentation.

## Metrics Calculator

### Basic Usage

```python
from metrics_calculator import MetricsCalculator

calculator = MetricsCalculator()

# Calculate individual metrics
success_rate = calculator.calculate_success_rate(results)
quality_score = calculator.calculate_quality_score(results)
tool_accuracy = calculator.calculate_tool_accuracy(results)

# Calculate all metrics at once
metrics = calculator.calculate_all_metrics(results)

# Generate report
report = calculator.generate_metrics_report(metrics, "metrics.txt")
```

### MetricsCalculator API

**calculate_success_rate(results: Dict) -> float**
- Calculate percentage of passed tests

**calculate_quality_score(results: Dict) -> float**
- Calculate quality score with error penalties

**calculate_tool_accuracy(results: Dict) -> Dict[str, float]**
- Calculate accuracy per tool used

**calculate_all_metrics(results: Dict) -> Dict**
- Calculate all metrics and return comprehensive data

**generate_metrics_report(metrics: Dict, output_file: str = None) -> str**
- Generate formatted metrics report

### Running Examples

```bash
# Basic prompt testing
python3 example_usage.py

# Metrics calculation
python3 example_metrics.py

# Integrated testing + metrics
python3 example_integrated.py

# A/B testing prompt versions
python3 example_ab_test.py

# Multi-version comparison
python3 example_multi_version.py

# Automated iteration workflow
python3 example_iteration.py

# Manual iteration workflow
python3 example_manual_iteration.py
```

## Iteration Workflow

### Automated Workflow

```python
from iteration_workflow import IterationWorkflow

workflow = IterationWorkflow()

# Define refiner function
def refiner(prompt, iteration):
    # Analyze iteration results and improve prompt
    if iteration['metrics']['success_rate'] < 80:
        prompt += "\nYou must verify all responses."
    return prompt

# Run automated workflow
summary = workflow.run_workflow(
    initial_prompt="You are an AI assistant.",
    test_cases=test_cases,
    evaluator=evaluator,
    refiner=refiner,
    max_iterations=5,
    target_score=90.0
)

# Generate report
report = workflow.generate_iteration_report("iteration_report.txt")
```

### Manual Iteration

```python
workflow = IterationWorkflow()

# Test multiple versions manually
for version_name, prompt in prompts.items():
    iteration = workflow.run_iteration(
        prompt, test_cases, evaluator, version_name
    )

# Get best version
best = workflow.get_best_version()

# Compare iterations
comparison = workflow.compare_iterations(1, 3)
```

### IterationWorkflow API

**run_iteration(prompt: str, test_cases: List[Dict], evaluator: Callable, version_name: str = None) -> Dict**
- Run single iteration: test, evaluate, analyze
- Returns iteration results with metrics and analysis

**run_workflow(initial_prompt: str, test_cases: List[Dict], evaluator: Callable, refiner: Callable, max_iterations: int = 5, target_score: float = 95.0) -> Dict**
- Run complete automated workflow
- Automatically refines prompt based on results
- Stops when target score reached or max iterations hit

**compare_iterations(iteration_a: int, iteration_b: int) -> Dict**
- Compare two iterations by number
- Returns success rate and quality score changes

**get_best_version() -> Dict**
- Get the best performing version from all iterations

**generate_iteration_report(output_file: str = None) -> str**
- Generate formatted iteration report
- Includes progress tracking and issue analysis

**save_workflow(filepath: str)**
- Save complete workflow history to JSON

### Workflow Features

- **Version Tracking**: Automatic versioning of all prompt iterations
- **Performance Analysis**: Identifies issues and performance levels
- **Automated Refinement**: Refiner function improves prompts based on results
- **Progress Tracking**: Monitor improvement across iterations
- **Best Version Selection**: Automatically identifies top performer

## A/B Testing

### Basic Usage

```python
from ab_testing import ABTester

tester = ABTester()

# Define two prompt versions
version_a = "You are a formal assistant..."
version_b = "You are a casual assistant..."

# Compare versions
comparison = tester.compare_versions(
    version_a, version_b, test_cases, evaluator
)

# Generate report
report = tester.generate_comparison_report(comparison, "ab_report.txt")
print(report)
```

### ABTester API

**run_version(prompt: str, test_cases: List[Dict], evaluator: Callable) -> Dict**
- Run tests for a single prompt version

**compare_versions(version_a: str, version_b: str, test_cases: List[Dict], evaluator: Callable) -> Dict**
- Compare two prompt versions with statistical analysis
- Returns detailed comparison including winner and confidence level

**generate_comparison_report(comparison: Dict, output_file: str = None) -> str**
- Generate formatted A/B test report
- Includes performance metrics, statistical comparison, and tool accuracy

### Comparison Metrics

- **Success Rate Difference**: Change in test pass rate
- **Quality Score Difference**: Change in quality metrics
- **Overall Improvement**: Percentage improvement between versions
- **Winner**: Determined by combined success rate + quality score
- **Confidence**: High (>10% difference), Medium (5-10%), Low (<5%)
- **Tool Accuracy**: Per-tool performance comparison
