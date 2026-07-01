#!/usr/bin/env bash
# pain-trend-diff.sh — Convenience wrapper for pain-trend-diff.py
#
# Default state file location: sigil-plugin root (alongside the skill).
# Use --json for programmatic output.
#
# Usage:
#   ./scripts/pain-trend-diff.sh                    # uses sigil-plugin/reddit-pain-state.json
#   ./scripts/pain-trend-diff.sh path/to/state.json
#   ./scripts/pain-trend-diff.sh --json

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/pain-trend-diff.py"

# Resolve plugin root: scripts/ is at sigil-plugin root
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DEFAULT_STATE="$PLUGIN_ROOT/reddit-pain-state.json"

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

# Default: plugin root
if [[ -z "$STATE_FILE" ]]; then
  if [[ -f "$DEFAULT_STATE" ]]; then
    STATE_FILE="$DEFAULT_STATE"
  else
    echo "Error: no state file found. Expected at: $DEFAULT_STATE" >&2
    exit 1
  fi
fi

echo "State file: $STATE_FILE" >&2
exec python3 "$PYTHON_SCRIPT" "$STATE_FILE" "${ARGS[@]}"
