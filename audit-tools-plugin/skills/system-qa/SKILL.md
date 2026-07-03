---
name: system-qa
description: "360-degree QA for running systems — discover, test, and auto-fix defects across test infrastructure, API contracts, integration health, edge cases, and silent failures. Audit AND fix in a 4-phase pipeline."
tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - Agent
  - AskUserQuestion
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - Agent
  - AskUserQuestion
---

# System QA

> **Skill Type:** QA/TESTING · **Category:** Code Health & Reliability · **Cost:** Free (all tools open-source)

Audits AND auto-fixes a codebase's testing, integration, and runtime quality. Unlike static-only audits, this skill exercises **running components** — it starts the app, calls endpoints, checks contracts, then fixes what it finds. 4-phase pipeline modeled on the 360-deep-audit pattern but for dynamic (runtime) QA.

**Key differentiator:** Other QA skills test OR audit OR fix. This skill does ALL THREE — discover defects in running code, then fix them and verify.

## When to Use

**Always:**
- Before a release or deploy
- After significant refactoring
- When test coverage is unknown
- When you inherit a codebase
- When CI is green but you distrust it
- When silent failures are suspected (empty catch blocks, swallowed returns)

**Activation phrases:**
- "grep the codebase for problems, then fix them"
- "lint the whole stack — static, runtime, integration"
- "deep scan — find all the bugs, dead code, and gaps"
- "linguist: analyze the code quality and fix what's broken"
- "full diagnostics: static analysis, runtime checks, auto-repair"
- "diff against best practices — find and fix every gap"
- "syscheck: audit test infra, API contracts, runtime edge cases"
- "survey the system — every layer, every contract, every failure mode"

**Skip if:**
- The project has zero test infrastructure and you're not adding any (use 360-deep-audit instead)
- You only need static code analysis (use 360-deep-audit)
- You're in a build environment with no network access to start the app

## Essential Principles

1. **Evidence over belief.** Every fix is verified by re-running the check that found it. "Looks right" is not verification.
2. **Fail loud.** Silent error swallowing is the highest-priority finding — it masks all other bugs.
3. **Fix before finding more.** Auto-fix P3/P2 findings immediately so the remaining report reflects only real remaining work.
4. **Runtime == truth.** Static analysis finds symptoms. Runtime checks find actual defects. Both are required.
5. **Generic by design.** This skill auto-detects language, framework, and test tools. It does not assume any specific stack.

### Phase 1: Static QA Scan (no runtime)

Discover the project's language, framework, test tools, and infrastructure — scan for defects visible without running the app.

**Checks:**

| # | Check | Tool/Pattern | What it catches |
|---|-------|-------------|-----------------|
| 1.1 | Test framework detection | `grep pyproject.toml`, `grep package.json` | pytest/vitest/jest presence and config |
| 1.2 | Test infrastructure health | conftest patterns, fixtures, `pytest_collection_modifyitems` | Duplicate fixtures, bad asyncio_mode, missing scope, missing markers |
| 1.3 | Linter presence | `ruff`, `eslint`, `shellcheck` | Missing or misconfigured linters |
| 1.4 | Linter output | `ruff check .`, `eslint .` | Auto-fixable and non-fixable violations |
| 1.5 | Dead code scan | `vulture src/`, `knip` | Unused exports, orphaned functions, dead imports |
| 1.6 | Secret leak scan | `gitleaks detect --source .` | Committed credentials, API keys |
| 1.7 | Fail-loud audit | Grep `except.*pass`, bare `except:`, `return None` on error | Silent error swallowing |
| 1.8 | Mock-vs-real drift | Compare mock signatures to real imports | Mocks that drifted from their real types |
| 1.9 | Coverage gate check | `--cov-fail-under` in pyproject.toml | Missing or zero coverage floor |
| 1.10 | Custom gate integrity | Project-specific hook scripts | Broken or missing custom pre-commit hooks |
| 1.11 | i18n readiness | `grep _()` for gettext, `grep i18n\|t()` in JS | Hardcoded strings without i18n wrappers |
| 1.12 | a11y baseline | `npx axe-core` or `pa11y-ci` over HTML output (preferred); fallback: `grep aria-`, `grep role=`, `grep alt=` in HTML/JSX | Missing ARIA labels, form labels, image alt text (axe-core preferred — grep is a shallow baseline) |
| 1.13 | Build artifact signing | Only if build artifacts exist (`ls dist/ build/ *.exe *.dmg *.AppImage 2>/dev/null`): check `gpg\|gpg2\|sha256sum\|codesign\|minisign` | Unsigned releases, missing checksums |
| 1.14 | Test command detection | `Makefile`, `pyproject.toml`, `package.json` | Do `pytest`, `npm test` etc. exist? |
| 1.15 | Zero-day CVE scan | `trivy fs . --severity HIGH,CRITICAL` + kernel version check | Known CVEs, needrestart-style local privilege escalation, unpatched OS-level vulns |
| 1.16 | Unix security posture | Check `find / -perm -4000`, kernel params, `/etc/security/limits.conf` | SUID bits, missing kernel hardening, capability misconfiguration |
| 1.17 | Dependency supply chain | `pip-audit` / `npm audit`, SBOM generation check | Unpatched transitive deps, missing SBOM for compliance |
| 1.18 | Pytest quality audit | Check `asyncio_mode`, fixture scoping, conftest structure, missing markers | Flaky test patterns, fixture misuse, race conditions |
| 1.19 | Type checking | `mypy src/ --strict` or `pyright` | Missing type annotations, type inconsistencies |
| 1.20 | Integration anti-patterns | Scan for real API calls in unit tests, DB connections in test fixtures | Test/prod boundary leaks, tests that depend on external services |

