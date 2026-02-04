"""
Advanced Prompt System - Unified Interface
Combines CoT, Tool Chaining, Multi-Step Planning, and Error Recovery
"""

from typing import List, Dict, Optional
from cot_prompt_builder import CoTPromptBuilder
from tool_chaining_prompts import ToolChainingPromptBuilder
from multi_step_prompts import MultiStepPromptBuilder
from error_recovery_prompts import ErrorRecoveryPromptBuilder


class AdvancedPromptSystem:
    """Unified interface for all advanced prompt techniques"""
    
    def __init__(self):
        self.cot = CoTPromptBuilder()
        self.chaining = ToolChainingPromptBuilder()
        self.multi_step = MultiStepPromptBuilder()
        self.error = ErrorRecoveryPromptBuilder()
    
    def build_prompt(
        self,
        task: str,
        techniques: List[str],
        tools: Optional[List[Dict[str, str]]] = None,
        steps: Optional[List[str]] = None,
        context: Optional[str] = None
    ) -> str:
        """Build prompt combining specified techniques"""
        sections = ["You are an advanced AI assistant."]
        
        if "cot" in techniques:
            sections.append(self.cot.COT_INSTRUCTION)
        
        if "multi_step" in techniques:
            sections.append(self.multi_step.MULTI_STEP_INSTRUCTION)
        
        if "chaining" in techniques and tools:
            sections.append(self.chaining.CHAINING_INSTRUCTION)
            sections.append(self._format_tools(tools))
        
        if "error_recovery" in techniques:
            sections.append(self.error.ERROR_RECOVERY_INSTRUCTION)
        
        if steps:
            sections.append("Steps:\n" + "\n".join(f"{i}. {s}" for i, s in enumerate(steps, 1)))
        
        if context:
            sections.append(f"Context:\n{context}")
        
        sections.append(f"Task: {task}\n\nBegin:")
        
        return "\n\n".join(sections)
    
    def build_all(
        self,
        task: str,
        tools: List[Dict[str, str]],
        context: Optional[str] = None
    ) -> str:
        """Build prompt with all techniques enabled"""
        return self.build_prompt(
            task,
            techniques=["cot", "chaining", "multi_step", "error_recovery"],
            tools=tools,
            context=context
        )
    
    def _format_tools(self, tools: List[Dict[str, str]]) -> str:
        """Format tools list"""
        return "Available Tools:\n" + "\n".join(f"- {t['name']}: {t['description']}" for t in tools)
