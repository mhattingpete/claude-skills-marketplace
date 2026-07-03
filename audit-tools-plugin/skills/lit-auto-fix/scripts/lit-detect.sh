#!/usr/bin/env bash
# Consolidated Lit anti-pattern detection — run from project root (e.g. widget/)
set -euo pipefail

SRC=${1:-src}
ONLY=${2:-}  # optional pattern number (1-8)

p() {
  local n=$1 label=$2 cmd=$3
  if [ -n "$ONLY" ] && [ "$ONLY" != "$n" ]; then return; fi
  echo "=== P$n: $label ==="
  eval "$cmd" || true
  echo ""
}

p 1 'Buttons missing type=button' \
  "grep -rn '<button[^>]*>' \"$SRC\" --include='*.ts' | grep -v 'type=\"button\"' | grep -v 'type=' | grep -v '\.css\`' | grep -v 'NodeListOf' || echo 'NONE'"

p 2 'querySelector on renderRoot' \
  "grep -rn 'renderRoot\.querySelector\|shadowRoot\.querySelector' \"$SRC\" --include='*.ts' || echo 'NONE'"

p 3 'HTML generation without unsafeHTML import' \
  'for f in $(grep -rl "_renderMarkdown\|innerHTML" "$SRC" --include="*.ts" 2>/dev/null); do
    grep -q "unsafeHTML" "$f" 2>/dev/null || echo "MISSING: $f"
  done; echo "NONE"'

p 4 'Object/Array @property missing attribute:false' \
  "grep -rn '@property({ type: Object\|@property({ type: Array' \"$SRC\" --include='*.ts' | grep -v 'attribute: false' | grep -v 'attribute:false' || echo 'NONE'"

p 5 'Lifecycle missing super call' \
  'for f in $(grep -rl "connectedCallback\|disconnectedCallback" "$SRC" --include="*.ts" 2>/dev/null); do
    grep -q "connectedCallback" "$f" && ! grep -q "super.connectedCallback" "$f" && echo "connected: $f" || true
    grep -q "disconnectedCallback" "$f" && ! grep -q "super.disconnectedCallback" "$f" && echo "disconnected: $f" || true
  done; echo "NONE"'

p 6 'Listener leak (add > remove count)' \
  'for f in $(grep -rl "addEventListener" "$SRC" --include="*.ts" 2>/dev/null); do
    add=$(grep -c "addEventListener" "$f" || echo 0)
    rmv=$(grep -c "removeEventListener" "$f" || echo 0)
    [ "$add" -gt "$rmv" ] && echo "LEAK: $f ($add add, $rmv remove)" || true
  done; echo "NONE"'

p 7 'Redundant requestUpdate calls' \
  'for f in $(grep -rl "requestUpdate(" "$SRC" --include="*.ts" 2>/dev/null); do
    props=$(grep -c "@property\|@state" "$f" || echo 0)
    calls=$(grep -c "requestUpdate(" "$f" || echo 0)
    echo "  $f ($props props, $calls requestUpdate)"
  done; echo "NONE"'

p 8 'Interactive elements missing role/aria' \
  "grep -rn '@click\|tabindex=\"0\"' \"$SRC\" --include='*.ts' | grep -v 'role=' | grep -v 'aria-label' | grep -v 'aria-' | grep -v '\.css\`' || echo 'NONE'"
