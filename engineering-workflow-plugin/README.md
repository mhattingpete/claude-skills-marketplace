# Engineering Workflow Skills

Automate common software engineering workflows including feature planning, testing, git operations, and code review implementation.

**Version:** 1.1.0

---

## Skills

### 1. feature-planning

**Activates when you say:**
- "Add user authentication"
- "Build a dashboard"
- "Implement X feature"
- "Plan how to do X"

**What it does:**
- Asks clarifying questions about requirements
- Explores codebase for existing patterns
- Creates detailed implementation plan
- Hands off to plan-implementer agent for execution

---

### 2. test-fixing

**Activates when you say:**
- "Fix the tests"
- "Tests are failing"
- "Make the test suite green"

**What it does:**
- Runs test suite to identify failures
- Groups errors by type/cause
- Fixes issues systematically
- Verifies all tests pass

---

### 3. git-pushing

**Activates when you say:**
- "Push these changes"
- "Commit and push"
- "Create a PR"

**What it does:**
- Stages all changes
- Generates conventional commit message
- Pushes to remote
- Creates pull request (if requested)

---

### 4. review-implementing

**Activates when you say:**
- "Implement this review feedback"
- "Address these comments"
- "Apply review suggestions"

**What it does:**
- Parses reviewer feedback
- Creates todo list for each item
- Implements changes systematically
- Verifies all feedback addressed

---

## Agent

### plan-implementer

Focused agent for implementing code from detailed plans. Uses Haiku model for cost-effective execution.

**Used by:** feature-planning skill
**Purpose:** Execute discrete implementation tasks with strict scope adherence

---

## Workflow Example

```
User: "Add user authentication"
  ↓
feature-planning → creates plan, asks questions
  ↓
plan-implementer → implements each task
  ↓
test-fixing → fixes any test failures
  ↓
git-pushing → commits and pushes changes
```

---

## Installation

Add to your `.claude-plugin/marketplace.json`:

```json
{
  "plugins": [
    {
      "name": "engineering-workflow-skills",
      "source": "github:anthropics/claude-skills-marketplace/engineering-workflow-plugin",
      "version": "1.1.0"
    }
  ]
}
```

---

## Author

**mhattingpete**
