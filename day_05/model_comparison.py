from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def compare_models(prompt):
    """Compare standard and reasoning models"""
    
    # Standard model
    standard_response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Reasoning model (if available)
    reasoning_response = client.chat.completions.create(
        model="o1-preview",  # or available reasoning model
        messages=[{"role": "user", "content": prompt}]
    )
    
    return {
        "standard": standard_response.choices[0].message.content,
        "reasoning": reasoning_response.choices[0].message.content
    }

# Test with complex problem
result = compare_models("Solve step by step: If a train travels 120 miles in 2 hours, how long will it take to travel 300 miles?")
print("Standard:", result["standard"])
print("Reasoning:", result["reasoning"])
