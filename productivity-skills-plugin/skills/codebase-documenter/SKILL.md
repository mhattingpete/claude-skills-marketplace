---
name: codebase-documenter
description: Generates comprehensive documentation explaining how a codebase works, including architecture, key components, data flow, and development guidelines. Use when user wants to understand unfamiliar code, create onboarding docs, document architecture, or explain how the system works. Also activates when user says "explain this codebase", "document the architecture", "how does this code work", "create developer documentation", or similar documentation requests.
---

# Codebase Documenter Skill

## Purpose

Generates comprehensive documentation explaining how a codebase works, including architecture, key components, data flow, and development guidelines. Creates onboarding material for new developers or helps existing developers understand unfamiliar code.

## When to Use

This skill automatically activates when users want to:
- Understand an unfamiliar codebase
- Create onboarding documentation
- Document architecture and design decisions
- Explain how the system works
- Prepare for knowledge transfer
- Create developer guides
- Document technical specifications

**Activation phrases:**
- "explain this codebase"
- "document the architecture"
- "how does this code work"
- "create developer documentation"
- "generate codebase overview"
- "help me understand this project"
- "create onboarding docs"

## What It Does

Creates comprehensive documentation covering:

### 1. Project Overview
- **Purpose & Vision**: What the project does and why
- **Target Users**: Who uses it and how
- **Key Features**: Main functionality
- **Technology Stack**: Languages, frameworks, libraries
- **Project Status**: Maturity, active development, versioning

### 2. Architecture
- **High-Level Structure**: System components and layers
- **Design Patterns**: Patterns employed and why
- **Data Flow**: How information moves through the system
- **Control Flow**: Request/response cycles, event handling
- **Diagrams**: Visual representations (Mermaid)
- **Architectural Decisions**: ADRs or rationale

### 3. Directory Structure
- **Organization**: Purpose of each directory
- **Conventions**: File naming and organization patterns
- **Entry Points**: Where execution begins
- **Core Modules**: Most important files/directories
- **Configuration**: Where settings live

### 4. Key Components
- **Major Modules**: Primary code units
- **Classes & Functions**: Important abstractions
- **Responsibilities**: What each component does
- **Interactions**: How components work together
- **Extension Points**: Where to add new features
- **Code Examples**: Typical usage patterns

### 5. External Integrations
- **APIs Consumed**: Third-party services used
- **Databases**: Data stores and schemas
- **Authentication**: How auth works
- **Caching**: Caching strategies
- **Message Queues**: Async communication
- **File Storage**: Where files are stored

### 6. Data Models
- **Database Schema**: Tables, relationships
- **Data Structures**: Key types and interfaces
- **Validation**: How data is validated
- **Migrations**: Schema evolution
- **Data Flow**: How data transforms

### 7. Development Setup
- **Prerequisites**: Required tools and versions
- **Installation**: Step-by-step setup
- **Configuration**: Environment variables, configs
- **Running**: How to start the application
- **Testing**: How to run tests
- **Debugging**: Debugging strategies
- **Common Issues**: Troubleshooting guide

### 8. Development Guidelines
- **Coding Conventions**: Style and patterns
- **Testing Approach**: Testing philosophy
- **Error Handling**: How errors are handled
- **Logging**: Logging practices
- **Security Practices**: Security considerations
- **Performance**: Performance patterns

### 9. Deployment
- **Build Process**: How to build for production
- **Deployment Steps**: How to deploy
- **Environments**: Dev, staging, production
- **Monitoring**: How the system is monitored
- **Rollback**: How to undo deployments

### 10. Contributing
- **Development Workflow**: Branch strategy, PR process
- **Code Review**: Review guidelines
- **Testing Requirements**: What tests are needed
- **Documentation**: When/how to update docs

## Approach

### Analysis Strategy

1. **Explore thoroughly** using Explore agent
2. **Map structure** with Glob to find key files
3. **Read critical files** (README, main entry points, core modules)
4. **Identify patterns** through Grep (imports, exports, patterns)
5. **Understand data flow** by tracing execution paths
6. **Extract knowledge** from existing docs, comments, tests
7. **Synthesize** into cohesive documentation

