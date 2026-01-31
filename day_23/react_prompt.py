"""
ReAct Prompt Builder - Reasoning and Acting Pattern
"""

from typing import List, Dict, Optional


class ReActPromptBuilder:
    """Builds prompts following the ReAct (Reasoning + Acting) pattern"""
    
    REACT_INSTRUCTIONS = """Follow the ReAct pattern for problem-solving:

Thought: Reason about the current situation and what to do next
Action: Choose and execute a tool with parameters
Observation: Analyze the result from the action

Repeat this cycle until you reach the final answer."""

    REACT_EXAMPLE = """Example:
Question: What is the weather in Paris?

Thought: I need to get weather information for Paris
Action: get_weather(location="Paris")
Observation: Temperature is 18°C, partly cloudy

Thought: I have the weather information needed
Action: finish(answer="The weather in Paris is 18°C and partly cloudy")"""

    def build_react_prompt(
        self,
        question: str,
        tools: List[Dict[str, str]],
        history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """Build a complete ReAct-style prompt"""
        sections = [
            "You are an AI agent that uses the ReAct pattern.",
            self.REACT_INSTRUCTIONS,
            self._format_tools(tools),
            self.REACT_EXAMPLE
        ]
        
        if history:
            sections.append(self._format_history(history))
        
        sections.append(f"Question: {question}\n\nThought:")
        
        return "\n\n".join(sections)
    
    def _format_tools(self, tools: List[Dict[str, str]]) -> str:
        """Format tools for ReAct pattern"""
        tool_list = "\n".join(
            f"- {t['name']}: {t['description']}"
            for t in tools
        )
        return f"Available Tools:\n{tool_list}"
    
    def _format_history(self, history: List[Dict[str, str]]) -> str:
        """Format previous ReAct steps"""
        steps = "\n\n".join(
            f"{msg['role']}: {msg['content']}"
            for msg in history
        )
        return f"Previous Steps:\n{steps}"
    
    @staticmethod
    def create_example_prompt() -> str:
        """Create an example ReAct prompt for demonstration"""
        builder = ReActPromptBuilder()
        
        tools = [
            {"name": "search", "description": "Search the web for information"},
            {"name": "calculate", "description": "Perform mathematical calculations"},
            {"name": "finish", "description": "Return final answer to user"}
        ]
        
        return builder.build_react_prompt(
            question="What is 15% of 240?",
            tools=tools
        )
