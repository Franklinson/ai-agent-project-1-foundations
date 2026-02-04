"""
Demo: Tool Chaining Prompt Builder Usage
"""

from tool_chaining_prompts import ToolChainingPromptBuilder


def demo_sequential_chain():
    """Demonstrate sequential tool chaining"""
    print("=" * 60)
    print("DEMO 1: Sequential Tool Chain")
    print("=" * 60)
    
    builder = ToolChainingPromptBuilder()
    
    tool_chain = [
        {"name": "get_weather", "description": "Fetch weather data for location", "output": "temperature, conditions"},
        {"name": "format_email", "description": "Create formatted email body", "output": "email text"},
        {"name": "send_email", "description": "Send email to recipient", "output": "confirmation"}
    ]
    
    prompt = builder.build_chaining_prompt(
        task="Get weather for Tokyo and email it to sarah@example.com",
        tool_chain=tool_chain,
        pattern="sequential"
    )
    
    print(prompt)
    print("\n")


def demo_parallel_merge():
    """Demonstrate parallel execution with merge"""
    print("=" * 60)
    print("DEMO 2: Parallel-Merge Pattern")
    print("=" * 60)
    
    builder = ToolChainingPromptBuilder()
    
    parallel_tools = [
        {"name": "get_weather", "description": "Fetch current weather"},
        {"name": "get_news", "description": "Fetch latest news"},
        {"name": "get_stock_price", "description": "Fetch stock prices"}
    ]
    
    merge_tool = {"name": "create_dashboard", "description": "Combine all data into dashboard"}
    
    prompt = builder.build_parallel_merge_chain(
        task="Create a morning briefing dashboard with weather, news, and stocks",
        parallel_tools=parallel_tools,
        merge_tool=merge_tool
    )
    
    print(prompt)
    print("\n")


def demo_conditional_chain():
    """Demonstrate conditional tool chaining"""
    print("=" * 60)
    print("DEMO 3: Conditional Chain")
    print("=" * 60)
    
    builder = ToolChainingPromptBuilder()
    
    initial_tool = {"name": "check_file_type", "description": "Determine file format"}
    
    conditional_tools = {
        "file is CSV": [
            {"name": "parse_csv", "description": "Parse CSV data"},
            {"name": "validate_csv", "description": "Validate CSV structure"}
        ],
        "file is JSON": [
            {"name": "parse_json", "description": "Parse JSON data"},
            {"name": "validate_json", "description": "Validate JSON schema"}
        ],
        "file is XML": [
            {"name": "parse_xml", "description": "Parse XML data"},
            {"name": "validate_xml", "description": "Validate XML structure"}
        ]
    }
    
    prompt = builder.build_conditional_chain(
        task="Process uploaded file based on its format",
        initial_tool=initial_tool,
        conditional_tools=conditional_tools
    )
    
    print(prompt)
    print("\n")


def demo_explicit_dependencies():
    """Demonstrate sequential chain with explicit dependencies"""
    print("=" * 60)
    print("DEMO 4: Explicit Dependencies")
    print("=" * 60)
    
    builder = ToolChainingPromptBuilder()
    
    tools = [
        {"name": "search_products", "description": "Search for products"},
        {"name": "get_reviews", "description": "Fetch product reviews"},
        {"name": "analyze_sentiment", "description": "Analyze review sentiment"},
        {"name": "generate_report", "description": "Create summary report"}
    ]
    
    dependencies = [
        "search_products(query) → product_list",
        "get_reviews(product_list) → reviews",
        "analyze_sentiment(reviews) → sentiment_scores",
        "generate_report(sentiment_scores) → final_report"
    ]
    
    prompt = builder.build_sequential_chain(
        task="Find laptops, analyze their reviews, and create a sentiment report",
        tools=tools,
        dependencies=dependencies
    )
    
    print(prompt)
    print("\n")


def demo_all_examples():
    """Show all built-in chaining examples"""
    print("=" * 60)
    print("DEMO 5: Built-in Chaining Examples")
    print("=" * 60)
    
    examples = ToolChainingPromptBuilder.get_chaining_examples()
    
    for name, example in examples.items():
        print(f"\n{name.upper().replace('_', ' ')} Example:")
        print(f"Task: {example['task']}")
        print("\nTool Chain:")
        for i, tool in enumerate(example['chain'], 1):
            print(f"  {i}. {tool['name']}: {tool['description']}")
            if 'output' in tool:
                print(f"     → Output: {tool['output']}")
        print(f"\nExecution:\n{example['execution']}")
        print("-" * 60)


def demo_all_patterns():
    """Show all chaining patterns"""
    print("=" * 60)
    print("DEMO 6: All Chaining Patterns")
    print("=" * 60)
    
    for pattern_name, pattern_desc in ToolChainingPromptBuilder.CHAINING_PATTERNS.items():
        print(f"\n{pattern_name.upper().replace('_', ' ')}:")
        print(pattern_desc)
        print("-" * 60)


if __name__ == "__main__":
    demo_sequential_chain()
    demo_parallel_merge()
    demo_conditional_chain()
    demo_explicit_dependencies()
    demo_all_examples()
    demo_all_patterns()
