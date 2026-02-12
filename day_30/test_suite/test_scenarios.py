import sys
import json
import os
from typing import Dict, List, Any
from datetime import datetime

# Add paths for agent modules
sys.path.append('../day_29')
sys.path.append('../day_28')
sys.path.append('../day_27')

from complete_agent import CompleteAgent
from perception import PerceptionModule
from reasoning import ReasoningModule
from action import ActionModule
from observation import ObservationModule


class TestScenarios:
    """Comprehensive test scenarios for AI agent"""
    
    def __init__(self):
        self.agent = CompleteAgent()
        self.perception = PerceptionModule()
        self.reasoning = ReasoningModule()
        self.action = ActionModule()
        self.observation = ObservationModule()
        self.results = []
        
    def load_test_cases(self) -> Dict[str, List[Dict]]:
        """Load test cases from JSON file"""
        with open('test_cases.json', 'r') as f:
            return json.load(f)
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all test scenarios"""
        print("Starting comprehensive agent test suite...")
        
        test_cases = self.load_test_cases()
        results = {
            'timestamp': datetime.now().isoformat(),
            'perception_tests': self.test_perception_accuracy(test_cases),
            'reasoning_tests': self.test_reasoning_quality(test_cases),
            'tool_tests': self.test_tool_usage(test_cases),
            'observation_tests': self.test_observation_accuracy(test_cases),
            'complete_loop_tests': self.test_complete_loop_operation(test_cases),
            'summary': {}
        }
        
        results['summary'] = self._generate_summary(results)
        return results
    
    def test_perception_accuracy(self, test_cases: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Test perception module accuracy"""
        print("Testing perception accuracy...")
        
        results = {'passed': 0, 'failed': 0, 'details': []}
        
        for category, cases in test_cases.items():
            for case in cases:
                try:
                    perceived = self.perception.process(case['input'])
                    
                    # Check intent accuracy
                    intent_correct = perceived['intent'] == case['expected_intent']
                    
                    # Check entity extraction
                    has_entities = len(perceived['entities']) > 0
                    expected_entities = 'entity_processor' in case.get('expected_tools', [])
                    entities_correct = has_entities == expected_entities
                    
                    passed = intent_correct and entities_correct
                    
                    if passed:
                        results['passed'] += 1
                    else:
                        results['failed'] += 1
                    
                    results['details'].append({
                        'case_id': case['id'],
                        'input': case['input'],
                        'expected_intent': case['expected_intent'],
                        'actual_intent': perceived['intent'],
                        'intent_correct': intent_correct,
                        'entities_correct': entities_correct,
                        'passed': passed
                    })
                    
                except Exception as e:
                    results['failed'] += 1
                    results['details'].append({
                        'case_id': case['id'],
                        'error': str(e),
                        'passed': False
                    })
        
        results['accuracy'] = results['passed'] / (results['passed'] + results['failed'])
        return results
    
    def test_reasoning_quality(self, test_cases: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Test reasoning module quality"""
        print("Testing reasoning quality...")
        
        results = {'passed': 0, 'failed': 0, 'details': []}
        
        for category, cases in test_cases.items():
            for case in cases:
                try:
                    perceived = self.perception.process(case['input'])
                    reasoning_result = self.reasoning.reason(perceived)
                    
                    # Check if plan is generated
                    has_plan = len(reasoning_result.get('plan', [])) > 0
                    
                    # Check if expected tools are in plan
                    planned_tools = [action.get('tool') for action in reasoning_result.get('plan', [])]
                    expected_tools = case.get('expected_tools', [])
                    
                    tools_match = any(tool in planned_tools for tool in expected_tools)
                    
                    passed = has_plan and tools_match
                    
                    if passed:
                        results['passed'] += 1
                    else:
                        results['failed'] += 1
                    
                    results['details'].append({
                        'case_id': case['id'],
                        'has_plan': has_plan,
                        'expected_tools': expected_tools,
                        'planned_tools': planned_tools,
                        'tools_match': tools_match,
                        'passed': passed
                    })
                    
                except Exception as e:
                    results['failed'] += 1
                    results['details'].append({
                        'case_id': case['id'],
                        'error': str(e),
                        'passed': False
                    })
        
        results['quality_score'] = results['passed'] / (results['passed'] + results['failed'])
        return results
    
    def test_tool_usage(self, test_cases: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Test tool usage and execution"""
        print("Testing tool usage...")
        
        results = {'passed': 0, 'failed': 0, 'details': []}
        
        for category, cases in test_cases.items():
            for case in cases:
                try:
                    perceived = self.perception.process(case['input'])
                    reasoning_result = self.reasoning.reason(perceived)
                    action_results = self.action.execute(reasoning_result['plan'])
                    
                    # Check if actions were executed
                    has_results = len(action_results) > 0
                    
                    # Check success rate
                    successful_actions = sum(1 for r in action_results if r.get('status') == 'success')
                    success_rate = successful_actions / len(action_results) if action_results else 0
                    
                    passed = has_results and success_rate > 0
                    
                    if passed:
                        results['passed'] += 1
                    else:
                        results['failed'] += 1
                    
                    results['details'].append({
                        'case_id': case['id'],
                        'has_results': has_results,
                        'success_rate': success_rate,
                        'action_count': len(action_results),
                        'passed': passed
                    })
                    
                except Exception as e:
                    results['failed'] += 1
                    results['details'].append({
                        'case_id': case['id'],
                        'error': str(e),
                        'passed': False
                    })
        
        results['usage_score'] = results['passed'] / (results['passed'] + results['failed'])
        return results
    
    def test_observation_accuracy(self, test_cases: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Test observation module accuracy"""
        print("Testing observation accuracy...")
        
        results = {'passed': 0, 'failed': 0, 'details': []}
        
        for category, cases in test_cases.items():
            for case in cases:
                try:
                    perceived = self.perception.process(case['input'])
                    reasoning_result = self.reasoning.reason(perceived)
                    action_results = self.action.execute(reasoning_result['plan'])
                    observation = self.observation.observe(action_results, case['input'])
                    
                    # Check if observation has required components
                    has_evaluation = 'evaluation' in observation
                    has_reflection = 'reflection' in observation
                    has_decision = 'decision' in observation
                    
                    # Check decision accuracy
                    expected_outcome = case.get('expected_outcome', 'complete')
                    decision_correct = observation['decision'] == expected_outcome
                    
                    passed = has_evaluation and has_reflection and has_decision and decision_correct
                    
                    if passed:
                        results['passed'] += 1
                    else:
                        results['failed'] += 1
                    
                    results['details'].append({
                        'case_id': case['id'],
                        'has_evaluation': has_evaluation,
                        'has_reflection': has_reflection,
                        'has_decision': has_decision,
                        'expected_outcome': expected_outcome,
                        'actual_decision': observation.get('decision'),
                        'decision_correct': decision_correct,
                        'passed': passed
                    })
                    
                except Exception as e:
                    results['failed'] += 1
                    results['details'].append({
                        'case_id': case['id'],
                        'error': str(e),
                        'passed': False
                    })
        
        results['accuracy_score'] = results['passed'] / (results['passed'] + results['failed'])
        return results
    
    def test_complete_loop_operation(self, test_cases: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Test complete agent loop operation"""
        print("Testing complete loop operation...")
        
        results = {'passed': 0, 'failed': 0, 'details': []}
        
        for category, cases in test_cases.items():
            for case in cases:
                try:
                    result = self.agent.run(case['input'], max_iterations=3)
                    
                    # Check if loop completed
                    completed = result.get('status') == 'success'
                    
                    # Check iterations
                    iterations = result.get('iterations', 0)
                    reasonable_iterations = 1 <= iterations <= 3
                    
                    # Check termination reason
                    termination = result.get('termination_reason')
                    valid_termination = termination in ['goal_achieved', 'max_iterations_reached', 'error_termination']
                    
                    passed = completed and reasonable_iterations and valid_termination
                    
                    if passed:
                        results['passed'] += 1
                    else:
                        results['failed'] += 1
                    
                    results['details'].append({
                        'case_id': case['id'],
                        'completed': completed,
                        'iterations': iterations,
                        'termination_reason': termination,
                        'reasonable_iterations': reasonable_iterations,
                        'valid_termination': valid_termination,
                        'passed': passed
                    })
                    
                except Exception as e:
                    results['failed'] += 1
                    results['details'].append({
                        'case_id': case['id'],
                        'error': str(e),
                        'passed': False
                    })
        
        results['operation_score'] = results['passed'] / (results['passed'] + results['failed'])
        return results
    
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate test summary"""
        total_tests = 0
        total_passed = 0
        
        test_categories = ['perception_tests', 'reasoning_tests', 'tool_tests', 
                          'observation_tests', 'complete_loop_tests']
        
        category_scores = {}
        
        for category in test_categories:
            if category in results:
                cat_results = results[category]
                total_tests += cat_results['passed'] + cat_results['failed']
                total_passed += cat_results['passed']
                
                score_keys = [k for k in cat_results.keys() if k.endswith('_score')]
                if score_keys:
                    category_scores[category] = cat_results[score_keys[0]]
                else:
                    category_scores[category] = 0.0
        
        overall_score = total_passed / total_tests if total_tests > 0 else 0
        
        return {
            'total_tests': total_tests,
            'total_passed': total_passed,
            'total_failed': total_tests - total_passed,
            'overall_score': overall_score,
            'category_scores': category_scores,
            'grade': self._get_grade(overall_score)
        }
    
    def _get_grade(self, score: float) -> str:
        """Get letter grade based on score"""
        if score >= 0.9:
            return 'A'
        elif score >= 0.8:
            return 'B'
        elif score >= 0.7:
            return 'C'
        elif score >= 0.6:
            return 'D'
        else:
            return 'F'
    
    def save_results(self, results: Dict[str, Any], filename: str = 'test_results.json'):
        """Save test results to file"""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {filename}")
    
    def print_summary(self, results: Dict[str, Any]):
        """Print test summary"""
        summary = results['summary']
        
        print("\n" + "="*50)
        print("AGENT TEST SUITE SUMMARY")
        print("="*50)
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['total_passed']}")
        print(f"Failed: {summary['total_failed']}")
        print(f"Overall Score: {summary['overall_score']:.2%}")
        print(f"Grade: {summary['grade']}")
        print("\nCategory Scores:")
        
        for category, score in summary['category_scores'].items():
            print(f"  {category.replace('_', ' ').title()}: {score:.2%}")
        
        print("="*50)


def main():
    """Run the test suite"""
    test_runner = TestScenarios()
    
    # Change to test_suite directory
    os.chdir('test_suite')
    
    # Run all tests
    results = test_runner.run_all_tests()
    
    # Save and display results
    test_runner.save_results(results)
    test_runner.print_summary(results)
    
    return results


if __name__ == "__main__":
    main()