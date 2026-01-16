import tiktoken
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


class ContextManager:
    def __init__(self, model="gpt-4", max_tokens=100000, recent_count=10):
        self.model = model
        self.encoding = tiktoken.encoding_for_model(model)
        self.max_tokens = max_tokens
        self.recent_count = recent_count
        self.messages = []
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def count_tokens(self, text):
        """Count tokens"""
        return len(self.encoding.encode(text))
    
    def add_message(self, role, content):
        """Add message and manage context"""
        self.messages.append({"role": role, "content": content})
        self._manage_context()
    
    def _manage_context(self):
        """Manage context to stay within limits"""
        total = sum(self.count_tokens(str(m)) for m in self.messages)
        
        if total > self.max_tokens:
            system_msgs = [m for m in self.messages if m["role"] == "system"]
            non_system = [m for m in self.messages if m["role"] != "system"]
            
            recent = non_system[-self.recent_count:]
            old = non_system[:-self.recent_count]
            
            if old:
                summary = self._summarize(old)
                self.messages = system_msgs + [
                    {"role": "system", "content": f"Previous conversation summary: {summary}"}
                ] + recent
    
    def _summarize(self, messages):
        """Summarize old messages using LLM"""
        conversation = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": "Summarize this conversation concisely, preserving key information and context."
                }, {
                    "role": "user",
                    "content": conversation
                }],
                max_tokens=200
            )
            return response.choices[0].message.content
        except:
            return "Previous conversation: " + conversation[:200]
    
    def get_context(self):
        """Get current context"""
        return self.messages

def test_context_manager():
    """Test with long conversations"""
    print("=== Testing Context Manager ===")
    
    # Test 1: Basic functionality
    manager = ContextManager(max_tokens=500, recent_count=6)
    for i in range(20):
        manager.add_message("user", f"This is user message number {i} with some additional text to increase token count")
        manager.add_message("assistant", f"This is assistant response number {i} with detailed information")
    
    print(f"\nTest 1 - Long conversation:")
    print(f"Final message count: {len(manager.get_context())}")
    print(f"Total tokens: {sum(manager.count_tokens(str(m)) for m in manager.get_context())}")
    
    # Test 2: Token counting
    manager2 = ContextManager()
    test_text = "Hello, how are you today?"
    tokens = manager2.count_tokens(test_text)
    print(f"\nTest 2 - Token counting:")
    print(f"Text: '{test_text}'")
    print(f"Tokens: {tokens}")
    
    # Test 3: Context retrieval
    manager3 = ContextManager(recent_count=4)
    manager3.add_message("system", "You are a helpful assistant")
    manager3.add_message("user", "Hello")
    manager3.add_message("assistant", "Hi there!")
    print(f"\nTest 3 - Context retrieval:")
    print(f"Messages: {manager3.get_context()}")
    
    print("\n=== All tests completed ===")

if __name__ == "__main__":
    test_context_manager()
