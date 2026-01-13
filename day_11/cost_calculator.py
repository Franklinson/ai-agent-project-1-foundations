import tiktoken

class CostCalculator:
    def __init__(self):
        self.pricing = {
            "gpt-4": {"input": 0.01, "output": 0.03},
            "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015}
        }
        self.total_cost = 0
        self.requests = []
    
    def count_tokens(self, text, model="gpt-4"):
        """Count tokens"""
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    
    def calculate_cost(self, input_text, output_text, model="gpt-4"):
        """Calculate request cost"""
        input_tokens = self.count_tokens(input_text, model)
        output_tokens = self.count_tokens(output_text, model)
        
        input_cost = (input_tokens / 1000) * self.pricing[model]["input"]
        output_cost = (output_tokens / 1000) * self.pricing[model]["output"]
        total = input_cost + output_cost
        
        self.total_cost += total
        self.requests.append({
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": total,
            "model": model
        })
        
        return total
    
    def get_stats(self):
        """Get cost statistics"""
        return {
            "total_cost": self.total_cost,
            "total_requests": len(self.requests),
            "avg_cost": self.total_cost / len(self.requests) if self.requests else 0
        }

# Test
calc = CostCalculator()
cost = calc.calculate_cost(
    "What is AI?",
    "AI is artificial intelligence...",
    "gpt-4"
)
print(f"Cost: ${cost:.4f}")
print(calc.get_stats())
