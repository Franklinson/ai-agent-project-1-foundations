from typing import Dict, Any
from perception import PerceptionModule
from reasoning import ReasoningModule
from action import ActionModule
from observation import ObservationModule
from state_manager import StateManager

class Agent:
    def __init__(self):
        self.perception = PerceptionModule()
        self.reasoning = ReasoningModule()
        self.action = ActionModule()
        self.observation = ObservationModule()
        self.state = StateManager()
    
    def run(self, user_input: str, goal: str = "Process user request") -> Dict[str, Any]:
        self.state.add_goal(goal)
        
        # Perception: Process input
        perceived = self.perception.process(user_input)
        
        # Reasoning: Analyze and plan
        reasoning_result = self.reasoning.reason(perceived, self.state.get_context())
        
        # Action: Execute plan
        action_results = self.action.execute(reasoning_result['plan'])
        
        # Observation: Evaluate and decide
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
