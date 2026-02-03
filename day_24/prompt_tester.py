"""
Prompt testing and evaluation utilities.
Validates prompt structure, completeness, and quality.
"""

from dataclasses import dataclass
from typing import List, Dict
import re


@dataclass
class TestCase:
    """Structure for prompt test cases."""
    name: str
    prompt_content: str
    expected_components: List[str]
    expected_tools: List[str] = None
    expected_examples: int = 0


@dataclass
class ValidationResult:
    """Result of prompt validation."""
    passed: bool
    score: float
    issues: List[str]
    strengths: List[str]


class PromptTester:
    """Utilities to test and evaluate prompts."""
    
    def __init__(self):
        self.required_sections = ['role', 'instructions', 'format', 'examples']
    
    def validate_prompt(self, prompt: str) -> ValidationResult:
        """
        Validate prompt structure and completeness.
        
        Args:
            prompt: Prompt text to validate
            
        Returns:
            ValidationResult with score and feedback
        """
        issues = []
        strengths = []
        score = 0.0
        max_score = 10.0
        
        # Check for role definition
        if self._has_role_definition(prompt):
            score += 2.0
            strengths.append("Clear role definition present")
        else:
            issues.append("Missing clear role definition")
        
        # Check for specific instructions
        if self._has_specific_instructions(prompt):
            score += 2.0
            strengths.append("Specific instructions provided")
        else:
            issues.append("Instructions too vague or missing")
        
        # Check for tool descriptions
        if self._has_tool_descriptions(prompt):
            score += 2.0
            strengths.append("Tool descriptions included")
        else:
            issues.append("Missing tool descriptions")
        
        # Check for format specifications
        if self._has_format_specifications(prompt):
            score += 2.0
            strengths.append("Output format specified")
        else:
            issues.append("No clear output format")
        
        # Check for examples
        if self._has_examples(prompt):
            score += 2.0
            strengths.append("Examples provided")
        else:
            issues.append("Missing concrete examples")
        
        passed = score >= 7.0
        return ValidationResult(passed, score, issues, strengths)
    
    def _has_role_definition(self, prompt: str) -> bool:
        """Check if prompt has clear role definition."""
        role_patterns = [
            r'(?i)you are (a|an) .+ agent',
            r'(?i)## role',
            r'(?i)role:',
        ]
        return any(re.search(pattern, prompt) for pattern in role_patterns)
    
    def _has_specific_instructions(self, prompt: str) -> bool:
        """Check if prompt has specific, actionable instructions."""
        instruction_patterns = [
            r'(?i)## (core )?instructions',
            r'(?i)instructions:',
            r'(?i)## process',
        ]
        has_section = any(re.search(pattern, prompt) for pattern in instruction_patterns)
        
        # Check for bullet points or numbered lists
        has_list = bool(re.search(r'(^|\n)[-*\d]+\.?\s+', prompt))
        
        return has_section and has_list
    
    def _has_tool_descriptions(self, prompt: str) -> bool:
        """Check if prompt describes available tools."""
        tool_patterns = [
            r'(?i)## (available )?tools',
            r'(?i)### \w+\(',  # Function signature
            r'(?i)tool selection',
        ]
        return any(re.search(pattern, prompt) for pattern in tool_patterns)
    
    def _has_format_specifications(self, prompt: str) -> bool:
        """Check if prompt specifies output format."""
        format_patterns = [
            r'(?i)## (response |output )?format',
            r'(?i)format:',
            r'```[\s\S]+?```',  # Code blocks for format examples
        ]
        return any(re.search(pattern, prompt) for pattern in format_patterns)
    
    def _has_examples(self, prompt: str) -> bool:
        """Check if prompt includes examples."""
        example_patterns = [
            r'(?i)## examples?',
            r'(?i)\*\*user\*\*:',
            r'(?i)\*\*agent( response)?\*\*:',
        ]
        return any(re.search(pattern, prompt) for pattern in example_patterns)
    
    def count_tools(self, prompt: str) -> int:
        """Count number of tools described in prompt."""
        tool_pattern = r'### \w+\('
        return len(re.findall(tool_pattern, prompt))
    
    def count_examples(self, prompt: str) -> int:
        """Count number of examples in prompt."""
        example_pattern = r'(?i)\*\*user\*\*:'
        return len(re.findall(example_pattern, prompt))
    
    def check_components(self, prompt: str, expected: List[str]) -> Dict[str, bool]:
        """
        Check if expected components are present in prompt.
        
        Args:
            prompt: Prompt text
            expected: List of expected keywords/phrases
            
        Returns:
            Dict mapping component to presence boolean
        """
        return {
            component: component.lower() in prompt.lower()
            for component in expected
        }
    
    def evaluate_prompt(self, test_case: TestCase) -> Dict:
        """
        Evaluate a prompt against test case expectations.
        
        Args:
            test_case: TestCase with prompt and expectations
            
        Returns:
            Dict with evaluation results
        """
        validation = self.validate_prompt(test_case.prompt_content)
        
        # Check expected components
        component_results = self.check_components(
            test_case.prompt_content,
            test_case.expected_components
        )
        components_present = sum(component_results.values())
        components_total = len(test_case.expected_components)
        
        # Check tools if specified
        tools_count = self.count_tools(test_case.prompt_content)
        tools_match = True
        if test_case.expected_tools:
            tools_match = tools_count >= len(test_case.expected_tools)
        
        # Check examples
        examples_count = self.count_examples(test_case.prompt_content)
        examples_match = examples_count >= test_case.expected_examples
        
        return {
            'test_name': test_case.name,
            'validation': validation,
            'components': {
                'present': components_present,
                'total': components_total,
                'details': component_results
            },
            'tools': {
                'count': tools_count,
                'match': tools_match
            },
            'examples': {
                'count': examples_count,
                'match': examples_match
            },
            'overall_pass': (
                validation.passed and
                components_present == components_total and
                tools_match and
                examples_match
            )
        }
    
    def print_results(self, results: Dict):
        """Print evaluation results in readable format."""
        print(f"\n{'='*60}")
        print(f"TEST: {results['test_name']}")
        print(f"{'='*60}")
        
        val = results['validation']
        print(f"\n✓ Validation Score: {val.score}/10.0 - {'PASS' if val.passed else 'FAIL'}")
        
        if val.strengths:
            print("\nStrengths:")
            for strength in val.strengths:
                print(f"  ✓ {strength}")
        
        if val.issues:
            print("\nIssues:")
            for issue in val.issues:
                print(f"  ✗ {issue}")
        
        comp = results['components']
        print(f"\n✓ Components: {comp['present']}/{comp['total']}")
        for component, present in comp['details'].items():
            status = "✓" if present else "✗"
            print(f"  {status} {component}")
        
        print(f"\n✓ Tools: {results['tools']['count']} found")
        print(f"✓ Examples: {results['examples']['count']} found")
        
        print(f"\n{'='*60}")
        print(f"OVERALL: {'✓ PASS' if results['overall_pass'] else '✗ FAIL'}")
        print(f"{'='*60}")


