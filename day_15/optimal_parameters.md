# Optimal Parameter Settings Guide

## Overview

This guide provides comprehensive recommendations for LLM parameter settings across different use cases, based on empirical testing and best practices.

---

## Core Parameters

### 1. Temperature (0.0 - 2.0)
Controls randomness in token selection. Lower values = more deterministic, higher values = more creative.

### 2. Top P (0.0 - 1.0)
Nucleus sampling - considers tokens with cumulative probability up to P.

### 3. Frequency Penalty (0.0 - 2.0)
Reduces repetition of tokens based on their frequency in the text.

### 4. Presence Penalty (0.0 - 2.0)
Reduces repetition of tokens regardless of frequency.

### 5. Max Tokens
Maximum length of generated output.

---

## Use Case Configurations

### 1. Factual Content & Documentation

**Use Cases:**
- Technical documentation
- API responses
- Data extraction
- Fact-based Q&A
- Code generation

**Optimal Parameters:**
```json
{
  "temperature": 0.1,
  "top_p": 0.9,
  "frequency_penalty": 0.0,
  "presence_penalty": 0.0,
  "max_tokens": 500
}
```

**Why These Settings:**
- Low temperature ensures consistency and accuracy
- No penalties allow natural technical terminology repetition
- Predictable outputs for production systems

**Trade-offs:**
- ✅ High consistency and reliability
- ✅ Minimal hallucinations
- ❌ Limited creativity
- ❌ Repetitive phrasing possible

**Example:**
```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Explain REST API"}],
    temperature=0.1,
    top_p=0.9
)
```

---

### 2. Creative Writing & Storytelling

**Use Cases:**
- Fiction writing
- Marketing copy
- Brainstorming
- Poetry
- Character dialogue

**Optimal Parameters:**
```json
{
  "temperature": 1.2,
  "top_p": 0.95,
  "frequency_penalty": 0.3,
  "presence_penalty": 0.2,
  "max_tokens": 1000
}
```

**Why These Settings:**
- High temperature enables creative, unexpected outputs
- Penalties prevent repetitive language
- Higher top_p allows diverse vocabulary

**Trade-offs:**
- ✅ Unique, creative outputs
- ✅ Varied vocabulary and style
- ❌ Less predictable
- ❌ May require multiple generations

**Example:**
```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Write a sci-fi story"}],
    temperature=1.2,
    frequency_penalty=0.3,
    presence_penalty=0.2
)
```

---

### 3. Code Generation

**Use Cases:**
- Function implementation
- Code completion
- Bug fixes
- Code refactoring
- Algorithm implementation

**Optimal Parameters:**
```json
{
  "temperature": 0.2,
  "top_p": 0.9,
  "frequency_penalty": 0.0,
  "presence_penalty": 0.0,
  "max_tokens": 800
}
```

**Why These Settings:**
- Very low temperature for syntactic correctness
- No penalties - code naturally repeats patterns
- Deterministic for reliable compilation

**Trade-offs:**
- ✅ Syntactically correct code
- ✅ Follows best practices
- ✅ Consistent style
- ❌ Less creative solutions
- ❌ May stick to common patterns

**Example:**
```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Write a binary search in Python"}],
    temperature=0.2,
    top_p=0.9
)
```

---

### 4. Conversational AI & Chatbots

**Use Cases:**
- Customer support
- Virtual assistants
- Interactive chat
- Tutoring systems
- General conversation

**Optimal Parameters:**
```json
{
  "temperature": 0.7,
  "top_p": 0.9,
  "frequency_penalty": 0.2,
  "presence_penalty": 0.1,
  "max_tokens": 300
}
```

**Why These Settings:**
- Balanced temperature for natural conversation
- Light penalties prevent robotic repetition
- Moderate length for chat context

**Trade-offs:**
- ✅ Natural, engaging responses
- ✅ Balanced consistency and variety
- ✅ Good for multi-turn conversations
- ❌ Occasional unexpected responses

**Example:**
```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "How do I reset my password?"}
    ],
    temperature=0.7,
    frequency_penalty=0.2,
    presence_penalty=0.1
)
```

---

### 5. Educational Content

**Use Cases:**
- Explanations
- Tutorials
- Study guides
- Concept simplification
- Learning materials

**Optimal Parameters:**
```json
{
  "temperature": 0.5,
  "top_p": 0.9,
  "frequency_penalty": 0.1,
  "presence_penalty": 0.1,
  "max_tokens": 600
}
```

**Why These Settings:**
- Medium-low temperature for accuracy with clarity
- Light penalties for varied explanations
- Longer outputs for thorough explanations

**Trade-offs:**
- ✅ Clear, accurate explanations
- ✅ Appropriate detail level
- ✅ Engaging without sacrificing accuracy
- ❌ May be verbose

**Example:**
```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Explain quantum computing simply"}],
    temperature=0.5,
    frequency_penalty=0.1,
    presence_penalty=0.1
)
```

---

### 6. Data Analysis & Summarization

**Use Cases:**
- Text summarization
- Data insights
- Report generation
- Key point extraction
- Trend analysis

**Optimal Parameters:**
```json
{
  "temperature": 0.3,
  "top_p": 0.9,
  "frequency_penalty": 0.0,
  "presence_penalty": 0.0,
  "max_tokens": 400
}
```

**Why These Settings:**
- Low temperature for factual accuracy
- No penalties for technical terms
- Focused, concise outputs

**Trade-offs:**
- ✅ Accurate summaries
- ✅ Consistent format
- ✅ Reliable extraction
- ❌ May miss nuanced interpretations

