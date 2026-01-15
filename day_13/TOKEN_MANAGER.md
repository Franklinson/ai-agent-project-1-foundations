# TokenManager Documentation

## Overview
`TokenManager` is a utility class for tracking and managing token usage against a defined budget when working with LLM APIs. It uses `tiktoken` to accurately count tokens for specific models.

## Class: TokenManager

### Constructor
```python
TokenManager(model="gpt-4", budget=100000)
```

**Parameters:**
- `model` (str): The LLM model name (default: "gpt-4"). Used to get the correct tokenizer encoding.
- `budget` (int): Maximum token limit (default: 100000).

**Attributes:**
- `model`: Stores the model name
- `encoding`: Tiktoken encoding instance for the specified model
- `budget`: Maximum allowed tokens
- `used`: Current token count used

### Methods

#### count_tokens(text)
Counts the number of tokens in the provided text.

**Parameters:**
- `text` (str): Text to tokenize

**Returns:**
- `int`: Number of tokens in the text

**Example:**
```python
manager = TokenManager()
tokens = manager.count_tokens("Hello world")  # Returns token count
```

#### can_add(text)
Checks if adding the text would stay within the budget.

**Parameters:**
- `text` (str): Text to check

**Returns:**
- `bool`: True if text fits within remaining budget, False otherwise

**Example:**
```python
if manager.can_add("Some text"):
    manager.add("Some text")
```

#### add(text)
Adds text to the token budget and updates the used count.

**Parameters:**
- `text` (str): Text to add to budget

**Returns:**
- `int`: Number of tokens added

**Raises:**
- `ValueError`: If adding the text would exceed the budget

**Example:**
```python
tokens_added = manager.add("Hello world")
```

#### remaining()
Returns the number of tokens remaining in the budget.

**Returns:**
- `int`: Remaining tokens (budget - used)

**Example:**
```python
available = manager.remaining()
```

## Usage Example

```python
# Initialize with custom budget
manager = TokenManager(model="gpt-4", budget=1000)

# Add text and track usage
manager.add("Hello world Franklin Etsey Hassey")

# Check remaining budget
print(f"Remaining: {manager.remaining()}")

# Verify before adding
if manager.can_add("More text"):
    manager.add("More text")
```

## Use Cases
- Managing context window limits for LLM APIs
- Preventing token budget overruns
- Tracking token consumption in multi-turn conversations
- Optimizing prompt engineering within constraints
