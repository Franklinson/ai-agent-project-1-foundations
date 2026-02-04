"""
Error Recovery Prompt Builder for AI Agents
Implements error detection, handling, and recovery strategies
"""

from typing import List, Dict, Optional


class ErrorRecoveryPromptBuilder:
    """Builds prompts with error handling and recovery guidance"""
    
    ERROR_RECOVERY_INSTRUCTION = """Error Handling Protocol:

1. Detect: Identify when an error occurs
2. Classify: Determine error type and severity
3. Analyze: Understand the root cause
4. Recover: Apply appropriate recovery strategy
5. Retry: Attempt the operation again if applicable
6. Fallback: Use alternative approach if recovery fails
7. Report: Communicate error and resolution"""

    ERROR_TYPES = {
        "validation": "Input data is invalid or malformed",
        "network": "Connection or API communication failure",
        "timeout": "Operation exceeded time limit",
        "permission": "Insufficient access rights",
        "not_found": "Resource does not exist",
        "rate_limit": "Too many requests",
        "server_error": "External service failure",
        "data_error": "Data processing or transformation failure"
    }

    RECOVERY_STRATEGIES = {
        "retry": """Retry Strategy:
- Wait with exponential backoff
- Maximum retry attempts: 3
- Retry only for transient errors""",
        
        "fallback": """Fallback Strategy:
- Use alternative tool or method
- Provide degraded functionality
- Use cached or default data""",
        
        "skip": """Skip Strategy:
- Mark step as failed
- Continue with remaining steps
- Log error for later review""",
        
        "abort": """Abort Strategy:
- Stop execution immediately
- Rollback changes if possible
- Report critical failure"""
    }

    def __init__(self, system_role: str = "error-aware assistant"):
        self.system_role = system_role

    def build_error_aware_prompt(
        self,
        task: str,
        tools: Optional[List[Dict[str, str]]] = None,
        context: Optional[str] = None,
        error_handling: str = "retry"
    ) -> str:
        """Build prompt with error handling guidance"""
        sections = [
            f"You are a {self.system_role}.",
            self.ERROR_RECOVERY_INSTRUCTION
        ]
        
        if tools:
            sections.append(self._format_tools_with_errors(tools))
        
        sections.append("Common Error Types:")
        for error_type, description in self.ERROR_TYPES.items():
            sections.append(f"- {error_type}: {description}")
        
        if error_handling in self.RECOVERY_STRATEGIES:
            sections.append(self.RECOVERY_STRATEGIES[error_handling])
        
        if context:
            sections.append(f"\nContext:\n{context}")
        
        sections.append(f"\nTask: {task}")
        sections.append("\nExecute with error handling:")
        
        return "\n\n".join(sections)

    def build_retry_prompt(
        self,
        task: str,
        failed_step: str,
        error_message: str,
        retry_count: int = 0,
        max_retries: int = 3
    ) -> str:
        """Build prompt for retry scenarios"""
        sections = [
            f"You are a {self.system_role}.",
            f"Task: {task}",
            f"\nFailed Step: {failed_step}",
            f"Error: {error_message}",
            f"Retry Attempt: {retry_count + 1}/{max_retries}",
            """
Retry Protocol:
1. Analyze the error message
2. Determine if error is transient
3. Adjust parameters if needed
4. Wait before retrying (exponential backoff)
5. Attempt operation again
6. If max retries reached, use fallback strategy

Retry now:"""
        ]
        
        return "\n\n".join(sections)

    def build_fallback_prompt(
        self,
        task: str,
        failed_approach: str,
        alternative_approaches: List[str]
    ) -> str:
        """Build prompt for fallback strategies"""
        sections = [
            f"You are a {self.system_role}.",
            f"Task: {task}",
            f"\nFailed Approach: {failed_approach}",
            "\nAlternative Approaches:"
        ]
        
        for i, approach in enumerate(alternative_approaches, 1):
            sections.append(f"{i}. {approach}")
        
        sections.append("""
Fallback Protocol:
1. Select most appropriate alternative
2. Explain why this alternative should work
3. Execute alternative approach
4. Verify result meets requirements

Proceed with fallback:""")
        
        return "\n\n".join(sections)

    def build_error_classification_prompt(
        self,
        error_message: str,
        context: Optional[str] = None
    ) -> str:
        """Build prompt for classifying errors"""
        sections = [
            f"You are a {self.system_role}.",
            f"Error Message: {error_message}",
            """
Classify this error:

1. Error Type: [validation | network | timeout | permission | not_found | rate_limit | server_error | data_error]
2. Severity: [low | medium | high | critical]
3. Is Transient: [yes | no]
4. Can Retry: [yes | no]
5. Root Cause: [brief explanation]
6. Recommended Action: [retry | fallback | skip | abort]

Provide classification:"""
        ]
        
        if context:
            sections.insert(2, f"Context: {context}")
        
        return "\n\n".join(sections)

    def build_multi_error_prompt(
        self,
        task: str,
        steps: List[Dict[str, str]],
        error_policies: Dict[str, str]
    ) -> str:
        """Build prompt for handling multiple potential errors"""
        sections = [
            f"You are a {self.system_role}.",
            f"Task: {task}",
            "\nSteps with Error Policies:"
        ]
        
        for i, step in enumerate(steps, 1):
            policy = error_policies.get(step['name'], 'retry')
            sections.append(f"{i}. {step['description']}")
            sections.append(f"   Error Policy: {policy}")
            if 'potential_errors' in step:
                sections.append(f"   Potential Errors: {', '.join(step['potential_errors'])}")
        
        sections.append("""
Execution Guidelines:
- Execute each step carefully
- Monitor for errors at each step
- Apply designated error policy when errors occur
- Log all errors and recovery actions
- Continue to next step after successful recovery

Begin execution:""")
        
        return "\n\n".join(sections)

    def _format_tools_with_errors(self, tools: List[Dict[str, str]]) -> str:
        """Format tools with potential errors"""
        tool_list = "Available Tools:\n"
        for tool in tools:
            tool_list += f"- {tool['name']}: {tool['description']}\n"
            if 'errors' in tool:
                tool_list += f"  Possible Errors: {', '.join(tool['errors'])}\n"
        return tool_list

    @staticmethod
    def get_error_examples() -> Dict[str, Dict]:
        """Return example error scenarios and recovery"""
        return {
            "api_timeout": {
                "task": "Fetch user data from API",
                "error": "Request timeout after 30 seconds",
                "classification": {
                    "type": "timeout",
                    "severity": "medium",
                    "transient": True,
                    "can_retry": True
                },
                "recovery": """
Attempt 1: Failed with timeout
→ Wait 2 seconds (exponential backoff)
→ Retry with increased timeout (60s)

Attempt 2: Success
→ Retrieved user data
→ Continue with task""",
                "strategy": "retry"
            },
            
            "invalid_input": {
                "task": "Process user registration",
                "error": "Email format is invalid",
                "classification": {
                    "type": "validation",
                    "severity": "low",
                    "transient": False,
                    "can_retry": False
                },
                "recovery": """
Error: Invalid email format
→ Cannot retry (validation error)
→ Request corrected input from user
→ Validate new input
→ Proceed if valid""",
                "strategy": "request_correction"
            },
            
            "service_unavailable": {
                "task": "Send email notification",
                "error": "Email service returned 503 Service Unavailable",
                "classification": {
                    "type": "server_error",
                    "severity": "high",
                    "transient": True,
                    "can_retry": True
                },
                "recovery": """
Attempt 1: Failed (503 error)
→ Wait 5 seconds
→ Retry

Attempt 2: Failed (503 error)
→ Wait 10 seconds
→ Retry

Attempt 3: Failed (503 error)
→ Max retries reached
→ Fallback: Queue email for later delivery
→ Log error and continue""",
                "strategy": "retry_then_fallback"
            },
            
            "rate_limit": {
                "task": "Fetch data from external API",
                "error": "429 Too Many Requests - Rate limit exceeded",
                "classification": {
                    "type": "rate_limit",
                    "severity": "medium",
                    "transient": True,
                    "can_retry": True
                },
                "recovery": """
Error: Rate limit exceeded
→ Extract retry-after header: 60 seconds
→ Wait 60 seconds
→ Retry request
→ Success""",
                "strategy": "wait_and_retry"
            },
            
            "data_corruption": {
                "task": "Process uploaded file",
                "error": "File is corrupted or unreadable",
                "classification": {
                    "type": "data_error",
                    "severity": "high",
                    "transient": False,
                    "can_retry": False
                },
                "recovery": """
Error: Corrupted file
→ Cannot process
→ Notify user of corruption
→ Request file re-upload
→ Abort current processing""",
                "strategy": "abort_and_notify"
            }
        }
