"""
Chain-of-Thought (CoT) Prompt Builder for AI Agents
Implements step-by-step reasoning patterns for complex tasks
"""

from typing import List, Dict, Optional


class CoTPromptBuilder:
    """Builds prompts with Chain-of-Thought reasoning patterns"""
    
    COT_INSTRUCTION = """Think step-by-step to solve this task:

1. Understand: Analyze the task and identify what needs to be done
2. Plan: Break down the solution into logical steps
3. Execute: Work through each step systematically
4. Verify: Check if the solution addresses the original task

Show your reasoning at each step."""

    TASK_TEMPLATES = {
        "analysis": """Analyze the following step-by-step:
1. What is the main question or problem?
2. What information do we have?
3. What information is missing?
4. What approach should we take?
5. What is the conclusion?""",
        
        "problem_solving": """Solve this problem step-by-step:
1. Identify the problem clearly
2. List known facts and constraints
3. Consider possible solutions
4. Evaluate each solution
5. Choose and implement the best solution
6. Verify the result""",
        
        "decision_making": """Make this decision step-by-step:
1. Define the decision to be made
2. List all available options
3. Identify criteria for evaluation
4. Analyze pros and cons of each option
5. Make the decision based on analysis
6. Explain the reasoning""",
        
        "planning": """Create a plan step-by-step:
1. Define the goal clearly
2. Identify required resources and constraints
3. Break down into subtasks
4. Order tasks logically
5. Identify dependencies
6. Create timeline and milestones""",
        
        "debugging": """Debug this issue step-by-step:
1. What is the expected behavior?
2. What is the actual behavior?
3. Where does the error occur?
4. What could cause this error?
5. Test each hypothesis
6. Implement and verify the fix"""
    }

    def __init__(self, system_role: str = "analytical AI assistant"):
        self.system_role = system_role

    def build_cot_prompt(
        self,
        task: str,
        tools: Optional[List[Dict[str, str]]] = None,
        context: Optional[str] = None,
        task_type: str = "problem_solving"
    ) -> str:
        """Build a Chain-of-Thought prompt for the given task"""
        sections = [
            f"You are a {self.system_role}.",
            self.COT_INSTRUCTION
        ]
        
        if task_type in self.TASK_TEMPLATES:
            sections.append(self.TASK_TEMPLATES[task_type])
        
        if tools:
            sections.append(self._format_tools_cot(tools))
        
        if context:
            sections.append(f"Context:\n{context}")
        
        sections.append(f"Task: {task}")
        sections.append("\nLet's work through this step-by-step:")
        
        return "\n\n".join(sections)

    def build_few_shot_cot(
        self,
        task: str,
        examples: List[Dict[str, str]],
        tools: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """Build CoT prompt with few-shot examples"""
        sections = [
            f"You are a {self.system_role}.",
            "Learn from these examples of step-by-step reasoning:\n"
        ]
        
        for i, example in enumerate(examples, 1):
            sections.append(f"Example {i}:")
            sections.append(f"Task: {example['task']}")
            sections.append(f"Reasoning:\n{example['reasoning']}")
            sections.append(f"Answer: {example['answer']}\n")
        
        if tools:
            sections.append(self._format_tools_cot(tools))
        
        sections.append(f"Now solve this task using the same step-by-step approach:")
        sections.append(f"Task: {task}")
        sections.append("\nStep-by-step reasoning:")
        
        return "\n\n".join(sections)

    def build_tool_use_cot(
        self,
        task: str,
        tools: List[Dict[str, str]],
        context: Optional[str] = None
    ) -> str:
        """Build CoT prompt specifically for tool usage"""
        sections = [
            f"You are a {self.system_role} with access to tools.",
            """When using tools, think step-by-step:

1. Understand what the user needs
2. Identify which tool(s) can help
3. Determine the correct parameters
4. Execute the tool call
5. Interpret the results
6. Provide a clear answer to the user""",
            self._format_tools_cot(tools)
        ]
        
        if context:
            sections.append(f"Context:\n{context}")
        
        sections.append(f"User Request: {task}")
        sections.append("\nStep-by-step reasoning:")
        
        return "\n\n".join(sections)

    def _format_tools_cot(self, tools: List[Dict[str, str]]) -> str:
        """Format tools with CoT reasoning guidance"""
        tool_list = "\n".join(
            f"- {t['name']}: {t['description']}"
            for t in tools
        )
        return f"""Available Tools:
{tool_list}

When selecting tools, explain:
- Why this tool is appropriate
- What parameters are needed
- What result you expect"""

    @staticmethod
    def get_cot_examples() -> Dict[str, Dict[str, str]]:
        """Return example CoT reasoning patterns"""
        return {
            "math": {
                "task": "If a store has 15 apples and sells 40% of them, how many are left?",
                "reasoning": """Step 1: Identify what we know
- Total apples: 15
- Percentage sold: 40%

Step 2: Calculate apples sold
- 40% of 15 = 0.40 × 15 = 6 apples

Step 3: Calculate remaining apples
- Remaining = Total - Sold
- Remaining = 15 - 6 = 9 apples

Step 4: Verify
- Sold 6 out of 15 = 40% ✓
- 6 + 9 = 15 ✓""",
                "answer": "9 apples remain"
            },
            
            "logic": {
                "task": "All cats are mammals. Fluffy is a cat. Is Fluffy a mammal?",
                "reasoning": """Step 1: Identify the premises
- Premise 1: All cats are mammals
- Premise 2: Fluffy is a cat

Step 2: Apply logical reasoning
- If all cats are mammals (universal statement)
- And Fluffy is a cat (specific case)
- Then Fluffy must be a mammal (logical conclusion)

Step 3: Verify the logic
- This follows the valid syllogism pattern
- No contradictions exist""",
                "answer": "Yes, Fluffy is a mammal"
            },
            
            "tool_selection": {
                "task": "Find the weather in Paris and send an email about it",
                "reasoning": """Step 1: Break down the request
- Need to: Get weather data
- Need to: Send email with that data

Step 2: Identify required tools
- get_weather(location) - to fetch Paris weather
- send_email(to, subject, body) - to send the email

Step 3: Determine execution order
- First: Call get_weather("Paris")
- Second: Use result to compose email
- Third: Call send_email with weather info

Step 4: Plan parameters
- get_weather needs: location="Paris"
- send_email needs: recipient, subject, weather data in body""",
                "answer": "Use get_weather first, then send_email with results"
            }
        }
