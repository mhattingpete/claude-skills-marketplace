# 360 Review Skills

Multi-perspective 360 review that generates positive and negative user stories using 5 expert lenses (Engineering, Security, UX, CEO/Strategy, QA). Apply to any codebase, skill, design doc, or idea.

## Skills Included

### 1. 360 Review

**Purpose:** Comprehensive analysis that produces 100 balanced user stories — 10 positive and 10 negative per lens — with evidence markers and severity ratings.

**Activates when you say:**
- "Do a 360 review of this"
- "Generate user stories for this skill"
- "Analyze this from all angles"
- "What are the positive and negative use cases for..."
- "Validate this idea comprehensively"

**What it does:**
- Spawns 5 parallel expert agents (Engineering, Security, UX, CEO/Strategy, QA)
- Each agent generates 10 positive + 10 negative user stories (100 total)
- Every story has an evidence marker (✅ verified, ⚠️ plausible, ❌ uncertain)
- Negative stories get severity ratings (critical/high/medium/low)
- Synthesis report identifies top themes and actionable recommendations

**Example:**
```
User: "Do a 360 review of this skill"

Skill:
1. Reads the target SKILL.md and plugin files
2. Spawns 5 parallel expert agents
3. Each agent analyzes from their lens
4. Synthesizes 100 stories into a report
5. Presents findings with evidence markers and priorities
```

## Installation

Add this marketplace to your Claude Code:

```bash
claude plugin marketplace add mhattingpete/claude-skills-marketplace
claude plugin install 360-review
```

## Usage Tips

- Run 360 Review **before** Sigil certification to identify improvement areas
- Use on marketplace skills to find competitive gaps
- Apply to design docs before implementation to catch blind spots
- Re-run after major revisions to measure improvement
- Save the synthesis report for project documentation

## Quality Standards

This skill follows Sigil citation discipline:
- ✅ Every claim cites a source
- ⚠️ Plausible claims are clearly marked
- ❌ Speculative claims are flagged for human review
- No unsupported numerical claims
- "I don't know" is valid output

## Version

1.0.0

## Author

Sigil Project
