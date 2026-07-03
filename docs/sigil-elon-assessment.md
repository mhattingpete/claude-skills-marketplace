# Elon Musk First-Principles Assessment: Sigil Verification Protocol

**Date:** 2026-06-30
**Lens:** CEO/Strategy — Adversarial First-Principles (Elon Musk framing)

---

## Verdict Summary

| Dimension | Grade | Why |
|-----------|-------|-----|
| Core insight direction | B+ | "Deterministic > AI opinion" is right, but the unit of value is misidentified |
| Build quality vs insight | D | Protocol claims determinism but has a timestamp in its own output |
| Defensibility | F | 6 bash scripts is not a moat — anyone can write grep wrappers |
| Product-market fit | D | One persona (skill author marketing badge), $0 price point |
| 10x potential | B | Behavioral verification is real and valuable — but wasn't built |

---

## Key Findings

### 1. The "deterministic" claim is false by design

`sigil-verify.sh` outputs a timestamp on every run: `date -u +%Y-%m-%dT%H:%M:%SZ`. The stdout (what humans read) is non-deterministic. The verification hash at the end hashes result files — but the timestamp is in the human-readable output. This is a first-order bug.

`dependency-check.sh` silently PASSES when `pip-audit` isn't installed. A verification protocol that produces "PASS" when the tool is missing is worse than no check — it creates the illusion of security.

### 2. 6 patterns is not a library — it's 6 grep commands

- `file-structure` — "does plugin.json exist?" is trivially checkable by any human
- `frontmatter-valid` — a Markdown linter rule, not evidence
- `version-consistency` — if VERSION doesn't match plugin.json, that's a doc bug, not a trust issue
- `dependency-check` — silently passes when pip-audit missing (actively dangerous)

Only `secrets-check` (gitleaks derivative) and `content-digest` (tamper evidence) add real value.

### 3. The evidence generator is keyword matching on LLM output

`sigil-generate-evidence.py` classifies findings by checking description text for keywords like "secret", "token", "credential". This pipes the output of a non-deterministic system (AI findings) into a script that tries to produce deterministic checks. For non-secret findings, it generates:
```bash
echo "PASS:Manual review recommended for this finding"
exit 0
```
This is not evidence. It's a TODO comment.

### 4. The "Dockerized runner" from the 360 report was not built

The recommendation was: "A Dockerized CLI that executes every script against pinned tooling." What was built is `sigil-verify.sh` — a bash script running whatever tools happen to be on the user's PATH. Different machines produce different results.

### 5. The real moat is behavioral verification (10x version)

The 10x version is not better bash scripts. It's a sandboxed Claude Code session that:
1. Runs the skill against a test harness
2. Records every tool call, file access, and network egress
3. Applies a policy engine: "skill X called Write on paths outside its directory — FAIL"
4. Builds a threat model per skill type

This is verifiable, not bypassable by editing SKILL.md, and actually useful to buyers.

---

## What I Would Do

1. Drop the pretense that 6 grep scripts are a verification protocol
2. Ship `secrets-check` as standalone `sigil-scan` — one thing well, $0
3. Get adoption from early users, learn from real feedback
4. Build the behavioral sandbox as v2
5. Only at v2 call it a verification protocol

The current build is "grep in a trench coat." The 10x version makes grep irrelevant.
