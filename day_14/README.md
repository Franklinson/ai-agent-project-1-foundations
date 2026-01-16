# Day 14: Context Manager

## Overview
Context manager for tracking conversation history, managing token budgets, and summarizing old messages to maintain efficient LLM interactions.

## Features
- **Conversation tracking** - Store and manage message history
- **Token budget management** - Stay within configurable token limits
- **LLM-based summarization** - Intelligently compress old messages
- **Recent context preservation** - Keep most recent messages intact

## Usage

```python
from context_manager import ContextManager

# Initialize
manager = ContextManager(max_tokens=100000, recent_count=10)

# Add messages
manager.add_message("user", "Hello!")
manager.add_message("assistant", "Hi there!")

# Get context
context = manager.get_context()

# Count tokens
tokens = manager.count_tokens("Some text")
```

## Configuration
- `model`: LLM model for token encoding (default: "gpt-4")
- `max_tokens`: Maximum token budget (default: 100000)
- `recent_count`: Number of recent messages to preserve (default: 10)

## Testing
Run tests: `python context_manager.py`

## Requirements
- tiktoken
- openai
- python-dotenv
- OPENAI_API_KEY environment variable
