# Day 02: Terminal Mastery and Automation

## Overview

Day 2 focuses on terminal mastery and automation for AI agent development. This includes creating helper scripts, process management, log analysis, and building a foundation for production-ready agent operations.

## Agent Helper Script

The `scripts/agent_helper.sh` is a comprehensive terminal-based tool for managing AI agent development workflows. It provides a unified interface for common development tasks.

### What the Agent Helper Script Does

- **Project Management**: Initialize and maintain project structure
- **Process Control**: Start, stop, restart, and monitor agent processes
- **Log Management**: View, follow, and search through agent logs
- **System Monitoring**: Check agent status, resource usage, and statistics
- **Maintenance**: Clean up old files and manage disk space
- **Development Support**: Streamline common development workflows

## Commands Reference

### Project Setup
```bash
./scripts/agent_helper.sh init
```
Creates the required directory structure and placeholder files.

### Process Management
```bash
# Start the agent
./scripts/agent_helper.sh start

# Stop the agent
./scripts/agent_helper.sh stop

# Restart the agent
./scripts/agent_helper.sh restart

# Check agent status
./scripts/agent_helper.sh status
```

### Log Management
```bash
# View last 50 lines of logs (default)
./scripts/agent_helper.sh logs

# View specific number of log lines
./scripts/agent_helper.sh logs 100

# Follow logs in real-time
./scripts/agent_helper.sh follow

# Search logs for specific terms
./scripts/agent_helper.sh search "ERROR"
./scripts/agent_helper.sh search "timeout"
```

### Maintenance
```bash
# Clean up old files (>7 days)
./scripts/agent_helper.sh cleanup

# Show agent statistics
./scripts/agent_helper.sh stats

# Show help
./scripts/agent_helper.sh help
```

## Common Workflows

### 1. Initial Setup
```bash
# Initialize project structure
./scripts/agent_helper.sh init

# Start the agent
./scripts/agent_helper.sh start

# Check if it's running
./scripts/agent_helper.sh status
```

### 2. Development Cycle
```bash
# Make code changes to sample_agent.py
# Restart agent to apply changes
./scripts/agent_helper.sh restart

# Monitor logs for issues
./scripts/agent_helper.sh follow
```

### 3. Debugging Issues
```bash
# Check agent status
./scripts/agent_helper.sh status

# Search for errors
./scripts/agent_helper.sh search "ERROR"

# View recent logs
./scripts/agent_helper.sh logs 200

# Follow logs in real-time
./scripts/agent_helper.sh follow
```

### 4. Maintenance Tasks
```bash
# Check system statistics
./scripts/agent_helper.sh stats

# Clean up old files
./scripts/agent_helper.sh cleanup

# Stop agent when done
./scripts/agent_helper.sh stop
```

## Troubleshooting Tips

### Agent Won't Start
1. **Check if already running**: `./scripts/agent_helper.sh status`
2. **Check Python script exists**: Ensure `scripts/sample_agent.py` exists
3. **Check permissions**: `chmod +x scripts/agent_helper.sh`
4. **View logs**: `./scripts/agent_helper.sh logs` for error messages

### Agent Stops Unexpectedly
1. **Check logs**: `./scripts/agent_helper.sh search "ERROR"`
2. **Monitor resources**: `./scripts/agent_helper.sh status` for CPU/memory usage
3. **Check disk space**: `df -h` to ensure sufficient space
4. **Review recent changes**: Check if code changes caused issues

### Permission Errors
```bash
# Fix script permissions
chmod +x scripts/agent_helper.sh
chmod +x scripts/*.sh

# Fix directory permissions
chmod 755 logs outputs configs
```

### Log File Issues
```bash
# If log file is missing or corrupted
touch logs/agent.log
chmod 644 logs/agent.log

# If logs are too large
./scripts/agent_helper.sh cleanup
```

### Process Management Issues
```bash
# If PID file is stale
rm -f logs/agent.pid
./scripts/agent_helper.sh start

# If process won't stop
./scripts/agent_helper.sh stop
# If still running, manually kill:
ps aux | grep sample_agent.py
kill -9 <PID>
```

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Agent is already running" | Process already started | Use `status` to check, `stop` then `start` |
| "Agent process not found" | Process died unexpectedly | Check logs, restart agent |
| "Log file not found" | Missing log file | Run `init` or create manually |
| "Permission denied" | Script not executable | Run `chmod +x scripts/agent_helper.sh` |

## Directory Structure

```
day_02/
├── README.md                 # This file
├── terminal_exercises.md     # Terminal exercise documentation
├── scripts/
│   ├── agent_helper.sh      # Main helper script
│   ├── sample_agent.py      # Sample Python agent
│   ├── process_manager.sh   # Process management utilities
│   ├── setup_env.sh         # Environment setup
│   └── monitor_agent.sh     # Agent monitoring
├── logs/
│   ├── agent.log           # Main agent log file
│   └── agent.pid           # Process ID file
├── outputs/
│   └── agent_data.txt      # Agent output data
└── configs/
    ├── sample_config.json  # Configuration file
    └── backup_config.json  # Backup configuration
```

## Environment Variables

The helper script uses these environment variables (set by `setup_env.sh`):

- `AGENT_NAME`: Name of the agent instance
- `AGENT_ENV`: Environment (development/production)
- `LOG_FILE`: Path to the log file
- `PYTHONPATH`: Python module search path

## Best Practices

1. **Always check status** before starting/stopping agents
2. **Monitor logs regularly** during development
3. **Clean up old files** periodically to save disk space
4. **Use meaningful search terms** when debugging
5. **Follow logs in real-time** during testing
6. **Keep backups** of important configuration files

## Next Steps

- Explore advanced terminal commands in `terminal_exercises.md`
- Customize the agent helper script for your specific needs
- Set up automated monitoring and alerting
- Integrate with CI/CD pipelines for production deployment