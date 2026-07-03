---
name: "scorecard-auditor"
description: "Multi-lens quality assessment for any Claude Code output. Activates when users want to audit quality, evaluate an output, score something, review work, or get a structured assessment."
license: MIT
metadata:
  tier: "STANDARD"
  category: "Engineering / Quality Assurance"
cert: "sigil-verified"
---

# Scorecard Auditor

## Purpose

Evaluate any output across 4 lenses: Engineering (architecture, code quality), Security (auth, data handling, OWASP), UX (usability, error states), CEO/Strategy (does this move the needle?). Outputs structured Scorecard with evidence markers.

This skill replaces unstructured feedback with a repeatable, multi-perspective scoring system. Every finding is traceable to a specific evidence marker. Every verdict follows a gate rule that prevents "looks good" rubber-stamping.

## When to Use

**Activation phrases:**
- "audit this output"
- "score this work"
- "get a scorecard for {thing}"
- "review {thing} for quality"
- "evaluate this {PR / design / feature / document}"
- "is this ready to ship?"
- "grade this {implementation / proposal / architecture}"

## Process

### 1. INPUT

Accept the target output. Sources:

- Inline text (user provides directly)
- File path (read the file)
- Conversation reference (the most recent code block, diff, or description)
- Git diff (staged or between refs, e.g. `main...HEAD`)

If the target is ambiguous, ask one clarifying question: "What exactly should I evaluate?" Do NOT ask more than one question.

### 2. PARALLEL EVALUATION

Four independent lens evaluations, each scoring on 0-100 with structured findings:

#### Engineering (Architecture, Code Quality, Maintainability)

Evaluate:
- Architecture: separation of concerns, dependency direction, abstraction level
- Maintainability: readability, naming, DRY, single-responsibility
- Test coverage: presence, meaningful assertions, edge cases, isolation
- Edge cases: null/empty/error paths, concurrency, state transitions, boundary conditions
- Performance: algorithmic complexity, unnecessary allocations, resource leaks

Scoring guide:
- 90-100: Production-grade. Clear architecture, tested, handles edge cases.
- 70-89: Good. Minor improvements needed but shippable.
- 40-69: Needs work. Structural issues, missing tests, unclear flows.
- 0-39: Problematic. Architecture is wrong, no tests, high technical debt.

#### Security (OWASP Top 10, Auth, Data Handling)

Evaluate:
- OWASP Top 10: injection, XSS, broken auth, sensitive data exposure, misconfiguration
- Authentication: credential handling, session management, token lifecycle
- Data handling: input validation, output encoding, PII exposure, logging of secrets
- Dependency risk: known-vulnerable dependencies, supply chain risk
- Error handling: information leakage through error messages, stack traces in responses

Scoring guide:
- 90-100: Secure by design. Defense in depth. No findings.
- 70-89: Generally secure with minor hardening opportunities.
- 40-69: Notable gaps. At least one real vulnerability class present.
- 0-39: Critical vulnerabilities present. Do not ship.

#### UX (Usability, Accessibility, Error Handling)

Evaluate:
- Usability: clear affordances, predictable behavior, minimal cognitive load
- Accessibility: keyboard navigation, screen reader support, color contrast, focus management
- Error handling: helpful error messages, graceful degradation, recovery paths
- Onboarding friction: setup steps, documentation clarity, learning curve
- Feedback: loading states, confirmation dialogs, undo support

Scoring guide:
- 90-100: Delightful. Intuitive, accessible, handles every state.
- 70-89: Solid. Minor friction points.
- 40-69: Rough. Missing states, accessibility gaps, confusing flows.
- 0-39: Broken. Users will get stuck or make irreversible mistakes.

#### CEO / Strategy (Does This Move the Needle?)

Evaluate:
- Business impact: does this solve a real customer problem or improve a key metric?
- Cost/benefit: implementation effort vs. expected value
- Opportunity cost: is this the best use of engineering time right now?
- Differentiation: does this create competitive advantage or parity?
- Risk: what happens if this is wrong? Are there rollback paths, feature flags?

