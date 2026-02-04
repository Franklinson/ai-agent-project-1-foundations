# Day 25: Chain-of-Thought Prompt Builder

## Overview

Implementation of advanced prompt engineering techniques for AI agents: Chain-of-Thought (CoT) reasoning, Tool Chaining, Multi-Step Planning, Error Recovery, and an Integrated System combining all techniques.

## Files

- `cot_prompt_builder.py`: CoT prompt builder with reasoning templates
- `tool_chaining_prompts.py`: Tool chaining prompt builder for sequential workflows
- `multi_step_prompts.py`: Multi-step planning and goal decomposition
- `error_recovery_prompts.py`: Error handling and recovery strategies
- `advanced_prompt_system.py`: **Unified interface combining all techniques**
- `integrated_prompt_system.py`: Extended integration with complex workflows
- `demo.py`: CoT usage examples and demonstrations
- `demo_chaining.py`: Tool chaining usage examples
- `demo_multi_step.py`: Multi-step planning examples
- `demo_error_recovery.py`: Error recovery examples
- `demo_advanced_system.py`: **Unified system demonstrations**
- `demo_integrated.py`: Extended integration examples

## Quick Start

### Unified Interface (Recommended)

Use `AdvancedPromptSystem` for simple, flexible prompt building:

```python
from advanced_prompt_system import AdvancedPromptSystem

system = AdvancedPromptSystem()

# Single technique
prompt = system.build_prompt(
    task="Calculate compound interest",
    techniques=["cot"]
)

# Multiple techniques
prompt = system.build_prompt(
    task="Process data pipeline",
    techniques=["cot", "chaining", "error_recovery"],
    tools=tools
)

# All techniques
prompt = system.build_all(
    task="Build production system",
    tools=tools,
    context="Mission-critical application"
)
```

### Individual Builders

Use individual builders for fine-grained control:

```python
from cot_prompt_builder import CoTPromptBuilder
from tool_chaining_prompts import ToolChainingPromptBuilder
# ... etc
```

## Features

### 1. CoT Prompt Builder
- Step-by-step reasoning instructions
- Task-specific templates (analysis, problem-solving, decision-making, planning, debugging)
- Tool usage with reasoning
- Few-shot learning support

### 2. Task Types

**Analysis**: Break down and examine information systematically
**Problem Solving**: Identify, evaluate, and solve problems
**Decision Making**: Compare options and make informed choices
**Planning**: Create structured plans with dependencies
**Debugging**: Systematically identify and fix issues

### 3. Reasoning Patterns

- Understand → Plan → Execute → Verify
- Question → Information → Approach → Conclusion
- Problem → Facts → Solutions → Evaluation → Implementation

## Usage

### Basic CoT Prompt

```python
from cot_prompt_builder import CoTPromptBuilder

builder = CoTPromptBuilder()

prompt = builder.build_cot_prompt(
    task="Calculate 15% tip on $45.50",
    task_type="problem_solving"
)
```

### CoT with Tools

```python
tools = [
    {"name": "search", "description": "Search for information"},
    {"name": "calculate", "description": "Perform calculations"}
]

prompt = builder.build_tool_use_cot(
    task="Find population of Tokyo and calculate density",
    tools=tools
)
```

### Few-Shot CoT

```python
examples = [
    {
        "task": "If 20% of 50 is X, what is X?",
        "reasoning": "Step 1: Convert 20% to decimal: 0.20\nStep 2: Multiply: 0.20 × 50 = 10",
        "answer": "X = 10"
    }
]

prompt = builder.build_few_shot_cot(
    task="If 35% of 80 is Y, what is Y?",
    examples=examples
)
```

## Benefits of CoT

1. **Improved Accuracy**: Step-by-step reasoning reduces errors
2. **Transparency**: Shows how conclusions are reached
3. **Complex Tasks**: Handles multi-step problems effectively
4. **Debugging**: Makes it easier to identify reasoning errors
5. **Learning**: Few-shot examples teach reasoning patterns

## When to Use CoT

- Mathematical calculations
- Logical reasoning
- Multi-step planning
- Decision making with trade-offs
- Debugging and troubleshooting
- Tool selection and sequencing
- Complex analysis tasks

## Running the Demo

```bash
cd day_25
python demo.py
```

