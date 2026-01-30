class Reflector:
    def __init__(self):
        self.experiences = []
    
    def analyze_outcome(self, result, evaluation):
        """Analyze the outcome of an action."""
        success = evaluation.get('success', False)
        quality_score = evaluation.get('quality', {}).get('score', 0)
        progress = evaluation.get('progress', {}).get('progress', 0)
        
        return {
            'outcome': 'positive' if success and quality_score > 70 else 'negative',
            'quality_score': quality_score,
            'progress_level': progress,
            'had_errors': len(evaluation.get('errors', [])) > 0
        }
    
    def extract_lessons(self, result, evaluation):
        """Extract lessons from the experience."""
        lessons = []
        
        if evaluation.get('success'):
            lessons.append('Action executed successfully')
            if evaluation.get('quality', {}).get('score', 0) == 100:
                lessons.append('High quality result achieved')
        else:
            lessons.append('Action failed - review approach')
        
        for error in evaluation.get('errors', []):
            lessons.append(f"Error encountered: {error.get('type')}")
        
        progress_status = evaluation.get('progress', {}).get('status')
        if progress_status == 'complete':
            lessons.append('Goal fully achieved')
        elif progress_status == 'partial':
            lessons.append('Goal partially achieved - may need follow-up')
        
        return lessons
    
    def suggest_improvements(self, result, evaluation):
        """Suggest improvements based on evaluation."""
        suggestions = []
        
        if not evaluation.get('success'):
            suggestions.append('Retry with different parameters')
            suggestions.append('Verify input data validity')
        
        quality_issues = evaluation.get('quality', {}).get('issues', [])
        if quality_issues:
            suggestions.append(f'Address quality issues: {", ".join(quality_issues)}')
        
        progress = evaluation.get('progress', {}).get('progress', 0)
        if progress < 100:
            suggestions.append('Consider additional actions to complete goal')
        
        return suggestions if suggestions else ['Continue current approach']
    
    def reflect(self, result, evaluation):
        """Perform comprehensive reflection and store experience."""
        analysis = self.analyze_outcome(result, evaluation)
        lessons = self.extract_lessons(result, evaluation)
        improvements = self.suggest_improvements(result, evaluation)
        
        experience = {
            'result': result,
            'evaluation': evaluation,
            'analysis': analysis,
            'lessons': lessons,
            'improvements': improvements
        }
        
        self.experiences.append(experience)
        
        return {
            'analysis': analysis,
            'lessons': lessons,
            'improvements': improvements,
            'total_experiences': len(self.experiences)
        }
