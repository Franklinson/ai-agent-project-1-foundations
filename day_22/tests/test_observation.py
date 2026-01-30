import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from result_evaluator import ResultEvaluator
from reflector import Reflector
from observation_decision_maker import ObservationDecisionMaker
from observation_system import ObservationSystem


# Test ResultEvaluator
def test_evaluator_success():
    evaluator = ResultEvaluator()
    result = {'success': True, 'valid': True, 'observation': 'Task completed'}
    
    assert evaluator.check_success(result) == True
    quality = evaluator.assess_quality(result)
    assert quality['score'] == 100
    assert len(quality['issues']) == 0


def test_evaluator_failure():
    evaluator = ResultEvaluator()
    result = {'success': False, 'valid': True, 'observation': 'Error occurred'}
    
    assert evaluator.check_success(result) == False
    quality = evaluator.assess_quality(result)
    assert quality['score'] == 0
    assert 'Execution failed' in quality['issues']


def test_evaluator_progress():
    evaluator = ResultEvaluator()
    goal = "complete task"
    
    # Complete progress
    result = {'success': True, 'valid': True, 'observation': 'complete task done'}
    progress = evaluator.assess_progress(result, goal)
    assert progress['progress'] == 100
    assert progress['status'] == 'complete'
    
    # Partial progress
    result = {'success': True, 'valid': True, 'observation': 'working on it'}
    progress = evaluator.assess_progress(result, goal)
    assert progress['progress'] == 50
    assert progress['status'] == 'partial'


def test_evaluator_errors():
    evaluator = ResultEvaluator()
    
    # No errors
    result = {'success': True, 'valid': True}
    errors = evaluator.identify_errors(result)
    assert len(errors) == 0
    
    # Validation error
    result = {'success': True, 'valid': False, 'observation': 'Invalid format'}
    errors = evaluator.identify_errors(result)
    assert len(errors) == 1
    assert errors[0]['type'] == 'validation'
    
    # Execution error
    result = {'success': False, 'valid': True, 'observation': 'Failed'}
    errors = evaluator.identify_errors(result)
    assert len(errors) == 1
    assert errors[0]['type'] == 'execution'


def test_evaluator_comprehensive():
    evaluator = ResultEvaluator()
    result = {'success': True, 'valid': True, 'observation': 'test goal achieved'}
    goal = "test goal"
    
    evaluation = evaluator.evaluate(result, goal)
    assert evaluation['success'] == True
    assert 'quality' in evaluation
    assert 'progress' in evaluation
    assert 'errors' in evaluation


# Test Reflector
def test_reflector_analyze_positive():
    reflector = Reflector()
    evaluation = {
        'success': True,
        'quality': {'score': 90},
        'progress': {'progress': 100},
        'errors': []
    }
    
    analysis = reflector.analyze_outcome({}, evaluation)
    assert analysis['outcome'] == 'positive'
    assert analysis['quality_score'] == 90
    assert analysis['had_errors'] == False


def test_reflector_analyze_negative():
    reflector = Reflector()
    evaluation = {
        'success': False,
        'quality': {'score': 20},
        'progress': {'progress': 10},
        'errors': [{'type': 'execution'}]
    }
    
    analysis = reflector.analyze_outcome({}, evaluation)
    assert analysis['outcome'] == 'negative'
    assert analysis['had_errors'] == True


def test_reflector_extract_lessons():
    reflector = Reflector()
    
    # Success lessons
    evaluation = {
        'success': True,
        'quality': {'score': 100},
        'progress': {'status': 'complete'},
        'errors': []
    }
    lessons = reflector.extract_lessons({}, evaluation)
    assert 'Action executed successfully' in lessons
    assert 'High quality result achieved' in lessons
    assert 'Goal fully achieved' in lessons
    
    # Failure lessons
    evaluation = {
        'success': False,
        'errors': [{'type': 'validation'}],
        'progress': {'status': 'minimal'}
    }
    lessons = reflector.extract_lessons({}, evaluation)
    assert 'Action failed - review approach' in lessons


