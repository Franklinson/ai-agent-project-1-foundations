"""Test suite loader and runner utility."""

import json
from typing import Dict, List, Any
from pathlib import Path


class TestSuiteLoader:
    """Load and manage test suites."""
    
    def __init__(self, test_cases_dir: str = "test_cases"):
        self.test_cases_dir = Path(test_cases_dir)
    
    def load_suite(self, suite_name: str) -> Dict[str, Any]:
        """Load a specific test suite by name."""
        suite_path = self.test_cases_dir / f"{suite_name}.json"
        with open(suite_path, 'r') as f:
            return json.load(f)
    
    def list_suites(self) -> List[str]:
        """List all available test suites."""
        return [f.stem for f in self.test_cases_dir.glob("*.json")]
    
    def get_test_cases(self, suite_name: str) -> List[Dict]:
        """Get test cases from a suite."""
        suite = self.load_suite(suite_name)
        return suite.get('test_cases', [])
    
    def filter_by_category(self, test_cases: List[Dict], category: str) -> List[Dict]:
        """Filter test cases by category."""
        return [tc for tc in test_cases if tc.get('category') == category]
    
    def filter_by_scenario(self, test_cases: List[Dict], scenario: str) -> List[Dict]:
        """Filter test cases by scenario type."""
        return [tc for tc in test_cases if tc.get('scenario') == scenario]
    
    def get_suite_info(self, suite_name: str) -> Dict[str, Any]:
        """Get summary information about a test suite."""
        suite = self.load_suite(suite_name)
        test_cases = suite.get('test_cases', [])
        
        categories = {}
        scenarios = {}
        
        for tc in test_cases:
            cat = tc.get('category', 'unknown')
            scen = tc.get('scenario', 'unknown')
            
            categories[cat] = categories.get(cat, 0) + 1
            scenarios[scen] = scenarios.get(scen, 0) + 1
        
        return {
            "name": suite.get('test_suite_name', suite_name),
            "version": suite.get('version', 'unknown'),
            "description": suite.get('description', ''),
            "total_tests": len(test_cases),
            "categories": categories,
            "scenarios": scenarios
        }


if __name__ == "__main__":
    loader = TestSuiteLoader()
    
    print("="*60)
    print("AVAILABLE TEST SUITES")
    print("="*60 + "\n")
    
    # List all suites
    suites = loader.list_suites()
    print(f"Found {len(suites)} test suite(s):\n")
    
    for suite_name in suites:
        info = loader.get_suite_info(suite_name)
        print(f"📋 {info['name']}")
        print(f"   File: {suite_name}.json")
        print(f"   Version: {info['version']}")
        print(f"   Tests: {info['total_tests']}")
        print(f"   Categories: {', '.join(info['categories'].keys())}")
        print(f"   Description: {info['description'][:60]}...")
        print()
    
    # Show detailed info for comprehensive suite
    if "test_suite" in suites:
        print("="*60)
        print("COMPREHENSIVE SUITE DETAILS")
        print("="*60 + "\n")
        
        info = loader.get_suite_info("test_suite")
        
        print("Categories:")
        for cat, count in sorted(info['categories'].items()):
            print(f"  {cat:20s}: {count} test(s)")
        
        print("\nScenarios:")
        for scen, count in sorted(info['scenarios'].items()):
            print(f"  {scen:20s}: {count} test(s)")
        
        # Show sample test cases
        test_cases = loader.get_test_cases("test_suite")
        print(f"\nSample Test Cases:")
        for tc in test_cases[:3]:
            print(f"\n  [{tc['id']}] {tc['description']}")
            print(f"  Input: {tc['input'][:50]}...")
            print(f"  Category: {tc['category']} | Scenario: {tc['scenario']}")
