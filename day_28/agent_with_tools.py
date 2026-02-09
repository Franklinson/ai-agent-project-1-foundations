"""Agent with integrated tool system."""

import sys
sys.path.append('../day_27')

from typing import Dict, Any
from perception import PerceptionModule
from observation import ObservationModule
from state_manager import StateManager
from tool_registry import ToolRegistry
from tool_executor import ToolExecutor
from tools import calculator, search, get_time


class ToolAwareReasoningModule:
    """Reasoning module that considers available tools."""
    
    def __init__(self, registry: ToolRegistry):
        self.registry = registry
    
    def reason(self, processed_input: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        analysis = self._analyze(processed_input)
        plan = self._plan(analysis, context or {})
        
        return {'analysis': analysis, 'plan': plan}
    
    def _analyze(self, processed_input: Dict[str, Any]) -> Dict[str, Any]:
        intent = processed_input.get('intent', 'unknown')
        entities = processed_input.get('entities', [])
        
        return {
            'intent': intent,
            'entities': entities,
            'available_tools': [t['name'] for t in self.registry.list_all()]
        }
    
    def _plan(self, analysis: Dict[str, Any], context: Dict[str, Any]) -> list:
        intent = analysis['intent']
        entities = analysis['entities']
        
        # Map intents to tools
        if intent == 'calculate' or any('number' in str(e).lower() for e in entities):
            return [{'tool': 'calculator', 'params': self._extract_calc_params(entities)}]
        elif intent == 'search' or intent == 'question':
            return [{'tool': 'search', 'params': self._extract_search_params(entities)}]
        elif intent == 'time':
            return [{'tool': 'get_time', 'params': {'format': 'readable'}}]
        
        return [{'tool': 'search', 'params': {'query': str(entities[0]) if entities else 'default'}}]
    
    def _extract_calc_params(self, entities: list) -> Dict[str, Any]:
        # Simple extraction - look for operation and numbers
        ops = ['add', 'subtract', 'multiply', 'divide']
        operation = next((e for e in entities if e in ops), 'add')
        numbers = [e for e in entities if isinstance(e, (int, float))]
        
        return {
            'operation': operation,
            'a': numbers[0] if len(numbers) > 0 else 0,
            'b': numbers[1] if len(numbers) > 1 else 0
        }
    
    def _extract_search_params(self, entities: list) -> Dict[str, Any]:
        query = ' '.join(str(e) for e in entities) if entities else 'AI'
        return {'query': query}


class ToolAwareActionModule:
    """Action module that uses tool executor."""
    
    def __init__(self, executor: ToolExecutor):
        self.executor = executor
    
    def execute(self, actions: list) -> list:
        results = []
        
        for action in actions:
            tool_name = action.get('tool')
            params = action.get('params', {})
            
            result = self.executor.execute(tool_name, params)
            results.append(result)
        
        return results


class AgentWithTools:
    """Agent with integrated tool system."""
    
    def __init__(self):
        # Initialize tool system
        self.registry = ToolRegistry()
        self.registry.register(calculator)
        self.registry.register(search)
        self.registry.register(get_time)
        
        self.executor = ToolExecutor(self.registry)
        
        # Initialize modules
        self.perception = PerceptionModule()
        self.reasoning = ToolAwareReasoningModule(self.registry)
        self.action = ToolAwareActionModule(self.executor)
        self.observation = ObservationModule()
        self.state = StateManager()
    
    def run(self, user_input: str, goal: str = "Process user request") -> Dict[str, Any]:
        self.state.add_goal(goal)
        
        # Perception
        perceived = self.perception.process(user_input)
        
        # Reasoning with tool awareness
        reasoning_result = self.reasoning.reason(perceived, self.state.get_context())
        
        # Action using tool executor
        action_results = self.action.execute(reasoning_result['plan'])
        
        # Observation
        observation = self.observation.observe(action_results, goal)
        
        # Update state
        self.state.add_to_history({
            'input': user_input,
            'perceived': perceived,
            'reasoning': reasoning_result,
            'actions': action_results,
            'observation': observation
        })
        
        return {
            'perceived': perceived,
            'reasoning': reasoning_result,
            'actions': action_results,
            'observation': observation,
            'decision': observation['decision']
        }
