# Evaluation Rubrics

Detailed scoring criteria for evaluating ensemble solutions.

## Base Rubric

| Criterion | Weight | Score 9-10 | Score 7-8 | Score 5-6 | Score 3-4 | Score 1-2 |
|-----------|--------|------------|-----------|-----------|-----------|-----------|
| **Correctness** | 30% | Flawless, handles all cases | Works correctly, minor edge cases | Mostly correct, some issues | Significant bugs | Fundamentally broken |
| **Completeness** | 20% | All requirements, extras | All requirements met | Most requirements | Missing key features | Incomplete |
| **Quality** | 20% | Production-ready, polished | High quality, minor polish | Acceptable, needs work | Rough, needs rework | Unusable |
| **Clarity** | 15% | Crystal clear, self-documenting | Clear, easy to follow | Understandable with effort | Confusing | Incomprehensible |
| **Elegance** | 15% | Beautiful, minimal | Clean and simple | Adequate | Over-complicated | Mess |

## Task-Specific Adjustments

### Code Generation Rubric

| Criterion | Adjusted Weight |
|-----------|-----------------|
| Correctness | 35% |
| Completeness | 20% |
| Quality | 15% |
| Clarity | 10% |
| Elegance | 10% |
| **Testability** | 10% |

**Testability scoring:**
- 9-10: Easy to test, clear inputs/outputs, no side effects
- 7-8: Testable with minor setup
- 5-6: Testable but requires mocking/stubs
- 3-4: Difficult to test in isolation
- 1-2: Untestable without major refactoring

### Architecture/Design Rubric

| Criterion | Adjusted Weight |
|-----------|-----------------|
| Correctness | 25% |
| Completeness | 25% |
| Quality | 15% |
| Clarity | 10% |
| Elegance | 15% |
| **Flexibility** | 10% |

**Flexibility scoring:**
- 9-10: Easily adapts to changing requirements
- 7-8: Can accommodate most changes
- 5-6: Some flexibility, some rigidity
- 3-4: Requires significant rework for changes
- 1-2: Locked-in, impossible to modify

### Creative Tasks Rubric

| Criterion | Adjusted Weight |
|-----------|-----------------|
| Correctness | 20% |
| Completeness | 20% |
| Quality | 15% |
| Clarity | 10% |
| Elegance | 25% |
| **Originality** | 10% |

**Originality scoring:**
- 9-10: Fresh perspective, memorable
- 7-8: Interesting take, stands out
- 5-6: Competent but conventional
- 3-4: Generic, forgettable
- 1-2: Cliched, uninspired

## Evaluation Process

### Step 1: Score Each Solution

For each criterion, assess the solution on a 1-10 scale:

```
Solution 1: [Approach Name]
- Correctness: X/10
- Completeness: X/10
- Quality: X/10
- Clarity: X/10
- Elegance: X/10
- [Task-specific]: X/10
```

### Step 2: Calculate Weighted Scores

```
Total = Sum(score × weight) for each criterion
```

Example calculation (Code Generation):
```
Correctness: 8 × 0.35 = 2.80
Completeness: 7 × 0.20 = 1.40
Quality: 8 × 0.15 = 1.20
Clarity: 9 × 0.10 = 0.90
Elegance: 7 × 0.10 = 0.70
Testability: 8 × 0.10 = 0.80
Total: 7.80
```

### Step 3: Compare and Select

1. Identify highest scoring solution
2. Check margin of victory:
   - > 0.5 points: Clear winner
   - 0.2-0.5 points: Winner with caveats
   - < 0.2 points: Tie, consider synthesis

### Step 4: Consider Synthesis

If solutions are close, check if combining elements improves result:
- Can we take the core from Solution A and the error handling from Solution B?
- Does Solution C have a unique insight we can incorporate?

Only synthesize if the combination is clearly better than any individual solution.

## Scoring Calibration

### What "Correctness" Means By Task Type

**Code:**
- Compiles/runs without errors
- Produces expected output
- Handles edge cases
- No security vulnerabilities

**Architecture:**
- Meets functional requirements
- Satisfies non-functional requirements
- Components interact correctly
- Data flows as expected

**Creative:**
- Addresses the brief
- Appropriate for audience
- Achieves intended effect
- Factually accurate (if applicable)

### What "Elegance" Means By Task Type

**Code:**
- Minimal lines for the job
- Clear flow, no convoluted logic
- Good abstractions (not too many, not too few)
- Idiomatic for the language

**Architecture:**
- Simple components, clear responsibilities
- Minimal coupling between parts
- Obvious how pieces fit together
- No unnecessary complexity

**Creative:**
- Concise yet complete
- Well-structured
- Flows naturally
- Aesthetically pleasing

## Edge Cases

### When to Override Scores

**Dealbreakers** (score 0 for entire solution):
- Security vulnerability
- Data corruption risk
- Violates explicit requirements
- Fundamentally misunderstands problem

**Bonuses** (add up to +0.5):
- Exceptional insight
- Solves adjacent problems
- Educational value
- Particularly maintainable

### Handling Ties

If two solutions are within 0.2 points:

1. **Prefer simpler** if equivalent quality
2. **Prefer more testable** if code
3. **Prefer more flexible** if architecture
4. **Prefer more original** if creative
5. **Ask user** if still tied

## Output Template

```markdown
## Evaluation Results

### Scores

| Criterion | Weight | Sol 1 | Sol 2 | Sol 3 |
|-----------|--------|-------|-------|-------|
| Correctness | 35% | 8 | 7 | 9 |
| Completeness | 20% | 7 | 8 | 8 |
| Quality | 15% | 8 | 7 | 8 |
| Clarity | 10% | 9 | 6 | 7 |
| Elegance | 10% | 7 | 5 | 8 |
| Testability | 10% | 8 | 6 | 9 |
| **Weighted Total** | | **7.80** | **6.85** | **8.35** |

### Winner: Solution 3

**Margin**: +0.55 over Solution 1 (clear winner)

**Key differentiators**:
- Higher correctness (handles all edge cases)
- Better testability (pure functions, no side effects)
- More elegant abstraction

**When alternatives might be preferred**:
- Solution 1: If simplicity is paramount
- Solution 2: If you need maximum performance (benchmark first)
```
