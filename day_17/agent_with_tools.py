from tools.calculator_tool import CalculatorTool
from tools.text_tool import TextTool

def demonstrate_tools():
    """Demonstrate tool usage with various inputs and error handling."""
    # Initialize tools
    calculator = CalculatorTool()
    text_tool = TextTool()
    
    print("=== Calculator Tool Demonstrations ===")
    
    # Successful operations
    print("\n1. Addition:")
    result = calculator.calculate("add", 10, 5)
    print(f"   {result}")
    
    print("\n2. Multiplication:")
    result = calculator.calculate("multiply", 7, 6)
    print(f"   {result}")
    
    # Error handling: Division by zero
    print("\n3. Division by zero (error case):")
    result = calculator.calculate("divide", 10, 0)
    print(f"   {result}")
    
    # Error handling: Invalid operation
    print("\n4. Invalid operation (error case):")
    result = calculator.calculate("power", 2, 3)
    print(f"   {result}")
    
    print("\n=== Text Tool Demonstrations ===")
    
    # Word count
    print("\n5. Word count:")
    result = text_tool.word_count("The quick brown fox jumps over the lazy dog")
    print(f"   {result}")
    
    # Word search
    print("\n6. Word search:")
    result = text_tool.word_search("hello world hello universe hello", "hello")
    print(f"   {result}")
    
    # Error handling: Invalid input type
    print("\n7. Invalid input type (error case):")
    result = text_tool.word_count(12345)
    print(f"   {result}")
    
    # Error handling: Empty search word
    print("\n8. Empty search word (error case):")
    result = text_tool.word_search("test text", "")
    print(f"   {result}")

if __name__ == "__main__":
    demonstrate_tools()
