from typing import Dict, List, Any
from datetime import datetime


class MetricsCalculator:
    """Calculate performance metrics for AI agent"""
    
    def calculate_success_rate(self, results: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate success rate metrics"""
        total = len(results)
        if total == 0:
            return {'overall': 0.0, 'completed': 0.0, 'failed': 0.0}
        
        completed = sum(1 for r in results if r.get('status') == 'success')
        failed = sum(1 for r in results if r.get('status') == 'error')
        
        return {
            'overall': completed / total,
            'completed': completed / total,
            'failed': failed / total,
            'total_tests': total,
            'completed_count': completed,
            'failed_count': failed
        }
    
    def calculate_quality_score(self, results: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate quality scoring metrics"""
        if not results:
            return {'average_quality': 0.0, 'high_quality': 0.0, 'low_quality': 0.0}
        
        quality_scores = []
        high_quality = 0
        low_quality = 0
        
        for result in results:
            progress = result.get('progress', [])
            if progress:
                avg_success = sum(p.get('success_rate', 0) for p in progress) / len(progress)
                quality_scores.append(avg_success)
                
                if avg_success >= 0.8:
                    high_quality += 1
                elif avg_success < 0.5:
                    low_quality += 1
        
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
        
        return {
            'average_quality': avg_quality,
            'high_quality': high_quality / len(results),
            'low_quality': low_quality / len(results),
            'quality_distribution': {
                'high': high_quality,
                'medium': len(results) - high_quality - low_quality,
                'low': low_quality
            }
        }
    
    def calculate_efficiency_metrics(self, results: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate efficiency metrics"""
        if not results:
            return {'avg_iterations': 0.0, 'min_iterations': 0, 'max_iterations': 0}
        
        iterations = [r.get('iterations', 0) for r in results]
        
        # Calculate termination reasons
        termination_counts = {}
        for result in results:
            reason = result.get('termination_reason', 'unknown')
            termination_counts[reason] = termination_counts.get(reason, 0) + 1
        
        return {
            'avg_iterations': sum(iterations) / len(iterations),
            'min_iterations': min(iterations),
            'max_iterations': max(iterations),
            'total_iterations': sum(iterations),
            'efficiency_score': 1.0 - (sum(iterations) / (len(iterations) * 5)),  # Normalized to max 5
            'termination_reasons': termination_counts
        }
    
    def calculate_tool_usage_metrics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate tool usage metrics"""
        tool_calls = {}
        tool_success = {}
        tool_failures = {}
        
        for result in results:
            history = result.get('history', [])
            for entry in history:
                actions = entry.get('actions', [])
                for action in actions:
                    tool = action.get('tool', 'unknown')
                    status = action.get('status', 'unknown')
                    
                    tool_calls[tool] = tool_calls.get(tool, 0) + 1
                    
                    if status == 'success':
                        tool_success[tool] = tool_success.get(tool, 0) + 1
                    elif status == 'error':
                        tool_failures[tool] = tool_failures.get(tool, 0) + 1
        
        # Calculate success rates per tool
        tool_success_rates = {}
        for tool in tool_calls:
            successes = tool_success.get(tool, 0)
            tool_success_rates[tool] = successes / tool_calls[tool] if tool_calls[tool] > 0 else 0.0
        
        return {
            'total_tool_calls': sum(tool_calls.values()),
            'unique_tools_used': len(tool_calls),
            'tool_calls': tool_calls,
            'tool_success_rates': tool_success_rates,
            'most_used_tool': max(tool_calls.items(), key=lambda x: x[1])[0] if tool_calls else None,
            'tool_failures': tool_failures
        }
    
    def calculate_error_metrics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate error-related metrics"""
        total_errors = 0
        error_phases = {}
        
        for result in results:
            errors = result.get('errors', [])
            total_errors += len(errors)
            
            for error in errors:
                phase = error.get('phase', 'unknown')
                error_phases[phase] = error_phases.get(phase, 0) + 1
        
        return {
            'total_errors': total_errors,
            'avg_errors_per_test': total_errors / len(results) if results else 0.0,
            'error_phases': error_phases,
            'error_rate': total_errors / len(results) if results else 0.0
        }
    
    def calculate_all_metrics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate all metrics at once"""
        return {
            'timestamp': datetime.now().isoformat(),
            'success_metrics': self.calculate_success_rate(results),
            'quality_metrics': self.calculate_quality_score(results),
            'efficiency_metrics': self.calculate_efficiency_metrics(results),
            'tool_usage_metrics': self.calculate_tool_usage_metrics(results),
            'error_metrics': self.calculate_error_metrics(results)
        }
