---
description: Create a pull request using the git-pushing skill
---

Use the `git-pushing` skill to create a pull request for the current changes.

Follow the git-pushing skill workflow:
1. Run git status and git diff to understand current changes
2. Analyze commits from when branch diverged from base branch (use git log and git diff [base-branch]...HEAD)
3. Draft a comprehensive PR summary based on ALL commits (not just the latest)
4. Create new branch if needed, push to remote, and create PR using gh pr create

Important: Make sure to review the FULL commit history for this branch, not just the most recent commit.
