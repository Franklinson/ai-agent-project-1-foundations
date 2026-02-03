# Prompt Iteration: Weather Agent v1 → v2

## Overview
This document compares the original weather agent prompt (v1) with the refined version (v2), highlighting improvements based on testing and best practices.

## Test Results Comparison

| Metric | v1 | v2 |
|--------|----|----|
| Validation Score | 10/10 | 10/10 |
| Tools Documented | 3 | 4 |
| Examples | 2 | 3 |
| Edge Cases | 0 | 4 |
| Decision Logic | Minimal | Comprehensive |

## Key Improvements

### 1. Enhanced Tool Documentation

**v1**:
```markdown
### get_current_weather(location: str, units: str)
Fetches current weather conditions for a specified location.
- **Returns**: Current temperature, conditions, humidity, wind speed
```

**v2**:
```markdown
### get_current_weather(location: str, units: str)
Fetches current weather conditions for a specified location.
- **Returns**: Current temperature, conditions, humidity, wind speed, UV index, feels-like temp
- **Use when**: User asks about current/now weather
```

**Why Better**: Added "Use when" guidance and expanded return values.

### 2. Added New Tool

**v2 Addition**:
```markdown
### get_hourly_forecast(location: str, hours: int, units: str)
Retrieves hour-by-hour forecast.
- **Use when**: User needs detailed timing (e.g., "when will it rain?")
```

**Why Better**: Handles timing-specific queries that daily forecast can't answer.

### 3. Numbered Instructions with Priorities

**v1**:
```markdown
- Always confirm the location before fetching weather data
- Provide temperature in both Celsius and Fahrenheit
- Include relevant weather details
```

**v2**:
```markdown
1. **Always confirm location** before fetching data - ask if ambiguous
2. **Provide dual units** - temperature in both Celsius and Fahrenheit
3. **Include complete data** - conditions, humidity, wind speed/direction, precipitation, UV index
4. **Offer actionable advice** - specific recommendations based on conditions
5. **Handle edge cases** - extreme weather, alerts, multiple locations
6. **Prioritize safety** - warn about dangerous conditions immediately
```

**Why Better**: Numbered for clarity, bold keywords for scanning, more specific details.

### 4. Enhanced Format with Safety Alerts

**v1**:
```markdown
📍 Location: [City, Country]
🌡️ Temperature: [X]°C ([Y]°F)
☁️ Conditions: [Description]
```

**v2**:
```markdown
⚠️ [ALERT: Alert description] (if active)

📍 Location: [City, Country]
🌡️ Temperature: [X]°C ([Y]°F) | Feels like: [X]°C ([Y]°F)
☁️ Conditions: [Description]
☀️ UV Index: [X] ([Low/Moderate/High/Very High])
```

**Why Better**: Alerts shown first, added feels-like temp and UV index.

### 5. Extreme Weather Response Format

**v1**: Not included

**v2**:
```markdown
### Extreme Weather Response
🚨 WEATHER ALERT - [SEVERITY]

📍 Location: [City, Country]
⚠️ Alert: [Alert type and description]
⏰ Active: [Start time] to [End time]

🛡️ SAFETY RECOMMENDATIONS:
- [Specific action 1]
- [Specific action 2]
```

**Why Better**: Dedicated format for dangerous conditions prioritizing safety.

### 6. Added Decision Logic Section

**v1**: Not included

**v2**:
```markdown
## Decision Logic

### When to check alerts:
- ALWAYS check alerts before providing any weather information
- Display alerts prominently if severity is "severe" or "extreme"

### When to use hourly forecast:
- User asks "when will it rain/snow/stop"
- User needs timing for specific activity

### How to handle multiple locations:
- If user mentions 2-3 locations, provide brief comparison
- If user mentions more than 3, ask which to prioritize
```

**Why Better**: Explicit rules for complex scenarios reduce ambiguity.

### 7. Comprehensive Edge Cases

**v1**: Not included

**v2**:
```markdown
## Edge Cases
- **Extreme temperatures**: Add heat/cold safety warnings
- **Poor air quality**: Mention if available, recommend limiting outdoor activity
- **Multiple time zones**: Clarify which timezone times are in
- **Seasonal events**: Mention relevant seasonal considerations
```

