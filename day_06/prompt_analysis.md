# Prompt Comparison Analysis

## Test Results

| Approach | Accuracy Score |
|----------|----------------|
| direct   | 0.67          |
| role     | 0.67          |
| options  | 0.33          |
| examples | 0.33          |

## Analysis

**Best Approach:** `direct` 
**Performance Gap:** 0.33

## Findings

- Simple direct prompts performed best (0.67 accuracy)
- Role-based prompts matched direct performance 
- Explicit options and examples underperformed (0.33 accuracy)
- Performance gap of 0.33 between best and worst approaches

## Recommendation

Use `direct` approach: "Classify sentiment: {text}" for highest accuracy in sentiment classification tasks.

## Key Insights

- Simplicity outperforms complexity in this test case
- Adding examples or explicit options reduced performance
- Direct instructions are most effective for clear classification tasks