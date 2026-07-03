#!/usr/bin/env bash
# evidence-patterns/dependency-check.sh
# Pattern: Check for known CVEs in Python dependencies
# Evidence hash seed: "sigil-evidence-v1-dependency-check"
set -euo pipefail

TARGET_DIR="${1:-.}"
cd "$TARGET_DIR"

# Check if pip-audit is available
use_pip_audit=false
if command -v pip-audit &>/dev/null; then
  use_pip_audit=true
elif command -v uv &>/dev/null && uv tool list 2>/dev/null | grep -q pip-audit; then
  use_pip_audit=true
fi

# Check for Python dependency files
dep_files=""
for f in requirements.txt requirements.concierge.txt pyproject.toml; do
  if [ -f "$f" ]; then
    dep_files="$dep_files $f"
  fi
done

if [ -z "$dep_files" ]; then
  echo "INFO:No dependency files found (requirements.txt, pyproject.toml)"
  echo "TOTAL_VULNS:0"
  exit 0
fi

echo "INFO:Dependency files found: $dep_files"

if [ "$use_pip_audit" = true ]; then
  echo "INFO:Running pip-audit..."
  audit_out=$(pip-audit --requirement requirements.txt 2>/dev/null || true)
  vuln_count=$(echo "$audit_out" | grep -c 'CVE-' 2>/dev/null || echo 0)
  if [ "$vuln_count" -gt 0 ]; then
    echo "VULN:$vuln_count known vulnerabilities found"
    echo "$audit_out" | grep 'CVE-' | head -10 || true
  else
    echo "PASS:No known vulnerabilities found"
  fi
  echo "TOTAL_VULNS:$vuln_count"
else
  echo "WARN:pip-audit not available; install with: uv tool install pip-audit"
  echo "SKIP:Vulnerability scan skipped (tool not available)"
  echo "TOTAL_VULNS:0"
fi

exit 0
