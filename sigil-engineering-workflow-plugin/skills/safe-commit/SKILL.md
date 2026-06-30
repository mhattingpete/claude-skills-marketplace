---
name: safe-commit
description: Security-gated git workflow with secret scanning, individual file staging, retry logic with exponential backoff, merge conflict resolution, and auto-generated commit messages
---

# Safe Commit

## Purpose
Git workflow that never stages secrets, never force-pushes, and never commits merge conflicts. Stages files individually with user review, runs secret scanning before every operation, retries push failures with exponential backoff, and generates accurate commit messages from the staged diff.

## When to Use

**Activation phrases:**
- "Commit these changes"
- "Push my changes safely"
- "Stage and commit my work"
- "Create a pull request"
- "What's in my working tree?"
- "Save my progress to git"

## What It Does

1. **Status review**: Shows `git status --porcelain` and groups changes by type (modified, new, deleted, renamed)
2. **Secret scan**: Runs `scripts/detect-secrets.sh` on all changed files BEFORE staging anything
3. **Individual staging**: Stages files one logical group at a time — never `git add .`
4. **User confirmation**: Shows what will be committed before proceeding
5. **Commit message generation**: Analyzes staged diff to generate a descriptive message (not filename heuristics)
6. **Push with retry**: Pushes with exponential backoff: 2s, 4s, 8s (3 attempts)
7. **Merge conflict handling**: If pull needed, detects conflicts and resolves interactively

## Approach

### Step 1: Review Working Tree
```
git status --porcelain
```
Group changes:
- **Modified**: Existing files changed
- **Untracked**: New files
- **Deleted**: Removed files
- **Renamed**: Moved/renamed files

### Step 2: Secret Scan
```bash
scripts/detect-secrets.sh $(git diff --name-only) $(git ls-files --others --exclude-standard)
```
If secrets found: show files, patterns matched, and BLOCK the commit.

### Step 3: Stage in Groups
Present groups to user:
```
Modified: src/api/users.py, src/api/auth.py
New: tests/test_users.py
Deleted: (none)
Stage all? [y/n/details]
```
If "details": stage one file at a time with user confirmation.

### Step 4: Generate Commit Message
Analyze the staged diff:
- Primary changes: what files changed and why
- Scope: feature, fix, refactor, docs, test
- Breaking: any breaking API changes?
Present to user for editing.

### Step 5: Commit and Push
```bash
git commit -m "<generated message>"
# Push with retry
for delay in 2 4 8; do
  git push && break
  echo "Push failed, retrying in ${delay}s..."
  sleep $delay
done
```

### Step 6: Handle Pull Conflicts
If push is rejected (non-fast-forward):
```bash
git pull --rebase
# If conflict:
# 1. Show conflicting files
# 2. Offer to resolve each interactively
# 3. git rebase --continue
# 4. git push
```

## Tools Used
- **Bash**: Run git commands, detect-secrets.sh
- **Read**: Review diffs before staging
- **AskUserQuestion**: Confirm staging groups and edit commit messages
- **Scripts**: `detect-secrets.sh` for secret detection

## Success Criteria
- No secrets committed (verified by detect-secrets.sh before every commit)
- Individual files reviewed before staging (never `git add .`)
- Push succeeds within 3 retry attempts
- Merge conflicts resolved interactively (never committed)
- Commit message accurately describes the change

## Integration
Works with: review-apply (to commit review fixes), test-doctor (to commit test changes), plan-execute (to commit implementation)
