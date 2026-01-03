#!/usr/bin/env python3
"""Test chat interface for StreamingChatAgent"""

from chat_agent import StreamingChatAgent

def test_chat_interface():
    """Test the chat agent interface"""
    agent = StreamingChatAgent()
    
    print("Chat Agent Test (type 'quit' to exit, 'clear' to reset)")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'clear':
                agent.clear_history()
                print("History cleared.")
                continue
            elif not user_input:
                continue
            
            print("Agent: ", end="")
            agent.chat(user_input)
            print()  # New line after streaming
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_chat_interface()