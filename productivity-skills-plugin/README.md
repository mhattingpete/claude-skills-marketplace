# Productivity Skills Plugin

Workflow optimization and productivity skills for Claude Code. These skills help analyze your usage patterns, audit code quality, bootstrap projects, and generate documentation.

## Skills Included

### 1. Conversation Analyzer

**Purpose:** Analyzes your Claude Code conversation history to identify patterns, common mistakes, and workflow improvement opportunities.

**Activates when you say:**
- "Analyze my conversations"
- "Review my Claude Code history"
- "How can I improve my workflow"
- "What patterns do you see in my usage"
- "Am I using Claude Code effectively"

**What it does:**
- Loads conversation history from `~/.claude/history.jsonl`
- Analyzes request patterns, project distribution, timing
- Identifies repetitive tasks that could be automated
- Detects common mistakes or inefficiencies
- Provides actionable recommendations

**Example:**
```
You: "Analyze my recent conversations and tell me how to improve"

Claude: [conversation-analyzer skill activates]
- Analyzes last 200 conversations
- Identifies that 60% are in Project X
- Notes you request same test fixes 8 times
- Recommends: Use test-fixing skill, create project-specific utilities
```

---

### 2. Code Auditor

**Purpose:** Comprehensive codebase analysis covering architecture, quality, security, performance, testing, and maintainability.

**Activates when you say:**
- "Audit the code"
- "Analyze code quality"
- "Check for issues"
- "Review the codebase"
- "Find technical debt"
- "Security audit"
- "Performance review"

**What it does:**
- Explores codebase thoroughly
- Analyzes across 6 dimensions:
  - Architecture & design patterns
  - Code quality & complexity
  - Security vulnerabilities
  - Performance bottlenecks
  - Testing coverage & quality
  - Maintainability & technical debt
- Generates detailed report with file:line references
- Prioritizes findings (Critical/High/Medium/Low)
- Provides action plan

**Example:**
```
You: "Audit the code quality and find issues"

Claude: [code-auditor skill activates]
- Finds SQL injection vulnerability in query builder
- Identifies 3 files with high complexity
- Notes 40% code duplication
- Missing tests for critical auth flow
- Generates prioritized action plan
```

---

### 3. Project Bootstrapper

**Purpose:** Sets up new projects or improves existing ones with best practices, tooling, documentation, and workflow automation.

**Activates when you say:**
- "Set up a new project"
- "Bootstrap this project"
- "Add best practices"
- "Improve project structure"
- "Set up development tooling"
- "Initialize project properly"

**What it does:**
- Asks clarifying questions about project type
- Sets up appropriate directory structure
- Configures git (gitignore, hooks, etc.)
- Creates comprehensive documentation (README, CONTRIBUTING)
- Sets up testing framework and examples
- Configures code quality tools (linters, formatters)
- Adds development workflow automation
- Sets up CI/CD if applicable

**Example:**
```
You: "Set up this new Python project properly"

Claude: [project-bootstrapper skill activates]
- Asks: Purpose? → "CLI tool for data processing"
- Asks: Preferences? → "Use Poetry, pytest"
- Implements:
  - Project structure (src/, tests/, docs/)
  - Poetry configuration
  - Git setup with hooks
  - README with docs
  - Pytest setup
  - Black + Ruff linting
  - GitHub Actions CI
  - Makefile with commands
```

---

### 4. Codebase Documenter

**Purpose:** Generates comprehensive documentation explaining codebase architecture, components, data flow, and development guidelines.

**Activates when you say:**
- "Explain this codebase"
- "Document the architecture"
- "How does this code work"
- "Create developer documentation"
- "Generate codebase overview"
- "Help me understand this project"

**What it does:**
- Explores codebase thoroughly
- Documents:
  - Project overview and purpose
  - Architecture and design patterns
  - Directory structure explanation
  - Key components and their interactions
  - External integrations (APIs, databases)
  - Data models and flow
  - Development setup instructions
  - Deployment process
  - Contributing guidelines
- Creates visual diagrams (Mermaid)
- Includes code examples from actual codebase
- Provides file:line references

**Example:**
```
You: "Explain this codebase and create documentation"

Claude: [codebase-documenter skill activates]
- Identifies Express.js REST API structure
- Maps routes → controllers → services → models
- Documents JWT auth flow
- Creates architecture diagrams
- Generates docs/:
  - ARCHITECTURE.md
  - DEVELOPMENT.md
  - API.md
  - DEPLOYMENT.md
```

---

## Installation

1. Install the marketplace plugin:
```bash
/plugin marketplace add mhattingpete/claude-skills-marketplace
```

2. The productivity-skills plugin will be available automatically

3. Skills activate automatically when you use trigger phrases

---

## Usage Tips

### Let Skills Activate Naturally

Instead of manually invoking skills, just use natural language:

**✅ Natural (Recommended):**
```
"Analyze my conversations and suggest improvements"
"Audit the code for security issues"
"Set up this Python project with best practices"
"Explain how this authentication system works"
```

**❌ Manual (Unnecessary):**
```
"/skill productivity-skills:conversation-analyzer"
```

Skills detect intent from your request and activate automatically.

### Combine Skills

Skills work great together:

1. `conversation-analyzer` → identifies you need project standards
2. `project-bootstrapper` → sets up standardized project structure
3. `code-auditor` → validates the setup quality
4. `codebase-documenter` → generates documentation

### Focus Areas

Most skills support focused analysis:

```
"Security audit only"
"Performance analysis"
"Just analyze the testing setup"
"Quick architecture overview"
```

---

## Integration with Other Skills

Works seamlessly with:

- **engineering-workflow-skills**
  - feature-planning: Plan implementations from audit findings
  - test-fixing: Fix issues identified by code-auditor
  - git-pushing: Commit improvements from bootstrapper

- **visual-documentation-skills**
  - visual-html-creator: Create visual diagrams for documentation

---

## Privacy & Local-Only

- **conversation-analyzer**: All analysis happens locally, history never leaves your machine
- **code-auditor**: Analyzes local code only
- **project-bootstrapper**: Creates files locally
- **codebase-documenter**: Documents local code only

No data is sent anywhere except standard Claude API calls for analysis.

---

## Version

**Current version:** 1.0.0

---

## Author

Created by mhattingpete based on analysis of 900+ Claude Code conversations to identify common needs and workflow optimization opportunities.

---

## Feedback & Issues

Found a bug or have a suggestion? Create an issue in the marketplace repo:
https://github.com/kuatro-group/claude-skills-marketplace/issues
