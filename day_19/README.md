# Day 19: Input Processing Pipeline

## Overview

A modular input processing system that preprocesses, parses, and enriches user input with conversation context.

## Components

- **preprocessor.py**: Text normalization and validation
- **parser.py**: Intent classification and entity extraction
- **context_manager.py**: Conversation history and user preferences
- **input_processor.py**: Main pipeline integrating all components

## Usage

```python
from input_processor import InputHandler

handler = InputHandler()
result = handler.process("What is the weather on 2024-01-15?", user_id="user_123")

if result['success']:
    print(result['data']['intent'])      # 'query'
    print(result['data']['entities'])    # {'dates': ['2024-01-15']}
```

## Features

- Whitespace normalization and text cleaning
- Intent classification (query, command, greeting, unknown)
- Entity extraction (dates, keywords)
- Conversation history tracking
- User preferences management
- Context enrichment

## Demo

```bash
cd day_19
python3 demo.py
```

## Tests

```bash
cd day_19/tests
python3 test_input_processing.py
```

21 unit tests covering all components.
