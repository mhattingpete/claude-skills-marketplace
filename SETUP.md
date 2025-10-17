# Setting Up Your Claude Skills Marketplace

This guide walks through publishing your Skills marketplace on GitHub.

## Prerequisites

- GitHub account
- Git installed locally
- Skills repository created at `~/Documents/Repos/claude-skills-marketplace`

## Step 1: Initialize Git Repository

```bash
cd ~/Documents/Repos/claude-skills-marketplace

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "feat: initial Skills marketplace with git-pushing, test-fixing, and review-implementing

Includes:
- Three production-ready Skills
- Documentation and contributing guidelines
- Apache 2.0 license
- Installation instructions

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Step 2: Create GitHub Repository

### Option A: Using GitHub CLI

```bash
# Install gh if not already installed
# macOS: brew install gh

# Authenticate
gh auth login

# Create public repository
gh repo create claude-skills-marketplace --public --source=. --remote=origin

# Push to GitHub
git push -u origin main
```

### Option B: Using GitHub Web Interface

1. Go to https://github.com/new
2. Repository name: `claude-skills-marketplace`
3. Description: "Claude Code Skills for software engineering workflows"
4. Visibility: **Public**
5. Do NOT initialize with README (we already have one)
6. Click "Create repository"

Then push:
```bash
git remote add origin git@github.com:mhattingpete/claude-skills-marketplace.git
git branch -M main
git push -u origin main
```

## Step 3: Configure Repository

### Add Topics

Add GitHub topics for discoverability:

1. Go to repository settings
2. Under "About", click ⚙️
3. Add topics:
   - `claude-code`
   - `claude-skills`
   - `ai-agents`
   - `anthropic`
   - `developer-tools`
   - `automation`

### Update Repository Description

```
Claude Code Skills for software engineering workflows - Git automation, testing, and code review
```

### Add Website Link

```
https://docs.claude.com/en/docs/claude-code/skills
```

## Step 4: Enable GitHub Pages (Optional)

If you want a website for your Skills:

1. Settings → Pages
2. Source: Deploy from branch
3. Branch: `main` / `root`
4. Save

GitHub will generate a site at: `https://mhattingpete.github.io/claude-skills-marketplace`

## Step 5: Test Installation

### Via Plugin Marketplace (Once Registered)

```bash
# In Claude Code
/plugin marketplace add mhattingpete/claude-skills-marketplace
```

Note: This requires registering with Claude Code plugin system (contact Anthropic or check docs).

### Manual Installation

```bash
# Clone to test
git clone https://github.com/mhattingpete/claude-skills-marketplace.git /tmp/test-skills

# Copy a skill
cp -r /tmp/test-skills/git-pushing ~/.claude/skills/

# Test in Claude Code
# Say: "Push these changes"
# The git-pushing skill should activate
```

## Step 6: Promote Your Marketplace

### Add to README Badges

```markdown
![Skills](https://img.shields.io/badge/Skills-3-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-green)
![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-purple)
```

### Share Links

- Anthropic Claude community
- Reddit: r/ClaudeAI
- Twitter/X with #ClaudeCode hashtag
- Discord communities

### Create Announcement

Example post:
```
🚀 Just published claude-skills-marketplace - a collection of Claude Code
Skills for common dev workflows!

Includes:
✅ Git automation with conventional commits
✅ Smart test fixing with error grouping
✅ Code review feedback implementation

All skills use natural language - no need to memorize commands!

Check it out: https://github.com/mhattingpete/claude-skills-marketplace
```

## Maintenance

### Adding New Skills

```bash
# Create new skill directory
mkdir my-new-skill

# Create SKILL.md
# ... (following guidelines in CONTRIBUTING.md)

# Test locally
cp -r my-new-skill ~/.claude/skills/

# Commit and push
git add my-new-skill
git commit -m "feat(skills): add my-new-skill for X functionality"
git push
```

### Accepting Contributions

1. Review PRs for:
   - Valid SKILL.md format
   - Clear description with triggers
   - Follows best practices
   - Updated README

2. Test the skill locally

3. Merge if quality standards met

### Versioning

Consider semantic versioning for major updates:

```bash
# Tag releases
git tag -a v1.0.0 -m "Release v1.0.0: Initial three skills"
git push --tags
```

## Troubleshooting

### Skills Don't Load

- Verify YAML frontmatter is valid
- Check file is named `SKILL.md` (case-sensitive)
- Ensure description field exists

### Installation Issues

- Confirm repository is public
- Check file permissions (should be readable)
- Verify directory structure matches examples

### Activation Problems

- Review description for clear triggers
- Test with exact phrases from description
- Add more activation examples

## Next Steps

1. **Create more Skills**: Identify common workflows in your projects
2. **Gather feedback**: Ask users what they'd like automated
3. **Contribute upstream**: Share generalized Skills with Anthropic
4. **Build community**: Encourage contributions

## Resources

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/skills)
- [Anthropic Skills Repo](https://github.com/anthropics/skills)
- [Skills Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices.md)

## Support

Questions or issues?
- Open an issue on GitHub
- Check Claude Code discussions
- Contact via repository discussions
