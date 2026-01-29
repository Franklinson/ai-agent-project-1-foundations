import time

class ActionExecutor:
    def __init__(self, tool_registry):
        self.tool_registry = tool_registry
        self.max_retries = 3
        self.retryable_errors = ('timeout', 'network', 'connection')
    
    def execute(self, action):
        """Execute an action with parameter validation and error handling."""
        try:
            tool_name = action.get('tool')
            parameters = action.get('parameters', {})
            
            tool = self.tool_registry.get(tool_name)
            if not tool:
                return {'success': False, 'error': f'Tool {tool_name} not found'}
            
            required_params = tool.get('required_parameters', [])
            for param in required_params:
                if param not in parameters:
                    return {'success': False, 'error': f'Missing required parameter: {param}'}
            
            result = tool['function'](**parameters)
            return {'success': True, 'result': result}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def execute_with_retry(self, action):
        """Execute an action with retry logic and exponential backoff."""
        for attempt in range(self.max_retries + 1):
            result = self.execute(action)
            
            if result['success'] or attempt == self.max_retries:
                return result
            
            error = result.get('error', '').lower()
            if any(retryable in error for retryable in self.retryable_errors):
                time.sleep(2 ** attempt)
            else:
                return result
        
        return result
