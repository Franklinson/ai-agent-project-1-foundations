#!/usr/bin/env python3
"""Test script for webhook server"""

import requests
import json
import time
import sys

def test_webhook_server(base_url="http://localhost:5000"):
    """Test the webhook server with various event types"""
    print("🧪 Testing Webhook Server...")
    
    # Test payloads
    test_events = [
        {
            "id": "test-001",
            "event": "task.created",
            "timestamp": "2024-01-15T10:30:00Z",
            "task": {
                "id": "task-123",
                "title": "Complete project documentation",
                "status": "pending"
            }
        },
        {
            "id": "test-002", 
            "event": "user.registered",
            "timestamp": "2024-01-15T10:35:00Z",
            "user": {
                "id": "user-456",
                "email": "jane@example.com",
                "name": "Jane Smith"
            }
        },
        {
            "id": "test-003",
            "event": "payment.completed", 
            "timestamp": "2024-01-15T10:40:00Z",
            "payment": {
                "id": "pay-789",
                "amount": "99.99",
                "currency": "USD"
            }
        },
        {
            "id": "test-004",
            "event": "order.shipped",
            "timestamp": "2024-01-15T10:45:00Z", 
            "order": {
                "id": "order-101",
                "tracking_number": "1Z999AA1234567890"
            }
        }
    ]
    
    try:
        # Test health endpoint
        print("1. Testing health endpoint...")
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test events list
        print("\n2. Testing events list...")
        response = requests.get(f"{base_url}/webhook/events")
        print(f"   Status: {response.status_code}")
        events = response.json().get("supported_events", [])
        print(f"   Supported events: {len(events)}")
        
        # Test webhook events
        print("\n3. Testing webhook events...")
        for i, event_data in enumerate(test_events, 1):
            print(f"\n   3.{i} Testing {event_data['event']}...")
            
            response = requests.post(
                f"{base_url}/webhook/test",
                json=event_data,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"        Status: {response.status_code}")
            print(f"        Response: {response.json()}")
            
            time.sleep(0.5)  # Small delay between requests
        
        # Test idempotency
        print("\n4. Testing idempotency...")
        duplicate_event = test_events[0]  # Send same event twice
        
        response1 = requests.post(f"{base_url}/webhook/test", json=duplicate_event)
        response2 = requests.post(f"{base_url}/webhook/test", json=duplicate_event)
        
        print(f"   First request: {response1.status_code}")
        print(f"   Duplicate request: {response2.status_code}")
        
        # Test unknown event
        print("\n5. Testing unknown event...")
        unknown_event = {
            "id": "test-999",
            "event": "unknown.event",
            "data": {"test": "data"}
        }
        
        response = requests.post(f"{base_url}/webhook/test", json=unknown_event)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        print("\n✅ All webhook tests completed!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to webhook server.")
        print("   Make sure the server is running: python webhook_server.py")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    # Allow custom URL as command line argument
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    success = test_webhook_server(url)
    sys.exit(0 if success else 1)