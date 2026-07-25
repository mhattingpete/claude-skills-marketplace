# Prompt Diversification Strategies

This reference provides detailed guidance on generating diverse prompts that lead to genuinely different solutions.

## Strategy Selection Matrix

| Task Type | Primary Strategy | Secondary Option |
|-----------|-----------------|------------------|
| Function/Class implementation | Constraint Variation | Persona |
| API design | Approach Variation | Constraint |
| System architecture | Approach Variation | Persona |
| Algorithm selection | Constraint Variation | Approach |
| Documentation writing | Persona Variation | Constraint |
| Naming/Branding | Persona Variation | Approach |
| Refactoring | Constraint Variation | Approach |
| Test strategy | Approach Variation | Constraint |

## Constraint Variation (Technical Tasks)

Use when: Optimizing for different quality attributes.

### Template

```markdown
## Task
[Original user request]

## Optimization Focus: [SIMPLICITY / PERFORMANCE / EXTENSIBILITY]

## Guidelines
[Specific guidelines for this focus]

## Constraints
[What to prioritize and de-prioritize]

## Output
[Expected deliverable format]
```

### Simplicity Focus

**Guidelines:**
- Minimize lines of code
- Use standard library over external dependencies
- Prefer obvious implementations over clever ones
- Readable by any developer in 30 seconds

**Constraints:**
- No premature optimization
- No unnecessary abstractions
- Inline where it aids readability
- Comments only where truly needed

### Performance Focus

**Guidelines:**
- Minimize time complexity
- Reduce memory allocations
- Use efficient data structures
- Consider cache locality

**Constraints:**
- Pre-compute where possible
- Use early exits
- Avoid unnecessary copies
- Profile-guided decisions

### Extensibility Focus

**Guidelines:**
- Clean separation of concerns
- Dependency injection where appropriate
- Interface-driven design
- Easy to add new variants

**Constraints:**
- SOLID principles
- Don't repeat yourself
- Open for extension, closed for modification
- Document extension points

## Approach Variation (Architecture Tasks)

Use when: Multiple valid design philosophies exist.

### Template

```markdown
## Task
[Original user request]

## Design Approach: [TOP-DOWN / BOTTOM-UP / LATERAL]

## Methodology
[How to approach the problem]

## Starting Point
[Where to begin the design]

## Output
[Expected deliverable format]
```

### Top-Down Approach

**Methodology:**
- Start from user requirements and business goals
- Define high-level interfaces first
- Decompose into components
- Implementation details emerge from contracts

**Starting Point:**
- What does the user need to accomplish?
- What are the main use cases?
- What data flows through the system?

### Bottom-Up Approach

**Methodology:**
- Start from primitives and building blocks
- Compose small, well-tested pieces
- Let structure emerge from usage patterns
- Refactor as patterns become clear

**Starting Point:**
- What are the fundamental operations?
- What data types are involved?
- What existing utilities can we build on?

### Lateral Approach

**Methodology:**
- Draw analogies from other domains
- Challenge conventional patterns
- Look for proven solutions in adjacent fields
- Question "obvious" approaches

**Starting Point:**
- What similar problems exist elsewhere?
- What unconventional patterns might apply?
- What would a completely different industry do?

## Persona Variation (Creative Tasks)

Use when: Tone, style, or perspective matters.

### Template

```markdown
## Task
[Original user request]

## Persona: [EXPERT / PRAGMATIC / INNOVATIVE]

## Voice
[How to communicate]

## Priorities
[What this persona values]

## Output
[Expected deliverable format]
```

### Expert Persona

**Voice:**
- Technical and precise
- Authoritative but accessible
- Reference best practices and standards
- Use proper terminology

**Priorities:**
- Correctness over brevity
- Industry standards
- Comprehensive coverage
- Professional polish

### Pragmatic Persona

**Voice:**
- Direct and practical
- Focus on shipping
- Acknowledge trade-offs explicitly
- "Good enough" is valid

**Priorities:**
- Getting things done
- Clear ROI
- Maintainability
- Team velocity

### Innovative Persona

**Voice:**
- Creative and exploratory
- Challenge assumptions
- Embrace unconventional ideas
- Think differently

**Priorities:**
- Novel approaches
- User delight
- Breaking from convention when valuable
- Future possibilities

## Combining Strategies

For complex tasks, combine strategies:

**Example: "Design a caching system"**

| Solution | Primary | Secondary |
|----------|---------|-----------|
| 1 | Top-down | Simplicity |
| 2 | Bottom-up | Performance |
| 3 | Lateral | Extensibility |

This ensures diversity across both design approach AND optimization focus.

## Anti-Patterns

**Don't generate prompts that are:**
- Trivially different (just reworded)
- Focused on same trade-off space
- Likely to produce identical solutions
- Too vague to guide differentiation

**Do generate prompts that:**
- Target different quality attributes
- Use different reasoning approaches
- Would appeal to different stakeholders
- Explore different parts of solution space
