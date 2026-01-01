#!/bin/bash
# monitor_agent.sh - Monitor agent process

PID_FILE="logs/agent.pid"
CHECK_INTERVAL=5
MAX_CHECKS=12

check_count=0

while [ $check_count -lt $MAX_CHECKS ]; do
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            CPU=$(ps -p "$PID" -o %cpu --no-headers | tr -d ' ')
            MEM=$(ps -p "$PID" -o %mem --no-headers | tr -d ' ')
            echo "[$(date '+%H:%M:%S')] Agent running (CPU: ${CPU}%, MEM: ${MEM}%)"
        else
            echo "[$(date '+%H:%M:%S')] Agent process not found"
            break
        fi
    else
        echo "[$(date '+%H:%M:%S')] Agent not running (no PID file)"
        break
    fi
    
    check_count=$((check_count + 1))
    sleep $CHECK_INTERVAL
done
