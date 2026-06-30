---
name: 360-review
description: Multi-perspective 360 review that generates positive AND negative user stories per expert lens (Engineering, Security, UX, CEO/Strategy, QA). Applies to any codebase, skill, design doc, or idea. Outputs structured findings with evidence markers.
---

# 360 Review: User Stories Generator

Multi-perspective analysis that generates balanced positive and negative user stories for any codebase, skill, design doc, or idea. Uses 5 expert lenses to identify strengths, weaknesses, and improvement opportunities.

## When to Use

**Activation phrases:**
- "Do a 360 review of this"
- "Generate user stories for this skill"
- "Analyze this from all angles"
- "What are the positive and negative use cases for..."
- "Audit this comprehensively"
- "Review this before I ship it"
- "Can you identify edge cases for..."
- "What would go wrong with this approach?"
- "Validate this idea comprehensively"
- "Give me the good, the bad, and the ugly of..."

**Good candidates:**
- Marketplace skills about to be submitted
- Design docs or PRDs
- Codebases before major refactors
- New feature ideas
- API designs
- Pricing or business models
- Any decision with trade-offs

## What It Does

The 360 review spawns 5 parallel expert agents, each generating balanced positive and negative user stories for the target. Results are synthesized into a comprehensive report with severity ratings and evidence markers.

### The 5 Lenses

| Lens | Focus | Story Types |
|------|-------|-------------|
| Engineering | Architecture, code quality, maintainability, performance | Integration complexity, edge cases, refactoring needs |
| Security | OWASP top 10, secrets, injections, auth boundaries | Attack vectors, data exposure, privilege escalation |
| UX | Accessibility, onboarding, error states, flow gaps | Confusion points, dead ends, learnability friction |
| CEO/Strategy | Cost/benefit, opportunity cost, market fit, timing | Adoption resistance, ROI failure modes, competitive gaps |
| QA | Edge cases, failure modes, test coverage, state explosion | Crash paths, data corruption, race conditions, invalid states |

### Output Structure

Each lens produces:
- **10 positive user stories**: "As a [role], I can [action] so that [benefit]"
- **10 negative user stories**: "As a [role], I cannot [action] because [reason], causing [harm]"
- **Evidence markers**: ✅ verified, ⚠️ plausible, ❌ uncertain — on every claim
- **Severity**: low / medium / high / critical for negative stories

Total output: 100 user stories (50 positive, 50 negative) + synthesis report.

## Workflow

### Step 1: Understand the Target

Read the target codebase, skill, design doc, or idea:
- If a skill: Read the SKILL.md, plugin.json, README, and any agent files
- If a codebase: Explore the architecture, read key files
- If a design doc: Read it fully, note scope and constraints
- If an idea: Clarify scope with the user if ambiguous

### Step 2: Cite Your Sources

Before generating any stories, identify and cite:
- Files read (path:line)
- Documentation referenced
- Code patterns observed
- Design decisions noted

Every claim in the output MUST trace back to a source. Unverified claims get ❌ markers.

### Step 3: Spawn 5 Lens Agents

Use the Task tool with `subagent_type='general-purpose'` to spawn 5 parallel agents:

**Agent 1 — Engineering:**
```
Prompt: "You are the Engineering lens for a 360 review. Analyze [target].
Generate exactly 10 positive and 10 negative user stories.
Each story must follow: 'As a [role], I can/cannot [action] so that/because [reason].'
Mark every claim: ✅ verified from source, ⚠️ plausible but unverified, ❌ cannot verify.
Rate negative stories: critical / high / medium / low.
Focus on: architecture, code quality, maintainability, performance, integration complexity."
```

**Agent 2 — Security:**
```
Prompt: "You are the Security lens for a 360 review. Analyze [target].
Generate exactly 10 positive and 10 negative user stories.
Each story must follow: 'As an [attacker/role], I can/cannot [action] so that/because [reason].'
Mark every claim with evidence markers.
Focus on: OWASP top 10, data exposure, auth boundaries, injection vectors, secrets handling."
```

