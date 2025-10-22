# Claude Code Instructions for Skills Marketplace Development

**Repository:** claude-skills-marketplace
**Purpose:** Development guidelines for creating high-quality Claude Code skills and plugins

---

## 🎯 Repository Context

This is the **Claude Skills Marketplace** - a collection of reusable skills and plugins for Claude Code. When working in this repository, you are helping develop skills that will be used by many developers.

### Current Plugins

1. **engineering-workflow-skills** (v1.1.0)
   - feature-planning, test-fixing, git-pushing, review-implementing
   - plan-implementer agent

2. **visual-documentation-skills** (v1.0.0)
   - visual-html-creator for stunning HTML documentation

3. **productivity-skills** (v1.0.0)
   - conversation-analyzer, code-auditor, project-bootstrapper, codebase-documenter

---

## 🏗️ Plugin Structure Standards

### Required Directory Structure

```
{plugin-name}-plugin/
├── .claude-plugin/
│   └── plugin.json              # REQUIRED: Plugin metadata ONLY (no skills array)
├── skills/                      # Skills directory (auto-discovered)
│   └── {skill-name}/
│       ├── SKILL.md             # REQUIRED: Skill specification
│       ├── references/          # OPTIONAL: Reference materials (markdown)
│       │   └── *.md             # Additional context/guides
│       └── scripts/             # OPTIONAL: Helper scripts
│           └── *.py             # Python scripts, shell scripts, etc.
├── agents/                      # OPTIONAL: Agents directory (auto-discovered)
│   └── {agent-name}/
│       └── AGENT.md             # Agent specification
├── commands/                    # OPTIONAL: Commands directory (auto-discovered)
│   └── {command-name}.md
├── README.md                    # REQUIRED: Plugin documentation
├── CHANGELOG.md                 # RECOMMENDED: Version history
└── EXAMPLES.md                  # RECOMMENDED: Usage examples
```

**CRITICAL: Skills are auto-discovered!**
- Skills MUST be in `skills/` subdirectory at plugin root
- Skills are automatically discovered - NO listing in plugin.json
- plugin.json contains ONLY metadata (name, version, description, author)
- Same applies to agents/ and commands/ - all auto-discovered

**Directory purposes:**
- `skills/` - All skills (auto-discovered from SKILL.md files)
- `agents/` - All agents (auto-discovered from AGENT.md files)
- `commands/` - All commands (auto-discovered from .md files)
- `references/` - Markdown documentation, guides, best practices
- `scripts/` - Executable scripts (Python, shell, etc.) that skills can use

### Critical Files

#### 1. `.claude-plugin/plugin.json`

**Location matters!** Must be in `.claude-plugin/` subdirectory, not at root.

```json
{
  "name": "example-skills",
  "version": "1.0.0",
  "description": "Clear, concise description of what the plugin provides",
  "author": {
    "name": "author-name"
  }
}
```

**Key points:**
- **ONLY metadata** - name, version, description, author
- **NO skills array** - skills are auto-discovered from skills/ directory
- **NO agents array** - agents are auto-discovered from agents/ directory
- **NO commands array** - commands are auto-discovered from commands/ directory
- Keep it simple - just plugin metadata!

#### 2. `SKILL.md`

Every skill MUST have a SKILL.md file. This is the instruction set for Claude.

**Required sections:**

```markdown
# {Skill Name}

## Purpose
Clear statement of what this skill does and why it exists.

## When to Use
List of scenarios where this skill is appropriate.

**Activation phrases:**
- "phrase that triggers this skill"
- "another trigger phrase"
- "third example"

## What It Does
Detailed explanation of the skill's workflow:
1. First step
2. Second step
3. etc.

## Approach
How the skill should approach the task, including:
- Analysis strategy
- Tool usage patterns
- Decision-making criteria
- Error handling

## Example Interaction
```
User: "example request"