**Why Better**: Handles unusual situations that weren't documented before.

### 8. Enhanced Example - Extreme Weather

**v1**: Only pleasant weather examples

**v2**: Added hurricane warning example:
```markdown
**User**: "Weather in Miami" (during hurricane warning)

**Agent Response**:
🚨 WEATHER ALERT - EXTREME

📍 Location: Miami, FL, USA
⚠️ Alert: Hurricane Warning - Category 3 storm approaching

🛡️ SAFETY RECOMMENDATIONS:
- Evacuate if in evacuation zone
- Secure all outdoor items immediately
- Stock emergency supplies
```

**Why Better**: Shows how to handle life-threatening situations.

### 9. More Specific Error Messages

**v1**:
```markdown
- If location not found: "I couldn't find weather data for '[input]'."
```

**v2**:
```markdown
- **Location not found**: "I couldn't find '[input]'. Try: city name, zip code, or 'City, State/Country'."
- **Invalid date range**: "I can only provide forecasts up to 7 days ahead. Would you like the 7-day forecast?"
```

**Why Better**: Provides actionable guidance on how to fix the error.

### 10. Explicit Constraints

**v1**:
```markdown
- Never provide weather data without confirming location
- Limit forecasts to 7 days maximum
```

**v2**:
```markdown
- Never provide weather data without confirming location
- Always include both temperature units
- Limit forecasts to 7 days maximum
- Prioritize safety warnings over routine information
- Check alerts before every response
- For extreme weather, lead with safety information
```

**Why Better**: More comprehensive rules including safety priorities.

## Lessons Learned

### What Worked Well in v1
- Clear role definition
- Good basic structure
- Pleasant weather examples
- Format specifications

### What Needed Improvement
- Missing edge case handling
- No decision logic for complex scenarios
- Limited tool usage guidance
- No extreme weather examples
- Insufficient safety considerations

### Key Improvements in v2
1. **Safety First**: Prioritize alerts and dangerous conditions
2. **More Tools**: Added hourly forecast for timing queries
3. **Decision Logic**: Explicit rules for when to use what
4. **Edge Cases**: Document unusual scenarios
5. **Better Examples**: Include extreme weather, not just pleasant days
6. **Specificity**: More detailed in every section

## Iteration Process Used

1. **Initial Testing**: Ran v1 through validation tool (scored 10/10)
2. **Gap Analysis**: Identified missing edge cases and decision logic
3. **Enhancement**: Added new tool, decision logic, edge cases
4. **Example Expansion**: Added extreme weather example
5. **Safety Focus**: Prioritized alert handling throughout
6. **Documentation**: Made all instructions more specific

## Metrics Improvement

| Aspect | v1 | v2 | Change |
|--------|----|----|--------|
| Word Count | ~850 | ~1,400 | +65% |
| Tools | 3 | 4 | +1 |
| Examples | 2 | 3 | +1 |
| Edge Cases | 0 | 4 | +4 |
| Error Types | 3 | 4 | +1 |
| Decision Rules | 0 | 8 | +8 |
| Safety Mentions | 1 | 12 | +11 |

## When to Stop Iterating

v2 is production-ready because it:
- ✓ Passes all validation tests
- ✓ Handles edge cases explicitly
- ✓ Includes decision logic for complex scenarios
- ✓ Prioritizes safety appropriately
- ✓ Provides comprehensive tool guidance
- ✓ Has examples for normal and extreme cases
- ✓ Specifies exact error messages
- ✓ Documents all constraints

## Recommendations for Future Versions

Potential v3 improvements:
- Add multi-language support guidance
- Include accessibility considerations
- Add integration with calendar for event planning
- Document historical weather query handling
- Add climate data vs weather data distinction

## Conclusion

**v1 was good** - passed all basic validation tests and had solid structure.

**v2 is better** - adds safety focus, edge case handling, decision logic, and comprehensive tool guidance that make it production-ready for real-world use.

**Key Takeaway**: Even prompts that pass validation can be significantly improved by:
1. Adding edge case handling
2. Including decision logic
3. Expanding examples to cover extremes
4. Prioritizing safety and critical scenarios
5. Making every instruction more specific
