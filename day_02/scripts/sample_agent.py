#!/usr/bin/env python3
"""Sample agent for process management exercises."""
import time
import os
import sys

def main():
    agent_name = os.getenv('AGENT_NAME', 'default_agent')
    log_file = os.getenv('LOG_FILE', 'logs/agent.log')
    
    print(f"Agent {agent_name} starting...")
    print(f"Log file: {log_file}")
    
    # Simulate agent work
    for i in range(10):
        print(f"Agent working... iteration {i+1}/10")
        time.sleep(2)
    
    print("Agent completed successfully!")
    return 0

if __name__ == '__main__':
    sys.exit(main())