from openai import OpenAI
from cost_calculator import CostCalculator
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def interactive_ai_test():
    """Interactive test with user prompts, AI responses, and cost tracking"""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    calc = CostCalculator()
    
    print("=== AI Cost Tracking Test ===")
    print("Enter prompts (type 'quit' to exit)\n")
    
    conversations = []
    
    while True:
        # Get user input
        prompt = input("Your prompt: ").strip()
        
        if prompt.lower() == 'quit':
            break
        
        if not prompt:
            continue
        
        # Get AI response
        print("Generating response...")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        
        output = response.choices[0].message.content
        
        # Calculate cost
        cost = calc.calculate_cost(prompt, output, "gpt-4")
        
        # Display results
        print(f"\nAI Response: {output}")
        print(f"Cost: ${cost:.4f}\n")
        print("-" * 50)
        
        # Store conversation
        conversations.append({
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "response": output,
            "cost": cost
        })
    
    # Save to file
    output_data = {
        "conversations": conversations,
        "statistics": calc.get_stats(),
        "detailed_requests": calc.requests
    }
    
    filename = f"ai_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    # Display summary
    stats = calc.get_stats()
    print("\n=== Session Summary ===")
    print(f"Total prompts: {stats['total_requests']}")
    print(f"Total cost: ${stats['total_cost']:.4f}")
    print(f"Average cost per prompt: ${stats['avg_cost']:.4f}")
    print(f"\nResults saved to: {filename}")

if __name__ == "__main__":
    interactive_ai_test()