Skill:
1. Does X
2. Asks Y
3. Implements Z
```

## Tools Used
- **ToolName**: Why and when to use it
- **AnotherTool**: Purpose

## Success Criteria
How to know when the skill has succeeded:
- Criterion 1
- Criterion 2

## Integration
How this skill works with other skills (if applicable).
```

**Best practices for SKILL.md:**
- Be specific about activation phrases
- Include concrete examples
- Explain the "why" not just the "what"
- Mention tool usage patterns
- Define success criteria clearly
- Use realistic example interactions

#### 3. `README.md`

Plugin README should be user-facing documentation:

```markdown
# {Plugin Name}

Brief description of what the plugin provides.

## Skills Included

### 1. Skill Name

**Purpose:** What it does

**Activates when you say:**
- "trigger phrase"
- "another phrase"

**What it does:**
- Feature 1
- Feature 2

**Example:**
```
User: "example"
Claude: [does X, Y, Z]
```

## Installation

Instructions for installing the plugin.

## Usage Tips

How to get the best results from these skills.

## Integration

How skills work together or with other plugins.

## Version

Current version number.

## Author

Author information.
```

---

## 🎨 Skill Design Principles

### 1. Automatic Activation

Skills should activate based on **natural language intent**, not explicit invocation.

**Good activation triggers:**
```
"audit the code"              → code-auditor
"set up this project"         → project-bootstrapper
"fix the tests"               → test-fixing
```

**Bad (requiring explicit invocation):**
```
"/audit"                      → Too manual
"run code-auditor"            → Not natural
```

### 2. Clear Scope

Each skill should have a **single, well-defined purpose**.

**Good (focused):**
- `test-fixing`: Fix failing tests
- `git-pushing`: Handle git operations
- `code-auditor`: Audit code quality

**Bad (too broad):**
- `do-everything`: Multiple unrelated functions
- `developer-helper`: Vague purpose

### 3. Tool-Rich Implementation

Skills should leverage **all available tools** effectively:

- **Read**: File analysis
- **Write/Edit**: Code changes
- **Grep/Glob**: Pattern matching and file discovery
- **Bash**: Execute commands, run tests
- **Task (agents)**: Delegate complex sub-tasks
- **AskUserQuestion**: Gather requirements

**Example from code-auditor:**
```
1. Use Explore agent for thorough codebase mapping
2. Use Grep for pattern detection (security issues, TODOs)
3. Use Read for detailed file analysis
4. Use Bash to run linters/analyzers if available
5. Synthesize findings into report
```

### 4. User Interaction

When to ask vs. when to proceed:

**ASK when:**
- Multiple valid approaches exist (technology choices, architectural decisions)
- Requirements are ambiguous
- User preference matters (depth of analysis, output format)
- Potentially destructive operations

**PROCEED when:**
- Best practice is clear
- Request has sufficient context
- Operation is safe and reversible
- Asking would slow down unnecessarily

**Use AskUserQuestion for structured choices:**
```
Questions:
- "Which testing framework?"
  Options: pytest, unittest, nose2
- "Deployment target?"
  Options: Docker, AWS Lambda, Traditional server
```

### 5. Comprehensive Documentation

Skills should be **self-documenting**:

- Explain what they're doing as they work
- Provide file:line references for all findings
- Summarize results clearly
- Suggest next steps

**Good example:**
```
"I've analyzed the codebase and found 3 security issues:

1. SQL injection risk in database/query.py:45
   - Uses string concatenation for queries
   - Recommendation: Use parameterized queries

2. Hardcoded credentials in config/settings.py:12
   - API key visible in code
   - Recommendation: Use environment variables

3. Missing input validation in api/users.py:78
   - User input directly used in file paths
   - Recommendation: Add path sanitization

Priority: Fix item 1 (critical) immediately."
```

---

## 🔨 Creating a New Skill

### Step 1: Plan

Before coding, define:

