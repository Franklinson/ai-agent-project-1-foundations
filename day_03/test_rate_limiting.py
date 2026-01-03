#!/usr/bin/env python3
"""Test rate limiting functionality"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_client import APIClient
from utils.rate_limiter import RateLimiter

def test_rate_limiting():
    """Test rate limiting with API client"""
    print("Testing Rate Limiting...")
    
    # Create rate limiter: 2 requests per second
    rate_limiter = RateLimiter(requests_per_second=2)
    
    # Create API client with rate limiter
    client = APIClient(
        base_url="https://jsonplaceholder.typicode.com",
        rate_limiter=rate_limiter
    )
    
    print("Making 5 requests with 2 req/sec limit...")
    start_time = time.time()
    
    for i in range(5):
        try:
            response = client.get(f"/posts/{i+1}")
            elapsed = time.time() - start_time
            print(f"Request {i+1}: Status {response.status_code} at {elapsed:.2f}s")
            
            # Check rate limiter status
            status = rate_limiter.get_status()
            print(f"  Rate limiter: {status['requests_last_second']} req/sec")
            
        except Exception as e:
            print(f"Request {i+1} failed: {e}")
    
    total_time = time.time() - start_time
    print(f"\nTotal time: {total_time:.2f}s")
    
    # Should take at least 2 seconds for 5 requests at 2 req/sec
    if total_time >= 2.0:
        print("✅ Rate limiting working correctly!")
        return True
    else:
        print("❌ Rate limiting may not be working")
        return False

if __name__ == "__main__":
    success = test_rate_limiting()
    sys.exit(0 if success else 1)