---
name: project-bootstrapper
description: Sets up new projects or improves existing projects with development best practices, tooling, documentation, and workflow automation. Use when user wants to start a new project, improve project structure, add development tooling, or establish professional workflows.
---

# Project Bootstrapper

Sets up new projects or improves existing projects with development best practices, tooling, documentation, and workflow automation.

## When to Use

- "set up a new project"
- "bootstrap this project"
- "add best practices"
- "improve project structure"
- "set up development tooling"
- "initialize project properly"

## What It Sets Up

### 1. Project Structure
- Standard directories (src/, tests/, docs/, scripts/, .github/)
- Logical file organization
- Structure improvements

### 2. Git Configuration
- Comprehensive `.gitignore`
- `.gitattributes` for line endings/diffs
- Git hooks (pre-commit, commit-msg)
- Branch protection patterns
- Git LFS if needed

### 3. Documentation
- Comprehensive `README.md`
- `CONTRIBUTING.md`
- Code documentation (JSDoc, docstrings)
- `CHANGELOG.md` structure
- Architecture docs if complex

### 4. Testing Setup
- Identify/suggest testing framework
- Test structure and conventions
- Example/template tests
- Configure test runners
- Coverage reporting
- Testing scripts/commands

### 5. Code Quality Tools
- Linters (ESLint, Pylint, etc.)
- Formatters (Prettier, Black, etc.)
- Type checking (TypeScript, mypy, etc.)
- Pre-commit hooks for quality
- Editor configs (.editorconfig)
- Code quality badges

### 6. Dependencies Management
- Package manager configuration
- Organize dependencies
- Check security vulnerabilities
- Set up dependency updates (Dependabot, Renovate)
- Create lock files
- Document dependency choices

### 7. Development Workflow
- Useful npm scripts / Makefile targets
- Environment variable templates (.env.example)
- Docker configuration if appropriate
- Development startup scripts
- Hot-reload / watch modes
- Document development workflow

### 8. CI/CD Setup
- GitHub Actions / GitLab CI config
- Automated testing
- Automated deployment (if applicable)
- Status badges
- Release automation
- Branch protection

## Approach

### Discovery Phase

Ask clarifying questions:
1. **Project type**: New or existing?
2. **Primary purpose**: Web app, library, CLI tool?
3. **Language/framework**: JS/TS, Python, Go, etc.?
4. **Collaboration**: Personal or team?
5. **Deployment target**: Server, cloud, mobile, desktop?
6. **Preferences**: Specific tools/frameworks?
7. **Scope**: Full setup or specific areas?

### Implementation Phase

1. **Analyze existing** structure (if existing project)
2. **Create plan** based on answers
3. **Show plan** and get approval
4. **Implement systematically** (one area at a time)
5. **Verify completeness**
6. **Provide handoff** documentation

## Customization

Adapts to:
- **Language ecosystem**: Node.js vs Python vs Go vs Rust
- **Project size**: Small script vs large app
- **Team size**: Solo vs collaborative
- **Maturity**: Startup speed vs enterprise standards

## Tools Used

- **AskUserQuestion**: Gather requirements
- **Write**: Create configuration files, documentation
- **Edit**: Update existing files
- **Bash**: Initialize tools (git init, npm init)
- **Read**: Analyze existing structure
- **Glob**: Find files to update

## Success Criteria

- All standard files present and configured
- Clear and complete documentation
- Documented development workflow
- Automated quality tooling (pre-commit hooks)
- Easy test execution
- Follows language/framework conventions
- Quick developer onboarding
- No obvious best practices missing

## Templates

- Node.js/TypeScript web app
- Python CLI tool
- Python web API (FastAPI/Flask)
- React/Next.js app
- Go service
- Rust CLI/library

## Integration

- **feature-planning**: For planning custom features
- **code-auditor**: For validating setup quality
- **codebase-documenter**: For generating detailed docs

## Scope Control

- **Full bootstrap**: Everything from scratch
- **Partial setup**: Specific areas only (e.g., "just add testing")
- **Improvement pass**: Enhance existing project
- **Audit + fix**: Check what's missing and add it