1. **Purpose**: What problem does this solve?
2. **Activation**: What phrases trigger it?
3. **Scope**: What's included/excluded?
4. **Tools**: Which tools will it use?
5. **Integration**: How does it work with existing skills?

### Step 2: Create Structure

```bash
# In existing plugin or create new
mkdir -p {plugin-name}-plugin/.claude-plugin
mkdir -p {plugin-name}-plugin/{skill-name}

# Create files
touch {plugin-name}-plugin/.claude-plugin/plugin.json
touch {plugin-name}-plugin/{skill-name}/SKILL.md
touch {plugin-name}-plugin/README.md
```

### Step 3: Write SKILL.md

Start with the template above. Be specific about:
- **When to activate** (trigger phrases)
- **What to do** (step-by-step workflow)
- **How to do it** (tool usage patterns)
- **Success criteria** (when is it done?)

### Step 4: Update plugin.json

Add your skill to the skills array:

```json
{
  "name": "skill-name",
  "source": "./skill-directory",
  "description": "Activates when users [trigger phrase]. Does [what it does].",
  "gitignored": false,
  "project": false
}
```

### Step 5: Document

Create/update README.md with:
- Skill purpose and benefits
- Activation examples
- Usage tips
- Integration notes

### Step 6: Test

Test the skill with various inputs:
- ✅ Natural activation phrases
- ✅ Edge cases
- ✅ Error conditions
- ✅ Integration with other skills

### Step 7: Add to Marketplace

Update `.claude-plugin/marketplace.json`:

```json
{
  "plugins": [
    {
      "name": "your-plugin-name",
      "source": "./your-plugin-directory",
      "description": "Clear description",
      "version": "1.0.0",
      "author": {
        "name": "your-name"
      }
    }
  ]
}
```

---

## 📚 Reference Materials

Skills can include reference materials in `references/` directory:

```
skill-name/
├── SKILL.md
└── references/
    ├── best-practices.md      # Industry best practices
    ├── examples.md            # Code examples
    ├── patterns.md            # Design patterns
    └── troubleshooting.md     # Common issues
```

Claude can read these during skill execution for additional context.

**When to use references:**
- Detailed technical specifications
- Code examples and templates
- Best practices guides
- Troubleshooting information
- Pattern libraries

**Examples from existing skills:**
- `visual-html-creator/references/design_patterns.md` - Design patterns for visual docs
- `visual-html-creator/references/svg_library.md` - SVG component library
- `feature-planning/references/planning-best-practices.md` - Planning guide

---

## 🤖 Creating Agents

Agents are specialized sub-agents with specific purposes.

### Agent Structure

```
agents/
└── {agent-name}/
    └── AGENT.md
```

### AGENT.md Template

```markdown
# {Agent Name}

## Purpose
What this agent specializes in.

## When to Use
Scenarios where this agent should be invoked.

## Capabilities
What this agent can do:
- Capability 1
- Capability 2

## Approach
How the agent should work:
1. Step 1
2. Step 2

## Tools
Tools this agent has access to.

## Constraints
What this agent should NOT do.

## Output
What this agent should return.
```

### Agent Best Practices

1. **Focused purpose**: Agents should have narrow, well-defined scope
2. **Clear constraints**: Explicitly state what agent should NOT do
3. **Efficient model**: Use Haiku for cost-effective execution when possible
4. **Clear output**: Define what agent should return to parent skill

**Example from plan-implementer:**
- **Purpose**: Implement code from detailed plans
- **Model**: claude-3-5-haiku (cost-effective)
- **Constraints**: No feature creep, stick to plan
- **Output**: Working implementation with tests

---

## 🎯 Quality Standards

### Required Elements

Every skill must have:
- ✅ Clear purpose statement
- ✅ Specific activation phrases
- ✅ Step-by-step approach
- ✅ Tool usage specification
- ✅ Success criteria
- ✅ Example interactions
- ✅ User-facing documentation

### Best Practices

