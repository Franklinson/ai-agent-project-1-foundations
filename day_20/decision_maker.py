class DecisionMaker:
    """Selects appropriate tools for actions based on intent and entities."""
    
    def __init__(self):
        self.tool_registry = {
            'search_tool': {
                'intents': ['query'],
                'actions': ['search_knowledge_base', 'identify_query'],
                'required_params': ['query']
            },
            'text_formatter': {
                'intents': ['query'],
                'actions': ['format_response', 'synthesize_results'],
                'required_params': ['text']
            },
            'command_executor': {
                'intents': ['command'],
                'actions': ['execute_operation', 'execute'],
                'required_params': ['command']
            },
            'validator': {
                'intents': ['command'],
                'actions': ['validate_command', 'validate_input'],
                'required_params': ['input']
            },
            'response_generator': {
                'intents': ['greeting', 'query'],
                'actions': ['generate_greeting', 'generate_response'],
                'required_params': ['context']
            }
        }
        
        self.entity_tool_map = {
            'dates': 'date_parser',
            'keywords': 'keyword_extractor'
        }
    
    def select_tool(self, intent, action, entities=None):
        """Select appropriate tool for given intent and action."""
        try:
            candidates = self._find_candidate_tools(intent, action)
            
            if not candidates:
                return {
                    'success': False,
                    'tool': None,
                    'parameters': {},
                    'reason': 'No matching tool found'
                }
            
            selected = self._rank_and_select(candidates, entities)
            parameters = self._build_parameters(selected, intent, action, entities)
            
            return {
                'success': True,
                'tool': selected,
                'parameters': parameters,
                'reason': f'Selected {selected} for {action}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'tool': None,
                'parameters': {},
                'reason': f'Error: {str(e)}'
            }
    
    def _find_candidate_tools(self, intent, action):
        """Find tools that match intent and action."""
        candidates = []
        for tool_name, tool_spec in self.tool_registry.items():
            if intent in tool_spec['intents'] and action in tool_spec['actions']:
                candidates.append(tool_name)
        return candidates
    
    def _rank_and_select(self, candidates, entities):
        """Rank candidates and select best tool."""
        if len(candidates) == 1:
            return candidates[0]
        
        if entities:
            for tool in candidates:
                if any(entity in self.entity_tool_map for entity in entities.keys()):
                    return tool
        
        return candidates[0]
    
    def _build_parameters(self, tool, intent, action, entities):
        """Build parameters for selected tool."""
        tool_spec = self.tool_registry.get(tool, {})
        params = {}
        
        for param in tool_spec.get('required_params', []):
            if param == 'query' and entities:
                params['query'] = entities.get('keywords', [''])[0] if entities.get('keywords') else ''
            elif param == 'command':
                params['command'] = action
            elif param == 'input':
                params['input'] = entities if entities else {}
            elif param == 'text':
                params['text'] = ''
            elif param == 'context':
                params['context'] = {'intent': intent, 'entities': entities}
        
        return params
