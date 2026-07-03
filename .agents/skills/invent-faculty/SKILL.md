---
name: "invent-faculty"
description: "CHORUS Stage 6 — divergent generation via adversarial constraint injection. Fills the inventiveness faculty gap (the last faculty). When standard output scores <70/100, injects novel constraints and regenerates. GAN-inspired: Generator → Critic → Regenerate until quality threshold met."
license: MIT
metadata:
  tier: "STANDARD"
  category: "E-commerce / Surface Generation"
---

# INVENT — Divergent Generation Faculty

## Purpose

The inventiveness faculty for the CHORUS brain. Activates when standard generation produces competent-but-mediocre output. Injects adversarial constraints (voice mutation, category swap, commerce model flip) to force the generator out of its local optimum, then re-evaluates. This is the GAN-inspired Generator → Critic → Regenerate loop that prevents the flywheel from converging on bland, safe output.

Without INVENT, the flywheel produces the most probable output — correct, safe, forgettable. With INVENT, it explores the edges of the solution space and surfaces what's genuinely novel.

## When to Run

**Automatic trigger:** When `scorecard-auditor` (Stage 5) returns < 70/100 on any lens for a generated surface. The flywheel fires INVENT immediately before declaring the surface as FAIL.

**Manual trigger:**
- "make this more creative"
- "that's too safe, give me something unexpected"
- "try a completely different angle"
- "what would a competitor never do?"
- "invent a new approach"
- "be more interesting"

## Process

### 1. RECEIVE: Original surface + scorecard findings

Input includes:
- The surface that failed quality gate (concierge / product_finder / smart_compare JSON)
- The scorecard findings showing WHY it failed (which lenses, specific issues)
- The Brand Profile (so mutations stay on-brand even when diverging)

### 2. SELECT: Constraint injection strategy

Pick ONE strategy per mutation. Rotate strategies across mutations (never use the same one twice in a row):

| Strategy | Injection | Example |
|----------|-----------|---------|
| **Voice flip** | Move to adjacent register (warm_authority → irreverent_expert, minimalist → poetic) | RBT "serene educator" → "your tea-obsessed friend who found something incredible" |
| **Category swap** | Restructure around a different category as the entry point (premium → value, tea → wellness) | "Which oolong?" → "What feeling are you chasing today?" |
| **Constraint remove** | Remove the most restrictive filter (price floor, persona, aesthetic) | Drop the $8-120 range entirely — what does the brand say when money isn't mentioned? |
| **Constraint add** | Inject an artificial constraint that forces novel structure | "This must recommend EXACTLY ONE product — no options, no categories. Convince them. |
| **Format flip** | Change output format entirely (quiz → letter, matrix → story) | Instead of a comparison table, write a letter from the founder comparing two teas |
| **Anti-brand** | Generate the opposite of brand voice, then invert it | Write it in corporate MBA-speak, then translate back to brand voice. The gaps reveal themselves. |

### 3. MUTATE: Generate constrained variation

Feed the original surface + the constraint to the generator. Instruction format:

```
ORIGINAL SURFACE:
{surface_json}

CONSTRAINT:
Apply strategy: {strategy}
Specific injection: {detailed_constraint}

Regenerate the surface to satisfy this constraint while preserving brand identity.
Output MUST differ structurally from the original, not cosmetically.
```

### 4. CRITIC: Evaluate mutation against original

Compare the mutation to the original on 4 dimensions:

| Dimension | What it measures | Weight |
|-----------|-----------------|--------|
| **Novelty** | Is this structurally different from the original, not just reworded? | 0.35 |
| **Brand fidelity** | Does it still sound like the brand, even if it reads differently? | 0.30 |
| **Merchant readiness** | Can this be deployed? All references resolvable? | 0.20 |
| **Commercial sense** | Does it still convert? Not sacrificing efficacy for novelty. | 0.15 |

Score each 0-10. Weighted sum = mutation_score.

### 5. DECIDE: Accept, retry, or reject

| Condition | Action |
|-----------|--------|
| Mutation score >= 7.0 AND >= original score | **ACCEPT** — replace original with mutation, declare INVENT SUCCESS |
| Mutation score >= 7.0 BUT < original score | **KEEP BOTH** — surface original as safe default, flag mutation as "INVENT: alternative approach" |
| Mutation score < 7.0 AND retries < 3 | **RETRY** — pick a different strategy from Step 2, mutate again with previous mutations as seen list |
| Mutation score < 7.0 AND retries >= 3 | **REJECT** — surface original with note: "INVENT exhausted 3 strategies. Last gap remains open." |

### 6. OUTPUT: Mutation summary

```json
{
  "invent_stage": {
    "surface_type": "concierge",
    "original_score": 62,
    "strategies_tried": ["voice_flip", "constraint_remove"],
    "best_mutation_score": 7.3,
    "verdict": "ACCEPT",
    "mutations": [
      {
        "strategy": "voice_flip",
        "score": 7.3,
        "diff_summary": "Changed register from warm_authority to warm_curator. Greeting now invites exploration instead of offering guidance. Category entry points restructured around feeling-states instead of product types.",
        "accepted": true
      },
      {
        "strategy": "constraint_remove",
        "score": 5.8,
        "diff_summary": "Removed price anchors. Output became too abstract — lost commercial signals entirely.",
        "accepted": false
      }
    ],
    "last_gap_status": "CLOSED — inventiveness faculty operational via adversarial constraint injection"
  }
}
```

## Integration

**Role in CHORUS flywheel:** Stage 3.5 (Generation Bootstrap) — fires between Stage 3 (Generate) and Stage 4/5 when surfaces score below threshold.

**Trigger contract:** Activated by `scorecard-auditor` output when any lens score < 70/100.

**Input:** Failed surface JSON + scorecard findings + Brand Profile.

**Output:** Mutation summary with accepted/kept/rejected verdicts. If ACCEPT, replaces the original surface in the pipeline.

**Cross-skill use:**
- `scorecard-auditor` — provides the quality signal that triggers INVENT
- `chorus-surface-generator` — the generator INVENT mutates
- `knowledge-extraction-engine` — can inform constraint selection with "what hasn't been tried in this domain"

## Guardrails

- MAX 3 mutations per surface per cycle
- NEVER mutate a surface that scored >= 70/100 (it passed — ship it)
- NEVER use the same strategy twice in a row (forces exploration)
- Mutation must preserve brand identity even when diverging
- If 3/3 mutations fail, surface original with INVENT note — don't silently discard
- Budget: $0.15 per mutation attempt (capped at $0.45 per cycle)
