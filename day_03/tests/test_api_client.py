import unittest
from unittest.mock import Mock, patch, MagicMock
import requests
import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import APIClient, APIError, RateLimitError
from utils.rate_limiter import RateLimiter

# Debugging utility
class RequestLogger:
    """Utility to log API requests and responses for debugging"""
    
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.requests = []
        
    def log_request(self, method, url, headers=None, data=None):
        if self.enabled:
            log_entry = {
                'method': method,
                'url': url, 
                'headers': headers or {},
                'data': data
            }
            self.requests.append(log_entry)
            print(f"🔍 REQUEST: {method} {url}")
            if headers:
                print(f"   Headers: {headers}")
            if data:
                print(f"   Data: {data}")
    
    def log_response(self, response):
        if self.enabled:
            print(f"📥 RESPONSE: {response.status_code}")
            try:
                print(f"   Body: {response.json()}")
            except:
                print(f"   Body: {response.text[:200]}...")
    
    def get_logs(self):
        return self.requests
    
    def clear_logs(self):
        self.requests.clear()

class TestAPIClient(unittest.TestCase):
    def setUp(self):
        self.client = APIClient(
            base_url="https://api.example.com",
            api_key="test-key"
        )
        self.logger = RequestLogger()
    
    def tearDown(self):
        self.logger.clear_logs()
    
    @patch('requests.request')
    def test_successful_request(self, mock_request):
        """Test successful API request"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_request.return_value = mock_response
        
        response = self.client.get("/users/123")
        
        self.assertEqual(response.status_code, 200)
        mock_request.assert_called_once()
    
    @patch('requests.request')
    def test_retry_on_server_error(self, mock_request):
        """Test retry logic on server error"""
        # First call fails, second succeeds
        mock_request.side_effect = [
            Mock(status_code=500),
            Mock(status_code=200, json=lambda: {"data": "test"})
        ]
        
        response = self.client.get("/users/123")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_request.call_count, 2)
    
    @patch('requests.request')
    def test_debugging_utility(self, mock_request):
        """Test request/response logging utility"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"debug": "test"}
        mock_response.text = '{"debug": "test"}'
        mock_request.return_value = mock_response
        
        # Log the request
        self.logger.log_request("GET", "/test", {"Authorization": "Bearer test"}, None)
        
        response = self.client.get("/test")
        
        # Log the response
        self.logger.log_response(response)
        
        # Verify logging worked
        logs = self.logger.get_logs()
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]['method'], 'GET')
        self.assertEqual(logs[0]['url'], '/test')
    
    @patch('requests.request')
    def test_rate_limiter_integration(self, mock_request):
        """Test API client with rate limiter"""
        rate_limiter = RateLimiter(requests_per_second=1)
        client = APIClient(
            base_url="https://api.example.com",
            rate_limiter=rate_limiter
        )
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_request.return_value = mock_response
        
        # Make request - should work with rate limiter
        response = client.get("/test")
        self.assertEqual(response.status_code, 200)
        
        # Verify rate limiter status
        status = rate_limiter.get_status()
        self.assertGreater(status['total_requests_last_hour'], 0)

class TestAPIClientIntegration(unittest.TestCase):
    """Integration tests against real APIs"""
    
    def setUp(self):
        self.logger = RequestLogger()
        # Use JSONPlaceholder for real API testing
        self.client = APIClient(base_url="https://jsonplaceholder.typicode.com")
    
    def test_real_api_get_request(self):
        """Test GET request against real API"""
        try:
            self.logger.log_request("GET", "/posts/1")
            response = self.client.get("/posts/1")
            self.logger.log_response(response)
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn('id', data)
            self.assertIn('title', data)
        except requests.exceptions.ConnectionError:
            self.skipTest("No internet connection available")
    
    def test_real_api_post_request(self):
        """Test POST request against real API"""
        try:
            payload = {"title": "Test", "body": "Test body", "userId": 1}
            self.logger.log_request("POST", "/posts", data=payload)
            response = self.client.post("/posts", json=payload)
            self.logger.log_response(response)
            
            self.assertEqual(response.status_code, 201)
            data = response.json()
            self.assertIn('id', data)
        except requests.exceptions.ConnectionError:
            self.skipTest("No internet connection available")
    
    def test_real_api_error_handling(self):
        """Test error handling with real API"""
        try:
            self.logger.log_request("GET", "/posts/999999")
            
            # This should raise an APIError for non-existent resource
            with self.assertRaises(APIError):
                response = self.client.get("/posts/999999")
                
        except requests.exceptions.ConnectionError:
            self.skipTest("No internet connection available")

class TestMockServer(unittest.TestCase):
    """Tests using mock server for controlled scenarios"""
    
    @patch('requests.request')
    def test_mock_server_timeout(self, mock_request):
        """Test timeout handling with mock server"""
        mock_request.side_effect = requests.exceptions.Timeout("Request timed out")
        
        client = APIClient(base_url="https://mock.api.com", max_retries=1)
        
        with self.assertRaises(APIError) as context:
            client.get("/test")
        
        self.assertIn("timed out", str(context.exception))
    
    @patch('requests.request')
    def test_mock_server_connection_error(self, mock_request):
        """Test connection error handling"""
        mock_request.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        client = APIClient(base_url="https://mock.api.com", max_retries=1)
        
        with self.assertRaises(APIError) as context:
            client.get("/test")
        
        self.assertIn("Connection failed", str(context.exception))
    
    @patch('requests.request')
    def test_mock_server_rate_limit_retry(self, mock_request):
        """Test rate limit retry with mock server"""
        # First call rate limited, second succeeds
        rate_limit_response = Mock()
        rate_limit_response.status_code = 429
        rate_limit_response.headers = {"Retry-After": "0.1"}  # Short wait for testing
        
        success_response = Mock()
        success_response.status_code = 200
        success_response.json.return_value = {"data": "success"}
        
        mock_request.side_effect = [rate_limit_response, success_response]
        
        client = APIClient(base_url="https://mock.api.com")
        response = client.get("/test")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_request.call_count, 2)

if __name__ == "__main__":
    # Enable detailed logging for debugging
    logging.basicConfig(level=logging.INFO)
    
    # Run tests with verbose output
    unittest.main(verbosity=2)