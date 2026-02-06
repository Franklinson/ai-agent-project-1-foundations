from typing import Dict, List, Any

class StateManager:
    def __init__(self):
        self.conversation_history: List[Dict[str, Any]] = []
        self.goals: List[str] = []
        self.context: Dict[str, Any] = {}
    
    def add_to_history(self, entry: Dict[str, Any]) -> None:
        self.conversation_history.append(entry)
    
    def get_history(self) -> List[Dict[str, Any]]:
        return self.conversation_history
    
    def add_goal(self, goal: str) -> None:
        self.goals.append(goal)
    
    def get_goals(self) -> List[str]:
        return self.goals
    
    def update_context(self, key: str, value: Any) -> None:
        self.context[key] = value
    
    def get_context(self) -> Dict[str, Any]:
        return self.context
