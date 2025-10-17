# Claude Skills Marketplace

A curated collection of Claude Code Skills for software engineering workflows, focusing on data processing, testing, and DevOps automation.

## What are Skills?

Skills are model-invoked capabilities that extend Claude Code's functionality. Unlike slash commands that require explicit user activation, Skills are automatically triggered by Claude based on context and the Skill's description.

Each Skill consists of a `SKILL.md` file with:
- YAML frontmatter (name, description, metadata)
- Detailed instructions for Claude
- Optional supporting files (scripts, templates, references)

## Installation

### Install All Skills

```bash
# In Claude Code
/plugin marketplace add mhattingpete/claude-skills-marketplace
```

### Install Individual Skills

```bash
# Clone this repository
git clone https://github.com/mhattingpete/claude-skills-marketplace.git

# Copy specific skill to your project
cp -r claude-skills-marketplace/git-pushing .claude/skills/

# Or copy to personal skills directory (available across all projects)
cp -r claude-skills-marketplace/git-pushing ~/.claude/skills/
```

## Available Skills

### Git & Version Control

#### `git-pushing`
Automatically stage, commit with conventional commit messages, and push changes to remote.

**Activates when:** User mentions pushing changes, committing work, or saving to remote.

**Example usage:**
- "Push these changes"
- "Commit and push to github"
- "Let's save this work"

---

### Testing & Quality

#### `test-fixing`
Systematically identify and fix failing tests using smart error grouping strategies.

**Activates when:** User reports test failures, asks to fix tests, or wants test suite passing.

**Example usage:**
- "Fix the failing tests"
- "Make the test suite green"
- "Tests are broken after my refactor"

---

### Code Review

#### `review-implementing`
Process and implement code review feedback systematically with todo tracking.

**Activates when:** User provides reviewer comments, PR feedback, or asks to address review notes.

**Example usage:**
- "Implement this review feedback: [paste comments]"
- "Address these PR comments"
- "The reviewer suggested these changes"

---

## Skill Locations

Skills can be installed in three locations:

- **Project Skills**: `.claude/skills/` (team-shared, version-controlled)
- **Personal Skills**: `~/.claude/skills/` (available across all your projects)
- **Plugin Skills**: Installed via plugin marketplace

## Creating Custom Skills

Want to create your own Skills? Follow this structure:

```
my-skill/
├── SKILL.md          # Main skill file with frontmatter and instructions
└── reference.md      # Optional: Additional context loaded on-demand
```

### SKILL.md Template

```yaml
---
name: my-skill-name
description: What it does and when to use it. Be specific about activation triggers.
---

# Skill Title

Brief overview of what this skill does.

## When to Use

List specific scenarios when Claude should activate this skill:
- User says X
- User mentions Y
- Context includes Z

## Instructions

Step-by-step instructions for Claude to follow...
```

### Best Practices

1. **Description is key**: Include both what the skill does AND when to use it
2. **Use gerund forms**: Name skills with "-ing" (e.g., "git-pushing", not "git-push")
3. **Keep concise**: Skills under 500 lines load faster
4. **Progressive disclosure**: Move detailed content to separate reference files
5. **Test across models**: Verify skills work with Sonnet, Opus, and Haiku

## Contributing

Contributions are welcome! To add a new skill:

1. Fork this repository
2. Create your skill in a new directory
3. Follow the SKILL.md template and best practices
4. Add your skill to this README
5. Submit a pull request

## License

Apache 2.0 - See LICENSE file for details.

## Resources

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/skills)
- [Official Anthropic Skills](https://github.com/anthropics/skills)
- [Agent Skills Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices.md)

## Support

Issues and questions:
- Open an issue on this repository
- Check [Claude Code discussions](https://github.com/anthropics/claude-code/discussions)

---

**Note**: These skills are designed for the 25L Taxonomy Assistant project but are generalized for broader use. Adapt descriptions and instructions to fit your specific workflows.
