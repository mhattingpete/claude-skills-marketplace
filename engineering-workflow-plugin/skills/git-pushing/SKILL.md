---
name: git-pushing
description: Stage, commit, and push git changes with conventional commit messages. Use when user wants to commit and push changes, mentions pushing to remote, or asks to save and push their work. Also activates when user says "push changes", "commit and push", "push this", "push to github", or similar git workflow requests.
---

# Git Push Workflow

Stage all changes, create a conventional commit, and push to the remote branch.

## When to Use

Automatically activate when the user:
- Explicitly asks to push changes ("push this", "commit and push")
- Mentions saving work to remote ("save to github", "push to remote")
- Completes a feature and wants to share it
- Says phrases like "let's push this up" or "commit these changes"

## Workflow

**ALWAYS use the smart_commit.sh script** - Do NOT use manual git commands:

```bash
bash skills/git-pushing/scripts/smart_commit.sh
```

This script handles everything automatically:
- ✅ Staging all changes
- ✅ Auto-generating conventional commit messages
- ✅ Adding Claude Code footer
- ✅ Pushing to remote (with -u for new branches)
- ✅ Showing PR link for GitHub repos

**With custom message:**
```bash
bash skills/git-pushing/scripts/smart_commit.sh "feat: add new feature"
```

The script automatically:
- Determines commit type (feat/fix/docs/test/chore/refactor)
- Extracts scope from changed files
- Handles new vs existing branches
- Shows colored output for better UX

**IMPORTANT**: Do NOT use manual git add/commit/push commands. Always use the script.

## Script Behavior

The script will automatically:
1. Check git status
2. Stage all changes with `git add .`
3. Generate conventional commit message (or use provided one)
4. Add Claude Code footer
5. Create commit
6. Push to remote (with -u flag for new branches)
7. Show PR creation link for GitHub repos

You just need to run the script - it handles everything.

## Examples

**User:** "Push these changes"
**Action:**
```bash
bash skills/git-pushing/scripts/smart_commit.sh
```

**User:** "Commit with message 'fix: resolve table extraction issue'"
**Action:**
```bash
bash skills/git-pushing/scripts/smart_commit.sh "fix: resolve table extraction issue"
```

**User:** "Let's save this to github"
**Action:**
```bash
bash skills/git-pushing/scripts/smart_commit.sh
# Script auto-generates appropriate commit message
```
