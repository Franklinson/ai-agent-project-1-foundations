# Prompt Writing Best Practices Guide

## Overview
This guide documents best practices for writing effective AI agent prompts based on testing and iteration of weather, email, and research agents.

## Core Principles

### 1. Be Specific and Clear
**Why**: Vague instructions lead to inconsistent agent behavior.

**Good**:
```
Always confirm location before fetching weather data.
Provide temperature in both Celsius and Fahrenheit.
```

**Bad**:
```
Get weather information and show it to the user.
```

### 2. Define Clear Role and Scope
**Why**: Agents need to understand their purpose and boundaries.

**Good**:
```
You are a weather information agent that provides accurate, 
location-specific weather data and forecasts with actionable recommendations.
```

**Bad**:
```
You help with weather.
```

### 3. Provide Context and Examples
**Why**: Examples demonstrate expected behavior better than descriptions alone.

**Good**:
```
**User**: "What's the weather in Tokyo?"

**Agent Response**:
📍 Location: Tokyo, Japan
🌡️ Temperature: 18°C (64°F)
☁️ Conditions: Partly cloudy
💡 Advice: Light jacket recommended.
```

**Bad**:
```
Respond with weather information when asked.
```

### 4. Specify Output Format
**Why**: Consistent formatting improves user experience and parsing.

**Good**:
```
## Response Format
📧 Draft Email

To: [recipient@example.com]
Subject: [Subject line]

[Email body]

---
Reply 'yes' to send or provide changes.
```

**Bad**:
```
Format the email nicely.
```

### 5. Document Tools Thoroughly
**Why**: Agents need to know when and how to use each tool.

**Good**:
```
### send_email(to: str, subject: str, body: str, cc: str = None)
Sends an email to specified recipients.
- **to**: Recipient email address(es), comma-separated
- **subject**: Email subject line
- **body**: Email body content
- **Returns**: Confirmation with message ID
- **Use when**: User confirms they want to send
```

**Bad**:
```
send_email - sends emails
```

## Prompt Structure Template

```markdown
# [Agent Name] Prompt

## Role
[Clear, specific role definition]

## Core Instructions
1. [Specific instruction with action verb]
2. [Specific instruction with action verb]
3. [Include edge cases and priorities]

## Available Tools

### tool_name(param: type)
[Description of what it does]
- **param**: [What it is, format, examples]
- **Returns**: [What it returns]
- **Use when**: [Specific scenarios]

## Response Format

### [Scenario Name]
```
[Exact format template with placeholders]
```

## Examples

**User**: "[Example user input]"

**Agent Response**:
```
[Complete example response]
```

## Decision Logic
[When to use which tool/approach]

## Error Handling
- [Error type]: "[Exact error message]"

## Constraints
- [Hard limit or rule]
- [Safety consideration]

## Edge Cases
- [Unusual scenario]: [How to handle]
```

## Best Practices Checklist

### Before Writing
- [ ] Understand the agent's purpose and scope
- [ ] List all available tools and their capabilities
- [ ] Identify common user requests and edge cases
- [ ] Define success criteria for the agent

### While Writing
- [ ] Start with clear role definition
- [ ] Use numbered or bulleted lists for instructions
- [ ] Document each tool with parameters and return values
- [ ] Include "Use when" guidance for each tool
- [ ] Provide exact output format templates
- [ ] Add 2-3 concrete examples per major use case
- [ ] Specify error messages verbatim
- [ ] Include decision logic for complex scenarios
- [ ] Address edge cases explicitly
- [ ] Define constraints and safety rules

### After Writing
- [ ] Test with validation tool
- [ ] Check all required components present
- [ ] Verify examples are complete and realistic
- [ ] Ensure format specifications are unambiguous
- [ ] Review for vague language ("nicely", "appropriately", "good")
- [ ] Confirm tool descriptions include when to use them
- [ ] Test with edge cases
- [ ] Get feedback from actual usage

## Common Pitfalls to Avoid

### 1. Vague Instructions
❌ "Be helpful and friendly"
✅ "Maintain professional tone unless user specifies otherwise"

### 2. Missing Tool Usage Guidance
❌ "Use the available tools"
✅ "Use web_search for recent news, academic_search for peer-reviewed research"

### 3. Ambiguous Format
❌ "Format the response clearly"
✅ Provide exact template with placeholders

### 4. No Examples
❌ Only describing what agent should do
✅ Show 2-3 complete interaction examples

### 5. Ignoring Edge Cases
❌ Only handling happy path
✅ Document extreme weather, missing data, ambiguous input

### 6. Unclear Priorities
❌ List all instructions equally
✅ "ALWAYS check alerts before providing weather information"

### 7. Missing Error Messages
❌ "Handle errors appropriately"
✅ 'Location not found: "I couldn\'t find \'[input]\'. Try: city name or zip code."'

### 8. No Decision Logic
❌ Assume agent will figure it out
✅ "If severity is 'extreme', lead with safety information"

## Iteration Process

### Step 1: Initial Draft
- Write basic structure with role, instructions, tools, format
- Include at least 1 example
- Focus on core functionality

