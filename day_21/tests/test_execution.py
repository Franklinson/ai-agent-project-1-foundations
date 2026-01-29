import unittest
import sys
sys.path.insert(0, '..')

from tool_registry import ToolRegistry
from action_executor import ActionExecutor
from result_processor import ResultProcessor
from execution_system import ExecutionSystem


class TestToolRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = ToolRegistry()
    
    def test_register_and_get(self):
        tool = {'name': 'test_tool', 'function': lambda x: x}
        self.registry.register(tool)
        self.assertEqual(self.registry.get('test_tool'), tool)
    
    def test_get_nonexistent(self):
        self.assertIsNone(self.registry.get('nonexistent'))
    
    def test_list_available(self):
        self.registry.register({'name': 'tool1', 'function': lambda: None})
        self.registry.register({'name': 'tool2', 'function': lambda: None})
        self.assertEqual(set(self.registry.list_available()), {'tool1', 'tool2'})


class TestActionExecutor(unittest.TestCase):
    def setUp(self):
        self.registry = ToolRegistry()
        self.executor = ActionExecutor(self.registry)
    
    def test_execute_success(self):
        self.registry.register({
            'name': 'add',
            'function': lambda a, b: a + b,
            'required_parameters': ['a', 'b']
        })
        result = self.executor.execute({'tool': 'add', 'parameters': {'a': 2, 'b': 3}})
        self.assertTrue(result['success'])
        self.assertEqual(result['result'], 5)
    
    def test_execute_tool_not_found(self):
        result = self.executor.execute({'tool': 'nonexistent', 'parameters': {}})
        self.assertFalse(result['success'])
        self.assertIn('not found', result['error'])
    
    def test_execute_missing_parameter(self):
        self.registry.register({
            'name': 'add',
            'function': lambda a, b: a + b,
            'required_parameters': ['a', 'b']
        })
        result = self.executor.execute({'tool': 'add', 'parameters': {'a': 2}})
        self.assertFalse(result['success'])
        self.assertIn('Missing required parameter', result['error'])
    
    def test_execute_exception(self):
        def error_func():
            raise ValueError('Test error')
        self.registry.register({'name': 'error', 'function': error_func})
        result = self.executor.execute({'tool': 'error', 'parameters': {}})
        self.assertFalse(result['success'])
        self.assertIn('Test error', result['error'])


class TestResultProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = ResultProcessor()
    
    def test_validate_valid(self):
        self.assertTrue(self.processor.validate({'success': True}))
    
    def test_validate_invalid(self):
        self.assertFalse(self.processor.validate({'result': 'data'}))
        self.assertFalse(self.processor.validate('not a dict'))
    
    def test_extract_data_success(self):
        data = self.processor.extract_data({'success': True, 'result': 'test'})
        self.assertEqual(data, 'test')
    
    def test_extract_data_error(self):
        data = self.processor.extract_data({'success': False, 'error': 'failed'})
        self.assertEqual(data, 'failed')
    
    def test_transform(self):
        self.assertEqual(self.processor.transform(42), '42')
        self.assertEqual(self.processor.transform(None), '')
    
    def test_process_success(self):
        result = self.processor.process({'success': True, 'result': 'data'})
        self.assertTrue(result['valid'])
        self.assertTrue(result['success'])
        self.assertEqual(result['observation'], 'data')
    
    def test_process_invalid(self):
        result = self.processor.process({'invalid': 'format'})
        self.assertFalse(result['valid'])


class TestExecutionSystem(unittest.TestCase):
    def setUp(self):
        self.system = ExecutionSystem()
        self.system.tool_registry.register({
            'name': 'multiply',
            'function': lambda x, y: x * y,
            'required_parameters': ['x', 'y']
        })
    
    def test_execute_action_plan(self):
        actions = [
            {'tool': 'multiply', 'parameters': {'x': 3, 'y': 4}},
            {'tool': 'multiply', 'parameters': {'x': 2, 'y': 5}}
        ]
        results = self.system.execute_action_plan(actions)
        self.assertEqual(results['total_actions'], 2)
        self.assertEqual(results['successful'], 2)
        self.assertEqual(results['failed'], 0)
    
    def test_execute_action_plan_with_failures(self):
        actions = [
            {'tool': 'multiply', 'parameters': {'x': 3, 'y': 4}},
            {'tool': 'nonexistent', 'parameters': {}}
        ]
        results = self.system.execute_action_plan(actions)
        self.assertEqual(results['total_actions'], 2)
        self.assertEqual(results['successful'], 1)
        self.assertEqual(results['failed'], 1)


if __name__ == '__main__':
    unittest.main()
