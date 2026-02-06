# Day 27: Agent Loop Implementation

## Overview
A complete agent system implementing the Perception-Reasoning-Action-Observation (PRAO) loop.

## Components

### 1. PerceptionModule (`perception.py`)
- Normalizes user input
- Extracts intent using keyword matching
- Extracts entities (emails, numbers, dates)
- Returns structured data

### 2. ReasoningModule (`reasoning.py`)
- Analyzes perceived input
- Creates action plans
- Selects appropriate tools based on intent
- Returns analysis and action plan

### 3. ActionModule (`action.py`)
- Maintains tool registry
- Executes planned actions
- Handles errors gracefully
- Returns execution results

### 4. ObservationModule (`observation.py`)
- Evaluates action results
- Reflects on outcomes
- Makes decisions (complete/continue/error)
- Returns observation with decision

### 5. StateManager (`state_manager.py`)
- Stores conversation history
- Tracks goals
- Manages context
- Provides state retrieval

### 6. Agent (`agent.py`)
- Coordinates all modules
- Implements main agent loop
- Manages state updates
- Returns complete execution trace

## Agent Loop Flow

```
User Input → Perception → Reasoning → Action → Observation → Decision
                ↓            ↓          ↓          ↓
              State ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
```

## Usage

```python
from agent import Agent

agent = Agent()
result = agent.run("What is the weather today?")
print(result['decision'])  # 'complete'
```

## Running the Demo

```bash
cd day_27
python3 demo.py
```

## Test Cases

The demo includes 4 test cases:
1. Question: "What is the weather today?"
2. Command with entities: "Create a meeting on 12/25/2024 at 3 PM"
3. Request with email: "Please send report to john@example.com"
4. Greeting: "Hello, how are you?"

## Architecture

- **Modular design**: Each component is independent
- **Minimal implementation**: Only essential code
- **Error handling**: Basic try/except in action execution
- **State management**: In-memory storage for conversation tracking
- **Extensible**: Easy to add new tools and intents