### Step 2: Validation
- Run through validation tool
- Check for missing components
- Verify structure completeness

### Step 3: Enhancement
- Add more examples (aim for 2-3 per major use case)
- Expand tool documentation with "Use when" guidance
- Add decision logic for complex scenarios
- Document edge cases

### Step 4: Testing
- Test with real or simulated user inputs
- Identify unclear instructions
- Find missing error handling
- Discover undocumented edge cases

### Step 5: Refinement
- Address issues found in testing
- Make instructions more specific
- Add missing examples
- Clarify ambiguous language

### Step 6: Review
- Compare against checklist
- Ensure all components present
- Verify examples are complete
- Check for vague language

## Good vs Bad Examples

### Example 1: Instructions

**Bad**:
```
Help users with their emails.
Be professional.
```

**Good**:
```
1. Maintain professional tone unless user specifies otherwise
2. Always confirm before sending emails
3. Ask for missing required fields (recipient, subject, body)
4. Preserve context from previous messages in threads
```

### Example 2: Tool Documentation

**Bad**:
```
search_emails - searches for emails
```

**Good**:
```
### search_emails(query: str, folder: str = "inbox", limit: int = 10)
Searches emails based on query parameters.
- **query**: Search terms (sender, subject, keywords, date range)
- **folder**: "inbox", "sent", "drafts", "archive", "all"
- **limit**: Maximum results to return (1-50)
- **Returns**: List of matching emails with metadata
- **Use when**: User asks to find/search emails or mentions sender/topic
```

### Example 3: Format Specification

**Bad**:
```
Show the weather in a nice format.
```

**Good**:
```
📍 Location: [City, Country]
🌡️ Temperature: [X]°C ([Y]°F)
☁️ Conditions: [Description]
💧 Humidity: [X]%
💨 Wind: [X] km/h ([Y] mph) [Direction]
💡 Advice: [Specific actionable recommendation]
```

### Example 4: Examples

**Bad**:
```
When user asks about weather, provide weather information.
```

**Good**:
```
**User**: "What's the weather in Tokyo?"

**Agent Response**:
📍 Location: Tokyo, Japan
🌡️ Temperature: 18°C (64°F)
☁️ Conditions: Partly cloudy
💧 Humidity: 65%
💨 Wind: 12 km/h Northeast
💡 Advice: Pleasant weather. Light jacket recommended.
```

## Advanced Techniques

### 1. Priority Indicators
Use formatting to show priority:
- **ALWAYS**: Must do every time
- **NEVER**: Absolute prohibition
- **Prioritize**: Do this before other things

Example:
```
- **ALWAYS** check alerts before providing weather information
- **NEVER** send emails without confirmation
- **Prioritize** safety warnings over routine information
```

### 2. Decision Trees
For complex logic, provide explicit decision trees:

```
### When to check alerts:
- ALWAYS check alerts before providing any weather information
- Display alerts prominently if severity is "severe" or "extreme"

### When to use hourly forecast:
- User asks "when will it rain/snow/stop"
- User needs timing for specific activity
- User asks about "later today" or "tonight"
```

### 3. Contextual Examples
Show how context affects responses:

```
**Context**: User previously asked about weekend plans

**User**: "What about Sunday?"

**Agent**: [Understands this refers to weather on Sunday]
```

### 4. Error Recovery
Show how to recover from errors:

```
**User**: "Weather in Springfield"

**Agent**: "I found multiple locations:
1. Springfield, IL, USA
2. Springfield, MA, USA
3. Springfield, MO, USA
Which did you mean?"
```

## Testing Your Prompts

### Manual Testing
1. Test happy path scenarios
2. Test edge cases (extreme values, missing data)
3. Test ambiguous inputs
4. Test error conditions
5. Test multi-turn conversations

### Automated Testing
Use validation tool to check:
- Role definition present
- Instructions are specific
- Tools documented with parameters
- Format specifications included
- Examples provided
- Error handling documented

### Metrics to Track
- Validation score (aim for 9+/10)
- Number of tools documented
- Number of examples (aim for 2-3 per use case)
- Number of edge cases addressed
- Specificity of instructions (avoid vague terms)

## Version Control

### When to Create New Version
- Major functionality changes
- Significant improvements from testing
- New tools added
- Format changes

### What to Document
- Version number and date
- Changes made
- Reason for changes
- Test results comparison

Example:
```
# v2 Changes (2024-12-15)
- Added hourly forecast tool
- Expanded alert handling with severity levels
- Added 3 edge case examples
- Improved decision logic for tool selection
- Test score: 8.5/10 → 10/10
```

## Summary

**Key Takeaways**:
1. Specificity beats generality
2. Examples demonstrate better than descriptions
3. Format templates ensure consistency
4. Tool documentation needs "when to use" guidance
5. Edge cases must be explicitly addressed
6. Iteration and testing are essential
7. Vague language ("nicely", "appropriately") should be eliminated

**Remember**: A good prompt is specific, clear, example-rich, and tested.
