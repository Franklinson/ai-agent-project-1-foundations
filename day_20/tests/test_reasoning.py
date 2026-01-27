"""Unit tests for Day 20 reasoning system components."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from reasoner import Reasoner
from planner import Planner, Plan
from decision_maker import DecisionMaker
from reasoning_system import ReasoningSystem


class TestReasoner(unittest.TestCase):
    """Test cases for Reasoner component."""
    
    def setUp(self):
        self.reasoner = Reasoner()
    
    def test_query_intent(self):
        """Test reasoner with query intent."""
        result = self.reasoner.reason({
            'intent': 'query',
            'entities': {'keywords': ['test']},
            'text': 'What is the test?'
        })
        
        self.assertTrue(result['success'])
        self.assertEqual(result['goal'], 'retrieve_information')
        self.assertIn('reasoning', result)
        self.assertGreater(result['confidence'], 0.7)
    
    def test_command_intent(self):
        """Test reasoner with command intent."""
        result = self.reasoner.reason({
            'intent': 'command',
            'entities': {'keywords': ['create']},
            'text': 'Create a file'
        })
        
        self.assertTrue(result['success'])
        self.assertEqual(result['goal'], 'execute_action')
        self.assertIn('User wants to execute', result['reasoning'])
    
    def test_greeting_intent(self):
        """Test reasoner with greeting intent."""
        result = self.reasoner.reason({
            'intent': 'greeting',
            'entities': {},
            'text': 'Hello'
        })
        
        self.assertTrue(result['success'])
        self.assertEqual(result['goal'], 'acknowledge_user')
        self.assertIn('initiating conversation', result['reasoning'])
    
    def test_unknown_intent(self):
        """Test reasoner with unknown intent."""
        result = self.reasoner.reason({
            'intent': 'unknown',
            'entities': {},
            'text': 'Random text'
        })
        
        self.assertFalse(result['success'])
        self.assertIsNone(result['goal'])
        self.assertIn('error', result)
    
    def test_confidence_with_entities(self):
        """Test confidence increases with entities."""
        result_with_entities = self.reasoner.reason({
            'intent': 'query',
            'entities': {'keywords': ['test']},
            'text': 'Test'
        })
        
        result_without_entities = self.reasoner.reason({
            'intent': 'query',
            'entities': {},
            'text': 'Test'
        })
        
        self.assertGreater(
            result_with_entities['confidence'],
            result_without_entities['confidence']
        )
    
    def test_actions_mapping(self):
        """Test actions are correctly mapped."""
        result = self.reasoner.reason({
            'intent': 'query',
            'entities': {},
            'text': 'Test'
        })
        
        self.assertIn('actions', result)
        self.assertIsInstance(result['actions'], list)
        self.assertGreater(len(result['actions']), 0)


class TestPlanner(unittest.TestCase):
    """Test cases for Planner component."""
    
    def setUp(self):
        self.planner = Planner()
    
    def test_retrieve_information_goal(self):
        """Test planning for retrieve_information goal."""
        plan = self.planner.decompose_goal('retrieve_information')
        
        self.assertIsInstance(plan, Plan)
        self.assertEqual(plan.goal, 'retrieve_information')
        self.assertEqual(len(plan.sub_goals), 3)
        self.assertIn('identify_query', plan.sub_goals)
        self.assertIn('search_data', plan.sub_goals)
        self.assertIn('synthesize_results', plan.sub_goals)
    
    def test_execute_action_goal(self):
        """Test planning for execute_action goal."""
        plan = self.planner.decompose_goal('execute_action')
        
        self.assertEqual(plan.goal, 'execute_action')
        self.assertEqual(len(plan.sub_goals), 4)
        self.assertIn('validate_input', plan.sub_goals)
        self.assertIn('execute', plan.sub_goals)
    
    def test_acknowledge_user_goal(self):
        """Test planning for acknowledge_user goal."""
        plan = self.planner.decompose_goal('acknowledge_user')
        
        self.assertEqual(plan.goal, 'acknowledge_user')
        self.assertEqual(len(plan.sub_goals), 1)
        self.assertIn('generate_response', plan.sub_goals)
    
    def test_step_ordering(self):
        """Test steps are ordered by dependencies."""
        plan = self.planner.decompose_goal('retrieve_information')
        
        # Check that steps are ordered
        actions = [step['action'] for step in plan.steps]
        
        # identify_query should come before search_data
        self.assertLess(
            actions.index('identify_query'),
            actions.index('search_data')
        )
        
        # search_data should come before synthesize_results
        self.assertLess(
            actions.index('search_data'),
            actions.index('synthesize_results')
        )
    
    def test_step_dependencies(self):
        """Test step dependencies are correctly set."""
        plan = self.planner.decompose_goal('execute_action')
        
        for step in plan.steps:
            if step['action'] == 'execute':
                self.assertIn('prepare_resources', step['dependencies'])
            if step['action'] == 'prepare_resources':
                self.assertIn('validate_input', step['dependencies'])
    
    def test_plan_to_dict(self):
        """Test Plan.to_dict() method."""
        plan = self.planner.decompose_goal('retrieve_information')
        plan_dict = plan.to_dict()
        
        self.assertIn('goal', plan_dict)
        self.assertIn('sub_goals', plan_dict)
        self.assertIn('steps', plan_dict)
        self.assertIn('total_steps', plan_dict)
        self.assertEqual(plan_dict['total_steps'], len(plan.steps))
    
    def test_unknown_goal(self):
        """Test planning with unknown goal."""
        plan = self.planner.decompose_goal('unknown_goal')
        
        self.assertEqual(plan.goal, 'unknown_goal')
        self.assertIn('handle_unknown', plan.sub_goals)
    
    def test_context_in_steps(self):
        """Test context is added to steps."""
        context = {'user_id': 'test_user'}
        plan = self.planner.decompose_goal('retrieve_information', context)
        
        for step in plan.steps:
            self.assertIn('context', step)
            self.assertEqual(step['context'], context)


class TestDecisionMaker(unittest.TestCase):
    """Test cases for DecisionMaker component."""
    
    def setUp(self):
        self.decision_maker = DecisionMaker()
    
    def test_search_tool_selection(self):
        """Test selection of search tool."""
        result = self.decision_maker.select_tool(
            'query',
            'search_knowledge_base',
            {'keywords': ['test']}
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['tool'], 'search_tool')
        self.assertIn('query', result['parameters'])
    
    def test_command_executor_selection(self):
        """Test selection of command executor."""
        result = self.decision_maker.select_tool(
            'command',
            'execute_operation',
            {}
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['tool'], 'command_executor')
        self.assertIn('command', result['parameters'])
    
    def test_validator_selection(self):
        """Test selection of validator."""
        result = self.decision_maker.select_tool(
            'command',
            'validate_input',
            {'keywords': ['test']}
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['tool'], 'validator')
        self.assertIn('input', result['parameters'])
    
    def test_response_generator_selection(self):
        """Test selection of response generator."""
        result = self.decision_maker.select_tool(
            'greeting',
            'generate_greeting',
            {}
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['tool'], 'response_generator')
        self.assertIn('context', result['parameters'])
    
    def test_no_matching_tool(self):
        """Test when no tool matches."""
        result = self.decision_maker.select_tool(
            'unknown',
            'unknown_action',
            {}
        )
        
        self.assertFalse(result['success'])
        self.assertIsNone(result['tool'])
        self.assertIn('No matching tool', result['reason'])
    
    def test_multiple_tool_candidates(self):
        """Test handling of multiple tool candidates."""
        result = self.decision_maker.select_tool(
            'query',
            'generate_response',
            {'keywords': ['test']}
        )
        
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['tool'])
    
    def test_parameter_building(self):
        """Test parameter building for tools."""
        result = self.decision_maker.select_tool(
            'query',
            'search_knowledge_base',
            {'keywords': ['weather', 'today']}
        )
        
        self.assertIn('parameters', result)
        self.assertIsInstance(result['parameters'], dict)
        self.assertEqual(result['parameters']['query'], 'weather')
    
    def test_entity_tool_mapping(self):
        """Test entity-based tool selection."""
        result = self.decision_maker.select_tool(
            'query',
            'identify_query',
            {'dates': ['2024-01-01']}
        )
        
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['tool'])


class TestReasoningSystem(unittest.TestCase):
    """Integration tests for ReasoningSystem."""
    
    def setUp(self):
        self.system = ReasoningSystem()
    
    def test_full_pipeline_query(self):
        """Test full pipeline with query intent."""
        result = self.system.process({
            'intent': 'query',
            'entities': {'keywords': ['weather']},
            'text': 'What is the weather?'
        })
        
        self.assertTrue(result['success'])
        self.assertEqual(result['goal'], 'retrieve_information')
        self.assertIn('reasoning', result)
        self.assertIn('plan', result)
        self.assertIn('action_plan', result)
        self.assertGreater(len(result['action_plan']), 0)
    
    def test_full_pipeline_command(self):
        """Test full pipeline with command intent."""
        result = self.system.process({
            'intent': 'command',
            'entities': {'keywords': ['create']},
            'text': 'Create a file'
        })
        
        self.assertTrue(result['success'])
        self.assertEqual(result['goal'], 'execute_action')
        self.assertGreater(len(result['action_plan']), 0)
    
    def test_full_pipeline_greeting(self):
        """Test full pipeline with greeting intent."""
        result = self.system.process({
            'intent': 'greeting',
            'entities': {},
            'text': 'Hello'
        })
        
        self.assertTrue(result['success'])
        self.assertEqual(result['goal'], 'acknowledge_user')
        self.assertEqual(len(result['action_plan']), 1)
    
    def test_action_plan_structure(self):
        """Test action plan has correct structure."""
        result = self.system.process({
            'intent': 'query',
            'entities': {},
            'text': 'Test'
        })
        
        for action in result['action_plan']:
            self.assertIn('step_id', action)
            self.assertIn('action', action)
            self.assertIn('tool', action)
            self.assertIn('parameters', action)
            self.assertIn('dependencies', action)
    
    def test_confidence_in_result(self):
        """Test confidence is included in result."""
        result = self.system.process({
            'intent': 'query',
            'entities': {'keywords': ['test']},
            'text': 'Test'
        })
        
        self.assertIn('confidence', result)
        self.assertGreater(result['confidence'], 0)
        self.assertLessEqual(result['confidence'], 1)
    
    def test_unknown_intent_handling(self):
        """Test system handles unknown intent."""
        result = self.system.process({
            'intent': 'unknown',
            'entities': {},
            'text': 'Unknown'
        })
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)
        self.assertEqual(result['stage'], 'reasoning')
    
    def test_plan_dict_in_result(self):
        """Test plan is converted to dict in result."""
        result = self.system.process({
            'intent': 'command',
            'entities': {},
            'text': 'Test'
        })
        
        self.assertIn('plan', result)
        self.assertIsInstance(result['plan'], dict)
        self.assertIn('total_steps', result['plan'])
    
    def test_action_plan_ordering(self):
        """Test action plan maintains dependency order."""
        result = self.system.process({
            'intent': 'command',
            'entities': {},
            'text': 'Execute command'
        })
        
        actions = [a['action'] for a in result['action_plan']]
        
        # validate_input should come before execute
        if 'validate_input' in actions and 'execute' in actions:
            self.assertLess(
                actions.index('validate_input'),
                actions.index('execute')
            )


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_empty_entities(self):
        """Test with empty entities."""
        system = ReasoningSystem()
        result = system.process({
            'intent': 'query',
            'entities': {},
            'text': 'Test'
        })
        
        self.assertTrue(result['success'])
    
    def test_missing_text(self):
        """Test with missing text field."""
        system = ReasoningSystem()
        result = system.process({
            'intent': 'query',
            'entities': {}
        })
        
        self.assertTrue(result['success'])
    
    def test_none_entities(self):
        """Test with None entities."""
        decision_maker = DecisionMaker()
        result = decision_maker.select_tool('query', 'search_knowledge_base', None)
        
        self.assertTrue(result['success'])
    
    def test_empty_input(self):
        """Test with minimal input."""
        reasoner = Reasoner()
        result = reasoner.reason({
            'intent': 'query',
            'entities': {},
            'text': ''
        })
        
        self.assertTrue(result['success'])
    
    def test_large_entity_list(self):
        """Test with large entity list."""
        system = ReasoningSystem()
        result = system.process({
            'intent': 'query',
            'entities': {'keywords': ['word' + str(i) for i in range(100)]},
            'text': 'Test with many keywords'
        })
        
        self.assertTrue(result['success'])


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestReasoner))
    suite.addTests(loader.loadTestsFromTestCase(TestPlanner))
    suite.addTests(loader.loadTestsFromTestCase(TestDecisionMaker))
    suite.addTests(loader.loadTestsFromTestCase(TestReasoningSystem))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
