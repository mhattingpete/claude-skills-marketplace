#!/usr/bin/env bash
# evidence-patterns/secrets-check.sh
# Pattern: Scan for secret/credential leaks
# Evidence hash seed: "sigil-evidence-v1-secrets"
set -euo pipefail

TARGET_DIR="${1:-.}"
cd "$TARGET_DIR"

# Known secret patterns from .gitleaks.toml + common patterns
PATTERNS=(
  'shpat_[a-f0-9]{32}'
  'shpss_[a-f0-9]{32}'
  'sk_live_[a-zA-Z0-9]{24,}'
  'sk_test_[a-zA-Z0-9]{24,}'
  'whsec_[a-zA-Z0-9]{24,}'
  'ghp_[a-zA-Z0-9]{36}'
  'ghs_[a-zA-Z0-9]{36}'
  'AKIA[0-9A-Z]{16}'
  'sk-proj-[a-zA-Z0-9]{20,}'
  'sk-or-v1-[a-zA-Z0-9]{20,}'
  '-----BEGIN [A-Z ]*PRIVATE KEY-----'
)

total_leaks=0
for pattern in "${PATTERNS[@]}"; do
  # grep -r: recursive, -n: line numbers, -P: perl regex, -l: only filenames
  # Exclude .git/, node_modules/, evidence-patterns/ itself
  matches=$(grep -rnP "$pattern" --include='*.py' --include='*.js' --include='*.ts' --include='*.sh' --include='*.yaml' --include='*.yml' --include='*.json' --include='*.md' --include='*.env' --include='*.cfg' --include='*.ini' --include='*.toml' --exclude-dir='.git' --exclude-dir='node_modules' --exclude-dir='evidence-patterns' --exclude-dir='__pycache__' --exclude-dir='.venv' . 2>/dev/null || true)
  if [ -n "$matches" ]; then
    while IFS= read -r line; do
      echo "LEAK:${line}"
      total_leaks=$((total_leaks + 1))
    done <<< "$matches"
  fi
done

# Also check for common env var patterns that indicate secrets
env_matches=$(grep -rnP '^\s*(SECRET|PASSWORD|API_KEY|TOKEN|PRIVATE_KEY)\s*=' --include='*.env' --include='*.env.*' --include='*.cfg' --include='*.ini' . 2>/dev/null || true)
if [ -n "$env_matches" ]; then
  while IFS= read -r line; do
    echo "ENV_SECRET:${line}"
    total_leaks=$((total_leaks + 1))
  done <<< "$env_matches"
fi

echo "TOTAL:$total_leaks"
exit 0
