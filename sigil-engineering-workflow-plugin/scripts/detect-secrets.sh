#!/usr/bin/env bash
# detect-secrets.sh — Scan files for secret patterns before staging/commit
# Exit code 1 = secrets found (blocks operation)
# Exit code 0 = clean
set -euo pipefail

# Patterns that indicate secrets (grep -E pattern)
SECRET_PATTERNS=(
  'shpat_[a-fA-F0-9]{32,}'
  'shpss_[a-fA-F0-9]{32,}'
  'shpca_[a-fA-F0-9]{32,}'
  'sk_live_[a-zA-Z0-9]{20,}'
  'sk_test_[a-zA-Z0-9]{20,}'
  'whsec_[a-zA-Z0-9]{16,}'
  'rk_live_[a-zA-Z0-9]{20,}'
  'ghp_[a-zA-Z0-9]{36,}'
  'ghs_[a-zA-Z0-9]{36,}'
  'AKIA[0-9A-Z]{16}'
  'sk-proj-[a-zA-Z0-9]{20,}'
  'sk-or-v1-[a-zA-Z0-9]{20,}'
  '-----BEGIN [A-Z ]*PRIVATE KEY-----'
)

FILES_TO_SCAN=("$@")
if [ ${#FILES_TO_SCAN[@]} -eq 0 ]; then
  # Default: scan all tracked and staged files
  FILES_TO_SCAN=($(git ls-files 2>/dev/null || echo "."))
fi

FOUND=0
for file in "${FILES_TO_SCAN[@]}"; do
  [ -f "$file" ] || continue
  for pattern in "${SECRET_PATTERNS[@]}"; do
    if grep -Eq "$pattern" "$file" 2>/dev/null; then
      echo "SECRET DETECTED: $file matched pattern: ${pattern:0:20}..."
      FOUND=1
    fi
  done
done

if [ $FOUND -eq 1 ]; then
  echo ""
  echo "⚠️  Secrets found! Commit blocked."
  echo "Remove secrets or add files to .gitignore before retrying."
  exit 1
fi

exit 0
