#!/usr/bin/env bash
# scan-skill.sh — Pattern Library scanner
#
# Reads the pattern registry (patterns/registry.jsonl) and runs every
# detection signature against the target directory. Reports matches per
# pattern with file paths, line numbers, and matched text.
#
# Usage:
#   ./scripts/scan-skill.sh <target-dir>          # scan all patterns
#   ./scripts/scan-skill.sh <target-dir> --drift   # only config-drift pattern
#   ./scripts/scan-skill.sh <target-dir> --silent  # exit 0/1, no verbose output
#   ./scripts/scan-skill.sh <target-dir> --json    # machine-readable JSON output
#
# Exit codes:
#   0 = no patterns detected
#   1 = one or more patterns detected
#   2 = usage error or registry not found

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"
REGISTRY="${PLUGIN_DIR}/patterns/registry.jsonl"
TARGET="${1:?Usage: scan-skill.sh <target-dir> [--drift|--silent|--json]}"
MODE="${2:-all}"
SILENT=false
JSON_MODE=false
MATCHES=0

if [ "$MODE" = "--silent" ]; then
  MODE="all"
  SILENT=true
elif [ "$MODE" = "--drift" ]; then
  PATTERN_FILTER="config-drift"
elif [ "$MODE" = "--json" ]; then
  MODE="all"
  JSON_MODE=true
  SILENT=true
fi

if [ ! -f "$REGISTRY" ]; then
  echo "ERROR: Pattern registry not found at $REGISTRY" >&2
  exit 2
fi

if [ ! -d "$TARGET" ]; then
  echo "ERROR: Target directory not found: $TARGET" >&2
  exit 2
fi

JSON_TMP=$(mktemp)
trap 'rm -f "$JSON_TMP"' EXIT

if ! $SILENT; then
  echo "═══ Pattern Library Scan ═══"
  echo "Registry: $REGISTRY"
  echo "Target:   $TARGET"
  echo "Mode:     ${PATTERN_FILTER:-all patterns}"
  echo ""
fi

while IFS= read -r line; do
  [ -z "$line" ] && continue
  [ "${line:0:1}" != "{" ] && continue

  PATTERN_ID=$(echo "$line" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['pattern_id'])" 2>/dev/null || echo "")
  PATTERN_NAME=$(echo "$line" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['name'])" 2>/dev/null || echo "")
  SEVERITY=$(echo "$line" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['severity'])" 2>/dev/null || "")
  SIGNATURE_COUNT=$(echo "$line" | python3 -c "import sys,json; print(len(json.loads(sys.stdin.read())['detection']['signatures']))" 2>/dev/null || echo "0")

  [ -n "${PATTERN_FILTER:-}" ] && [ "$PATTERN_ID" != "$PATTERN_FILTER" ] && continue

  if ! $SILENT; then
    echo "─ $PATTERN_NAME (${SEVERITY})"
  fi

  PATTERN_MATCHES=0

  for i in $(seq 0 $((SIGNATURE_COUNT - 1))); do
    SEARCH=$(echo "$line" | python3 -c "
import sys, json
p=json.loads(sys.stdin.read())
s=p['detection']['signatures'][$i]
print(s.get('search',''))
" 2>/dev/null || echo "")
    CONTEXT=$(echo "$line" | python3 -c "
import sys, json
p=json.loads(sys.stdin.read())
s=p['detection']['signatures'][$i]
print(s.get('context',''))
" 2>/dev/null || echo "")
    STYPE=$(echo "$line" | python3 -c "
import sys, json
p=json.loads(sys.stdin.read())
s=p['detection']['signatures'][$i]
print(s.get('type','regex'))
" 2>/dev/null || echo "")

    [ -z "$SEARCH" ] && continue

    FILE_PATTERNS=$(echo "$line" | python3 -c "
import sys, json
ps=json.loads(sys.stdin.read())['detection']['file_patterns']
for p in ps: print(p)
" 2>/dev/null || echo "")

    FIND_CMD="find \"$TARGET\" -type f"
    while IFS= read -r fp; do
      [ -z "$fp" ] && continue
      FIND_CMD+=" -name \"$fp\" -o"
    done <<< "$FILE_PATTERNS"
    FIND_CMD="${FIND_CMD% -o}"

    if [ "$STYPE" = "regex" ] || [ "$STYPE" = "grep" ]; then
      GREP_RESULT=$(eval "$FIND_CMD" 2>/dev/null | head -200 | xargs grep -n "$SEARCH" 2>/dev/null || true)
    else
      GREP_RESULT=$(eval "$FIND_CMD" 2>/dev/null | head -200 | xargs grep -n "$SEARCH" 2>/dev/null || true)
    fi

    HIT_COUNT=$(echo "$GREP_RESULT" | grep -c "." 2>/dev/null || true)

    if [ "$HIT_COUNT" -gt 0 ]; then
      PATTERN_MATCHES=$((PATTERN_MATCHES + HIT_COUNT))
      if ! $SILENT; then
        echo "  [DETECTED] $CONTEXT ($HIT_COUNT hits)"
        echo "$GREP_RESULT" | head -10 | while IFS=: read -r file line rest; do
          echo "    $file:$line"
        done
        TOTAL_HITS=$(echo "$GREP_RESULT" | grep -c "." 2>/dev/null || true)
        if [ "$TOTAL_HITS" -gt 10 ]; then
          echo "    ... and $((TOTAL_HITS - 10)) more matches"
        fi
      fi
    else
      if ! $SILENT; then
        echo "  [CLEAN] $CONTEXT — no matches found"
      fi
    fi
  done

  MATCHES=$((MATCHES + PATTERN_MATCHES))

  if ! $SILENT; then
    if [ "$PATTERN_MATCHES" -eq 0 ]; then
      echo "  → PASS: No ${PATTERN_NAME} patterns detected"
    else
      echo "  → FAIL: ${PATTERN_NAME} patterns FOUND ($PATTERN_MATCHES matches)"
    fi
    echo ""
  fi

  if $JSON_MODE && [ "$PATTERN_MATCHES" -gt 0 ]; then
    echo '{"pattern_id":"'"$PATTERN_ID"'","pattern_name":"'"$PATTERN_NAME"'","severity":"'"$SEVERITY"'","match_count":'"$PATTERN_MATCHES"'}' >> "$JSON_TMP"
  fi

done < "$REGISTRY"

if $JSON_MODE; then
  python3 -c "
import json
patterns = []
try:
  with open('$JSON_TMP') as f:
    for line in f:
      line = line.strip()
      if line:
        patterns.append(json.loads(line))
except FileNotFoundError:
  pass
print(json.dumps({'total_matches': $MATCHES, 'patterns': patterns}, indent=2))
"
elif ! $SILENT; then
  echo "═══ Scan Complete ═══"
  if [ "$MATCHES" -eq 0 ]; then
    echo "Result: PASS — no known antipatterns detected"
  else
    echo "Result: FAIL — $MATCHES antipattern matches found — review and remediate"
  fi
fi

exit $(( MATCHES > 0 ? 1 : 0 ))
