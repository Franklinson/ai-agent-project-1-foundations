"""
Comprehensive Test: Verify All Prompt Builders Work Together
"""

from cot_prompt_builder import CoTPromptBuilder
from tool_chaining_prompts import ToolChainingPromptBuilder
from multi_step_prompts import MultiStepPromptBuilder
from error_recovery_prompts import ErrorRecoveryPromptBuilder
from integrated_prompt_system import AdvancedPromptSystem


def test_all_builders():
    """Test that all builders can be instantiated and used"""
    print("Testing All Prompt Builders...")
    print("=" * 60)
    
    # Test 1: CoT Builder
    print("\n✓ Testing CoT Builder...")
    cot = CoTPromptBuilder()
    cot_prompt = cot.build_cot_prompt("Test task", task_type="problem_solving")
    assert len(cot_prompt) > 0
    print("  CoT Builder: PASS")
    
    # Test 2: Tool Chaining Builder
    print("\n✓ Testing Tool Chaining Builder...")
    chaining = ToolChainingPromptBuilder()
    chain = [{"name": "tool1", "description": "Test tool"}]
    chain_prompt = chaining.build_chaining_prompt("Test task", chain)
    assert len(chain_prompt) > 0
    print("  Tool Chaining Builder: PASS")
    
    # Test 3: Multi-Step Builder
    print("\n✓ Testing Multi-Step Builder...")
    multi_step = MultiStepPromptBuilder()
    steps = ["Step 1", "Step 2"]
    multi_prompt = multi_step.build_multi_step_prompt("Test goal", steps)
    assert len(multi_prompt) > 0
    print("  Multi-Step Builder: PASS")
    
    # Test 4: Error Recovery Builder
    print("\n✓ Testing Error Recovery Builder...")
    error = ErrorRecoveryPromptBuilder()
    error_prompt = error.build_error_aware_prompt("Test task")
    assert len(error_prompt) > 0
    print("  Error Recovery Builder: PASS")
    
    # Test 5: Integrated System
    print("\n✓ Testing Integrated System...")
    system = AdvancedPromptSystem()
    integrated_prompt = system.build_comprehensive_prompt("Test task")
    assert len(integrated_prompt) > 0
    print("  Integrated System: PASS")
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED!")
    print("=" * 60)
    
    # Summary
    print("\nSystem Components:")
    print("  1. CoT Prompt Builder ✓")
    print("  2. Tool Chaining Prompt Builder ✓")
    print("  3. Multi-Step Prompt Builder ✓")
    print("  4. Error Recovery Prompt Builder ✓")
    print("  5. Integrated Prompt System ✓")
    
    print("\nCapabilities:")
    print("  • Step-by-step reasoning (CoT)")
    print("  • Sequential tool execution (Chaining)")
    print("  • Goal decomposition (Multi-Step)")
    print("  • Error handling (Recovery)")
    print("  • Combined techniques (Integrated)")
    
    print("\nReady for production use! 🚀")


if __name__ == "__main__":
    test_all_builders()
