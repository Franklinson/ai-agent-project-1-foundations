#!/usr/bin/env python3
"""
Performance Evaluation Runner

Run from day_30 directory to evaluate agent performance.
"""

import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.getcwd(), 'day_29'))
sys.path.insert(0, os.path.join(os.getcwd(), 'day_28'))
sys.path.insert(0, os.path.join(os.getcwd(), 'day_27'))
sys.path.insert(0, os.path.join(os.getcwd(), 'evaluation'))

# Change to parent directory if needed
if os.path.basename(os.getcwd()) != 'day_30':
    parent = os.path.dirname(os.path.abspath(__file__))
    os.chdir(parent)
    sys.path.insert(0, os.path.join(parent, 'day_29'))
    sys.path.insert(0, os.path.join(parent, 'day_28'))
    sys.path.insert(0, os.path.join(parent, 'day_27'))

from evaluation.performance_evaluator import PerformanceEvaluator

def main():
    """Run performance evaluation"""
    print("Initializing Performance Evaluator...")
    evaluator = PerformanceEvaluator()
    
    # Change to evaluation directory for output
    eval_dir = os.path.join(os.getcwd(), 'evaluation')
    os.chdir(eval_dir)
    
    # Run evaluation
    results = evaluator.run_evaluation(max_iterations=3)
    
    # Calculate metrics
    metrics = evaluator.calculate_metrics(results)
    
    # Generate reports
    evaluator.generate_report(metrics)
    evaluator.generate_json_report(metrics)
    evaluator.print_summary(metrics)
    
    print("\n✅ Performance evaluation completed successfully!")
    return metrics

if __name__ == "__main__":
    main()
