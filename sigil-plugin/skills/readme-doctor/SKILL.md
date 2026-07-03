---
name: readme-doctor
description: 5-lens README and documentation audit with automated rewrite. Spawns parallel expert agents (Engineering, Security, UX, CEO/Strategy, QA) to review any README, landing page, or documentation for overclaiming, audience gaps, missing trust signals, and structural issues — then rewrites it.
triggers:
  - review this readme
  - audit this readme
  - fix this readme
  - review this documentation
  - check this readme for overclaiming
  - readme doctor
  - make this readme sell itself
  - doc review
  - rewrite this readme
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Agent
  - AskUserQuestion
  - Grep
---

# Readme Doctor

A Sigil-powered content audit pipeline. Reviews any README, documentation page, landing page, or marketing text through 5 expert lenses, then produces a rewritten version that is honest, audience-targeted, and self-selling.

**How this differs from the general Sigil review:** The general Sigil skill certifies code and skills with a structured verdict. This skill is specifically for *content and documentation*, and it goes further — it also *rewrites* the content, not just reports on it.

---

## Phase 0 — Pre-Flight Check (HARD GATE)

Before spawning any expert agents, run the cheapest disconfirming test to avoid wasted context:

\`\`\`bash
scripts/readme-doctor-preflight.sh <state-file> <target-path>
\`\`\`

**Exit codes:**
- **0** (PROCEED) → target valid, enter Phase 1
- **1** (BLOCKED) → target missing, empty, unreadable, not .md — report reason, stop
- **10** (WARNING) → target has template placeholders or is very large — warn but proceed

**What it saves:** The 5-agent review pipeline spends ~30s-2min + context budget. Without pre-flight, a missing or empty README wastes all 5 agents' context. These 8 checks run in < 1s total (bash only, no agent calls).

Pre-flight checks performed:
1. State file not terminated (residual from prior runs)
2. Target path exists
3. Target is a regular file (not directory)
4. Target has .md extension (case-insensitive)
5. Target is readable by current user
6. Target is not empty
7. Target is not abnormally large (>100KB)
8. Target has minimum meaningful content (>3 lines)
9. No template placeholders (TODO/FIXME/lorem ipsum)

---

## When to invoke

- Before publishing any plugin, skill, or project — the README is the first thing users see
- After writing a first draft of documentation — this catches all the common overclaiming patterns
- When a README isn't converting (low installs, user confusion, support tickets asking "what does this do?")
- Before submitting to any marketplace, Product Hunt, or HN
- Any time you need an honest, unbiased review of your own writing

---

## Pipeline

### Step 1 — Read the target + detect domain

Read the full README or documentation content. If the user provides a path, read the file. If the content is in the message, use it directly.

While reading, detect the **domain** of the project the README describes. This determines whether specialist reviewers join the core 5:

| If the README is for... | Invite these specialists |
|--------------------------|------------------------|
| DeFi / crypto / smart contract | DeFi Security Auditor, Tokenomics Reviewer |
| Healthcare / HIPAA | Compliance Specialist |
| AI / ML model or API | AI Safety Reviewer |
| Legal / terms / privacy policy | Legal Counsel |
| SaaS pricing / business model | Pricing Strategist |
| API / SDK / developer tool | Developer Experience (DX) Specialist |
| E-commerce / payments | Payments Compliance Specialist |
| Mobile app | Mobile UX Specialist |
| Frontend UI library | Design Systems Expert |
| Game | Game Designer |
| Embedded / IoT | Embedded Systems Engineer |
| Generic / undetermined | Core 5 only — no specialists needed |

Each specialist is spawned as an agent alongside the core 5, with the same citation discipline.

### Step 2 — Spawn 5 parallel core expert reviewers

Spawn all 5 agents in parallel. Each receives the full content plus their lens-specific instructions.

**Agent 1 — Engineering Lens** (agents/engineering.md + README content)

Evaluate:
- Technical accuracy — do the claims match what the code actually does?
- Overclaiming — any "12+ frameworks", "95% of secrets", "2-minute fixes" that aren't backed?
- Implementation gaps — features described that don't exist or are aspirational?
- Credibility of numbers — any fabricated statistics, unsourced percentages, unverifiable benchmarks?

Output: Up to 10 specific claims that are wrong, inflated, or unverifiable. For each: exact line, what reality says, recommended fix.

**Agent 2 — Security Lens** (agents/security.md + README content)

Evaluate:
- Security scope claims — does the README say "security-gated" when the scanner is a 13-pattern grep?
- False confidence — does any language encourage users to skip real security measures?
- Architecture overpromise — does the README imply capabilities the security mechanisms don't have?
- Certification theater — does it claim independent third-party review that is actually self-certification?

Output: Up to 10 claims that give false security confidence or overstate scope. For each: exact line, the risk, recommended fix.

**Agent 3 — UX Lens** (agents/ux.md + README content)

Evaluate:
- Pacing — does the reader get tired by section 3? Is the structure predictable to the point of skimming?
- Emotional arc — does the README hook, sustain, and land, or front-load all engagement in the first paragraph?
- Skimmability — can a reader who only reads headers and bold text get the value proposition?
- First-use path — does the reader know what to do *after* installing? Or does it end at "Install it"?
- Cognitive load — are there too many concepts stacked in the title or first paragraph?

Output: Up to 10 structural and pacing issues. For each: what the reader will feel, recommended structural fix.

**Agent 4 — CEO/Strategy Lens** (agents/ceo.md + README content)

Evaluate:
- Audience — is the target reader named? Or does it talk to everyone (which means no one)?
- Competition frame — does it compete against a named competitor (risky) or against the reader's inertia (better)?
- Social proof — is there any evidence anyone uses this? Stars, testimonials, download counts?
- Call to action — what does the reader do after reading? Is it a single, clear next step?
- Trust signals — license, "try before you install", open source, auditability?
- Monetization frame — does the reader understand if this is free, paid, tiered, OSS?

Output: Up to 10 strategic positioning issues. For each: why it fails to sell, recommended fix.

**Agent 5 — QA Lens** (agents/qa.md + README content)

Evaluate:
- Broken promises — claims that will generate support tickets on day one
- Edge case blind spots — does the README work for monorepos, polyglot projects, non-developers?
- Silent failures — does the README describe behavior that will silently fail in certain environments?
- Installation friction — any steps that assume specific tooling, OS, or configuration?
- Known issues — are limitations disclosed, or hidden?

Output: Up to 10 failure modes a user will discover in practice. For each: what will go wrong, how to disclose it.

### Step 3 — Synthesize findings

After all 5 agents return, aggregate the findings:

1. **De-duplicate** — same issue mentioned by multiple lenses counts once, with cross-references
2. **Severity** — classify each unique issue as BLOCKER / HIGH / MEDIUM / LOW
3. **Theme clusters** — group related findings (e.g., "overclaiming cluster", "audience confusion cluster")
4. **Quick wins** — issues that are trivially fixable (remove one line, add one link)
5. **Structural** — issues requiring a rewrite of a section or the whole document

### Step 4 — Rewrite

Apply the fixes in order:

1. Remove or correct ALL overclaims — every fabricated stat, every "95%" / "2 minutes" / "12+" that isn't verified
2. Remove unnamed competitor attacks — don't open as a hit piece
3. Add audience declaration — "Who this is for" section with explicit audiences named
4. Add try-before-you-install path — concrete commands the reader can run in 30 seconds
5. Add license — MIT, Apache, or whatever is correct. If none exists, add one.
6. Add "What this isn't" section — honest boundaries of what the tool does not do
7. Add known limitations — inline with each feature description, not buried in a footnotes section
8. Scope down trust signals — replace "security-gated" with "scans for 13 patterns via grep", replace "self-testing" with "7 static checks"

Style rules for the rewrite:
- **Audience-first**: Start with "Who this is for" even before "Features."
- **One call to action**: The reader should know exactly one thing to do next.
- **No competitor names**: Don't name your competition. Compete against inertia.
- **Short sections, varied structure**: Don't give every feature the same header template.
- **Inline limitations**: Put caveats right next to the claim, not at the bottom.
- **"What this isn't" section**: A short, specific list of boundaries. Builds trust by admitting limits.

### Step 5 — Show the diff

After writing the new content, show what changed:

1. **Before/After summary**: Bullet list of the most important changes
2. **Deleted section note**: If anything was removed entirely (fabricated stats, competitor attacks), flag it
3. **Diff length**: Line count comparison

### Step 6 — Offer follow-up

Ask if the user wants to:
- Apply the changes to the file (Write it)
- See a particular section rewritten differently
- Run the pipeline again on a different README

---

## Reference

See the corresponding agent files in `agents/` for the full sub-agent definitions:
- `agents/engineering.md`
- `agents/security.md`
- `agents/ux.md`
- `agents/ceo.md`
- `agents/qa.md`

See `skills/sigil/SKILL.md` for the general-purpose Sigil certification skill (use when you need a structured verdict and certificate, not a full rewrite).
