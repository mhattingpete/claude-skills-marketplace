---
name: feature-planning
description: Break down feature requests into detailed, implementable plans with clear tasks. Use when user requests a new feature, enhancement, or complex change.
---

# Feature Planning

Systematically analyze feature requests and create detailed, actionable implementation plans.

## When to Use

- Requests new feature ("add user authentication", "build dashboard")
- Asks for enhancements ("improve performance", "add export")
- Describes complex multi-step changes
- Explicitly asks for planning ("plan how to implement X")
- Provides vague requirements needing clarification

## Planning Workflow

### 1. Understand Requirements

**Ask clarifying questions:**
- What problem does this solve?
- Who are the users?
- Specific technical constraints?
- What does success look like?

**Explore the codebase:**
Use Task tool with `subagent_type='Explore'` and `thoroughness='medium'` to understand:
- Existing architecture and patterns
- Similar features to reference
- Where new code should live
- What will be affected

### 2. Analyze & Design

**Identify components:**
- Database changes (models, migrations, schemas)
- Backend logic (API endpoints, business logic, services)
- Frontend changes (UI, state, routing)
- Testing requirements
- Documentation updates

**Consider architecture:**
- Follow existing patterns (check CLAUDE.md)
- Identify reusable components
- Plan error handling and edge cases
- Consider performance implications
- Think about security and validation

**Check dependencies:**
- New packages/libraries needed
- Compatibility with existing stack
- Configuration changes required

### 3. Create Implementation Plan

Break feature into **discrete, sequential tasks**:

```markdown
## Feature: [Feature Name]

### Overview
[Brief description of what will be built and why]

### Architecture Decisions
- [Key decision 1 and rationale]
- [Key decision 2 and rationale]

### Implementation Tasks

#### Task 1: [Component Name]
- **File**: `path/to/file.py:123`
- **Description**: [What needs to be done]
- **Details**:
  - [Specific requirement 1]
  - [Specific requirement 2]
- **Dependencies**: None (or list task numbers)

#### Task 2: [Component Name]
...

### Testing Strategy
- [What types of tests needed]
- [Critical test cases to cover]

### Integration Points
- [How this connects with existing code]
- [Potential impacts on other features]
```

**Include specific references:**
- File paths with line numbers (`src/utils/auth.py:45`)
- Existing patterns to follow
- Relevant documentation

### 4. Review Plan with User

Confirm:
- Does this match expectations?
- Missing requirements?
- Adjust priorities or approach?
- Ready to proceed?

### 5. Execute with plan-implementer

Launch plan-implementer agent for each task:

```
Task tool with:
- subagent_type: 'plan-implementer'
- description: 'Implement [task name]'
- prompt: Detailed task description from plan
```

**Execution strategy:**
- Implement sequentially (respect dependencies)
- Verify each task before next
- Adjust plan if issues discovered
- Let test-fixing skill handle failures
- Let git-pushing skill handle commits

## Best Practices

**Planning:**
- Start broad, then specific
- Reference existing code patterns
- Include file paths and line numbers
- Think through edge cases upfront
- Keep tasks focused and atomic

**Communication:**
- Explain architectural decisions
- Highlight trade-offs and alternatives
- Be explicit about assumptions
- Provide context for future maintainers

**Execution:**
- Implement one task at a time
- Verify before moving forward
- Keep user informed
- Adapt based on discoveries

## Integration

- **plan-implementer agent**: Receives task specs, implements
- **test-fixing skill**: Auto-triggered on test failures
- **git-pushing skill**: Triggered for commits
