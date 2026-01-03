#!/usr/bin/env python3
"""Simple test script to verify API client functionality"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_client import APIClient, APIError, AuthenticationError, RateLimitError, ServerError
from utils.rate_limiter import RateLimiter

def test_api_client():
    """Test the API client with a real endpoint"""
    print("Testing API Client...")
    
    # Test with JSONPlaceholder (free testing API)
    client = APIClient(base_url="https://jsonplaceholder.typicode.com")
    
    try:
        # Test GET request
        print("1. Testing GET request...")
        response = client.get("/posts/1")
        print(f"   Status: {response.status_code}")
        print(f"   Data: {response.json()}")
        
        # Test POST request
        print("\n2. Testing POST request...")
        data = {"title": "Test", "body": "Test body", "userId": 1}
        response = client.post("/posts", json=data)
        print(f"   Status: {response.status_code}")
        print(f"   Created: {response.json()}")
        
        # Test with rate limiter
        print("\n3. Testing with rate limiter...")
        rate_limiter = RateLimiter(requests_per_second=1)
        client_with_limiter = APIClient(
            base_url="https://jsonplaceholder.typicode.com",
            rate_limiter=rate_limiter
        )
        response = client_with_limiter.get("/posts/2")
        print(f"   Status: {response.status_code}")
        
        # Test error handling with invalid endpoint
        print("\n4. Testing error handling...")
        try:
            response = client.get("/invalid-endpoint")
        except Exception as e:
            print(f"   Handled error: {type(e).__name__}: {e}")
        
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {type(e).__name__}: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_api_client()
    sys.exit(0 if success else 1)