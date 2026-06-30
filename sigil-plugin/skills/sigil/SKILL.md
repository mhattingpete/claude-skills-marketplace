---
name: sigil
description: Certification authority for Claude Code skills. Multi-perspective review engine that spawns expert agents (Engineering, Security, UX, CEO/Strategy, QA) to audit any codebase, design doc, or skill. Emits structured certificates for marketplace listing qualification.
triggers:
  - review this
  - audit this
  - sigil review
  - certify this
  - stamp of approval
  - multi-perspective review
  - quality gate
  - assess this skill
  - evaluate this
  - should I use this skill
  - is this safe
  - verify quality
  - code review
  - design review
  - parliament review
allowed-tools:
  - Bash
  - Read
  - Agent
  - Workflow
  - AskUserQuestion
---

# Sigil

Certification authority for Claude Code skills. Assembles a panel of expert agents — Engineering, Security, UX, CEO/Strategy, and QA — each analyzing from their lens. Produces a structured certificate with verdict, findings, evidence markers, and 90-day validity.

**Why "Sigil"?** A sigil is a seal of approval — it certifies that something has been verified. That's what this skill does: stamps skills with a verifiable quality certificate.

**Citation Discipline:** Every agent must source its claims. Unsupported numbers are forbidden. Each finding is marked ✅ (verified), ⚠️ (plausible but unverified), or ❌ (cannot verify). See individual agent files for full discipline rules.

**Certificate Authority:** Sigil emits structured certificates (`sigil-certificate.json`) that marketplaces can consume. Only Sigil-certified skills may list for payment on AEO Sky. See `docs/certificate.schema.json`.

**Free at:** https://github.com/BlueBoobyAI/sigil (OSS, MIT)
**Premium at:** [our marketplace URL — coming soon]

## When to Invoke

- User says "review this code" or "audit this skill"
- Before publishing any skill to a marketplace
- Before deploying critical infrastructure changes
- Evaluating whether to adopt a third-party tool or skill

## Instructions

### Step 1 — Determine review scope + detect domain

Read the target from context or from the user's message. Determine:

**A) Tier** — how deep to go:

| Tier | Depth | Core Agents | Time |
|------|-------|-------------|------|
| **Quick** | Surface audit, 1-2 lenses | Engineering + Security | ~30s |
| **Standard** | Full audit, all lenses | All 5 core agents | ~2min |
| **Deep** | Exhaustive + adversarial | All 5 + specialists + adversarial refute | ~5min |

Default to **Standard** unless the user specifies otherwise.

**B) Domain** — what kind of thing is being reviewed? Scan the target for domain signals (keywords, file extensions, imports, project type):

| If the target is... | Invite these specialists in addition to the core panel |
|---------------------|------------------------------------------------------|
| DeFi / crypto / smart contract | DeFi Security Auditor, Tokenomics Reviewer |
| Healthcare / PHI / HIPAA | Compliance Specialist (HIPAA/HITECH) |
| AI / ML model or pipeline | AI Safety Reviewer, Data Scientist |
| API design / OpenAPI spec | API Architect |
| Legal document / terms / privacy policy | Legal Counsel |
| Database schema / migration | Database Administrator |
| Frontend / UI component library | Accessibility (a11y) Specialist, Design Systems Expert |
| Mobile app (iOS/Android) | Mobile Architect |
| DevOps / infra / CI/CD / SRE | Site Reliability Engineer |
| SaaS pricing / business model | Pricing Strategist |
| Content / documentation / README | Technical Writer (see also: readme-doctor skill) |
| E-commerce / checkout / payments | Payments Compliance Specialist (PCI-DSS) |
| Authentication / authorization system | Identity & Access Management (IAM) Specialist |
| Embedded / IoT / firmware | Embedded Systems Engineer |
| Game / game engine | Game Designer, Game Security Specialist |
| Anything financial / accounting | Financial Auditor |
| Generic / undetermined | Core 5 only — no specialists needed |

Each specialist is spawned as an agent with the same citation discipline and evidence markers as the core panel. Their findings are weighted equally in the synthesis.

### Step 2 — Spawn parallel expert agents

**Always spawn the 5 core agents** (this is the baseline panel):

```
Agent 1: Engineering  — architecture, code quality, maintainability, test coverage
Agent 2: Security     — OWASP top 10, auth, data handling, dependency risk
Agent 3: UX           — usability, accessibility, onboarding friction, error states
Agent 4: CEO/Strategy — does this move the needle? cost/benefit, opportunity cost
Agent 5: QA           — edge cases, failure modes, test gaps, breakpoints
```

**If domain matches a specialist above, spawn them in parallel too.** The review now has a variable panel size: 5 agents for generic targets, 6+ for domain-specific ones.

