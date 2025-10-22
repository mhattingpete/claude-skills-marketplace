# Productivity Skills Plugin

Workflow optimization skills for analyzing usage patterns, auditing code quality, bootstrapping projects, and generating documentation.

**Version:** 1.0.0

---

## Skills

### 1. conversation-analyzer

**Activates when you say:**
- "Analyze my conversations"
- "How can I improve my workflow"
- "Review my Claude Code history"

**What it does:**
- Analyzes conversation history from `~/.claude/history.jsonl`
- Identifies patterns, repetitive tasks, and inefficiencies
- Provides actionable recommendations

---

### 2. code-auditor

**Activates when you say:**
- "Audit the code"
- "Check for security issues"
- "Review code quality"

**What it does:**
- Comprehensive analysis across 6 dimensions: architecture, quality, security, performance, testing, maintainability
- Generates detailed report with file:line references
- Prioritizes findings and provides action plan

---

### 3. project-bootstrapper

**Activates when you say:**
- "Set up a new project"
- "Bootstrap this project"
- "Add best practices"

**What it does:**
- Sets up directory structure, git, testing, linting, CI/CD
- Creates documentation (README, CONTRIBUTING)
- Configures development workflow automation

---

### 4. codebase-documenter

**Activates when you say:**
- "Explain this codebase"
- "Document the architecture"
- "Create developer documentation"

**What it does:**
- Explores codebase and documents architecture, components, data flow
- Creates visual diagrams and includes code examples
- Generates comprehensive documentation files

---

## Installation

Add to your `.claude-plugin/marketplace.json`:

```json
{
  "plugins": [
    {
      "name": "productivity-skills-plugin",
      "source": "github:anthropics/claude-skills-marketplace/productivity-skills-plugin",
      "version": "1.0.0"
    }
  ]
}
```

---

## Integration

Works seamlessly with:
- **engineering-workflow-skills**: Plan implementations from audit findings, fix issues, commit changes
- **visual-documentation-skills**: Create visual diagrams for documentation

---

## Author

**mhattingpete**
