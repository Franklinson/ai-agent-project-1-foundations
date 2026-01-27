class Reasoner:
    """Analyzes processed input and identifies goals and actions."""
    
    def __init__(self):
        self.intent_goals = {
            'query': 'retrieve_information',
            'command': 'execute_action',
            'greeting': 'acknowledge_user'
        }
        
        self.action_map = {
            'query': ['search_knowledge_base', 'format_response'],
            'command': ['validate_command', 'execute_operation', 'confirm_result'],
            'greeting': ['generate_greeting']
        }
    
    def reason(self, processed_input):
        """Analyze input and return structured reasoning results."""
        try:
            intent = processed_input.get('intent', 'unknown')
            entities = processed_input.get('entities', {})
            text = processed_input.get('text', '')
            
            if intent == 'unknown':
                return {
                    'success': False,
                    'error': 'Unable to determine intent',
                    'goal': None,
                    'actions': [],
                    'reasoning': 'Intent classification failed'
                }
            
            goal = self.intent_goals.get(intent, 'handle_unknown')
            actions = self.action_map.get(intent, ['log_unknown_intent'])
            
            reasoning = self._generate_reasoning(intent, entities, text)
            
            return {
                'success': True,
                'goal': goal,
                'actions': actions,
                'reasoning': reasoning,
                'confidence': self._calculate_confidence(intent, entities)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'goal': None,
                'actions': [],
                'reasoning': f'Error during reasoning: {str(e)}'
            }
    
    def _generate_reasoning(self, intent, entities, text):
        """Generate reasoning explanation."""
        reasoning = f"Detected intent: {intent}. "
        
        if entities:
            reasoning += f"Found entities: {list(entities.keys())}. "
        
        if intent == 'query':
            reasoning += "User is seeking information."
        elif intent == 'command':
            reasoning += "User wants to execute an action."
        elif intent == 'greeting':
            reasoning += "User is initiating conversation."
        
        return reasoning
    
    def _calculate_confidence(self, intent, entities):
        """Calculate confidence score."""
        base_confidence = 0.7
        
        if intent != 'unknown':
            base_confidence += 0.2
        
        if entities:
            base_confidence += 0.1
        
        return min(base_confidence, 1.0)
