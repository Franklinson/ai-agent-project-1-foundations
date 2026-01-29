class ToolRegistry:
    def __init__(self):
        self.tools = {}
    
    def register(self, tool):
        """Register a tool with its schema and implementation."""
        self.tools[tool['name']] = tool
    
    def get(self, tool_name):
        """Retrieve a tool by name."""
        return self.tools.get(tool_name)
    
    def list_available(self):
        """List all available tool names."""
        return list(self.tools.keys())
