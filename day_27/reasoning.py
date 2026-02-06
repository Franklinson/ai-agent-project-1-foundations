from typing import Dict, List, Any

class ReasoningModule:
    def __init__(self):
        self.tool_mapping = {
            'question': 'search_tool',
            'request': 'assistant_tool',
            'command': 'execution_tool',
            'greeting': 'response_tool',
            'unknown': 'fallback_tool'
        }
    
    def reason(self, processed_input: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        analysis = self._analyze(processed_input)
        plan = self._plan(analysis, context or {})
        
        return {
            'analysis': analysis,
            'plan': plan
        }
    
    def _analyze(self, processed_input: Dict[str, Any]) -> Dict[str, Any]:
        intent = processed_input.get('intent', 'unknown')
        entities = processed_input.get('entities', [])
        
        return {
            'intent': intent,
            'entity_count': len(entities),
            'has_entities': len(entities) > 0,
            'complexity': 'high' if len(entities) > 2 else 'low'
        }
    
    def _plan(self, analysis: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        intent = analysis['intent']
        tool = self._select_tool(intent)
        
        actions = [{
            'action': 'execute',
            'tool': tool,
            'priority': 1
        }]
        
        if analysis['has_entities']:
            actions.append({
                'action': 'process_entities',
                'tool': 'entity_processor',
                'priority': 2
            })
        
        return actions
    
    def _select_tool(self, intent: str) -> str:
        return self.tool_mapping.get(intent, 'fallback_tool')
