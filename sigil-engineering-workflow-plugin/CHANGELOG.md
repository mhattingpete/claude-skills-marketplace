# Changelog

## [1.0.0] - 2026-06-30

### Added
- Initial release of sigil-engineering-workflow plugin
- 5 skills: plan-execute, test-doctor, safe-commit, review-apply, solution-ensemble
- 2 agents: plan-executor, secret-scanner
- 2 commands: help, version
- 3 scripts: smoke-check.sh, detect-secrets.sh, version.sh
- Language-agnostic framework detection
- Security-gated git workflow (no `git add .`)
- Test-driven bug fixing
- 5-dimension solution evaluation including security
- Market launch strategy doc from 5-lens 360 review

### Changed
- README rewritten v2 — audience-first, honest capability bounds, 30-second try-it path, MIT license, no overclaiming
- self-test.sh renamed to smoke-check.sh with corrected scope description (static checks, not functional verification)
- plugin.json description updated to match honest README language
- Fixed shell redirect bug in smoke-check.sh (checks 5 and 6 output was suppressed)

### Removed
- All fabricated statistics ("95% of secret leaks", "2-minute test fix")
- All unnamed competitor attacks (no longer opens as a hit piece)
- AEO Sky marketplace reference (not yet launched)
- "Sigil certification" branding implying external authority (self-certified)
