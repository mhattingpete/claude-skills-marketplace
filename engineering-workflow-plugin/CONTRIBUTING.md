# Contributing to Claude Skills Marketplace

Thank you for your interest in contributing! This guide will help you create high-quality Skills that work reliably across different Claude models.

## Skill Structure

A basic Skill consists of:

```
skill-name/
├── SKILL.md          # Required: Main skill file
├── reference.md      # Optional: Detailed reference material
├── examples/         # Optional: Example files or templates
└── scripts/          # Optional: Executable scripts
```

## SKILL.md Format

```yaml
---
name: skill-name
description: What it does and when to use it. Include activation triggers.
model: sonnet              # Optional: Preferred model (sonnet, opus, haiku)
---

# Skill Title

Brief overview (1-2 sentences).

## When to Use

Specific activation scenarios:
- User says "X"
- Context includes Y
- Task involves Z

## Instructions

Step-by-step instructions for Claude...
```

## Best Practices

### 1. Write Clear Descriptions

**Good:**
```yaml
description: Analyze vendorlist extraction performance and F1-scores. Use when user mentions vendorlist evaluation, low F1-scores, extraction accuracy issues, or asks to analyze vendorlist performance.
```

**Bad:**
```yaml
description: Helps with vendorlists
```

The description should answer:
- **What** does this skill do?
- **When** should it activate?
- **Why** would someone use it?

### 2. Use Gerund Names

**Good:** `git-pushing`, `test-fixing`, `review-implementing`

**Bad:** `git-push`, `fix-test`, `implement-review`

Gerund forms (-ing) indicate ongoing processes and match natural language patterns.

### 3. Keep Skills Focused

Each Skill should do ONE thing well. If you find yourself writing "and also" in the description, consider splitting into separate Skills.

### 4. Structure for Progressive Disclosure

**Keep SKILL.md under 500 lines:**
- Core instructions in SKILL.md
- Detailed reference material in reference.md
- Examples in separate files

This allows Claude to load only what's needed.

### 5. Assume Claude's Knowledge

Don't explain basic concepts. Claude already knows Python, git, testing frameworks, etc.

**Good:**
```markdown
Run `pytest -k "pattern"` to test specific cases.
```

**Bad:**
```markdown
Pytest is a testing framework for Python. The -k flag filters tests by pattern. You should use this command: `pytest -k "pattern"` to run tests that match the pattern.
```

### 6. Match Specificity to Risk

**High-risk operations** (database migrations, deployments):
- Provide step-by-step instructions
- Include validation checks
- Require confirmation

**Low-risk operations** (code formatting, documentation):
- Give general guidance
- Allow flexibility

### 7. Use Platform-Agnostic Paths

**Good:** `backend/src/utils/helper.py`

**Bad:** `backend\src\utils\helper.py`

Always use forward slashes for file paths.

### 8. Test Across Models

Test your Skill with:
- Claude Sonnet (balanced)
- Claude Opus (most capable)
- Claude Haiku (fastest)

Some models may need more detail than others.

## Submission Process

1. **Fork this repository**

2. **Create your skill:**
   ```bash
   mkdir my-skill
   cd my-skill
   # Create SKILL.md following the template
   ```

3. **Test thoroughly:**
   - Test with different phrasings
   - Verify activation triggers work
   - Check across multiple models if possible

4. **Update README.md:**
   - Add your skill to the "Available Skills" section
   - Include activation examples
   - Describe what it does

5. **Submit Pull Request:**
   - Title: "Add [skill-name] skill"
   - Description: Explain what the skill does and why it's useful
   - Include example usage

## Skill Categories

Organize your skill into one of these categories:

- **Git & Version Control**: Git workflows, commits, branches
- **Testing & Quality**: Test running, fixing, coverage
- **Code Review**: Review feedback, PR management
- **Documentation**: Docs generation, README updates
- **DevOps**: CI/CD, deployment, infrastructure
- **Data Processing**: ETL, analysis, transformation
- **Development Tools**: Linting, formatting, refactoring

## Examples of Good Skills

Look at existing skills in this repository for inspiration:

- **git-pushing**: Clear activation triggers, conventional commits
- **test-fixing**: Smart grouping strategy, systematic approach
- **review-implementing**: Todo tracking, systematic workflow

## Quality Checklist

Before submitting, verify:

- [ ] YAML frontmatter is valid
- [ ] Description includes activation triggers
- [ ] Instructions are concise (no unnecessary explanations)
- [ ] File paths use forward slashes
- [ ] Skill is under 500 lines (or uses reference files)
- [ ] Examples demonstrate activation
- [ ] README.md updated with new skill
- [ ] Tested with actual use cases
- [ ] No hard-coded paths or environment-specific details

## Getting Help

Questions or need guidance?

- Open an issue with your question
- Check [official documentation](https://docs.claude.com/en/docs/claude-code/skills)
- Look at [Anthropic's skills](https://github.com/anthropics/skills) for examples

## License

By contributing, you agree that your contributions will be licensed under the Apache 2.0 License.
