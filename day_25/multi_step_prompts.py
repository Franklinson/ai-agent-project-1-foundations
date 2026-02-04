"""
Multi-Step Prompt Builder for AI Agents
Implements goal decomposition, planning, and state management
"""

from typing import List, Dict, Optional


class MultiStepPromptBuilder:
    """Builds prompts for multi-step reasoning and planning"""
    
    MULTI_STEP_INSTRUCTION = """Approach this task through multi-step planning:

1. Goal Analysis: Understand the final objective
2. Decomposition: Break goal into manageable steps
3. Sequencing: Order steps logically with dependencies
4. Execution: Complete each step systematically
5. State Tracking: Monitor progress and intermediate results
6. Verification: Ensure goal is achieved"""

    STATE_MANAGEMENT = """State Management:
- Track completion status of each step
- Store intermediate results for later steps
- Handle failures and retry logic
- Maintain context across steps
- Update state after each action"""

    PLANNING_TEMPLATES = {
        "linear": """Linear Plan:
Step 1 → Step 2 → Step 3 → Goal
Each step must complete before next begins.""",
        
        "hierarchical": """Hierarchical Plan:
Main Goal
├─ Subgoal 1
│  ├─ Task 1.1
│  └─ Task 1.2
└─ Subgoal 2
   ├─ Task 2.1
   └─ Task 2.2""",
        
        "adaptive": """Adaptive Plan:
Initial Plan → Execute → Evaluate → Adjust Plan → Continue
Plan evolves based on results and feedback."""
    }

    def __init__(self, system_role: str = "planning assistant"):
        self.system_role = system_role

    def build_multi_step_prompt(
        self,
        goal: str,
        steps: Optional[List[str]] = None,
        context: Optional[str] = None,
        planning_type: str = "linear"
    ) -> str:
        """Build prompt for multi-step task execution"""
        sections = [
            f"You are a {self.system_role}.",
            self.MULTI_STEP_INSTRUCTION
        ]
        
        if planning_type in self.PLANNING_TEMPLATES:
            sections.append(self.PLANNING_TEMPLATES[planning_type])
        
        sections.append(self.STATE_MANAGEMENT)
        
        if context:
            sections.append(f"Context:\n{context}")
        
        sections.append(f"Goal: {goal}")
        
        if steps:
            sections.append(self._format_steps(steps))
        else:
            sections.append("\nDecompose this goal into steps:")
        
        return "\n\n".join(sections)

    def build_goal_decomposition_prompt(
        self,
        goal: str,
        constraints: Optional[List[str]] = None,
        resources: Optional[List[str]] = None
    ) -> str:
        """Build prompt for decomposing complex goals"""
        sections = [
            f"You are a {self.system_role}.",
            f"Goal: {goal}",
            """
Decompose this goal using:

1. Identify Prerequisites: What must exist before starting?
2. Break Into Subgoals: What are the major milestones?
3. Define Tasks: What specific actions achieve each subgoal?
4. Identify Dependencies: Which tasks depend on others?
5. Estimate Effort: How complex is each task?
6. Create Timeline: In what order should tasks execute?"""
        ]
        
        if constraints:
            sections.append("Constraints:\n" + "\n".join(f"- {c}" for c in constraints))
        
        if resources:
            sections.append("Available Resources:\n" + "\n".join(f"- {r}" for r in resources))
        
        sections.append("\nProvide decomposition:")
        
        return "\n\n".join(sections)

    def build_hierarchical_plan(
        self,
        main_goal: str,
        subgoals: List[Dict[str, any]],
        context: Optional[str] = None
    ) -> str:
        """Build prompt for hierarchical goal planning"""
        sections = [
            f"You are a {self.system_role}.",
            f"Main Goal: {main_goal}",
            "\nHierarchical Breakdown:"
        ]
        
        for i, subgoal in enumerate(subgoals, 1):
            sections.append(f"\nSubgoal {i}: {subgoal['name']}")
            if 'tasks' in subgoal:
                for j, task in enumerate(subgoal['tasks'], 1):
                    sections.append(f"  {i}.{j}. {task}")
        
        sections.append(self.STATE_MANAGEMENT)
        
        if context:
            sections.append(f"\nContext:\n{context}")
        
        sections.append("\nExecute this plan step-by-step:")
        
        return "\n\n".join(sections)

    def build_adaptive_plan_prompt(
        self,
        goal: str,
        initial_steps: List[str],
        evaluation_criteria: List[str]
    ) -> str:
        """Build prompt for adaptive planning that adjusts based on results"""
        sections = [
            f"You are a {self.system_role}.",
            f"Goal: {goal}",
            """
Adaptive Planning Process:

1. Execute current step
2. Evaluate outcome against criteria
3. Decide: Continue, Adjust, or Retry
4. Update plan if needed
5. Proceed to next step

Be flexible and adjust the plan based on results."""
        ]
        
        sections.append("\nInitial Plan:")
        sections.append(self._format_steps(initial_steps))
        
        sections.append("\nEvaluation Criteria:")
        sections.append("\n".join(f"- {c}" for c in evaluation_criteria))
        
        sections.append("""
State Tracking Format:
- Current Step: [step number]
- Status: [not started | in progress | completed | failed]
- Result: [outcome of step]
- Next Action: [continue | adjust | retry]

Begin execution:""")
        
        return "\n\n".join(sections)

    def build_state_tracking_prompt(
        self,
        goal: str,
        steps: List[Dict[str, str]],
        current_state: Dict[str, any]
    ) -> str:
        """Build prompt with explicit state tracking"""
        sections = [
            f"You are a {self.system_role}.",
            f"Goal: {goal}",
            "\nPlan with State:"
        ]
        
        for i, step in enumerate(steps, 1):
            status = step.get('status', 'pending')
            sections.append(f"{i}. {step['description']} [{status}]")
            if step.get('result'):
                sections.append(f"   Result: {step['result']}")
        
        sections.append("\nCurrent State:")
        for key, value in current_state.items():
            sections.append(f"- {key}: {value}")
        
        sections.append("""
Next Actions:
1. Identify next incomplete step
2. Check if prerequisites are met
3. Execute the step
4. Update state with result
5. Proceed to next step

Continue execution:""")
        
        return "\n\n".join(sections)

    def _format_steps(self, steps: List[str]) -> str:
        """Format steps as numbered list"""
        return "Steps:\n" + "\n".join(f"{i}. {step}" for i, step in enumerate(steps, 1))

    @staticmethod
    def get_multi_step_examples() -> Dict[str, Dict]:
        """Return example multi-step scenarios"""
        return {
            "project_setup": {
                "goal": "Set up a new web application project",
                "steps": [
                    "Create project directory structure",
                    "Initialize version control (git)",
                    "Set up virtual environment",
                    "Install dependencies",
                    "Create configuration files",
                    "Set up database",
                    "Write initial tests",
                    "Create README documentation"
                ],
                "state_tracking": """
Step 1: Create project directory structure [completed]
  Result: Created /project with /src, /tests, /docs folders

Step 2: Initialize version control [completed]
  Result: Git repository initialized, .gitignore added

Step 3: Set up virtual environment [in progress]
  Result: Creating .venv...

Step 4: Install dependencies [pending]
Step 5: Create configuration files [pending]
..."""
            },
            
            "data_analysis": {
                "goal": "Analyze sales data and generate report",
                "hierarchical": {
                    "main_goal": "Complete sales analysis",
                    "subgoals": [
                        {
                            "name": "Data Collection",
                            "tasks": ["Fetch data from database", "Validate data quality", "Handle missing values"]
                        },
                        {
                            "name": "Analysis",
                            "tasks": ["Calculate metrics", "Identify trends", "Compare periods"]
                        },
                        {
                            "name": "Reporting",
                            "tasks": ["Create visualizations", "Write summary", "Export report"]
                        }
                    ]
                }
            },
            
            "deployment": {
                "goal": "Deploy application to production",
                "adaptive_plan": {
                    "initial_steps": [
                        "Run test suite",
                        "Build production bundle",
                        "Deploy to staging",
                        "Run smoke tests",
                        "Deploy to production",
                        "Monitor metrics"
                    ],
                    "evaluation": [
                        "All tests pass",
                        "Build completes without errors",
                        "Staging deployment successful",
                        "Smoke tests pass",
                        "No critical errors in logs"
                    ],
                    "adaptive_execution": """
Step 1: Run test suite [completed]
  Result: 2 tests failed
  Evaluation: Does not meet criteria
  Decision: Fix failing tests before proceeding
  Adjusted Plan: Add "Fix test failures" before build

Step 1b: Fix test failures [completed]
  Result: All tests now pass
  Evaluation: Meets criteria
  Decision: Continue to next step

Step 2: Build production bundle [in progress]..."""
                }
            }
        }
