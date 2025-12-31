"""
Test script for Day 1 API endpoints.

This script tests all API endpoints and verifies they work correctly.
"""
import requests
import json
import sys
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def print_test(name: str):
    """Print test name."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")

def print_response(response: requests.Response):
    """Print response details."""
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_health_check():
    """Test health check endpoint."""
    print_test("Health Check")
    response = requests.get(f"{BASE_URL}/api/health")
    print_response(response)
    
    assert response.status_code == 200, "Health check should return 200"
    data = response.json()
    assert data["status"] == "healthy", "Status should be 'healthy'"
    print("✓ Health check passed")

def test_create_task():
    """Test task creation."""
    print_test("Create Task")
    
    task_data = {
        "title": "Test task from script",
        "priority": "high",
        "due_date": "2024-01-20"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/tasks",
        json=task_data
    )
    print_response(response)
    
    assert response.status_code == 201, "Task creation should return 201"
    data = response.json()
    assert data["title"] == task_data["title"], "Title should match"
    assert data["priority"] == task_data["priority"], "Priority should match"
    assert "id" in data, "Response should include task ID"
    assert data["status"] == "created", "Status should be 'created'"
    
    print("✓ Task creation passed")
    return data["id"]  # Return task ID for other tests

def test_create_task_invalid_priority():
    """Test task creation with invalid priority."""
    print_test("Create Task - Invalid Priority")
    
    task_data = {
        "title": "Test task",
        "priority": "invalid_priority"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/tasks",
        json=task_data
    )
    print_response(response)
    
    assert response.status_code == 400, "Should return 400 for invalid priority"
    print("✓ Invalid priority handling passed")

def test_create_task_invalid_date():
    """Test task creation with invalid date format."""
    print_test("Create Task - Invalid Date Format")
    
    task_data = {
        "title": "Test task",
        "due_date": "2024/01/20"  # Wrong format
    }
    
    response = requests.post(
        f"{BASE_URL}/api/tasks",
        json=task_data
    )
    print_response(response)
    
    assert response.status_code == 400, "Should return 400 for invalid date format"
    print("✓ Invalid date format handling passed")

def test_list_tasks():
    """Test listing all tasks."""
    print_test("List All Tasks")
    
    response = requests.get(f"{BASE_URL}/api/tasks")
    print_response(response)
    
    assert response.status_code == 200, "Should return 200"
    data = response.json()
    assert isinstance(data, list), "Response should be a list"
    print(f"✓ Found {len(data)} task(s)")
    return data

def test_get_task(task_id: int):
    """Test getting a specific task."""
    print_test(f"Get Task {task_id}")
    
    response = requests.get(f"{BASE_URL}/api/tasks/{task_id}")
    print_response(response)
    
    assert response.status_code == 200, "Should return 200"
    data = response.json()
    assert data["id"] == task_id, "Task ID should match"
    print("✓ Get task passed")

def test_get_task_not_found():
    """Test getting a non-existent task."""
    print_test("Get Task - Not Found")
    
    response = requests.get(f"{BASE_URL}/api/tasks/99999")
    print_response(response)
    
    assert response.status_code == 404, "Should return 404 for non-existent task"
    print("✓ Not found handling passed")

def test_update_task_status(task_id: int):
    """Test updating task status."""
    print_test(f"Update Task {task_id} Status")
    
    response = requests.patch(
        f"{BASE_URL}/api/tasks/{task_id}",
        params={"status": "in_progress"}
    )
    print_response(response)
    
    assert response.status_code == 200, "Should return 200"
    data = response.json()
    assert data["status"] == "in_progress", "Status should be updated"
    print("✓ Status update passed")

def test_update_task_invalid_status():
    """Test updating task with invalid status."""
    print_test("Update Task - Invalid Status")
    
    response = requests.patch(
        f"{BASE_URL}/api/tasks/1",
        params={"status": "invalid_status"}
    )
    print_response(response)
    
    assert response.status_code == 400, "Should return 400 for invalid status"
    print("✓ Invalid status handling passed")

def test_root_endpoint():
    """Test root endpoint."""
    print_test("Root Endpoint")
    
    response = requests.get(f"{BASE_URL}/")
    print_response(response)
    
    assert response.status_code == 200, "Should return 200"
    data = response.json()
    assert "message" in data, "Should include message"
    print("✓ Root endpoint passed")

def run_all_tests():
    """Run all API tests."""
    print("\n" + "="*60)
    print("Starting API Tests")
    print("="*60)
    print(f"Testing API at: {BASE_URL}")
    print("\nMake sure the API server is running!")
    print("Start it with: uvicorn main:app --reload")
    
    try:
        # Test root endpoint
        test_root_endpoint()
        
        # Test health check
        test_health_check()
        
        # Test task creation
        task_id = test_create_task()
        
        # Test invalid inputs
        test_create_task_invalid_priority()
        test_create_task_invalid_date()
        
        # Test listing tasks
        test_list_tasks()
        
        # Test getting specific task
        test_get_task(task_id)
        test_get_task_not_found()
        
        # Test updating task
        test_update_task_status(task_id)
        test_update_task_invalid_status()
        
        print("\n" + "="*60)
        print("All Tests Passed! ✓")
        print("="*60)
        return 0
        
    except requests.exceptions.ConnectionError:
        print("\n" + "="*60)
        print("ERROR: Could not connect to API")
        print("="*60)
        print("Make sure the API server is running:")
        print("  cd day_01")
        print("  uvicorn main:app --reload")
        return 1
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())