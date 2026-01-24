import re
from datetime import datetime


class IntentClassifier:
    """Classifies user intent based on keywords."""
    
    def __init__(self):
        self.intents = {
            'query': ['what', 'how', 'why', 'when', 'where', 'who', 'explain', 'tell me'],
            'command': ['create', 'delete', 'update', 'run', 'execute', 'start', 'stop'],
            'greeting': ['hello', 'hi', 'hey', 'greetings']
        }
    
    def classify(self, text):
        """Classify intent from text."""
        text_lower = text.lower()
        
        for intent, keywords in self.intents.items():
            if any(keyword in text_lower for keyword in keywords):
                return intent
        
        return 'unknown'


class EntityExtractor:
    """Extracts entities from text."""
    
    def __init__(self):
        self.date_pattern = r'\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}/\d{1,2}/\d{4}\b'
    
    def extract(self, text):
        """Extract entities from text."""
        entities = {}
        
        dates = re.findall(self.date_pattern, text)
        if dates:
            entities['dates'] = dates
        
        words = text.split()
        keywords = [w for w in words if len(w) > 3 and w[0].isupper()]
        if keywords:
            entities['keywords'] = keywords
        
        return entities


class InputParser:
    """Parses input text to extract intent and entities."""
    
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.entity_extractor = EntityExtractor()
    
    def parse(self, text):
        """Parse text and return structured output."""
        try:
            intent = self.intent_classifier.classify(text)
            entities = self.entity_extractor.extract(text)
            
            return {
                'intent': intent,
                'entities': entities,
                'text': text
            }
        except Exception as e:
            return {
                'intent': 'unknown',
                'entities': {},
                'text': text,
                'error': str(e)
            }
