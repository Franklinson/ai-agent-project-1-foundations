"""Minimal system for calculating evaluation metrics."""

from typing import Dict, Any, List


class MetricsCalculator:
    """Calculator for agent evaluation metrics."""
    
    def calculate_success_rate(self, results: Dict[str, Any]) -> float:
        """Calculate test success rate."""
        total = results.get('total', 0)
        if total == 0:
            return 0.0
        passed = results.get('passed', 0)
        return round((passed / total) * 100, 2)
    
    def calculate_quality_score(self, results: Dict[str, Any]) -> float:
        """Calculate quality score based on test results and errors."""
        total = results.get('total', 0)
        if total == 0:
            return 0.0
        
        passed = results.get('passed', 0)
        test_results = results.get('results', [])
        
        # Count errors separately from failures
        errors = sum(1 for r in test_results if r.get('status') == 'ERROR')
        
        # Quality score: passed tests minus error penalty
        error_penalty = errors * 0.5
        quality = ((passed - error_penalty) / total) * 100
        
        return round(max(0, quality), 2)
    
    def calculate_tool_accuracy(self, results: Dict[str, Any]) -> Dict[str, float]:
        """Calculate tool usage accuracy from test results."""
        test_results = results.get('results', [])
        
        tool_stats = {}
        for result in test_results:
            tool_used = result.get('tool_used')
            if not tool_used:
                continue
            
            if tool_used not in tool_stats:
                tool_stats[tool_used] = {'correct': 0, 'total': 0}
            
            tool_stats[tool_used]['total'] += 1
            if result.get('status') == 'PASS':
                tool_stats[tool_used]['correct'] += 1
        
        # Calculate accuracy per tool
        accuracy = {}
        for tool, stats in tool_stats.items():
            accuracy[tool] = round((stats['correct'] / stats['total']) * 100, 2)
        
        return accuracy
    
    def calculate_all_metrics(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate all metrics and return comprehensive report."""
        success_rate = self.calculate_success_rate(results)
        quality_score = self.calculate_quality_score(results)
        tool_accuracy = self.calculate_tool_accuracy(results)
        
        # Calculate average response quality if available
        test_results = results.get('results', [])
        response_scores = [r.get('quality_score', 0) for r in test_results if 'quality_score' in r]
        avg_response_quality = round(sum(response_scores) / len(response_scores), 2) if response_scores else None
        
        metrics = {
            'success_rate': success_rate,
            'quality_score': quality_score,
            'tool_accuracy': tool_accuracy,
            'total_tests': results.get('total', 0),
            'passed': results.get('passed', 0),
            'failed': results.get('failed', 0),
            'timestamp': results.get('timestamp')
        }
        
        if avg_response_quality is not None:
            metrics['avg_response_quality'] = avg_response_quality
        
        return metrics
    
    def generate_metrics_report(self, metrics: Dict[str, Any], output_file: str = None) -> str:
        """Generate formatted metrics report."""
        report = f"""
=== Evaluation Metrics Report ===
Timestamp: {metrics.get('timestamp', 'N/A')}

Overall Performance:
  Success Rate: {metrics['success_rate']}%
  Quality Score: {metrics['quality_score']}%
  Total Tests: {metrics['total_tests']}
  Passed: {metrics['passed']}
  Failed: {metrics['failed']}
"""
        
        if 'avg_response_quality' in metrics:
            report += f"  Avg Response Quality: {metrics['avg_response_quality']}\n"
        
        if metrics['tool_accuracy']:
            report += "\nTool Accuracy:\n"
            for tool, accuracy in metrics['tool_accuracy'].items():
                report += f"  {tool}: {accuracy}%\n"
        else:
            report += "\nTool Accuracy: No tool usage data\n"
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
        
        return report
