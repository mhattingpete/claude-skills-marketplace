#!/usr/bin/env bash
# version.sh — Single source of truth for plugin version
# All version info derives from VERSION file at plugin root
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"
VERSION_FILE="$PLUGIN_DIR/VERSION"

if [ ! -f "$VERSION_FILE" ]; then
  echo "ERROR: VERSION file not found at $VERSION_FILE" >&2
  exit 1
fi

PLUGIN_VERSION=$(cat "$VERSION_FILE" | tr -d '[:space:]')

case "${1:-}" in
  --plugin-json)
    # Verify plugin.json matches VERSION
    PLUGIN_JSON_VERSION=$(python3 -c "import json; f=open('$PLUGIN_DIR/.claude-plugin/plugin.json'); d=json.load(f); print(d['version'])" 2>/dev/null || echo "MISMATCH")
    if [ "$PLUGIN_JSON_VERSION" != "$PLUGIN_VERSION" ]; then
      echo "MISMATCH: VERSION says $PLUGIN_VERSION, plugin.json says $PLUGIN_JSON_VERSION" >&2
      exit 1
    fi
    echo "$PLUGIN_VERSION"
    ;;
  --check)
    if echo "$PLUGIN_VERSION" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+$'; then
      echo "OK $PLUGIN_VERSION"
    else
      echo "INVALID: $PLUGIN_VERSION (expected semver)" >&2
      exit 1
    fi
    ;;
  *)
    echo "$PLUGIN_VERSION"
    ;;
esac
