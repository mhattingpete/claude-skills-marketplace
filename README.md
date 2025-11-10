# Claude Skills Marketplace

A curated marketplace of Claude Code plugins for software engineering workflows.

<img src="assets/skill-loading.gif" alt="Skill Loading Demo" width="600">

## Repository Structure

```
claude-skills-marketplace/
├── .claude-plugin/
│   └── marketplace.json              # Marketplace manifest
├── execution-runtime/                 # 🚀 Code execution environment (NEW!)
│   ├── api/                           # Importable API library
│   ├── mcp-server/                    # FastMCP server
│   ├── setup.sh                       # One-command installation
│   └── README.md
├── engineering-workflow-plugin/       # Engineering workflow plugin
│   ├── .claude-plugin/
│   │   └── plugin.json               # Plugin manifest
│   ├── agents/
│   │   └── plan-implementer.md       # Plan implementation agent
│   ├── skills/
│   │   ├── feature-planning/         # Feature planning skill
│   │   ├── git-pushing/              # Git automation skill
│   │   ├── review-implementing/      # Code review skill
│   │   └── test-fixing/              # Test fixing skill
│   └── README.md
├── visual-documentation-plugin/       # Visual documentation plugin
│   ├── .claude-plugin/
│   │   └── plugin.json               # Plugin manifest
│   ├── skills/
│   │   ├── architecture-diagram-creator/  # Architecture diagram skill
│   │   ├── dashboard-creator/        # Dashboard creation skill
│   │   ├── flowchart-creator/        # Flowchart creation skill
│   │   ├── technical-doc-creator/    # Technical documentation skill
│   │   └── timeline-creator/         # Timeline creation skill
│   ├── EXAMPLES.md
│   └── README.md
├── productivity-skills-plugin/        # Productivity & optimization plugin
│   ├── .claude-plugin/
│   │   └── plugin.json               # Plugin manifest
│   ├── skills/
│   │   ├── code-auditor/             # Code auditing skill
│   │   ├── codebase-documenter/      # Codebase documentation skill
│   │   ├── conversation-analyzer/    # Usage analysis skill
│   │   └── project-bootstrapper/     # Project setup skill
│   └── README.md
├── code-operations-plugin/            # Code manipulation plugin
│   ├── .claude-plugin/
│   │   └── plugin.json               # Plugin manifest
│   ├── skills/
│   │   ├── code-execution/           # 🚀 Python execution skill (NEW!)
│   │   │   └── examples/             # Example scripts
│   │   ├── code-transfer/            # Code transfer skill
│   │   │   └── scripts/
│   │   │       └── line_insert.py    # Line-based insertion script
│   │   ├── code-refactor/            # Bulk refactoring skill
│   │   └── file-operations/          # File analysis skill
│   └── README.md
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

## 🚀 NEW: Execution Runtime (90%+ Token Savings)

The marketplace now includes a **code execution environment** implementing the [Anthropic code execution pattern](https://www.anthropic.com/engineering/code-execution-with-mcp). Instead of loading code through context, Claude executes Python locally with API access—achieving **90-99% token reduction** for bulk operations.

### Quick Benefits

✅ **Massive token savings**: Process 100 files with 1K tokens instead of 100K
✅ **Faster operations**: Local execution vs multiple API round-trips
✅ **Stateful workflows**: Resume multi-step refactoring across sessions
✅ **Auto-secure**: PII/secret masking, sandboxed execution

### Setup (2 minutes)

```bash
# After installing marketplace plugin
~/.claude/plugins/marketplaces/mhattingpete-claude-skills/execution-runtime/setup.sh
```

### When It Activates

Skills automatically use execution mode for:
- Bulk operations (10+ files)
- Complex multi-step workflows
- Iterative processing
- Codebase-wide analysis

**Example**: "Rename getUserData to fetchUserData in all Python files"
- **Without execution**: ~25,000 tokens (read/edit 50 files)
- **With execution**: ~600 tokens (script + summary) - **97.6% savings**

[Full documentation →](execution-runtime/README.md)

## Installation

### Install from Marketplace

```bash
# In Claude Code - installs the entire plugin with all skills and agents
/plugin marketplace add mhattingpete/claude-skills-marketplace
```

This installs the `engineering-workflow-plugin` which includes all skills and the plan-implementer agent.

To install individual plugins:

```bash
# Install only engineering workflows
/plugin marketplace add mhattingpete/claude-skills-marketplace/engineering-workflow-plugin

# Install only visual documentation
/plugin marketplace add mhattingpete/claude-skills-marketplace/visual-documentation-plugin

# Install only productivity skills
/plugin marketplace add mhattingpete/claude-skills-marketplace/productivity-skills-plugin

