import sys
import json
import os
from typing import Dict, List, Any
from datetime import datetime

# Add parent directories to path - use absolute paths
current_file = os.path.abspath(__file__)
evaluation_dir = os.path.dirname(current_file)
day_30_dir = os.path.dirname(evaluation_dir)
project_root = os.path.dirname(day_30_dir)

sys.path.insert(0, os.path.join(project_root, 'day_29'))
sys.path.insert(0, os.path.join(project_root, 'day_28'))
sys.path.insert(0, os.path.join(project_root, 'day_27'))

from complete_agent import CompleteAgent
from metrics_calculator import MetricsCalculator


class PerformanceEvaluator:
    """Evaluate AI agent performance across multiple dimensions"""
    
    def __init__(self):
        self.agent = CompleteAgent()
        self.calculator = MetricsCalculator()
        self.results = []
    
    def load_test_cases(self, filepath: str = '../test_suite/test_cases.json') -> Dict[str, List[Dict]]:
        """Load test cases from JSON file"""
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def run_evaluation(self, max_iterations: int = 3) -> List[Dict[str, Any]]:
        """Run evaluation on all test cases"""
        print("Running performance evaluation...")
        
        test_cases = self.load_test_cases()
        results = []
        
        test_count = 0
        for category, cases in test_cases.items():
            print(f"Evaluating {category}...")
            for case in cases:
                test_count += 1
                try:
                    result = self.agent.run(case['input'], max_iterations=max_iterations)
                    result['test_id'] = case['id']
                    result['test_name'] = case['name']
                    result['category'] = category
                    results.append(result)
                except Exception as e:
                    results.append({
                        'test_id': case['id'],
                        'test_name': case['name'],
                        'category': category,
                        'status': 'error',
                        'error': str(e),
                        'iterations': 0
                    })
        
        print(f"Completed {test_count} evaluations")
        self.results = results
        return results
    
    def calculate_metrics(self, results: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate all performance metrics"""
        if results is None:
            results = self.results
        
        print("Calculating performance metrics...")
        return self.calculator.calculate_all_metrics(results)
    
    def generate_report(self, metrics: Dict[str, Any], output_file: str = 'performance_report.txt') -> str:
        """Generate human-readable performance report"""
        print("Generating performance report...")
        
        lines = [
            "=" * 70,
            "AI AGENT PERFORMANCE EVALUATION REPORT",
            "=" * 70,
            f"Generated: {metrics['timestamp']}",
            "",
            "=" * 70,
            "SUCCESS METRICS",
            "=" * 70,
            f"Overall Success Rate: {metrics['success_metrics']['overall']:.2%}",
            f"Completed Tests: {metrics['success_metrics']['completed_count']}/{metrics['success_metrics']['total_tests']}",
            f"Failed Tests: {metrics['success_metrics']['failed_count']}/{metrics['success_metrics']['total_tests']}",
            "",
            "=" * 70,
            "QUALITY METRICS",
            "=" * 70,
            f"Average Quality Score: {metrics['quality_metrics']['average_quality']:.2%}",
            f"High Quality Rate: {metrics['quality_metrics']['high_quality']:.2%}",
            f"Low Quality Rate: {metrics['quality_metrics']['low_quality']:.2%}",
            "",
            "Quality Distribution:",
            f"  High Quality: {metrics['quality_metrics']['quality_distribution']['high']} tests",
            f"  Medium Quality: {metrics['quality_metrics']['quality_distribution']['medium']} tests",
            f"  Low Quality: {metrics['quality_metrics']['quality_distribution']['low']} tests",
            "",
            "=" * 70,
            "EFFICIENCY METRICS",
            "=" * 70,
            f"Average Iterations: {metrics['efficiency_metrics']['avg_iterations']:.2f}",
            f"Min Iterations: {metrics['efficiency_metrics']['min_iterations']}",
            f"Max Iterations: {metrics['efficiency_metrics']['max_iterations']}",
            f"Total Iterations: {metrics['efficiency_metrics']['total_iterations']}",
            f"Efficiency Score: {metrics['efficiency_metrics']['efficiency_score']:.2%}",
            "",
            "Termination Reasons:",
        ]
        
        for reason, count in metrics['efficiency_metrics']['termination_reasons'].items():
            lines.append(f"  {reason}: {count}")
        
        lines.extend([
            "",
            "=" * 70,
            "TOOL USAGE METRICS",
            "=" * 70,
            f"Total Tool Calls: {metrics['tool_usage_metrics']['total_tool_calls']}",
            f"Unique Tools Used: {metrics['tool_usage_metrics']['unique_tools_used']}",
            f"Most Used Tool: {metrics['tool_usage_metrics']['most_used_tool']}",
            "",
            "Tool Call Distribution:",
        ])
        
        for tool, count in sorted(metrics['tool_usage_metrics']['tool_calls'].items(), 
                                  key=lambda x: x[1], reverse=True):
            success_rate = metrics['tool_usage_metrics']['tool_success_rates'].get(tool, 0)
            lines.append(f"  {tool}: {count} calls ({success_rate:.1%} success)")
        
        lines.extend([
            "",
            "=" * 70,
            "ERROR METRICS",
            "=" * 70,
            f"Total Errors: {metrics['error_metrics']['total_errors']}",
            f"Average Errors per Test: {metrics['error_metrics']['avg_errors_per_test']:.2f}",
            f"Error Rate: {metrics['error_metrics']['error_rate']:.2f}",
            "",
            "Errors by Phase:",
        ])
        
        for phase, count in metrics['error_metrics']['error_phases'].items():
            lines.append(f"  {phase}: {count}")
        
        lines.extend([
            "",
            "=" * 70,
            "OVERALL ASSESSMENT",
            "=" * 70,
        ])
        
        # Generate overall grade
        overall_score = (
            metrics['success_metrics']['overall'] * 0.3 +
            metrics['quality_metrics']['average_quality'] * 0.3 +
            metrics['efficiency_metrics']['efficiency_score'] * 0.2 +
            (1 - metrics['error_metrics']['error_rate'] / 10) * 0.2
        )
        
        grade = self._get_grade(overall_score)
        
        lines.extend([
            f"Overall Performance Score: {overall_score:.2%}",
            f"Grade: {grade}",
            "",
            self._get_assessment(overall_score),
            "",
            "=" * 70,
        ])
        
        report = "\n".join(lines)
        
        # Save to file
        with open(output_file, 'w') as f:
            f.write(report)
        
        print(f"Report saved to {output_file}")
        return report
    
    def generate_json_report(self, metrics: Dict[str, Any], output_file: str = 'performance_metrics.json'):
        """Generate JSON format report"""
        with open(output_file, 'w') as f:
            json.dump(metrics, f, indent=2)
        print(f"JSON metrics saved to {output_file}")
    
    def _get_grade(self, score: float) -> str:
        """Get letter grade based on score"""
        if score >= 0.9:
            return 'A (Excellent)'
        elif score >= 0.8:
            return 'B (Good)'
        elif score >= 0.7:
            return 'C (Acceptable)'
        elif score >= 0.6:
            return 'D (Poor)'
        else:
            return 'F (Failing)'
    
    def _get_assessment(self, score: float) -> str:
        """Get assessment text based on score"""
        if score >= 0.9:
            return "Assessment: Excellent performance across all metrics. Agent is production-ready."
        elif score >= 0.8:
            return "Assessment: Good performance with minor areas for improvement."
        elif score >= 0.7:
            return "Assessment: Acceptable performance but requires optimization."
        elif score >= 0.6:
            return "Assessment: Poor performance. Significant improvements needed."
        else:
            return "Assessment: Failing performance. Major overhaul required."
    
    def print_summary(self, metrics: Dict[str, Any]):
        """Print quick summary of metrics"""
        print("\n" + "=" * 50)
        print("PERFORMANCE EVALUATION SUMMARY")
        print("=" * 50)
        print(f"Success Rate: {metrics['success_metrics']['overall']:.2%}")
        print(f"Quality Score: {metrics['quality_metrics']['average_quality']:.2%}")
        print(f"Efficiency Score: {metrics['efficiency_metrics']['efficiency_score']:.2%}")
        print(f"Error Rate: {metrics['error_metrics']['error_rate']:.2f}")
        print(f"Total Tool Calls: {metrics['tool_usage_metrics']['total_tool_calls']}")
        print("=" * 50)


def main():
    """Run performance evaluation"""
    evaluator = PerformanceEvaluator()
    
    # Change to evaluation directory
    os.chdir('evaluation')
    
    # Run evaluation
    results = evaluator.run_evaluation(max_iterations=3)
    
    # Calculate metrics
    metrics = evaluator.calculate_metrics(results)
    
    # Generate reports
    evaluator.generate_report(metrics)
    evaluator.generate_json_report(metrics)
    evaluator.print_summary(metrics)
    
    return metrics


if __name__ == "__main__":
    main()
