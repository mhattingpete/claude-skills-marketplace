# Sigil

**Multi-perspective AI review engine + certification authority for Claude Code.**

Spawns parallel expert agents (Engineering, Security, UX, CEO/Strategy, QA) to audit any codebase, design doc, or skill — then produces a structured certificate (`sigil-certificate.json`) with verdict, findings, evidence markers, and validity period.

The quality gate for AI skills marketplaces. Only Sigil-certified skills may list for payment on AEO Sky.

## Features

- **5 expert lenses** — Engineering, Security, UX, CEO/Strategy, QA
- **3 review tiers** — Quick (30s), Standard (2min), Deep (5min)
- **Structured certificates** — JSON output with SHA-256 content digest for tamper detection
- **Citation discipline** — Every finding marked ✅ (verified), ⚠️ (plausible), or ❌ (cannot verify)
- **Adversarial verify pass** — Findings are challenged before reporting
- **90-day validity** — Skills re-certified after version bumps

## Usage

```
/sigil review this code           # Standard tier
/sigil quick audit ~/skill/SKILL.md  # Quick tier
/sigil deep review ./plugin       # Deep tier (all 5 agents)
```

## Certificate Schema

See `docs/certificate.schema.json` for the full JSON Schema. Certificates include:
- Skill identity and content digest
- Per-lens verdicts (PASS / FAIL / BLOCKER)
- Findings with evidence markers and source citations
- Validity period (90 days default)
- Optional Ed25519/Sigstore signature for supply-chain integrity

## Sigil-Certified Plugins

These plugins pass the Sigil 5-panel certification process:

| Plugin | What it does |
|--------|-------------|
| **[sigil-engineering-workflow](../sigil-engineering-workflow-plugin/README.md)** v1.0.0 | 5 engineering skills: plan-execute, test-doctor, safe-commit, review-apply, solution-ensemble. Security-gated, language-agnostic, self-testing. |
| **[360-review](../360-review-plugin/)** v1.0.0 | Generates 100 structured user stories (50 positive, 50 negative) across 5 expert lenses with evidence markers. Used internally by Sigil for all certifications. |

## Also available on AEO Sky

For Sigil-audited skills with free trials, usage caps, and creator payouts:

\`\`\`bash
claude plugin marketplace add BlueBoobyAI/aeo-sky-marketplace
\`\`\`
