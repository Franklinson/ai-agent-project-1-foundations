"""
Demonstration of Prompt System Components
"""

from prompt_templates import PromptTemplates
from prompt_builder import PromptBuilder
from react_prompt import ReActPromptBuilder
from prompt_tester import PromptTester, create_example_test_cases


def demo_prompt_templates():
    """Demonstrate PromptTemplates usage"""
    print("=== Prompt Templates Demo ===\n")
    
    prompt = PromptTemplates.build_full_prompt(
        capabilities=["Answer questions", "Use tools", "Reason step-by-step"],
        role="AI research assistant",
        guidelines=["Be accurate", "Cite sources", "Ask clarifying questions"],
        tools=[
            {"name": "search", "description": "Search for information"},
            {"name": "calculate", "description": "Perform calculations"}
        ],
        history=[
            {"role": "user", "content": "What is AI?"},
            {"role": "assistant", "content": "AI is artificial intelligence..."}
        ]
    )
    
    print(prompt)
    print("\n" + "="*50 + "\n")


def demo_prompt_builder():
    """Demonstrate PromptBuilder usage"""
    print("=== Dynamic Prompt Builder Demo ===\n")
    
    builder = PromptBuilder(system_role="customer support agent")
    
    prompt = builder.build_prompt(
        user_input="How do I reset my password?",
        tools=[
            {"name": "check_account", "description": "Check account status"},
            {"name": "send_reset_link", "description": "Send password reset link"}
        ],
        context=[
            {"role": "user", "content": "I can't log in"},
            {"role": "assistant", "content": "Let me help you with that"}
        ],
        goal="Help user reset their password"
    )
    
    print(prompt)
    print("\n" + "="*50 + "\n")


def demo_react_prompt():
    """Demonstrate ReAct prompt builder"""
    print("=== ReAct Prompt Demo ===\n")
    
    builder = ReActPromptBuilder()
    
    prompt = builder.build_react_prompt(
        question="What is the capital of France and its population?",
        tools=[
            {"name": "search", "description": "Search for information"},
            {"name": "finish", "description": "Return final answer"}
        ]
    )
    
    print(prompt)
    print("\n" + "="*50 + "\n")


def demo_prompt_testing():
    """Demonstrate prompt testing utilities"""
    print("=== Prompt Testing Demo ===\n")
    
    tester = PromptTester()
    test_cases = create_example_test_cases()
    results = tester.run_test_cases(test_cases)
    
    print(f"Total Tests: {results['total']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}\n")
    
    for detail in results['details']:
        status = "✓" if detail['passed'] else "✗"
        print(f"{status} {detail['name']}")
        if detail['issues']:
            print(f"  Issues: {', '.join(detail['issues'])}")
    
    print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    demo_prompt_templates()
    demo_prompt_builder()
    demo_react_prompt()
    demo_prompt_testing()