## Key Concepts

**Chain-of-Thought**: Prompting technique that elicits step-by-step reasoning

**Few-Shot Learning**: Providing examples to teach reasoning patterns

**Zero-Shot CoT**: Simply adding "Let's think step-by-step" to prompts

**Tool-Use CoT**: Reasoning about which tools to use and when

## Examples Included

- Math problem solving
- Logical reasoning
- Tool selection
- Decision making
- Debugging scenarios

## Integration

Use with existing prompt builders:

```python
from cot_prompt_builder import CoTPromptBuilder
from day_23.prompt_builder import PromptBuilder

cot_builder = CoTPromptBuilder()
base_builder = PromptBuilder()

# Combine approaches as needed
```

## Tool Chaining Patterns

### Sequential Chain
Tools execute one after another, each using the previous result:
```
Tool A → Result A → Tool B → Result B → Tool C → Final Answer
```

### Parallel-Merge
Independent tools run simultaneously, results merge:
```
Tool A → Result A \
                   → Merge → Tool C → Final Answer
Tool B → Result B /
```

### Conditional Chain
Tool selection based on intermediate results:
```
Tool A → Result A → Decision
                    ├─ If X: Tool B
                    └─ If Y: Tool C
```

### Iterative Chain
Repeat tool calls until condition met:
```
Tool A → Result → Check
  ↑              ├─ Complete: Done
  └──────────────└─ Incomplete: Retry
```

## Tool Chaining Usage

### Basic Sequential Chain

```python
from tool_chaining_prompts import ToolChainingPromptBuilder

builder = ToolChainingPromptBuilder()

tool_chain = [
    {"name": "search", "description": "Search web", "output": "results"},
    {"name": "summarize", "description": "Summarize content", "output": "summary"}
]

prompt = builder.build_chaining_prompt(
    task="Research AI agents and summarize findings",
    tool_chain=tool_chain,
    pattern="sequential"
)
```

### Parallel-Merge Pattern

```python
parallel_tools = [
    {"name": "get_weather", "description": "Fetch weather"},
    {"name": "get_news", "description": "Fetch news"}
]

merge_tool = {"name": "create_report", "description": "Combine data"}

prompt = builder.build_parallel_merge_chain(
    task="Create morning briefing",
    parallel_tools=parallel_tools,
    merge_tool=merge_tool
)
```

### Conditional Chain

```python
initial_tool = {"name": "check_type", "description": "Detect file type"}

conditional_tools = {
    "CSV file": [{"name": "parse_csv", "description": "Parse CSV"}],
    "JSON file": [{"name": "parse_json", "description": "Parse JSON"}]
}

prompt = builder.build_conditional_chain(
    task="Process file based on type",
    initial_tool=initial_tool,
    conditional_tools=conditional_tools
)
```

## Multi-Step Planning

### Goal Decomposition

Break complex goals into manageable steps:

```python
from multi_step_prompts import MultiStepPromptBuilder

builder = MultiStepPromptBuilder()

prompt = builder.build_goal_decomposition_prompt(
    goal="Launch an e-commerce website",
    constraints=["Budget: $50k", "Timeline: 3 months"],
    resources=["Cloud hosting", "Payment API"]
)
```

### Hierarchical Planning

Organize goals into subgoals and tasks:

```python
subgoals = [
    {
        "name": "Backend Development",
        "tasks": ["Design schema", "Build API", "Add auth"]
    },
    {
        "name": "Frontend Development",
        "tasks": ["Create UI", "Connect API"]
    }
]

prompt = builder.build_hierarchical_plan(
    main_goal="Build web application",
    subgoals=subgoals
)
```

### Adaptive Planning

Adjust plans based on execution results:

```python
prompt = builder.build_adaptive_plan_prompt(
    goal="Optimize performance",
    initial_steps=["Analyze", "Identify bottlenecks", "Optimize"],
    evaluation_criteria=["20% improvement", "No new bugs"]
)
```

### State Tracking

Monitor progress across steps:

```python
steps = [
    {"description": "Fetch data", "status": "completed", "result": "1000 records"},
    {"description": "Process data", "status": "in progress"},
    {"description": "Generate report", "status": "pending"}
]

current_state = {"records_processed": 1000, "errors": 0}

prompt = builder.build_state_tracking_prompt(
    goal="Generate report",
    steps=steps,
    current_state=current_state
)
```

