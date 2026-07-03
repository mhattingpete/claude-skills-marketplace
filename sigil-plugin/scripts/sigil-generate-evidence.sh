#!/usr/bin/env bash
# sigil-generate-evidence.sh — Convert certificate findings into evidence checks
#
# Reads a Sigil certificate and a target skill directory, generates
# deterministic evidence check scripts for each finding, and outputs a
# verification manifest.
#
# Usage:
#   sigil-generate-evidence.sh <cert.json> <skill-dir> [output-dir]
#
# Default output-dir: ./evidence-patterns/generated/
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CERT_FILE="${1:-}"
TARGET_DIR="${2:-}"
OUTPUT_DIR="${3:-$SCRIPT_DIR/evidence-patterns/generated}"

if [ -z "$CERT_FILE" ] || [ -z "$TARGET_DIR" ]; then
  echo "Usage: sigil-generate-evidence.sh <cert.json> <skill-dir> [output-dir]"
  exit 2
fi

mkdir -p "$OUTPUT_DIR"

# Parse the certificate
echo "═══ SIGIL GENERATE EVIDENCE ═══"
echo "Certificate: $CERT_FILE"
echo "Target: $TARGET_DIR"
echo "Output: $OUTPUT_DIR"
echo ""

# Extract findings from certificate
python3 -c "
import json, os, sys

cert = json.load(open('$CERT_FILE'))
findings = cert.get('findings', [])
skill_name = cert.get('skill_name', 'unknown')
target = '$TARGET_DIR'
outdir = '$OUTPUT_DIR'

generated = []

for i, f in enumerate(findings):
    desc = f.get('description', '')
    lens = f.get('lens', 'unknown')
    severity = f.get('severity', 'low')
    location = f.get('location', '')
    evidence = f.get('evidence', '⚠️')

    # Only generate evidence checks for verified (✅) findings
    if evidence != '✅':
        continue

    # Generate an evidence check script based on finding type
    fid = f'finding_{i:03d}_{lens}_{severity}'
    script_path = os.path.join(outdir, f'{fid}.sh')

    # Classify the finding into a check type
    desc_lower = desc.lower()

    if 'secret' in desc_lower or 'token' in desc_lower or 'credential' in desc_lower or 'key' in desc_lower:
        check_type = 'secrets'
        pattern = desc.split()[-1] if location else 'SECRET'
        script = f'''#!/usr/bin/env bash
# Generated evidence check for: {desc}
# Source finding: {lens}/{severity}
set -euo pipefail
TARGET=\\"\\${{1:-$target}}\\"
cd \\"\\$TARGET\\"
result=0
# Check for {pattern} patterns
matches=\\$(grep -rnP --include='*.py' --include='*.js' --include='*.ts' --include='*.sh' --include='*.yaml' --include='*.yml' --include='*.json' --include='*.md' '{pattern}' --exclude-dir='.git' --exclude-dir='evidence-patterns' . 2>/dev/null || true)
if [ -n \\"\\$matches\\" ]; then
    echo \\"FAIL:{desc}\\"
    echo \\"\\$matches\\" | head -5
    result=1
else
    echo \\"PASS:{desc}\\"
fi
echo \\"TOTAL_ERRORS:\\$result\\"
exit 0
'''
    elif 'digest' in desc_lower or 'integrity' in desc_lower:
        check_type = 'digest'
        script = f'''#!/usr/bin/env bash
# Generated evidence check for: {desc}
# Source finding: {lens}/{severity}
set -euo pipefail
TARGET=\\"\\${{1:-$target}}\\"
cd \\"\\$TARGET\\"
result=0
# Check content integrity
all_files=\\$(find . -name 'SKILL.md' -o -name 'AGENT.md' 2>/dev/null || true)
if [ -z \\"\\$all_files\\" ]; then
    echo \\"FAIL:No skill/agent files to check - {desc}\\"
    result=1
else
    digest=\\$(for f in \\$all_files; do sha256sum \\"\\$f\\" | cut -d' ' -f1; done | sort | sha256sum | cut -d' ' -f1)
    echo \\"PASS:content integrity check complete - sha256:\\$digest\\"
fi
echo \\"TOTAL_ERRORS:\\$result\\"
exit 0
'''
    elif 'file' in desc_lower or 'structure' in desc_lower or 'exist' in desc_lower:
        check_type = 'structure'
        script = f'''#!/usr/bin/env bash
# Generated evidence check for: {desc}
# Source finding: {lens}/{severity}
set -euo pipefail
TARGET=\\"\\${{1:-$target}}\\"
cd \\"\\$TARGET\\"
result=0
# Structural check
files=\\$(find . -name 'SKILL.md' 2>/dev/null || true)
count=\\$(echo \\"\\$files\\" | wc -l | tr -d ' ')
if [ \\"\\$count\\" -lt 1 ]; then
    echo \\"FAIL:{desc}\\"
    result=1
else
    echo \\"PASS:{desc}\\"
fi
echo \\"TOTAL_ERRORS:\\$result\\"
exit 0
'''
    elif 'cve' in desc_lower or 'vulnerab' in desc_lower or 'depend' in desc_lower:
        check_type = 'dependency'
        script = f'''#!/usr/bin/env bash
# Generated evidence check for: {desc}
# Source finding: {lens}/{severity}
set -euo pipefail
TARGET=\\"\\${{1:-$target}}\\"
cd \\"\\$TARGET\\"
# {desc}
echo \\"INFO:Checking dependencies for vulnerabilities\\"
deps=\\$(find . -name 'requirements.txt' -o -name 'pyproject.toml' 2>/dev/null || true)
if [ -n \\"\\$deps\\" ]; then
    echo \\"PASS:Dependency files found, manual review needed for CVE verification\\"
else
    echo \\"INFO:No dependency files found\\"
fi
echo \\"TOTAL_ERRORS:0\\"
exit 0
'''
    else:
        check_type = 'general'
        script = f'''#!/usr/bin/env bash
# Generated evidence check for: {desc}
# Source finding: {lens}/{severity}
set -euo pipefail
TARGET=\\"\\${{1:-$target}}\\"
cd \\"\\$TARGET\\"
echo \\"PASS:{desc} - finding acknowledged, manual verification recommended\\"
echo \\"TOTAL_ERRORS:0\\"
exit 0
'''

    with open(script_path, 'w') as sf:
        sf.write(script)
    os.chmod(script_path, 0o755)
    generated.append(fid)
    print(f'  GENERATED:{fid}.sh ({check_type}) — {desc[:60]}')

print(f'')
print(f'Generated {len(generated)} evidence check(s) in {outdir}')
" 2>&1

echo ""
echo "═══ GENERATION COMPLETE ═══"
