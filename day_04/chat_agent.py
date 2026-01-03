from openai import OpenAI
import os

class StreamingChatAgent:
    def __init__(self, max_history=10):
        self.history = []
        self.max_history = max_history
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def chat(self, message):
        """Handle chat with streaming"""
        if not message.strip():
            return "Please provide a message."
            
        self.history.append({"role": "user", "content": message})
        self._trim_history()
        
        try:
            response = ""
            for token in self._stream():
                response += token
                print(token, end="", flush=True)
            
            self.history.append({"role": "assistant", "content": response})
            return response
        except Exception as e:
            return f"Error: {e}"
    
    def _stream(self):
        """Stream tokens from LLM"""
        stream = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.history,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    def _trim_history(self):
        """Keep conversation history within limits"""
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def clear_history(self):
        """Clear conversation history"""
        self.history = []
