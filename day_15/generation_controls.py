from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class GenerationControlTester:
    def __init__(self):
        self.results = []
    
    def test_parameters(self, prompt, parameter_sets):
        """Test multiple parameter combinations"""
        for params in parameter_sets:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                **params
            )
            
            result = {
                "parameters": params,
                "output": response.choices[0].message.content,
                "tokens": response.usage.total_tokens
            }
            self.results.append(result)
        
        return self.results
    
    def compare_outputs(self):
        """Compare outputs from different parameters"""
        for i, result in enumerate(self.results):
            print(f"\n=== Test {i+1} ===")
            print(f"Parameters: {result['parameters']}")
            print(f"Output: {result['output'][:200]}...")
            print(f"Tokens: {result['tokens']}")
    
    def save_to_json(self, filename="results.json"):
        """Save results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nResults saved to {filename}")
    
    def save_to_markdown(self, filename="results.md"):
        """Save results to Markdown file"""
        with open(filename, 'w') as f:
            f.write("# Generation Control Test Results\n\n")
            for i, result in enumerate(self.results, 1):
                f.write(f"## Test {i}\n\n")
                f.write(f"**Parameters:** `{result['parameters']}`\n\n")
                f.write(f"**Tokens Used:** {result['tokens']}\n\n")
                f.write(f"**Output:**\n\n{result['output']}\n\n")
                f.write("---\n\n")
        print(f"Markdown report saved to {filename}")

# Test different temperature values
tester = GenerationControlTester()

parameter_sets = [
    {"temperature": 0.1},
    {"temperature": 0.7},
    {"temperature": 1.0},
    {"temperature": 1.5}
]

results = tester.test_parameters(
    "Write a creative story about a robot",
    parameter_sets
)

tester.compare_outputs()
tester.save_to_json("generation_results.json")
tester.save_to_markdown("generation_results.md")
