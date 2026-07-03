---
name: github-audit
description: "Audit a GitHub repository for security, CI/CD health, code quality, dependency hygiene, and maintenance posture. Recommends free 80/20 tools — all open-source, 1k-28k★. Use before acquiring a dependency, assessing a project, or doing due diligence on any public repo."
---

# GitHub Repository Audit

> **Skill Type:** INVESTIGATION · **Category:** Security & Due Diligence · **Cost:** Free (zero-cost tools for public repos)

Systematic audit of any public GitHub repo across 6 dimensions. Every tool listed is free, open-source, and battle-tested (1k-28k★). The 80/20 recommendation is marked at each layer.

**Activation phrases:**
- "audit this repo"
- "check this GitHub project"
- "due diligence on org/repo"
- "is this dependency safe to use?"
- "security audit of the repository"
- "should we trust this library?"
- "scorecard this project"
- "is this package still maintained?"
- "vet this before we add it as a dependency"

**Skip if:**
- The target is your own repo and you want project-specific gates too (use 360-deep-audit instead)
- You need runtime/API-contract checks against a live system (use system-qa)

## Quick Start

```bash
# 80/20 — run these 3 commands, get 90% coverage in 2 minutes:
npx github-repo-healthcheck <org/repo>    # 1min — health score
pip install ossf-scorecard && scorecard --repo=github.com/<org/repo>  # 2min — security audit
npx @b执/mega-linter-runner --flavor javascript  # 30min — full lint suite
```

## 3-Phase Pipeline

This skill operates in 3 phases. Phase 1 is the current investigation behavior. Phases 2-3 extend it to drive findings to resolution.

### Phase 1: Audit (Investigation)
The current behavior — run checks, collect findings, generate report. See Audit Layers below.

### Phase 2: Triage & Fix Planning
After Phase 1 completes, score each finding:
- **Severity**: P0 (blocker) / P1 (critical) / P2 (standard) / P3 (cosmetic)
- **Fix effort**: S (minutes) / M (<1h) / L (half-day) / XL (multi-day)
- **Auto-fix eligibility**: S+low-risk findings can auto-fix. P0/P1 and XL effort require human gate.
- Generate a fix spec for each finding: what to change, how to change it, validation criteria

### Phase 3: Fix Execution & Verification
Apply fixes and verify them:
1. **Auto-fix**: P3+S, P2+S findings → apply fix, re-check, commit
2. **Dispatch tasks**: P2+M, P2+L findings → spawn subagent with fix spec, verify result
3. **Escalate**: P0/P1, XL effort → present fix spec to human, wait for approval
4. **Verify each fix**: re-run the audit check that found it — fix is not done until the check passes
5. **Re-audit**: run full Phase 1 again to confirm no regressions
6. **Report**: produces `findings-fixed.md`, `needs-human-review.md`, `deferred.md`

**Gate rule**: Phase 3 never runs without Phase 1 and 2 completing. Fix without audit = cargo cult.

## Fix Actions Per Layer

Each audit layer below includes a **Fix** section showing how to resolve findings in that dimension.

## Audit Layers

### 1. Security Posture (OSSF Scorecard — 5k★)  ⬅ 80/20: START HERE

