---
name: "determination-protocol"
description: "Cross-approach escalation ladder for stubborn problems. When direct approaches fail, systematically escalate through model swaps, strategy shifts, tool changes, and problem decomposition — never retry harder, always retry differently."
license: MIT
metadata:
  tier: "STANDARD"
  category: "Engineering / Methodology"
---

# Determination Protocol

## Purpose
The CHORUS brain's "determination" faculty. When a direct approach fails to solve a problem (test fails, build breaks, skill returns wrong answer, tool errors), this protocol escalates systematically through four levels — never trying the same thing harder, always switching to a different approach. This is what separates a brute-force retry loop from genuine resilience.

## When to Use
- A test is failing after 3 fix attempts
- A build keeps breaking with the same error
- A skill keeps producing wrong answers
- A tool consistently errors
- The diminished-retries-guard fires BLOCKED or CIRCUIT_BREAKER
- "Nothing I've tried works on this"
- "I'm stuck, need to escalate"

## The Escalation Ladder (4 Levels)

### Level 1 — Model Swap (cheapest)
The first thing to change is WHICH model drives the solution. Models have different strengths, biases, and failure modes.

| Current Model | Swap To | Why |
|--------------|---------|-----|
| Sonnet 4.6 | Haiku 4.5 or vice versa | Different architecture, different failure modes |
| DeepSeek | Claude or vice versa | Different training, different reasoning patterns |
| Haiku | Sonnet | More capable, more expensive — justified when stuck |
| Default | Explicit reasoning model | "Think step by step" prompt addition |

**How:**
1. Set explicit model override in the agent() or tool call
2. Do NOT change anything else — same approach, different model
3. If it works: note the model-sensitive pattern in STICKY.md
4. If ≤2 attempts at this level fail → escalate

### Level 2 — Strategy Swap
Change the entire approach to the problem. Not a parameter tweak — a formula family change.

**Strategy archetypes to rotate through:**
- **Top-down**: Design first, implement from spec
- **Bottom-up**: Build the simplest thing, verify, extend
- **Outside-in**: Write the test/user story first, implement to pass
- **Divide-and-conquer**: Cut the problem in half, solve each independently
- **First-principles**: Throw out all prior work, derive from axioms
- **Analogy**: "How would this be solved in a different domain?"
- **Heuristic**: "What's the cheap solution that works 80% of the time?"
- **Inversion**: "What would make this fail? How do I avoid that?"

**How:**
1. Name the current strategy (e.g., "top-down spec-to-implement")
2. Name at least one alternative (e.g., "bottom-up: implement the minimal case")
3. Execute the alternative with zero code reuse from the failed attempt
4. If it works: document "strategy {X} works for problem class {Y}"
5. If ≤2 strategies tried → escalate

### Level 3 — Tool Swap
Change the implementation tools entirely. This is a bigger escalation — it may mean rewriting.

**Tool archetypes:**
- **High-level → Low-level**: Python script → raw bash/curl
- **Third-party → Manual**: Plugin → hand-coded equivalent
- **Sync → Async**: Blocking → event-driven
- **Library → Protocol**: HTTP library → raw socket
- **GUI → CLI**: Browser automation → curl + grep

**How:**
1. Identify the current tool stack
2. Pick a different-level tool (low-level rules if high-level failed)
3. Re-implement from scratch with the new tool
4. If it works: add tool preference to the skill's SKILL.md

### Level 4 — Decompose & Distribute
The problem is too big for a single approach. Split it up.

**How:**
1. List sub-problems that the current approach combines
2. Solve each sub-problem independently with potentially different approaches
3. Re-compose the solutions
4. Verify each sub-solution independently before integration

## Process

### Step 1 — Diagnose Failure Mode
Before escalating, diagnose: what exactly failed?
- **Algorithmic**: Wrong answer, logic error → Level 1 or 2
- **Tool limitation**: Tool doesn't support the pattern → Level 3
- **Scope too large**: Context overflow, timeout → Level 4
- **Random flake**: Non-deterministic → log and retry once, then escalate
- **Silent wrong**: Produced plausible but incorrect output → Level 2 (different strategy)

### Step 2 — Execute Escalation
Walk the ladder in order. At each level:
1. Name what you're changing (model/strategy/tool/decomposition)
2. Explain WHY the previous attempt failed (not just "didn't work")
3. Execute the new approach with zero assumptions from prior attempts
4. Verify the result

### Step 3 — Record
If an escalation level produces a fix, record:
```json
{
  "problem_fingerprint": "string - keywords or error pattern",
  "failed_levels": ["1", "2"],
  "solved_at": "3 - tool swap",
  "what_worked": "Used curl instead of Python requests library",
  "pattern": "tool-swap required for HTTP/2 proxy issues"
}
```

### Step 4 — Update Knowledge
If the same failure mode has hit this level before (check STICKY.md gotchas), skip directly to the known solution level.

## Escalation Budget
| Level | Max Attempts Per Problem | Cumulative Cost |
|-------|------------------------|-----------------|
| 1 - Model swap | 2 | Low (different API call) |
| 2 - Strategy swap | 2 | Medium (new code) |
| 3 - Tool swap | 1 | High (full rewrite) |
| 4 - Decompose | 1 | Highest (multi-agent) |

Total budget: 6 attempts per problem. After all exhausted → HUMAN_ESCALATE. Do NOT loop back to Level 1.

## Success Criteria
- Every failure is diagnosed NOT just retried
- Each escalation level changes one structural thing (model OR strategy OR tool)
- No blind retries at the same level
- Escalation paths are recorded for knowledge base
- Human escalation falls through cleanly with full problem context
- Budget never exceeded without explicit user consent

## Integration
- Diminishing retries guard (BLOCKED/CIRCUIT_BREAKER → invoke determination-protocol)
- Skills God (failed skill invocation → try Level 2 strategy swap)
- STICKY.md gotchas (read problem fingerprints before starting)
- self-assessment-meta-loop (records which faculties needed escalation)
