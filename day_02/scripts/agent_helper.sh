#!/bin/bash
# agent_helper.sh - Comprehensive agent development helper

set -e  # Exit on error (with exceptions)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DAY_DIR="$PROJECT_ROOT/day_02"

AGENT_SCRIPT="$DAY_DIR/scripts/sample_agent.py"
PID_FILE="$DAY_DIR/logs/agent.pid"
LOG_FILE="$DAY_DIR/logs/agent.log"
CONFIG_DIR="$DAY_DIR/configs"
OUTPUT_DIR="$DAY_DIR/outputs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function: Initialize project structure
init_project() {
    log_info "Initializing project structure..."
    mkdir -p "$DAY_DIR"/{scripts,logs,outputs,configs}
    touch "$DAY_DIR"/logs/.gitkeep "$DAY_DIR"/outputs/.gitkeep
    log_success "Project structure created"
}

# Function: Start agent
start_agent() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            log_warning "Agent is already running (PID: $PID)"
            return 1
        else
            rm -f "$PID_FILE"
        fi
    fi
    
    log_info "Starting agent..."
    cd "$DAY_DIR"
    nohup python3 "$AGENT_SCRIPT" > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    log_success "Agent started (PID: $(cat $PID_FILE))"
}

# Function: Stop agent
stop_agent() {
    if [ ! -f "$PID_FILE" ]; then
        log_warning "Agent is not running (no PID file)"
        return 1
    fi
    
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        log_info "Stopping agent (PID: $PID)..."
        kill "$PID" || true
        sleep 1
        if ps -p "$PID" > /dev/null 2>&1; then
            log_warning "Agent didn't stop gracefully, forcing..."
            kill -9 "$PID" || true
        fi
        rm -f "$PID_FILE"
        log_success "Agent stopped"
    else
        log_warning "Agent process not found, cleaning up PID file"
        rm -f "$PID_FILE"
    fi
}

# Function: Check agent status
status_agent() {
    if [ ! -f "$PID_FILE" ]; then
        log_warning "Agent is not running"
        return 1
    fi
    
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        CPU=$(ps -p "$PID" -o %cpu --no-headers | tr -d ' ')
        MEM=$(ps -p "$PID" -o %mem --no-headers | tr -d ' ')
        log_success "Agent is running"
        echo "  PID: $PID"
        echo "  CPU: ${CPU}%"
        echo "  MEM: ${MEM}%"
        return 0
    else
        log_warning "Agent is not running (stale PID file)"
        rm -f "$PID_FILE"
        return 1
    fi
}

# Function: View agent logs
view_logs() {
    if [ ! -f "$LOG_FILE" ]; then
        log_error "Log file not found: $LOG_FILE"
        return 1
    fi
    
    local lines=${1:-50}
    log_info "Showing last $lines lines of agent log:"
    echo "---"
    tail -n "$lines" "$LOG_FILE"
}

# Function: Follow logs in real-time
follow_logs() {
    if [ ! -f "$LOG_FILE" ]; then
        log_error "Log file not found: $LOG_FILE"
        return 1
    fi
    
    log_info "Following agent logs (Ctrl+C to stop)..."
    tail -f "$LOG_FILE"
}

# Function: Search logs
search_logs() {
    if [ ! -f "$LOG_FILE" ]; then
        log_error "Log file not found: $LOG_FILE"
        return 1
    fi
    
    local pattern=${1:-"ERROR"}
    log_info "Searching logs for: $pattern"
    echo "---"
    grep -i "$pattern" "$LOG_FILE" | tail -20
}

# Function: Clean up old files
cleanup() {
    log_info "Cleaning up old files..."
    
    # Remove old log files (older than 7 days)
    find "$DAY_DIR/logs" -name "*.log" -mtime +7 -delete 2>/dev/null || true
    
    # Remove old output files
    find "$DAY_DIR/outputs" -name "*.txt" -mtime +7 -delete 2>/dev/null || true
    
    log_success "Cleanup completed"
}

# Function: Show statistics
show_stats() {
    log_info "Agent Statistics:"
    echo "---"
    
    if [ -f "$LOG_FILE" ]; then
        echo "Log file size: $(du -h "$LOG_FILE" | cut -f1)"
        echo "Total log lines: $(wc -l < "$LOG_FILE")"
        echo "Error count: $(grep -ic "error" "$LOG_FILE" || echo "0")"
        echo "Warning count: $(grep -ic "warning" "$LOG_FILE" || echo "0")"
    else
        echo "No log file found"
    fi
    
    echo "Output files: $(find "$OUTPUT_DIR" -type f 2>/dev/null | wc -l)"
    echo "Config files: $(find "$CONFIG_DIR" -type f 2>/dev/null | wc -l)"
}

# Function: Show help
show_help() {
    cat << EOF
Agent Helper - Terminal-based agent development tool

Usage: $0 <command> [options]

Commands:
    init            Initialize project structure
    start           Start the agent
    stop            Stop the agent
    restart         Restart the agent
    status          Show agent status
    logs [N]        View last N lines of logs (default: 50)
    follow          Follow logs in real-time
    search <term>   Search logs for term (default: ERROR)
    cleanup         Clean up old log and output files
    stats           Show agent statistics
    help            Show this help message

Examples:
    $0 init
    $0 start
    $0 status
    $0 logs 100
    $0 search "timeout"
    $0 cleanup

EOF
}

# Main command dispatcher
case "${1:-help}" in
    init)
        init_project
        ;;
    start)
        start_agent
        ;;
    stop)
        stop_agent
        ;;
    restart)
        stop_agent
        sleep 2
        start_agent
        ;;
    status)
        status_agent
        ;;
    logs)
        view_logs "${2:-50}"
        ;;
    follow)
        follow_logs
        ;;
    search)
        search_logs "${2:-ERROR}"
        ;;
    cleanup)
        cleanup
        ;;
    stats)
        show_stats
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        log_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
