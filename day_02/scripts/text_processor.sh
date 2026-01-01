#!/bin/bash
# text_processor.sh - Demonstrates text processing

LOG_FILE="logs/agent.log"

echo "=== Error Summary ==="
grep -c "ERROR" "$LOG_FILE"

echo -e "\n=== Recent Errors ==="
grep "ERROR" "$LOG_FILE" | tail -5

echo -e "\n=== Log Level Distribution ==="
grep -oE "(INFO|ERROR|WARNING|DEBUG)" "$LOG_FILE" | sort | uniq -c | sort -rn