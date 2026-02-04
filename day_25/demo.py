"""
Demo: Chain-of-Thought Prompt Builder Usage
"""

from cot_prompt_builder import CoTPromptBuilder


def demo_basic_cot():
    """Demonstrate basic CoT prompt building"""
    print("=" * 60)
    print("DEMO 1: Basic CoT Prompt")
    print("=" * 60)
    
    builder = CoTPromptBuilder()
    
    prompt = builder.build_cot_prompt(
        task="Calculate the total cost of 3 books at $12.99 each with 8% tax",
        task_type="problem_solving"
    )
    
    print(prompt)
    print("\n")


def demo_tool_use_cot():
    """Demonstrate CoT with tool usage"""
    print("=" * 60)
    print("DEMO 2: CoT with Tools")
    print("=" * 60)
    
    builder = CoTPromptBuilder()
    
    tools = [
        {"name": "search_web", "description": "Search the internet for information"},
        {"name": "calculate", "description": "Perform mathematical calculations"},
        {"name": "send_email", "description": "Send an email to a recipient"}
    ]
    
    prompt = builder.build_tool_use_cot(
        task="Find the current price of Bitcoin and email it to john@example.com",
        tools=tools
    )
    
    print(prompt)
    print("\n")


def demo_few_shot_cot():
    """Demonstrate few-shot CoT prompting"""
    print("=" * 60)
    print("DEMO 3: Few-Shot CoT")
    print("=" * 60)
    
    builder = CoTPromptBuilder()
    examples = CoTPromptBuilder.get_cot_examples()
    
    prompt = builder.build_few_shot_cot(
        task="If 25% of students passed the exam and 60 students failed, how many students took the exam?",
        examples=[examples["math"]]
    )
    
    print(prompt)
    print("\n")


def demo_decision_making():
    """Demonstrate CoT for decision making"""
    print("=" * 60)
    print("DEMO 4: Decision Making CoT")
    print("=" * 60)
    
    builder = CoTPromptBuilder(system_role="strategic decision-making assistant")
    
    prompt = builder.build_cot_prompt(
        task="Should we migrate our application to microservices architecture?",
        context="Current: Monolithic app with 100K users, 5-person team, tight budget",
        task_type="decision_making"
    )
    
    print(prompt)
    print("\n")


def demo_debugging():
    """Demonstrate CoT for debugging"""
    print("=" * 60)
    print("DEMO 5: Debugging CoT")
    print("=" * 60)
    
    builder = CoTPromptBuilder(system_role="debugging assistant")
    
    prompt = builder.build_cot_prompt(
        task="API returns 500 error only for POST requests with large payloads",
        context="GET requests work fine. Small POST requests work. Error started after deployment.",
        task_type="debugging"
    )
    
    print(prompt)
    print("\n")


def demo_all_examples():
    """Show all built-in CoT examples"""
    print("=" * 60)
    print("DEMO 6: Built-in CoT Examples")
    print("=" * 60)
    
    examples = CoTPromptBuilder.get_cot_examples()
    
    for category, example in examples.items():
        print(f"\n{category.upper()} Example:")
        print(f"Task: {example['task']}")
        print(f"\nReasoning:\n{example['reasoning']}")
        print(f"\nAnswer: {example['answer']}")
        print("-" * 60)


if __name__ == "__main__":
    demo_basic_cot()
    demo_tool_use_cot()
    demo_few_shot_cot()
    demo_decision_making()
    demo_debugging()
    demo_all_examples()
