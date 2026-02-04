"""
Demo: Advanced Prompt System
Demonstrates unified interface for combining all techniques
"""

from advanced_prompt_system import AdvancedPromptSystem


def demo_single_technique():
    """Demonstrate using single technique"""
    print("=" * 60)
    print("DEMO 1: Single Technique (CoT)")
    print("=" * 60)
    
    system = AdvancedPromptSystem()
    
    prompt = system.build_prompt(
        task="Calculate compound interest on $1000 at 5% for 3 years",
        techniques=["cot"]
    )
    
    print(prompt)
    print("\n")


def demo_two_techniques():
    """Demonstrate combining two techniques"""
    print("=" * 60)
    print("DEMO 2: Two Techniques (CoT + Error Recovery)")
    print("=" * 60)
    
    system = AdvancedPromptSystem()
    
    prompt = system.build_prompt(
        task="Fetch user data from unreliable API",
        techniques=["cot", "error_recovery"],
        context="API has 30% failure rate"
    )
    
    print(prompt)
    print("\n")


def demo_three_techniques():
    """Demonstrate combining three techniques"""
    print("=" * 60)
    print("DEMO 3: Three Techniques (CoT + Chaining + Multi-Step)")
    print("=" * 60)
    
    system = AdvancedPromptSystem()
    
    tools = [
        {"name": "search", "description": "Search for information"},
        {"name": "summarize", "description": "Summarize content"},
        {"name": "save", "description": "Save to file"}
    ]
    
    steps = [
        "Search for relevant information",
        "Summarize findings",
        "Save summary to file"
    ]
    
    prompt = system.build_prompt(
        task="Research AI agents and save summary",
        techniques=["cot", "chaining", "multi_step"],
        tools=tools,
        steps=steps
    )
    
    print(prompt)
    print("\n")


def demo_all_techniques():
    """Demonstrate all techniques combined"""
    print("=" * 60)
    print("DEMO 4: All Techniques Combined")
    print("=" * 60)
    
    system = AdvancedPromptSystem()
    
    tools = [
        {"name": "fetch_api", "description": "Fetch data from API"},
        {"name": "validate", "description": "Validate data"},
        {"name": "transform", "description": "Transform data"},
        {"name": "store", "description": "Store in database"}
    ]
    
    prompt = system.build_all(
        task="Build robust data processing pipeline",
        tools=tools,
        context="Processing 10,000 records with potential errors"
    )
    
    print(prompt)
    print("\n")


def demo_custom_combinations():
    """Demonstrate various custom combinations"""
    print("=" * 60)
    print("DEMO 5: Custom Combinations")
    print("=" * 60)
    
    system = AdvancedPromptSystem()
    
    # Combination 1: Chaining + Error Recovery
    print("\nCombination 1: Chaining + Error Recovery")
    print("-" * 40)
    tools = [{"name": "api_call", "description": "Call external API"}]
    prompt1 = system.build_prompt(
        task="Call multiple APIs in sequence",
        techniques=["chaining", "error_recovery"],
        tools=tools
    )
    print(prompt1[:200] + "...\n")
    
    # Combination 2: Multi-Step + CoT
    print("\nCombination 2: Multi-Step + CoT")
    print("-" * 40)
    steps = ["Analyze problem", "Design solution", "Implement"]
    prompt2 = system.build_prompt(
        task="Solve complex problem",
        techniques=["multi_step", "cot"],
        steps=steps
    )
    print(prompt2[:200] + "...\n")
    
    print("-" * 60)


def demo_comparison():
    """Compare different technique combinations"""
    print("=" * 60)
    print("DEMO 6: Technique Comparison")
    print("=" * 60)
    
    system = AdvancedPromptSystem()
    task = "Process customer orders"
    
    print("\nScenario: Process customer orders\n")
    
    print("Option 1: CoT only")
    print("  Use case: Simple, straightforward task")
    print("  Benefits: Clear reasoning, easy to debug")
    
    print("\nOption 2: CoT + Error Recovery")
    print("  Use case: Task with potential failures")
    print("  Benefits: Reasoning + robustness")
    
    print("\nOption 3: Chaining + Multi-Step")
    print("  Use case: Complex workflow with dependencies")
    print("  Benefits: Structured execution + planning")
    
    print("\nOption 4: All Techniques")
    print("  Use case: Production system, mission-critical")
    print("  Benefits: Maximum reliability and transparency")
    
    print("\n" + "-" * 60)


if __name__ == "__main__":
    demo_single_technique()
    demo_two_techniques()
    demo_three_techniques()
    demo_all_techniques()
    demo_custom_combinations()
    demo_comparison()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("\nAdvanced Prompt System provides:")
    print("  ✓ Unified interface for all techniques")
    print("  ✓ Flexible combination of techniques")
    print("  ✓ Simple API: build_prompt() and build_all()")
    print("  ✓ Production-ready prompts")
    print("\nTechniques available:")
    print("  • cot: Chain-of-Thought reasoning")
    print("  • chaining: Tool chaining and orchestration")
    print("  • multi_step: Multi-step planning")
    print("  • error_recovery: Error handling and recovery")
    print("\n" + "=" * 60)
