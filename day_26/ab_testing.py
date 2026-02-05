"""Minimal A/B testing utilities for prompt versions."""

from typing import Dict, Any, List, Callable
from metrics_calculator import MetricsCalculator
from datetime import datetime


class ABTester:
    """A/B testing framework for comparing prompt versions."""
    
    def __init__(self):
        self.calculator = MetricsCalculator()
    
    def run_version(self, prompt: str, test_cases: List[Dict], 
                    evaluator: Callable) -> Dict[str, Any]:
        """Run tests for a single prompt version."""
        results = {
            "timestamp": datetime.now().isoformat(),
            "total": len(test_cases),
            "passed": 0,
            "failed": 0,
            "results": []
        }
        
        for i, test_case in enumerate(test_cases):
            eval_result = evaluator(prompt, test_case["input"], test_case["expected"])
            
            # Handle both dict and bool returns
            if isinstance(eval_result, dict):
                success = eval_result.get("success", False)
                tool_used = eval_result.get("tool_used")
                quality_score = eval_result.get("quality_score")
            else:
                success = eval_result
                tool_used = None
                quality_score = None
            
            status = "PASS" if success else "FAIL"
            results["passed" if success else "failed"] += 1
            
            result_entry = {
                "test_id": i + 1,
                "status": status,
                "input": test_case["input"]
            }
            if tool_used:
                result_entry["tool_used"] = tool_used
            if quality_score:
                result_entry["quality_score"] = quality_score
            
            results["results"].append(result_entry)
        
        return results
    
    def compare_versions(self, version_a: str, version_b: str, 
                        test_cases: List[Dict], evaluator: Callable) -> Dict[str, Any]:
        """Compare two prompt versions on same test cases."""
        # Run both versions
        results_a = self.run_version(version_a, test_cases, evaluator)
        results_b = self.run_version(version_b, test_cases, evaluator)
        
        # Calculate metrics for both
        metrics_a = self.calculator.calculate_all_metrics(results_a)
        metrics_b = self.calculator.calculate_all_metrics(results_b)
        
        # Statistical comparison
        comparison = self._statistical_comparison(metrics_a, metrics_b)
        
        return {
            "version_a": {"prompt": version_a, "results": results_a, "metrics": metrics_a},
            "version_b": {"prompt": version_b, "results": results_b, "metrics": metrics_b},
            "comparison": comparison,
            "winner": comparison["winner"]
        }
    
    def _statistical_comparison(self, metrics_a: Dict, metrics_b: Dict) -> Dict[str, Any]:
        """Perform statistical comparison between two metric sets."""
        success_diff = metrics_b["success_rate"] - metrics_a["success_rate"]
        quality_diff = metrics_b["quality_score"] - metrics_a["quality_score"]
        
        # Simple scoring: version with better overall performance wins
        score_a = metrics_a["success_rate"] + metrics_a["quality_score"]
        score_b = metrics_b["success_rate"] + metrics_b["quality_score"]
        
        # Determine winner (require >5% improvement for significance)
        if abs(score_b - score_a) < 5:
            winner = "tie"
            confidence = "low"
        elif score_b > score_a:
            winner = "version_b"
            confidence = "high" if abs(score_b - score_a) > 10 else "medium"
        else:
            winner = "version_a"
            confidence = "high" if abs(score_a - score_b) > 10 else "medium"
        
        return {
            "success_rate_diff": round(success_diff, 2),
            "quality_score_diff": round(quality_diff, 2),
            "winner": winner,
            "confidence": confidence,
            "improvement_percentage": round(abs(score_b - score_a) / score_a * 100, 2) if score_a > 0 else 0
        }
    
    def generate_comparison_report(self, comparison: Dict[str, Any], 
                                   output_file: str = None) -> str:
        """Generate formatted A/B test comparison report."""
        va = comparison["version_a"]
        vb = comparison["version_b"]
        comp = comparison["comparison"]
        
        report = f"""
=== A/B Test Comparison Report ===
Test Date: {va['results']['timestamp']}

Version A Prompt:
{va['prompt'][:100]}{'...' if len(va['prompt']) > 100 else ''}

Version B Prompt:
{vb['prompt'][:100]}{'...' if len(vb['prompt']) > 100 else ''}

=== Performance Metrics ===

Version A:
  Success Rate: {va['metrics']['success_rate']}%
  Quality Score: {va['metrics']['quality_score']}%
  Tests Passed: {va['metrics']['passed']}/{va['metrics']['total_tests']}

Version B:
  Success Rate: {vb['metrics']['success_rate']}%
  Quality Score: {vb['metrics']['quality_score']}%
  Tests Passed: {vb['metrics']['passed']}/{vb['metrics']['total_tests']}

=== Statistical Comparison ===
Success Rate Difference: {comp['success_rate_diff']:+.2f}%
Quality Score Difference: {comp['quality_score_diff']:+.2f}%
Overall Improvement: {comp['improvement_percentage']:.2f}%

Winner: {comp['winner'].upper()}
Confidence: {comp['confidence'].upper()}
"""
        
        # Tool accuracy comparison if available
        if va['metrics']['tool_accuracy'] or vb['metrics']['tool_accuracy']:
            report += "\n=== Tool Accuracy Comparison ===\n"
            all_tools = set(va['metrics']['tool_accuracy'].keys()) | set(vb['metrics']['tool_accuracy'].keys())
            for tool in all_tools:
                acc_a = va['metrics']['tool_accuracy'].get(tool, 0)
                acc_b = vb['metrics']['tool_accuracy'].get(tool, 0)
                diff = acc_b - acc_a
                report += f"{tool}: A={acc_a}% | B={acc_b}% | Diff={diff:+.2f}%\n"
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
        
        return report