**Output:** `phase1-report.json` — findings with severity (P0-P3) and auto-fix eligibility.

### Phase 2: Runtime QA (exercise the app)

Start or connect to a running instance. Verify it actually works — not just that the code compiles.

**Prerequisites:** The app must be startable (dev server, test mode, or already running). Phase 2 is skipped entirely if no runtime is available, and the report explicitly says so.

**Checks:**

| # | Check | How | What it catches |
|---|-------|-----|-----------------|
| 2.1 | Health endpoint | `curl /health` | Dead process, startup failure, missing health check |
| 2.2 | API contract verification | Hit discovered endpoints with known inputs | Response shape, status codes, error objects |
| 2.3 | Auth enforcement | Hit protected endpoints without credentials | Missing auth gates, public-by-default routes |
| 2.4 | Error handling | Send malformed input, missing fields | 500 crash vs 422, unhandled exceptions |
| 2.5 | Golden test suite | Run `pytest` key test files | Test failures before any fix attempts |
| 2.6 | Integration smoke | Cross-component flow (e.g., API → DB → response) | Component boundary failures |
| 2.7 | Edge case proving | Empty input, null payloads, boundary values | Crash-on-empty, missing null checks |
| 2.8 | Mock fidelity | Verify mock isolation (no real DB/network calls leaking) | Tests that pass but would fail against real deps |
| 2.9 | Prompt injection — OWASP LLM01 | Send 20 known jailbreak patterns across 9 categories (persona hijack, payload extraction, language-based bypass, identity impersonation, role-playing, delimiters, encoding, many-shot, refusal suppression) | LLM endpoint bypass, system prompt leak |
| 2.10 | Prompt injection — Pliny-style | Test prefix injection, suffix injection, refusal suppression, few-shot jailbreak, persona modulation, base64/rot13/hex obfuscation, leetspeak bypass, typoglycemia | Advanced jailbreak techniques from adversarial prompt research |
| 2.11 | Input sanitization check | Verify multi-layer pre-LLM defense: control-char stripping, homoglyph normalization, entity decoding, injection delimiter matching, encoded payload detection | LLM01 bypass through obfuscated input |
| 2.12 | Output moderation | Check for post-LLM gates: pattern-based scan, PII/secret detection, system prompt leakage pattern check, brand voice compliance | Raw LLM output served with leaked internals or PII |
| 2.13 | Web security headers | `curl -sI $URL | grep -iE "Strict-Transport-Security|Content-Security-Policy|X-Content-Type-Options|X-Frame-Options"` | Missing HSTS, CSP, or clickjacking protection |
| 2.14 | SSRF / command injection | Scan for `request.get(url_param)`, `exec()`, `eval()`, `subprocess(shell=True)` | Server-side request forgery, arbitrary code execution |

**Output:** `phase2-report.json` — failed checks, unexpected status codes, broken endpoints, failing tests.

### Phase 2 Skip Decision

Before entering Phase 2, detect whether a runtime is available. If the project has no visible start mechanism (`docker-compose.yml`, `Makefile` with `run` target, `pyproject.toml` with `[project.scripts]`, `package.json` with `dev`/`start` script, or a running process on a known port), offer the user a two-choice prompt:

```markdown
No runtime detected for Phase 2 (API health, auth enforcement, runtime tests).
Options:
1. Start it now — provide the start command (e.g., `uv run uvicorn main:app`)
2. Skip Phase 2 entirely — the report will note "P2 skipped: no runtime"
```

