"""
Prompt Testing and Validation Utilities
"""

from typing import List, Dict, Optional


class PromptTester:
    """Utilities for testing and validating prompts"""
    
    def validate_prompt(
        self,
        prompt: str,
        required_components: Optional[List[str]] = None
    ) -> Dict[str, any]:
        """Validate prompt structure and components"""
        results = {
            "valid": True,
            "length": len(prompt),
            "missing_components": [],
            "warnings": []
        }
        
        # Check minimum length
        if len(prompt) < 10:
            results["valid"] = False
            results["warnings"].append("Prompt too short")
        
        # Check required components
        if required_components:
            for component in required_components:
                if component.lower() not in prompt.lower():
                    results["valid"] = False
                    results["missing_components"].append(component)
        
        # Check for empty prompt
        if not prompt.strip():
            results["valid"] = False
            results["warnings"].append("Prompt is empty")
        
        return results
    
    def evaluate_prompt(self, prompt: str) -> Dict[str, any]:
        """Basic evaluation of prompt quality"""
        return {
            "length": len(prompt),
            "word_count": len(prompt.split()),
            "has_instructions": any(word in prompt.lower() for word in ["you are", "your role", "follow"]),
            "has_examples": "example" in prompt.lower(),
            "has_tools": "tool" in prompt.lower(),
            "has_context": any(word in prompt.lower() for word in ["context", "history"])
        }
    
    def create_test_case(
        self,
        name: str,
        prompt: str,
        expected_components: List[str],
        description: str = ""
    ) -> Dict[str, any]:
        """Create a test case structure"""
        return {
            "name": name,
            "description": description,
            "prompt": prompt,
            "expected_components": expected_components,
            "validation": self.validate_prompt(prompt, expected_components),
            "evaluation": self.evaluate_prompt(prompt)
        }
    
    def run_test_cases(self, test_cases: List[Dict[str, any]]) -> Dict[str, any]:
        """Run multiple test cases and return summary"""
        results = {
            "total": len(test_cases),
            "passed": 0,
            "failed": 0,
            "details": []
        }
        
        for test in test_cases:
            validation = test.get("validation", {})
            passed = validation.get("valid", False)
            
            if passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
            results["details"].append({
                "name": test["name"],
                "passed": passed,
                "issues": validation.get("missing_components", []) + validation.get("warnings", [])
            })
        
        return results


def create_example_test_cases() -> List[Dict[str, any]]:
    """Create example test cases for demonstration"""
    tester = PromptTester()
    
    test_cases = [
        tester.create_test_case(
            name="Basic Agent Prompt",
            prompt="You are a helpful AI assistant. Use tools when needed.",
            expected_components=["assistant", "tools"],
            description="Simple agent prompt with role and tools"
        ),
        tester.create_test_case(
            name="ReAct Prompt",
            prompt="Follow the ReAct pattern: Thought, Action, Observation",
            expected_components=["thought", "action", "observation"],
            description="ReAct pattern prompt"
        ),
        tester.create_test_case(
            name="Empty Prompt",
            prompt="",
            expected_components=["role"],
            description="Invalid empty prompt"
        )
    ]
    
    return test_cases