**Example:**
```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Summarize this data: [data]"}],
    temperature=0.3,
    top_p=0.9
)
```

---

### 7. Brainstorming & Ideation

**Use Cases:**
- Idea generation
- Problem solving
- Creative solutions
- Alternative approaches
- Innovation workshops

**Optimal Parameters:**
```json
{
  "temperature": 1.5,
  "top_p": 0.98,
  "frequency_penalty": 0.5,
  "presence_penalty": 0.3,
  "max_tokens": 500
}
```

**Why These Settings:**
- Very high temperature for maximum creativity
- High penalties force diverse ideas
- Wide token sampling for unexpected connections

**Trade-offs:**
- ✅ Highly creative, unique ideas
- ✅ Unexpected perspectives
- ✅ Breaks conventional thinking
- ❌ May produce impractical suggestions
- ❌ Requires filtering

**Example:**
```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Generate 10 unique app ideas"}],
    temperature=1.5,
    frequency_penalty=0.5,
    presence_penalty=0.3
)
```

---

### 8. Translation & Localization

**Use Cases:**
- Language translation
- Content localization
- Cultural adaptation
- Multilingual content

**Optimal Parameters:**
```json
{
  "temperature": 0.3,
  "top_p": 0.9,
  "frequency_penalty": 0.0,
  "presence_penalty": 0.0,
  "max_tokens": 500
}
```

**Why These Settings:**
- Low temperature for accurate translation
- No penalties for natural language patterns
- Preserves meaning over creativity

**Trade-offs:**
- ✅ Accurate translations
- ✅ Maintains context
- ✅ Consistent terminology
- ❌ May be literal rather than idiomatic

---

## Parameter Interaction Matrix

| Temperature | Frequency Penalty | Best For |
|-------------|-------------------|----------|
| 0.1 - 0.3   | 0.0 - 0.1        | Technical, factual content |
| 0.4 - 0.6   | 0.1 - 0.2        | Educational, explanatory |
| 0.7 - 0.9   | 0.2 - 0.3        | Conversational, balanced |
| 1.0 - 1.3   | 0.3 - 0.5        | Creative writing |
| 1.4 - 2.0   | 0.5 - 0.8        | Experimental, brainstorming |

---

## Advanced Tuning Strategies

### 1. A/B Testing Approach
```python
def compare_parameters(prompt, param_sets):
    results = []
    for params in param_sets:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            **params
        )
        results.append({
            "params": params,
            "output": response.choices[0].message.content
        })
    return results
```

### 2. Dynamic Parameter Adjustment
```python
def adaptive_temperature(task_complexity):
    if task_complexity == "simple":
        return 0.2
    elif task_complexity == "moderate":
        return 0.7
    else:
        return 1.2
```

### 3. Context-Aware Settings
```python
def get_context_params(context_length):
    if context_length > 2000:
        return {"temperature": 0.3, "max_tokens": 200}  # Concise
    else:
        return {"temperature": 0.7, "max_tokens": 500}  # Detailed
```

---

## Common Pitfalls

### ❌ Temperature Too High (> 1.5)
- **Problem:** Incoherent, unreliable outputs
- **Solution:** Use 1.2 max for production, 1.5 only for experimentation

### ❌ Conflicting Parameters
- **Problem:** High temperature + high penalties = unpredictable
- **Solution:** Balance creativity (temp) with control (penalties)

### ❌ Wrong Use Case Mapping
- **Problem:** Using creative settings for factual tasks
- **Solution:** Match parameters to task requirements

### ❌ Ignoring Token Costs
- **Problem:** High max_tokens increases costs
- **Solution:** Set appropriate limits per use case

---

## Quick Reference Table

| Use Case | Temperature | Frequency Penalty | Presence Penalty | Max Tokens |
|----------|-------------|-------------------|------------------|------------|
| Factual | 0.1 | 0.0 | 0.0 | 500 |
| Creative | 1.2 | 0.3 | 0.2 | 1000 |
| Code | 0.2 | 0.0 | 0.0 | 800 |
| Chat | 0.7 | 0.2 | 0.1 | 300 |
| Educational | 0.5 | 0.1 | 0.1 | 600 |
| Analysis | 0.3 | 0.0 | 0.0 | 400 |
| Brainstorm | 1.5 | 0.5 | 0.3 | 500 |
| Translation | 0.3 | 0.0 | 0.0 | 500 |

---

## Testing Your Parameters

```python
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def test_parameters(prompt, params):
    """Test parameter configuration"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        **params
    )
    
    print(f"Parameters: {params}")
    print(f"Output: {response.choices[0].message.content}")
    print(f"Tokens: {response.usage.total_tokens}")
    print("-" * 50)

# Test different configurations
test_parameters(
    "Explain machine learning",
    {"temperature": 0.1, "max_tokens": 200}
)

test_parameters(
    "Write a creative story",
    {"temperature": 1.2, "frequency_penalty": 0.3, "max_tokens": 300}
)
```

---

## Conclusion

Optimal parameter settings depend heavily on your specific use case. Start with the recommendations in this guide, then fine-tune based on:

1. **Output quality** - Does it meet your requirements?
2. **Consistency** - Is it reliable across multiple runs?
3. **Cost** - Are token counts acceptable?
4. **User feedback** - Does it satisfy end users?

**Golden Rule:** When in doubt, start with temperature 0.7 and adjust from there.

---

## Additional Resources

- Test your parameters with `parameter_tuner.py`
- Compare outputs with `parameter_dashboard.py`
- Review findings in `FINDINGS.md`
- Check tuning results in `tuning_recommendations.md`
