# Day 23: Prompt Engineering System

A comprehensive system for building, testing, and managing AI agent prompts.

## Components

### 1. Prompt Templates (`prompt_templates.py`)
Static templates for building structured prompts.

**Usage:**
```python
from prompt_templates import PromptTemplates

prompt = PromptTemplates.build_full_prompt(
    capabilities=["Answer questions", "Use tools"],
    role="AI assistant",
    guidelines=["Be helpful", "Be concise"],
    tools=[{"name": "search", "description": "Search the web"}],
    history=[{"role": "user", "content": "Hello"}]
)
```

### 2. Dynamic Prompt Builder (`prompt_builder.py`)
Builds prompts dynamically based on current state.

**Usage:**
```python
from prompt_builder import PromptBuilder

builder = PromptBuilder(system_role="helpful assistant")
prompt = builder.build_prompt(
    user_input="What is AI?",
    tools=[{"name": "search", "description": "Search"}],
    context=[{"role": "user", "content": "Previous message"}],
    goal="Explain AI concepts"
)
```

### 3. ReAct Prompt Builder (`react_prompt.py`)
Implements the ReAct (Reasoning + Acting) pattern.

**Usage:**
```python
from react_prompt import ReActPromptBuilder

builder = ReActPromptBuilder()
prompt = builder.build_react_prompt(
    question="What is 2+2?",
    tools=[{"name": "calculate", "description": "Do math"}]
)
```

**ReAct Pattern:**
- **Thought**: Reason about the problem
- **Action**: Execute a tool
- **Observation**: Analyze the result
- Repeat until solved

### 4. Prompt Tester (`prompt_tester.py`)
Validates and tests prompts.

**Usage:**
```python
from prompt_tester import PromptTester

tester = PromptTester()
validation = tester.validate_prompt(
    prompt="You are an AI assistant",
    required_components=["assistant"]
)

test_case = tester.create_test_case(
    name="Basic Test",
    prompt="Your prompt here",
    expected_components=["role", "tools"]
)
```

## Prompt Patterns

### Basic Agent Pattern
```
System Role → Tools → Context → User Input
```

### ReAct Pattern
```
Instructions → Tools → Example → Question → Thought
```

### Template Pattern
```
System Instructions → Tool Descriptions → Context → History
```

## Best Practices

1. **Be Specific**: Clearly define the agent's role and capabilities
2. **Include Examples**: Show the desired output format
3. **Structure Information**: Use clear sections and formatting
4. **Validate Prompts**: Test prompts before deployment
5. **Keep Context Relevant**: Only include necessary history
6. **Document Tools**: Clearly describe tool parameters and usage
7. **Use Patterns**: Follow established patterns like ReAct for consistency

## Running the Demo

```bash
cd day_23
python demo.py
```

## Testing

```python
from prompt_tester import create_example_test_cases, PromptTester

tester = PromptTester()
test_cases = create_example_test_cases()
results = tester.run_test_cases(test_cases)
print(f"Passed: {results['passed']}/{results['total']}")
```

## Key Concepts

- **System Prompt**: Defines agent behavior and capabilities
- **Tool Descriptions**: Explains available actions
- **Context**: Conversation history and current state
- **ReAct**: Iterative reasoning and action pattern
- **Validation**: Ensures prompts contain required components