1. **Descriptive names**: `code-auditor` not `checker`
2. **Natural activation**: Match how users naturally phrase requests
3. **Tool-rich**: Use multiple tools effectively
4. **Well-documented**: Both in SKILL.md and README
5. **Integration-aware**: Know how to work with other skills
6. **Error-resilient**: Handle edge cases gracefully
7. **User-friendly**: Explain what's happening, provide clear output

### Common Pitfalls to Avoid

❌ **Too broad**: Skill tries to do too many unrelated things
❌ **Manual activation**: Requires slash command or explicit invocation
❌ **Tool-poor**: Only uses basic tools, doesn't leverage full toolkit
❌ **Undocumented**: Unclear when/how to use
❌ **Silent**: Doesn't explain what it's doing
❌ **Isolated**: Doesn't integrate with other skills
❌ **Vague**: Unclear success criteria or output

---

## 📦 Version Management

### Semantic Versioning

Use semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes to skill interface
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, no new features

### CHANGELOG.md

Maintain a changelog:

```markdown
# Changelog

## [1.1.0] - 2025-10-22

### Added
- New skill: feature-planning
- Agent: plan-implementer

### Changed
- Improved git-pushing commit messages

### Fixed
- Bug in test-fixing error grouping

## [1.0.0] - 2025-10-15

### Added
- Initial release with 4 skills
```

---

## 🔄 Workflow for Updates

### Adding a New Skill to Existing Plugin

1. Create skill directory and SKILL.md
2. Update plugin.json (add to skills array)
3. Update README.md (document new skill)
4. Update CHANGELOG.md (note addition)
5. Increment version (MINOR version bump)
6. Test activation and functionality
7. Commit with descriptive message

### Creating a New Plugin

1. Create plugin directory structure
2. Create `.claude-plugin/plugin.json`
3. Create initial skill(s)
4. Create README.md and CHANGELOG.md
5. Update marketplace.json
6. Test thoroughly
7. Document in main README if appropriate
8. Commit and create PR if sharing

---

## 🧪 Testing Checklist

Before considering a skill complete:

- [ ] SKILL.md includes all required sections
- [ ] Activation phrases are natural and clear
- [ ] Tool usage is comprehensive and appropriate
- [ ] Success criteria are well-defined
- [ ] README.md documents the skill for users
- [ ] plugin.json correctly references the skill
- [ ] Works with natural language activation
- [ ] Handles edge cases gracefully
- [ ] Integrates well with related skills
- [ ] Example interactions are realistic
- [ ] Reference materials included if needed
- [ ] Version updated appropriately
- [ ] CHANGELOG updated

---

## 💡 Skill Ideas & Patterns

### Analysis Skills Pattern

Skills that analyze and report:
- Explore thoroughly first
- Use multiple analysis dimensions
- Provide specific findings with file:line references
- Prioritize recommendations
- Include both quick wins and long-term improvements

**Examples:** code-auditor, conversation-analyzer

### Setup/Bootstrap Skills Pattern

Skills that configure or initialize:
- Ask clarifying questions upfront
- Show plan before executing
- Work systematically through areas
- Explain each change
- Provide post-setup guidance

**Examples:** project-bootstrapper

### Documentation Skills Pattern

Skills that generate documentation:
- Explore to understand structure
- Create comprehensive coverage
- Include visual elements (diagrams)
- Provide concrete examples
- Make navigable and organized

**Examples:** codebase-documenter, visual-html-creator

### Workflow Automation Pattern

Skills that handle repetitive workflows:
- Minimize user input required
- Follow best practices automatically
- Handle edge cases
- Provide clear status/results
- Integrate with related workflows

**Examples:** git-pushing, test-fixing

---

## 🎓 Learning from Existing Skills

### Study These Examples

**Best activation phrases:**
- Look at engineering-workflow-skills for natural triggers
- Notice how they match common developer requests

**Best tool usage:**
- code-auditor: Comprehensive tool orchestration
- feature-planning: Effective use of AskUserQuestion
- plan-implementer: Focused agent with clear constraints

