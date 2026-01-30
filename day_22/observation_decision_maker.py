class ObservationDecisionMaker:
    COMPLETE = 'COMPLETE'
    CONTINUE = 'CONTINUE'
    RETRY = 'RETRY'
    TRY_ALTERNATIVE = 'TRY_ALTERNATIVE'
    ABORT = 'ABORT'
    
    def __init__(self):
        self.attempt_history = []
    
    def is_goal_achieved(self, evaluation, goal):
        """Check if goal is achieved."""
        progress = evaluation.get('progress', {})
        return (
            evaluation.get('success', False) and
            progress.get('status') == 'complete' and
            progress.get('progress', 0) >= 100
        )
    
    def handle_errors(self, evaluation):
        """Determine action based on errors."""
        errors = evaluation.get('errors', [])
        
        if not errors:
            return None
        
        error_types = [e.get('type') for e in errors]
        
        if 'validation' in error_types:
            return self.TRY_ALTERNATIVE
        if 'execution' in error_types:
            return self.RETRY
        
        return self.ABORT
    
    def decide(self, evaluation, goal):
        """Make decision based on evaluation and goal."""
        self.attempt_history.append(evaluation)
        
        # Check if goal achieved
        if self.is_goal_achieved(evaluation, goal):
            return {
                'decision': self.COMPLETE,
                'reason': 'Goal achieved successfully',
                'confidence': 1.0
            }
        
        # Handle errors
        error_decision = self.handle_errors(evaluation)
        if error_decision:
            attempts = len(self.attempt_history)
            if error_decision == self.RETRY and attempts >= 3:
                return {
                    'decision': self.ABORT,
                    'reason': 'Max retry attempts reached',
                    'confidence': 0.9
                }
            return {
                'decision': error_decision,
                'reason': f'Error handling: {error_decision}',
                'confidence': 0.7
            }
        
        # Check progress
        progress = evaluation.get('progress', {}).get('progress', 0)
        status = evaluation.get('progress', {}).get('status', 'minimal')
        
        if status == 'partial' and progress >= 50:
            return {
                'decision': self.CONTINUE,
                'reason': 'Partial progress made, continue',
                'confidence': 0.8
            }
        
        # Check if stuck
        if len(self.attempt_history) >= 2:
            recent_progress = [
                e.get('progress', {}).get('progress', 0) 
                for e in self.attempt_history[-2:]
            ]
            if all(p < 30 for p in recent_progress):
                return {
                    'decision': self.TRY_ALTERNATIVE,
                    'reason': 'Stuck with minimal progress',
                    'confidence': 0.75
                }
        
        return {
            'decision': self.CONTINUE,
            'reason': 'Continue current approach',
            'confidence': 0.6
        }
