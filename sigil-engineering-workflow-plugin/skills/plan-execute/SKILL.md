---
name: plan-execute
description: Verified, risk-assessed implementation planning with language detection, lightweight security/feasibility review, and parallel agent execution for complex work
---

# Plan Execute

## Purpose
Before accepting an implementation plan, run lightweight parallel reviews (engineering feasibility + security surface). For risky or complex tasks, execute with 2 parallel implementation agents and ensemble evaluation. Detects project language automatically — never assumes `make` or `pytest`.

## When to Use

**Activation phrases:**
- "Plan this feature implementation"
- "Plan this with security review"
- "What's the best approach for this feature?"
- "Assess the risk of this implementation"
- "Design the architecture for this change"
- "Should I build this the way I'm thinking?"

## What It Does

1. **Language detection**: Probes project root for pyproject.toml, package.json, Cargo.toml, go.mod, Makefile, CMakeLists.txt to determine toolchain
2. **Risk classification**: Analyzes scope to determine low/medium/high risk:
   - Low: single file change, well-understood, no external deps
   - Medium: multi-file, existing patterns, some ambiguity
   - High: cross-cutting change, new patterns, security surface
3. **Lightweight review** (medium+ risk): Spawns 2 parallel Sigil-style mini-reviews:
   - Engineering lens: feasibility, architecture fit, edge cases
   - Security lens: attack surface, data exposure, injection vectors
4. **Plan generation**: Produces a structured implementation plan with file list, dependencies, and risk assessment
5. **Parallel execution** (optional, high risk): Spawns 2 parallel implementation agents with ensemble comparison

## Approach

### Step 1: Detect Toolchain
Check files in order and set context:
```
pyproject.toml → python, pytest/uv
package.json → node, npm/yarn test
Cargo.toml → rust, cargo test
go.mod → go, go test ./...
Makefile → make test
CMakeLists.txt → cmake --build
```
If none detected: ask user what framework they use.

### Step 2: Classify Risk
- **Low**: No review needed. Generate plan directly.
- **Medium**: Run engineering + security mini-reviews in parallel. Incorporate findings into plan.
- **High**: Run reviews, generate plan, offer parallel execution with ensemble evaluation.

### Step 3: Generate Plan
Structured output:
```
Risk: [low/medium/high]
Toolchain: [detected]
Files to modify: [list with purpose]
Dependencies: [file A → file B order]
Risks: [from reviews, if applicable]
Recommendation: [single agent or parallel with ensemble]
```

### Step 4: Execute (if requested)
For high-risk or user-requested parallel execution:
1. Spawn 2 implementation agents with same plan but independent execution
2. Each returns: diff + test results
3. Compare: conflicts, quality differences, missed edge cases
4. Present ensemble verdict or unified diff

## Tools Used
- **Bash**: Detect toolchain files, run tests
- **Read**: Understand target files
- **Grep**: Find dependencies and cross-file references
- **Agent**: Spawn parallel review and implementation agents

## Success Criteria
- Language/framework detected correctly
- Risk classified with justification
- Plan includes file list, dependencies, and risks
- Parallel agents (if used) produce consistent, verified output
- Tests pass after implementation

## Integration
Works with: safe-commit (to commit changes), solution-ensemble (for approach selection), test-doctor (to fix post-implementation test failures)
