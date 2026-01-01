#!/bin/bash
# setup_env.sh - Set up environment for agent development

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Set environment variables
export AGENT_NAME="day2_agent"
export AGENT_ENV="development"
export LOG_FILE="$PROJECT_ROOT/day_02/logs/agent.log"
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Create necessary directories
mkdir -p "$PROJECT_ROOT/day_02/logs"
mkdir -p "$PROJECT_ROOT/day_02/outputs"

echo "Environment set up:"
echo "  AGENT_NAME: $AGENT_NAME"
echo "  AGENT_ENV: $AGENT_ENV"
echo "  LOG_FILE: $LOG_FILE"
echo "  PYTHONPATH: $PYTHONPATH"
