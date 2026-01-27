class Plan:
    """Structured plan with ordered steps."""
    
    def __init__(self, goal, steps, sub_goals):
        self.goal = goal
        self.steps = steps
        self.sub_goals = sub_goals
    
    def to_dict(self):
        return {
            'goal': self.goal,
            'sub_goals': self.sub_goals,
            'steps': self.steps,
            'total_steps': len(self.steps)
        }


class Planner:
    """Decomposes goals into actionable steps."""
    
    def __init__(self):
        self.goal_decomposition = {
            'retrieve_information': ['identify_query', 'search_data', 'synthesize_results'],
            'execute_action': ['validate_input', 'prepare_resources', 'execute', 'verify'],
            'acknowledge_user': ['generate_response']
        }
        
        self.step_dependencies = {
            'retrieve_information': {
                'search_data': ['identify_query'],
                'synthesize_results': ['search_data']
            },
            'execute_action': {
                'prepare_resources': ['validate_input'],
                'execute': ['prepare_resources'],
                'verify': ['execute']
            }
        }
    
    def decompose_goal(self, goal, context=None):
        """Decompose goal into actionable plan."""
        try:
            sub_goals = self.goal_decomposition.get(goal, ['handle_unknown'])
            
            steps = self._create_steps(goal, sub_goals, context)
            
            ordered_steps = self._order_steps(goal, steps)
            
            return Plan(goal, ordered_steps, sub_goals)
            
        except Exception as e:
            return Plan(goal, [{'action': 'error', 'details': str(e)}], [])
    
    def _create_steps(self, goal, sub_goals, context):
        """Convert sub-goals into actionable steps."""
        steps = []
        for idx, sub_goal in enumerate(sub_goals):
            step = {
                'id': idx + 1,
                'action': sub_goal,
                'status': 'pending',
                'dependencies': self._get_dependencies(goal, sub_goal)
            }
            if context:
                step['context'] = context
            steps.append(step)
        return steps
    
    def _get_dependencies(self, goal, sub_goal):
        """Get dependencies for a sub-goal."""
        deps = self.step_dependencies.get(goal, {})
        return deps.get(sub_goal, [])
    
    def _order_steps(self, goal, steps):
        """Order steps based on dependencies."""
        ordered = []
        completed = set()
        
        while len(ordered) < len(steps):
            for step in steps:
                if step['action'] in completed:
                    continue
                
                deps = step['dependencies']
                if all(dep in completed for dep in deps):
                    ordered.append(step)
                    completed.add(step['action'])
        
        return ordered
