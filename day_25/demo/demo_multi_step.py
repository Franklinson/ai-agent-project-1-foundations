"""
Demo: Multi-Step Prompt Builder Usage
"""

from multi_step_prompts import MultiStepPromptBuilder


def demo_basic_multi_step():
    """Demonstrate basic multi-step planning"""
    print("=" * 60)
    print("DEMO 1: Basic Multi-Step Planning")
    print("=" * 60)
    
    builder = MultiStepPromptBuilder()
    
    steps = [
        "Research target audience",
        "Define key features",
        "Create wireframes",
        "Develop prototype",
        "Gather feedback",
        "Iterate on design"
    ]
    
    prompt = builder.build_multi_step_prompt(
        goal="Design a mobile app for task management",
        steps=steps,
        planning_type="linear"
    )
    
    print(prompt)
    print("\n")


def demo_goal_decomposition():
    """Demonstrate goal decomposition"""
    print("=" * 60)
    print("DEMO 2: Goal Decomposition")
    print("=" * 60)
    
    builder = MultiStepPromptBuilder()
    
    prompt = builder.build_goal_decomposition_prompt(
        goal="Launch an e-commerce website",
        constraints=[
            "Budget: $50,000",
            "Timeline: 3 months",
            "Team: 4 developers"
        ],
        resources=[
            "Cloud hosting account",
            "Payment gateway API",
            "Product database"
        ]
    )
    
    print(prompt)
    print("\n")


def demo_hierarchical_plan():
    """Demonstrate hierarchical planning"""
    print("=" * 60)
    print("DEMO 3: Hierarchical Planning")
    print("=" * 60)
    
    builder = MultiStepPromptBuilder()
    
    subgoals = [
        {
            "name": "Backend Development",
            "tasks": [
                "Design database schema",
                "Implement REST API",
                "Add authentication",
                "Write unit tests"
            ]
        },
        {
            "name": "Frontend Development",
            "tasks": [
                "Create UI components",
                "Implement state management",
                "Connect to API",
                "Add responsive design"
            ]
        },
        {
            "name": "Deployment",
            "tasks": [
                "Set up CI/CD pipeline",
                "Configure production server",
                "Deploy application"
            ]
        }
    ]
    
    prompt = builder.build_hierarchical_plan(
        main_goal="Build a full-stack web application",
        subgoals=subgoals,
        context="Using React frontend and Node.js backend"
    )
    
    print(prompt)
    print("\n")


def demo_adaptive_planning():
    """Demonstrate adaptive planning"""
    print("=" * 60)
    print("DEMO 4: Adaptive Planning")
    print("=" * 60)
    
    builder = MultiStepPromptBuilder()
    
    initial_steps = [
        "Analyze current system performance",
        "Identify bottlenecks",
        "Implement optimization",
        "Measure improvement",
        "Deploy if successful"
    ]
    
    evaluation_criteria = [
        "Performance improves by at least 20%",
        "No new bugs introduced",
        "Memory usage stays within limits",
        "All tests pass"
    ]
    
    prompt = builder.build_adaptive_plan_prompt(
        goal="Optimize application performance",
        initial_steps=initial_steps,
        evaluation_criteria=evaluation_criteria
    )
    
    print(prompt)
    print("\n")


def demo_state_tracking():
    """Demonstrate state tracking"""
    print("=" * 60)
    print("DEMO 5: State Tracking")
    print("=" * 60)
    
    builder = MultiStepPromptBuilder()
    
    steps = [
        {"description": "Fetch user data", "status": "completed", "result": "Retrieved 1000 users"},
        {"description": "Process data", "status": "completed", "result": "Cleaned and normalized"},
        {"description": "Generate report", "status": "in progress", "result": None},
        {"description": "Send email", "status": "pending", "result": None}
    ]
    
    current_state = {
        "users_processed": 1000,
        "errors": 0,
        "current_step": 3,
        "start_time": "2024-01-15 10:00:00"
    }
    
    prompt = builder.build_state_tracking_prompt(
        goal="Generate and distribute user report",
        steps=steps,
        current_state=current_state
    )
    
    print(prompt)
    print("\n")


def demo_all_examples():
    """Show all built-in multi-step examples"""
    print("=" * 60)
    print("DEMO 6: Built-in Multi-Step Examples")
    print("=" * 60)
    
    examples = MultiStepPromptBuilder.get_multi_step_examples()
    
    # Project Setup Example
    print("\nPROJECT SETUP Example:")
    ex = examples["project_setup"]
    print(f"Goal: {ex['goal']}")
    print("\nSteps:")
    for i, step in enumerate(ex['steps'], 1):
        print(f"  {i}. {step}")
    print(f"\nState Tracking:\n{ex['state_tracking']}")
    print("-" * 60)
    
    # Data Analysis Example
    print("\nDATA ANALYSIS Example (Hierarchical):")
    ex = examples["data_analysis"]
    print(f"Goal: {ex['goal']}")
    hier = ex['hierarchical']
    print(f"\nMain Goal: {hier['main_goal']}")
    for subgoal in hier['subgoals']:
        print(f"\n  {subgoal['name']}:")
        for task in subgoal['tasks']:
            print(f"    - {task}")
    print("-" * 60)
    
    # Deployment Example
    print("\nDEPLOYMENT Example (Adaptive):")
    ex = examples["deployment"]
    print(f"Goal: {ex['goal']}")
    adapt = ex['adaptive_plan']
    print("\nInitial Steps:")
    for i, step in enumerate(adapt['initial_steps'], 1):
        print(f"  {i}. {step}")
    print("\nEvaluation Criteria:")
    for criterion in adapt['evaluation']:
        print(f"  - {criterion}")
    print(f"\nAdaptive Execution:\n{adapt['adaptive_execution']}")
    print("-" * 60)


def demo_planning_types():
    """Show all planning templates"""
    print("=" * 60)
    print("DEMO 7: Planning Templates")
    print("=" * 60)
    
    for plan_type, template in MultiStepPromptBuilder.PLANNING_TEMPLATES.items():
        print(f"\n{plan_type.upper()}:")
        print(template)
        print("-" * 60)


if __name__ == "__main__":
    demo_basic_multi_step()
    demo_goal_decomposition()
    demo_hierarchical_plan()
    demo_adaptive_planning()
    demo_state_tracking()
    demo_all_examples()
    demo_planning_types()
