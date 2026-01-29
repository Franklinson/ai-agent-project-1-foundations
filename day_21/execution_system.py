from tool_registry import ToolRegistry
from action_executor import ActionExecutor
from result_processor import ResultProcessor


class ExecutionSystem:
    def __init__(self):
        self.tool_registry = ToolRegistry()
        self.executor = ActionExecutor(self.tool_registry)
        self.processor = ResultProcessor()
    
    def execute_action_plan(self, actions):
        """Execute a list of actions and return aggregated results."""
        results = []
        
        for action in actions:
            execution_result = self.executor.execute_with_retry(action)
            processed_result = self.processor.process(execution_result)
            results.append(processed_result)
        
        return {
            'total_actions': len(actions),
            'successful': sum(1 for r in results if r.get('success')),
            'failed': sum(1 for r in results if not r.get('success')),
            'results': results
        }
