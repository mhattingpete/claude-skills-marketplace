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

**What it does:**
- Layers 1-3: Scorecard, Gitleaks, MegaLinter
- Layer 4: Project-specific custom gates (what MegaLinter CANNOT catch)
- Layers 5-7: Dependencies, dead code, Semgrep
- Layers 8-9: CI/CD audit, maintenance health
- Layers 10-12: OWASP ASVS, AI safety, meta-audit tracking
- **3-Phase Pipeline**: Audit → Triage & Fix Plan → Fix Execution

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

1.1.0

## Author

charlesliuson
