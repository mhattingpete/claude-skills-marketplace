---
name: review-apply
description: PR review feedback implementation with structured classification, test-driven development for bug fixes, and cross-file dependency tracing
---

# Review Apply

## Purpose
Apply PR review feedback systematically: classify each comment by type (BUG/SECURITY/DESIGN/STYLE/DOC), write failing tests for bugs FIRST, trace cross-file dependencies before modifying shared symbols, and verify no regressions after changes.

## When to Use

**Activation phrases:**
- "Apply this PR review feedback"
- "Implement the code review suggestions"
- "Address the review comments"
- "Fix the issues from the PR review"
- "Respond to reviewer feedback"

## What It Does

1. **Ingest feedback**: Read the review comments (from PR, markdown, or user paste)
2. **Classify by type**: BUG / SECURITY / DESIGN / STYLE / DOC — each gets a different procedure
3. **Trace dependencies**: Before modifying any shared symbol, grep for all callers
4. **TDD for bugs**: Write a failing test first, then fix the code (proves the fix works)
5. **Apply changes**: One classification group at a time, with verification between
6. **Verify regressions**: Re-run all tests after all changes
7. **Report**: Summary of what changed, what was TDD'd, what was verified

## Approach

### Step 1: Ingest and Classify
Parse each review comment:
```
Comment: "This function doesn't handle empty input"
Type: BUG → TDD required (write failing test first)
Files: api/users.py:42

Comment: "Consider using env vars instead of hardcoded secrets"
Type: SECURITY → Pre/post safety comparison required
Files: config/settings.py:12

Comment: "This could be refactored into a helper"
Type: DESIGN → Architecture review, dependency trace required
Files: src/utils.py:88, src/api/orders.py:15

Comment: "Remove commented-out code"
Type: STYLE → Direct edit, no test needed

Comment: "Add docstrings to public methods"
Type: DOC → Direct edit, no test needed
```

### Step 2: Dependency Trace (for BUG and DESIGN types)
Before modifying a shared function/symbol:
```bash
grep -r "symbol_name" src/ --include="*.py" | grep -v test | grep -v __pycache__
```
List all callers. Verify your fix won't break them.

### Step 3: TDD for BUG Classifications
For each BUG item:
1. Write a test that reproduces the bug (this test should FAIL)
2. Run the test to confirm it fails
3. Fix the code
4. Run the test again to confirm it passes
5. Keep the test as regression protection

### Step 4: Apply Changes by Group
Priority order:
1. SECURITY (highest risk)
2. BUG (user-facing)
3. DESIGN (architecture)
4. STYLE
5. DOC

After each group: re-run tests to catch breakage early.

### Step 5: Final Verification
```
All tests pass: ✅
Regression check: All N previously-passing tests still pass
New tests added: M (TDD for bugs)
```

## Tools Used
- **Bash**: Run tests, grep for dependencies
- **Read**: Understand review comments and target files
- **Edit/Write**: Apply changes
- **Grep**: Cross-file dependency tracing
- **Agent**: For complex TDD that needs independent verification

## Success Criteria
- All review comments are classified and addressed
- Every BUG classification has a new failing-then-passing test
- Cross-file dependencies are traced before any shared symbol modification
- All tests pass after all changes
- Report shows what changed and why

## Integration
Works with: safe-commit (to commit review fixes), test-doctor (if existing tests break during changes)
