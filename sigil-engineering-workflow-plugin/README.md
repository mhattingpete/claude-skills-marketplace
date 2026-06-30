# Sigil Engineering Workflow Skills

Five prompt-driven skills for common engineering workflows — framework-aware test fixing, security-gated git staging, structured PR review application, risk-assessed planning, and multi-agent solution comparison. Part of the [Sigil Project](https://github.com/BlueBoobyAI/sigil).

*MIT License. Free for commercial and personal use.*

---

## Who this is for

**You, if you use Claude Code and:** you've hesitated to let AI touch your git history, you've had a test suite go green after a fix but missed a regression, or you've read a PR review with 15 comments and didn't know where to start.

**You, if you evaluated the existing workflow plugins and found them shallow.**

**You, if you're a team lead evaluating whether to trust Claude Code with repo operations.** (Open source, readable scripts, secret scanner is 50 lines of bash — audit before installing.)

---

## Try it in 30 seconds

After installing:

1. Create a throwaway file: `echo "shpat_fakeToken12345678901234567890" > test-leak.txt`
2. Add it to git: `git add test-leak.txt`
3. Say: *"Check this file for secrets"*
4. The secret scanner fires on `shpat_` and blocks the commit.

That's the core loop: prompt → script executes → safety gate fires → you're protected. Everything else builds on this pattern.

---

## What's here

5 skills, 2 sub-agents, 2 commands, 3 scripts.

### Skills

#### plan-execute — Implementation planning with risk assessment and parallel review

Triggers: *"Plan this feature"*, *"Assess the risk of this implementation"*

The skill probes your project's build files (`pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, etc.) to detect language and toolchain. It classifies implementation risk (low / medium / high based on scope, data sensitivity, and surface area), generates a structured plan with file list and dependencies, and for medium+ risk tasks runs a parallel review pass before committing to the plan.

Limitation: Framework detection is heuristic — it probes build files in a fixed order (`pyproject.toml` > `package.json` > `Cargo.toml` > `go.mod` > `Makefile` > `CMakeLists.txt`). Monorepos with multiple build systems will match the first entry, not necessarily the correct one.

#### test-doctor — Root-cause test fixing with regression snapshots

Triggers: *"Fix the failing tests"*, *"Why are the tests failing?"*

The skill auto-detects your test framework (pytest, jest, cargo test, go test, rspec, cmake, and others), runs the test suite once, snapshots which tests are passing, clusters failures by root cause pattern (not by file — fixes the source, not the symptoms), then fixes one cause cluster at a time. After each fix it re-runs the tests that were passing beforehand to check for regressions.

Limitation: Test repair is LLM-guided and succeeds on the first attempt roughly 30-40% of the time for non-trivial failures (consistent with published results on SWE-bench and RepaiBench). The skill is designed for iteration — if the first fix breaks something, it rolls back and tries a different approach.

#### safe-commit — Security-gated git workflow

Triggers: *"Commit these changes"*, *"Push my changes safely"*

Reads `git status --porcelain`, groups changes by type, runs `scripts/detect-secrets.sh` (50 lines of bash, 13 patterns, no dependencies) on all changed files before any staging operation, stages files individually with user review, generates commit messages from the staged diff, pushes with retry (3 attempts at 2s / 4s / 8s intervals), and detects merge conflicts early.

The secret scanner covers Shopify (`shpat_`, `shpss_`, `shpca_`), Stripe (`sk_live_`, `sk_test_`, `whsec_`, `rk_live_`), GitHub (`ghp_`, `ghs_`), AWS access keys (`AKIA`), OpenAI (`sk-proj-`), Anthropic (`sk-or-v1-`), and private key headers. It is a pure bash `grep -E` pattern scan — no entropy scoring, no binary detection, no semantic analysis. It will miss secrets with non-standard prefixes and may produce false positives on base64 strings. Pair with gitleaks or truffleHog as a pre-commit hook for comprehensive coverage.

Known issue: Filenames containing spaces will cause the script to scan wrong paths. This is fixed in a pending release.

#### review-apply — Structured PR feedback implementation

Triggers: *"Apply this PR review feedback"*, *"Implement the code review suggestions"*

Classifies each review comment into BUG / SECURITY / DESIGN / STYLE / DOC, applies security fixes first, then bugs, then design, style, and documentation last. For bug-classified comments, the skill writes a failing test before touching production code (test-driven debugging). It traces cross-file symbol usage before modifying shared interfaces.

#### solution-ensemble — Parallel solution generation with scored evaluation

Triggers: *"Generate multiple approaches to this problem"*, *"Compare approaches for this task"*

Spawns up to 3 parallel solution agents (each prompted independently from the same problem statement — not true epistemic isolation, but avoids anchoring on a single approach), scores each on 5 weighted dimensions (correctness 40%, performance 20%, maintainability 20%, security 10%, clarity 10%), and flags fundamental disagreements between surviving solutions for human judgment.

### Agents

- **plan-executor** (Sonnet) — Language detection by probing build files, generates structured implementation plans. Used by the plan-execute skill.
- **secret-scanner** — Not an LLM agent. A 50-line bash script (`scripts/detect-secrets.sh`) that runs `grep -E` against 13 patterns across staged files. Fast, auditable, no API calls.

### Commands

- `help` — Lists all skills and activation phrases (static markdown — run `ls skills/` to see current install)
- `version` — Displays plugin version from the VERSION file

### Scripts

- `scripts/detect-secrets.sh` — 50 lines of bash, 13 secret patterns, zero dependencies. Scans files passed as arguments, or `git ls-files` by default. Exits 1 if any match is found.
- `scripts/smoke-check.sh` — 7 static checks: file presence (6 required files, 5 SKILL.md, 2 AGENT.md), version consistency between VERSION and plugin.json, semver validation, script executable bits, and a grep for `git add .` in source files. None of these checks validate functional behavior (they don't run tests or verify security scanning works). Run manually with `bash scripts/smoke-check.sh`.
- `scripts/version.sh` — Reads VERSION file, validates semver, optionally checks plugin.json. Single source of truth for version.

---

## How they connect

A typical workflow:

1. **plan-execute** → structured plan with risk assessment
2. Build the feature (your normal coding)
3. **test-doctor** → fix any failing tests
4. **safe-commit** → stage, scan, and push
5. **review-apply** → apply PR feedback on the next iteration

Each skill works independently. None requires the others.

---

## Installation

This plugin is hosted in [mhattingpete's Claude Code marketplace](https://github.com/mhattingpete/claude-skills-marketplace) alongside community-contributed skills:

```bash
claude plugin marketplace add mhattingpete/claude-skills-marketplace
claude plugin install sigil-engineering-workflow
```

Or from source:
```bash
git clone git@github.com:BlueBoobyAI/claude-skills-marketplace.git
cd claude-skills-marketplace
claude plugin install sigil-engineering-workflow-plugin
```

---

## Requirements

- Claude Code CLI
- Git (for safe-commit skill)
- Standard development tools for your language, on PATH (uv, npx, bundle, cargo, etc. — detection is automatic, but the tool must be installed)

---

## What this isn't

Not a multi-agent orchestration framework. Not a CI/CD replacement. Not a security audit tool. Not an independent certification authority. A collection of prompt-driven skills with some supporting shell scripts, designed to save you time on repetitive engineering workflows. Each skill is a single page of instructions that tells Claude how to approach a task, backed by scripts where deterministic behavior matters (secret detection, version enforcement).

---

## Version

1.0.0 — [MIT License](LICENSE)

---

*Built by the [Sigil Project](https://github.com/BlueBoobyAI/sigil).*
