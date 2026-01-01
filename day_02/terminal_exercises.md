# Terminal Exercises - Day 02

# Terminal Navigation and File Operations

This document contains terminal exercises for Day 2 of the AI Agent Project, focusing on directory structure creation and file operations.

## Exercise 1: Create Project Structure

### Command:
```bash
mkdir -p day_02/{scripts,logs,outputs,configs}
```

### Description:
Creates the main day_02 directory with subdirectories for scripts, logs, outputs, and configs.

## Exercise 2: Navigate to Project Directory

### Command:
```bash
cd day_02
```

### Description:
Changes to the day_02 directory to work within the project structure.

## Exercise 3: Create Placeholder Files

### Command:
```bash
touch scripts/.gitkeep logs/.gitkeep outputs/.gitkeep configs/.gitkeep
```

### Description:
Creates .gitkeep files in each subdirectory to ensure they are tracked by Git even when empty.

## Exercise 4: Create Documentation Files

### Command:
```bash
touch README.md terminal_exercises.md
```

### Description:
Creates README.md and terminal_exercises.md files in the day_02 directory.

## Exercise 5: Create Configuration File

### Command:
```bash
cat > configs/sample_config.json << 'EOF'
{
  "agent_name": "sample_agent",
  "environment": "development",
  "log_level": "INFO"
}
EOF
```

### Description:
Creates a sample JSON configuration file using heredoc syntax.

## Exercise 6: Copy Configuration File

### Command:
```bash
cp configs/sample_config.json configs/backup_config.json
```

### Description:
Creates a backup copy of the configuration file.

## Exercise 7: Create Test Output

### Command:
```bash
echo "Test content" > outputs/test.txt
```

### Description:
Creates a test file with sample content in the outputs directory.

## Exercise 8: Read File Content

### Command:
```bash
cat outputs/test.txt
```

### Output:
```
Test content
```

### Description:
Displays the content of the test file to verify it was created correctly.

## Exercise 9: List Directory Contents

### Command:
```bash
ls -lah scripts
```

### Output:
```
total 0
drwxr-xr-x@ 3 admin  staff    96B Jan  1 12:51 .
drwxr-xr-x@ 8 admin  staff   256B Jan  1 12:52 ..
-rw-r--r--@ 1 admin  staff     0B Jan  1 12:51 .gitkeep
```

### Description:
Shows detailed listing of the scripts directory, confirming the .gitkeep file was created successfully.

# Text Processing and Search

## Exercise 10: Create Agent Log File

### Command:
```bash
cat > logs/agent.log << 'EOF'
2024-01-15 10:00:00 INFO Agent started successfully
2024-01-15 10:00:05 DEBUG Processing user request
2024-01-15 10:00:10 INFO API call to OpenAI completed
2024-01-15 10:00:15 WARNING Rate limit approaching
2024-01-15 10:00:20 ERROR API request failed: timeout
2024-01-15 10:00:25 INFO Retrying API request
2024-01-15 10:00:30 INFO API call successful
2024-01-15 10:00:35 DEBUG Response processed
2024-01-15 10:00:40 ERROR Database connection failed
2024-01-15 10:00:45 INFO Agent completed task
EOF
```

### Description:
Creates a sample agent log file with various log levels for testing text processing commands.

## Exercise 11: Create Agent Data File

### Command:
```bash
cat > outputs/agent_data.txt << 'EOF'
agent1,success,2.5,100
agent2,error,0.0,0
agent3,success,1.8,95
agent4,timeout,0.0,0
agent5,success,3.2,150
EOF
```

### Description:
Creates a CSV file with agent performance data for processing exercises.

## Exercise 12: Search for Errors

### Command:
```bash
grep "ERROR" logs/agent.log
```

### Output:
```
2024-01-15 10:00:20 ERROR API request failed: timeout
2024-01-15 10:00:40 ERROR Database connection failed
```

### Description:
Searches for lines containing "ERROR" in the log file.

## Exercise 13: Case-Insensitive Pattern Search

### Command:
```bash
grep -iE "info|error" logs/agent.log
```

### Output:
```
2024-01-15 10:00:00 INFO Agent started successfully
2024-01-15 10:00:10 INFO API call to OpenAI completed
2024-01-15 10:00:20 ERROR API request failed: timeout
2024-01-15 10:00:25 INFO Retrying API request
2024-01-15 10:00:30 INFO API call successful
2024-01-15 10:00:40 ERROR Database connection failed
2024-01-15 10:00:45 INFO Agent completed task
```

### Description:
Searches for lines containing either "info" or "error" (case-insensitive) using extended regex.

## Exercise 14: Count Pattern Matches

### Command:
```bash
grep -c "ERROR" logs/agent.log
```

### Output:
```
2
```

### Description:
Counts the number of lines containing "ERROR" in the log file.

## Exercise 15: Show Line Numbers

### Command:
```bash
grep -n "ERROR" logs/agent.log
```

### Output:
```
5:2024-01-15 10:00:20 ERROR API request failed: timeout
9:2024-01-15 10:00:40 ERROR Database connection failed
```

### Description:
Shows line numbers along with matching lines containing "ERROR".

## Exercise 16: Text Substitution

### Command:
```bash
sed 's/ERROR/CRITICAL/g' logs/agent.log > logs/agent_modified.log
```

### Description:
Replaces all occurrences of "ERROR" with "CRITICAL" and saves to a new file.

## Exercise 17: Delete Lines with Pattern

### Command:
```bash
sed '/DEBUG/d' logs/agent.log > logs/agent_no_debug.log
```

### Description:
Removes all lines containing "DEBUG" and saves to a new file.

