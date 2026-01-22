import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.text_tool import TextTool

def test_word_count():
    tool = TextTool()
    result = tool.word_count("Hello world this is a test")
    assert result["success"] == True
    assert result["count"] == 6

def test_word_count_empty():
    tool = TextTool()
    result = tool.word_count("")
    assert result["success"] == True
    assert result["count"] == 0

def test_word_count_invalid_input():
    tool = TextTool()
    result = tool.word_count(123)
    assert result["success"] == False
    assert "error" in result

def test_word_search():
    tool = TextTool()
    result = tool.word_search("hello world hello", "hello")
    assert result["success"] == True
    assert result["count"] == 2

def test_word_search_case_insensitive():
    tool = TextTool()
    result = tool.word_search("Hello HELLO hello", "hello")
    assert result["success"] == True
    assert result["count"] == 3

def test_word_search_not_found():
    tool = TextTool()
    result = tool.word_search("hello world", "test")
    assert result["success"] == True
    assert result["count"] == 0

def test_word_search_empty_word():
    tool = TextTool()
    result = tool.word_search("hello world", "")
    assert result["success"] == False
    assert "error" in result

def test_word_search_invalid_input():
    tool = TextTool()
    result = tool.word_search(123, "hello")
    assert result["success"] == False
    assert "error" in result

if __name__ == "__main__":
    test_word_count()
    test_word_count_empty()
    test_word_count_invalid_input()
    test_word_search()
    test_word_search_case_insensitive()
    test_word_search_not_found()
    test_word_search_empty_word()
    test_word_search_invalid_input()
    print("All text tool tests passed!")
