def mock_llm(prompt):
    """Mock LLM for testing"""
    if "positive" in prompt.lower() or "love" in prompt.lower():
        return "positive"
    elif "negative" in prompt.lower() or "hate" in prompt.lower():
        return "negative"
    return "neutral"

def evaluate(response, expected):
    """Score response accuracy"""
    return 1.0 if expected.lower() in response.lower() else 0.0

# Prompt variations for sentiment analysis
variations = {
    "direct": "Classify sentiment: {text}",
    "options": "Classify as positive, negative, or neutral: {text}",
    "role": "As an expert, classify sentiment: {text}",
    "examples": """Examples:
'I love it' -> positive
'I hate it' -> negative

Classify: {text}"""
}

# Test cases
test_cases = [
    {"inputs": {"text": "I love this product!"}, "expected": "positive"},
    {"inputs": {"text": "This is terrible"}, "expected": "negative"},
    {"inputs": {"text": "It's okay"}, "expected": "neutral"}
]

# Compare performance
results = {}
for name, template in variations.items():
    scores = []
    for case in test_cases:
        prompt = template.format(**case["inputs"])
        response = mock_llm(prompt)
        score = evaluate(response, case["expected"])
        scores.append(score)
    
    results[name] = {
        "avg_score": sum(scores) / len(scores),
        "scores": scores
    }

# Analyze results
analysis = {
    "best_approach": max(results.items(), key=lambda x: x[1]['avg_score'])[0],
    "worst_approach": min(results.items(), key=lambda x: x[1]['avg_score'])[0],
    "performance_gap": max(results.values(), key=lambda x: x['avg_score'])['avg_score'] - 
                      min(results.values(), key=lambda x: x['avg_score'])['avg_score']
}

# Document findings
print("Results Analysis:")
for name, metrics in sorted(results.items(), key=lambda x: x[1]["avg_score"], reverse=True):
    print(f"{name}: {metrics['avg_score']:.2f}")

print(f"\nBest: {analysis['best_approach']} (gap: {analysis['performance_gap']:.2f})")
print(f"Recommendation: Use '{analysis['best_approach']}' for highest accuracy")