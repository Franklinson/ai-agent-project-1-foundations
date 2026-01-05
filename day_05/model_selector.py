import re
import json

class ModelSelector:
    def __init__(self):
        self.standard_model = "gpt-4"
        self.reasoning_model = "o1-preview"
        self.selection_log = []
    
    def estimate_complexity(self, prompt):
        """Estimate task complexity with refined logic"""
        prompt_lower = prompt.lower()
        
        # High complexity indicators (weight: 3)
        high_complexity = [
            r"step by step", r"solve.*equation", r"calculate.*complex",
            r"mathematical.*proof", r"logical.*reasoning", r"multi.*step"
        ]
        
        # Medium complexity indicators (weight: 2)
        medium_complexity = [
            r"analyze", r"compare.*contrast", r"explain why", r"reason",
            r"evaluate", r"assess", r"determine", r"prove"
        ]
        
        # Basic complexity indicators (weight: 1)
        basic_complexity = [
            r"calculate", r"solve", r"find", r"compute", r"what.*result"
        ]
        
        score = 0
        score += sum(3 for pattern in high_complexity if re.search(pattern, prompt_lower))
        score += sum(2 for pattern in medium_complexity if re.search(pattern, prompt_lower))
        score += sum(1 for pattern in basic_complexity if re.search(pattern, prompt_lower))
        
        # Length factor
        if len(prompt.split()) > 50:
            score += 1
            
        return score
    
    def select_model(self, prompt):
        """Select model with refined logic"""
        complexity = self.estimate_complexity(prompt)
        
        # Refined thresholds
        if complexity >= 4:
            selected = self.reasoning_model
            reason = "High complexity detected"
        elif complexity >= 2:
            selected = self.reasoning_model
            reason = "Medium complexity detected"
        else:
            selected = self.standard_model
            reason = "Low complexity, standard model sufficient"
        
        # Log selection
        self.selection_log.append({
            "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
            "complexity_score": complexity,
            "selected_model": selected,
            "reason": reason
        })
        
        return selected
    
    def get_selection_stats(self):
        """Get selection statistics"""
        if not self.selection_log:
            return {"total": 0, "standard": 0, "reasoning": 0}
        
        total = len(self.selection_log)
        reasoning_count = sum(1 for log in self.selection_log if log["selected_model"] == self.reasoning_model)
        standard_count = total - reasoning_count
        
        return {
            "total": total,
            "standard": standard_count,
            "reasoning": reasoning_count,
            "reasoning_percentage": round((reasoning_count / total) * 100, 1)
        }

def save_test_results(results, stats, selector):
    """Save test results to file"""
    output = {
        "test_results": results,
        "statistics": stats,
        "model_selection_log": selector.selection_log
    }
    
    with open("model_selector_test_results.json", "w") as f:
        json.dump(output, f, indent=2)
    
    return "model_selector_test_results.json"

if __name__ == "__main__":
    selector = ModelSelector()
    
    test_prompts = [
        "What is the weather today?",
        "Calculate the area of a circle with radius 5",
        "Solve step by step: 2x + 5 = 15",
        "Analyze and compare the economic impacts of inflation vs deflation",
        "Explain why photosynthesis is important for life on Earth",
        "Find the derivative of x^2 + 3x + 2",
        "What's the capital of France?",
        "Prove that the square root of 2 is irrational using mathematical proof",
        "Evaluate the logical reasoning behind the trolley problem in ethics",
        "How do I make coffee?"
    ]
    
    results = []
    for prompt in test_prompts:
        model = selector.select_model(prompt)
        complexity = selector.estimate_complexity(prompt)
        results.append({
            "prompt": prompt,
            "selected_model": model,
            "complexity_score": complexity
        })
    
    stats = selector.get_selection_stats()
    
    print("Model Selection Test Results:")
    print("=" * 50)
    
    for result in results:
        print(f"Prompt: {result['prompt'][:60]}...")
        print(f"Model: {result['selected_model']} (Score: {result['complexity_score']})")
        print()
    
    print(f"Statistics: {stats}")
    filename = save_test_results(results, stats, selector)
    print(f"Results saved to {filename}")