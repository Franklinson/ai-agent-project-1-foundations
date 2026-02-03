# Day 24: Prompt Engineering Best Practices

## Overview
This module demonstrates prompt engineering best practices through creating, testing, and iterating on AI agent prompts.

## Deliverables

### 1. Agent Prompts (`prompts/`)
Three production-ready agent prompts following best practices:

- **weather_agent_prompt.md**: Weather information agent with location handling, forecasts, and alerts
- **email_agent_prompt.md**: Email management agent for composing, searching, and organizing
- **research_agent_prompt.md**: Research agent for multi-source investigation and synthesis
- **weather_agent_prompt_v2.md**: Enhanced weather agent with edge cases and safety features

Each prompt includes:
- Clear role definition
- Specific instructions
- Tool documentation with parameters
- Output format specifications
- Concrete examples
- Error handling
- Edge cases

### 2. Prompt Construction (`prompt_examples.py`)
Programmatic prompt building utilities demonstrating:

- `build_weather_prompt(user_input, context)`: Dynamic weather prompt construction
- `build_email_prompt(user_input, context)`: Context-aware email prompt building
- `build_research_prompt(user_input, context, goal)`: Adaptive research prompt generation

**Features**:
- Context injection
- Format specifications
- Example inclusion
- Adaptive based on parameters

**Usage**:
```bash
python3 day_24/prompt_examples.py
```

### 3. Prompt Testing (`prompt_tester.py`)
Validation and evaluation utilities:

**Classes**:
- `TestCase`: Structure for test cases with expected components
- `ValidationResult`: Test results with score and feedback
- `PromptTester`: Main testing class

**Validation Checks**:
- Role definition present
- Specific instructions included
- Tool descriptions documented
- Format specifications provided
- Examples included

**Metrics**:
- Validation score (0-10)
- Component presence
- Tool count
- Example count

**Usage**:
```bash
python3 day_24/prompt_tester.py
```

**Test Results**:
- Weather Agent: 10/10 ✓ PASS
- Email Agent: 10/10 ✓ PASS
- Research Agent: 10/10 ✓ PASS

### 4. Best Practices Guide (`prompt_guidelines.md`)
Comprehensive documentation covering:

**Core Principles**:
1. Be specific and clear
2. Define clear role and scope
3. Provide context and examples
4. Specify output format
5. Document tools thoroughly

**Includes**:
- Prompt structure template
- Best practices checklist
- Common pitfalls to avoid
- Iteration process
- Good vs bad examples
- Advanced techniques
- Testing guidelines
- Version control approach

## Key Learnings

### What Makes a Good Prompt

1. **Specificity**: "Always confirm location before fetching data" vs "Be helpful"
2. **Examples**: Show complete interactions, not just descriptions
3. **Format Templates**: Exact output format with placeholders
4. **Tool Guidance**: Document when to use each tool, not just what it does
5. **Edge Cases**: Explicitly handle extreme weather, missing data, ambiguous input
6. **Decision Logic**: Provide clear rules for complex scenarios

### Common Pitfalls

- ❌ Vague instructions ("nicely", "appropriately")
- ❌ Missing tool usage guidance
- ❌ Ambiguous format specifications
- ❌ No concrete examples
- ❌ Ignoring edge cases
- ❌ Unclear priorities
- ❌ Missing error messages

### Iteration Process

1. **Initial Draft**: Basic structure with core functionality
2. **Validation**: Run through testing tool
3. **Enhancement**: Add examples, decision logic, edge cases
4. **Testing**: Test with real inputs
5. **Refinement**: Address issues found
6. **Review**: Final checklist verification

## Quick Start

### Test Existing Prompts
```bash
cd day_24
python3 prompt_tester.py
```

### Generate Example Prompts
```bash
python3 prompt_examples.py
```

### Create Your Own Prompt

1. Use template from `prompt_guidelines.md`
2. Follow the checklist
3. Add to `prompt_tester.py` test cases
4. Run validation
5. Iterate based on results

## File Structure

```
day_24/
├── prompts/
│   ├── weather_agent_prompt.md       # Weather agent v1
│   ├── weather_agent_prompt_v2.md    # Weather agent v2 (enhanced)
│   ├── email_agent_prompt.md         # Email management agent
│   └── research_agent_prompt.md      # Research agent
├── prompt_examples.py                 # Programmatic prompt construction
├── prompt_tester.py                   # Testing and validation utilities
├── prompt_guidelines.md               # Best practices documentation
└── README.md                          # This file
```

## Best Practices Summary

### ✓ Do
- Use specific, actionable instructions
- Provide 2-3 examples per use case
- Include exact format templates
- Document when to use each tool
- Address edge cases explicitly
- Use priority indicators (ALWAYS, NEVER)
- Test and iterate

### ✗ Don't
- Use vague language
- Assume agent will figure it out
- Skip examples
- Ignore error handling
- Forget edge cases
- Leave format ambiguous
- Skip testing

## Next Steps

1. Apply these practices to your own agents
2. Build a prompt library for common use cases
3. Create domain-specific prompt templates
4. Integrate testing into CI/CD pipeline
5. Collect user feedback for continuous improvement

## Resources

- `prompt_guidelines.md`: Complete best practices guide
- `prompt_tester.py`: Validation tool source code
- `prompt_examples.py`: Construction examples
- Agent prompts in `prompts/`: Reference implementations
