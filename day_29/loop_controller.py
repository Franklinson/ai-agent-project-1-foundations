import sys
sys.path.append('../day_27')

from typing import Dict, Any
from perception import PerceptionModule
from reasoning import ReasoningModule
from action import ActionModule
from observation import ObservationModule
from state_manager import StateManager


class LoopController:
    def __init__(self):
        self.perception = PerceptionModule()
        self.reasoning = ReasoningModule()
        self.action = ActionModule()
        self.observation = ObservationModule()
        self.state = StateManager()
        self.iteration_count = 0
        self.progress = []
    
    def run(self, user_input: str, goal: str, max_iterations: int = 5) -> Dict[str, Any]:
        self.state.add_goal(goal)
        self.iteration_count = 0
        self.progress = []
        termination_reason = None
        errors = []
        
        try:
            while self.iteration_count < max_iterations:
                self.iteration_count += 1
                
                # Perception with error handling
                perceived = self._safe_perception(user_input, errors)
                if perceived is None:
                    break
                
                # Reasoning with error handling
                reasoning_result = self._safe_reasoning(perceived, errors)
                if reasoning_result is None:
                    break
                
                # Action with error handling
                action_results = self._safe_action(reasoning_result['plan'], errors)
                if action_results is None:
                    break
                
                # Observation with error handling
                observation = self._safe_observation(action_results, goal, errors)
                if observation is None:
                    break
                
                # Track progress
                self._track_progress(observation)
                
                # Update state
                self.state.add_to_history({
                    'iteration': self.iteration_count,
                    'perceived': perceived,
                    'reasoning': reasoning_result,
                    'actions': action_results,
                    'observation': observation,
                    'errors': errors.copy()
                })
                
                # Check termination conditions
                termination_reason = self._check_termination(observation, max_iterations)
                if termination_reason:
                    break
            
            # Set termination reason if max iterations reached
            if not termination_reason:
                termination_reason = 'max_iterations_reached'
            
            return {
                'status': 'success',
                'iterations': self.iteration_count,
                'final_decision': observation['decision'],
                'termination_reason': termination_reason,
                'progress': self.progress,
                'errors': errors,
                'history': self.state.get_history()
            }
        
        except Exception as e:
            errors.append({'phase': 'loop', 'error': str(e)})
            return {
                'status': 'error',
                'error': str(e),
                'iterations': self.iteration_count,
                'termination_reason': 'loop_error',
                'progress': self.progress,
                'errors': errors,
                'history': self.state.get_history()
            }
    
    def _check_termination(self, observation: Dict[str, Any], max_iterations: int) -> str:
        """Check if loop should terminate"""
        decision = observation['decision']
        
        # Goal achieved
        if decision == 'complete':
            return 'goal_achieved'
        
        # Error requiring termination
        if decision == 'error':
            return 'error_termination'
        
        # Max iterations check handled by while loop
        return None
    
    def _track_progress(self, observation: Dict[str, Any]) -> None:
        """Track progress across iterations"""
        self.progress.append({
            'iteration': self.iteration_count,
            'success_rate': observation['evaluation']['success_rate'],
            'decision': observation['decision']
        })
    
    def _safe_perception(self, user_input: str, errors: list) -> Dict[str, Any]:
        """Handle perception errors"""
        try:
            return self.perception.process(user_input)
        except Exception as e:
            errors.append({'phase': 'perception', 'error': str(e)})
            # Recovery: return minimal valid structure
            return {'text': user_input, 'intent': 'unknown', 'entities': []}
    
    def _safe_reasoning(self, perceived: Dict[str, Any], errors: list) -> Dict[str, Any]:
        """Handle reasoning errors"""
        try:
            return self.reasoning.reason(perceived, self.state.get_context())
        except Exception as e:
            errors.append({'phase': 'reasoning', 'error': str(e)})
            # Recovery: return fallback plan
            return {'analysis': {}, 'plan': [{'action': 'fallback', 'tool': 'fallback_tool', 'priority': 1}]}
    
    def _safe_action(self, plan: list, errors: list) -> list:
        """Handle action errors"""
        try:
            return self.action.execute(plan)
        except Exception as e:
            errors.append({'phase': 'action', 'error': str(e)})
            # Recovery: return error result
            return [{'action': 'error', 'tool': 'none', 'status': 'error', 'error': str(e)}]
    
    def _safe_observation(self, action_results: list, goal: str, errors: list) -> Dict[str, Any]:
        """Handle observation errors"""
        try:
            return self.observation.observe(action_results, goal)
        except Exception as e:
            errors.append({'phase': 'observation', 'error': str(e)})
            # Recovery: return error decision
            return {
                'evaluation': {'total_actions': 0, 'successful': 0, 'failed': 0, 'success_rate': 0},
                'reflection': {'all_successful': False, 'has_errors': True, 'error_messages': [str(e)], 'quality': 'low'},
                'decision': 'error'
            }
