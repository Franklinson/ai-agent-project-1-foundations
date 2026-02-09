"""Calculator tool for basic math operations."""

from typing import Dict, Any


def calculator(operation: str, a: float, b: float = 0) -> Dict[str, Any]:
    """
    Perform basic math operations.
    
    Args:
        operation: Math operation (add, subtract, multiply, divide, power, modulo)
        a: First number
        b: Second number (default: 0)
    
    Returns:
        Dict with result and status
    """
    try:
        ops = {
            'add': lambda x, y: x + y,
            'subtract': lambda x, y: x - y,
            'multiply': lambda x, y: x * y,
            'divide': lambda x, y: x / y if y != 0 else None,
            'power': lambda x, y: x ** y,
            'modulo': lambda x, y: x % y if y != 0 else None
        }
        
        if operation not in ops:
            return {'success': False, 'error': f'Invalid operation: {operation}'}
        
        result = ops[operation](a, b)
        
        if result is None:
            return {'success': False, 'error': 'Division by zero'}
        
        return {'success': True, 'result': result, 'operation': operation}
    
    except Exception as e:
        return {'success': False, 'error': str(e)}