def create_example_test_cases() -> List[TestCase]:
    """Create example test cases for each prompt type."""
    import os
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Weather agent test case
    weather_test = TestCase(
        name="Weather Agent Prompt",
        prompt_content=open(f'{base_path}/prompts/weather_agent_prompt.md').read(),
        expected_components=[
            'location', 'temperature', 'conditions', 'humidity',
            'wind', 'forecast', 'advice'
        ],
        expected_tools=['get_current_weather', 'get_forecast', 'get_weather_alerts'],
        expected_examples=2
    )
    
    # Email agent test case
    email_test = TestCase(
        name="Email Agent Prompt",
        prompt_content=open(f'{base_path}/prompts/email_agent_prompt.md').read(),
        expected_components=[
            'send', 'search', 'compose', 'recipient', 'subject',
            'body', 'confirm', 'context'
        ],
        expected_tools=['send_email', 'search_emails', 'get_email'],
        expected_examples=3
    )
    
    # Research agent test case
    research_test = TestCase(
        name="Research Agent Prompt",
        prompt_content=open(f'{base_path}/prompts/research_agent_prompt.md').read(),
        expected_components=[
            'search', 'sources', 'verify', 'cite', 'synthesize',
            'findings', 'conclusion'
        ],
        expected_tools=['web_search', 'academic_search', 'fact_check'],
        expected_examples=2
    )
    
    return [weather_test, email_test, research_test]


def run_tests():
    """Run all test cases and print results."""
    tester = PromptTester()
    test_cases = create_example_test_cases()
    
    print("\n" + "="*60)
    print("PROMPT TESTING SUITE")
    print("="*60)
    
    all_passed = True
    for test_case in test_cases:
        results = tester.evaluate_prompt(test_case)
        tester.print_results(results)
        if not results['overall_pass']:
            all_passed = False
    
    print("\n" + "="*60)
    print(f"FINAL RESULT: {'✓ ALL TESTS PASSED' if all_passed else '✗ SOME TESTS FAILED'}")
    print("="*60 + "\n")


if __name__ == "__main__":
    run_tests()
