# Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the Refined AI Agent in production environments.

---

## Prerequisites

### System Requirements

- **Operating System**: Linux (Ubuntu 20.04+), macOS (10.15+), or Windows 10+
- **Python**: 3.11 or higher
- **Memory**: Minimum 512MB RAM per agent instance
- **CPU**: 1+ cores recommended
- **Disk Space**: 100MB for application and dependencies

### Software Dependencies

- Python 3.11+
- pip (Python package manager)
- virtualenv (recommended)
- Git (for version control)

---

## Environment Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd ai-agent-project-1-foundations/day_30
```

### 2. Create Virtual Environment

**Linux/macOS**:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**:
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**requirements.txt** (if not exists, create with):
```
# Core dependencies
typing-extensions>=4.0.0

# Optional: For production deployments
gunicorn>=20.1.0  # WSGI server
uvicorn>=0.20.0   # ASGI server
fastapi>=0.95.0   # API framework
pydantic>=2.0.0   # Data validation
```

### 4. Verify Installation

```bash
python3 -c "from refined_agent import RefinedAgent; print('Installation successful')"
```

---

## Configuration

### Environment Variables

Create `.env` file in the project root:

```bash
# Agent Configuration
AGENT_MAX_ITERATIONS=5
AGENT_TIMEOUT=30

# Logging
LOG_LEVEL=INFO
LOG_FILE=agent.log

# Performance
ENABLE_CACHING=true
CACHE_TTL=3600

# Security
RATE_LIMIT=100
RATE_LIMIT_PERIOD=60
```

### Configuration File

Create `config.py`:

```python
import os
from typing import Dict, Any

class AgentConfig:
    """Agent configuration"""
    
    # Agent settings
    MAX_ITERATIONS = int(os.getenv('AGENT_MAX_ITERATIONS', 5))
    TIMEOUT = int(os.getenv('AGENT_TIMEOUT', 30))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'agent.log')
    
    # Performance
    ENABLE_CACHING = os.getenv('ENABLE_CACHING', 'true').lower() == 'true'
    CACHE_TTL = int(os.getenv('CACHE_TTL', 3600))
    
    # Security
    RATE_LIMIT = int(os.getenv('RATE_LIMIT', 100))
    RATE_LIMIT_PERIOD = int(os.getenv('RATE_LIMIT_PERIOD', 60))
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            'max_iterations': cls.MAX_ITERATIONS,
            'timeout': cls.TIMEOUT,
            'log_level': cls.LOG_LEVEL,
            'enable_caching': cls.ENABLE_CACHING
        }
```

### Logging Configuration

Create `logging_config.py`:

```python
import logging
import sys
from config import AgentConfig

