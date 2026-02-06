from typing import Dict, List, Any, Callable

class ActionModule:
    def __init__(self):
        self.tool_registry: Dict[str, Callable] = {
            'search_tool': self._search_tool,
            'assistant_tool': self._assistant_tool,
            'execution_tool': self._execution_tool,
            'response_tool': self._response_tool,
            'entity_processor': self._entity_processor,
            'fallback_tool': self._fallback_tool
        }
    
    def execute(self, actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        
        for action in actions:
            try:
                tool_name = action.get('tool')
                tool_func = self.tool_registry.get(tool_name)
                
                if tool_func:
                    result = tool_func(action)
                    results.append({
                        'action': action.get('action'),
                        'tool': tool_name,
                        'status': 'success',
                        'result': result
                    })
                else:
                    results.append({
                        'action': action.get('action'),
                        'tool': tool_name,
                        'status': 'error',
                        'error': f'Tool {tool_name} not found'
                    })
            except Exception as e:
                results.append({
                    'action': action.get('action'),
                    'tool': action.get('tool'),
                    'status': 'error',
                    'error': str(e)
                })
        
        return results
    
    def _search_tool(self, action: Dict[str, Any]) -> str:
        return "Search completed"
    
    def _assistant_tool(self, action: Dict[str, Any]) -> str:
        return "Assistant response generated"
    
    def _execution_tool(self, action: Dict[str, Any]) -> str:
        return "Command executed"
    
    def _response_tool(self, action: Dict[str, Any]) -> str:
        return "Response sent"
    
    def _entity_processor(self, action: Dict[str, Any]) -> str:
        return "Entities processed"
    
    def _fallback_tool(self, action: Dict[str, Any]) -> str:
        return "Fallback response"
