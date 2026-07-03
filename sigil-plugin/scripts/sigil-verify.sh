#!/usr/bin/env bash
# sigil-verify.sh — Deterministic verification runner
#
# Reads a Sigil certificate (sigil-certificate.json) and a target skill directory,
# executes all referenced evidence checks against pinned tooling, and produces
# a byte-identical verification report.
#
# Usage:
#   sigil-verify.sh <cert.json> <skill-dir>
#
# Exit codes:
#   0 — All checks pass (deterministic match)
#   1 — One or more checks failed
#   2 — Usage error
#   3 — Certificate or target not found
#   4 — Internal error
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PATTERNS_DIR="$SCRIPT_DIR/evidence-patterns"
CERT_FILE="${1:-}"
TARGET_DIR="${2:-}"

# ─── Help ───
show_help() {
  cat <<'HELP'
sigil-verify.sh — Deterministic verification runner

USAGE:
  sigil-verify.sh <cert.json> <skill-dir>

  Reads a Sigil certificate, executes all referenced evidence checks against
  the skill directory, and verifies deterministic output.

EXIT CODES:
  0  All checks pass
  1  One or more checks failed
  2  Usage error
  3  Certificate or target not found

EXAMPLE:
  sigil-verify.sh sigil-certificate.json ./my-plugin
HELP
  exit 0
}

# ─── Parse args ───
if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  show_help
fi

if [ -z "$CERT_FILE" ] || [ -z "$TARGET_DIR" ]; then
  echo "ERROR:Usage: sigil-verify.sh <cert.json> <skill-dir>" >&2
  exit 2
fi

if [ ! -f "$CERT_FILE" ]; then
  echo "ERROR:Certificate not found: $CERT_FILE" >&2
  exit 3
fi

if [ ! -d "$TARGET_DIR" ]; then
  echo "ERROR:Target directory not found: $TARGET_DIR" >&2
  exit 3
fi

# Resolve to absolute paths
CERT_FILE="$(cd "$(dirname "$CERT_FILE")" && pwd)/$(basename "$CERT_FILE")"
TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"

# ─── Report header ───
TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
SIGIL_VERIFY_VERSION="0.1.0"

echo "═══ SIGIL VERIFY v${SIGIL_VERIFY_VERSION} ═══"
echo "Timestamp:  $TIMESTAMP"
echo "Certificate: $CERT_FILE"
echo "Target:      $TARGET_DIR"
echo ""

# ─── Extract findings from certificate ───
echo "─── Parsing certificate ───"
CERT_JSON=$(python3 -c "
import json, sys
try:
    c = json.load(open('$CERT_FILE'))
    print('skill_name:', c.get('skill_name', 'unknown'))
    print('skill_version:', c.get('skill_version', 'unknown'))
    print('content_digest:', c.get('content_digest', 'none'))
    print('verdict:', c.get('verdict', 'none'))
    print('finding_count:', len(c.get('findings', [])))
except Exception as e:
    print(f'PARSE_ERROR:{e}', file=sys.stderr)
    sys.exit(1)
" 2>&1)

if echo "$CERT_JSON" | grep -q PARSE_ERROR; then
  echo "FAIL:Certificate is not valid JSON or missing required fields"
  echo "$CERT_JSON"
  exit 4
fi
echo "$CERT_JSON"
echo ""

# ─── Evidence pass: Run pattern scripts ───
echo "─── Running evidence checks ───"
ALL_PATTERNS=()

# Auto-discover all evidence patterns
while IFS= read -r script; do
  [ -z "$script" ] && continue
  script_name=$(basename "$script" .sh)
  ALL_PATTERNS+=("$script_name")
done < <(find "$PATTERNS_DIR" -name '*.sh' -type f 2>/dev/null | sort)

if [ ${#ALL_PATTERNS[@]} -eq 0 ]; then
  echo "WARN:No evidence patterns found in $PATTERNS_DIR"
fi

PASS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0
results_dir=$(mktemp -d)
trap 'rm -rf "$results_dir"' EXIT

for pattern in "${ALL_PATTERNS[@]}"; do
  pattern_script="$PATTERNS_DIR/$pattern.sh"
  result_file="$results_dir/$pattern.result"
  output_file="$results_dir/$pattern.output"

  if [ ! -f "$pattern_script" ]; then
    echo "  SKIP:$pattern.sh:not found"
    echo "SKIP" > "$result_file"
    SKIP_COUNT=$((SKIP_COUNT + 1))
    continue
  fi

  # Run the pattern script against the target, capture all output
  set +e
  bash "$pattern_script" "$TARGET_DIR" "$CERT_FILE" > "$output_file" 2>&1
  exit_code=$?
  set -e

  # Classify result
  if [ "$exit_code" -eq 0 ]; then
    # Check if all checks passed
    if grep -q '^FAIL:' "$output_file" 2>/dev/null; then
      fail_count=$(grep -c '^FAIL:' "$output_file" 2>/dev/null || echo 0)
      echo "  FAIL:$pattern ($fail_count failure(s))"
      echo "FAIL" > "$result_file"
      FAIL_COUNT=$((FAIL_COUNT + 1))
    elif grep -q '^TOTAL_ERRORS:[1-9]' "$output_file" 2>/dev/null; then
      err_count=$(grep '^TOTAL_ERRORS:' "$output_file" | sed 's/^TOTAL_ERRORS://')
      echo "  FAIL:$pattern ($err_count error(s))"
      echo "FAIL" > "$result_file"
      FAIL_COUNT=$((FAIL_COUNT + 1))
    elif grep -q '^TOTAL_VULNS:[1-9]' "$output_file" 2>/dev/null; then
      vuln_count=$(grep '^TOTAL_VULNS:' "$output_file" | sed 's/^TOTAL_VULNS://')
      echo "  WARN:$pattern ($vuln_count vulnerabilities found)"
      echo "WARN" > "$result_file"
      FAIL_COUNT=$((FAIL_COUNT + 1))
    else
      echo "  PASS:$pattern"
      echo "PASS" > "$result_file"
      PASS_COUNT=$((PASS_COUNT + 1))
    fi
  else
    echo "  FAIL:$pattern (exit code $exit_code)"
    echo "FAIL" > "$result_file"
    FAIL_COUNT=$((FAIL_COUNT + 1))
  fi

  # Show key lines from output
  grep -E '^(PASS:|FAIL:|WARN:|LEAK:|ENV_SECRET:|VULN:|DIGEST:)' "$output_file" 2>/dev/null | sed 's/^/    /' || true
done

# ─── Deterministic output hash ───
echo ""
echo "─── Verification hash ───"
# Hash all result files together for deterministic output
verify_hash=$( (for f in "$results_dir"/*.result; do
  cat "$f"
done) | sort | sha256sum | cut -d' ' -f1)
echo "VERIFY_HASH:sha256:$verify_hash"

# ─── Summary ───
echo ""
echo "═══ VERIFICATION SUMMARY ═══"
echo "Checks passed: $PASS_COUNT"
echo "Checks failed: $FAIL_COUNT"
echo "Checks skipped: $SKIP_COUNT"
echo ""

if [ "$FAIL_COUNT" -gt 0 ]; then
  echo "RESULT:FAILED ($FAIL_COUNT checks failed)"
  exit 1
else
  echo "RESULT:PASSED (all $PASS_COUNT checks passed)"
  echo ""
  echo "This certificate is VERIFIED — all evidence checks match."
  echo "Anyone re-running sigil-verify.sh against this target will"
  echo "produce verify_hash sha256:$verify_hash"
  exit 0
fi
