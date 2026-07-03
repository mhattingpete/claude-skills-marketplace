#!/usr/bin/env bash
# sigil-scan.sh — Standalone secrets scanner for Claude Code skills
#
# Scans a skill directory for leaked credentials and secret patterns.
# The only deterministic check that actually finds things a human wouldn't
# trivially catch.
#
# Usage:
#   sigil-scan.sh <skill-dir>
#
# Exit codes:
#   0 — No leaks found
#   1 — Leaks found
#   2 — Usage error
set -euo pipefail

TARGET_DIR="${1:-}"
if [ -z "$TARGET_DIR" ]; then
  echo "Usage: sigil-scan.sh <skill-dir>"
  exit 2
fi
if [ ! -d "$TARGET_DIR" ]; then
  echo "Error: Not a directory: $TARGET_DIR"
  exit 2
fi

TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"

echo "═══ SIGIL SCAN v0.1.0 ═══"
echo "Target: $TARGET_DIR"
echo ""

TOTAL_LEAKS=0

scan_pattern() {
  local label="$1"
  local pattern="$2"
  local include="$3"
  local exclude="${4:-}"

  local cmd="grep -rnP '$pattern' --include='$include' --exclude-dir='.git' --exclude-dir='node_modules' --exclude-dir='__pycache__' --exclude-dir='.venv'"
  if [ -n "$exclude" ]; then
    cmd="$cmd --exclude-dir='$exclude'"
  fi
  cmd="$cmd '$TARGET_DIR' 2>/dev/null || true"

  local matches
  matches=$(eval "$cmd")

  if [ -n "$matches" ]; then
    local count
    count=$(echo "$matches" | wc -l | tr -d ' ')
    echo "  LEAK:$label — $count match(es)"
    echo "$matches" | while IFS= read -r line; do
      echo "    $line"
    done
    TOTAL_LEAKS=$((TOTAL_LEAKS + count))
  fi
}

echo "─── Scanning for credential leaks ───"

# Shopify API tokens
scan_pattern "Shopify Admin API token (shpat_)"  'shpat_[a-f0-9]{32}'          "*.py,*.js,*.ts,*.sh,*.yaml,*.yml,*.json,*.md,*.env,*.toml,*.cfg"
scan_pattern "Shopify Secret token (shpss_)"     'shpss_[a-f0-9]{32}'           "*.py,*.js,*.ts,*.sh,*.yaml,*.yml,*.json,*.md,*.env"

# Stripe
scan_pattern "Stripe Live key (sk_live_)"        'sk_live_[a-zA-Z0-9]{24,}'     "*.py,*.js,*.ts,*.sh,*.yaml,*.yml,*.json,*.md,*.env"
scan_pattern "Stripe Test key (sk_test_)"        'sk_test_[a-zA-Z0-9]{24,}'     "*.py,*.js,*.ts,*.sh,*.yaml,*.yml,*.json,*.md,*.env"
scan_pattern "Stripe Webhook secret (whsec_)"    'whsec_[a-zA-Z0-9]{24,}'       "*.py,*.js,*.ts,*.sh,*.yaml,*.yml,*.json,*.md,*.env"

# GitHub
scan_pattern "GitHub Personal Access (ghp_)"     'ghp_[a-zA-Z0-9]{36}'          "*.py,*.js,*.ts,*.sh,*.yaml,*.yml,*.json,*.md,*.env"
scan_pattern "GitHub OAuth (ghs_)"               'ghs_[a-zA-Z0-9]{36}'          "*.py,*.js,*.ts,*.sh,*.yaml,*.yml,*.json,*.md,*.env"

# AWS
scan_pattern "AWS Access Key (AKIA)"             'AKIA[0-9A-Z]{16}'             "*.py,*.js,*.ts,*.sh,*.yaml,*.yml,*.json,*.md,*.env"

# OpenAI / Anthropic / AI API keys
scan_pattern "OpenAI Project key (sk-proj-)"     'sk-proj-[a-zA-Z0-9]{20,}'     "*.py,*.js,*.ts,*.sh,*.yaml,*.yml,*.json,*.md,*.env"
scan_pattern "OpenRouter / custom (sk-or-)"      'sk-or-v1-[a-zA-Z0-9]{20,}'    "*.py,*.js,*.ts,*.sh,*.yaml,*.yml,*.json,*.md,*.env"

# Private keys
scan_pattern "Private Key (PEM)"                 '-----BEGIN [A-Z ]*PRIVATE KEY-----'  "*.py,*.js,*.ts,*.sh,*.md" "__pycache__"

# Generic secret patterns in env/config files
scan_pattern "Hardcoded SECRET= in .env"         '^SECRET='                     ".env,.env.*" "__pycache__"
scan_pattern "Hardcoded PASSWORD= in .env"       '^PASSWORD='                   ".env,.env.*" "__pycache__"
scan_pattern "Hardcoded API_KEY= in .env"        '^API_KEY='                    ".env,.env.*" "__pycache__"
scan_pattern "Hardcoded TOKEN= in .env"          '^TOKEN='                      ".env,.env.*" "__pycache__"

echo ""
echo "═══ SCAN COMPLETE ═══"
echo "Total leaks found: $TOTAL_LEAKS"

if [ "$TOTAL_LEAKS" -gt 0 ]; then
  exit 1
fi
exit 0
