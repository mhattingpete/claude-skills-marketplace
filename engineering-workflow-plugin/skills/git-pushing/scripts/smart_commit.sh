#!/bin/bash
# Smart Git Commit Script for git-pushing skill
# Handles staging, commit message generation, and pushing

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
info() { echo -e "${GREEN}→${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
error() { echo -e "${RED}✗${NC} $1" >&2; }

# Get current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
info "Current branch: $CURRENT_BRANCH"

# Check if there are changes
if git diff --quiet && git diff --cached --quiet; then
    warn "No changes to commit"
    exit 0
fi

# Stage all changes
info "Staging all changes..."
git add .

# Get staged files for commit message analysis
STAGED_FILES=$(git diff --cached --name-only)
DIFF_STAT=$(git diff --cached --stat)

# Analyze changes to determine commit type
determine_commit_type() {
    local files="$1"

    # Check for specific patterns
    if echo "$files" | grep -q "test"; then
        echo "test"
    elif echo "$files" | grep -qE "\.(md|txt|rst)$"; then
        echo "docs"
    elif echo "$files" | grep -qE "package\.json|requirements\.txt|Cargo\.toml"; then
        echo "chore"
    elif git diff --cached | grep -qE "^[\+].*fix|^[\+].*bug"; then
        echo "fix"
    elif git diff --cached | grep -qE "^[\+].*refactor"; then
        echo "refactor"
    else
        echo "feat"
    fi
}

# Analyze files to determine scope
determine_scope() {
    local files="$1"

    # Extract directory or component name
    local scope=$(echo "$files" | head -1 | cut -d'/' -f1)

    # Check for common patterns
    if echo "$files" | grep -q "plugin"; then
        echo "plugin"
    elif echo "$files" | grep -q "skill"; then
        echo "skill"
    elif echo "$files" | grep -q "agent"; then
        echo "agent"
    elif [ -n "$scope" ] && [ "$scope" != "." ]; then
        echo "$scope"
    else
        echo ""
    fi
}

# Generate commit message if not provided
if [ -z "$1" ]; then
    COMMIT_TYPE=$(determine_commit_type "$STAGED_FILES")
    SCOPE=$(determine_scope "$STAGED_FILES")

    # Count files changed
    NUM_FILES=$(echo "$STAGED_FILES" | wc -l | xargs)

    # Generate description based on changes
    if [ "$COMMIT_TYPE" = "docs" ]; then
        DESCRIPTION="update documentation"
    elif [ "$COMMIT_TYPE" = "test" ]; then
        DESCRIPTION="update tests"
    elif [ "$COMMIT_TYPE" = "chore" ]; then
        DESCRIPTION="update dependencies"
    else
        DESCRIPTION="update $NUM_FILES file(s)"
    fi

    # Build commit message
    if [ -n "$SCOPE" ]; then
        COMMIT_MSG="${COMMIT_TYPE}(${SCOPE}): ${DESCRIPTION}"
    else
        COMMIT_MSG="${COMMIT_TYPE}: ${DESCRIPTION}"
    fi

    info "Generated commit message: $COMMIT_MSG"
else
    COMMIT_MSG="$1"
    info "Using provided message: $COMMIT_MSG"
fi

# Create commit with Claude Code footer
git commit -m "$(cat <<EOF
${COMMIT_MSG}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

COMMIT_HASH=$(git rev-parse --short HEAD)
info "Created commit: $COMMIT_HASH"

# Push to remote
info "Pushing to origin/$CURRENT_BRANCH..."

# Check if branch exists on remote
if git ls-remote --exit-code --heads origin "$CURRENT_BRANCH" >/dev/null 2>&1; then
    # Branch exists, just push
    if git push; then
        info "Successfully pushed to origin/$CURRENT_BRANCH"
        echo "$DIFF_STAT"
    else
        error "Push failed"
        exit 1
    fi
else
    # New branch, push with -u
    if git push -u origin "$CURRENT_BRANCH"; then
        info "Successfully pushed new branch to origin/$CURRENT_BRANCH"
        echo "$DIFF_STAT"

        # Check if it's GitHub and show PR link
        REMOTE_URL=$(git remote get-url origin)
        if echo "$REMOTE_URL" | grep -q "github.com"; then
            REPO=$(echo "$REMOTE_URL" | sed -E 's/.*github\.com[:/](.*)\.git/\1/')
            warn "Create PR: https://github.com/$REPO/pull/new/$CURRENT_BRANCH"
        fi
    else
        error "Push failed"
        exit 1
    fi
fi

exit 0