def test_reflector_suggest_improvements():
    reflector = Reflector()
    
    # Failed action
    evaluation = {'success': False, 'quality': {'issues': []}, 'progress': {'progress': 0}}
    suggestions = reflector.suggest_improvements({}, evaluation)
    assert 'Retry with different parameters' in suggestions
    
    # Partial progress
    evaluation = {'success': True, 'quality': {'issues': []}, 'progress': {'progress': 50}}
    suggestions = reflector.suggest_improvements({}, evaluation)
    assert 'Consider additional actions to complete goal' in suggestions


def test_reflector_stores_experience():
    reflector = Reflector()
    result = {'success': True}
    evaluation = {'success': True, 'quality': {'score': 100}, 'progress': {'progress': 100}, 'errors': []}
    
    assert len(reflector.experiences) == 0
    reflection = reflector.reflect(result, evaluation)
    assert len(reflector.experiences) == 1
    assert reflection['total_experiences'] == 1


# Test ObservationDecisionMaker
def test_decision_maker_goal_achieved():
    dm = ObservationDecisionMaker()
    evaluation = {
        'success': True,
        'progress': {'status': 'complete', 'progress': 100},
        'errors': []
    }
    
    assert dm.is_goal_achieved(evaluation, "test goal") == True
    decision = dm.decide(evaluation, "test goal")
    assert decision['decision'] == ObservationDecisionMaker.COMPLETE


def test_decision_maker_goal_not_achieved():
    dm = ObservationDecisionMaker()
    evaluation = {
        'success': True,
        'progress': {'status': 'partial', 'progress': 50},
        'errors': []
    }
    
    assert dm.is_goal_achieved(evaluation, "test goal") == False


def test_decision_maker_handle_errors():
    dm = ObservationDecisionMaker()
    
    # Validation error
    evaluation = {'errors': [{'type': 'validation'}]}
    assert dm.handle_errors(evaluation) == ObservationDecisionMaker.TRY_ALTERNATIVE
    
    # Execution error
    evaluation = {'errors': [{'type': 'execution'}]}
    assert dm.handle_errors(evaluation) == ObservationDecisionMaker.RETRY
    
    # No errors
    evaluation = {'errors': []}
    assert dm.handle_errors(evaluation) == None


def test_decision_maker_retry_limit():
    dm = ObservationDecisionMaker()
    evaluation = {
        'success': False,
        'progress': {'progress': 0},
        'errors': [{'type': 'execution'}]
    }
    
    # First two attempts should retry
    decision1 = dm.decide(evaluation, "goal")
    assert decision1['decision'] == ObservationDecisionMaker.RETRY
    
    decision2 = dm.decide(evaluation, "goal")
    assert decision2['decision'] == ObservationDecisionMaker.RETRY
    
    # Third attempt should abort
    decision3 = dm.decide(evaluation, "goal")
    assert decision3['decision'] == ObservationDecisionMaker.ABORT


def test_decision_maker_partial_progress():
    dm = ObservationDecisionMaker()
    evaluation = {
        'success': True,
        'progress': {'status': 'partial', 'progress': 60},
        'errors': []
    }
    
    decision = dm.decide(evaluation, "goal")
    assert decision['decision'] == ObservationDecisionMaker.CONTINUE
    assert decision['confidence'] == 0.8


def test_decision_maker_stuck_detection():
    dm = ObservationDecisionMaker()
    evaluation = {
        'success': True,
        'progress': {'status': 'minimal', 'progress': 20},
        'errors': []
    }
    
    dm.decide(evaluation, "goal")
    decision = dm.decide(evaluation, "goal")
    assert decision['decision'] == ObservationDecisionMaker.TRY_ALTERNATIVE
    assert 'Stuck' in decision['reason']


