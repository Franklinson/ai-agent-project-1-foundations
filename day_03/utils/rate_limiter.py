import time
from collections import deque
from typing import Optional

class RateLimiter:
    """Rate limiter for API requests"""
    
    def __init__(self, requests_per_second: Optional[float] = None,
                 requests_per_minute: Optional[int] = None,
                 requests_per_hour: Optional[int] = None):
        self.requests_per_second = requests_per_second
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        
        self.request_times = deque()
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        now = time.time()
        
        # Clean old requests
        if self.request_times:
            while self.request_times and now - self.request_times[0] > 3600:
                self.request_times.popleft()
        
        # Check per-second limit
        if self.requests_per_second:
            recent_requests = [t for t in self.request_times if now - t < 1.0]
            if len(recent_requests) >= self.requests_per_second:
                wait_time = 1.0 - (now - recent_requests[0])
                if wait_time > 0:
                    time.sleep(wait_time)
                    now = time.time()
        
        # Check per-minute limit
        if self.requests_per_minute:
            recent_requests = [t for t in self.request_times if now - t < 60.0]
            if len(recent_requests) >= self.requests_per_minute:
                wait_time = 60.0 - (now - recent_requests[0])
                if wait_time > 0:
                    time.sleep(wait_time)
                    now = time.time()
        
        # Check per-hour limit
        if self.requests_per_hour:
            recent_requests = [t for t in self.request_times if now - t < 3600.0]
            if len(recent_requests) >= self.requests_per_hour:
                wait_time = 3600.0 - (now - recent_requests[0])
                if wait_time > 0:
                    time.sleep(wait_time)
        
        # Record this request
        self.request_times.append(time.time())
    
    def get_status(self) -> dict:
        """Get current rate limit status"""
        now = time.time()
        
        # Clean old requests
        while self.request_times and now - self.request_times[0] > 3600:
            self.request_times.popleft()
        
        status = {
            "total_requests_last_hour": len(self.request_times),
            "requests_per_second_limit": self.requests_per_second,
            "requests_per_minute_limit": self.requests_per_minute,
            "requests_per_hour_limit": self.requests_per_hour
        }
        
        if self.requests_per_second:
            recent = [t for t in self.request_times if now - t < 1.0]
            status["requests_last_second"] = len(recent)
        
        if self.requests_per_minute:
            recent = [t for t in self.request_times if now - t < 60.0]
            status["requests_last_minute"] = len(recent)
        
        return status