def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=getattr(logging, AgentConfig.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(AgentConfig.LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger('refined_agent')

logger = setup_logging()
```

---

## Deployment Options

### Option 1: Standalone Script

**Use Case**: Simple deployments, testing, development

**Deployment**:

1. Create `run_agent.py`:
```python
from refined_agent import RefinedAgent
from config import AgentConfig
from logging_config import logger

def main():
    agent = RefinedAgent()
    logger.info("Agent initialized")
    
    # Example usage
    result = agent.run("Calculate 15 + 25", max_iterations=AgentConfig.MAX_ITERATIONS)
    logger.info(f"Result: {result['status']}")
    
    return result

if __name__ == "__main__":
    main()
```

2. Run:
```bash
python3 run_agent.py
```

### Option 2: REST API with FastAPI

**Use Case**: Web services, microservices, API endpoints

**Deployment**:

1. Create `api_server.py`:
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from refined_agent import RefinedAgent
from config import AgentConfig
from logging_config import logger

app = FastAPI(title="Refined AI Agent API")
agent = RefinedAgent()

class AgentRequest(BaseModel):
    user_input: str
    goal: str = None
    max_iterations: int = AgentConfig.MAX_ITERATIONS

class AgentResponse(BaseModel):
    status: str
    iterations: int
    final_decision: str
    termination_reason: str

@app.post("/agent/run", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    """Execute agent"""
    try:
        result = agent.run(
            request.user_input,
            request.goal,
            request.max_iterations
        )
        return AgentResponse(**result)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

2. Run:
```bash
uvicorn api_server:app --host 0.0.0.0 --port 8000 --workers 4
```

3. Test:
```bash
curl -X POST http://localhost:8000/agent/run \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Calculate 15 + 25"}'
```

### Option 3: Docker Container

**Use Case**: Cloud deployments, Kubernetes, scalable services

**Deployment**:

1. Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY refined_agent.py .
COPY config.py .
COPY logging_config.py .
COPY api_server.py .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. Build:
```bash
docker build -t refined-agent:latest .
```

3. Run:
```bash
docker run -p 8000:8000 \
  -e AGENT_MAX_ITERATIONS=5 \
  -e LOG_LEVEL=INFO \
  refined-agent:latest
```

### Option 4: Kubernetes Deployment

**Use Case**: Large-scale production, high availability

**Deployment**:

1. Create `deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: refined-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: refined-agent
  template:
    metadata:
      labels:
        app: refined-agent
    spec:
      containers:
      - name: agent
        image: refined-agent:latest
        ports:
        - containerPort: 8000
        env:
        - name: AGENT_MAX_ITERATIONS
          value: "5"
        - name: LOG_LEVEL
          value: "INFO"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
---
apiVersion: v1
kind: Service
metadata:
  name: refined-agent-service
spec:
  selector:
    app: refined-agent
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

2. Deploy:
```bash
kubectl apply -f deployment.yaml
```

3. Check status:
```bash
kubectl get pods
kubectl get services
```

---

## Production Deployment Steps

### Step 1: Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Configuration reviewed
- [ ] Environment variables set
- [ ] Logging configured
- [ ] Monitoring setup
- [ ] Backup plan ready

### Step 2: Deploy to Staging

```bash
# 1. Deploy to staging environment
./deploy.sh staging

# 2. Run smoke tests
python3 test_refined_agent.py

# 3. Monitor logs
tail -f agent.log

# 4. Verify health
curl http://staging-url/health
```

### Step 3: Deploy to Production

```bash
# 1. Create backup
./backup.sh

# 2. Deploy to production
./deploy.sh production

# 3. Run health checks
./health_check.sh

# 4. Monitor metrics
./monitor.sh
```

### Step 4: Post-Deployment Verification

```bash
# 1. Check service status
systemctl status refined-agent

# 2. Test endpoints
curl http://production-url/health
curl -X POST http://production-url/agent/run -d '{"user_input": "test"}'

# 3. Monitor logs
tail -f /var/log/refined-agent/agent.log

# 4. Check metrics
curl http://production-url/metrics
```

---

## Monitoring and Maintenance

### Health Checks

```python
# health_check.py
import requests
import sys

def check_health():
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            print("✓ Service healthy")
            return 0
        else:
            print(f"✗ Service unhealthy: {response.status_code}")
            return 1
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(check_health())
```

### Logging

Monitor logs for:
- Error rates
- Response times
- Iteration counts
- Tool usage patterns

```bash
# View recent errors
grep ERROR agent.log | tail -20

# Monitor in real-time
tail -f agent.log | grep -E "(ERROR|WARNING)"

# Analyze patterns
awk '/ERROR/ {print $0}' agent.log | sort | uniq -c | sort -rn
```

### Performance Metrics

Track:
- Requests per second
- Average response time
- Success rate
- Error rate
- Resource usage (CPU, memory)

### Backup and Recovery

```bash
# Backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf backup_${DATE}.tar.gz refined_agent.py config.py

# Recovery script
#!/bin/bash
tar -xzf backup_latest.tar.gz
systemctl restart refined-agent
```

---

## Troubleshooting

### Issue: Agent Not Starting

**Symptoms**: Service fails to start

**Solutions**:
1. Check Python version: `python3 --version`
2. Verify dependencies: `pip list`
3. Check logs: `tail -f agent.log`
4. Validate configuration: `python3 -c "from config import AgentConfig; print(AgentConfig.to_dict())"`

### Issue: High Memory Usage

**Symptoms**: Memory consumption increasing

**Solutions**:
1. Reduce max_iterations
2. Clear history after each run
3. Implement caching with TTL
4. Monitor for memory leaks

```python
# Clear history periodically
if len(agent.state['history']) > 100:
    agent.state['history'] = agent.state['history'][-50:]
```

### Issue: Slow Response Times

**Symptoms**: Requests taking too long

**Solutions**:
1. Reduce max_iterations
2. Optimize tool execution
3. Enable caching
4. Add timeout limits

```python
# Add timeout
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Agent execution timeout")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(30)  # 30 second timeout

try:
    result = agent.run(input)
finally:
    signal.alarm(0)
```

### Issue: High Error Rates

**Symptoms**: Many failed requests

**Solutions**:
1. Check input validation
2. Review error logs
3. Verify tool availability
4. Test with known inputs

```bash
# Analyze error patterns
grep ERROR agent.log | awk '{print $NF}' | sort | uniq -c | sort -rn
```

### Issue: Tool Selection Errors

**Symptoms**: Wrong tools being selected

**Solutions**:
1. Review content patterns
2. Check intent keywords
3. Validate perception output
4. Test with debug logging

```python
# Enable debug logging
import logging
logging.getLogger('refined_agent').setLevel(logging.DEBUG)
```

### Issue: Docker Container Crashes

**Symptoms**: Container exits unexpectedly

**Solutions**:
1. Check container logs: `docker logs <container-id>`
2. Increase memory limits
3. Verify environment variables
4. Test locally first

```bash
# Debug container
docker run -it refined-agent:latest /bin/bash
python3 -c "from refined_agent import RefinedAgent; agent = RefinedAgent()"
```

---

## Security Best Practices

### 1. Input Validation

```python
def validate_input(user_input: str) -> bool:
    if not user_input or len(user_input) > 10000:
        return False
    # Add more validation
    return True
```

### 2. Rate Limiting

```python
from functools import wraps
from time import time

def rate_limit(max_calls, period):
    calls = []
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time()
            calls[:] = [c for c in calls if c > now - period]
            if len(calls) >= max_calls:
                raise Exception("Rate limit exceeded")
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_calls=100, period=60)
def run_agent(input):
    return agent.run(input)
```

### 3. Authentication

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != "your-secret-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return credentials.credentials

@app.post("/agent/run")
async def run_agent(request: AgentRequest, token: str = Depends(verify_token)):
    # Protected endpoint
    pass
```

---

## Scaling Strategies

### Horizontal Scaling

- Deploy multiple instances behind load balancer
- Use stateless design
- Implement distributed caching

### Vertical Scaling

- Increase CPU/memory per instance
- Optimize code performance
- Use faster storage

### Auto-Scaling

```yaml
# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: refined-agent-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: refined-agent
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## Conclusion

This deployment guide provides comprehensive instructions for deploying the Refined AI Agent in various environments. Follow the appropriate deployment option for your use case and refer to the troubleshooting section for common issues.