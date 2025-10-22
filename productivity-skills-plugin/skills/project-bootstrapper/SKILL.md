---
name: project-bootstrapper
description: Sets up new projects or improves existing projects with development best practices, tooling, documentation, and workflow automation. Use when user wants to start a new project, improve project structure, add development tooling, or establish professional workflows. Also activates when user says "set up a new project", "bootstrap this project", "add best practices", "improve project structure", or similar setup requests.
---

# Project Bootstrapper Skill

## Purpose

Sets up new projects or improves existing projects with development best practices, tooling, documentation, and workflow automation. Creates a professional, maintainable foundation for development.

## When to Use

This skill automatically activates when users want to:
- Start a new project from scratch
- Improve existing project structure
- Add missing development tooling
- Standardize project setup
- Set up CI/CD pipelines
- Create professional documentation
- Establish development workflows

**Activation phrases:**
- "set up a new project"
- "bootstrap this project"
- "add best practices"
- "improve project structure"
- "set up development tooling"
- "initialize project properly"
- "create project foundation"

## What It Does

Systematically sets up or improves a project across eight key areas:

### 1. Project Structure
- Analyzes existing structure (if any)
- Creates standard directories:
  - `src/` or language-specific source dirs
  - `tests/` or `__tests__/`
  - `docs/` for documentation
  - `scripts/` for automation
  - `.github/` for GitHub workflows (if applicable)
- Organizes files logically
- Suggests structure improvements

### 2. Git Configuration
- Creates/updates `.gitignore` with comprehensive patterns
- Sets up `.gitattributes` for line endings and diffs
- Configures git hooks (pre-commit, commit-msg, etc.)
- Adds branch protection patterns
- Sets up git LFS if needed

### 3. Documentation
- Creates comprehensive `README.md`:
  - Project description and purpose
  - Installation instructions
  - Usage examples
  - Development setup
  - Contributing guidelines
  - License information
- Adds `CONTRIBUTING.md` for collaboration
- Sets up code documentation (JSDoc, docstrings, etc.)
- Creates `CHANGELOG.md` structure
- Adds architecture documentation if complex

### 4. Testing Setup
- Identifies or suggests testing framework
- Sets up test structure and conventions
- Creates example/template tests
- Configures test runners
- Sets up coverage reporting
- Adds testing scripts/commands

### 5. Code Quality Tools
- Configures linters (ESLint, Pylint, etc.)
- Sets up code formatters (Prettier, Black, etc.)
- Adds type checking (TypeScript, mypy, etc.)
- Configures pre-commit hooks for quality
- Sets up editor configs (.editorconfig)
- Adds code quality badges

### 6. Dependencies Management
- Sets up package manager configuration
- Organizes dependencies logically
- Checks for security vulnerabilities
- Sets up dependency updates (Dependabot, Renovate)
- Creates lock files
- Documents dependency choices

### 7. Development Workflow
- Creates useful npm scripts / Makefile targets
- Sets up environment variable templates (.env.example)
- Adds Docker configuration if appropriate
- Creates development startup scripts
- Sets up hot-reload / watch modes
- Documents development workflow

### 8. CI/CD Setup
- Creates GitHub Actions / GitLab CI config
- Sets up automated testing
- Configures automated deployment (if applicable)
- Adds status badges
- Sets up release automation
- Configures branch protection

## Approach

### Discovery Phase

Before making changes, asks clarifying questions:

1. **Project type**: New or existing?
2. **Primary purpose**: Web app, library, CLI tool, etc.?
3. **Language/framework**: JavaScript/TypeScript, Python, Go, etc.?
4. **Collaboration**: Personal or team project?
5. **Deployment target**: Server, cloud, mobile, desktop?
6. **Preferences**: Specific tools or frameworks preferred?
7. **Scope**: Full setup or specific areas?

### Implementation Phase

1. **Analyze existing** structure (if existing project)
2. **Create plan** based on user answers
3. **Show plan** and get approval
4. **Implement systematically**:
   - One area at a time
   - Explain each change
   - Test as you go
5. **Verify completeness**
6. **Provide handoff** documentation

### Customization

Adapts to:
- **Language ecosystem**: Node.js vs Python vs Go vs Rust, etc.
- **Project size**: Small script vs large application
- **Team size**: Solo vs collaborative
- **Maturity**: Startup speed vs enterprise standards

## Example Interaction

```
User: "Set up this new Python project properly"

Skill:
Asks:
- Purpose? → "CLI tool for data processing"
- Deployment? → "PyPI package"
- Preferences? → "Use Poetry for deps, pytest for tests"

Implements:
1. Project structure (src/package_name, tests/, docs/)
2. Poetry configuration with pyproject.toml
3. Git setup (.gitignore for Python, pre-commit hooks)
4. README with installation and usage
5. Pytest setup with example tests
6. Black + Ruff for formatting/linting
7. GitHub Actions for CI
8. Makefile with common commands

Result: Professional, ready-to-develop project
```

## Tools Used

- **AskUserQuestion**: Gather requirements and preferences
- **Write**: Create configuration files, documentation
- **Edit**: Update existing files
- **Bash**: Initialize tools (git init, npm init, etc.)
- **Read**: Analyze existing project structure
- **Glob**: Find files to update or migrate

## Success Criteria

- All standard files present and configured
- Documentation is clear and complete
- Development workflow is documented
- Quality tooling is automated (pre-commit hooks)
- Tests can be run easily
- Project follows language/framework conventions
- New developers can onboard quickly
- No obvious best practices missing

## Templates

Maintains templates for common setups:
- **Node.js/TypeScript web app**
- **Python CLI tool**
- **Python web API (FastAPI/Flask)**
- **React/Next.js app**
- **Go service**
- **Rust CLI/library**

Uses appropriate template as starting point, customizes based on user needs.

## Integration

Works well with:
- **feature-planning**: For planning custom project features
- **code-auditor**: For validating setup quality
- **codebase-documenter**: For generating detailed docs

## Scope Control

Can do:
- **Full bootstrap**: Everything from scratch
- **Partial setup**: Specific areas only (e.g., "just add testing")
- **Improvement pass**: Enhance existing project
- **Audit + fix**: Check what's missing and add it

User can specify scope, defaults to full setup for new projects, improvement pass for existing.

## Post-Setup

After setup, provides:
- **Checklist** of what was done
- **Next steps** for starting development
- **Tips** specific to the stack
- **Commands reference** for common tasks
- **Customization guide** for adapting the setup