## Exercise 18: Extract First Column

### Command:
```bash
awk -F',' '{print $1}' outputs/agent_data.txt
```

### Output:
```
agent1
agent2
agent3
agent4
agent5
```

### Description:
Extracts the first column (agent names) from the CSV file using comma as delimiter.

## Exercise 19: Filter and Format Data

### Command:
```bash
awk -F',' '$2=="success" {print $1, $3, $4}' outputs/agent_data.txt
```

### Output:
```
agent1 2.5 100
agent3 1.8 95
agent5 3.2 150
```

### Description:
Filters rows where status is "success" and prints agent name, response time, and requests.

## Exercise 20: Calculate Average

### Command:
```bash
awk -F',' '{sum+=$3; count++} END {print "Average:", sum/count}' outputs/agent_data.txt
```

### Output:
```
Average: 1.5
```

### Description:
Calculates the average response time from the third column of the CSV file.

## Exercise 21: Create Executable Script

### Command:
```bash
touch scripts/text_processor.sh
chmod +x scripts/text_processor.sh
```

### Description:
Creates a new shell script file and makes it executable.

## Exercise 22: Execute Script

### Command:
```bash
./scripts/text_processor.sh
```

### Output:
```
=== Error Summary ===
2

=== Recent Errors ===
2024-01-15 10:00:20 ERROR API request failed: timeout
2024-01-15 10:00:40 ERROR Database connection failed

=== Log Level Distribution ===
   5 INFO
   2 ERROR
   2 DEBUG
   1 WARNING
```

### Description:
Executes the text processing script that analyzes the agent log file and provides a summary of errors and log level distribution.

# Process Management and Scripting

## Exercise 23: Create Python Agent Script

### Command:
```bash
touch scripts/sample_agent.py
chmod +x scripts/sample_agent.py
```

### Description:
Creates a Python script file for the sample agent and makes it executable.

## Exercise 24: Create Process Manager Script

### Command:
```bash
touch scripts/process_manager.sh
chmod _x scripts/process_manager.sh
```

### Output:
```
chmod: Invalid file mode: _x
```

### Command (Corrected):
```bash
chmod +x scripts/process_manager.sh
```

### Description:
Creates a process manager script. Shows common typo error with chmod and the correction.

## Exercise 25: Start Agent Process

### Command:
```bash
./scripts/process_manager.sh start
```

### Output:
```
Starting agent...
Agent started (PID: 80804)
```

### Description:
Starts the agent process using the process manager script and displays the process ID.

## Exercise 26: Check Agent Status

### Command:
```bash
./scripts/process_manager.sh status
```

### Output:
```
ps: illegal option -- -
usage: ps [-AaCcEefhjlMmrSTvwXx] [-O fmt | -o fmt] [-G gid[,gid...]]
          [-g grp[,grp...]] [-u [uid,uid...]]
          [-p pid[,pid...]] [-t tty[,tty...]] [-U user[,user...]]
       ps [-L]
ps: illegal option -- -
usage: ps [-AaCcEefhjlMmrSTvwXx] [-O fmt | -o fmt] [-G gid[,gid...]]
          [-g grp[,grp...]] [-u [uid,uid...]]
          [-p pid[,pid...]] [-t tty[,tty...]] [-U user[,user...]]
       ps [-L]
Agent is running (PID: 80804, CPU: %, MEM: %)
```

### Description:
Checks the status of the agent process. Shows ps command errors due to incorrect options but still reports agent status.

## Exercise 27: Wait and Stop Process

### Command:
```bash
sleep 5
./scripts/process_manager.sh stop
```

### Output:
```
Agent process not found, cleaning up PID file
```

### Description:
Waits 5 seconds then attempts to stop the agent process. Process had already terminated.

## Exercise 28: Verify Process Stopped

### Command:
```bash
./scripts/process_manager.sh status
```

### Output:
```
Agent is not running
```

### Description:
Confirms that the agent process is no longer running.

## Exercise 29: Create Additional Scripts

### Command:
```bash
touch scripts/setup_env.sh
touch scripts/monitor_agent.sh
```

### Description:
Creates environment setup and monitoring scripts for the agent system.

## Exercise 30: Source Environment Setup

### Command:
```bash
source scripts/setup_env.sh
```

### Output:
```
Environment set up:
  AGENT_NAME: day2_agent
  AGENT_ENV: development
  LOG_FILE: /Users/admin/Desktop/Bozoma/ai-agent-project-1-foundations/day_02/logs/agent.log
  PYTHONPATH: /Users/admin/Desktop/Bozoma/ai-agent-project-1-foundations:
```

### Description:
Sources the environment setup script to configure agent environment variables.

## Exercise 31: Start Agent Again

### Command:
```bash
./scripts/process_manager.sh start
```

### Output:
```
Starting agent...
Agent started (PID: 84730)
```

### Description:
Starts the agent process again with a new process ID.

## Exercise 32: Run Monitor Script

### Command:
```bash
./scripts/monitor_agent.sh
```

### Output:
```
zsh: permission denied: ./scripts/monitor_agent.sh
```

### Command (Fix Permissions):
```bash
chmod +x scripts/monitor_agent.sh
./scripts/monitor_agent.sh
```

### Output:
```
[13:26:48] Agent process not found
```

### Description:
Attempts to run the monitoring script, encounters permission error, fixes it, then runs successfully.

## Exercise 33: Final Cleanup

### Command:
```bash
./scripts/process_manager.sh stop
```

### Output:
```
Agent process not found, cleaning up PID file
```

### Description:
Performs final cleanup by stopping any remaining agent processes.
