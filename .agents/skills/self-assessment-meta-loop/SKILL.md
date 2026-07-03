---
name: "self-assessment-meta-loop"
description: "KEYSTONE CHORUS skill. Runs at end of every flywheel cycle: 4-question audit (quality, domain gaps, community signals, memory staleness). Detects deficits, spawns builders. Plus weekly Human Faculties Framework deep pass. This is the threshold between a tool and a cognitive architecture."
license: MIT
metadata:
  tier: "DEEP"
  category: "Meta / Cognitive Architecture"
---

# Self-Assessment Meta-Loop

## Purpose

**The keystone of the CHORUS flywheel.** The meta-cognitive audit cycle that transforms the system from bounded competence (runs what it has) to open-ended growth (acquires what it doesn't have). This is the threshold between a tool and a cognitive architecture.

Without it, the other 11 skills are holes you'll see but only a human can fill. With it, the system detects its own deficits and spawns research/building to fix them automatically. The meta-loop IS the flywheel applied to itself.

## When to Run

**At the end of EVERY flywheel cycle** — this is the keystone stage. After scorecard-auditor produces the quality assessment, the meta-loop fires immediately.

Also run:
- After every 3-5 new skills added to the toolbelt
- When the flywheel encounters a class of problem it repeatedly fails at
- When the user asks "what are we missing?"
- Weekly session startup audit (run the full Human Faculties Framework deep pass)
- After any significant architecture change

**Activation phrases:**
- "audit our capabilities"
- "what faculties are we missing"
- "self-assessment"
- "run the meta-loop"
- "gap analysis on our skills"
- "what are we not seeing"
- "flywheel self-audit"

## The 4-Question Audit Engine (Core Loop)

At the end of every flywheel cycle, ask exactly these 4 questions. Each has a detection signal and an action. No more, no fewer — brevity is the point. The meta-loop fails when it tries to be exhaustive instead of actionable.

| # | Question | Detection Signal | Action on "yes" |
|---|----------|----------------|-----------------|
| 1 | **Did any stage produce low-quality output 3+ times?** | Check scorecard history for below-threshold scores (<70/100 on any lens) in recent flywheel cycles | Spawn research agent: investigate root cause, propose structural fix (not retry). Possible causes: weak skill prompt, wrong model tier, missing reference data. |
| 2 | **Is there a domain the system keeps referencing but has no skill for?** | Scan flywheel logs / conversation context for "unknown domain", "failed lookup", "no matching skill", or fallback pathways triggered repeatedly | Run `skills-god.sh search` for equivalent. If none found, scaffold new skill. Wire into toolbelt. |
| 3 | **Are there new community signals about a gap?** | Check Reddit/HN/Twitter for "Shopify + [pain point]" or "Claude Code + [missing capability]" patterns since last cycle | Research the pain point. If it's a genuine gap and no skill exists, create one. |
| 4 | **Is memory stale (long gaps between reads of key docs)?** | Audit doc access timestamps against `last_read` in memory graph. Key docs read >7 days ago = stale. | Re-index stale docs through knowledge-extraction-engine, or summarize for hot memory (STICKY.md / STATE.md). |

### Execution

1. Answer each question deterministically from available data (log files, scorecard outputs, doc timestamps)
2. If the signal is ambiguous, answer "no" — the meta-loop does not fabricate detective work
3. For each "yes", spawn ONE action. Max 2 actions per cycle (prevents proliferation)
4. Report what was detected and what action was taken
5. If all 4 are "no" — output `self-assessment: CLEAN` and exit

### Quick Mode (every cycle)

```json
{
  "cycle_number": 142,
  "questions": [
    {"q": "low-quality output 3+?", "signal": false, "action": null},
    {"q": "domain with no skill?", "signal": true, "action": "SPAWNED: knowledge-extraction-engine for 'citation-intake' pattern"},
    {"q": "community gap signal?", "signal": false, "action": null},
    {"q": "memory stale?", "signal": false, "action": null}
  ],
  "actions_taken": 1,
  "verdict": "SELF_IMPROVING"
}
```

## The Human Faculties Framework (Deep Pass — Weekly or On Request)

A periodic deeper analysis using the human-equivalent intelligence framework. Runs on explicit request or weekly session startup. Complements the 4-question engine with faculty-level scores.

| Faculty | Definition | Measures |
|---------|-----------|----------|
| IQ (Analysis) | Pure reasoning, pattern matching, logic | Scorecard Auditor accuracy, Skeptic hit rate |
| EQ (Human reading) | Reading user state (frustration, fatigue, confusion) | User sentiment, rephrase rate, patience threshold |
| Resilience | Recovery from failure, approach-switching | Retry patterns, cross-approach escalation |
| Determination | Sustained effort on hard problems | Iteration depth, budget governors |
| Inventiveness | Structured creativity, new solutions | Novel approach ratio, cross-domain transfer |
| Memory | Episodic + semantic recall across sessions | Fact accuracy, context recovery speed |
| Research | Finding new knowledge | Source diversity, extraction quality |
| Senses | Environmental awareness (browser, files, community) | Coverage breadth, monitor depth |

### Deep Pass Steps

### Step 1 -- Audit Toolbelt
Use skills-god to list all installed skills. Scan the manifest. Check each skill's category (E-commerce, Engineering, etc.) and tier (QUICK, STANDARD, DEEP).

### Step 2 -- Evaluate Each Faculty
For each of the 8 faculties, ask:
- Do we have a skill/script that directly serves this?
- What evidence exists that this faculty works? (Test results, actual outputs)
- Is this faculty silent-failing? (No alerts when it breaks)

### Step 3 -- Generate Gap Report
Produce structured gap analysis:
```json
{
  "timestamp": "ISO-8601",
  "faculties": {
    "iq": {"score": 4, "evidence": "scorecard-auditor + skeptic", "gap": "No adversarial cross-validation"},
    "eq": {"score": 1, "evidence": "none", "gap": "NO faculty for reading user state or adapting behavior"}
  },
  "gaps": [
    {"faculty": "eq", "severity": "HIGH", "consequence": "Cannot detect user frustration -- power through when should pivot"},
    {"faculty": "inventiveness", "severity": "MEDIUM", "consequence": "Stays in known patterns, no structured ideation"}
  ],
  "recommended_skills": [
    "eq-user-reading -- detect user frustration, confusion, fatigue",
    "stickiness-framework -- structured inventiveness via constraint expansion"
  ]
}
```

### Step 4 -- Spawn Skill Builders
For each HIGH/MEDIUM gap, spawn a research agent that:
1. Searches `claude-skills-marketplace` for existing equivalent
2. If none found, designs a new skill spec
3. Returns: "PROCEED" (no equivalent found, build new) or "EXISTS at path"
4. If PROCEED, builds the skill using the marketplace CLAUDE.md conventions

### Step 5 -- Wire Into Flywheel
After building:
1. Run `skills-god.sh ensure`
2. Register in manifest
3. Flag as `self-assessed: PASS` in the skill metadata
4. Update STICKY.md with new capability

## Approach

- **Every cycle**: run the 4-question engine. Fast, deterministic, actionable. Target: <5s overhead.
- **Weekly or on request**: run the full Human Faculties Framework deep pass. Target: <30s overhead.
- Start from evidence, not beliefs: check real log outputs, scorecard history, doc timestamps
- If signal is ambiguous, answer "no" — do not fabricate detective work
- Max 2 actions per cycle (prevents proliferation even in deepest passes)
- Spawn research agents only when the question is "yes" and the action requires investigation
- Heavyweight skills (>200 lines SKILL.md) run through Sigil scorecard before wiring

## Guardrails

- MAX 2 new skills per audit cycle (prevents proliferation across both modes)
- Quick mode caps at 1 action. Deep mode at 2. Never both running same cycle.
- New skill must pass the "would a human need this?" test
- If all 4 questions answer "no", output `self-assessment: CLEAN` — no actions, no docs, no overhead
- Heavyweight skills (>200 lines SKILL.md) run through Sigil scorecard before wiring
- Quick mode must complete in under 5s overhead. Deep mode under 30s.
- Never fabricate detective work — ambiguous signal = "no"

## Tools Used

- **Bash**: Run `skills-god.sh` to list installed skills and check manifest
- **Grep/Glob**: Search `claude-skills-marketplace/` for existing equivalents before spawning new builds
- **Read**: Inspect existing SKILL.md files for capability mapping; audit doc access timestamps
- **Agent (research)**: Spawn research sub-agents for Q1 root cause analysis, Q3 community signal exploration, and deep pass gap-filling
- **Write**: Create new SKILL.md files for approved gap-filling skills
- **Python (scorecard history)**: Parse scorecard output files for below-threshold patterns

## Output

### Quick Mode (every cycle)
Inline JSON status appended to flywheel cycle log: `{"cycle": N, "meta": {"q1": false, "q2": true, "action": "SPAWNED: ..."}}`

### Deep Mode (weekly / on request)
Structured audit report saved to `docs/audit/self-assessment-{YYYY-MM-DD}.md` including:
- 4-question engine results since last deep pass
- Faculty scores (0-5 per dimension with cited evidence)
- Gap table with severity and consequence
- Recommended builds
- Skills-god manifest snapshot

## Success Criteria

- Quick mode runs at end of every flywheel cycle in under 5s
- 4 questions answered deterministically from real data (not fabricated)
- "yes" answers produce concrete actions (not just flags)
- Max 1 action per cycle in quick mode, max 2 in deep mode
- Faculty gap report (deep mode) has cited evidence for every score
- New skills pass marketplace CLAUDE.md conventions review
- STICKY.md updated with new capabilities from deep pass
- `self-assessment: CLEAN` is a valid, routine output — the system is stable, not broken

## Integration

- `scripts/chorus-loop.sh` -- **Stage 6**: fire 4-question engine after every scorecard-auditor evaluation
- `scripts/skills-god.sh` -- source of truth for installed skills
- STICKY.md -- update with findings from deep pass
- Session startup -- run quick 4-question check; if any "yes" in last 24h, investigate
- Sigil scorecard -- heavyweight skills gate before wiring
- `knowledge-extraction-engine` -- used for Q2 (domain gap → extract pattern) and Q4 (re-index stale docs)
- `reddit-community-monitor` -- used for Q3 (community signal detection) in deep pass