### Documentation Output

Creates a comprehensive markdown document (or multiple docs):

```
docs/
├── README.md                    # Overview and quick start
├── ARCHITECTURE.md              # System architecture
├── DEVELOPMENT.md               # Development guide
├── API.md                       # API documentation (if applicable)
├── DEPLOYMENT.md                # Deployment guide
└── CONTRIBUTING.md              # Contribution guidelines
```

Or single comprehensive doc if preferred.

### Depth Levels

Adapts depth based on needs:
- **Quick**: High-level overview (15-30 min)
- **Standard**: Comprehensive coverage (30-60 min)
- **Deep**: Exhaustive with examples (60+ min)

### Visual Elements

Includes:
- **Mermaid diagrams**: Architecture, flow charts, sequence diagrams
- **Code examples**: Real code from the codebase
- **File references**: Specific file:line pointers
- **Tables**: For structured information
- **Lists**: For guidelines and conventions

## Example Interaction

```
User: "Explain this codebase and create documentation"

Skill:
1. Explores codebase structure
2. Identifies:
   - Express.js REST API
   - PostgreSQL database
   - React frontend (separate repo)
   - Redis caching
   - JWT authentication
3. Maps architecture:
   - routes/ → controllers/ → services/ → models/
   - middleware for auth, validation, logging
   - config/ for environment-specific settings
4. Generates documentation:
   - Architecture diagram (Mermaid)
   - API endpoint reference
   - Database schema
   - Development setup guide
   - Contributing guidelines
   - Deployment process
5. Creates docs/ directory with organized markdown files
```

## Tools Used

- **Task (Explore agent)**: Comprehensive codebase exploration
- **Glob**: Map directory structure and find files
- **Grep**: Find patterns, imports, exports
- **Read**: Analyze key files in detail
- **Write**: Create documentation files
- **Bash**: Extract metadata (git log, dependency versions)

## Success Criteria

- Complete coverage of all documentation areas
- Clear explanations with examples
- Visual diagrams for complex concepts
- Specific file:line references throughout
- Actionable setup/development instructions
- New developer can onboard using only this doc
- Organized, navigable structure
- Accurate and up-to-date information

## Output Formats

Can generate:
- **Markdown files**: Standard developer docs
- **HTML**: For internal wikis or hosting
- **PDF**: Using document-skills if requested
- **Inline**: Single comprehensive response

User can specify format preference, defaults to markdown files.

## Customization

Adapts to:
- **Audience**: New developers vs experienced team
- **Depth**: Quick overview vs comprehensive guide
- **Focus**: Architecture-focused vs development-focused
- **Format**: Multiple files vs single doc

## Integration

Works well with:
- **code-auditor**: Includes quality/security context in docs
- **project-bootstrapper**: Documents bootstrap decisions
- **visual-html-creator**: Create visual diagrams and flows

## Special Features

### Auto-Discovery

Automatically detects and documents:
- **Framework conventions**: Rails, Django, Next.js patterns
- **API patterns**: REST, GraphQL, gRPC
- **Testing approaches**: Unit, integration, e2e
- **Build systems**: Webpack, Vite, etc.
- **Deployment targets**: Docker, serverless, etc.

### Living Documentation

Can suggest:
- Where to add code comments for clarity
- What should be documented in code vs external docs
- How to keep documentation synchronized with code
- Automation for doc generation (JSDoc, Sphinx, etc.)

## Post-Documentation

After generating docs, provides:
- **Summary** of what was documented
- **Gaps** that couldn't be fully documented (need clarification)
- **Suggestions** for keeping docs current
- **Next steps** for improving codebase clarity
- **Templates** for future documentation

## Privacy & Security

- **Avoids** documenting sensitive information (secrets, keys)
- **Redacts** credentials if found
- **Flags** security issues for separate discussion
- **Respects** .gitignore (doesn't document ignored files)
