from openai import OpenAI
import os
import sys

def get_client():
    """Initialize OpenAI client with error handling"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return OpenAI(api_key=api_key)

def stream_response(prompt):
    """Stream LLM response with error handling"""
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")
    
    try:
        client = get_client()
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        
        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                token = chunk.choices[0].delta.content
                full_response += token
                print(token, end="", flush=True)
        
        return full_response
    
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    response = stream_response("Tell me a short story")
    print("\n\nComplete response received")
