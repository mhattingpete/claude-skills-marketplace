---
name: "failure-generator"
description: "Adversarial stress-test protocol for Claude Code skills. Activates when users want to test a skill, find its failure modes, calibrate accuracy, run a stress test, or validate robustness."
license: MIT
metadata:
  tier: "STANDARD"
  category: "Engineering / Quality Assurance"
---

# Failure Generator

## Purpose

Test whether a skill produces structurally sound but factually wrong outputs. The goal is to find where it silently fails.

Most testing confirms a skill works on clean inputs. The failure generator flips this: feed deliberately difficult, edge-case, or adversarial inputs and observe where the output looks correct but is actually wrong. A skill that produces confident-sounding nonsense is more dangerous than one that crashes.

## When to Use

Invoke this skill explicitly:

- "stress test {skill}"
- "find failure modes of {skill}"
- "calibrate {skill}"
- "run failure generator on {skill}"
- "what breaks when I ask {skill} to handle {unusual-input}"

Do not use this skill when you need a skill to perform normally. This is a diagnostic, not a production workflow.

## Protocol

Run the target skill against each test store below. For each run, record the observation log. After all 4 runs, classify failures and produce the calibration dashboard.

### Test Stores

#### 1. Liquid Death (mountain-water canned beverage)

- **Brand profile**: irreverent, death-metal aesthetic, anti-corporate, sparse brand copy, voice lives on TikTok/Instagram not the About page
- **Product category**: canned still/sparkling water and iced tea
- **Expected failure mode**: over-formalization — the skill will write polite, professional brand copy that sounds nothing like Liquid Death
- **Trap**: the About page says "kill your thirst" but the real brand voice is in short-form video, not the web copy. A scraping-only skill misses it entirely.

#### 2. Red Blossom Tea (specialty tea importer, San Francisco)

- **Brand profile**: serene, literary, terroir-focused, narrative-rich descriptions
- **Product category**: premium Chinese/Taiwanese tea
- **Expected failure mode**: too accurate on voice but misses commercial logic — produces beautiful copy that doesn't convert, ignores urgency, doesn't prompt purchase
- **Trap**: the voice is easy to replicate. The harder problem is balancing it with direct-response commerce signals. A skill that nails voice but omits CTA or scarcity fails silently.

#### 3. Gymshark (fitness apparel)

- **Brand profile**: fitness community, influencer-heavy, aspirational, UK-founded
- **Product category**: men's and women's athletic wear
- **Expected failure mode**: confuses community voice with brand voice — produces "we are a community" copy when the brand actually sells aspirational identity, not belonging
- **Trap**: the About page emphasizes "community" but the real brand transaction is "become the person who trains like this." A skill that parrots the About page misses the psychological transaction.

#### 4. Broken English store (<10 products, broken descriptions)

- **Brand profile**: fragmented, incomplete, mismatched product images and descriptions, missing fields
- **Product category**: miscellaneous (clearance items, discontinued lines)
- **Expected failure mode**: over-interpretation — the skill will invent coherent brand narratives from noise. It will "fix" the brokenness by hallucinating consistency.
- **Trap**: the correct output is "this store has no coherent brand." A skill that produces polished copy from garbage input is silently wrong — it should flag the input quality instead.

### Execution

1. For each store, gather available public-facing content (About page, product descriptions, social media snippets if accessible).
2. Run the target skill with the gathered content as input.
3. Record the input, output, and your assessment in the observation log.
4. Do not cherry-pick stores. Run all 4 in sequence.

## Observation Log Template

Run this for each store. Use JSON.

```json
{
  "run_id": "failure-gen-YYYYMMDD-HHMM",
  "test_store": "Liquid Death | Red Blossom Tea | Gymshark | Broken English",
  "target_skill": "<skill name being tested>",
  "input": {
    "source_material": ["About page", "Product descriptions (count)", "Social snippets (count)"],
    "notes": "Any caveats about input quality or availability"
  },
  "output": "<full output from the skill, or summary if too long>",
  "assessment": {
    "structurally_sound": true | false,
    "factually_correct": true | false,
    "voice_accuracy": 1-5,
    "commercial_sense": 1-5,
    "would_ship_to_client": true | false,
    "failure_modes_detected": ["string list"]
  },
  "skeptic_review": {
    "skeptic_accuracy_score": 0.0-1.0,
    "false_positive_claims": 0,
    "false_negative_claims": 0,
    "skeptic_notes": "Was the skeptic right about the failure? Did it catch everything?"
  }
}
```

## Failure Mode Classification

Classify each issue detected in the assessment into one of these categories:

| Failure Mode | Description | Signal |
|---|---|---|
| **Over-formalization** | Output is too formal, polite, or corporate for the actual brand voice | Reads like a bank wrote it. No edge. |
| **Hallucinated authority** | Output invents credentials, awards, certifications, or historical facts | Check every claim. Survival tip: search "X award" + brand name. |
| **Voice drift** | Output captures the general topic but shifts into a different brand voice halfway through | Reads like two different people wrote it. Tone inconsistency. |
| **Sparse over-interpretation** | Output invents a coherent brand narrative from fragmentary or broken inputs | Polished output from garbage input. The smoothness is the bug. |
| **Skeptic false negative** | The in-house critic (if one exists) approves output that is actually wrong | False sense of safety. The critic validated bad output. |
| **Skeptic false positive** | The in-house critic flags output that is actually correct | Wasted time. The critic cried wolf. |

### Severity Levels

- **Critical**: Output would damage the brand or mislead a customer if shipped (hallucinated authority, voice drift to wrong identity).
- **High**: Output is wrong but would not immediately cause damage (over-formalization on an irreverent brand).
- **Medium**: Output is correct but misses the point (voice is right, no commercial logic).
- **Low**: Output is correct but a human would still polish it. Not a real failure.

## Calibration Dashboard

After all 4 stores are run, produce a summary:

```json
{
  "calibration_run": {
    "date": "YYYY-MM-DD",
    "target_skill": "<skill name>",
    "stores_tested": 4,
    "total_outputs": 4,
    "outputs_needing_correction": 0,
    "correction_rate_pct": 0.0
  },
  "failure_mode_distribution": {
    "over_formalization": {"count": 0, "stores": []},
    "hallucinated_authority": {"count": 0, "stores": []},
    "voice_drift": {"count": 0, "stores": []},
    "sparse_over_interpretation": {"count": 0, "stores": []},
    "skeptic_false_negative": {"count": 0, "stores": []},
    "skeptic_false_positive": {"count": 0, "stores": []}
  },
  "severity_breakdown": {
    "critical": 0,
    "high": 0,
    "medium": 0,
    "low": 0
  },
  "skeptic_accuracy": {
    "overall_score": 0.0,
    "true_positives": 0,
    "false_positives": 0,
    "false_negatives": 0
  },
  "recommendation": "GO | CONDITIONAL_GO | NO_GO"
}
```

### Correction Rate Interpretation

| Rate | Verdict | Meaning |
|---|---|---|
| < 10% | Lenient | Skill passes the easy tests. Run harder inputs or lower your standards are wrong. |
| 10-30% | Healthy | Skill is useful but needs human review. This is the target zone for production tools. |
| 30-50% | Brittle | Skill works in narrow band. Document the known working conditions. |
| > 50% | Wrong architecture | The approach is fundamentally wrong. Redesign, don't patch. |

### Recommendation Rules

- **GO**: correction_rate < 10% AND no critical findings. Ship without reservation.
- **CONDITIONAL_GO**: correction_rate 10-30% OR 1-2 high findings. Ship with documented caveats and human review gate.
- **NO_GO**: correction_rate > 30% OR any critical finding. Do not ship. Fix or replace.

## Success Criteria

After a full 4-store run:

1. You know what percentage of the target skill's outputs need human correction.
2. You have a distribution of failure modes (which failure types dominate).
3. You have a Skeptic accuracy score (how well the in-house critic detects these failures).
4. You have a GO/CONDITIONAL_GO/NO_GO recommendation supported by data, not opinion.
5. At least one previously unknown failure mode is documented.

If after the run you cannot answer all 5, the failure generator run is incomplete. Re-run with more attention to classification.

## Output

Produce a structured comparison report containing:

1. **Executive summary**: one-paragraph verdict with correction rate and recommendation.
2. **Per-store results**: all 4 observation logs inline.
3. **Failure mode distribution**: table with counts per mode and severity.
4. **Skeptic accuracy assessment**: score and analysis of false negatives.
5. **Recommendation**: GO / CONDITIONAL_GO / NO_GO with supporting evidence.
6. **Action items**: if CONDITIONAL_GO, what to fix. If NO_GO, what to redesign. If GO, what to monitor.

The report is the artifact. Share it, file it next to the skill, and reference it when the skill is used in production.

## Related

- `/adversarial-reviewer` — code-level adversarial review (different scope: single diff review, not brand/content skill calibration)
- `/stress-test` — broader load/performance stress testing
- `/skill-tester` — functional test authoring for skills (unit tests, not adversarial calibration)

## Integration Contract

**Role in CHORUS flywheel:** Calibration/Diagnostic (outside the main loop) — stress-tests the pipeline before deployment.

This skill is NOT part of the production flywheel loop. It is a diagnostic tool used during calibration. Per the Parliament's recommendation: "Don't include failure-generator in the loop (it's a calibration tool)."

**Integration rules:**
- Run failure-generator during bootstrap/calibration before enabling the CHORUS pipeline
- Do NOT include in the production loop (monitor → brand → generate → challenge → score)
- Output is a Calibration Dashboard that identifies pipeline failure modes, not a pipeline artifact
- Pipeline components (brand-profile-decoder, chorus-surface-generator, scorecard-auditor) are the calibration targets
- BrandProfile schema at `src/aeo/schemas/brand_profile.py` is the reference contract — the failure-generator tests what happens when inputs violate this contract
