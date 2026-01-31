"""
Prompt Template System for AI Agents
"""

from typing import List, Dict, Optional


class PromptTemplates:
    """Template system for building agent prompts"""
    
    SYSTEM_INSTRUCTIONS = """You are an AI assistant with the following capabilities:
{capabilities}

Your role: {role}

Guidelines:
{guidelines}"""

    TOOL_DESCRIPTION = """Available Tools:
{tools}

Tool Usage Instructions:
- Use tools when necessary to complete tasks
- Provide all required parameters
- Handle tool responses appropriately"""

    CONTEXT_TEMPLATE = """Conversation History:
{history}

Current Context:
{context}"""

    @staticmethod
    def format_system_prompt(
        capabilities: List[str],
        role: str,
        guidelines: List[str]
    ) -> str:
        """Format system instructions"""
        return PromptTemplates.SYSTEM_INSTRUCTIONS.format(
            capabilities="\n".join(f"- {c}" for c in capabilities),
            role=role,
            guidelines="\n".join(f"- {g}" for g in guidelines)
        )

    @staticmethod
    def format_tools(tools: List[Dict[str, str]]) -> str:
        """Format tool descriptions"""
        tool_list = "\n\n".join(
            f"{i+1}. {t['name']}: {t['description']}"
            for i, t in enumerate(tools)
        )
        return PromptTemplates.TOOL_DESCRIPTION.format(tools=tool_list)

    @staticmethod
    def format_context(
        history: List[Dict[str, str]],
        context: Optional[str] = None
    ) -> str:
        """Format conversation history and context"""
        history_text = "\n".join(
            f"{msg['role']}: {msg['content']}"
            for msg in history
        )
        return PromptTemplates.CONTEXT_TEMPLATE.format(
            history=history_text or "No previous messages",
            context=context or "No additional context"
        )

    @staticmethod
    def build_full_prompt(
        capabilities: List[str],
        role: str,
        guidelines: List[str],
        tools: Optional[List[Dict[str, str]]] = None,
        history: Optional[List[Dict[str, str]]] = None,
        context: Optional[str] = None
    ) -> str:
        """Combine all templates into a full prompt"""
        sections = [
            PromptTemplates.format_system_prompt(capabilities, role, guidelines)
        ]
        
        if tools:
            sections.append(PromptTemplates.format_tools(tools))
        
        if history:
            sections.append(PromptTemplates.format_context(history, context))
        
        return "\n\n---\n\n".join(sections)
