import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'day_19'))

from reasoning_system import ReasoningSystem
from input_processor import InputHandler
import json


def print_result(title, result):
    """Pretty print results."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print('='*60)
    print(json.dumps(result, indent=2))


def demo_with_input_processor():
    """Demonstrate full pipeline with Day 19 input processor."""
    print("\n🤖 REASONING SYSTEM DEMO - WITH INPUT PROCESSOR")
    print("="*60)
    
    input_handler = InputHandler()
    reasoning_system = ReasoningSystem()
    
    test_cases = [
        ("What is the weather today?", "user_001"),
        ("Create a new project called MyApp", "user_002"),
        ("Hello there!", "user_003")
    ]
    
    for raw_input, user_id in test_cases:
        print(f"\n📝 Input: '{raw_input}'")
        
        # Process input
        processed = input_handler.process(raw_input, user_id)
        
        if not processed['success']:
            print(f"❌ Input processing failed: {processed['error']}")
            continue
        
        # Run through reasoning system
        result = reasoning_system.process(processed['data'])
        print_result(f"Result for: {raw_input}", result)


def demo_standalone():
    """Demonstrate reasoning system with mock processed input."""
    print("\n🤖 REASONING SYSTEM DEMO - STANDALONE")
    print("="*60)
    
    reasoning_system = ReasoningSystem()
    
    test_inputs = [
        {
            'intent': 'query',
            'entities': {'keywords': ['weather', 'today']},
            'text': 'What is the weather today?'
        },
        {
            'intent': 'command',
            'entities': {'keywords': ['Create', 'MyApp']},
            'text': 'Create a new project called MyApp'
        },
        {
            'intent': 'greeting',
            'entities': {},
            'text': 'Hello there!'
        }
    ]
    
    for processed_input in test_inputs:
        result = reasoning_system.process(processed_input)
        print_result(f"Input: {processed_input['text']}", result)


def main():
    """Run demonstrations."""
    print("\n" + "="*60)
    print("🚀 INTEGRATED REASONING SYSTEM DEMONSTRATION")
    print("="*60)
    
    # Try with input processor first
    try:
        demo_with_input_processor()
    except ImportError:
        print("\n⚠️  Day 19 input processor not available, using standalone demo")
        demo_standalone()
    except Exception as e:
        print(f"\n⚠️  Error with input processor: {e}")
        print("Falling back to standalone demo")
        demo_standalone()


if __name__ == "__main__":
    main()
