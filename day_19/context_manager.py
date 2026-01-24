from collections import defaultdict
from datetime import datetime


class ContextManager:
    """Manages conversation history and context enrichment."""
    
    def __init__(self):
        self.history = defaultdict(list)
        self.preferences = defaultdict(dict)
    
    def store_message(self, user_id, message):
        """Store a message in conversation history."""
        self.history[user_id].append({
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_recent_messages(self, user_id, limit=5):
        """Retrieve recent messages for a user."""
        return self.history[user_id][-limit:] if user_id in self.history else []
    
    def set_preference(self, user_id, key, value):
        """Set user preference."""
        self.preferences[user_id][key] = value
    
    def get_preference(self, user_id, key, default=None):
        """Get user preference."""
        return self.preferences[user_id].get(key, default)
    
    def enrich(self, parsed_input, user_id):
        """Enrich parsed input with context."""
        recent_messages = self.get_recent_messages(user_id)
        user_prefs = self.preferences.get(user_id, {})
        
        enriched = {
            **parsed_input,
            'context': {
                'recent_messages': recent_messages,
                'preferences': user_prefs,
                'message_count': len(self.history[user_id])
            }
        }
        
        return enriched
