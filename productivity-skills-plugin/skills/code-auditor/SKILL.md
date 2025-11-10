---
name: code-auditor
description: Performs comprehensive codebase analysis covering architecture, code quality, security, performance, testing, and maintainability. Use when user wants to audit code quality, identify technical debt, find security issues, assess test coverage, or get a codebase health check.
---

# Code Auditor

Comprehensive codebase analysis covering architecture, code quality, security, performance, testing, and maintainability.

## When to Use

- "audit the code"
- "analyze code quality"
- "check for issues"
- "review the codebase"
- "find technical debt"
- "security audit"
- "performance review"

## What It Analyzes

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

1. **Explore** using Explore agent (thorough mode)
2. **Identify patterns** with Grep and Glob
3. **Read critical files** for detailed analysis
4. **Run static analysis tools** if available
5. **Synthesize findings** into actionable report

## Thoroughness Levels

- **Quick** (15-30 min): High-level, critical issues only
- **Standard** (30-60 min): Comprehensive across all dimensions
- **Deep** (60+ min): Exhaustive with detailed examples

## Output Format

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

## Tools Used

- **Task (Explore agent)**: Thorough codebase exploration
- **Grep**: Pattern matching for issues
- **Glob**: Find files by type/pattern
- **Read**: Detailed file analysis
- **Bash**: Run linters, coverage tools

## Success Criteria

- Comprehensive coverage of all six dimensions
- Specific file:line references for all findings
- Severity/priority ratings (Critical/High/Medium/Low)
- Actionable recommendations (not just observations)
- Estimated effort for fixes
- Both quick wins and long-term improvements

## Integration

- **feature-planning**: Plan technical debt reduction
- **test-fixing**: Address test gaps identified
- **project-bootstrapper**: Set up quality tooling

## Configuration

Can focus on specific areas:
- Security-only audit
- Performance-only audit
- Testing-only assessment
- Quick architecture review
