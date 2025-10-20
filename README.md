# Claude Skills Marketplace

A curated marketplace of Claude Code plugins for software engineering workflows.

<img src="assets/skill-loading.gif" alt="Skill Loading Demo" width="600">

## Repository Structure

```
claude-skills-marketplace/
├── .claude-plugin/
│   └── marketplace.json              # Marketplace manifest
├── engineering-workflow-plugin/       # Engineering workflow plugin
│   ├── .claude-plugin/
│   │   └── plugin.json               # Plugin manifest
│   ├── agents/
│   │   └── plan-implementer/         # Plan implementation agent
│   ├── skills/
│   │   ├── feature-planning/         # Feature planning skill
│   │   ├── git-pushing/              # Git automation skill
│   │   ├── review-implementing/      # Code review skill
│   │   └── test-fixing/              # Test fixing skill
│   ├── CHANGELOG.md
│   ├── CONTRIBUTING.md
│   └── SETUP.md
├── LICENSE
└── README.md
```

## What are Skills and Agents?

**Skills** are model-invoked capabilities that extend Claude Code's functionality. Unlike slash commands that require explicit user activation, Skills are automatically triggered by Claude based on context and the Skill's description.

Each Skill consists of a `SKILL.md` file with:
- YAML frontmatter (name, description, metadata)
- Detailed instructions for Claude
- Optional supporting files (scripts, templates, references)

**Agents** are specialized Claude instances that can be invoked by Claude to handle specific types of work. They run independently with their own context and can use different models optimized for their task.

Each Agent consists of an `AGENT.md` file with:
- YAML frontmatter (name, description, model selection)
- Specialized instructions and constraints
- Decision-making frameworks for their domain

Skills and Agents work together: Skills can orchestrate when to invoke Agents, and Agents can use Skills while executing their tasks.

## Installation

### Install from Marketplace

```bash
# In Claude Code - installs the entire plugin with all skills and agents
/plugin marketplace add mhattingpete/claude-skills-marketplace
```

This installs the `engineering-workflow-plugin` which includes all skills and the plan-implementer agent.

## Available Skills

### Feature Development

#### `feature-planning`
Break down feature requests into detailed, implementable plans with clear tasks that can be executed by the plan-implementer agent.

**Activates when:** User requests a new feature, enhancement, or complex change requiring planning.

**Example usage:**
- "Add user authentication"
- "Build a dashboard for analytics"
- "Plan how to implement export functionality"

**Works with:** `plan-implementer` agent for execution

---

### Git & Version Control

#### `git-pushing`
Automatically stage, commit with conventional commit messages, and push changes to remote.

**Activates when:** User mentions pushing changes, committing work, or saving to remote.

**Example usage:**
- "Push these changes"
- "Commit and push to github"
- "Let's save this work"

---

### Testing & Quality

#### `test-fixing`
Systematically identify and fix failing tests using smart error grouping strategies.

**Activates when:** User reports test failures, asks to fix tests, or wants test suite passing.

**Example usage:**
- "Fix the failing tests"
- "Make the test suite green"
- "Tests are broken after my refactor"

---

### Code Review

#### `review-implementing`
Process and implement code review feedback systematically with todo tracking.

**Activates when:** User provides reviewer comments, PR feedback, or asks to address review notes.

**Example usage:**
- "Implement this review feedback: [paste comments]"
- "Address these PR comments"
- "The reviewer suggested these changes"

---

## Available Agents

### Implementation

#### `plan-implementer`
Focused agent for implementing code based on specific plans or task descriptions. Uses Haiku model for efficient, cost-effective execution.

**Use when:** You have a clear specification or plan to execute.

**Invoked by:** `feature-planning` skill automatically, or manually via Task tool

**Example usage:**
- Implementing tasks from a feature plan
- Executing specific implementation subtasks
- Following project conventions for focused code changes

**Model:** claude-3-5-haiku (fast and efficient for implementation tasks)

---

## Plugin Development

Want to add your own plugin to this marketplace? Follow this structure:

```
your-plugin/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── agents/                       # Optional: Agent definitions
├── skills/                       # Skills directory
└── README.md                    # Plugin documentation
```

Then add it to `.claude-plugin/marketplace.json` in this repository.

## Creating Custom Skills

Want to create your own Skills? Follow this structure:

```
my-skill/
├── SKILL.md          # Main skill file with frontmatter and instructions
└── reference.md      # Optional: Additional context loaded on-demand
```

### SKILL.md Template

```yaml
---
name: my-skill-name
description: What it does and when to use it. Be specific about activation triggers.
---

# Skill Title

Brief overview of what this skill does.

## When to Use

List specific scenarios when Claude should activate this skill:
- User says X
- User mentions Y
- Context includes Z

## Instructions

Step-by-step instructions for Claude to follow...
```

### Best Practices

1. **Description is key**: Include both what the skill does AND when to use it
2. **Use gerund forms**: Name skills with "-ing" (e.g., "git-pushing", not "git-push")
3. **Keep concise**: Skills under 500 lines load faster
4. **Progressive disclosure**: Move detailed content to separate reference files
5. **Test across models**: Verify skills work with Sonnet, Opus, and Haiku

## Contributing

Contributions are welcome! To add a new skill:

1. Fork this repository
2. Create your skill in a new directory
3. Follow the SKILL.md template and best practices
4. Add your skill to this README
5. Submit a pull request

## License

Apache 2.0 - See LICENSE file for details.

## Resources

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/skills)
- [Official Anthropic Skills](https://github.com/anthropics/skills)
- [Agent Skills Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices.md)

## Support

Issues and questions:
- Open an issue on this repository
- Check [Claude Code discussions](https://github.com/anthropics/claude-code/discussions)

---

## Complete Workflow Example

Here's how the skills and agent work together for a typical feature development flow:

1. **User**: "Add user authentication to the app"
2. **`feature-planning` skill** activates and:
   - Asks clarifying questions (OAuth? JWT? Session-based?)
   - Explores codebase for existing patterns
   - Creates detailed plan with 8 discrete tasks
   - Reviews plan with user
3. **`plan-implementer` agent** executes each task:
   - Implements User model
   - Creates auth middleware
   - Adds login/logout endpoints
   - Builds frontend auth flow
4. **`test-fixing` skill** automatically activates if tests fail:
   - Identifies and groups test failures
   - Fixes issues systematically
5. **User**: "Push these changes"
6. **`git-pushing` skill** activates:
   - Creates conventional commit message
   - Pushes to remote branch

---

**Note**: These skills are generalized for broad software engineering use. Adapt descriptions and instructions to fit your specific workflows.
