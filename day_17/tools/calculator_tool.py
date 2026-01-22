class CalculatorTool:
    """Tool for performing basic mathematical calculations."""
    
    def calculate(self, operation: str, a: float, b: float) -> dict:
        """
        Perform a mathematical operation.
        
        Args:
            operation: One of 'add', 'subtract', 'multiply', 'divide'
            a: First number
            b: Second number
            
        Returns:
            Dictionary with result and operation details
        """
        try:
            a, b = float(a), float(b)
        except (ValueError, TypeError):
            return {"success": False, "error": "Invalid number input"}
        
        operations = {
            "add": lambda x, y: x + y,
            "subtract": lambda x, y: x - y,
            "multiply": lambda x, y: x * y,
            "divide": lambda x, y: x / y if y != 0 else None
        }
        
        if operation not in operations:
            return {"success": False, "error": f"Invalid operation: {operation}"}
        
        result = operations[operation](a, b)
        
        if result is None:
            return {"success": False, "error": "Division by zero"}
        
        return {"success": True, "operation": operation, "a": a, "b": b, "result": result}
