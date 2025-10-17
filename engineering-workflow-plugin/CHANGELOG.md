# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-10-17

### Added
- **feature-planning skill**: Breaks down feature requests into detailed, implementable plans
  - Asks clarifying questions to understand requirements
  - Explores codebase for existing patterns
  - Creates detailed implementation plans with discrete tasks
  - Includes comprehensive planning best practices reference guide (381 lines)
- **plan-implementer agent**: Executes implementation tasks using Haiku model
  - Uses claude-3-5-haiku for cost-effective implementation
  - Focuses on clean, maintainable code following project conventions
  - Presents options when facing best-practice vs. simplicity conflicts
  - Strict scope adherence (no feature creep)

### Changed
- Restructured repository to follow standard plugin format
  - Moved all skills to `skills/` directory
  - Moved plan-implementer to `agents/` directory
  - Added `plugin.json` in `.claude-plugin/` directory
  - Updated `marketplace.json` to reference plugin correctly
- Updated README with Skills vs Agents explanation
- Added complete workflow example showing integration between components

## [1.0.0] - 2025-10-17

### Added
- **git-pushing skill**: Stage, commit, and push git changes with conventional commit messages
- **test-fixing skill**: Systematically identify and fix failing tests using smart error grouping
- **review-implementing skill**: Process and implement code review feedback systematically
- Initial marketplace structure
- Documentation (README, CONTRIBUTING, SETUP)
- Apache 2.0 License

[1.1.0]: https://github.com/mhattingpete/claude-skills-marketplace/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/mhattingpete/claude-skills-marketplace/releases/tag/v1.0.0
