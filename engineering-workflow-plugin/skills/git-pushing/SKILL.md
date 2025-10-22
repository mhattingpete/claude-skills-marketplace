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

### Fast Path (Recommended)

Use the automated script for maximum speed:

```bash
bash scripts/smart_commit.sh
```

This script handles:
- ✅ Staging all changes
- ✅ Auto-generating conventional commit messages
- ✅ Adding Claude Code footer
- ✅ Pushing to remote (with -u for new branches)
- ✅ Showing PR link for GitHub repos

**With custom message:**
```bash
bash scripts/smart_commit.sh "feat: add new feature"
```

The script automatically:
- Determines commit type (feat/fix/docs/test/chore/refactor)
- Extracts scope from changed files
- Handles new vs existing branches
- Shows colored output for better UX

### Manual Path (Fallback)

Use when script is unavailable or custom workflow needed:

**1. Check Git Status**

Run `git status` to understand:
- Which files have changed
- What will be committed
- Current branch name

**2. Stage Changes**

- Run `git add .` to stage all changes
- Alternatively, stage specific files if partial commit is needed

**3. Create Commit Message**

**If user provided a message:**
- Use it directly

**If no message provided:**
- Analyze changes using `git diff`
- Generate a conventional commit message:
  - Format: `type(scope): description`
  - Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`
  - Keep description concise (50-90 characters)
  - Use imperative mood: "Add" not "Added"
- Always append Claude Code footer:
  ```
  🤖 Generated with [Claude Code](https://claude.com/claude-code)

  Co-Authored-By: Claude <noreply@anthropic.com>
  ```

**Use heredoc format:**
```bash
git commit -m "$(cat <<'EOF'
commit message here

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**4. Push to Remote**

- Run `git push` to push commits
- If new branch, use `git push -u origin <branch>`
- If push fails due to diverged branches, inform user and ask how to proceed

**5. Confirm Success**

- Report commit hash
- Summarize what was committed
- Confirm push succeeded

## Examples

User: "Push these changes"
→ Check status, stage all, generate commit message, push

User: "Commit with message 'fix: resolve table extraction issue'"
→ Use provided message, push

User: "Let's save this to github"
→ Activate workflow, generate appropriate commit message
