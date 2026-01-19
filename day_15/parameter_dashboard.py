from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ParameterDashboard:
    def __init__(self):
        self.test_results = []
    
    def add_test_result(self, params, output, metrics):
        """Add test result"""
        self.test_results.append({
            "params": params,
            "output": output,
            "metrics": metrics
        })
    
    def run_comparison(self, prompt, param_sets):
        """Run comparison across multiple parameter sets"""
        for params in param_sets:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                **params
            )
            output = response.choices[0].message.content
            metrics = {
                "tokens": response.usage.total_tokens,
                "length": len(output),
                "words": len(output.split())
            }
            self.add_test_result(params, output, metrics)
    
    def generate_report(self):
        """Generate parameter comparison report"""
        report = "# Generation Parameter Comparison Report\n\n"
        
        for i, result in enumerate(self.test_results):
            report += f"## Test {i+1}\n\n"
            report += f"**Parameters:**\n"
            for key, value in result["params"].items():
                report += f"- {key}: {value}\n"
            report += f"\n**Output:**\n{result['output'][:500]}...\n\n"
            report += f"**Metrics:**\n"
            for key, value in result["metrics"].items():
                report += f"- {key}: {value}\n\n"
            report += "---\n\n"
        
        return report
    
    def save_report(self, filename="parameter_report.md"):
        """Save report to file"""
        report = self.generate_report()
        with open(filename, "w") as f:
            f.write(report)
        print(f"Report saved to {filename}")
    
    def save_json(self, filename="parameter_results.json"):
        """Save results as JSON"""
        with open(filename, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        print(f"JSON saved to {filename}")


if __name__ == "__main__":
    dashboard = ParameterDashboard()
    
    # Test different parameter combinations
    param_sets = [
        {"temperature": 0.1, "max_tokens": 150},
        {"temperature": 0.7, "max_tokens": 150},
        {"temperature": 1.2, "max_tokens": 150, "frequency_penalty": 0.3}
    ]
    
    print("Running parameter comparison...")
    dashboard.run_comparison(
        "Write a short paragraph about artificial intelligence",
        param_sets
    )
    
    # Save results
    dashboard.save_report("day_15/parameter_dashboard_report.md")
    dashboard.save_json("day_15/parameter_dashboard_results.json")