**Best documentation:**
- visual-documentation-skills: Excellent README structure
- productivity-skills: Clear activation examples

**Best integration:**
- feature-planning + plan-implementer: Skill → Agent handoff
- All engineering-workflow skills: Complementary capabilities

---

## 🚀 When Working on This Repository

### Your Role

You are helping develop **high-quality, reusable skills** for the Claude Code community.

**Priorities:**
1. **Skills first**: ALWAYS use available skills before manual implementation
2. **Quality over speed**: Take time to design well
3. **User experience**: Natural activation, clear output
4. **Documentation**: Both technical (SKILL.md) and user-facing (README)
5. **Integration**: Consider how skills work together
6. **Standards**: Follow established patterns and structure

### Critical Working Guidelines

**1. ALWAYS use skills when available**

For ANY task in this repository:
- Check if a skill can handle it FIRST
- Use git-pushing for all git operations
- Use feature-planning for complex features
- Use test-fixing for test failures
- **Use skill-creator for creating new skills** - ensures proper structure
- Never implement manually when a skill exists

**CRITICAL: When creating new skills:**
- ALWAYS use the skill-creator skill from example-skills
- Never manually create skill structure
- skill-creator ensures all required files and structure are correct
- Manual creation often leads to missing files (skill.json, proper directories, etc.)

**2. NEVER create markdown files unless explicitly requested by the user.**

This includes:
- ❌ Don't create README.md, CHANGELOG.md, or other docs proactively
- ❌ Don't create example files or guides without being asked
- ❌ Don't create markdown documentation as a "helpful addition"
- ✅ Only create .md files when the user specifically requests them
- ✅ Focus on code and functionality first, documentation when asked

**Exception:** When creating a new skill/plugin per user request, the required files (SKILL.md, plugin.json, README.md) are part of the deliverable and should be created.

### Making Changes

**When adding features:**
1. Understand the existing pattern
2. Design before implementing
3. Follow structure conventions
4. Document thoroughly
5. Update version and changelog
6. Test comprehensively

**When improving existing skills:**
1. Read SKILL.md fully to understand intent
2. Maintain backward compatibility if possible
3. Update documentation
4. Test that existing use cases still work
5. Version bump appropriately

### Code Quality

**For SKILL.md files:**
- Clear, concise language
- Specific instructions, not vague guidelines
- Concrete examples
- Realistic scenarios

**For reference materials:**
- Well-organized
- Comprehensive but focused
- Practical examples
- Up-to-date best practices

---

## 📋 Quick Reference

### File Locations (Critical!)

```
✅ CORRECT:
plugin-name-plugin/.claude-plugin/plugin.json
plugin-name-plugin/skill-name/SKILL.md

❌ WRONG:
plugin-name-plugin/plugin.json              # Wrong location
plugin-name-plugin/skill-name/README.md     # Wrong filename (use SKILL.md)
```

### Skill Naming

- Use kebab-case: `code-auditor`, `feature-planning`
- Be descriptive: `test-fixing` not `fixer`
- Match purpose: Name should indicate what it does

### Description Writing

**In plugin.json:**
Focus on when it activates and what it does:
```
"description": "Activates when users want to [trigger]. Provides [benefit]."
```

**In SKILL.md:**
Focus on how it works and detailed approach.

**In README.md:**
Focus on user benefits and practical examples.

---

## 🎁 Remember

**You're building tools that developers will use every day.**

Make them:
- 🎯 **Purposeful** - Clear, focused scope
- 🗣️ **Natural** - Activate with natural language
- 🔧 **Powerful** - Leverage all available tools
- 📖 **Well-documented** - Easy to understand and use
- 🤝 **Integrated** - Work well with other skills
- ✨ **Delightful** - Make developers' lives easier

---

*This repository analysis is based on existing plugins: engineering-workflow-skills, visual-documentation-skills, and productivity-skills.*