**Agent 3 — UX:**
```
Prompt: "You are the UX lens for a 360 review. Analyze [target].
Generate exactly 10 positive and 10 negative user stories.
Each story must follow: 'As a [user/role], I can/cannot [action] so that/because [reason].'
Mark every claim with evidence markers.
Focus on: accessibility, onboarding, error states, flow gaps, learnability, confusion points."
```

**Agent 4 — CEO/Strategy:**
```
Prompt: "You are the CEO/Strategy lens for a 360 review. Analyze [target].
Generate exactly 10 positive and 10 negative user stories.
Each story must follow: 'As a [stakeholder/role], I can/cannot [action] so that/because [reason].'
Mark every claim with evidence markers.
Focus on: cost/benefit, opportunity cost, market fit, timing, adoption resistance, ROI failure."
```

**Agent 5 — QA:**
```
Prompt: "You are the QA lens for a 360 review. Analyze [target].
Generate exactly 10 positive and 10 negative user stories.
Each story must follow: 'As a [system/role], I can/cannot [action] so that/because [reason].'
Mark every claim with evidence markers.
Focus on: edge cases, failure modes, test coverage gaps, state explosion, crash paths, race conditions."
```

### Step 4: Synthesize Results

After all 5 agents complete (100 stories total):

1. **Count by lens**: How many positive/negative per lens
2. **Severity distribution**: Critical / high / medium / low counts
3. **Evidence quality**: ✅ / ⚠️ / ❌ ratio — what's verified vs. unverified
4. **Top patterns**: Recurring themes across lenses
5. **Recommendations**: What to fix first, what to double down on

### Step 5: Report

Output format:

```
═══ 360 REVIEW: [Target Name] ═══

## Engineering Lens
✅ Verified claims: [N] | ⚠️ Plausible: [N] | ❌ Unverified: [N]

### Positive Stories (10)
1. [✅] As a developer, I can... so that...
2. [⚠️] As a developer, I can... so that...
...

### Negative Stories (10)
1. [✅] [CRITICAL] As a developer, I cannot... because..., causing...
2. [⚠️] [HIGH] As a developer, I cannot... because..., causing...
...

--- repeat for Security, UX, CEO/Strategy, QA ---

═══ SYNTHESIS ═══
Total stories: 100 (50 positive, 50 negative)
Severity breakdown: Critical: N, High: N, Medium: N, Low: N
Evidence quality: ✅ N% verified, ⚠️ N% plausible, ❌ N% unverified

### Top 5 Themes
1. [Theme] — appears in [N] lenses — [brief summary]
2. ...

### Most Critical Issues (must fix)
1. ...

### Most Valuable Strengths (double down)
1. ...

### Recommendations
- Short-term (fix now):
- Medium-term (next iteration):
- Long-term (strategic):
```

## Evidence Markers

- **✅ Verified** — Claim confirmed from source (file:line, documented behavior, test output)
- **⚠️ Plausible** — Reasonable inference but no direct source citation
- **❌ Cannot verify** — Speculative claim requiring human investigation

Unsupported numerical claims are forbidden. "I don't know" is valid output.

## Success Criteria

- 100 user stories generated (50 positive, 50 negative across 5 lenses)
- Every story has an evidence marker
- Negative stories have severity ratings
- Synthesis identifies recurring themes and actionable recommendations
- Output is saved to file if user requests

## Tools Used

- **Task (subagent_type='general-purpose')**: Spawn 5 parallel expert agents
- **Read**: Analyze the target (SKILL.md, code, design docs)
- **Explore agent**: Understand codebase structure if needed
- **Grep**: Find specific patterns or issues
- **Bash**: Run tests or validations on the target

## Integration with Sigil

This skill complements Sigil — where Sigil produces certification certificates (verdicts, gate results), 360 Review produces detailed user stories (qualitative exploration). Use Sigil for certification, 360 Review for discovery.

For marketplace-eligible skills, run:
1. 360 Review → understand strengths and gaps
2. Sigil certification → get the structured certificate
3. Fix issues from 360 Review
4. Re-certify with Sigil
5. Submit to marketplace

## Citation Discipline

- Every story references a source file, line, or documented behavior
- No numerical claims without backing evidence
- "I don't know" is preferred over speculation
- Evidence markers are REQUIRED on every story
