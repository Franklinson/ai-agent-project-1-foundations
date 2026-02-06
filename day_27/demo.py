from agent import Agent
import json

def print_result(label: str, result: dict) -> None:
    print(f"\n{'='*60}")
    print(f"{label}")
    print('='*60)
    print(json.dumps(result, indent=2))

def main():
    agent = Agent()
    
    # Test 1: Question
    print("\n🤖 Test 1: Question Input")
    result1 = agent.run("What is the weather today?")
    print_result("Result", result1)
    
    # Test 2: Command with entities
    print("\n🤖 Test 2: Command with Entities")
    result2 = agent.run("Create a meeting on 12/25/2024 at 3 PM")
    print_result("Result", result2)
    
    # Test 3: Request with email
    print("\n🤖 Test 3: Request with Email")
    result3 = agent.run("Please send report to john@example.com")
    print_result("Result", result3)
    
    # Test 4: Greeting
    print("\n🤖 Test 4: Greeting")
    result4 = agent.run("Hello, how are you?")
    print_result("Result", result4)
    
    # Show conversation history
    print("\n📜 Conversation History")
    print('='*60)
    history = agent.state.get_history()
    print(f"Total interactions: {len(history)}")
    for i, entry in enumerate(history, 1):
        print(f"\n{i}. Input: {entry['input']}")
        print(f"   Intent: {entry['perceived']['intent']}")
        print(f"   Decision: {entry['observation']['decision']}")

if __name__ == "__main__":
    main()
