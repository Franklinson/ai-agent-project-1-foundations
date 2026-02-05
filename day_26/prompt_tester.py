"""Minimal testing framework for evaluating agent prompts."""

import json
from typing import List, Dict, Any, Callable
from datetime import datetime


class PromptTester:
    """Framework for testing and evaluating agent prompts."""
    
    def __init__(self):
        self.results = []
    
    def load_test_cases(self, filepath: str) -> List[Dict[str, Any]]:
        """Load test cases from JSON file."""
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def run_tests(self, prompt: str, test_cases: List[Dict[str, Any]], 
                  evaluator: Callable[[str, str, Dict], bool]) -> Dict[str, Any]:
        """
        Run tests on a prompt with given test cases.
        
        Args:
            prompt: The prompt template to test
            test_cases: List of test cases with 'input' and 'expected' keys
            evaluator: Function that takes (prompt, input, expected) and returns pass/fail
            
        Returns:
            Dictionary with test results and summary
        """
        self.results = []
        passed = 0
        failed = 0
        
        for i, test_case in enumerate(test_cases):
            test_input = test_case.get('input', '')
            expected = test_case.get('expected', {})
            
            try:
                success = evaluator(prompt, test_input, expected)
                status = 'PASS' if success else 'FAIL'
                
                if success:
                    passed += 1
                else:
                    failed += 1
                    
                self.results.append({
                    'test_id': i + 1,
                    'status': status,
                    'input': test_input,
                    'expected': expected
                })
            except Exception as e:
                failed += 1
                self.results.append({
                    'test_id': i + 1,
                    'status': 'ERROR',
                    'input': test_input,
                    'error': str(e)
                })
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total': len(test_cases),
            'passed': passed,
            'failed': failed,
            'pass_rate': f"{(passed/len(test_cases)*100):.1f}%" if test_cases else "0%",
            'results': self.results
        }
    
    def generate_report(self, results: Dict[str, Any], output_file: str = None) -> str:
        """Generate a test report."""
        report = f"""
=== Prompt Test Report ===
Timestamp: {results['timestamp']}
Total Tests: {results['total']}
Passed: {results['passed']}
Failed: {results['failed']}
Pass Rate: {results['pass_rate']}

=== Test Details ===
"""
        for result in results['results']:
            report += f"\nTest #{result['test_id']}: {result['status']}\n"
            report += f"  Input: {result['input']}\n"
            if 'error' in result:
                report += f"  Error: {result['error']}\n"
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
        
        return report
