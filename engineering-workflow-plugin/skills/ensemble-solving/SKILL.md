---
name: ensemble-solving
description: Generate multiple diverse solutions in parallel and select the best. Use for architecture decisions, code generation with multiple valid approaches, or creative tasks where exploring alternatives improves quality.
---

# Ensemble Problem Solving

Generate multiple solutions in parallel by spawning 3 subagents with different approaches, then evaluate and select the best result.

## When to Use

**Activation phrases:**
- "Give me options for..."
- "What's the best way to..."
- "Explore different approaches..."
- "I want to see alternatives..."
- "Compare approaches for..."
- "Which approach should I use..."

**Good candidates:**
- Architecture decisions with trade-offs
- Code generation with multiple valid implementations
- API design with different philosophies
- Naming, branding, documentation style
- Refactoring strategies
- Algorithm selection

**Skip ensemble for:**
- Simple lookups or syntax questions
- Single-cause bug fixes
- File operations, git commands
- Deterministic configuration changes
- Tasks with one obvious solution

## What It Does

1. **Analyzes the task** to determine if ensemble approach is valuable
2. **Generates 3 distinct prompts** using appropriate diversification strategy
3. **Spawns 3 parallel subagents** to develop solutions independently
4. **Evaluates all solutions** using weighted criteria
5. **Returns the best solution** with explanation and alternatives summary

## Approach

### Step 1: Classify Task Type

Determine which category fits:
- **Code Generation**: Functions, classes, APIs, algorithms
- **Architecture/Design**: System design, data models, patterns
- **Creative**: Writing, naming, documentation

### Step 2: Invoke Ensemble Orchestrator

```
Task tool with:
- subagent_type: 'ensemble-orchestrator'
- description: 'Generate and evaluate 3 parallel solutions'
- prompt: [User's original task with full context]
```

The orchestrator handles:
- Prompt diversification
- Parallel execution
- Solution evaluation
- Winner selection

### Step 3: Present Result

The orchestrator returns:
- The winning solution (in full)
- Evaluation scores for all 3 approaches
- Why the winner was selected
- When alternatives might be preferred

## Diversification Strategies

**For Code (Constraint Variation):**
| Approach | Focus |
|----------|-------|
| Simplicity | Minimal code, maximum readability |
| Performance | Efficient, optimized |
| Extensibility | Clean abstractions, easy to extend |

**For Architecture (Approach Variation):**
| Approach | Focus |
|----------|-------|
| Top-down | Requirements → Interfaces → Implementation |
| Bottom-up | Primitives → Composition → Structure |
| Lateral | Analogies from other domains |

**For Creative (Persona Variation):**
| Approach | Focus |
|----------|-------|
| Expert | Technical precision, authoritative |
| Pragmatic | Ship-focused, practical |
| Innovative | Creative, unconventional |

## Evaluation Rubric

| Criterion | Base Weight | Description |
|-----------|-------------|-------------|
| Correctness | 30% | Solves the problem correctly |
| Completeness | 20% | Addresses all requirements |
| Quality | 20% | How well-crafted |
| Clarity | 15% | How understandable |
| Elegance | 15% | How simple/beautiful |

Weights adjust based on task type.

## Example

**User:** "What's the best way to implement a rate limiter?"

**Skill:**
1. Classifies as Code Generation
2. Invokes ensemble-orchestrator
3. Three approaches generated:
   - Simple: Token bucket with in-memory counter
   - Performance: Sliding window with atomic operations
   - Extensible: Strategy pattern with pluggable backends
4. Evaluation selects extensible approach (score 8.4)
5. Returns full implementation with explanation

**Output:**
```
## Selected Solution

[Full rate limiter implementation with strategy pattern]

## Why This Solution Won

The extensible approach scored highest (8.4) because it provides
a clean abstraction that works for both simple use cases and
complex distributed scenarios. The strategy pattern allows
swapping Redis/Memcached backends without code changes.

## Alternatives

- **Simple approach**: Best if you just need basic in-memory
  limiting and will never scale beyond one process.

- **Performance approach**: Best for high-throughput scenarios
  where every microsecond matters.
```

## Success Criteria

- 3 genuinely different solutions generated
- Clear evaluation rationale provided
- Winner selected with confidence
- Alternatives summarized with use cases
- User understands trade-offs

## Token Cost

~4x overhead vs single attempt. Worth it for:
- High-stakes architecture decisions
- Creative work where first attempt rarely optimal
- Learning scenarios where seeing alternatives is valuable
- Code that will be maintained long-term

## Integration

- **feature-planning**: Can ensemble architecture decisions
- **code-auditor**: Can ensemble analysis perspectives
- **plan-implementer**: Executes the winning approach
