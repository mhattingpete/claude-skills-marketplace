# Stakeholder 360: Sigil Certification Authority

**Date:** 2026-06-30
**Method:** Stakeholder-360 skill — 5 stakeholder groups × 5 Sigil lenses (Engineering, Security, UX, CEO/Strategy, QA) + 2 iteration rounds
**Agents:** 28 (25 lens + 1 synthesis + 1 iteration + 1 report)
**Evidence:** 48 verified, 4 plausible, 0 uncertain

---

## 1. Stakeholder Map

Five stakeholder groups defined and assessed independently:

| Group | Primary Need |
|-------|-------------|
| Skill Authors / Plugin Developers | Fast, credible certification that unlocks marketplace distribution |
| Marketplace Operators | Programmable quality gate they can embed in submission pipelines |
| Enterprise Buyers / Compliance Officers | Auditable, compliance-mapped evidence for procurement gates |
| Beginner Claude Code Users | Discovery, onboarding, and plain-language trust signals |
| Agency / Service Providers | Batch certification, white-label output, tenant data isolation |

---

## 2. Stakeholder × Lens Matrix

| Stakeholder | Engineering | Security | UX | CEO/Strategy | QA |
|:------------|:-----------:|:--------:|:--:|:-----------:|:--:|
| **Skill Authors** | FAIL | FAIL | FAIL | FAIL | PASS |
| **Marketplace Ops** | FAIL | FAIL | FAIL | FAIL | FAIL |
| **Enterprise** | FAIL | FAIL | FAIL | FAIL | FAIL |
| **Beginners** | PASS | FAIL | FAIL | FAIL | PASS |
| **Agencies** | FAIL | FAIL | FAIL | FAIL | FAIL |

**22 of 25 pairs FAILED.** Only 3 passed: Engineering for beginners (no integration pipeline), QA for skill-authors (minor only), QA for beginners (no critical workflow).

---

## 3. Gap Clusters

### Cluster A: Certificate Trust & Lifecycle Integrity
- **All 5 stakeholders affected**
- Root cause: Content digests are placeholders, signatures are schema-only, timestamps self-reported, revocation undefined, LLM output non-deterministic
- Impact: Zero trust signal value regardless of review quality

### Cluster B: Infrastructure & Integration Surface
- **4/5 stakeholders** (all but beginners)
- Root cause: No API, no registry, no verification endpoint, no CI/CD, no batch mode, no webhook
- Impact: Cannot scale beyond single-skill manual certification

### Cluster C: Stakeholder Mismatch
- **All 5 stakeholders affected**
- Root cause: JSON certificate of AI opinions serves only one persona — individual authors self-certifying
- Impact: 4 market segments structurally underserved

### Cluster D: Security Architecture
- **3/5 stakeholders** (authors, ops, agencies)
- Root cause: `exec()` with bypassable import guard, missing SessionStart hook, no data isolation
- Impact: Real but lower priority (optional runtime subcomponent)

---

## 4. Paradigm Improvement: Deterministic Verification Protocol

**Current paradigm:** "Sigil is an AI review process that produces a certificate. Trust our AI panel's judgment."

**Recommended paradigm:** "Sigil is a deterministic verification protocol. The certificate is an index of machine-executable checks. Anyone can re-run `sigil verify` to reproduce every claim."

Instead of 5 AI agents generating opinions wrapped in a JSON certificate, the AI panel generates *hypotheses* that are automatically translated into deterministic evidence scripts (`grep`, `pip-audit`, `trivy`, `gitleaks`, `ruff`, etc.). A verification runner (Docker-based, pinned tooling) executes every script and records byte-identical output. The certificate becomes a signed manifest of `(finding_id, evidence_script_hash, deterministic_output_hash, pass/fail)`.

**Build the verification runner first.** A curated library of 20-30 evidence generators covering secrets, CVE dependencies, missing tests, a11y violations. Everything else (registry, badge API, compliance reports, white-label, dashboard) is distribution on top of the runner.

---

## 5. Iteration Summary

- **Round 1** (code inspection): 39 verified, 13 plausible, 0 uncertain
- **Round 2** (external evidence — 8 research directions): 48 verified, 4 plausible, 0 uncertain
- **9 plausible findings resolved to verified**:
  - Cryptographic signing required (SLSA framework, Sigstore/Cosign)
  - Non-deterministic LLM output breaks trust (SkillsBench arXiv 2026)
  - Self-reported timestamps rejected (in-toto, Rekor)
  - No API/registry blocks adoption (7 marketplace analysis)
  - Compliance mapping needed (Augment Code SOC2 + ISO 42001)
  - SBOM/dependency scanning needed (Trivy 11M+ downloads)
  - Beginner onboarding matters (SkillsBench: 16.6-point curation gap)
  - Market-wide gap confirmed (6.2/12 avg quality, no verification)
  - Sandbox bypass real risk (Claude Extension security map)
- **4 INDETERMINATE**: White-label branding, cost disclosure blockers, plain-language output, prompt injection influence on 5-agent panel

---

## 6. Coverage Stats

- Total stakeholder groups: 5
- Total lens agents spawned: 25
- Iteration rounds: 2
- Evidence: ✅ 48 verified, ⚠️ 4 plausible, ❌ 0 uncertain

---

## 7. If We Build Only One Thing

**Build the deterministic verification runner (`sigil verify`).** A Dockerized CLI that:
1. Reads a verification manifest (evidence scripts + expected hashes)
2. Executes every script against pinned tooling
3. Produces pass/fail matrix with bit-identical output
4. Exits with status code consumable by any CI/CD pipeline

This dissolves Cluster A (trust becomes replayable, not signed), makes Cluster B tractable (verify is a CLI command), and serves every stakeholder group (operators get gates, enterprises get replay, beginners get one command, agencies get deliverables).