If the user provides a start command, proceed with Phase 2. If they skip, note it in the final report and continue with Phase 3 on Phase 1 findings alone.

### Golden Test Suite (Check 2.5 expanded)

Check 2.5 (golden test suite) has its own protocol to avoid false negatives from flaky or time-consuming test runs:

1. **Pre-identification:** Run the test framework's dry-run / list mode (`pytest --co`, `npx vitest list`, `npm test -- --list`) to enumerate available tests.
2. **Selection:** Pick 5-10 representative tests — 1 from each key test file or functional area, prioritizing integration and end-to-end tests over unit tests.
3. **Execution budget:** Timebox to 30 seconds. If the full suite takes longer, run only the selected golden tests. Never run a 5-minute test suite in Phase 2.
4. **Zero dependencies:** Golden tests must work with just the test framework — no Docker, no external API keys, no network access. If they require external services, note "skipped (external deps)" and move on.
5. **No mock-injection:** Golden tests run as-is with existing mocks. Do NOT create new mocks or fixtures for Phase 2 — that belongs in Phase 3 auto-fix.

### Adversarial Triage (ambiguous P0/P1 only)

Before a P0/P1 finding enters Phase 3, check if it's ambiguous: conflicting signals (e.g. a linter flags it but the pattern is a known-safe idiom elsewhere in the codebase), no clear reproduction, or severity that hinges on judgment rather than a hard rule. Skip this step for clear-cut findings — it exists to catch false positives and severity misgrades before they burn a fix cycle, not to re-litigate every finding.

Dispatch two forced-finding personas in parallel (self-contained — no dependency on another plugin):

- **QA-Skeptic**: "Assume this finding is a false positive. Prove it — cite the suppression, known-safe pattern, or missing reproduction that makes it non-issue." Must either confirm the finding is real or produce the specific evidence that it isn't.
- **Severity-Realist**: "Assume the severity is wrong. Is this actually reachable in production, or gated behind an unused path/dev-only flag/test fixture?" Must state the actual blast radius, not the linter's default severity.

Both personas receive the same finding + surrounding context (file, call sites, existing tests). Neither may return "looks fine, no comment" — each must return a verdict:

```json
{"persona": "QA-Skeptic", "verdict": "REAL" | "FALSE_POSITIVE", "evidence": "..."}
{"persona": "Severity-Realist", "verdict": "P0" | "P1" | "P2" | "P3", "blast_radius": "..."}
```