**Tool:** [ossf/scorecard](https://github.com/ossf/scorecard) — OpenSSF's automated security health metrics.

```bash
# Install (brew, pip, or docker)
brew install ossf/scorecard/scorecard

# Run against any public repo
scorecard --repo=github.com/org/repo --show-details
```

Checks 18 dimensions (score 0-10 each):
- **Branch Protection** — are PRs required before merge?
- **Code Review** — are changes reviewed?
- **CI Tests** — does CI fail on broken tests?
- **Dangerous Workflow** — no `pull_request_target` with write tokens
- **Dependency Update Tool** — Dependabot or Renovate configured?
- **Fuzzing** — OSS-Fuzz integrated?
- **License** — does it have a license?
- **Maintained** — recent commits?
- **Pinned Dependencies** — pin action versions by SHA, not tag
- **SAST** — static analysis in CI?
- **Secret Push Protection** — pre-commit secret scanning?
- **Security Policy** — SECURITY.md present?
- **Signed Releases** — are releases signed?
- **Token Permissions** — minimal GHA token scoping?

**GitHub Action** (same, as CI): add `ossf/scorecard-action@v2` to a workflow — auto-generates a badge for the repo README.

**80/20:** Just the `scorecard` CLI on the repo. Covers security posture, branch protection, CI quality, dependency updates, pinning, SAST, and permissions. Single command, 18 checks.

**Fix actions:**
- **Score < 5**: Create `.github/workflows/scorecard.yml` using `ossf/scorecard-action@v2` — auto-fix (S effort)
- **No Dependabot**: Add `dependabot.yml` — auto-fix (S effort, 10 lines of YAML)
- **No SECURITY.md**: Create from template — auto-fix (S effort)
- **No branch protection**: Generate issue with GitHub API URL to repo settings → dispatch as subagent task (M effort)
- **No SAST**: Add `semgrep.yml` workflow — auto-fix (S effort)
- **No pinned deps**: Pin `actions/checkout` and other GHA actions to SHA refs — auto-fix (S effort per file)
- **No token permissions**: Add `permissions: read-all` to workflows — auto-fix (S effort per workflow)

### 2. Secret Leak Detection (Gitleaks — 28k★)  ⬅ 80/20: PAIR WITH SCORECARD

**Tool:** [gitleaks/gitleaks](https://github.com/gitleaks/gitleaks) — Fastest open-source git history secret scanner.

```bash
# Scan full git history
gitleaks detect --source . --report-path gitleaks-report.json --report-format json

# Scan uncommitted changes only (pre-commit)
gitleaks protect --source . --staged

# Scan a repo without cloning
gitleaks detect --no-git --source /path/to/exported-repo
```

| Feature | Gitleaks | TruffleHog (16k★) | detect-secrets (4k★) |
|---------|----------|-------------------|---------------------|
| Speed | Fastest | Moderate | Moderate |
| Pre-commit | Native | Via hook | Native |
| Entropy detection | Regex + entropy | Deep entropy + verification | Regex only |
| SARIF output | Yes | No | No |
| Custom rules | TOML config | YAML config | `.secrets.baseline` |
| Live credential verification | No | Yes (TruffleHog) | No |
| False positive rate | Medium | Low (verification step) | Medium |

**80/20:** Gitleaks. Fastest, MIT-licensed, native pre-commit hook, SARIF output, and already the one in our `.pre-commit-config.yaml`. Pair with TruffleHog only for verified credential scanning.

**Fix actions:**
- **Real secret found**: Rotate the credential immediately (human gate — P0). Generate issue with exact file:line and commit SHA. Do NOT commit a fix that removes a secret without rotating first.
- **False positive**: Add to `.gitleaks.toml` allowlist — auto-fix (S effort)
- **No gitleaks hook**: Add `repo: https://github.com/gitleaks/gitleaks` to `.pre-commit-config.yaml` — auto-fix (S effort)
- **Leaked in git history**: Use `git filter-repo` or `BFG Repo-Cleaner` to purge — dispatch as subagent (M effort). Verify with re-scan.

### 3. Code Quality (MegaLinter — 2k★)  ⬅ 80/20: THE BIG ONE

**Tool:** [oxsecurity/megalinter](https://github.com/oxsecurity/megalinter) — 100+ linters in one Docker image, 50+ languages.

```yaml
# .mega-linter.yml — a single config covers everything
APPLY_FIXES: none
ENABLE:
  - PYTHON
  - JAVASCRIPT
  - TYPESCRIPT
  - SHELL
  - MARKDOWN
  - YAML
  - DOCKERFILE
DISABLE_ERRORS_LINTERS:
  - PYTHON_PYLINT  # ruff replaces it
```

Covers (all through one CI step or local Docker run):
- **Python**: ruff, mypy, bandit, vulture, pylint, black, isort, pydocstyle
- **JS/TS**: eslint (with plugins), prettier, cspell
- **Shell**: shellcheck, shfmt, bash-exec
- **Secrets**: gitleaks, trivy, devskim
- **Infra**: hadolint, checkov, kube-linter, trivy (CVE scanning)
- **Formats**: yamllint, markdownlint, actionlint
- **Copy-paste detection**: duplicate detection across the codebase

```bash
# Run locally (Docker required — install with brew)
docker run --rm -v "$PWD:/tmp/lint" oxsecurity/megalinter:v8
```

**80/20:** MegaLinter replaces 14+ individual pre-commit hooks with one config. ~30 min setup, ~1GB Docker image once.

**Fix actions:**
- **Linter errors found**: For each flagged linter (ruff, eslint, shellcheck, etc.), run the auto-fix variant (`--fix`, `--format`) — auto-fix (S-M per file batch)
- **MegaLinter not configured**: Create `.mega-linter.yml` with language ENABLE list — auto-fix (S effort, 15 lines)
- **Specific exclude needed**: Add path to `FILTER_REGEX_EXCLUDE` — auto-fix (S effort)
- **CI integration missing**: Add MegaLinter to `.github/workflows/` — auto-fix (S effort)

### 4. Dependency & Supply Chain

| Tool | Stars | What it catches | How |
|------|-------|-----------------|-----|
| [aquasecurity/trivy](https://github.com/aquasecurity/trivy) | 24k★ | OS packages + language deps CVEs | `trivy fs . --severity HIGH,CRITICAL` |
| [pip-audit](https://github.com/pypa/pip-audit) | 2k★ | Python package CVEs | `uv run pip-audit` |
| [npm audit](https://docs.npmjs.com/cli/v11/commands/npm-audit) | Built-in | JS package CVEs | `npm audit --audit-level=high` |
| [CycloneDX SBOM](https://github.com/CycloneDX/cyclonedx-python) | 1k★ | Generate SBOM | `uv run cyclonedx-py requirements -i <(uv pip freeze) -o bom.xml` |

**80/20:** `trivy fs .` — single command scans OS packages, Python deps, JS deps, IaC misconfigs, and secrets. Covers the same ground as pip-audit + npm audit + safety in one pass.

**Fix actions:**
- **HIGH/CRITICAL CVE**: Check if a patch version exists → run `uv add <pkg>@<patch>` or `npm update <pkg>` — auto-fix (S effort per dep). If no patch, generate issue tracking the CVE.
- **No SBOM**: Add `cyclonedx-py` to CI — auto-fix (S effort)
- **Outdated lockfile**: Run `uv lock` or `npm update` — auto-fix (S effort)

### 5. Maintenance & Community Health

```bash
# Quick pulse metrics (no tool needed)
git log --oneline --since="6 months ago" | wc -l                          # commit velocity
git log --oneline --since="6 months ago" --author="$(git log --format='%ae' | sort | uniq -c | sort -rn | head -1 | awk '{print $2}')" | wc -l  # bus factor
gh issue list --state open --json createdAt --jq 'length'                # open issue count
gh pr list --state open --json createdAt --jq 'length'                   # open PR count
```

| Signal | Healthy | Warning | Dead |
|--------|---------|---------|------|
| Last commit | < 1 month | 1-6 months | > 6 months |
| Release cadence | Regular (quarterly+) | Annual | No releases |
| Open issues/PRs | < 200 total, responded-to | 200-500 | > 500 stale |
| Bus factor (committers) | >= 3 active | 1-2 active | 1 or unknown |
| Security policy | SECURITY.md present | Mentioned in docs | None |
| CI passing | Green badge | Occasional red | No badge or red since 2023 |

**80/20:** Check last commit date + issue response + bus factor. If the repo has 500+ open issues and < 3 committers, dig deeper before depending on it.

### 6. Semantic / Static Analysis (Semgrep — 14k★)  ⬅ ADVANCED

**Tool:** [semgrep/semgrep](https://github.com/semgrep/semgrep) — AST-based pattern matching across 30+ languages.

```bash
# Quick scan with community rules
semgrep --config=auto --metrics=off .

# Search for a custom pattern
semgrep --pattern 'os.environ[$KEY]' --lang python .
```

**When to use:** For finding specific code patterns across a codebase — like "find all Python files using bare `os.environ` instead of `os.environ.get`." Semgrep understands the AST, not just regex, so it catches multi-line variants and can do taint tracking.

**80/20:** Use after the other layers flag specific concerns. Not a first-pass tool.

**Fix actions:**
- **Semgrep finding**: Each match has a rule ID. Look up the rule's `fix:` field (if the rule has an auto-fix). Apply with `--autofix` flag — auto-fix (S effort per finding)
- **Custom pattern match (e.g., bare `os.environ`)**: Rewrite as `os.environ.get()` — auto-fix via `replace_in_files` regex (S effort per file batch)

## 80/20 Matrix (What to Run First)

| Layer | 80% tool | Time | Covers |
|-------|----------|------|--------|
| **Security** | `scorecard --repo=org/repo` | 1 min | 18 dimensions: branch protection, CI, SAST, dependency updates, permissions |
| **Secrets** | `gitleaks detect --source .` | 2 min | 500+ secret patterns across git history |
| **Code quality** | MegaLinter (one YAML) | 30 min setup | 100+ linters, 50 languages — replaces 14+ hooks |
| **Dependencies** | `trivy fs .` | 2 min | OS + language CVEs in one pass |
| **Maintenance** | git log + issue count | 30 sec | Bus factor, velocity, maintainer responsiveness |
| **Semantic** | `semgrep --config=auto` | 5 min | AST-aware pattern matching (when needed) |

## Scoring Rubric

| Score | Meaning |
|-------|---------|
| 9-10 | Production-ready — would deploy this as a dependency without reservation |
| 7-8.9 | Good — minor concerns but well-maintained |
| 5-6.9 | Adequate — usable but has gaps worth watching |
| 3-4.9 | Risky — significant concerns, prefer alternatives |
| 0-2.9 | Avoid — unhealthy or insecure |

## Audit Report Template (Phase 1)

```markdown
# GitHub Audit: org/repo

## Scorecard: 7.8/10
- CI Tests: 9/10 ✅
- Branch Protection: 4/10 ⚠️ (no required reviews on release branches)
- SAST: 0/10 ❌ (no static analysis in CI)
- Dependency Update Tool: 10/10 ✅ (Dependabot configured)
- Token Permissions: 10/10 ✅ (minimal scopes)
- Security Policy: 7/10 ✅ (SECURITY.md present)

## Secrets: 0 critical
- Gitleaks pass: clean

## Dependencies: 2 HIGH CVEs
- lodash@4.17.20 → upgrade to 4.17.21
- axios@0.21.1 → upgrade to 1.7.0+

## Maintenance: HEALTHY
- Last commit: 3 days ago
- 4 active committers
- Issues responded to within 48h

## Verdict: APPROVED
Low risk. Dependable dependency.
```

## Fix Report Template (Phase 2+3)

```markdown
# Fix Report: org/repo

## Auto-fixed (3)
| Finding | Check | Fix applied | Verified |
|---------|-------|-------------|----------|
| No SECURITY.md | scorecard | Created SECURITY.md from template | ✅ re-scan clean |
| No Dependabot | scorecard | Added dependabot.yml | ✅ re-scan clean |
| lodash@4.17.20 | trivy | Upgraded to 4.17.21 | ✅ re-scan clean |

## Needs Human Review (1)
| Finding | Severity | Effort | Why manual | Fix spec |
|---------|----------|--------|------------|----------|
| No branch protection | P1 | M | Requires GitHub org admin | See `fix-specs/01-branch-protection.md` |

## Deferred (1)
| Finding | Reason | Next action |
|---------|--------|-------------|
| No SAST in CI | Low-priority for this repo | Re-assess in next audit cycle |

## Summary
- 3/5 findings fixed automatically (auto-fix rate: 60%)
- 1 finding ready for human review (fix spec prepared)
- 1 finding deferred (low priority for current context)
```