# Install only code operations
/plugin marketplace add mhattingpete/claude-skills-marketplace/code-operations-plugin
```

## Available Plugins

### Engineering Workflow Plugin

Skills for common software engineering workflows including git operations, test fixing, code review implementation, and feature planning.

[View Plugin Documentation →](engineering-workflow-plugin/README.md)

### Visual Documentation Plugin

Skills for creating stunning visual HTML documentation with modern UI design, SVG diagrams, flowcharts, dashboards, timelines, and comprehensive project architecture diagrams.

[View Plugin Documentation →](visual-documentation-plugin/README.md)

### Productivity Skills Plugin

Productivity and workflow optimization skills for analyzing usage patterns, auditing code quality, bootstrapping projects, and generating comprehensive documentation.

[View Plugin Documentation →](productivity-skills-plugin/README.md)

### Code Operations Plugin

High-precision code manipulation operations including line-based insertion, bulk refactoring, and file analysis. Converted from [code-copy-mcp](https://github.com/mhattingpete/code-copy-mcp) to native Claude Code skills.

[View Plugin Documentation →](code-operations-plugin/README.md)

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

### Code Operations

#### `code-execution` 🆕
Execute Python code locally with marketplace API access for 90%+ token savings on bulk operations.

**Activates when:** Bulk operations (10+ files), complex workflows, codebase-wide transformations, performance needs.

**Example usage:**
- "Refactor 50 files to use new API"
- "Extract all utility functions to separate files"
- "Audit code quality across entire codebase"

**Token savings:** 97-99% for bulk operations (25K → 600 tokens)

---

#### `code-transfer`
Transfer code between files with line-based precision. Auto-uses execution mode for 10+ file operations.

**Activates when:** User requests copying code between files, moving functions/classes, extracting code, or inserting at specific line numbers.

**Example usage:**
- "Copy the authenticate function from auth.py to utils.py"
- "Move this class to a separate file"
- "Extract this function to a new file"
- "Insert this code at line 45"

**Key feature:** Includes Python script for precise line-number-based insertion where Edit tool's string matching isn't suitable.

---

#### `code-refactor`
Perform bulk code refactoring operations. Auto-switches to execution mode for 10+ files (90% token savings).

**Activates when:** User requests renaming identifiers, replacing deprecated patterns, updating API calls, or making consistent changes across multiple locations.

**Example usage:**
- "Rename getUserData to fetchUserData everywhere"
- "Replace all var declarations with let or const"
- "Update all authentication API calls to use the new endpoint"
- "Convert callbacks to async/await"

---

#### `file-operations`
Analyze files and get detailed metadata without modifying them.

**Activates when:** User requests file information, statistics, or analysis without making changes.

**Example usage:**
- "Analyze this file"
- "How many lines in app.py?"
- "Compare the sizes of all Python files"
- "Give me code quality metrics for the project"

---

### Productivity & Analysis

#### `conversation-analyzer`
Analyze Claude Code conversation history to identify patterns, common mistakes, and workflow optimization opportunities.

**Activates when:** User wants to understand usage patterns, optimize workflow, or check best practices.

**Example usage:**
- "Analyze my conversations"
- "Review my history"
- "How can I improve my workflow"

---

#### `code-auditor`
Comprehensive codebase analysis covering architecture, code quality, security, performance, testing, and maintainability.

**Activates when:** User wants to audit code quality, identify technical debt, find security issues, or assess test coverage.

**Example usage:**
- "Audit the code"
- "Check for issues"
- "Review the codebase"
- "Security audit"

---

#### `codebase-documenter`
Generate comprehensive documentation explaining how a codebase works, including architecture, key components, data flow, and development guidelines.

**Activates when:** User wants to understand unfamiliar code, create onboarding docs, document architecture, or explain how the system works.

**Example usage:**
- "Explain this codebase"
- "Document the architecture"
- "How does this code work"
- "Create developer documentation"

---

#### `project-bootstrapper`
Set up new projects or improve existing projects with development best practices, tooling, documentation, and workflow automation.

**Activates when:** User wants to start a new project, improve project structure, add development tooling, or establish professional workflows.

**Example usage:**
- "Set up a new project"
- "Bootstrap this project"
- "Add best practices"
- "Improve project structure"

---

### Visual Documentation

#### `architecture-diagram-creator`
Create comprehensive HTML architecture diagrams covering business objectives, data flows, processing pipelines, features (functional and non-functional), system architecture, and deployment information.

**Activates when:** User requests architecture diagrams, system overviews, project documentation, or high-level system design.

**Example usage:**
- "Create an architecture diagram for this project"
- "Generate a project architecture overview"
- "Document the system architecture with data flows and processing pipeline"

---

#### `flowchart-creator`
Create stunning HTML flowcharts and process flow diagrams with decision trees, color-coded stages, and swimlanes.

**Activates when:** User requests flowcharts, process diagrams, workflow visualizations, or decision trees.

**Example usage:**
- "Create a flowchart for our order processing"
- "Generate a process flow diagram showing deployment steps"
- "Make a decision tree for our approval workflow"

---

#### `dashboard-creator`
Create professional HTML dashboards with KPI metric cards, bar/pie/line charts, and progress indicators.

**Activates when:** User requests dashboards, metrics displays, KPI visualizations, or data charts.

**Example usage:**
- "Create a dashboard showing website analytics"
- "Make a KPI dashboard for our sales metrics"
- "Generate a performance dashboard with charts"

---

#### `technical-doc-creator`
Create comprehensive HTML technical documentation with code blocks, API workflows, and system architecture diagrams.

**Activates when:** User requests technical documentation, API docs, code examples, or system architecture.

**Example usage:**
- "Create API documentation for our user endpoints"
- "Generate technical docs for our authentication system"
- "Document our microservices architecture"

---

#### `timeline-creator`
Create beautiful HTML timelines and project roadmaps with Gantt charts, milestones, and phase groupings.

**Activates when:** User requests timelines, roadmaps, Gantt charts, project schedules, or milestone visualizations.

**Example usage:**
- "Create a timeline for our product launch"
- "Generate a roadmap showing Q1-Q4 milestones"
- "Make a Gantt chart for our project schedule"

**Common Features (All Skills):**
- Modern gradient backgrounds and responsive design
- Semantic color system (success/warning/error/info)
- Self-contained HTML (no external dependencies)
- WCAG AA accessibility compliance

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
