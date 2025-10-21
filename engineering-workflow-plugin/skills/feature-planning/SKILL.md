---
name: feature-planning
description: Break down feature requests into detailed, implementable plans with clear tasks. Use when user requests a new feature, enhancement, or complex change. Activates on phrases like "add a feature", "implement X", "build Y", "create X feature", "I need X", or "plan this feature".
---

# Feature Planning Workflow

Systematically analyze feature requests and create detailed, actionable implementation plans that can be executed by the plan-implementer agent.

## When to Use

Automatically activate when the user:
- Requests a new feature ("add user authentication", "build a dashboard")
- Asks for enhancements ("improve performance", "add export functionality")
- Describes complex changes requiring multiple steps
- Explicitly asks for planning ("plan how to implement X")
- Provides vague requirements that need clarification

## Planning Workflow

### 1. Understand Requirements

**Ask clarifying questions** to ensure complete understanding:
- What problem does this feature solve?
- Who are the users and what are their needs?
- Are there specific technical constraints?
- What does success look like?

**Explore the codebase** to understand:
- Existing architecture and patterns
- Similar features or components to reference
- Where new code should live
- What will be affected by changes

Use the Task tool with `subagent_type='Explore'` and `thoroughness='medium'` to efficiently explore the codebase.

### 2. Analyze & Design

**Identify components:**
- Database changes (models, migrations, schemas)
- Backend logic (API endpoints, business logic, services)
- Frontend changes (UI components, state management, routing)
- Testing requirements (unit tests, integration tests)
- Documentation updates

**Consider architecture:**
- Follow existing project patterns (check CLAUDE.md)
- Identify reusable components
- Plan for error handling and edge cases
- Consider performance implications
- Think about security and validation

**Check dependencies:**
- New packages or libraries needed
- Compatibility with existing stack
- Configuration changes required

### 3. Create Implementation Plan

Break down the feature into **discrete, sequential tasks** where each task:
- Has a clear objective and acceptance criteria
- Can be completed independently (or lists dependencies)
- Is small enough to implement in one focused session
- Follows the project's conventions

**Plan structure:**

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
- [What types of tests are needed]
- [Critical test cases to cover]

### Integration Points
- [How this connects with existing code]
- [Potential impacts on other features]
```

**Reference similar code:**
- Include file paths with line numbers (`src/utils/auth.py:45`)
- Point to existing patterns to follow
- Link to relevant documentation

### 4. Review Plan with User

Present the plan and confirm:
- Does this match your expectations?
- Are there any missing requirements?
- Should we adjust priorities or approach?
- Are you ready to proceed with implementation?

### 5. Execute with plan-implementer

Once the plan is approved, use the Task tool to launch the plan-implementer agent for each task:

```
I'll now implement Task 1 using the plan-implementer agent.
```

Then invoke:
```
Task tool with:
- subagent_type: 'plan-implementer'
- description: 'Implement [task name]'
- prompt: Detailed task description from the plan
```

**Execution strategy:**
- Implement tasks sequentially (respect dependencies)
- Verify each task before moving to next
- Adjust plan if issues discovered during implementation
- Let test-fixing skill handle test failures automatically
- Let git-pushing skill handle commits when user requests

## Best Practices

**Planning:**
- Start broad, then get specific
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
- Keep user informed of progress
- Adapt plan based on discoveries

## Example Workflows

### Example 1: Simple Feature

User: "Add export to CSV functionality for the user table"

1. Ask: "Should it export all users or support filtering?"
2. Explore codebase for existing export patterns
3. Create plan:
   - Task 1: Add export endpoint in `api/users.py`
   - Task 2: Create CSV formatting utility
   - Task 3: Add export button to frontend
   - Task 4: Add tests for export functionality
4. Review plan with user
5. Execute tasks using plan-implementer agent

### Example 2: Complex Feature

User: "I want to add a user authentication system"

1. Ask clarifying questions:
   - OAuth, JWT, or session-based?
   - Social login needed?
   - Password requirements?
2. Explore existing auth-related code
3. Create detailed plan with 8-12 tasks covering:
   - Database models
   - Authentication middleware
   - API endpoints (login, logout, register)
   - Frontend auth flow
   - Protected routes
   - Tests
4. Review architecture decisions with user
5. Execute incrementally with plan-implementer

### Example 3: Vague Request

User: "Make the app faster"

1. Ask specific questions:
   - What feels slow? (page load, API responses, interactions)
   - Do you have specific performance targets?
   - Are there particular pages or features to prioritize?
2. Based on answers, create focused plan
3. Might split into multiple features:
   - Database query optimization
   - Frontend bundle size reduction
   - API response caching
4. Prioritize with user
5. Execute highest priority items first

## Integration with Other Skills

**plan-implementer agent:**
- Receives detailed task specifications from this skill
- Implements each task following the plan
- Reports completion back

**test-fixing skill:**
- Automatically triggered if tests fail during implementation
- Fixes issues systematically
- Returns control to plan-implementer

**git-pushing skill:**
- Triggered when user wants to commit progress
- Creates conventional commits
- Pushes to remote

## References

For detailed planning best practices, see `references/planning-best-practices.md`.