All agents spawn concurrently. Each receives:
1. The target (code, SKILL.md, design doc, or description)
2. Their specific lens instructions
3. A "be adversarial — find what's wrong, don't rubber-stamp" mandate
4. The citation discipline rules (✅ ⚠️ ❌ markers)

### Step 3 — Collect and synthesize

Read each agent's output. Grade each lens:

| Grade | Meaning |
|-------|---------|
| PASS | No issues found, or minor only |
| PASS_W_CONCERNS | Minor issues, worth noting |
| FAIL | Must fix before proceeding |
| BLOCKER | Cannot proceed — fundamental flaw |

Gate logic (applies to the full panel including any invited specialists):
- Quick: >= 50% PASS or PASS_W_CONCERNS → GO. Less → NO-GO.
- Standard: >= 60% PASS or PASS_W_CONCERNS → GO. Less → NO-GO.
- Deep: >= 70% PASS or PASS_W_CONCERNS → GO. Less → NO-GO.

### Step 4 — Adversarial Verify (HARD GATE)

Before reporting, challenge every FAIL and BLOCKER finding. For each one:

1. **Could this be wrong?** What would a defense lawyer argue?
2. **Is the evidence verified?** If the source marker is ⚠️ or ❌, downgrade severity by one level.
3. **Would this fail a real human review?** If yes, flag as LOW confidence.

Update the evidence markers based on verify findings. Findings that fail verification must be marked ❌ and excluded from the gate score.

Gate integrity rule: A BLOCKER that cannot be reproduced in verification becomes FAIL. A FAIL that cannot be reproduced becomes PASS_W_CONCERNS or drops entirely.

### Step 5 — Report

Output a structured verdict:

```
═══ SIGIL VERDICT ═══
Tier: Standard
Panel Size: 6 (5 core + 1 specialist)
Gate: GO (4/6 PASS — 66.6% ≥ 60%)
Domain: API Design
Invited specialist: API Architect

Engineering:  PASS  — well-structured, good test coverage
Security:     FAIL  — hardcoded API key in config.example.py [✅]
UX:           PASS  — clear error messages, good keyboard nav
CEO/Strategy: PASS  — directly addresses the user's pain point
QA:           PASS  — good edge case handling
API Design:   PASS_W_CONCERNS — versioning strategy could be clearer

Summary: Solid implementation. Fix the hardcoded key before shipping.
Certificate: emitted to sigil-certificate.json
```

Include actionable remediation for FAIL/BLOCKER items.

### Step 6 — Emit Certificate (REQUIRED for marketplace skills)

If reviewing a marketplace skill, the certificate is REQUIRED — not optional. It serves as the listing qualification document for any marketplace that accepts Sigil-certified skills (AEO Sky, community marketplaces, etc.).

Generate a `sigil-certificate.json` file with the full certificate:

```json
{
  "certificate_version": "0.2.0",
  "skill_name": "skill-name",
  "skill_version": "1.0.0",
  "skill_source": "path or URL to the skill being reviewed",
  "content_digest": "sha256:hex-of-skill-files-manifest",
  "tier": "standard",
  "domain": "api-design",
  "panel_size": 6,
  "invited_specialists": ["api-architect"],
  "verdict": "GO",
  "sigil_score": 85,
  "gate_results": {
    "engineering": "PASS",
    "security": "FAIL",
    "ux": "PASS",
    "ceo": "PASS",
    "qa": "PASS",
    "api-architect": "PASS_W_CONCERNS"
  },
  "findings": [
    {"evidence": "✅", "lens": "security", "severity": "critical", "description": "Hardcoded API key in config.example.py:15"},
    {"evidence": "✅", "lens": "engineering", "severity": "low", "description": "Minor naming inconsistency"}
  ],
  "uncertainties": ["What couldn't be verified"],
  "validity": {
    "issued": "2026-06-30T00:00:00Z",
    "expires":  "2026-09-28T00:00:00Z",
    "validity_days": 90
  },
  "metadata": {
    "sigil_version": "0.2.0",
    "agents_used": ["engineering", "security", "ux", "ceo", "qa", "api-architect"],
    "total_agent_cost_estimate": "$0.00"
  }
}
```

**Certificate validity:** Certificates expire 90 days from issue. Skills must be re-certified after any version bump or significant code change.

**Marketplace listing requirement:** Only skills with a valid (non-expired) Sigil certificate may list for payment on AEO Sky marketplace. Certificate is published alongside the listing for buyer transparency.

## Reference

See `agents/` for the full sub-agent definitions. See `docs/certificate.schema.json` for the certificate schema.