# Test ObservationSystem
def test_observation_system_integration():
    system = ObservationSystem()
    goal = "complete task"
    
    action_results = [
        {'success': True, 'valid': True, 'observation': 'complete task done'}
    ]
    
    observation = system.observe(action_results, goal)
    
    assert 'observations' in observation
    assert 'overall_decision' in observation
    assert 'total_experiences' in observation
    assert len(observation['observations']) == 1


def test_observation_system_multiple_results():
    system = ObservationSystem()
    goal = "multi-step task"
    
    action_results = [
        {'success': True, 'valid': True, 'observation': 'Step 1 done'},
        {'success': True, 'valid': True, 'observation': 'Step 2 done'}
    ]
    
    observation = system.observe(action_results, goal)
    assert len(observation['observations']) == 2


def test_observation_system_overall_decision_complete():
    system = ObservationSystem()
    goal = "finish task"
    
    action_results = [
        {'success': True, 'valid': True, 'observation': 'finish task completed'}
    ]
    
    observation = system.observe(action_results, goal)
    assert observation['overall_decision'] == ObservationDecisionMaker.COMPLETE


def test_observation_system_overall_decision_abort():
    system = ObservationSystem()
    goal = "task"
    
    action_results = [
        {'success': False, 'valid': True, 'observation': 'Error'}
    ]
    
    # Trigger multiple failures to reach abort
    for _ in range(3):
        observation = system.observe(action_results, goal)
    
    assert observation['overall_decision'] == ObservationDecisionMaker.ABORT


def test_observation_system_experience_accumulation():
    system = ObservationSystem()
    goal = "task"
    
    action_results = [{'success': True, 'valid': True, 'observation': 'Done'}]
    
    obs1 = system.observe(action_results, goal)
    assert obs1['total_experiences'] == 1
    
    obs2 = system.observe(action_results, goal)
    assert obs2['total_experiences'] == 2


# Edge cases
def test_edge_case_empty_observation():
    evaluator = ResultEvaluator()
    result = {'success': True, 'valid': True, 'observation': ''}
    
    quality = evaluator.assess_quality(result)
    assert quality['score'] == 50


def test_edge_case_missing_fields():
    evaluator = ResultEvaluator()
    result = {}
    
    assert evaluator.check_success(result) == False
    errors = evaluator.identify_errors(result)
    assert len(errors) > 0


def test_edge_case_none_values():
    reflector = Reflector()
    evaluation = {
        'success': None,
        'quality': {},
        'progress': {},
        'errors': []
    }
    
    analysis = reflector.analyze_outcome({}, evaluation)
    assert 'outcome' in analysis


# Run all tests
def run_tests():
    tests = [
        # ResultEvaluator tests
        test_evaluator_success,
        test_evaluator_failure,
        test_evaluator_progress,
        test_evaluator_errors,
        test_evaluator_comprehensive,
        
        # Reflector tests
        test_reflector_analyze_positive,
        test_reflector_analyze_negative,
        test_reflector_extract_lessons,
        test_reflector_suggest_improvements,
        test_reflector_stores_experience,
        
        # ObservationDecisionMaker tests
        test_decision_maker_goal_achieved,
        test_decision_maker_goal_not_achieved,
        test_decision_maker_handle_errors,
        test_decision_maker_retry_limit,
        test_decision_maker_partial_progress,
        test_decision_maker_stuck_detection,
        
        # ObservationSystem tests
        test_observation_system_integration,
        test_observation_system_multiple_results,
        test_observation_system_overall_decision_complete,
        test_observation_system_overall_decision_abort,
        test_observation_system_experience_accumulation,
        
        # Edge cases
        test_edge_case_empty_observation,
        test_edge_case_missing_fields,
        test_edge_case_none_values,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            print(f"✓ {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: {type(e).__name__}: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Tests passed: {passed}/{len(tests)}")
    print(f"Tests failed: {failed}/{len(tests)}")
    print(f"{'='*50}")
    
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
