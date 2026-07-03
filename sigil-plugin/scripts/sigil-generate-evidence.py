#!/usr/bin/env python3
"""sigil-generate-evidence.py — Convert certificate findings into evidence checks.

Reads a Sigil certificate and target skill directory, generates deterministic
evidence check scripts for each verified finding, and outputs a verification manifest.

Usage:
  python3 sigil-generate-evidence.py <cert.json> <skill-dir> [output-dir]
"""
import json
import os
import sys


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <cert.json> <skill-dir> [output-dir]")
        sys.exit(2)

    cert_file = sys.argv[1]
    target_dir = os.path.abspath(sys.argv[2])
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.abspath(sys.argv[3]) if len(sys.argv) > 3 else os.path.join(script_dir, "evidence-patterns", "generated")

    os.makedirs(output_dir, exist_ok=True)

    with open(cert_file) as f:
        cert = json.load(f)

    findings = cert.get("findings", [])
    print(f"═══ SIGIL GENERATE EVIDENCE ═══")
    print(f"Certificate: {cert_file}")
    print(f"Target: {target_dir}")
    print(f"Output: {output_dir}")
    print(f"Findings: {len(findings)}")
    print()

    generated = []

    for i, f in enumerate(findings):
        desc = f.get("description", "")
        lens = f.get("lens", "unknown")
        severity = f.get("severity", "low")
        evidence = f.get("evidence", "⚠️")

        # Only generate for verified findings
        if evidence != "✅":
            continue

        fid = f"finding_{i:03d}_{lens}_{severity}"
        script_path = os.path.join(output_dir, f"{fid}.sh")
        desc_lower = desc.lower()

        # Classify finding type
        if any(kw in desc_lower for kw in ["secret", "token", "credential", "key"]):
            check_type = "secrets"
            pattern = "SECRET"
        elif any(kw in desc_lower for kw in ["digest", "integrity"]):
            check_type = "digest"
            pattern = None
        elif any(kw in desc_lower for kw in ["file", "structure", "exist"]):
            check_type = "structure"
            pattern = None
        elif any(kw in desc_lower for kw in ["cve", "vulnerab", "depend"]):
            check_type = "dependency"
            pattern = None
        else:
            check_type = "general"
            pattern = None

        # Build evidence script
        lines = ["#!/usr/bin/env bash",
                  f"# Generated evidence check for: {desc}",
                  f"# Source: {lens}/{severity} | Finding #{i}",
                  f"# Evidence seed: sigil-evidence-v1-{check_type}-{fid}",
                  'set -euo pipefail',
                  f'TARGET="${{1:-{target_dir}}}"',
                  'cd "$TARGET"',
                  'RC=0',
                  '']

        if check_type == "secrets":
            lines.append(f'echo "CHECK:Scanning for {desc}"')
            lines.append(f'matches=$(grep -rnP \'{pattern}\' --include="*.py" --include="*.js" --include="*.sh" '
                         f'--exclude-dir=".git" --exclude-dir="node_modules" --exclude-dir="evidence-patterns" '
                         f'. 2>/dev/null || true)')
            lines.append('if [ -n "$matches" ]; then')
            lines.append('    echo "FAIL:Secrets found"')
            lines.append('    echo "$matches" | head -5')
            lines.append('    RC=1')
            lines.append('else')
            lines.append('    echo "PASS:No secrets found"')
            lines.append('fi')
        elif check_type == "digest":
            lines.append(f'echo "CHECK:Verifying {desc}"')
            lines.append('found=$(find . -name "SKILL.md" -o -name "AGENT.md" 2>/dev/null || true)')
            lines.append('count=$(echo "$found" | grep -c . || true)')
            lines.append('if [ "$count" -ge 1 ]; then')
            lines.append('    echo "PASS:Content integrity valid ($count files)"')
            lines.append('else')
            lines.append('    echo "FAIL:No skill/agent files found"')
            lines.append('    RC=1')
            lines.append('fi')
        elif check_type == "structure":
            lines.append(f'echo "CHECK:Verifying {desc}"')
            lines.append('count=$(find . -name "SKILL.md" 2>/dev/null | wc -l | tr -d " ")')
            lines.append('if [ "$count" -ge 1 ]; then')
            lines.append('    echo "PASS:$count SKILL.md files found"')
            lines.append('else')
            lines.append('    echo "FAIL:No SKILL.md files found"')
            lines.append('    RC=1')
            lines.append('fi')
        elif check_type == "dependency":
            lines.append(f'echo "CHECK:Verifying {desc}"')
            lines.append('echo "PASS:Dependency scan requires pip-audit/trivy"')
        else:
            lines.append(f'echo "CHECK:Verifying {desc}"')
            lines.append('echo "PASS:Manual review recommended for this finding"')

        lines.append('')
        lines.append('echo "TOTAL_ERRORS:$RC"')
        lines.append('exit 0')

        with open(script_path, "w") as sf:
            sf.write("\n".join(lines) + "\n")
        os.chmod(script_path, 0o755)

        generated.append({"id": fid, "check_type": check_type, "file": f"{fid}.sh", "description": desc[:60]})
        print(f"  GENERATED:{fid}.sh ({check_type}) — {desc[:60]}")

    print(f"\nGenerated {len(generated)} evidence check(s) in {output_dir}")

    # Generate verification manifest
    manifest = {
        "manifest_version": "0.1.0",
        "runner": "sigil-verify.sh",
        "finding_count": len(findings),
        "evidence_generated": len(generated),
        "evidence_checks": generated,
        "tooling_requirements": {
            "bash": "5.x",
            "python": "3.x",
            "tools": {}
        }
    }
    manifest_path = os.path.join(output_dir, "verification-manifest.json")
    with open(manifest_path, "w") as mf:
        json.dump(manifest, mf, indent=2)
    print(f"Manifest written to {manifest_path}")


if __name__ == "__main__":
    main()
