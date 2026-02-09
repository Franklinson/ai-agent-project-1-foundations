import sys
sys.path.append('../day_27')
sys.path.append('../day_28')

from typing import Dict, Any
from loop_controller import LoopController
from tool_registry import ToolRegistry
from tool_executor import ToolExecutor


class CompleteAgent:
    """Complete agent with integrated loop controller and tool system"""
    
    def __init__(self):
        self.loop_controller = LoopController()
        self.tool_registry = ToolRegistry()
        self.tool_executor = ToolExecutor(self.tool_registry)
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register default tools"""
        self.tool_registry.register(self._calculator, "calculator", "Perform calculations")
        self.tool_registry.register(self._search, "search", "Search for information")
        self.tool_registry.register(self._time, "time", "Get current time")
    
    def _calculator(self, expression: str) -> Dict[str, Any]:
        """Calculate mathematical expression"""
        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _search(self, query: str) -> Dict[str, Any]:
        """Search for information"""
        return {"success": True, "result": f"Search results for: {query}"}
    
    def _time(self) -> Dict[str, Any]:
        """Get current time"""
        from datetime import datetime
        return {"success": True, "result": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    def run(self, user_input: str, goal: str = None, max_iterations: int = 5) -> Dict[str, Any]:
        """
        Run the complete agent loop
        
        Args:
            user_input: User's input text
            goal: Goal to achieve (defaults to processing the input)
            max_iterations: Maximum loop iterations
            
        Returns:
            Complete execution result
        """
        if goal is None:
            goal = f"Process: {user_input}"
        
        result = self.loop_controller.run(user_input, goal, max_iterations)
        
        # Enhance result with tool information
        result['available_tools'] = self.tool_registry.list_all()
        
        return result
    
    def get_summary(self, result: Dict[str, Any]) -> str:
        """Get human-readable summary of execution"""
        lines = [
            f"Status: {result['status']}",
            f"Iterations: {result['iterations']}",
            f"Termination: {result['termination_reason']}",
            f"Decision: {result.get('final_decision', 'N/A')}"
        ]
        
        if result.get('errors'):
            lines.append(f"Errors: {len(result['errors'])}")
        
        if result.get('progress'):
            avg_success = sum(p['success_rate'] for p in result['progress']) / len(result['progress'])
            lines.append(f"Avg Success Rate: {avg_success:.2%}")
        
        return "\n".join(lines)
