---
name: solution-ensemble
description: Multi-agent solution generation with 5-dimension evaluation including security. Flags fundamental disagreements between surviving solutions.
---

# Solution Ensemble

## Purpose
Generate multiple independent solutions to a problem using parallel agents, evaluate each across 5 dimensions (correctness, performance, maintainability, security, clarity), and select the best. Flags fundamental disagreements between surviving solutions so the user can make the final call.

## When to Use

**Activation phrases:**
- "Generate multiple approaches to this problem"
- "Find the best solution for this problem"
- "What are different ways to implement this?"
- "Compare approaches for"
- "Which design pattern should I use here?"
- "Evaluate the options for"

## What It Does

1. **Problem analysis**: Understand the problem from description and context
2. **Spawn 3 parallel solution agents**: Each independently generates a solution approach
3. **5-dimension evaluation**: Each solution scored on correctness, performance, maintainability, security (10% weight), and clarity
4. **Disagreement detection**: Flags where solutions fundamentally conflict (architecture, approach, assumptions)
5. **Recommendation**: Best solution OR fundamental disagreement requiring human judgment

## Approach

### Step 1: Understand the Problem
Read context files if provided. Ask clarifying question if ambiguous. Define success criteria.

### Step 2: Parallel Solution Generation
Spawn 3 agents with compact output instructions:
```
Prompt: "Generate a solution for: [problem]. 
Keep output compact — focus on approach, key files, tradeoffs.
Include a 'Risks' section for each approach."
```

Each agent returns:
- Solution name
- Approach description (concise)
- Key implementation details
- Risks and tradeoffs

### Step 3: Evaluate Each Solution
Score each on 5 dimensions (1-10):

| Dimension | Weight | Focus |
|-----------|--------|-------|
| Correctness | 40% | Does it solve the problem? |
| Performance | 20% | Runtime, memory, scaling |
| Maintainability | 20% | Readability, modularity, testability |
| Security | 10% | Attack surface, data handling, injection vectors |
| Clarity | 10% | How easy to understand and modify |

### Step 4: Detect Disagreements
Compare solutions for:
- **Architectural conflict**: Monolith vs microservice vs event-driven
- **Implementation conflict**: Library A vs Library B
- **Assumption conflict**: "Data fits in memory" vs "must stream"
- **Strategy conflict**: Optimize now vs optimize later

Flag disagreements to the user:
```
⚠️  FUNDAMENTAL DISAGREEMENT: Solutions A and B disagree on whether data fits in memory.
A assumes < 1GB, B assumes streaming. Verify actual data size before proceeding.
```

### Step 5: Recommend
- **Consensus**: Clear winner exists → recommend with supporting scores
- **Disagreement**: Present options with tradeoff descriptions and let user decide
- **Hybrid**: Best elements from multiple solutions can be combined

## Output Format
```
═══ Solution Ensemble ═══

### Solutions Generated
1. [Name A] — [brief approach]
2. [Name B] — [brief approach]
3. [Name C] — [brief approach]

### Evaluation
| Solution | Correctness | Perf | Maint | Security | Clarity | Total |
|----------|------------|------|-------|----------|---------|-------|
| A        | 9          | 7    | 8     | 9        | 8       | 8.3   |
| B        | 8          | 9    | 7     | 6        | 7       | 7.6   |
| C        | 7          | 8    | 9     | 8        | 9       | 7.9   |

### Risks
[per-solution risk summary]

### Disagreements
[any flagged conflicts]

### Recommendation
[clear recommendation or request for human judgment]
```

## Tools Used
- **Agent**: Spawn 3 parallel solution agents and evaluation
- **Read**: Understand problem context
- **AskUserQuestion**: Clarify ambiguous requirements, resolve fundamental disagreements

## Success Criteria
- 3 independent solutions generated
- Each scored on 5 dimensions with weighted total
- Fundamental disagreements flagged to user
- Clear recommendation or clear request for human judgment
- All output compact enough to read in one screen

## Integration
Works with: plan-execute (to implement selected solution), review-apply (for peer review of chosen approach)
