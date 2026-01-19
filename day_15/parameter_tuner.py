from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ParameterTuner:
    def __init__(self):
        self.tuning_results = []
        self.use_cases = {
            "factual": {
                "temperature": 0.1,
                "top_p": 0.9,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0
            },
            "creative": {
                "temperature": 1.2,
                "top_p": 0.95,
                "frequency_penalty": 0.3,
                "presence_penalty": 0.2
            },
            "code": {
                "temperature": 0.2,
                "top_p": 0.9,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0
            },
            "conversation": {
                "temperature": 0.8,
                "top_p": 0.9,
                "frequency_penalty": 0.2,
                "presence_penalty": 0.1
            }
        }
    
    def get_params(self, use_case):
        """Get parameters for use case"""
        return self.use_cases.get(use_case, self.use_cases["conversation"])
    
    def tune_for_task(self, prompt, task_type, test_cases):
        """Tune parameters for specific task"""
        best_params = None
        best_score = 0
        self.tuning_results = []
        
        # Test parameter ranges
        for temp in [0.1, 0.5, 0.8, 1.0, 1.2]:
            for freq_penalty in [0.0, 0.2, 0.4, 0.6]:
                params = {
                    "temperature": temp,
                    "frequency_penalty": freq_penalty,
                    "top_p": 0.9
                }
                
                # Test with cases
                score = self._evaluate_params(prompt, params, test_cases)
                
                self.tuning_results.append({
                    "params": params,
                    "score": score
                })
                
                if score > best_score:
                    best_score = score
                    best_params = params
        
        return best_params, best_score
    
    def _evaluate_params(self, prompt, params, test_cases):
        """Evaluate parameter set"""
        total_score = 0
        for test_case in test_cases:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt.format(**test_case)}],
                **params
            )
            output = response.choices[0].message.content
            score = self._score_output(output, test_case.get("expected", ""))
            total_score += score
        return total_score / len(test_cases) if test_cases else 0
    
    def _score_output(self, output, expected):
        """Score output quality"""
        if not expected:
            return len(output) / 1000  # Basic length-based scoring
        similarity = sum(word in output.lower() for word in expected.lower().split())
        return similarity / len(expected.split())
    
    def save_results(self, filename="tuning_results.md"):
        """Save tuning results to markdown"""
        with open(filename, 'w') as f:
            f.write("# Parameter Tuning Results\n\n")
            f.write("## All Tested Combinations\n\n")
            
            sorted_results = sorted(self.tuning_results, key=lambda x: x['score'], reverse=True)
            
            for i, result in enumerate(sorted_results, 1):
                f.write(f"### Rank {i}\n\n")
                f.write(f"**Score:** {result['score']:.4f}\n\n")
                f.write(f"**Parameters:**\n")
                for key, val in result['params'].items():
                    f.write(f"- {key}: {val}\n")
                f.write("\n---\n\n")
        print(f"Results saved to {filename}")
    
    def generate_recommendations(self, best_params, score, filename="recommendations.md"):
        """Generate recommendations based on tuning results"""
        with open(filename, 'w') as f:
            f.write("# Parameter Tuning Recommendations\n\n")
            f.write(f"## Optimal Configuration\n\n")
            f.write(f"**Best Score Achieved:** {score:.4f}\n\n")
            f.write("**Recommended Parameters:**\n```json\n")
            f.write(json.dumps(best_params, indent=2))
            f.write("\n```\n\n")
            
            f.write("## Analysis\n\n")
            temp = best_params.get('temperature', 0.7)
            freq = best_params.get('frequency_penalty', 0.0)
            
            if temp <= 0.3:
                f.write("- **Low Temperature ({})**: Optimal for factual, deterministic outputs\n".format(temp))
            elif temp <= 0.8:
                f.write("- **Medium Temperature ({})**: Balanced creativity and consistency\n".format(temp))
            else:
                f.write("- **High Temperature ({})**: Maximizes creativity and variation\n".format(temp))
            
            if freq == 0.0:
                f.write("- **No Frequency Penalty**: Allows natural repetition\n")
            elif freq <= 0.3:
                f.write("- **Low Frequency Penalty ({})**: Slight reduction in repetition\n".format(freq))
            else:
                f.write("- **High Frequency Penalty ({})**: Strong discouragement of repetition\n".format(freq))
            
            f.write("\n## Use Case Recommendations\n\n")
            if temp <= 0.3 and freq <= 0.2:
                f.write("Best for: Technical documentation, factual Q&A, code generation\n")
            elif temp <= 0.8 and freq <= 0.3:
                f.write("Best for: General conversation, educational content, balanced tasks\n")
            else:
                f.write("Best for: Creative writing, brainstorming, diverse outputs\n")
        
        print(f"Recommendations saved to {filename}")


if __name__ == "__main__":
    tuner = ParameterTuner()
    
    # Example: Get preset parameters
    print("Factual parameters:", tuner.get_params("factual"))
    print("Creative parameters:", tuner.get_params("creative"))
    print("Code parameters:", tuner.get_params("code"))
    print("Conversation parameters:", tuner.get_params("conversation"))
    
    # Example: Tune for specific task
    test_cases = [
        {"topic": "Python", "expected": "programming language syntax variables"},
        {"topic": "JavaScript", "expected": "web development functions async"}
    ]
    
    print("\nTuning parameters...")
    best_params, score = tuner.tune_for_task(
        "Explain {topic} in simple terms",
        "educational",
        test_cases
    )
    
    print(f"\nBest parameters: {best_params}")
    print(f"Score: {score:.2f}")
    
    # Save results and recommendations
    tuner.save_results("tuning_results.md")
    tuner.generate_recommendations(best_params, score, "tuning_recommendations.md")
