"""Minimal workflow system for prompt iteration."""

from typing import Dict, Any, List, Callable, Optional
from datetime import datetime
from metrics_calculator import MetricsCalculator
from ab_testing import ABTester
import json


class IterationWorkflow:
    """Automated workflow for iterative prompt refinement."""
    
    def __init__(self):
        self.calculator = MetricsCalculator()
        self.ab_tester = ABTester()
        self.versions = []
        self.iteration_history = []
    
    def run_iteration(self, prompt: str, test_cases: List[Dict], 
                     evaluator: Callable, version_name: str = None) -> Dict[str, Any]:
        """Run single iteration: test, evaluate, analyze."""
        iteration_num = len(self.iteration_history) + 1
        version_name = version_name or f"v{iteration_num}"
        
        # Test
        results = self.ab_tester.run_version(prompt, test_cases, evaluator)
        
        # Evaluate
        metrics = self.calculator.calculate_all_metrics(results)
        
        # Analyze
        analysis = self._analyze_results(metrics, results)
        
        # Track version
        iteration = {
            "iteration": iteration_num,
            "version": version_name,
            "prompt": prompt,
            "timestamp": datetime.now().isoformat(),
            "results": results,
            "metrics": metrics,
            "analysis": analysis
        }
        
        self.iteration_history.append(iteration)
        self.versions.append({"name": version_name, "prompt": prompt})
        
        return iteration
    
    def run_workflow(self, initial_prompt: str, test_cases: List[Dict],
                    evaluator: Callable, refiner: Callable, 
                    max_iterations: int = 5, target_score: float = 95.0) -> Dict[str, Any]:
        """Run complete iteration workflow with auto-refinement."""
        print(f"Starting iteration workflow (max {max_iterations} iterations, target {target_score}%)\n")
        
        current_prompt = initial_prompt
        
        for i in range(max_iterations):
            print(f"=== Iteration {i+1} ===")
            
            # Run iteration
            iteration = self.run_iteration(
                current_prompt, test_cases, evaluator, f"v{i+1}"
            )
            
            # Check if target reached
            score = iteration["metrics"]["success_rate"]
            quality = iteration["metrics"]["quality_score"]
            combined = (score + quality) / 2
            
            print(f"Success Rate: {score}%")
            print(f"Quality Score: {quality}%")
            print(f"Combined Score: {combined:.2f}%")
            
            if combined >= target_score:
                print(f"\n✓ Target reached! Stopping at iteration {i+1}")
                break
            
            # Refine for next iteration
            if i < max_iterations - 1:
                print(f"Refining prompt for next iteration...")
                current_prompt = refiner(current_prompt, iteration)
                print()
        
        # Generate final report
        workflow_summary = self._generate_workflow_summary()
        
        return workflow_summary
    
    def _analyze_results(self, metrics: Dict, results: Dict) -> Dict[str, Any]:
        """Analyze results and provide insights."""
        analysis = {
            "performance": "excellent" if metrics["success_rate"] >= 90 else
                          "good" if metrics["success_rate"] >= 75 else
                          "needs_improvement",
            "issues": []
        }
        
        # Identify issues
        if metrics["success_rate"] < 100:
            failed_count = metrics["failed"]
            analysis["issues"].append(f"{failed_count} test(s) failed")
        
        if metrics["quality_score"] < metrics["success_rate"]:
            analysis["issues"].append("Quality below success rate (errors detected)")
        
        # Tool accuracy issues
        for tool, accuracy in metrics.get("tool_accuracy", {}).items():
            if accuracy < 80:
                analysis["issues"].append(f"{tool} accuracy low ({accuracy}%)")
        
        return analysis
    
    def compare_iterations(self, iteration_a: int, iteration_b: int) -> Dict[str, Any]:
        """Compare two iterations."""
        if iteration_a < 1 or iteration_b < 1:
            raise ValueError("Iteration numbers must be >= 1")
        if iteration_a > len(self.iteration_history) or iteration_b > len(self.iteration_history):
            raise ValueError("Iteration number out of range")
        
        iter_a = self.iteration_history[iteration_a - 1]
        iter_b = self.iteration_history[iteration_b - 1]
        
        metrics_a = iter_a["metrics"]
        metrics_b = iter_b["metrics"]
        
        return {
            "iteration_a": iteration_a,
            "iteration_b": iteration_b,
            "success_rate_change": metrics_b["success_rate"] - metrics_a["success_rate"],
            "quality_score_change": metrics_b["quality_score"] - metrics_a["quality_score"],
            "improvement": metrics_b["success_rate"] > metrics_a["success_rate"]
        }
    
    def get_best_version(self) -> Dict[str, Any]:
        """Get the best performing version."""
        if not self.iteration_history:
            return None
        
        best = max(self.iteration_history, 
                  key=lambda x: x["metrics"]["success_rate"] + x["metrics"]["quality_score"])
        
        return {
            "iteration": best["iteration"],
            "version": best["version"],
            "prompt": best["prompt"],
            "success_rate": best["metrics"]["success_rate"],
            "quality_score": best["metrics"]["quality_score"]
        }
    
    def _generate_workflow_summary(self) -> Dict[str, Any]:
        """Generate summary of entire workflow."""
        if not self.iteration_history:
            return {"error": "No iterations run"}
        
        best = self.get_best_version()
        first = self.iteration_history[0]
        last = self.iteration_history[-1]
        
        improvement = (
            (last["metrics"]["success_rate"] - first["metrics"]["success_rate"]) +
            (last["metrics"]["quality_score"] - first["metrics"]["quality_score"])
        ) / 2
        
        return {
            "total_iterations": len(self.iteration_history),
            "best_version": best,
            "first_iteration": {
                "success_rate": first["metrics"]["success_rate"],
                "quality_score": first["metrics"]["quality_score"]
            },
            "last_iteration": {
                "success_rate": last["metrics"]["success_rate"],
                "quality_score": last["metrics"]["quality_score"]
            },
            "overall_improvement": round(improvement, 2),
            "iterations": self.iteration_history
        }
    
    def generate_iteration_report(self, output_file: str = None) -> str:
        """Generate formatted iteration report."""
        summary = self._generate_workflow_summary()
        
        if "error" in summary:
            return summary["error"]
        
        report = f"""
=== Prompt Iteration Workflow Report ===

Total Iterations: {summary['total_iterations']}
Overall Improvement: {summary['overall_improvement']:+.2f}%

=== Best Version ===
Iteration: {summary['best_version']['iteration']} ({summary['best_version']['version']})
Success Rate: {summary['best_version']['success_rate']}%
Quality Score: {summary['best_version']['quality_score']}%
Prompt: {summary['best_version']['prompt'][:100]}...

=== Progress ===
First Iteration:
  Success Rate: {summary['first_iteration']['success_rate']}%
  Quality Score: {summary['first_iteration']['quality_score']}%

Last Iteration:
  Success Rate: {summary['last_iteration']['success_rate']}%
  Quality Score: {summary['last_iteration']['quality_score']}%

=== Iteration Details ===
"""
        
        for iteration in summary['iterations']:
            report += f"\nIteration {iteration['iteration']} ({iteration['version']}):\n"
            report += f"  Success: {iteration['metrics']['success_rate']}% | "
            report += f"Quality: {iteration['metrics']['quality_score']}% | "
            report += f"Performance: {iteration['analysis']['performance']}\n"
            if iteration['analysis']['issues']:
                report += f"  Issues: {', '.join(iteration['analysis']['issues'])}\n"
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
        
        return report
    
    def save_workflow(self, filepath: str):
        """Save complete workflow to JSON."""
        summary = self._generate_workflow_summary()
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2)
