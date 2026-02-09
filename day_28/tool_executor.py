"""Tool executor for invoking registered tools."""

from typing import Dict, Any
from tool_registry import ToolRegistry


class ToolExecutor:
    """Executes tools from the registry with parameter handling."""
    
    def __init__(self, registry: ToolRegistry):
        self.registry = registry
    
    def execute(self, tool_name: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute a tool with given parameters.
        
        Args:
            tool_name: Name of the tool to execute
            parameters: Dict of parameters to pass to the tool
            
        Returns:
            Dict with execution result
        """
        parameters = parameters or {}
        
        # Get tool from registry
        tool = self.registry.get(tool_name)
        if not tool:
            return {
                'success': False,
                'error': f'Tool not found: {tool_name}'
            }
        
        # Validate parameters
        tool_params = tool['parameters']
        required_params = [p for p, meta in tool_params.items() if meta['default'] == 'NO_DEFAULT']
        missing = [p for p in required_params if p not in parameters]
        
        if missing:
            return {
                'success': False,
                'error': f'Missing required parameters: {missing}'
            }
        
        # Execute tool
        try:
            result = tool['function'](**parameters)
            # Check if tool itself returned an error
            if isinstance(result, dict) and not result.get('success', True):
                return {
                    'success': False,
                    'tool': tool_name,
                    'error': result.get('error', 'Tool execution failed')
                }
            return {
                'success': True,
                'tool': tool_name,
                'result': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Execution error: {str(e)}'
            }
