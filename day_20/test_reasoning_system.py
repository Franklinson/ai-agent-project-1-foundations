"""Tests for Day 20 reasoning system components."""

from reasoner import Reasoner
from planner import Planner
from decision_maker import DecisionMaker
from reasoning_system import ReasoningSystem


def test_reasoner():
    """Test reasoner component."""
    print("Testing Reasoner...")
    reasoner = Reasoner()
    
    result = reasoner.reason({
        'intent': 'query',
        'entities': {'keywords': ['test']},
        'text': 'Test query'
    })
    
    assert result['success'] == True
    assert result['goal'] == 'retrieve_information'
    assert 'reasoning' in result
    print("✅ Reasoner test passed")


def test_planner():
    """Test planner component."""
    print("Testing Planner...")
    planner = Planner()
    
    plan = planner.decompose_goal('retrieve_information')
    
    assert plan.goal == 'retrieve_information'
    assert len(plan.steps) > 0
    assert plan.steps[0]['id'] == 1
    print("✅ Planner test passed")


def test_decision_maker():
    """Test decision maker component."""
    print("Testing Decision Maker...")
    decision_maker = DecisionMaker()
    
    result = decision_maker.select_tool('query', 'search_knowledge_base', {'keywords': ['test']})
    
    assert result['success'] == True
    assert result['tool'] is not None
    assert 'parameters' in result
    print("✅ Decision Maker test passed")


def test_reasoning_system():
    """Test integrated reasoning system."""
    print("Testing Reasoning System...")
    system = ReasoningSystem()
    
    result = system.process({
        'intent': 'command',
        'entities': {'keywords': ['create']},
        'text': 'Create something'
    })
    
    assert result['success'] == True
    assert result['goal'] == 'execute_action'
    assert 'action_plan' in result
    assert len(result['action_plan']) > 0
    print("✅ Reasoning System test passed")


def test_intent_types():
    """Test different intent types."""
    print("Testing Multiple Intent Types...")
    system = ReasoningSystem()
    
    intents = ['query', 'command', 'greeting']
    
    for intent in intents:
        result = system.process({
            'intent': intent,
            'entities': {},
            'text': f'Test {intent}'
        })
        assert result['success'] == True
        print(f"  ✅ {intent} intent handled")
    
    print("✅ Intent types test passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("🧪 RUNNING REASONING SYSTEM TESTS")
    print("="*60 + "\n")
    
    tests = [
        test_reasoner,
        test_planner,
        test_decision_maker,
        test_reasoning_system,
        test_intent_types
    ]
    
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"❌ Test failed: {test.__name__}")
            print(f"   Error: {e}")
            return False
        except Exception as e:
            print(f"❌ Test error: {test.__name__}")
            print(f"   Error: {e}")
            return False
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED")
    print("="*60 + "\n")
    return True


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
