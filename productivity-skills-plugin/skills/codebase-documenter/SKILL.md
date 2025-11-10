---
name: codebase-documenter
description: Generates comprehensive documentation explaining how a codebase works, including architecture, key components, data flow, and development guidelines. Use when user wants to understand unfamiliar code, create onboarding docs, document architecture, or explain how the system works.
---

# Codebase Documenter

Generates comprehensive documentation for codebases - architecture, components, data flow, development guidelines.

## When to Use

- "explain this codebase"
- "document the architecture"
- "how does this code work"
- "create developer documentation"
- "generate codebase overview"
- "create onboarding docs"

## What It Documents

### 1. Project Overview
- Purpose & vision
- Target users
- Key features
- Technology stack
- Project status

### 2. Architecture
- High-level structure
- Design patterns
- Data flow
- Control flow
- Diagrams (Mermaid)
- Architectural decisions

### 3. Directory Structure
- Organization purpose
- Naming conventions
- Entry points
- Core modules
- Configuration locations

### 4. Key Components
- Major modules
- Classes & functions
- Responsibilities
- Interactions
- Extension points
- Code examples

### 5. External Integrations
- APIs consumed
- Databases & schemas
- Authentication
- Caching
- Message queues
- File storage

### 6. Data Models
- Database schema
- Data structures
- Validation
- Migrations
- Data transformations

### 7. Development Setup
- Prerequisites
- Installation steps
- Configuration
- Running the app
- Testing
- Debugging
- Troubleshooting

### 8. Development Guidelines
- Coding conventions
- Testing approach
- Error handling
- Logging
- Security practices
- Performance patterns

### 9. Deployment
- Build process
- Deployment steps
- Environments
- Monitoring
- Rollback procedures

### 10. Contributing
- Development workflow
- Code review guidelines
- Testing requirements
- Documentation updates

## Approach

1. **Explore** using Explore agent (thorough)
2. **Map structure** with Glob
3. **Read critical files** (README, entry points, core modules)
4. **Identify patterns** with Grep (imports, exports)
5. **Trace execution** paths
6. **Extract knowledge** from docs, comments, tests
7. **Synthesize** into cohesive documentation

## Output

Creates markdown documentation:
```
docs/
├── README.md              # Overview and quick start
├── ARCHITECTURE.md        # System architecture
├── DEVELOPMENT.md         # Development guide
├── API.md                 # API documentation
├── DEPLOYMENT.md          # Deployment guide
└── CONTRIBUTING.md        # Contribution guidelines
```

Or single comprehensive doc if preferred.

## Depth Levels

- **Quick**: High-level overview (15-30 min)
- **Standard**: Comprehensive coverage (30-60 min)
- **Deep**: Exhaustive with examples (60+ min)

## Visual Elements

- Mermaid diagrams (architecture, flow charts, sequence)
- Code examples from codebase
- Specific file:line references
- Tables for structured info
- Lists for guidelines

## Tools Used

- **Task (Explore agent)**: Codebase exploration
- **Glob**: Map directory structure
- **Grep**: Find patterns, imports, exports
- **Read**: Analyze key files
- **Write**: Create documentation
- **Bash**: Extract metadata (git log, versions)

## Success Criteria

- Complete coverage of all areas
- Clear explanations with examples
- Visual diagrams for complex concepts
- Specific file:line references
- Actionable setup/development instructions
- New developer can onboard using only docs
- Organized, navigable structure
- Accurate and current information

## Integration

- **code-auditor**: Includes quality/security context
- **project-bootstrapper**: Documents bootstrap decisions
- **visual-html-creator**: Create visual diagrams
