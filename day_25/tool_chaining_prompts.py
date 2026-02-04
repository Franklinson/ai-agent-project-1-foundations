"""
Tool Chaining Prompt Builder for AI Agents
Implements patterns for sequential tool usage and result passing
"""

from typing import List, Dict, Optional


class ToolChainingPromptBuilder:
    """Builds prompts for chaining multiple tools together"""
    
    CHAINING_INSTRUCTION = """Execute tools in sequence, passing results between them:

1. Identify all tools needed for the complete task
2. Determine the correct execution order
3. Execute first tool and capture result
4. Pass relevant data to next tool
5. Continue until task is complete
6. Synthesize final answer from all results"""

    RESULT_PASSING_GUIDE = """Result Passing Rules:
- Extract relevant data from each tool's output
- Transform data format if needed for next tool
- Maintain context across tool calls
- Handle errors at each step
- Verify data before passing forward"""

    CHAINING_PATTERNS = {
        "sequential": """Sequential Chain Pattern:
Tool A → Result A → Tool B → Result B → Tool C → Final Answer

Each tool depends on the previous tool's output.""",
        
        "parallel_then_merge": """Parallel-Merge Pattern:
Tool A → Result A \\
                    → Merge → Tool C → Final Answer
Tool B → Result B /

Independent tools run first, results merge for final tool.""",
        
        "conditional": """Conditional Chain Pattern:
Tool A → Result A → Decision
                    ├─ If X: Tool B → Result B
                    └─ If Y: Tool C → Result C
                    → Final Answer

Tool selection depends on intermediate results.""",
        
        "iterative": """Iterative Chain Pattern:
Tool A → Result → Check
         ↑         ├─ Complete: Final Answer
         └─────────└─ Incomplete: Repeat with new params

Repeat tool calls until condition met."""
    }

    def __init__(self, system_role: str = "tool orchestration assistant"):
        self.system_role = system_role

    def build_chaining_prompt(
        self,
        task: str,
        tool_chain: List[Dict[str, str]],
        context: Optional[str] = None,
        pattern: str = "sequential"
    ) -> str:
        """Build prompt for tool chaining scenario"""
        sections = [
            f"You are a {self.system_role}.",
            self.CHAINING_INSTRUCTION,
            self._format_tool_chain(tool_chain),
            self.RESULT_PASSING_GUIDE
        ]
        
        if pattern in self.CHAINING_PATTERNS:
            sections.append(self.CHAINING_PATTERNS[pattern])
        
        if context:
            sections.append(f"Context:\n{context}")
        
        sections.append(f"Task: {task}")
        sections.append("\nExecution Plan:")
        
        return "\n\n".join(sections)

    def build_sequential_chain(
        self,
        task: str,
        tools: List[Dict[str, str]],
        dependencies: List[str]
    ) -> str:
        """Build prompt for sequential tool chain with explicit dependencies"""
        sections = [
            f"You are a {self.system_role}.",
            "Execute tools sequentially, each using results from previous steps:\n"
        ]
        
        sections.append("Available Tools:")
        for tool in tools:
            sections.append(f"- {tool['name']}: {tool['description']}")
        
        sections.append("\nExecution Flow:")
        for i, dep in enumerate(dependencies, 1):
            sections.append(f"Step {i}: {dep}")
        
        sections.append(self.RESULT_PASSING_GUIDE)
        sections.append(f"\nTask: {task}")
        sections.append("\nExecute the chain:")
        
        return "\n\n".join(sections)

    def build_parallel_merge_chain(
        self,
        task: str,
        parallel_tools: List[Dict[str, str]],
        merge_tool: Dict[str, str]
    ) -> str:
        """Build prompt for parallel execution followed by merge"""
        sections = [
            f"You are a {self.system_role}.",
            "Execute tools in parallel, then merge results:\n"
        ]
        
        sections.append("Phase 1 - Parallel Execution:")
        for tool in parallel_tools:
            sections.append(f"- {tool['name']}: {tool['description']}")
        
        sections.append(f"\nPhase 2 - Merge Results:")
        sections.append(f"- {merge_tool['name']}: {merge_tool['description']}")
        
        sections.append("""
Process:
1. Execute all Phase 1 tools independently
2. Collect all results
3. Pass combined results to merge tool
4. Generate final answer""")
        
        sections.append(f"\nTask: {task}")
        
        return "\n\n".join(sections)

    def build_conditional_chain(
        self,
        task: str,
        initial_tool: Dict[str, str],
        conditional_tools: Dict[str, List[Dict[str, str]]],
        context: Optional[str] = None
    ) -> str:
        """Build prompt for conditional tool chaining"""
        sections = [
            f"You are a {self.system_role}.",
            "Execute tools conditionally based on intermediate results:\n"
        ]
        
        sections.append(f"Initial Tool:\n- {initial_tool['name']}: {initial_tool['description']}")
        
        sections.append("\nConditional Branches:")
        for condition, tools in conditional_tools.items():
            sections.append(f"\nIf {condition}:")
            for tool in tools:
                sections.append(f"  - {tool['name']}: {tool['description']}")
        
        sections.append("""
Process:
1. Execute initial tool
2. Analyze result to determine condition
3. Select appropriate branch
4. Execute branch tools
5. Return final result""")
        
        if context:
            sections.append(f"\nContext:\n{context}")
        
        sections.append(f"\nTask: {task}")
        
        return "\n\n".join(sections)

    def _format_tool_chain(self, tool_chain: List[Dict[str, str]]) -> str:
        """Format tool chain with data flow"""
        chain_text = "Tool Chain:\n"
        for i, tool in enumerate(tool_chain, 1):
            chain_text += f"{i}. {tool['name']}: {tool['description']}\n"
            if 'output' in tool:
                chain_text += f"   Output: {tool['output']}\n"
            if i < len(tool_chain):
                chain_text += "   ↓\n"
        return chain_text

    @staticmethod
    def get_chaining_examples() -> Dict[str, Dict]:
        """Return example tool chaining scenarios"""
        return {
            "weather_email": {
                "task": "Get weather for Paris and email it to user",
                "chain": [
                    {"name": "get_weather", "description": "Fetch weather data", "output": "temperature, conditions"},
                    {"name": "format_message", "description": "Create email body", "output": "formatted text"},
                    {"name": "send_email", "description": "Send email", "output": "confirmation"}
                ],
                "execution": """Step 1: get_weather(location="Paris")
→ Result: {"temp": 18, "conditions": "Sunny"}

Step 2: format_message(data=weather_result)
→ Result: "Weather in Paris: 18°C, Sunny"

Step 3: send_email(body=formatted_message, to=user)
→ Result: "Email sent successfully" """
            },
            
            "research_summarize": {
                "task": "Research a topic and create a summary report",
                "chain": [
                    {"name": "search_web", "description": "Search for information", "output": "search results"},
                    {"name": "extract_content", "description": "Get full articles", "output": "article texts"},
                    {"name": "summarize", "description": "Create summary", "output": "summary text"},
                    {"name": "save_file", "description": "Save to file", "output": "file path"}
                ],
                "execution": """Step 1: search_web(query="AI agents")
→ Result: [url1, url2, url3]

Step 2: extract_content(urls=search_results)
→ Result: [article1_text, article2_text, article3_text]

Step 3: summarize(texts=articles)
→ Result: "AI agents are autonomous systems..."

Step 4: save_file(content=summary, filename="report.txt")
→ Result: "/path/to/report.txt" """
            },
            
            "data_pipeline": {
                "task": "Fetch data, transform it, and store results",
                "chain": [
                    {"name": "fetch_api", "description": "Get raw data", "output": "json data"},
                    {"name": "validate", "description": "Check data quality", "output": "valid records"},
                    {"name": "transform", "description": "Process data", "output": "transformed data"},
                    {"name": "store_db", "description": "Save to database", "output": "record count"}
                ],
                "execution": """Step 1: fetch_api(endpoint="/users")
→ Result: [{"id": 1, "name": "John"}, ...]

Step 2: validate(data=api_result)
→ Result: 95 valid records, 5 invalid

Step 3: transform(data=valid_records)
→ Result: Normalized and enriched data

Step 4: store_db(data=transformed_data)
→ Result: "95 records stored successfully" """
            },
            
            "conditional_workflow": {
                "task": "Check inventory and reorder if needed",
                "chain": [
                    {"name": "check_inventory", "description": "Get stock levels", "output": "quantity"},
                    {"name": "calculate_reorder", "description": "Determine order amount", "output": "order quantity"},
                    {"name": "place_order", "description": "Order from supplier", "output": "order ID"}
                ],
                "execution": """Step 1: check_inventory(item="widgets")
→ Result: {"quantity": 15, "threshold": 50}

Step 2: Decision - quantity < threshold?
→ Yes, proceed to reorder

Step 3: calculate_reorder(current=15, target=100)
→ Result: order_quantity = 85

Step 4: place_order(item="widgets", quantity=85)
→ Result: "Order #12345 placed" """
            }
        }
