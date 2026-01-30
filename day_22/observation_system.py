from result_evaluator import ResultEvaluator
from reflector import Reflector
from observation_decision_maker import ObservationDecisionMaker


class ObservationSystem:
    def __init__(self):
        self.evaluator = ResultEvaluator()
        self.reflector = Reflector()
        self.decision_maker = ObservationDecisionMaker()
    
    def observe(self, action_results, goal):
        """Observe action results and make decisions."""
        observations = []
        
        for result in action_results:
            # Evaluate result
            evaluation = self.evaluator.evaluate(result, goal)
            
            # Reflect on outcome
            reflection = self.reflector.reflect(result, evaluation)
            
            # Make decision
            decision = self.decision_maker.decide(evaluation, goal)
            
            observations.append({
                'result': result,
                'evaluation': evaluation,
                'reflection': reflection,
                'decision': decision
            })
        
        # Determine overall decision
        decisions = [obs['decision']['decision'] for obs in observations]
        
        if ObservationDecisionMaker.COMPLETE in decisions:
            overall_decision = ObservationDecisionMaker.COMPLETE
        elif ObservationDecisionMaker.ABORT in decisions:
            overall_decision = ObservationDecisionMaker.ABORT
        elif ObservationDecisionMaker.TRY_ALTERNATIVE in decisions:
            overall_decision = ObservationDecisionMaker.TRY_ALTERNATIVE
        elif ObservationDecisionMaker.RETRY in decisions:
            overall_decision = ObservationDecisionMaker.RETRY
        else:
            overall_decision = ObservationDecisionMaker.CONTINUE
        
        return {
            'observations': observations,
            'overall_decision': overall_decision,
            'total_experiences': len(self.reflector.experiences)
        }
