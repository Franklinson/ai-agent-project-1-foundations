from reasoner import Reasoner
from planner import Planner
from decision_maker import DecisionMaker


class ReasoningSystem:
    """Integrated system combining reasoning, planning, and decision-making."""
    
    def __init__(self):
        self.reasoner = Reasoner()
        self.planner = Planner()
        self.decision_maker = DecisionMaker()
    
    def process(self, processed_input):
        """Process input through full reasoning pipeline."""
        try:
            # Step 1: Reason about the input
            reasoning_result = self.reasoner.reason(processed_input)
            
            if not reasoning_result['success']:
                return {
                    'success': False,
                    'error': reasoning_result.get('error'),
                    'stage': 'reasoning'
                }
            
            # Step 2: Create plan from goal
            goal = reasoning_result['goal']
            plan = self.planner.decompose_goal(goal, processed_input)
            
            # Step 3: Select tools for each action
            intent = processed_input.get('intent')
            entities = processed_input.get('entities', {})
            
            action_plan = []
            for step in plan.steps:
                tool_selection = self.decision_maker.select_tool(
                    intent, 
                    step['action'], 
                    entities
                )
                action_plan.append({
                    'step_id': step['id'],
                    'action': step['action'],
                    'tool': tool_selection['tool'],
                    'parameters': tool_selection['parameters'],
                    'dependencies': step['dependencies']
                })
            
            return {
                'success': True,
                'reasoning': reasoning_result['reasoning'],
                'goal': goal,
                'confidence': reasoning_result['confidence'],
                'plan': plan.to_dict(),
                'action_plan': action_plan
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'stage': 'system'
            }