## Planning Types

**Linear**: Sequential steps, each depends on previous
**Hierarchical**: Nested goals with subgoals and tasks
**Adaptive**: Dynamic planning that adjusts based on results

## Error Recovery

### Error-Aware Prompts

Build prompts with error handling:

```python
from error_recovery_prompts import ErrorRecoveryPromptBuilder

builder = ErrorRecoveryPromptBuilder()

tools = [
    {
        "name": "fetch_api",
        "description": "Fetch data from API",
        "errors": ["timeout", "network", "rate_limit"]
    }
]

prompt = builder.build_error_aware_prompt(
    task="Fetch user data",
    tools=tools,
    error_handling="retry"
)
```

### Retry Logic

Handle transient errors with retries:

```python
prompt = builder.build_retry_prompt(
    task="Send email",
    failed_step="send_email()",
    error_message="Connection timeout",
    retry_count=1,
    max_retries=3
)
```

### Fallback Strategies

Provide alternative approaches:

```python
prompt = builder.build_fallback_prompt(
    task="Get weather data",
    failed_approach="Primary API (503 error)",
    alternative_approaches=[
        "Use backup API",
        "Use cached data"
    ]
)
```

### Error Classification

Classify and analyze errors:

```python
prompt = builder.build_error_classification_prompt(
    error_message="Connection refused",
    context="Connecting to database"
)
```

## Error Types

- **Validation**: Invalid or malformed input
- **Network**: Connection failures
- **Timeout**: Operation exceeded time limit
- **Permission**: Insufficient access rights
- **Not Found**: Resource doesn't exist
- **Rate Limit**: Too many requests
- **Server Error**: External service failure
- **Data Error**: Processing failure

## Recovery Strategies

- **Retry**: Wait and retry with exponential backoff
- **Fallback**: Use alternative method or cached data
- **Skip**: Continue with remaining steps
- **Abort**: Stop execution and rollback

## Integrated Prompt System

Combine all techniques for maximum effectiveness:

```python
from integrated_prompt_system import AdvancedPromptSystem

system = AdvancedPromptSystem()

# Comprehensive prompt with all techniques
prompt = system.build_comprehensive_prompt(
    task="Process customer data pipeline",
    tools=tools,
    use_cot=True,
    use_chaining=True,
    use_multi_step=True,
    use_error_recovery=True
)
```

### Complex Workflow

Integrate multiple techniques:

```python
prompt = system.build_complex_workflow_prompt(
    goal="Process data pipeline",
    tool_chain=tool_chain,
    steps=steps,
    error_policies=error_policies
)
```

### Adaptive Agent

Create self-adjusting agents:

```python
prompt = system.build_adaptive_agent_prompt(
    task="Debug and fix issues",
    available_tools=tools,
    constraints=["Don't modify tests"],
    success_criteria=["All tests pass"]
)
```

### Robust Pipeline

Build fault-tolerant pipelines:

```python
prompt = system.build_robust_pipeline_prompt(
    pipeline_name="ETL Pipeline",
    stages=stages,
    rollback_strategy="abort"
)
```

## Benefits of Integration

✓ **Reliability**: Error recovery ensures robustness
✓ **Clarity**: CoT reasoning provides transparency
✓ **Efficiency**: Tool chaining optimizes execution
✓ **Adaptability**: Multi-step planning handles complexity
✓ **Success Rate**: Combined techniques improve outcomes

## Running Demos

```bash
cd day_25

# Unified system (recommended starting point)
python3 demo_advanced_system.py

# Individual techniques
python3 demo.py                  # CoT examples
python3 demo_chaining.py         # Tool chaining examples
python3 demo_multi_step.py       # Multi-step planning examples
python3 demo_error_recovery.py   # Error recovery examples

# Extended integration
python3 demo_integrated.py       # Complex workflows

# Test all components
python3 test_all.py
```

## References

- Wei et al. (2022): "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
- Kojima et al. (2022): "Large Language Models are Zero-Shot Reasoners"
- Schick et al. (2023): "Toolformer: Language Models Can Teach Themselves to Use Tools"
- Yao et al. (2023): "Tree of Thoughts: Deliberate Problem Solving with Large Language Models"
