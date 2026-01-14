# Transformer Architecture Notes

## High-Level Overview

Transformers are the foundation of modern LLMs (GPT, BERT, Claude, etc.). Unlike older sequential models (RNNs), transformers process all tokens in parallel using attention mechanisms.

**Key Innovation**: The ability to draw relationships between any tokens in the input, regardless of distance, all at once.

### Core Components

1. **Input Embedding**: Converts text tokens into numerical vectors
2. **Positional Encoding**: Adds position information (since parallel processing loses order)
3. **Encoder Layers**: Process and understand the input (used in BERT)
4. **Decoder Layers**: Generate output text (used in GPT)
5. **Attention Mechanism**: The "brain" that focuses on relevant parts

### Why Transformers Work

- **Parallel Processing**: All tokens processed simultaneously → faster training
- **Long-Range Dependencies**: Can connect tokens far apart in text
- **Scalability**: Architecture scales efficiently with more data and compute

## Attention Mechanisms

### What is Attention?

Attention is the LLM's ability to focus on different parts of the input when processing each token. Like reading a book and paying attention to important parts to derive meaning.

### Self-Attention (The Core Mechanism)

For each token, self-attention computes:
1. **Query (Q)**: "What am I looking for?"
2. **Key (K)**: "What do I contain?"
3. **Value (V)**: "What information do I carry?"

**Process**:
```
For token "cat" in "The cat sat on the mat":
- Query: What context do I need?
- Compare with Keys of all tokens (The, cat, sat, on, the, mat)
- Calculate attention scores (how relevant each token is)
- Weight the Values by these scores
- Result: Contextual representation of "cat"
```

### Multi-Head Attention

Instead of one attention mechanism, use multiple "heads" in parallel:
- Head 1 might focus on grammar relationships
- Head 2 might focus on semantic meaning
- Head 3 might focus on long-range dependencies

Each head learns different patterns, then results are combined.

### Why Attention Matters

**Example**: "The animal didn't cross the street because it was too tired."
- Attention helps the model understand "it" refers to "animal" (not "street")
- Creates relationships: it ← tired ← animal
- More context = better understanding

## Text Generation

### How LLMs Generate Text

LLMs work by predicting the next token based on previous tokens - similar to how our brain completes sentences.

### Generation Process

```
1. Start with prompt: "The cat sat"
   - Tokenize: ["The", "cat", "sat"]
   
2. Process through transformer:
   - Apply attention to understand context
   - Generate probability distribution over all possible next tokens
   
3. Sample next token: "on" (highest probability)
   - Sequence: ["The", "cat", "sat", "on"]
   
4. Repeat with updated sequence:
   - Process: ["The", "cat", "sat", "on"]
   - Predict: "the" 
   - Sequence: ["The", "cat", "sat", "on", "the"]
   
5. Continue until:
   - End token is generated
   - Max length reached
   - Stop sequence encountered
```

### Autoregressive Generation

Each prediction uses ALL previous tokens:
- Token 1: Based on prompt
- Token 2: Based on prompt + token 1
- Token 3: Based on prompt + token 1 + token 2
- And so on...

This is why:
- **More context = better predictions**
- Errors can compound (one wrong token affects all future tokens)
- Temperature/sampling strategies matter

### Sampling Strategies

1. **Greedy**: Always pick highest probability token (deterministic, boring)
2. **Temperature**: Control randomness (low = focused, high = creative)
3. **Top-k**: Sample from top k most likely tokens
4. **Top-p (nucleus)**: Sample from smallest set with cumulative probability p

### Key Insight

> "LLMs don't 'think' - they predict patterns. But with enough context and attention to relationships between tokens, these predictions become remarkably coherent and useful."

Providing rich context in prompts helps the attention mechanism focus on relevant information, leading to better token predictions.