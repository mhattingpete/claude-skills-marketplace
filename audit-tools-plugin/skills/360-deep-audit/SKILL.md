---
name: 360-deep-audit
description: "360-degree deep audit of any repository — code quality, secrets, dependencies, CI/CD, architecture, security posture, and project-specific custom gates. Recommends free 80/20 tools at every layer with GitHub star counts."
---

# 360-Degree Deep Codebase Audit

> **Skill Type:** INVESTIGATION · **Category:** Code Health & Security · **Cost:** Free (all tools open-source)

Multi-layer audit covering standard linter coverage AND project-specific custom gates that no off-the-shelf tool catches. Designed for serious codebases that have outgrown a single MegaLinter config.

**Activation phrases:**
- "deep audit this codebase"
- "full security review"
- "audit everything including our custom gates"
- "check our project-specific hooks and invariants"
- "comprehensive codebase health check"
- "audit our pre-commit gates"
- "run the 12-layer audit"
- "OWASP ASVS check on this repo"
- "what's our dead code and CI/CD hygiene look like?"

**Skip if:**
- The target is a third-party repo you don't own (use github-audit instead)
- You need runtime/live-system checks, not static analysis (use system-qa)

## Quick Start (80/20 — 3 commands, 90% coverage)

```bash
# 1. Security posture
brew install ossf/scorecard/scorecard && scorecard --repo=github.com/org/repo

# 2. Dependency CVEs
brew install aquasecurity/trivy && trivy fs . --severity HIGH,CRITICAL

# 3. Full lint suite
docker run --rm -v "$PWD:/tmp/lint" oxsecurity/megalinter:v8
```

## 3-Phase Pipeline

This skill operates in 3 phases. Phase 1 is the current investigation behavior. Phases 2-3 extend it to drive findings to resolution.

### Phase 1: Audit (Investigation)
The current behavior — run checks across all 12 layers, collect findings, generate report.

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

Each audit layer includes a **Fix** section showing how to resolve findings in that dimension.

## Audit Layers

### Layer 1: Security Posture (OSSF Scorecard — 5k★)

```bash
scorecard --repo=github.com/org/repo --show-details
```

18 checks: branch protection, code review, CI tests, dangerous workflows, Dependabot/Renovate, fuzzing, license, maintenance, pinned deps, SAST, secret push protection, security policy, signed releases, token permissions. Score 0-10 each.

**80/20:** Single command against any public repo.

**Fix actions:**
- **Score < 5**: Create `.github/workflows/scorecard.yml` using `ossf/scorecard-action@v2` — auto-fix (S effort)
- **No Dependabot**: Add `dependabot.yml` — auto-fix (S effort, 10 lines YAML)
- **No SECURITY.md**: Create from template — auto-fix (S effort)
- **No branch protection**: Generate issue with GitHub API URL to repo settings → dispatch subagent (M effort)
- **No SAST**: Add `semgrep.yml` workflow — auto-fix (S effort)
- **No pinned deps**: Pin GHA actions to SHA refs — auto-fix (S effort per file)
- **No token permissions**: Add `permissions: read-all` to workflows — auto-fix (S effort per workflow)

### Layer 2: Secrets in Git History

