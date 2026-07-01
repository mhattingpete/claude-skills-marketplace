#!/usr/bin/env bash
# pain-trend-diff.sh — Convenience wrapper for pain-trend-diff.py
#
# Usage:
#   ./scripts/pain-trend-diff.sh                    # uses reddit-pain-state.json in current dir
#   ./scripts/pain-trend-diff.sh path/to/state.json
#   ./scripts/pain-trend-diff.sh --json
#   ./scripts/pain-trend-diff.sh path/to/state.json --json --runs 1 2

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/pain-trend-diff.py"

# Find the state file
STATE_FILE=""
ARGS=()

for arg in "$@"; do
  if [[ "$arg" == *.json ]]; then
    STATE_FILE="$arg"
  else
    ARGS+=("$arg")
  fi
done

# Default state file: check cwd, then sigil-plugin root
if [[ -z "$STATE_FILE" ]]; then
  if [[ -f "reddit-pain-state.json" ]]; then
    STATE_FILE="reddit-pain-state.json"
  elif [[ -f "$SCRIPT_DIR/../reddit-pain-state.json" ]]; then
    STATE_FILE="$SCRIPT_DIR/../reddit-pain-state.json"
  else
    echo "Error: no state file found. Pass the path or run from sigil-plugin root." >&2
    exit 1
  fi
fi

echo "State file: $STATE_FILE" >&2
exec python3 "$PYTHON_SCRIPT" "$STATE_FILE" "${ARGS[@]}"
