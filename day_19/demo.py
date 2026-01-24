from input_processor import InputHandler
import json


def main():
    handler = InputHandler()
    user_id = "user_123"
    
    # Set user preferences
    handler.context_manager.set_preference(user_id, "language", "en")
    handler.context_manager.set_preference(user_id, "timezone", "UTC")
    
    # Test cases
    test_inputs = [
        "Hello!   How are you today?",
        "What is the weather on 2024-01-15?",
        "Create a new Project called DataPipeline",
        "   \n\n  Multiple    spaces   and newlines  \n\n  ",
        "",  # Empty input
        "Why is the sky blue?"
    ]
    
    print("=" * 60)
    print("INPUT PROCESSING DEMONSTRATION")
    print("=" * 60)
    
    for i, test_input in enumerate(test_inputs, 1):
        print(f"\n--- Test {i} ---")
        print(f"Input: {repr(test_input)}")
        
        result = handler.process(test_input, user_id)
        
        if result['success']:
            data = result['data']
            print(f"Intent: {data['intent']}")
            print(f"Entities: {data['entities']}")
            print(f"Processed Text: {data['text']}")
            print(f"Message Count: {data['context']['message_count']}")
        else:
            print(f"Error ({result['error_type']}): {result['error']}")
    
    # Show conversation history
    print("\n" + "=" * 60)
    print("CONVERSATION HISTORY")
    print("=" * 60)
    recent = handler.context_manager.get_recent_messages(user_id, limit=3)
    print(json.dumps(recent, indent=2))


if __name__ == "__main__":
    main()
