---
name: code-auditor
description: Performs comprehensive codebase analysis covering architecture, code quality, security, performance, testing, and maintainability. Use when user wants to audit code quality, identify technical debt, find security issues, assess test coverage, or get a codebase health check. Also activates when user says "audit the code", "check for issues", "review the codebase", "security audit", or similar analysis requests.
---

# Code Auditor Skill

## Purpose

Performs comprehensive codebase analysis covering architecture, code quality, security, performance, testing, and maintainability. Provides a detailed audit report with specific findings and prioritized recommendations.

## When to Use

This skill automatically activates when users want to:
- Understand code quality and technical debt
- Identify security vulnerabilities or risks
- Find performance bottlenecks
- Assess testing coverage and quality
- Prepare for major refactoring
- Onboard to an unfamiliar codebase
- Get a "health check" on their project

**Activation phrases:**
- "audit the code"
- "analyze code quality"
- "check for issues"
- "review the codebase"
- "find technical debt"
- "security audit"
- "performance review"

## What It Does

Conducts a thorough analysis across six key dimensions:

### 1. Architecture & Design
- Overall structure and organization
- Design patterns in use
- Module boundaries and separation of concerns
- Dependency management
- Architectural decisions and trade-offs

### 2. Code Quality
- Complexity hotspots (cyclomatic complexity)
- Code duplication (DRY violations)
- Naming conventions and consistency
- Documentation coverage
- Code smells and anti-patterns

### 3. Security
- Common vulnerabilities (OWASP Top 10)
- Input validation and sanitization
- Authentication and authorization
- Secrets management
- Dependency vulnerabilities

### 4. Performance
- Algorithmic complexity issues
- Database query optimization
- Memory usage patterns
- Caching opportunities
- Resource leaks

### 5. Testing
- Test coverage assessment
- Test quality and effectiveness
- Missing test scenarios
- Testing patterns and practices
- Integration vs unit test balance

### 6. Maintainability
- Technical debt assessment
- Coupling and cohesion
- Ease of future changes
- Onboarding friendliness
- Documentation quality

## Approach

### Analysis Strategy

1. **Explore codebase** using Explore agent (thorough mode)
2. **Identify patterns** through Grep and Glob
3. **Read critical files** for detailed analysis
4. **Run static analysis tools** if available (linters, complexity analyzers)
5. **Synthesize findings** into actionable report

### Thoroughness Levels

Adapts analysis depth based on:
- **Quick** (15-30 min): High-level overview, critical issues only
- **Standard** (30-60 min): Comprehensive across all dimensions
- **Deep** (60+ min): Exhaustive analysis with detailed examples

User can specify preference, defaults to Standard.

### Output Format

Structured markdown report with:

```markdown
# Code Audit Report

## Executive Summary
- Overall health score
- Critical issues count
- Top 3 priorities

## Findings by Category

### Architecture & Design
#### 🔴 High Priority
- [Finding with file:line reference]
  - Impact: [description]
  - Recommendation: [action]

#### 🟡 Medium Priority
...

### [Other categories]

## Prioritized Action Plan
1. Quick wins (< 1 day)
2. Medium-term improvements (1-5 days)
3. Long-term initiatives (> 5 days)

## Metrics
- Files analyzed: X
- Lines of code: Y
- Test coverage: Z%
- Complexity hotspots: N
```

## Example Interaction

```
User: "Audit the code quality and find issues"

Skill:
1. Uses Explore agent to map codebase
2. Identifies:
   - 3 files with cyclomatic complexity > 20
   - SQL injection vulnerability in query builder
   - 40% code duplication in data processing
   - Missing tests for critical auth flow
   - 12 TODO comments indicating incomplete work
3. Generates report with:
   - Critical: Fix SQL injection (file:line)
   - High: Add auth tests
   - Medium: Refactor duplicated code
   - Low: Address TODOs
4. Provides action plan with estimates
```

## Tools Used

- **Task (Explore agent)**: Thorough codebase exploration
- **Grep**: Pattern matching for issues (SQL, secrets, TODOs)
- **Glob**: Find files by type and pattern
- **Read**: Detailed file analysis
- **Bash**: Run linters, test coverage tools if available

## Success Criteria

- Comprehensive coverage of all six dimensions
- Specific file:line references for all findings
- Severity/priority ratings (Critical/High/Medium/Low)
- Actionable recommendations (not just observations)
- Estimated effort for fixes
- Both quick wins and long-term improvements identified

## Integration

Works well with:
- **feature-planning**: For planning technical debt reduction
- **test-fixing**: For addressing test gaps identified
- **project-bootstrapper**: For setting up quality tooling

## Configuration

Can focus analysis on specific areas if requested:
- Security-only audit
- Performance-only audit
- Testing-only assessment
- Quick architecture review

User can specify focus areas, or skill analyzes all dimensions by default.
