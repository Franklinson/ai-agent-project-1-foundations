# Cost Calculator Documentation

## Overview

The Cost Calculator is a utility for tracking and calculating API costs for OpenAI language model usage. It counts tokens and computes costs based on model-specific pricing for both input and output tokens.

## Features

- **Token Counting**: Accurate token counting using tiktoken
- **Cost Calculation**: Per-request cost tracking for input/output tokens
- **Multi-Model Support**: Handles different pricing for GPT-4 and GPT-3.5-turbo
- **Statistics Tracking**: Cumulative cost and usage statistics
- **Request History**: Detailed logs of all API requests

## Usage

### Basic Usage

```python
from cost_calculator import CostCalculator

# Initialize calculator
calc = CostCalculator()

# Calculate cost for a single request
cost = calc.calculate_cost(
    input_text="What is machine learning?",
    output_text="Machine learning is a subset of AI that enables systems to learn from data.",
    model="gpt-4"
)

print(f"Request cost: ${cost:.4f}")
```

### Tracking Multiple Requests

```python
calc = CostCalculator()

# Multiple requests
calc.calculate_cost("Question 1", "Answer 1", "gpt-4")
calc.calculate_cost("Question 2", "Answer 2", "gpt-3.5-turbo")
calc.calculate_cost("Question 3", "Answer 3", "gpt-4")

# Get statistics
stats = calc.get_stats()
print(f"Total cost: ${stats['total_cost']:.4f}")
print(f"Total requests: {stats['total_requests']}")
print(f"Average cost per request: ${stats['avg_cost']:.4f}")
```

### Token Counting Only

```python
calc = CostCalculator()

# Count tokens without calculating cost
text = "This is a sample text for token counting."
token_count = calc.count_tokens(text, model="gpt-4")
print(f"Token count: {token_count}")
```

## API Reference

### CostCalculator Class

#### `__init__()`
Initialize the cost calculator with default pricing.

**Pricing Structure:**
- GPT-4: $0.01 per 1K input tokens, $0.03 per 1K output tokens
- GPT-3.5-turbo: $0.0005 per 1K input tokens, $0.0015 per 1K output tokens

#### `count_tokens(text: str, model: str = "gpt-4") -> int`
Count the number of tokens in a text string.

**Parameters:**
- `text`: The text to tokenize
- `model`: Model name for tokenization (default: "gpt-4")

**Returns:** Integer token count

**Example:**
```python
tokens = calc.count_tokens("Hello, world!", "gpt-4")
# Returns: 4
```

#### `calculate_cost(input_text: str, output_text: str, model: str = "gpt-4") -> float`
Calculate the cost of an API request.

**Parameters:**
- `input_text`: The prompt/input text
- `output_text`: The generated response text
- `model`: Model used (default: "gpt-4")

**Returns:** Float cost in USD

**Side Effects:**
- Updates `total_cost`
- Appends request details to `requests` list

**Example:**
```python
cost = calc.calculate_cost(
    "Explain quantum computing",
    "Quantum computing uses quantum mechanics...",
    "gpt-4"
)
# Returns: 0.0234 (example)
```

#### `get_stats() -> dict`
Get cumulative usage statistics.

**Returns:** Dictionary with:
- `total_cost`: Total accumulated cost (float)
- `total_requests`: Number of requests tracked (int)
- `avg_cost`: Average cost per request (float)

**Example:**
```python
stats = calc.get_stats()
# Returns: {
#   "total_cost": 0.1234,
#   "total_requests": 5,
#   "avg_cost": 0.0247
# }
```

## Pricing Information

### Current Pricing (as of implementation)

| Model | Input (per 1K tokens) | Output (per 1K tokens) |
|-------|----------------------|------------------------|
| GPT-4 | $0.01 | $0.03 |
| GPT-3.5-turbo | $0.0005 | $0.0015 |

**Note:** Pricing may change. Update the `pricing` dictionary in `__init__` to reflect current rates.

## Use Cases

### 1. Budget Monitoring
```python
calc = CostCalculator()
BUDGET_LIMIT = 10.0  # $10 budget

for query in user_queries:
    cost = calc.calculate_cost(query, response, "gpt-4")
    
    if calc.total_cost > BUDGET_LIMIT:
        print("Budget exceeded!")
        break
```

