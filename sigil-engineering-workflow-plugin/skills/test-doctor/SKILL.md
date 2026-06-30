---
name: test-doctor
description: Language-agnostic test fixing with root-cause analysis, error clustering, and regression snapshots
---

# Test Doctor

## Purpose
Fix failing tests by grouping errors by ROOT CAUSE TYPE (not by file), clustering related failures, and proving zero regressions via before/after test snapshots. Language-agnostic — detects any test framework from the project's build files.

## When to Use

**Activation phrases:**
- "Fix the failing tests"
- "Why are the tests failing?"
- "These tests are broken"
- "Diagnose test failures"
- "Run the tests and fix any issues"
- "Make CI pass"

## What It Does

1. **Detects framework**: Automatically probes project for test framework (pytest, jest, cargo test, go test, rspec, etc.)
2. **Snapshots current state**: Saves currently-passing test names/IDs before any changes
3. **Runs and captures failures**: Executes tests, captures full error output
4. **Clusters by root cause**: Groups errors by underlying cause (import error, assertion mismatch, timeout, API mock, etc.) — NOT by file
5. **Fixes by cluster**: Addresses one root cause type at a time, re-running tests after each
6. **Verifies no regressions**: Re-runs the pre-fix passing tests to prove they still pass
7. **Reports**: What was broken, what was fixed, regression verification

## Approach

### Step 1: Detect Framework
Use `references/framework-detection.md` to determine the test framework. Probe build files in order: pyproject.toml → package.json → Cargo.toml → go.mod → Makefile → CMakeLists.txt.

### Step 2: Snapshot Passing Tests
Before touching any code:
```bash
# Capture current test output
[detected test command] 2>&1 | tee /tmp/test-output-before.txt
# Extract passing test names
grep "PASS\|✓\|ok " /tmp/test-output-before.txt > /tmp/passing-tests-before.txt
```

### Step 3: Cluster Failures by Root Cause
Analyze failure output. Common clusters:
- **Import/resolution errors**: Missing modules, bad imports, version conflicts
- **Assertion mismatches**: Expected ≠ actual values
- **Timeout/async**: Tests that hang or exceed timeout
- **Mock/API failures**: External service responses changed
- **State pollution**: Tests that pass alone but fail in suite
- **Environment**: Missing env vars, wrong Python/node version

### Step 4: Fix by Cluster
For each root cause cluster:
1. Fix all instances of that cause type
2. Re-run tests
3. Verify that cluster's failures are resolved
4. Verify no regressions: `grep "FAIL\|✗\|not ok"` on output

### Step 5: Regression Proof
After all fixes, demonstrate:
```
Before: 45 pass, 3 fail
After:  48 pass, 0 fail
Regression check: All 45 previously-passing tests still pass ✅
```

## Tools Used
- **Bash**: Run tests, capture output
- **Read**: Understand test code
- **Edit/Write**: Fix failing tests
- **Grep**: Find all instances of a broken pattern
- **References**: `framework-detection.md` for language-aware commands

## Success Criteria
- All tests pass after fixes
- Zero regressions in previously-passing tests
- Root causes are identified and reported
- Each cluster is fixed once (not file-by-file)
- Test command was detected, not hardcoded

## Integration
Works with: safe-commit (to commit test fixes), plan-execute (to plan test infrastructure improvements)
