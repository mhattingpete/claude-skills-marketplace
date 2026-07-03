#!/usr/bin/env bash
# evidence-patterns/version-consistency.sh
# Pattern: Verify version consistency across files
# Evidence hash seed: "sigil-evidence-v1-version-consistency"
set -euo pipefail

TARGET_DIR="${1:-.}"
cd "$TARGET_DIR"

errors=0

# Check VERSION file
version_file=""
if [ -f VERSION ]; then
  version_file=$(cat VERSION | tr -d '[:space:]')
  echo "PASS:VERSION file reads '$version_file'"
elif [ -f version.txt ]; then
  version_file=$(cat version.txt | tr -d '[:space:]')
  echo "PASS:version.txt reads '$version_file'"
elif [ -f .claude-plugin/plugin.json ]; then
  version_file=$(python3 -c "import json; print(json.load(open('.claude-plugin/plugin.json')).get('version',''))" 2>/dev/null)
  echo "INFO:plugin.json version = '$version_file'"
else
  echo "WARN:no VERSION file or plugin.json found"
fi

# Check plugin.json version matches VERSION
if [ -n "$version_file" ] && [ -f .claude-plugin/plugin.json ]; then
  plugin_version=$(python3 -c "import json; print(json.load(open('.claude-plugin/plugin.json')).get('version',''))" 2>/dev/null)
  if [ "$plugin_version" = "$version_file" ]; then
    echo "PASS:plugin.json version matches VERSION ($version_file)"
  else
    echo "FAIL:plugin.json version '$plugin_version' != VERSION '$version_file'"
    errors=$((errors + 1))
  fi
fi

# Check CHANGELOG.md has entry for current version
if [ -n "$version_file" ] && [ -f CHANGELOG.md ]; then
  if grep -q " $version_file " CHANGELOG.md 2>/dev/null; then
    echo "PASS:CHANGELOG.md has entry for v$version_file"
  else
    echo "WARN:CHANGELOG.md has no entry for v$version_file"
  fi
fi

echo "TOTAL_ERRORS:$errors"
exit 0
