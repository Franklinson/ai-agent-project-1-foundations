"""Tool registry for managing and discovering agent tools."""

from typing import Dict, Any, Callable, List, Optional
import inspect


class ToolRegistry:
    """Registry for managing agent tools."""
    
    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {}
    
    def register(self, tool: Callable, name: str = None, description: str = None) -> None:
        """
        Register a tool with metadata.
        
        Args:
            tool: Tool function
            name: Tool name (uses function name if None)
            description: Tool description (uses docstring if None)
        """
        tool_name = name or tool.__name__
        sig = inspect.signature(tool)
        
        self._tools[tool_name] = {
            'name': tool_name,
            'function': tool,
            'description': description or (tool.__doc__ or '').strip().split('\n')[0],
            'parameters': {
                param: {
                    'type': str(sig.parameters[param].annotation) if sig.parameters[param].annotation != inspect.Parameter.empty else 'Any',
                    'default': sig.parameters[param].default if sig.parameters[param].default != inspect.Parameter.empty else 'NO_DEFAULT'
                }
                for param in sig.parameters
            }
        }
    
    def get(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Get tool by name.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Tool metadata dict or None
        """
        return self._tools.get(tool_name)
    
    def list_all(self) -> List[Dict[str, Any]]:
        """
        List all registered tools.
        
        Returns:
            List of tool metadata (without function objects)
        """
        return [
            {
                'name': tool['name'],
                'description': tool['description'],
                'parameters': tool['parameters']
            }
            for tool in self._tools.values()
        ]
