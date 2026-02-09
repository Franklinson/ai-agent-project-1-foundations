# Agent Tools

Simple tools for AI agents to perform basic operations.

## Tools

### 1. Calculator Tool
**File:** `calculator_tool.py`

Performs basic math operations.

**Usage:**
```python
from tools import calculator

result = calculator('add', 10, 5)
# {'success': True, 'result': 15, 'operation': 'add'}
```

**Operations:**
- `add`: Addition
- `subtract`: Subtraction
- `multiply`: Multiplication
- `divide`: Division
- `power`: Exponentiation
- `modulo`: Modulo

### 2. Search Tool
**File:** `search_tool.py`

Searches for text in a list of strings.

**Usage:**
```python
from tools import search

result = search('Python')
# {'success': True, 'query': 'Python', 'matches': [...], 'count': 1, 'total_searched': 5}
```

**Parameters:**
- `query`: Search string
- `data`: Optional list of strings (uses mock data if None)

### 3. Time Tool
**File:** `time_tool.py`

Gets current time information.

**Usage:**
```python
from tools import get_time

result = get_time(format='readable')
# {'success': True, 'time': '2025-01-14 12:30:45', 'format': 'readable', ...}
```

**Formats:**
- `iso`: ISO 8601 format
- `timestamp`: Unix timestamp
- `readable`: Human-readable format

## Error Handling

All tools return structured results with:
- `success`: Boolean indicating success/failure
- `error`: Error message (if failed)
- Additional data fields (if successful)