### 2. Model Comparison
```python
calc_gpt4 = CostCalculator()
calc_gpt35 = CostCalculator()

# Same query on different models
calc_gpt4.calculate_cost(prompt, response_gpt4, "gpt-4")
calc_gpt35.calculate_cost(prompt, response_gpt35, "gpt-3.5-turbo")

print(f"GPT-4 cost: ${calc_gpt4.total_cost:.4f}")
print(f"GPT-3.5 cost: ${calc_gpt35.total_cost:.4f}")
```

### 3. Cost Optimization
```python
calc = CostCalculator()

# Analyze request history
for req in calc.requests:
    if req['cost'] > 0.05:  # Flag expensive requests
        print(f"High cost request: ${req['cost']:.4f}")
        print(f"Input tokens: {req['input_tokens']}")
        print(f"Output tokens: {req['output_tokens']}")
```

## Implementation Details

### Token Counting
Uses `tiktoken` library for accurate token counting that matches OpenAI's tokenization:
```python
encoding = tiktoken.encoding_for_model(model)
tokens = len(encoding.encode(text))
```

### Cost Formula
```
input_cost = (input_tokens / 1000) × input_price_per_1k
output_cost = (output_tokens / 1000) × output_price_per_1k
total_cost = input_cost + output_cost
```

### Request Tracking
Each request is stored with:
- `input_tokens`: Number of input tokens
- `output_tokens`: Number of output tokens
- `cost`: Total cost for the request
- `model`: Model used

## Best Practices

1. **Initialize Once**: Create a single CostCalculator instance per session
2. **Track All Requests**: Call calculate_cost for every API request
3. **Monitor Regularly**: Check get_stats() periodically
4. **Update Pricing**: Keep pricing dictionary current with OpenAI rates
5. **Export Data**: Save requests list for detailed analysis

## Limitations

- Pricing is hardcoded and needs manual updates
- No support for other model variants (e.g., GPT-4-32k)
- No built-in cost alerts or thresholds
- Request history stored in memory only
- No support for streaming token counting

## Future Enhancements

- Dynamic pricing updates from API
- Cost alerts and budget limits
- Export to CSV/JSON for analysis
- Support for additional models
- Streaming token counting
- Cost prediction based on input length
- Integration with OpenAI usage API

## Dependencies

- `tiktoken`: OpenAI's token counting library
- `openai`: OpenAI API client (for interactive test)
- `python-dotenv`: Environment variable management (for interactive test)

Install with:
```bash
pip install tiktoken openai python-dotenv
```

## Interactive Testing

An interactive test script is provided to test the cost calculator with real AI responses:

```bash
cd day_11
python test_interactive.py
```

### How It Works

1. User enters prompts interactively
2. AI generates responses using OpenAI API
3. Cost calculator tracks input/output tokens and costs
4. All conversations are saved to a timestamped JSON file
5. Session summary displays total costs and statistics

### Output File Structure

```json
{
  "conversations": [
    {
      "timestamp": "2024-01-15T10:30:45.123456",
      "prompt": "What is machine learning?",
      "response": "Machine learning is...",
      "cost": 0.0234
    }
  ],
  "statistics": {
    "total_cost": 0.0234,
    "total_requests": 1,
    "avg_cost": 0.0234
  },
  "detailed_requests": [
    {
      "input_tokens": 15,
      "output_tokens": 120,
      "cost": 0.0234,
      "model": "gpt-4"
    }
  ]
}
```

### Example Session

```
=== AI Cost Tracking Test ===
Enter prompts (type 'quit' to exit)

Your prompt: What is machine learning?
Generating response...

AI Response: Machine learning is a subset of artificial intelligence...
Cost: $0.0234

--------------------------------------------------
Your prompt: quit

=== Session Summary ===
Total prompts: 1
Total cost: $0.0234
Average cost per prompt: $0.0234

Results saved to: ai_test_results_20240115_103045.json
```

## Example Output

```
Cost: $0.0012
{
  'total_cost': 0.0012,
  'total_requests': 1,
  'avg_cost': 0.0012
}
```