from observation_system import ObservationSystem


def demo_successful_action():
    """Demo with successful action."""
    print("=== Demo 1: Successful Action ===")
    
    system = ObservationSystem()
    goal = "calculate sum of numbers"
    
    action_results = [
        {
            'success': True,
            'valid': True,
            'observation': 'Sum calculated: 15 (5+10)'
        }
    ]
    
    observation = system.observe(action_results, goal)
    
    print(f"Overall Decision: {observation['overall_decision']}")
    print(f"Total Experiences: {observation['total_experiences']}")
    
    for i, obs in enumerate(observation['observations']):
        print(f"\nObservation {i+1}:")
        print(f"  Success: {obs['evaluation']['success']}")
        print(f"  Quality Score: {obs['evaluation']['quality']['score']}")
        print(f"  Progress: {obs['evaluation']['progress']['progress']}%")
        print(f"  Decision: {obs['decision']['decision']}")
        print(f"  Reason: {obs['decision']['reason']}")
        print(f"  Lessons: {obs['reflection']['lessons']}")
    print()


def demo_failed_action():
    """Demo with failed action."""
    print("=== Demo 2: Failed Action ===")
    
    system = ObservationSystem()
    goal = "read file contents"
    
    action_results = [
        {
            'success': False,
            'valid': True,
            'observation': 'File not found error'
        }
    ]
    
    observation = system.observe(action_results, goal)
    
    print(f"Overall Decision: {observation['overall_decision']}")
    print(f"Errors: {observation['observations'][0]['evaluation']['errors']}")
    print(f"Improvements: {observation['observations'][0]['reflection']['improvements']}")
    print()


def demo_partial_progress():
    """Demo with partial progress."""
    print("=== Demo 3: Partial Progress ===")
    
    system = ObservationSystem()
    goal = "process data and generate report"
    
    action_results = [
        {
            'success': True,
            'valid': True,
            'observation': 'Data processed successfully'
        }
    ]
    
    observation = system.observe(action_results, goal)
    
    print(f"Overall Decision: {observation['overall_decision']}")
    print(f"Progress Status: {observation['observations'][0]['evaluation']['progress']['status']}")
    print(f"Decision Confidence: {observation['observations'][0]['decision']['confidence']}")
    print()


def demo_multiple_actions():
    """Demo with multiple actions."""
    print("=== Demo 4: Multiple Actions ===")
    
    system = ObservationSystem()
    goal = "complete workflow"
    
    action_results = [
        {
            'success': True,
            'valid': True,
            'observation': 'Step 1 complete workflow done'
        },
        {
            'success': True,
            'valid': True,
            'observation': 'Step 2 complete workflow finished'
        }
    ]
    
    observation = system.observe(action_results, goal)
    
    print(f"Overall Decision: {observation['overall_decision']}")
    print(f"Total Actions Observed: {len(observation['observations'])}")
    
    for i, obs in enumerate(observation['observations']):
        print(f"  Action {i+1}: {obs['decision']['decision']} - {obs['decision']['reason']}")
    print()


if __name__ == "__main__":
    demo_successful_action()
    demo_failed_action()
    demo_partial_progress()
    demo_multiple_actions()
