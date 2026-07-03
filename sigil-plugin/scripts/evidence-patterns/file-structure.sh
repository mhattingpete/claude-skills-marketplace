#!/usr/bin/env bash
# evidence-patterns/file-structure.sh
# Pattern: Verify required files exist for a Claude Code plugin
# Evidence hash seed: "sigil-evidence-v1-file-structure"
set -euo pipefail

TARGET_DIR="${1:-.}"
cd "$TARGET_DIR"

errors=0

# Check for plugin.json (required for marketplace plugins)
if [ -f .claude-plugin/plugin.json ] || [ -f plugin.json ]; then
  echo "PASS:plugin.json exists"
else
  echo "FAIL:plugin.json not found at .claude-plugin/plugin.json or ./plugin.json"
  errors=$((errors + 1))
fi

# Check for SKILL.md files in skills/ directory
if [ -d skills ]; then
  skill_count=$(find skills -name 'SKILL.md' -type f 2>/dev/null | wc -l)
  if [ "$skill_count" -gt 0 ]; then
    echo "PASS:$skill_count SKILL.md files found in skills/"
  else
    echo "FAIL:No SKILL.md files found in skills/ directory"
    errors=$((errors + 1))
  fi
else
  echo "WARN:No skills/ directory (standalone skills may not need one)"
fi

# Check for README.md
if [ -f README.md ]; then
  echo "PASS:README.md exists"
else
  echo "WARN:No README.md found"
fi

# gitignored files check
if [ -f .gitignore ]; then
  echo "PASS:.gitignore exists"
  if grep -q '\.env' .gitignore 2>/dev/null; then
    echo "PASS:.gitignore covers .env files"
  else
    echo "WARN:.gitignore does not cover .env files"
  fi
else
  echo "WARN:No .gitignore found"
fi

echo "TOTAL_ERRORS:$errors"
exit 0
