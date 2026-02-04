"""
Demo: Integrated Advanced Prompt System
"""

from integrated_prompt_system import AdvancedPromptSystem


def demo_comprehensive_prompt():
    """Demonstrate comprehensive prompt with multiple techniques"""
    print("=" * 60)
    print("DEMO 1: Comprehensive Prompt (All Techniques)")
    print("=" * 60)
    
    system = AdvancedPromptSystem()
    
    tools = [
        {"name": "search_web", "description": "Search for information online"},
        {"name": "analyze_data", "description": "Analyze and process data"},
        {"name": "generate_report", "description": "Create formatted report"}
    ]
    
    prompt = system.build_comprehensive_prompt(
        task="Research market trends and generate analysis report",
        tools=tools,
        context="Focus on tech industry, Q4 2024",
        use_cot=True,
        use_chaining=True,
        use_multi_step=True,
        use_error_recovery=True
    )
    
    print(prompt)
    print("\n")


def demo_complex_workflow():
    """Demonstrate complex workflow integration"""
    print("=" * 60)
    print("DEMO 2: Complex Workflow")
    print("=" * 60)
    
    system = AdvancedPromptSystem()
    
    tool_chain = [
        {"name": "fetch_api", "description": "Fetch data from API", "errors": ["timeout", "network"]},
        {"name": "validate", "description": "Validate data quality", "errors": ["validation"]},
        {"name": "transform", "description": "Transform data", "errors": ["data_error"]},
        {"name": "store_db", "description": "Store in database", "errors": ["permission"]}
    ]
    
    steps = [
        "Fetch raw data from external API",
        "Validate data structure and content",
        "Transform and normalize data",
        "Store processed data in database"
    ]
    
    error_policies = {
        "fetch_api": "retry",
        "validate": "skip",
        "transform": "fallback",
        "store_db": "retry"
    }
    
    prompt = system.build_complex_workflow_prompt(
        goal="Process customer data pipeline",
        tool_chain=tool_chain,
        steps=steps,
        error_policies=error_policies,
        context="Processing 10,000 customer records"
    )
    
    print(prompt)
    print("\n")


def demo_adaptive_agent():
    """Demonstrate adaptive agent prompt"""
    print("=" * 60)
    print("DEMO 3: Adaptive Agent")
    print("=" * 60)
    
    system = AdvancedPromptSystem()
    
    tools = [
        {"name": "search_docs", "description": "Search documentation"},
        {"name": "run_tests", "description": "Execute test suite"},
        {"name": "analyze_logs", "description": "Analyze error logs"},
        {"name": "apply_fix", "description": "Apply code fix"}
    ]
    
    prompt = system.build_adaptive_agent_prompt(
        task="Debug failing test suite and fix issues",
        available_tools=tools,
        constraints=["Don't modify test files", "Maintain backward compatibility"],
        success_criteria=["All tests pass", "No new warnings", "Code coverage maintained"]
    )
    
    print(prompt)
    print("\n")


def demo_robust_pipeline():
    """Demonstrate robust pipeline execution"""
    print("=" * 60)
    print("DEMO 4: Robust Pipeline")
    print("=" * 60)
    
    system = AdvancedPromptSystem()
    
    stages = [
        {
            "name": "Data Ingestion",
            "action": "Fetch data from multiple sources",
            "input": "API endpoints",
            "output": "Raw data",
            "error_policy": "retry"
        },
        {
            "name": "Data Validation",
            "action": "Validate schema and quality",
            "output": "Validated data",
            "error_policy": "skip"
        },
        {
            "name": "Data Transformation",
            "action": "Clean and normalize data",
            "output": "Transformed data",
            "error_policy": "fallback"
        },
        {
            "name": "Data Storage",
            "action": "Store in data warehouse",
            "output": "Storage confirmation",
            "error_policy": "retry"
        },
        {
            "name": "Notification",
            "action": "Send completion notification",
            "output": "Notification sent",
            "error_policy": "skip"
        }
    ]
    
    prompt = system.build_robust_pipeline_prompt(
        pipeline_name="ETL Data Pipeline",
        stages=stages,
        rollback_strategy="rollback_on_critical_failure"
    )
    
    print(prompt)
    print("\n")


def demo_integration_examples():
    """Show built-in integration examples"""
    print("=" * 60)
    print("DEMO 5: Integration Examples")
    print("=" * 60)
    
    examples = AdvancedPromptSystem.get_integration_examples()
    
    for name, example in examples.items():
        print(f"\n{name.upper().replace('_', ' ')}:")
        print(f"Description: {example['description']}")
        print(f"Techniques: {', '.join(example['techniques'])}")
        print(f"\nScenario:\n{example['scenario']}")
        print("-" * 60)


def demo_technique_comparison():
    """Compare individual vs integrated approaches"""
    print("=" * 60)
    print("DEMO 6: Technique Comparison")
    print("=" * 60)
    
    print("\nINDIVIDUAL TECHNIQUES:")
    print("- CoT: Step-by-step reasoning")
    print("- Tool Chaining: Sequential tool execution")
    print("- Multi-Step: Goal decomposition and planning")
    print("- Error Recovery: Robust error handling")
    
    print("\nINTEGRATED APPROACH:")
    print("- Combines all techniques for maximum effectiveness")
    print("- CoT reasoning guides tool selection")
    print("- Multi-step planning structures execution")
    print("- Tool chaining manages data flow")
    print("- Error recovery ensures robustness")
    
    print("\nBENEFITS OF INTEGRATION:")
    print("✓ More reliable execution")
    print("✓ Better error handling")
    print("✓ Clearer reasoning trail")
    print("✓ Improved success rates")
    print("✓ Adaptive to failures")
    print("-" * 60)


if __name__ == "__main__":
    demo_comprehensive_prompt()
    demo_complex_workflow()
    demo_adaptive_agent()
    demo_robust_pipeline()
    demo_integration_examples()
    demo_technique_comparison()
