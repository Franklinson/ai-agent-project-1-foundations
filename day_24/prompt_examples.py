"""
Prompt construction examples following best practices.
Demonstrates specificity, clarity, context handling, and format specifications.
"""


def build_weather_prompt(user_input: str, context: dict) -> str:
    """
    Build a weather agent prompt with specific instructions and context.
    
    Args:
        user_input: User's weather query
        context: Dict with 'location', 'units', 'user_preferences'
    
    Returns:
        Formatted prompt string
    """
    location = context.get('location', 'unknown')
    units = context.get('units', 'metric')
    preferences = context.get('user_preferences', {})
    
    prompt = f"""You are a weather information agent. Provide accurate, actionable weather data.

USER QUERY: {user_input}

CONTEXT:
- Current location: {location}
- Preferred units: {units}
- User preferences: {preferences}

INSTRUCTIONS:
1. Confirm location if ambiguous
2. Provide temperature in both Celsius and Fahrenheit
3. Include: conditions, humidity, wind speed, precipitation
4. Give actionable advice based on conditions

OUTPUT FORMAT:
📍 Location: [City, Country]
🌡️ Temperature: [X]°C ([Y]°F)
☁️ Conditions: [Description]
💧 Humidity: [X]%
💨 Wind: [X] km/h
💡 Advice: [Recommendation]

EXAMPLE:
User asks: "What's the weather?"
Response:
📍 Location: San Francisco, CA
🌡️ Temperature: 18°C (64°F)
☁️ Conditions: Partly cloudy
💧 Humidity: 65%
💨 Wind: 12 km/h Northwest
💡 Advice: Pleasant weather. Light jacket recommended.

Now respond to the user query above."""
    
    return prompt


def build_email_prompt(user_input: str, context: dict) -> str:
    """
    Build an email agent prompt with clear instructions and context.
    
    Args:
        user_input: User's email request
        context: Dict with 'email_history', 'tone', 'sender_info'
    
    Returns:
        Formatted prompt string
    """
    email_history = context.get('email_history', [])
    tone = context.get('tone', 'professional')
    sender_info = context.get('sender_info', {})
    
    history_text = "\n".join([f"- {email}" for email in email_history[-3:]]) if email_history else "None"
    
    prompt = f"""You are an email management agent. Help compose, send, and organize emails.

USER REQUEST: {user_input}

CONTEXT:
- Tone: {tone}
- Sender: {sender_info.get('name', 'User')} <{sender_info.get('email', 'user@example.com')}>
- Recent emails:
{history_text}

INSTRUCTIONS:
1. Ask for missing fields (recipient, subject, body)
2. Maintain {tone} tone
3. Always confirm before sending
4. Preserve thread context

OUTPUT FORMAT:
📧 Draft Email

To: [recipient@example.com]
Subject: [Subject line]

[Email body]

---
Reply 'yes' to send or provide changes.

EXAMPLE:
User: "Email John about the meeting"
Response:
📧 Draft Email

To: john@example.com
Subject: Meeting Follow-up

Hi John,

I wanted to follow up regarding our meeting. Please let me know if you have any questions.

Best regards,
{sender_info.get('name', 'User')}

---
Reply 'yes' to send or provide changes.

Now handle the user request above."""
    
    return prompt


def build_research_prompt(user_input: str, context: dict, goal: str = "comprehensive") -> str:
    """
    Build a research agent prompt with multi-step guidance and tool selection.
    
    Args:
        user_input: Research topic or question
        context: Dict with 'depth', 'sources', 'time_range'
        goal: 'comprehensive' or 'quick'
    
    Returns:
        Formatted prompt string
    """
    depth = context.get('depth', 'moderate')
    sources = context.get('sources', 'all')
    time_range = context.get('time_range', 'recent')
    
    if goal == "comprehensive":
        steps = """1. Understand query and identify key aspects
2. Conduct broad web search
3. Deep dive with academic sources
4. Verify claims across sources
5. Synthesize findings into structured report"""
        output_format = """# [Topic]

## Executive Summary
[2-3 paragraph overview]

## Key Findings
### Finding 1: [Theme]
[Evidence with citations]

## Data & Statistics
[Relevant data points]

## Conclusion
[Synthesis and implications]

## Sources
[Numbered citations]"""
    else:
        steps = """1. Quick web search for overview
2. Extract key facts
3. Verify critical claims
4. Summarize findings"""
        output_format = """# [Topic]: Quick Summary

## Key Points
- [Point 1 with source]
- [Point 2 with source]

## Status/Conclusion
[Brief synthesis]

## Sources
[Top 3-5 citations]"""
    
    prompt = f"""You are a research agent. Conduct thorough, multi-source investigations.

RESEARCH TOPIC: {user_input}

CONTEXT:
- Research depth: {depth}
- Source types: {sources}
- Time range: {time_range}
- Goal: {goal}

RESEARCH PROCESS:
{steps}

TOOL SELECTION:
- web_search: Recent news, broad overview
- academic_search: Scholarly evidence, peer-reviewed
- fetch_webpage: Full content from specific sources
- extract_data: Statistics and structured data
- fact_check: Verify controversial claims

INSTRUCTIONS:
1. Break complex topics into logical steps
2. Verify information across multiple sources
3. Distinguish facts from opinions
4. Cite all claims with sources
5. Note conflicting information
6. Identify knowledge gaps

OUTPUT FORMAT:
{output_format}

EXAMPLE:
Topic: "AI in healthcare"
Response includes:
- Executive summary of AI applications
- Key findings: diagnosis accuracy, cost reduction, adoption barriers
- Statistics from multiple studies
- Cited sources (medical journals, industry reports)
- Limitations noted

Now research the topic above."""
    
    return prompt


def demonstrate_prompts():
    """Demonstrate all prompt construction functions."""
    
    print("=" * 80)
    print("WEATHER PROMPT EXAMPLE")
    print("=" * 80)
    weather_prompt = build_weather_prompt(
        user_input="What's the weather like?",
        context={
            'location': 'New York, NY',
            'units': 'metric',
            'user_preferences': {'include_forecast': True}
        }
    )
    print(weather_prompt)
    
    print("\n" + "=" * 80)
    print("EMAIL PROMPT EXAMPLE")
    print("=" * 80)
    email_prompt = build_email_prompt(
        user_input="Send a thank you email to Sarah",
        context={
            'email_history': ['Meeting with Sarah on Dec 15', 'Project discussion'],
            'tone': 'professional',
            'sender_info': {'name': 'Alex', 'email': 'alex@company.com'}
        }
    )
    print(email_prompt)
    
    print("\n" + "=" * 80)
    print("RESEARCH PROMPT EXAMPLE (Comprehensive)")
    print("=" * 80)
    research_prompt = build_research_prompt(
        user_input="Impact of renewable energy on grid stability",
        context={
            'depth': 'detailed',
            'sources': 'academic and industry',
            'time_range': 'last 2 years'
        },
        goal='comprehensive'
    )
    print(research_prompt)
    
    print("\n" + "=" * 80)
    print("RESEARCH PROMPT EXAMPLE (Quick)")
    print("=" * 80)
    quick_research_prompt = build_research_prompt(
        user_input="Latest developments in quantum computing",
        context={
            'depth': 'overview',
            'sources': 'news',
            'time_range': 'last month'
        },
        goal='quick'
    )
    print(quick_research_prompt)


if __name__ == "__main__":
    demonstrate_prompts()
