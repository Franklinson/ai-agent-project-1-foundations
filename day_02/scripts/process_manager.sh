#!/bin/bash
# process_manager.sh - Manage agent processes

AGENT_SCRIPT="scripts/sample_agent.py"
PID_FILE="logs/agent.pid"
LOG_FILE="logs/agent.log"

start_agent() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "Agent is already running (PID: $PID)"
            return 1
        else
            rm -f "$PID_FILE"
        fi
    fi
    
    echo "Starting agent..."
    nohup python3 "$AGENT_SCRIPT" > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    echo "Agent started (PID: $(cat $PID_FILE))"
}

stop_agent() {
    if [ ! -f "$PID_FILE" ]; then
        echo "Agent is not running (no PID file)"
        return 1
    fi
    
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "Stopping agent (PID: $PID)..."
        kill "$PID"
        rm -f "$PID_FILE"
        echo "Agent stopped"
    else
        echo "Agent process not found, cleaning up PID file"
        rm -f "$PID_FILE"
    fi
}

status_agent() {
    if [ ! -f "$PID_FILE" ]; then
        echo "Agent is not running"
        return 1
    fi
    
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        CPU=$(ps -p "$PID" -o %cpu --no-headers | tr -d ' ')
        MEM=$(ps -p "$PID" -o %mem --no-headers | tr -d ' ')
        echo "Agent is running (PID: $PID, CPU: ${CPU}%, MEM: ${MEM}%)"
        return 0
    else
        echo "Agent is not running (stale PID file)"
        rm -f "$PID_FILE"
        return 1
    fi
}

case "$1" in
    start)
        start_agent
        ;;
    stop)
        stop_agent
        ;;
    status)
        status_agent
        ;;
    restart)
        stop_agent
        sleep 2
        start_agent
        ;;
    *)
        echo "Usage: $0 {start|stop|status|restart}"
        exit 1
        ;;
esac
