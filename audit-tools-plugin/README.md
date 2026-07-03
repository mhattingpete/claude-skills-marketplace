# Audit Tools Plugin

Deep codebase auditing skills for Claude Code. Every tool is free and open-source with GitHub stars cited.

## Skills Included

### 1. github-audit

**Purpose:** Audit a GitHub repository across 6 dimensions — security, secrets, code quality, dependencies, maintenance, and static analysis.

**Activates when you say:**
- "audit this repo"
- "check this GitHub project"
- "due diligence on org/repo"
- "is this dependency safe to use?"
- "security audit of the repository"
- "should we trust this library?"
- "scorecard this project"
- "is this package still maintained?"
- "vet this before we add it as a dependency"

**What it does:**
- OSSF Scorecard (18 security dimensions)
- Gitleaks secret scanning
- MegaLinter code quality (100+ linters)
- Trivy dependency CVE scanning
- Maintenance health & bus factor
- Semgrep static analysis
- **3-Phase Pipeline**: Audit → Triage & Fix Plan → Fix Execution

### 2. lit-auto-fix

**Purpose:** Detect and auto-fix 8 Lit framework anti-patterns that off-the-shelf linters miss — serialization bugs, lifecycle leaks, missing a11y, and redundant renders.

**Activates when you say:**
- "audit the Lit components"
- "check for Lit anti-patterns"
- "fix the widget Lit issues"
- "run lit-detect"
- "check Shadow DOM for listener leaks"
- "audit the Lit widget before merge"
- "scan Lit components for serialization bugs"
- "is this Lit component clean?"

**What it does:**
- P1: `<button>` missing `type="button"` (form submission risk)
- P2: `renderRoot.querySelector` instead of `@query` decorator
- P3: HTML strings rendered without `unsafeHTML` import
- P4: `@property({type: Object/Array})` missing `attribute: false`
- P5: Lifecycle methods missing `super.()` call
- P6: `addEventListener` without matching `removeEventListener`
- P7: Redundant `requestUpdate()` calls (Lit auto-queues)
- P8: Interactive elements missing role/aria/keyboard handlers

### 3. 360-deep-audit

**Purpose:** 360-degree deep audit of any repository — 12 layers covering what off-the-shelf tools miss.

**Activates when you say:**
- "deep audit this codebase"
- "full security review"
- "audit everything including custom gates"
- "check our project-specific hooks and invariants"
- "comprehensive codebase health check"
- "audit our pre-commit gates"
- "run the 12-layer audit"
- "OWASP ASVS check on this repo"
- "what's our dead code and CI/CD hygiene look like?"

**What it does:**
- Layers 1-3: Scorecard, Gitleaks, MegaLinter
- Layer 4: Project-specific custom gates (what MegaLinter CANNOT catch)
- Layers 5-7: Dependencies, dead code, Semgrep
- Layers 8-9: CI/CD audit, maintenance health
- Layers 10-12: OWASP ASVS, AI safety, meta-audit tracking
- **3-Phase Pipeline**: Audit → Triage & Fix Plan → Fix Execution

### 4. system-qa

**Purpose:** 360-degree QA for running systems — discover, test, and auto-fix defects across test infrastructure, API contracts, integration health, edge cases, and silent failures. Audit AND fix in a 4-phase pipeline.

**Activates when you say:**
- "grep the codebase for problems, then fix them"
- "lint the whole stack — static, runtime, integration"
- "deep scan — find all the bugs, dead code, and gaps"
- "linguist: analyze the code quality and fix what's broken"
- "full diagnostics: static analysis, runtime checks, auto-repair"
- "diff against best practices — find and fix every gap"
- "syscheck: audit test infra, API contracts, runtime edge cases"
- "survey the system — every layer, every contract, every failure mode"

**What it does:**
- Phase 1: 20 static checks (zero-day CVE, Unix security, pytest quality, type checking)
- Phase 2: 14 runtime checks (health, API contracts, auth, error handling, prompt injection, SSRF)
- **Adversarial triage**: ambiguous P0/P1 findings get a forced-verdict QA-Skeptic + Severity-Realist pass before entering the fix pipeline — catches false positives and severity misgrades, self-contained (no external plugin dependency)
- Phase 3: Auto-fix with P0-P3 severity — verifies every fix by re-running the check
- Phase 4: Composite report with score, before/after, and ranked recommendations
- **Key differentiator**: Other QA skills test OR audit OR fix. This skill does ALL THREE — discover defects in running code, then fix them and verify.

### 5. widget-embed-qa

**Purpose:** Diagnose and fix the "two chat buttons" class of bug in embedded widgets — duplicate elements from a legacy script coexisting with a new implementation, cleanup code that loses timing races, and deploys that don't reach the live page.

**Activates when you say:**
- "there are two widget buttons"
- "duplicate widget elements on the page"
- "the cleanup only removed the first duplicate"
- "old widget still shows after deploy"
- "element comes back after I remove it"
- "the fix is deployed but the page didn't change"
- "getElementById only returns one of them"
- "the MutationObserver didn't catch it"
- "qa the widget embed"

**What it does:**
- 6-layer diagnostic ladder: census → provenance → timing → identity → delivery → root source
- One-shot live-page diagnostic script (`diagnose-widget-dom.js`) returning a JSON verdict
- Identity-based cleanup fix pattern: marker attribute on new elements + idempotent sweep + persistent MutationObserver — no timing window to lose
- Delivery hardening: per-deploy version params, served-bytes verification
- **Key differentiator**: timing-window cleanups (run-early, observe-then-disconnect) all race the parser and the cache; the identity-based pattern is time-independent and cannot lose the race

## Which Skill?

These five overlap on purpose — pick by target, not by vibe:

| Target | Skill |
|--------|-------|
| A third-party repo you're evaluating (not yours) | `github-audit` |
| Your own repo, static analysis only (no server running) | `360-deep-audit` |
| Your own repo's Lit/TypeScript components specifically | `lit-auto-fix` |
| A running system — server up, endpoints live | `system-qa` |
| Duplicate/ghost elements from an embedded widget on a live page | `widget-embed-qa` |

If unsure whether static or runtime, default to `360-deep-audit` first — it's faster and will point you to `system-qa` if runtime checks are needed.

## Usage

```markdown
User: "audit github.com/org/repo for security issues"
Claude: Runs scorecard + gitleaks + trivy → generates audit report

User: "deep audit this codebase including our custom pre-commit gates"
Claude: Runs all 12 layers → scores findings → generates fix plan
```

## Quality Bar

- All tools free and open-source (1k-28k★)
- 80/20 recommendation marked at every layer
- Severity scoring (P0-P3) with effort estimation (S-XL)
- Auto-fix for low-risk findings, human gate for critical
- Re-audit verification after every fix

## Version

1.4.0

## Author

charlesliuson
