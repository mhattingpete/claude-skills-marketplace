#!/usr/bin/env bash
# evidence-patterns/frontmatter-valid.sh
# Pattern: Verify SKILL.md files have valid YAML frontmatter
# Evidence hash seed: "sigil-evidence-v1-frontmatter"
set -euo pipefail

TARGET_DIR="${1:-.}"
cd "$TARGET_DIR"

errors=0
checked=0

find_skill_files() {
  if [ -d skills ]; then
    find skills -name 'SKILL.md' -type f 2>/dev/null
  fi
  if [ -f SKILL.md ]; then
    echo "SKILL.md"
  fi
}

while IFS= read -r file; do
  [ -z "$file" ] && continue
  checked=$((checked + 1))

  # Check frontmatter exists (starts with ---)
  first_line=$(head -1 "$file" 2>/dev/null)
  if [ "$first_line" != "---" ]; then
    echo "FAIL:$file:missing frontmatter (does not start with ---)"
    errors=$((errors + 1))
    continue
  fi

  # Check frontmatter closes
  if ! head -50 "$file" | tail -n +2 | grep -q '^---'; then
    echo "FAIL:$file:unclosed frontmatter (no closing --- within first 50 lines)"
    errors=$((errors + 1))
    continue
  fi

  # Extract frontmatter between first and second ---
  fm=$(sed -n '/^---$/,/^---$/p' "$file" | sed '1d;$d' 2>/dev/null)

  # Check for name field
  if echo "$fm" | grep -qP '^name:\s*'; then
    name=$(echo "$fm" | grep -P '^name:\s*' | sed 's/^name:\s*//')
    echo "PASS:$file:name=\"$name\""
  else
    echo "FAIL:$file:missing 'name' field in frontmatter"
    errors=$((errors + 1))
  fi

  # Check for description field
  if echo "$fm" | grep -qP '^description:\s*'; then
    desc=$(echo "$fm" | grep -P '^description:\s*' | sed 's/^description:\s*//' | head -c 80)
    echo "PASS:$file:description=\"${desc}...\""
  else
    echo "FAIL:$file:missing 'description' field in frontmatter"
    errors=$((errors + 1))
  fi

  # Check for triggers field
  if echo "$fm" | grep -qP '^triggers:\s*'; then
    triggers=$(echo "$fm" | grep -cP '^\s+- ' || true)
    echo "PASS:$file:triggers field with $triggers trigger(s)"
  else
    echo "WARN:$file:missing 'triggers' field (may still activate via description)"
  fi

done < <(find_skill_files)

echo "CHECKED:$checked"
echo "TOTAL_ERRORS:$errors"
exit 0
