import os
import time
import requests
import logging
from typing import Optional, Dict, Any
from functools import wraps
from utils.rate_limiter import RateLimiter

logger = logging.getLogger(__name__)

class APIError(Exception):
    """Base API error"""
    pass

class AuthenticationError(APIError):
    """Authentication failed"""
    pass

class RateLimitError(APIError):
    """Rate limit exceeded"""
    pass

class ServerError(APIError):
    """Server error"""
    pass

class APIClient:
    """Production-ready API client with authentication, retry, and rate limiting"""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None,
                 oauth_client_id: Optional[str] = None,
                 oauth_client_secret: Optional[str] = None,
                 max_retries: int = 3,
                 base_delay: float = 1.0,
                 rate_limiter: Optional[RateLimiter] = None):
        if not base_url:
            raise ValueError("base_url is required")
        
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key or os.getenv("API_KEY")
        self.oauth_client_id = oauth_client_id
        self.oauth_client_secret = oauth_client_secret
        self.max_retries = max(0, max_retries)
        self.base_delay = max(0.1, base_delay)
        self.access_token = None
        self.token_expires_at = None
        self.rate_limiter = rate_limiter
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers"""
        headers = {}
        
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        elif self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        return headers
    
    def _exponential_backoff(self, attempt: int) -> float:
        """Calculate exponential backoff delay"""
        delay = min(self.base_delay * (2 ** attempt), 300)  # Max 5 minutes
        return delay
    
    def _should_retry(self, response: requests.Response, attempt: int) -> bool:
        """Determine if request should be retried"""
        if attempt >= self.max_retries:
            return False
        
        # Retry on server errors
        if response.status_code >= 500:
            return True
        
        # Retry on rate limiting
        if response.status_code == 429:
            return True
        
        # Retry on 401 if we can refresh token
        if response.status_code == 401 and self.oauth_client_id:
            if self._refresh_oauth_token():
                return True
        
        return False
    
    def _refresh_oauth_token(self) -> bool:
        """Refresh OAuth token"""
        # Implement OAuth token refresh logic
        # This is a placeholder - implement based on your OAuth provider
        return False
    
    def _handle_rate_limit(self, response: requests.Response) -> float:
        """Handle rate limit response and return wait time"""
        try:
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                return max(0.1, float(retry_after))
            
            # Calculate from reset time if available
            reset_time = response.headers.get("X-RateLimit-Reset")
            if reset_time:
                wait_time = max(0.1, int(reset_time) - time.time())
                return wait_time
        except (ValueError, TypeError) as e:
            logger.warning(f"Failed to parse rate limit headers: {e}")
        
        # Default exponential backoff
        return self._exponential_backoff(0)
    
    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make API request with retry logic"""
        if not method:
            raise ValueError("method is required")
        if not endpoint:
            raise ValueError("endpoint is required")
        
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            headers = self._get_auth_headers()
            headers.update(kwargs.get("headers", {}))
            kwargs["headers"] = headers
            
            # Set default timeout if not provided
            if "timeout" not in kwargs:
                kwargs["timeout"] = 30
            
            last_exception = None
        except Exception as e:
            raise APIError(f"Failed to prepare request: {e}") from e
        
        for attempt in range(self.max_retries + 1):
            try:
                # Apply rate limiting before making request
                if self.rate_limiter:
                    self.rate_limiter.wait_if_needed()
                
                response = requests.request(method, url, **kwargs)
                
                # Handle specific error cases
                if response.status_code == 401:
                    if attempt == 0 and self.oauth_client_id:
                        # Try to refresh token once
                        if self._refresh_oauth_token():
                            headers = self._get_auth_headers()
                            headers.update(kwargs.get("headers", {}))
                            kwargs["headers"] = headers
                            continue
                    raise AuthenticationError(f"Authentication failed: {response.text}")
                
                elif response.status_code == 429:
                    if attempt < self.max_retries:
                        wait_time = self._handle_rate_limit(response)
                        logger.warning(f"Rate limited. Waiting {wait_time:.1f}s...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise RateLimitError(f"Rate limit exceeded after {self.max_retries} retries")
                
                elif response.status_code >= 500:
                    if attempt < self.max_retries:
                        wait_time = self._exponential_backoff(attempt)
                        logger.warning(
                            f"Server error {response.status_code} (attempt {attempt + 1}/{self.max_retries + 1}). "
                            f"Retrying after {wait_time:.1f}s..."
                        )
                        time.sleep(wait_time)
                        continue
                    else:
                        error_text = getattr(response, 'text', 'Unknown error')
                        raise ServerError(f"Server error {response.status_code}: {error_text}")
                
                elif 400 <= response.status_code < 500:
                    # Client errors (except 401, 429 handled above)
                    error_text = getattr(response, 'text', 'Unknown error')
                    raise APIError(f"Client error {response.status_code}: {error_text}")
                
                # Log successful request
                if response.status_code < 400:
                    logger.info(f"{method} {endpoint} - {response.status_code}")
                
                # Raise for other HTTP errors (4xx except 401, 429)
                response.raise_for_status()
                return response
            
            except requests.exceptions.Timeout as e:
                last_exception = e
                if attempt < self.max_retries:
                    wait_time = self._exponential_backoff(attempt)
                    logger.warning(f"Timeout (attempt {attempt + 1}/{self.max_retries + 1}). Retrying after {wait_time:.1f}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise APIError(f"Request timed out after {self.max_retries + 1} attempts") from e
            
            except requests.exceptions.ConnectionError as e:
                last_exception = e
                if attempt < self.max_retries:
                    wait_time = self._exponential_backoff(attempt)
                    logger.warning(f"Connection error (attempt {attempt + 1}/{self.max_retries + 1}). Retrying after {wait_time:.1f}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise APIError(f"Connection failed after {self.max_retries + 1} attempts") from e
            
            except requests.exceptions.RequestException as e:
                # Don't retry on other request exceptions
                logger.error(f"Request failed: {e}")
                raise APIError(f"Request failed: {e}") from e
            
            except Exception as e:
                # Catch any other unexpected errors
                logger.error(f"Unexpected error: {e}")
                raise APIError(f"Unexpected error: {e}") from e
        
        # If we get here, all retries failed
        if last_exception:
            logger.error(f"All retries failed. Last error: {last_exception}")
            raise APIError(f"Request failed after {self.max_retries + 1} attempts") from last_exception
        
        return response
    
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """GET request"""
        return self.request("GET", endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """POST request"""
        return self.request("POST", endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> requests.Response:
        """PUT request"""
        return self.request("PUT", endpoint, **kwargs)
    
    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        """PATCH request"""
        return self.request("PATCH", endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """DELETE request"""
        return self.request("DELETE", endpoint, **kwargs)