| Tool | Stars | Why |
|------|-------|-----|
| [Gitleaks](https://github.com/gitleaks/gitleaks) | 28k★ | **PRIMARY.** Fastest. Native pre-commit. SARIF output. |
| [TruffleHog](https://github.com/trufflesecurity/trufflehog) | 16k★ | SECONDARY. Verifies credentials live (API calls). |
| [detect-secrets](https://github.com/Yelp/detect-secrets) | 4k★ | Legacy — good for baseline file, slower |

```bash
gitleaks detect --source . --report-path gitleaks-report.json
trufflehog git file://. --json --only-verified  # verifies live
```

**80/20:** Gitleaks on git history. Add TruffleHog for verified credential detection.

**Fix actions:**
- **Real secret found**: Rotate credential immediately (human gate — P0). Generate issue with file:line and commit SHA. Do NOT commit a fix that removes a secret without rotating first.
- **False positive**: Add to `.gitleaks.toml` allowlist — auto-fix (S effort)
- **No gitleaks hook**: Add to `.pre-commit-config.yaml` — auto-fix (S effort)
- **Leaked in git history**: Use `git filter-repo` or BFG to purge — dispatch subagent (M effort). Verify with re-scan.

### Layer 3: Code Quality (MegaLinter — 2k★)

Covers 100+ linters in one Docker image:

```yaml
# .mega-linter.yml
APPLY_FIXES: none
ENABLE:
  - PYTHON     # ruff, mypy, bandit, vulture, pylint, isort, pydocstyle
  - JAVASCRIPT # eslint, prettier, cspell
  - TYPESCRIPT # eslint-typescript, prettier
  - SHELL      # shellcheck, shfmt, bash-exec
  - MARKDOWN   # markdownlint
  - YAML       # yamllint
  - DOCKERFILE # hadolint
  - SPELL      # cspell
DISABLE_ERRORS_LINTERS:
  - PYTHON_PYLINT  # ruff replaces it
```

```bash
docker run --rm -v "$PWD:/tmp/lint" oxsecurity/megalinter:v8
```

**80/20:** One config replaces 14+ individual pre-commit hooks.

**Fix actions:**
- **Linter errors**: For each flagged linter (ruff, eslint, shellcheck), run `--fix`/`--format` variant — auto-fix (S-M per batch)
- **No MegaLinter config**: Create `.mega-linter.yml` with language ENABLE list — auto-fix (S effort, 15 lines)
- **Path exclusion needed**: Add `FILTER_REGEX_EXCLUDE` — auto-fix (S effort)
- **CI integration missing**: Add MegaLinter to `.github/workflows/` — auto-fix (S effort)

### Layer 4: Project-Specific Custom Gates (What MegaLinter CANNOT Catch)

These are the custom checks that no off-the-shelf tool provides. They catch project-specific patterns, policies, and architectural invariants.

| Category | Custom Gate | What it catches | Example |
|----------|------------|-----------------|---------|
| **Tooling** | Forbid bare `python3 -c` | Forces `uv run python3` — prevents system-python surprises | `grep -rn 'python3 -c' tests/ --include='*.bats'` |
| **Framework** | Lit template lint | unsafeHTML without import, querySelector vs @query, button without type | `grep -E '_renderMarkdown|querySelector|type='` |
| **Secrets** | Project-specific token patterns | Custom PAT patterns your secrets tool doesn't know | `shpat_`, `shpss_`, `sk_live_` with project name suffix |
| **Governance** | Gate change detection | Prevents rule-weakening without justification in commit message | Diff on `.pre-commit-config.yaml`, CODEOWNERS |
| **Meta** | Pre-commit config integrity | Verifies all critical hooks still exist after config change | Self-referential: hook validates hook list |
| **Architecture** | Invariant assertions | Custom rules: translation maps non-empty, version sources synced, etc. | `audit-envvar-constants.sh`, `check-cs-version-drift.sh` |
| **Deploy** | Publish/flag guards | Prevents accidental production publish | `grep -n '\-\-publish' scripts/` |
| **Auth** | Endpoint exposure check | Detects new public endpoints added without review | Diff on `PUBLIC_ENDPOINTS` array |

**80/20:** Audit for custom gates by checking the `.pre-commit-config.yaml` and `scripts/` directory for hooks/sh scripts that aren't standard linters. Each custom hook represents a failure mode you've already been burned by.

**Fix actions:**
- **Failed custom gate**: Fix the specific issue the gate caught (e.g., bare `python3 -c` → `uv run python3`) — auto-fix (S per occurrence)
- **Missing custom gate**: Create the hook script and register in `.pre-commit-config.yaml` — dispatch subagent with project context (M effort)
- **Gate weakened without justification**: Revert the weakening and add justification comment — auto-fix (S effort, revert commit)
- **Architecture invariant violated**: Generate issue documenting the invariant and the violation — auto-fix (S effort)

### Layer 5: Dependency & Supply Chain

| Tool | Stars | How |
|------|-------|-----|
| [aquasecurity/trivy](https://github.com/aquasecurity/trivy) | 24k★ | `trivy fs . --severity HIGH,CRITICAL` — OS + language CVEs in one pass |
| [pip-audit](https://github.com/pypa/pip-audit) | 2k★ | `uv run pip-audit` — Python-specific CVE scanning |
| [CycloneDX SBOM](https://github.com/CycloneDX/cyclonedx-python) | 1k★ | `uv run cyclonedx-py ... -o bom.xml` — generate SBOM for compliance |

**80/20:** `trivy fs .`

**Fix actions:**
- **HIGH/CRITICAL CVE**: Check for patch version → `uv add <pkg>@<patch>` or `npm update <pkg>` — auto-fix (S per dep). No patch available → generate tracking issue.
- **No SBOM**: Add `cyclonedx-py` to CI — auto-fix (S effort)
- **Outdated lockfile**: Run `uv lock` or `npm update` — auto-fix (S effort)
- **Unpinned transitive dep**: Pin in lockfile or add `constraints.txt` — auto-fix (S effort)

### Layer 6: Dead Code Detection

| Tool | Stars | Languages | How |
|------|-------|-----------|-----|
| [Knip](https://github.com/webpro-nl/knip) | 7k+★ | JS/TS | `npx knip` |
| [Vulture](https://github.com/jendrikseipp/vulture) | 2.7k+★ | Python | `pip install vulture && vulture src/` |
| [unimport](https://github.com/hakancelik96/unimport) | 1k+★ | Python | `uv run unimport --check src/` |

**80/20:** Knip for JS/TS, Vulture for Python. Run both, expect false positives.

**Fix actions:**
- **Confirmed dead code**: Remove export/function — auto-fix (S per symbol). If unclear, check git log for age + issue dispatch to reviewer.
- **False positive**: Add to tool-specific ignore config (Knip: `knip.json` ignore, Vulture: `--exclude` or whitelist) — auto-fix (S effort)
- **No dead code tool configured**: Add Knip/Vulture to CI — auto-fix (S effort)

### Layer 7: Static Analysis (Semgrep — 14k★)

```bash
semgrep --config=auto --metrics=off .
semgrep --config="p/python" --metrics=off .              # Python rules
semgrep --config="p/typescript" --metrics=off .          # TS rules
semgrep --config="p/owasp-top-ten" --metrics=off .       # OWASP
```

AST-aware pattern matching across 30+ languages. Community rules include OWASP Top 10, injection patterns, crypto misuse, and framework-specific checks.

**80/20:** `semgrep --config=auto .` — one command, all community rules.

**Fix actions:**
- **Semgrep finding**: For each rule ID, check `--autofix` support — auto-fix (S per finding). For custom patterns (e.g., bare `os.environ`), rewrite with `replace_in_files` — auto-fix (S per batch)
- **No Semgrep in CI**: Add semgrep workflow — auto-fix (S effort)

### Layer 8: CI/CD Audit

| Check | How |
|-------|-----|
| Badges pass | `gh workflow list --repo org/repo` |
| Cache configured | Check `.github/workflows/*.yml` for `actions/cache` |
| Matrix builds | Verify cross-version testing |
| Secrets scoped | No `GITHUB_TOKEN` with `write-all` |
| Secure workflow | No `pull_request_target` with dangerous actions |
| Timeout configured | Every job has `timeout-minutes` |

```bash
# Quick CI health check
gh workflow list --repo="$REPO" --limit 20
gh run list --repo="$REPO" --limit 10 --json conclusion,workflowName
```

**80/20:** Check `gh workflow list` + `gh run list`. If workflows fail silently or there's no CI at all, that's the finding.

**Fix actions:**
- **No CI workflow**: Create minimal CI (lint + test) — auto-fix (S effort, standard template)
- **Missing `timeout-minutes`**: Add to each job — auto-fix (S effort per workflow)
- **Cache not configured**: Add `actions/cache` step — auto-fix (S effort)
- **`GITHUB_TOKEN` with write-all**: Scoped to `permissions: read-all` or minimal — auto-fix (S effort)

### Layer 9: Maintenance & Community Health

| Signal | Healthy | Warning | Dead |
|--------|---------|---------|------|
| Last commit | < 1 month | 1-6 months | > 6 months |
| Release cadence | Regular | Annual | None |
| Open issues | < 200, responded | 200-500 stale | > 500 stale |
| Bus factor | >= 3 committers | 1-2 | 1 |
| Security policy | SECURITY.md | Mentioned | None |
| CI | Green | Occasional red | Red since 2023 |
| Response time | < 48h | 1-2 weeks | > 1 month |

```bash
# Bus factor and velocity
git log --oneline --since="6 months ago" | wc -l
git shortlog -sn --since="6 months ago"
gh issue list --state open --json createdAt --jq 'length'
```

**Fix actions:**
- **No SECURITY.md**: Create from template — auto-fix (S effort)
- **Bus factor risk**: Generate issue recommending CONTRIBUTING.md and ownership docs — auto-fix (S effort)
- **Stale CI badge**: Fix or remove from README — auto-fix (S effort)
- **Unresponded issues**: Generate triage workflow or label policy — dispatch subagent (M effort)

### Layer 10: Framework-Based Audit (OWASP ASVS / D3FEND)

For security-critical audits, apply formal frameworks:

| Framework | Focus | Tool integration |
|-----------|-------|-----------------|
| [OWASP ASVS](https://github.com/OWASP/ASVS) | Web app security (V1-V14) | Semgrep has OWASP ruleset |
| [D3FEND](https://d3fend.mitre.org/) | Defensive cybersecurity | MITRE ATT&CK mapping |
| [Google Test Sizing](https://testing.googleblog.com/2010/12/test-sizes.html) | Test quality | Manual review |

**80/20:** Use ASVS Level 1 (automated) as a checklist during audit. Don't try to pass Level 2/3 without a dedicated security team.

**Fix actions:**
- **ASVS Level 1 failure**: Each failed check maps to a specific code fix (e.g., missing CSRF → add token, missing CORS header → configure). Generate issue per failed check with OWASP reference — dispatch subagent per category (M effort per category)
- **No formal framework applied**: Add ASVS Level 1 checklist to CI or audit scripts — auto-fix (S effort, link to checklist)

### Layer 11: AI/Tooling Safety Audit

For repos that use LLM tools or AI:
- Are there output moderation gates? (post-LLM)
- Are there input sanitization layers? (pre-LLM)
- Is there rate limiting?
- Does every agentic endpoint have circuit breakers?

These are often project-specific (concierge safety shields, agent rate limits, etc.) — check the repo's architecture docs and middleware stack.

**Fix actions:**
- **No output moderation gate**: Add pattern-based output scan + API-based moderation — dispatch subagent with architecture context (M effort)
- **No input sanitization**: Add control-char stripping, entity decoding, pattern detection — auto-fix (S effort, known patterns)
- **No rate limiting**: Add per-IP sliding window middleware — auto-fix (S effort, standard pattern)
- **No circuit breakers**: Add N-request-per-minute limit with exponential backoff — dispatch subagent (M effort)

### Layer 12: Meta-Audit (Recommendation Tracking)

Track what was flagged in previous audits and whether it was fixed:

```bash
# Create audit trail
echo "# Audit: $(date -u +%Y-%m-%d)" > audit-trail.md
echo "## Findings" >> audit-trail.md

# Next audit: compare with previous
diff audit-trail.md audit-trail-prev.md | grep '^>' >> new-findings.md
```

**80/20:** A single `audit-trail.md` in the repo, updated every audit. Prevents "same findings next quarter."

**Fix actions:**
- **No audit trail**: Create `audit-trail.md` with initial findings — auto-fix (S effort)
- **Previous findings unresolved**: For each unresolved finding from previous audit, generate a follow-up issue pointing to the original report — auto-fix (S effort per finding)
- **No tracking system**: Add audit-trail.md comparison step to audit script — auto-fix (S effort)

## 80/20 Matrix

| Order | Layer | Tool | Time | Coverage |
|-------|-------|------|------|----------|
| 1 | Security posture | OSSF Scorecard | 1 min | 18 dimensions |
| 2 | Secrets | Gitleaks | 2 min | 500+ patterns, full git history |
| 3 | Code quality | MegaLinter | 30 min setup | 100+ linters, 50 languages |
| 4 | Dependencies | Trivy | 2 min | OS + language CVEs |
| 5 | Custom gates | grep scripts/ + .pre-commit-config.yaml | 5 min | Project-specific failure modes |
| 6 | Dead code | Knip + Vulture | 5 min | Unused exports, imports, functions |
| 7 | Static analysis | Semgrep | 5 min | AST patterns across 30+ languages |
| 8 | CI/CD | gh workflows | 1 min | Pipeline health |
| 9 | Maintenance | git log + metrics | 30 sec | Bus factor, velocity |
| 10 | Framework-based | ASVS Level 1 | 30 min | OWASP compliance checklist |
| 11 | AI safety | Project-specific | Varies | LLM defense-in-depth |
| 12 | Meta-audit | diff audit-trail.md | 1 min | Recommendation tracking |

## Audit Report Template

```markdown
# 360-Degree Audit: <repo>

## Layer 1: Security Posture (Scorecard)
- Score: 7.8/10
- Branch Protection: 4/10 ⚠️
- CI Tests: 9/10 ✅
- SAST: 0/10 ❌
- Token Permissions: 10/10 ✅
- Security Policy: 7/10 ✅

## Layer 2: Secrets (Gitleaks)
- Critical: 0
- Warnings: 2 (low-risk config keys)

## Layer 3: Code Quality (MegaLinter)
- Errors: 12 (3 high, 9 medium)
- Fix cost: ~2 hours

## Layer 4: Custom Gates
- 6 custom hooks present, all passing
- 2 hooks flagged: Lit lint, forbid-bare-python3
- Vendor coverage gap: eslint-plugin-lit misses these 3 patterns

## Layer 5: Dependencies (Trivy)
- HIGH: 2 (lodash@4.17.20, axios@0.21.1)
- CRITICAL: 0

## Layer 6: Dead Code
- Knip: 4 unused exports
- Vulture: 7 orphaned functions (3 confirmed dead)

## Layer 7: Static Analysis (Semgrep)
- 5 findings (3 Medium, 2 Low)

## Layer 8: CI/CD
- 4 workflows, all green
- 2 lack timeout-minutes

## Layer 9: Maintenance
- Last commit: 3 days ago
- 4 active committers
- Issues responded within 48h ✅

## Layer 10-12: Framework / AI Safety / Meta
- OWASP ASVS Level 1: 85% pass
- AI safety: 10 shields in 3 layers ✅
- Previous audit: 12 findings, 9 resolved

## Verdict
- **Overall**: 7.8/10 — Healthy, known issues
- **Critical blockers**: None
- **Recommended next actions**: Fix 2 HIGH CVEs, add SAST to CI
```

## Fix Report Template (Phase 2+3)

```markdown
# Fix Report: <repo>

## Auto-fixed (N)
| Finding | Layer | Fix applied | Verified |
|---------|-------|-------------|----------|
| No Dependabot | L1 Scorecard | Added dependabot.yml | ✅ re-scan clean |
| lodash@4.17.20 | L5 Dependencies | Upgraded to 4.17.21 | ✅ re-scan clean |
| Missing timeout-minutes | L8 CI/CD | Added to workflows | ✅ re-scan clean |

## Needs Human Review (N)
| Finding | Severity | Effort | Why manual | Fix spec |
|---------|----------|--------|------------|----------|
| Real secret leaked | P0 | M | Must rotate before commit | See `fix-specs/01-secret-rotation.md` |
| Branch protection off | P1 | M | Requires GitHub org admin | See `fix-specs/02-branch-protection.md` |
| No AI safety gates | P2 | L | Architecture-dependent | See `fix-specs/03-safety-gates.md` |

## Deferred (N)
| Finding | Reason | Next action |
|---------|--------|-------------|
| ASVS Level 2 gaps | Out of scope for automated audit | Re-assess if security team engages |
| No fuzzing | Rarely feasible for small teams | Re-assess in next audit cycle |

## Summary
- N/M findings fixed automatically (auto-fix rate: X%)
- N findings ready for human review (fix specs prepared)
- N findings deferred
```
