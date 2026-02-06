import re
from typing import Dict, List, Any

class PerceptionModule:
    def __init__(self):
        self.intent_keywords = {
            'question': ['what', 'how', 'why', 'when', 'where', 'who', '?'],
            'request': ['please', 'can you', 'could you', 'help', 'need'],
            'command': ['create', 'delete', 'update', 'run', 'execute', 'start', 'stop'],
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon']
        }
        
    def process(self, user_input: str) -> Dict[str, Any]:
        normalized_text = self._normalize_input(user_input)
        intent = self._extract_intent(normalized_text)
        entities = self._extract_entities(normalized_text)
        
        return {
            'text': normalized_text,
            'intent': intent,
            'entities': entities
        }
    
    def _normalize_input(self, text: str) -> str:
        return text.strip().lower()
    
    def _extract_intent(self, text: str) -> str:
        for intent, keywords in self.intent_keywords.items():
            if any(keyword in text for keyword in keywords):
                return intent
        return 'unknown'
    
    def _extract_entities(self, text: str) -> List[Dict[str, str]]:
        entities = []
        
        # Extract emails
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        entities.extend([{'type': 'email', 'value': email} for email in emails])
        
        # Extract numbers
        numbers = re.findall(r'\b\d+\b', text)
        entities.extend([{'type': 'number', 'value': num} for num in numbers])
        
        # Extract dates (simple format)
        dates = re.findall(r'\b\d{1,2}/\d{1,2}/\d{4}\b', text)
        entities.extend([{'type': 'date', 'value': date} for date in dates])
        
        return entities