Scoring guide:
- 90-100: High-leverage. Directly drives a business goal, clear ROI.
- 70-89: Valuable. Positive impact, worth doing.
- 40-69: Marginal. Unclear ROI. May not be worth the complexity.
- 0-39: Misaligned. Does not move any needle, or actively harms.

### 3. SYNTHESIS

Combine the four scores into a structured verdict.

Per-lens verdict classification:
- 70-100: PASS (or PASS_WITH_CONCERNS if score is 70-79)
- 0-69: FAIL

Gate logic:
- 3 or more lenses rate PASS or PASS_WITH_CONCERNS -> overall PASS
- 2 or fewer lenses rate PASS -> overall FAIL

Dedup findings: if the same issue is caught by multiple lenses, promote it one severity level and cite the cross-lens detection as a finding in itself.

### 4. OUTPUT

Render the structured JSON report and a readable scorecard.

## Output Format

```
═══ SCORECARD ═══
Engineering:  PASS  (85/100) — well-structured components, good test coverage
Security:     FAIL  (45/100) — hardcoded credentials [❌], no input validation [⚠️]
UX:           PASS  (72/100) — clear error messages [✅], no keyboard nav [⚠️]
CEO/Strategy: PASS  (90/100) — addresses the real pricing problem [✅]
───
Verdict: FAIL — fix security issue before shipping

Evidence markers:
  ✅ = strong / no issue
  ⚠️  = concern / needs attention
  ❌ = blocker / must fix

Top actions:
1. [SECURITY ❌] src/api/auth.py:42 — hardcoded API key, move to env var
2. [UX ⚠️] src/app.js:88 — no keyboard support for dropdown menu
3. [ENG ⚠️] src/models/user.py:12 — missing null check on email field
```

JSON mode (for machine consumption):

```json
{
  "scorecard": {
    "engineering": {"score": 85, "verdict": "PASS", "findings": [...]},
    "security": {"score": 45, "verdict": "FAIL", "findings": [...]},
    "ux": {"score": 72, "verdict": "PASS_WITH_CONCERNS", "findings": [...]},
    "ceo_strategy": {"score": 90, "verdict": "PASS", "findings": [...]},
    "overall": {"verdict": "FAIL", "reason": "Security lens below 70 threshold"}
  }
}
```

## Success Criteria

A successful Scorecard Audit produces:

1. **Evidence-backed scores** — each number traces to specific findings with file:line references
2. **Cross-lens consistency** — the same issue flagged by multiple lenses is detected and promoted
3. **Calculable total** — the four scores and gate logic produce a clear PASS/FAIL verdict
4. **Actionable findings** — every ❌ and ⚠️ finding includes a concrete remediation suggestion
5. **Gate logic traceable** — the verdict explanation references the exact rule that produced it

## Integration

This skill can be called by other skills as a quality gate:

- **Code review pipeline** — `/code-review` passes diff to Scorecard Auditor for post-review quality scoring
- **Design review** — `/design-review` routes final output through Scorecard Auditor for scoring
- **Pre-deploy gate** — CI/CD uses Scorecard Auditor JSON output to block deploys on security FAIL
- **Feature planning** — `/feature-planning` calls Scorecard Auditor on the PRD before implementation starts
- **Retro / post-mortem** — Scorecard Audit of shipped work identifies process gaps

Callers pass the target and optionally override lenses (e.g. skip CEO lens for internal tooling reviews). The integration contract is: pass a target, receive a structured scorecard.

### CHORUS Flywheel Integration

**Role in CHORUS flywheel:** Stage 5 (Score) — quality gate for generated surfaces.

This skill evaluates the OUTPUT of `chorus-surface-generator` (Stage 3: Generate) against brand authenticity and merchant-readiness criteria. It replaces the Skeptic review step when deeper scoring is needed.

**CHORUS contract:**
- **Input:** Surface generation output (concierge, product_finder, smart_compare JSON) + brand_profile for cross-reference
- **Output:** Structured scorecard with 4-lens scores (Engineering, Security, UX, CEO/Strategy)
- **Gate:** Score >= 7/10 across all lenses for PASS; below-threshold surfaces trigger regeneration
- **Schema reference:** Output surfaces are defined in `src/aeo/schemas/brand_profile.py` (Phase 1) — scorecard-auditor validates them against the brand contract
