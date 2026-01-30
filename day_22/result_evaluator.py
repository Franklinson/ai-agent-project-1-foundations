class ResultEvaluator:
    def check_success(self, result):
        """Determine if result indicates success."""
        return result.get('success', False) and result.get('valid', True)
    
    def assess_quality(self, result):
        """Assess quality of result."""
        if not self.check_success(result):
            return {'score': 0, 'issues': ['Execution failed']}
        
        observation = result.get('observation', '')
        score = 100 if observation else 50
        issues = [] if observation else ['No observation data']
        
        return {'score': score, 'issues': issues}
    
    def assess_progress(self, result, goal):
        """Evaluate progress toward goal."""
        if not self.check_success(result):
            return {'progress': 0, 'status': 'failed'}
        
        observation = str(result.get('observation', '')).lower()
        goal_lower = str(goal).lower()
        
        if goal_lower in observation:
            return {'progress': 100, 'status': 'complete'}
        elif observation:
            return {'progress': 50, 'status': 'partial'}
        return {'progress': 25, 'status': 'minimal'}
    
    def identify_errors(self, result):
        """Identify errors in result."""
        errors = []
        
        if not result.get('valid', True):
            errors.append({'type': 'validation', 'message': result.get('observation', 'Invalid format')})
        
        if not result.get('success', False):
            errors.append({'type': 'execution', 'message': result.get('observation', 'Execution failed')})
        
        return errors
    
    def evaluate(self, result, goal):
        """Comprehensive evaluation of result against goal."""
        return {
            'success': self.check_success(result),
            'quality': self.assess_quality(result),
            'progress': self.assess_progress(result, goal),
            'errors': self.identify_errors(result)
        }
