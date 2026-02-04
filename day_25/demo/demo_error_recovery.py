"""
Demo: Error Recovery Prompt Builder Usage
"""

from error_recovery_prompts import ErrorRecoveryPromptBuilder


def demo_basic_error_aware():
    """Demonstrate basic error-aware prompting"""
    print("=" * 60)
    print("DEMO 1: Basic Error-Aware Prompt")
    print("=" * 60)
    
    builder = ErrorRecoveryPromptBuilder()
    
    tools = [
        {
            "name": "fetch_api",
            "description": "Fetch data from external API",
            "errors": ["timeout", "network", "rate_limit"]
        },
        {
            "name": "process_data",
            "description": "Process and transform data",
            "errors": ["validation", "data_error"]
        }
    ]
    
    prompt = builder.build_error_aware_prompt(
        task="Fetch and process user data from API",
        tools=tools,
        error_handling="retry"
    )
    
    print(prompt)
    print("\n")


def demo_retry_scenario():
    """Demonstrate retry logic"""
    print("=" * 60)
    print("DEMO 2: Retry Scenario")
    print("=" * 60)
    
    builder = ErrorRecoveryPromptBuilder()
    
    prompt = builder.build_retry_prompt(
        task="Send email notification",
        failed_step="send_email(to='user@example.com')",
        error_message="Connection timeout: Unable to reach SMTP server",
        retry_count=1,
        max_retries=3
    )
    
    print(prompt)
    print("\n")


def demo_fallback_strategy():
    """Demonstrate fallback approaches"""
    print("=" * 60)
    print("DEMO 3: Fallback Strategy")
    print("=" * 60)
    
    builder = ErrorRecoveryPromptBuilder()
    
    prompt = builder.build_fallback_prompt(
        task="Get weather information for New York",
        failed_approach="Primary weather API (returned 503 error)",
        alternative_approaches=[
            "Use backup weather API",
            "Fetch cached weather data",
            "Use weather data from alternative source"
        ]
    )
    
    print(prompt)
    print("\n")


def demo_error_classification():
    """Demonstrate error classification"""
    print("=" * 60)
    print("DEMO 4: Error Classification")
    print("=" * 60)
    
    builder = ErrorRecoveryPromptBuilder()
    
    prompt = builder.build_error_classification_prompt(
        error_message="PostgreSQL connection failed: FATAL: password authentication failed for user 'admin'",
        context="Attempting to connect to production database"
    )
    
    print(prompt)
    print("\n")


def demo_multi_error_handling():
    """Demonstrate handling multiple error types"""
    print("=" * 60)
    print("DEMO 5: Multi-Error Handling")
    print("=" * 60)
    
    builder = ErrorRecoveryPromptBuilder()
    
    steps = [
        {
            "name": "validate_input",
            "description": "Validate user input data",
            "potential_errors": ["validation", "data_error"]
        },
        {
            "name": "fetch_external_data",
            "description": "Fetch data from external API",
            "potential_errors": ["timeout", "network", "rate_limit"]
        },
        {
            "name": "process_data",
            "description": "Process and transform data",
            "potential_errors": ["data_error"]
        },
        {
            "name": "save_to_database",
            "description": "Save results to database",
            "potential_errors": ["permission", "server_error"]
        }
    ]
    
    error_policies = {
        "validate_input": "abort",
        "fetch_external_data": "retry",
        "process_data": "fallback",
        "save_to_database": "retry"
    }
    
    prompt = builder.build_multi_error_prompt(
        task="Process and store user data",
        steps=steps,
        error_policies=error_policies
    )
    
    print(prompt)
    print("\n")


def demo_all_examples():
    """Show all built-in error examples"""
    print("=" * 60)
    print("DEMO 6: Built-in Error Examples")
    print("=" * 60)
    
    examples = ErrorRecoveryPromptBuilder.get_error_examples()
    
    for name, example in examples.items():
        print(f"\n{name.upper().replace('_', ' ')} Example:")
        print(f"Task: {example['task']}")
        print(f"Error: {example['error']}")
        print("\nClassification:")
        for key, value in example['classification'].items():
            print(f"  {key}: {value}")
        print(f"\nRecovery Strategy: {example['strategy']}")
        print(f"\nRecovery Process:\n{example['recovery']}")
        print("-" * 60)


def demo_recovery_strategies():
    """Show all recovery strategies"""
    print("=" * 60)
    print("DEMO 7: Recovery Strategies")
    print("=" * 60)
    
    for strategy_name, strategy_desc in ErrorRecoveryPromptBuilder.RECOVERY_STRATEGIES.items():
        print(f"\n{strategy_name.upper()}:")
        print(strategy_desc)
        print("-" * 60)


def demo_error_types():
    """Show all error types"""
    print("=" * 60)
    print("DEMO 8: Error Types")
    print("=" * 60)
    
    print("\nCommon Error Types:\n")
    for error_type, description in ErrorRecoveryPromptBuilder.ERROR_TYPES.items():
        print(f"{error_type.upper()}")
        print(f"  Description: {description}")
        print()


if __name__ == "__main__":
    demo_basic_error_aware()
    demo_retry_scenario()
    demo_fallback_strategy()
    demo_error_classification()
    demo_multi_error_handling()
    demo_all_examples()
    demo_recovery_strategies()
    demo_error_types()
