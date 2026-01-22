import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.calculator_tool import CalculatorTool

def test_add():
    calc = CalculatorTool()
    result = calc.calculate("add", 5, 3)
    assert result["success"] == True
    assert result["result"] == 8

def test_subtract():
    calc = CalculatorTool()
    result = calc.calculate("subtract", 10, 4)
    assert result["success"] == True
    assert result["result"] == 6

def test_multiply():
    calc = CalculatorTool()
    result = calc.calculate("multiply", 6, 7)
    assert result["success"] == True
    assert result["result"] == 42

def test_divide():
    calc = CalculatorTool()
    result = calc.calculate("divide", 20, 4)
    assert result["success"] == True
    assert result["result"] == 5

def test_division_by_zero():
    calc = CalculatorTool()
    result = calc.calculate("divide", 10, 0)
    assert result["success"] == False
    assert "error" in result

def test_invalid_operation():
    calc = CalculatorTool()
    result = calc.calculate("power", 2, 3)
    assert result["success"] == False
    assert "error" in result

def test_invalid_input():
    calc = CalculatorTool()
    result = calc.calculate("add", "abc", 5)
    assert result["success"] == False
    assert "error" in result

if __name__ == "__main__":
    test_add()
    test_subtract()
    test_multiply()
    test_divide()
    test_division_by_zero()
    test_invalid_operation()
    test_invalid_input()
    print("All calculator tests passed!")
