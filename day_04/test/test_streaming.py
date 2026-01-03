#!/usr/bin/env python3
"""Test script for streaming client"""

from streaming_client import stream_response
import os

def test_streaming():
    """Test streaming functionality"""
    
    # Test 1: Valid prompt
    print("Test 1: Valid prompt")
    response = stream_response("Say hello in 5 words")
    print(f"\n✓ Response received: {bool(response)}\n")
    
    # Test 2: Empty prompt
    print("Test 2: Empty prompt")
    try:
        stream_response("")
        print("✗ Should have failed")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}\n")
    
    # Test 3: Missing API key
    print("Test 3: Missing API key")
    original_key = os.environ.get("OPENAI_API_KEY")
    if original_key:
        del os.environ["OPENAI_API_KEY"]
    
    response = stream_response("Test")
    if response is None:
        print("✓ Handled missing API key\n")
    
    # Restore API key
    if original_key:
        os.environ["OPENAI_API_KEY"] = original_key

if __name__ == "__main__":
    test_streaming()