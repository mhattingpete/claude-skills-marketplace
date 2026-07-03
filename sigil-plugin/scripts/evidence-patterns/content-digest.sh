#!/usr/bin/env bash
# evidence-patterns/content-digest.sh
# Pattern: Verify content digest matches actual files
# Evidence hash seed: "sigil-evidence-v1-content-digest"
set -euo pipefail

TARGET_DIR="${1:-.}"
CERT_FILE="${2:-}"
cd "$TARGET_DIR"

if [ -z "$CERT_FILE" ] || [ ! -f "$CERT_FILE" ]; then
  echo "INFO:No certificate provided, computing digest only"
else
  # Extract expected digest from certificate
  expected_digest=$(python3 -c "import json; c=json.load(open('$CERT_FILE')); print(c.get('content_digest',''))" 2>/dev/null || echo "")
  if [ -z "$expected_digest" ]; then
    echo "FAIL:certificate has no content_digest field"
    exit 1
  fi
fi

# Compute actual digest of all SKILL.md + agent files
all_files=""
if [ -d skills ]; then
  all_files="$all_files $(find skills -name 'SKILL.md' -type f 2>/dev/null || true)"
fi
if [ -d agents ]; then
  all_files="$all_files $(find agents -name 'AGENT.md' -type f 2>/dev/null || true)"
fi

if [ -z "$all_files" ]; then
  echo "FAIL:no skill or agent files found to digest"
  exit 1
fi

# Compute sha256 over sorted, concatenated file contents
actual_digest=$(for f in $all_files; do sha256sum "$f" | cut -d' ' -f1; done | sort | sha256sum | cut -d' ' -f1)
echo "DIGEST:sha256:$actual_digest"

if [ -n "${expected_digest:-}" ]; then
  if [ "sha256:$actual_digest" = "$expected_digest" ]; then
    echo "PASS:content digest matches certificate"
  else
    echo "FAIL:content digest mismatch (expected: $expected_digest, actual: sha256:$actual_digest)"
    exit 1
  fi
fi

exit 0
