"""
Dynamic Prompt Builder for AI Agents
"""

from typing import List, Dict, Optional


class PromptBuilder:
    """Dynamically builds prompts based on current state"""
    
    def __init__(self, system_role: str = "helpful AI assistant"):
        self.system_role = system_role
    
    def build_prompt(
        self,
        user_input: str,
        tools: Optional[List[Dict[str, str]]] = None,
        context: Optional[List[Dict[str, str]]] = None,
        goal: Optional[str] = None
    ) -> str:
        """Build complete prompt dynamically based on available information"""
        sections = []
        
        # System role
        sections.append(f"You are a {self.system_role}.")
        
        # Goal if provided
        if goal:
            sections.append(f"Current Goal: {goal}")
        
        # Tools if available
        if tools:
            sections.append(self._format_tools(tools))
        
        # Context if available
        if context:
            sections.append(self._format_context(context))
        
        # User input
        sections.append(f"User: {user_input}")
        
        return "\n\n".join(sections)
    
    def _format_tools(self, tools: List[Dict[str, str]]) -> str:
        """Format tool descriptions"""
        tool_list = "\n".join(
            f"- {t['name']}: {t['description']}"
            for t in tools
        )
        return f"Available Tools:\n{tool_list}"
    
    def _format_context(self, context: List[Dict[str, str]]) -> str:
        """Format conversation context"""
        history = "\n".join(
            f"{msg['role']}: {msg['content']}"
            for msg in context[-5:]  # Last 5 messages
        )
        return f"Recent Context:\n{history}"
