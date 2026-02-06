from typing import Dict, List, Any

class ObservationModule:
    def __init__(self):
        pass
    
    def observe(self, results: List[Dict[str, Any]], goal: str) -> Dict[str, Any]:
        evaluation = self._evaluate(results)
        reflection = self._reflect(evaluation, results)
        decision = self._decide(evaluation, reflection)
        
        return {
            'evaluation': evaluation,
            'reflection': reflection,
            'decision': decision
        }
    
    def _evaluate(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        total = len(results)
        successful = sum(1 for r in results if r.get('status') == 'success')
        failed = total - successful
        
        return {
            'total_actions': total,
            'successful': successful,
            'failed': failed,
            'success_rate': successful / total if total > 0 else 0
        }
    
    def _reflect(self, evaluation: Dict[str, Any], results: List[Dict[str, Any]]) -> Dict[str, Any]:
        errors = [r.get('error') for r in results if r.get('status') == 'error']
        
        return {
            'all_successful': evaluation['failed'] == 0,
            'has_errors': len(errors) > 0,
            'error_messages': errors,
            'quality': 'high' if evaluation['success_rate'] > 0.8 else 'low'
        }
    
    def _decide(self, evaluation: Dict[str, Any], reflection: Dict[str, Any]) -> str:
        if reflection['all_successful']:
            return 'complete'
        elif evaluation['success_rate'] > 0:
            return 'continue'
        else:
            return 'error'