Resolution: if QA-Skeptic says `FALSE_POSITIVE`, drop the finding and note it in the report (don't silently discard — a dropped P0/P1 needs an audit trail). Otherwise, use Severity-Realist's verdict as the finding's final severity before it enters the Phase 3 fix-tier table.

This mirrors `.agents/skills/adversarial-reviewer`'s forced-finding, no-LGTM-escape technique, ported to finding triage instead of code review — deliberately reimplemented here rather than invoked as a dependency, since audit-tools-plugin must not assume another plugin is installed.

### Phase 3: Auto-Fix

Apply fixes for common defect classes. Each fix is verified by re-running the check that found it. Non-fixable findings (architecture changes, missing credentials) are escalated to a human review list.

**Fix tiers:**

| Severity | Effort | Auto-fix rule |
|----------|--------|---------------|
| P3 | S | Auto-fix, re-check, commit |
| P2 | S-M | Auto-fix with verification, note in report |
| P1 | M-L | Fix with human notification, offer to apply |
| P0 | L-XL | Escalate — generate fix spec, do not apply |

**Auto-fix actions:**

| Finding | Fix | Verification |
|---------|-----|-------------|
| Silent catch block | Add `log.warning()` before bare except | Re-run fail-loud scan |
| Missing linter config | Scaffold `ruff.toml`, `.eslintrc` | Re-run linter |
| Duplicate test fixtures | Consolidate into shared conftest.py | Re-run test suite |
| Dead code (confirmed) | Remove unused exports/functions | Re-run dead code scan |
| Mock signature drift | Update mock to match real API | Re-run test suite |
| Missing test for uncovered route | Generate skeleton test | Re-run coverage scan |
| Auto-fixable linter errors | `ruff check --fix`, `eslint --fix` | Re-run linter |
| API endpoint missing error handler | Add try/except with proper error response | Re-run endpoint smoke test |
| Health check missing | Add `/health` endpoint | curl /health |
| HIGH/CRITICAL CVE in dep | `pip install <pkg>@<patch>` or `npm update <pkg>` | Re-run trivy / pip-audit |
| Missing HSTS or CSP headers | Add to web server config / middleware | Re-run curl header check |
| Missing input sanitization | Scaffold control-char strip + entity decode + injection pattern matching | Re-run injection test payload |
| Missing output moderation | Add pattern-based scan + PII regex + leakage check post-LLM | Re-run output leak detection |

**Non-fixable (escalate):**
- Missing credentials (CI tokens, API keys)
- Architecture changes (split service, add DB)
- Framework migration (pytest → vitest)
- Coverage floor below target (requires real tests, not skeletons)
- Real secret leaks (must rotate, not just delete)

### Phase 4: Composite Report

```markdown
# System QA Report: <project>

## Score: 73/100

| Phase | Score | Issues Found | Auto-Fixed | Remaining |
|-------|-------|-------------|------------|-----------|
| P1: Static QA | 85/100 | 20 | 14 | 6 |
| P2: Runtime QA | 62/100 | 12 | 7 | 5 |
| P3: Auto-Fix | — | 21 fixed | 21 | 0 verified |
| **Total** | **73/100** | **32** | **21** | **11** |

## Fixed (21)
| Finding | Phase | Fix | Verification |
|---------|-------|-----|-------------|
| Silent except in auth.py:85 | P1 | Added log.warning | Re-scan: clean |
| Missing ruff.toml | P1 | Scaffolded | ruff runs clean |
| Health endpoint 503 | P2 | Fixed startup race | curl /health: 200 |
| ... | | | |

## Needs Human Review (11)
| Finding | Severity | Effort | Fix spec |
|---------|----------|--------|----------|
| Coverage floor at 42% (target: 64%) | P2 | L | Add tests for 12 uncovered modules |
| Trivy HIGH CVE in urllib3 | P1 | M | Pin >=v2.x |
| No CI/CD pipeline | P2 | XL | Scaffold GitHub Actions |
| ... | | | |

## Verdict
- **Ship blocker?** Yes — coverage floor + 1 HIGH CVE
- **Auto-fix rate:** 66% (21/32)
- **Recommendation:** Fix HIGH CVE, address coverage gap, ship
```

## Generalization Strategy (multi-project)

This skill auto-detects the project's language, framework, and test tools, then adapts its checks:

### Language Detection
```bash
# Python
ls pyproject.toml setup.py requirements.txt Pipfile 2>/dev/null
# TypeScript/JavaScript
ls package.json tsconfig.json 2>/dev/null
# Rust
ls Cargo.toml 2>/dev/null
# Go
ls go.mod go.sum 2>/dev/null
```

### Framework Detection
```bash
# FastAPI / Flask / Django
grep -l "FastAPI\|Flask\|Django" src/*/main.py 2>/dev/null
# Next.js / Express / Hono
grep -l "next\|express\|hono" package.json 2>/dev/null
# Lit / React / Vue
grep -l "lit\|react\|vue" package.json 2>/dev/null
```

### Test Tool Detection
```bash
# pytest
grep -l "pytest" pyproject.toml 2>/dev/null
# vitest / jest / playwright
grep -l "vitest\|jest\|@playwright" package.json 2>/dev/null
```

Based on detected stack, the skill dispatches the appropriate tools and checks. Unknown stacks get a generic scan with grep-based pattern matching.

## Sub-Skills & Integration

### REQUIRED: 360-deep-audit
Run 360-deep-audit layers 1-3 (Scorecard, Gitleaks, MegaLinter) as Phase 1 pre-flight. System QA handles Layer 4+ (custom gates, runtime checks, auto-fix).

### Integration with other QA skills:
- **widget-test**: If Lit/Web Component detected, invoke for Shadow DOM-specific QA
- **playwright-shadow-dom**: If E2E tests needed for Shadow DOM components
- **api-test-suite-builder**: If API endpoints need contract test generation
- **test-driven-development**: For RED-GREEN-REFACTOR on new tests

## Auto-Fix Patterns

### Fail-Loud Fix (most common finding)
```python
# Before
except Exception:
    return None

# After
except Exception as exc:
    log.warning("operation_failed", error=str(exc))
    return None
```
**Detection:** `grep -rn 'except.*:\s*$' src/ --include='*.py' | grep -v 'log\|logger\|pass'`

### Mock Signature Alignment
```python
# Before (drifted mock)
mock_get_user.return_value = {"id": 1}

# After (aligned with real User model fields)
mock_get_user.return_value = {"id": 1, "email": "test@example.com", "role": "user"}
```
**Detection:** Compare mock usages in `tests/` against actual model imports in `src/`. Report type mismatches.

### Health Endpoint Addition
```python
# Before
@app.get("/")  # No health endpoint

# After
@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}
```
**Detection:** `curl -sf http://localhost:$PORT/health` returns non-200.

## Example Workflow

```
User: "lint the whole stack — static, runtime, integration"

Skill:
1. Phase 1: Runs all 20 static checks (linters, dead code, secrets, fail-loud, mocks, CVE, Unix security, pytest quality, type checking, integration anti-patterns)
2. Phase 2: Starts app, hits /health, tests API contracts, runs golden tests, probes OWASP LLM01 + Pliny-style injection patterns
3. Phase 3: Auto-fixes 21 issues (fail-loud, dead code, missing config, CVE patches, missing security headers)
4. Escalates 11 non-trivial findings (coverage gap, architecture changes, real secret leaks)
5. Verifies each fix by re-running the detection check
6. Produces composite report with score, recommendations
```

## Subagent Dispatch Patterns

For efficient parallel execution, dispatch subagents in batches rather than one at a time:

### Batch Scanners (Phase 1)
Split Phase 1 checks into 3-4 logical groups, each dispatched as a single `Agent` call with a defined JSON return format:

| Batch | Checks | Rationale |
|-------|--------|-----------|
| Security & Secrets | 1.6, 1.15, 1.16, 1.17 | All security-adjacent, share `gitleaks` + `trivy` + `find` commands |
| Code Quality | 1.3, 1.4, 1.5, 1.19 | All linter/dead-code/type-check — batch tool scans |
| Test Health | 1.1, 1.2, 1.7, 1.8, 1.18, 1.20 | Test infra, fixtures, fail-loud, mock drift |
| Misc | 1.10, 1.11, 1.12, 1.13, 1.14 | Custom gates, i18n, a11y, build signing |

Each batch subagent returns `{findings: Array<{check_id, severity, file, line, description, auto_fixable}>}` — no prose, no narrative. Parse and merge into the composite `phase1-report.json`.

### Parallel Reviewers (Phase 3)
For complex findings (P1/P0), dispatch 2-3 independent reviewer agents with adversarial prompts:
- Reviewer A: "Assume this fix is WRONG. Prove it."
- Reviewer B: "Find the hidden regression this fix introduces."
- Reviewer C: "What edge case did the implementer miss?"

All reviewers receive the same diff and the same fix spec. The original implementer only applies the fix if >=2 reviewers raise no objections. This prevents plausible-but-wrong fixes from landing.

### Return Format Contract
Every subagent must return a structured result, not free text. Define the schema upfront in the dispatch prompt:
```json
{"findings": [{"check_id": "1.6", "severity": "P1", "file": "src/config.py:45", "description": "Gitleaks detected AWS key", "auto_fixable": false}]}
```
If a batch returns no findings, it returns `{"findings": []}` — not "nothing found" as prose.

## Tools Used
- **Bash**: Run linters, test suites, curl endpoints, start/stop app
- **Grep/Glob**: Pattern scan for fail-loud, mock drift, error handling
- **Read**: Analyze found defects for fix eligibility
- **Edit/Write**: Apply auto-fixes
- **Agent** (general-purpose): Spawn parallel scanners per check category
- **Agent** (general-purpose, parallel): For multi-perspective validation on complex findings — spawn multiple reviewer agents with independent prompts
- **AskUserQuestion**: Gate for P0/P1 findings before applying

## Success Criteria

The skill succeeds when:
- [ ] Phase 1 completes all 20 static checks (1.1-1.20)
- [ ] Phase 2 runs at least 5 runtime checks (skipped with reason if no runtime)
- [ ] Phase 3 auto-fixes >=50% of eligible findings
- [ ] Every auto-fix is verified by re-running the detection (not just "looks right")
- [ ] Non-fixable findings have a clear fix spec or escalation
- [ ] Composite report is generated with score, before/after, and ranking
- [ ] No regressions introduced by auto-fixes (unchanged tests still pass)

## Version History

- **1.4.0** — Activation phrases updated to Unix-command style (grep, lint, syscheck); added Phase 2 skip decision prompt, golden test suite protocol (30s budget, zero deps, pre-identification), subagent batch dispatch patterns with return format contract, parallel adversarial reviewer pattern for Phase 3
- **1.3.0** — Added zero-day CVE detection, Unix security (SUID/kernel), Pliny-style jailbreak patterns, OWASP LLM01 injection (9 categories), input sanitization + output moderation checks, web security headers, i18n readness, a11y baseline, build artifact signing, dependency supply chain, pytest quality audit, type checking, integration anti-patterns
- **1.2.0** — Concurrent release with audit-tools plugin v1.2.0: multi-language detection, fail-loud fix, golden test execution, report template
- **1.0.0** — Initial: 4-phase pipeline concept
