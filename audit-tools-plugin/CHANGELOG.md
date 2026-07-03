# Changelog

## [1.3.1] - 2026-07-02

### Added
- Explicit "Activation phrases" section to github-audit, 360-deep-audit, and lit-auto-fix SKILL.md (previously only system-qa had one — the other three relied solely on frontmatter `description` matching)
- "Skip if" disambiguation notes on github-audit and 360-deep-audit SKILL.md (third-party repo vs. own repo vs. runtime system)
- "Which Skill?" table in README.md — target-based routing across all 4 audit skills, since their scopes overlap by design

- Adversarial triage step in system-qa Phase 2→3 transition: ambiguous P0/P1 findings get a forced-verdict QA-Skeptic + Severity-Realist pass (false-positive check + blast-radius severity check) before entering the fix pipeline. Ported the forced-finding/no-LGTM-escape technique from `.agents/skills/adversarial-reviewer` — reimplemented inline rather than dispatched as a dependency, since a public marketplace plugin can't assume another plugin is installed

### Fixed
- README activation phrases for system-qa were paraphrased and out of sync with the canonical list in SKILL.md — now byte-for-byte matched
- README activation phrase lists for github-audit, lit-auto-fix, and 360-deep-audit expanded from 4-5 phrases each to 8-9, sourced from the newly-added canonical SKILL.md lists

## [1.3.0] - 2026-07-02

### Added
- Activation phrases: Unix-command style (grep, lint, syscheck, linguist)
- Phase 2 skip decision prompt (two-choice user gate when no runtime detected)
- Golden test suite protocol: pre-identification, 30s budget, zero dependencies, no mock-injection
- Subagent batch dispatch patterns: 4 logical batch groups with JSON return format contract
- Parallel adversarial reviewer pattern for Phase 3 (2-3 independent reviewers per P1/P0 finding)
- a11y baseline: axe-core/pa11y-ci preferred over grep fallback
- Build artifact signing: conditional on artifact detection

### Changed
- Report template numbers updated to match 20-static + 14-runtime check count (21 fixed, 11 escalated)
- Example workflow updated with current phase activation phrase
- Test infrastructure health (1.2) expanded: markers, pytest_collection_modifyitems
- Version history added to SKILL.md

## [1.2.0] - 2026-07-02

### Added
- New skill: system-qa — 4-phase "audit AND fix" pipeline
  - Phase 1: 20 static checks (zero-day CVE, Unix security, pytest quality, type checking, integration anti-patterns)
  - Phase 2: 14 runtime checks (OWASP LLM01, Pliny-style jailbreaks, input sanitization, output moderation, web security headers)
  - Phase 3: Auto-fix with P0-P3 severity tiers and verification
  - Phase 4: Composite report with score, before/after, and ranking
  - Essential principles, expert dispatch, multi-language detection

### Changed
- Extended 360-deep-audit Layer 11 (AI safety) with Pliny-style jailbreak detection patterns

## [1.1.0] - 2026-06-22

### Added
- New skill: lit-auto-fix — 8 Lit framework anti-patterns detection and auto-fix
- New skill: 360-deep-audit — 12-layer multi-phase audit pipeline

### Changed
- Plugin restructured to skills/ auto-discovery format
- README updated with all 3 skills documented

## [1.0.0] - 2026-06-15

### Added
- Initial release with github-audit skill
