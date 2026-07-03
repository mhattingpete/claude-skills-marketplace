---
name: build-optimizer
description: Recursive build optimizer. Uses Sigil to assess current state, identify the highest-value next thing to build, build it, then re-assess and loop. Terminates when no high-value items remain worth building or re-evaluating.
triggers:
  - what should I build next
  - optimize the build order
  - recursive optimizer
  - build the next best thing
  - what's the optimal next step
  - prioritize what to build
  - build loop
  - find the highest value next step
  - recursive build
  - build until done
  - what needs to be built
  - build optimizer
  - prioritize and build
  - assess and build
  - what's next
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Agent
  - Workflow
  - AskUserQuestion
  - mcp__aeo-platform__web_search
---
# Build Optimizer

**Recursive build optimizer.** Uses Sigil to assess current state, identify the highest-value next thing to build, build it, then re-assess and loop. Terminates when no high-value items remain worth building or re-evaluating.

**Why recursive:** One-pass planning is wrong. You don't know what to build next until you've built what you just built. Each cycle reveals new context, new opportunities, and new blocking dependencies. The optimizer re-assesses from the new ground truth after every build.

**Why Sigil-powered:** Sigil's 5-lens review (Engineering, Security, UX, CEO/Strategy, QA) gives a multi-dimensional assessment of what's worth building. The optimizer uses Sigil's lens system to rank candidates by impact, feasibility, and defensibility.

---

## When to Invoke

- At the start of a new project — "what should I build first?"
- When a major feature is done — "what's next?"
- When stuck deciding between options — "which one should I build?"
- When progress stalls — "am I building the right things?"
- When the user is unsure what to do — "assess and recommend the next build"
- **Any time the user asks about next steps or priorities**

---

## Pipeline

### State Tracking

The optimizer maintains state in `build-optimizer-state.json`:

```json
{
  "target": "Sigil certification authority",
  "iteration": 0,
  "max_iterations": 10,
  "phase": "assess",
  "history": [
    {"iteration": 0, "built": null, "assessment": null}
  ],
  "all_candidates": [],
  "remaining_high_value": [],
  "value_threshold": 7,
  "termination_reason": null
}
```

State is loaded at the start of each cycle and updated at the end. This makes the optimizer **resumable** — if interrupted mid-cycle, the next invocation picks up where it left off.

---

### Phase 0 — PRE-FLIGHT (cheapest disconfirming tests)

**Run this phase before any other phase — every cycle, including the first.**

The pre-flight runs 3 checks, all in Bash (< 1s each, zero Agent calls). Any check that fails means the entire cycle would be wasted — stop immediately.

```
scripts/optimizer-preflight.sh build-optimizer-state.json [target-path]
```

**Check 1 — Already terminated?**
If `build-optimizer-state.json` has a non-null `termination_reason`, the optimizer already completed. Running assessment would waste 2-5 minutes discovering "nothing to do."

**Check 2 — Max iterations exhausted?**
If `iteration >= max_iterations`, the optimizer hit its cap. Running assessment would waste time on a completed loop.

**Check 3 — Target reachable?**
If the user named a specific target (project path, directory), verify it exists. A nonexistent target produces a meaningless assessment.

**Exit codes:**
- **0** (PROCEED) → move to Phase 1
- **10** (ALREADY_TERMINATED) → report "already complete", do NOT enter Phase 1
- **20** (BLOCKED) → report "target unreachable", ask user to fix or provide valid target

**Why pre-flight?** Without it, the optimizer spends 30s-5min on a Sigil assessment before discovering the work was already done. These 3 checks complete in < 1s total.

---

### Phase 1 — ASSESS

Run pre-flight first. If PROCEED, load state. If no state exists, do a fresh assessment. If state exists, re-assess from current position.

**1a — Understand the target:**
Ask: what are we optimizing? The user's message usually contains the target. Examples:
- "optimize what to build for Sigil" → target = `Sigil certification authority`
- "what should I build next for AEO Sky?" → target = `AEO Sky marketplace`
- "what's the highest value thing for my project" → target = the current working project

If ambiguous, ask ONE clarifying question. Default to the working directory's project.

**1b — Run Sigil assessment:**

Use the Sigil skill (or stakeholder-360 skill if a full stakeholder map is needed) to assess the current state:

```
/sigil assess or /stakeholder-360
```

If the Sigil skill is unavailable, do a manual 5-lens assessment:

- **Engineering**: What's the technical bottleneck? What's the hardest unsolved problem?
- **Security**: What's the biggest risk? What could go wrong if we don't build this?
- **UX**: What's the biggest friction point for users right now?
- **CEO/Strategy**: What moves the needle most? What has the highest ROI?
- **QA**: What breaks first? What causes the most support tickets?

**1c — Generate candidate list:**

From the assessment, extract 3-7 concrete build candidates. For each:

| Candidate | Value (1-10) | Effort | Risk | Lens consensus |
|-----------|-------------|--------|------|----------------|
| [Thing to build] | 8 | 2 weeks | Low | Engineering: PASS, Security: PASS, UX: FAIL |
| [Another thing] | 9 | 1 week | Med | All PASS except CEO: FAIL (low willingness to pay) |

**1d — Rank and select:**

Rank by:
1. **Value**: How much does this move the needle? (primary)
2. **Effort**: Can we ship this in a reasonable time? (secondary tiebreaker)
3. **Dependencies**: Does this unblock other items? (bonus)

Select the highest-value candidate. If the highest-value candidate has value < 5 (on a 1-10 scale), skip to Phase 4 (terminate).

If the user asks "what should I build next", present the candidate list and the chosen item, then ask for confirmation before building. If the user says "just do it" or similar, proceed directly.

**Output:** A single selected build target with:
- Clear description of what to build
- Why it's the highest value
- What success looks like
- Estimated scope

---

### Phase 2 — BUILD

Execute the build of the selected target:

**2a — Plan the build:**
- Determine what files need to change or be created
- Define the exit criteria (what proves it's done)
- Estimate the work units (minutes to days)

**2b — Execute:**
- Create or modify files as needed
- Follow best practices for the domain
- Test that the build works

**2c — Verify:**
- Confirm the build meets the exit criteria
- Run any available tests
- If the build fails, fix it or mark it as blocked

**2d — Update state:**
- Record what was built in iteration history
- Note any discoveries or context changes from the build

---

### Phase 3 — RE-ASSESS

After building, re-assess the current state:

**3a — Run Sigil assessment again** (or stakeholder-360):
- Has the landscape changed now that this item is built?
- Did building this reveal new high-value items?
- Did building this make some other items obsolete?

**3b — Update candidate list:**
- Remove items that are now built
- Remove items made obsolete by the build
- Add any new items revealed by the build
- Re-rank remaining items based on the new context

**3c — Check termination condition:**
If the highest remaining item has value < 5 → terminate (log reason)
If the user has explicitly said to stop → terminate
If iteration count >= max_iterations → terminate

---

### Phase 4 — RECURSE OR TERMINATE

**If high-value items remain:**
- Write updated state to `build-optimizer-state.json`
- Recurse: invoke this skill again with the same target
- The skill re-enters at Phase 1, loading the updated state

**If no high-value items remain:**
- Write terminal state to `build-optimizer-state.json`
- Report completion summary:
  ```
  ═══ BUILD OPTIMIZER: COMPLETE ═══
  
  Target: [target]
  Iterations: [N]
  Built:
    1. [item] — [outcome]
    2. [item] — [outcome]
    ...
  
  Remaining (all below threshold):
    - [item] — value [N/10] — reason skipped
  
  Reason: [termination reason]
  ```
- The optimizer does NOT recurse. It stops.

---

### Integration with the Sigil Skill

The optimizer relies on the Sigil skill for assessment. The standard flow:

1. Invoke `/assess` (Sigil review of the project's current state)
2. Sigil's 5 lenses produce findings with evidence markers
3. Extract build candidates from findings (every FAIL/BLOCKER is a candidate; every PASS_W_CONCERNS that impacts scalability is a candidate)
4. Select the highest-value candidate
5. Build it
6. Re-invoke `/assess` to check if the landscape changed

If Sigil is not available, the optimizer does a manual 5-lens assessment inline.

---

## State File Format

The state file (`build-optimizer-state.json`) is the only persistent state. It lives at the project root:

```json
{
  "target": "Sigil certification authority",
  "iteration": 3,
  "max_iterations": 10,
  "phase": "assess",
  "status": "running",
  "history": [
    {
      "iteration": 0,
      "built": null,
      "assessment": {"candidates": [...], "selected": "registry"},
      "outcome": null
    },
    {
      "iteration": 1,
      "built": "Sigil Registry MVP",
      "assessment": {"value_before": 8, "value_after": 9},
      "outcome": "built and deployed"
    },
    {
      "iteration": 2,
      "built": "Badge API prototype",
      "assessment": {"value_before": 7, "value_after": null},
      "outcome": "built, needs docs"
    }
  ],
  "all_candidates": [
    {"id": "registry", "name": "Sigil Registry", "value": 9, "effort": "1 week", "status": "built"},
    {"id": "badge-api", "name": "Badge API", "value": 7, "effort": "3 days", "status": "built"},
    {"id": "verify-cli", "name": "sigil verify CLI", "value": 6, "effort": "2 weeks", "status": "remaining"},
    {"id": "enterprise-whitelist", "name": "Enterprise whitelist", "value": 4, "effort": "2 weeks", "status": "skipped_below_threshold"}
  ],
  "remaining_high_value": [
    {"id": "verify-cli", "name": "sigil verify CLI", "value": 6, "effort": "2 weeks"}
  ],
  "value_threshold": 5,
  "termination_reason": null
}
```

---

## Termination Conditions

The optimizer terminates when ANY of these is true:

| Condition | When | Action |
|-----------|------|--------|
| No items above threshold | All candidates < threshold value | Log reason, report summary |
| Max iterations reached | Iteration >= max_iterations | Log "reached max iterations", report partial summary |
| User cancel | User says stop/skip/pause | Respect the request, save state for resume |
| Assessment returns "nothing" | Sigil finds zero build candidates | Log "assessment returned empty", report |
| Blocking dependency | Next build requires external dependency | Log "blocked by X", report with remediation |

---

## Retry and Recovery

- **Build fails permanently**: Mark as blocked, re-assess, pick the next item
- **Assessment fails**: Retry once. If still fails, use cached assessment from last cycle as fallback
- **State file corrupted**: Start fresh, warn the user
- **User interrupts mid-build**: Save partial state, report what was done, next run picks up from re-assessment

---

## Reference

This skill is designed to work with:
- **sigil** (`skills/sigil/SKILL.md`) — 5-lens review engine for assessment
- **stakeholder-360** (`skills/stakeholder-360/SKILL.md`) — stakeholder mapping for assessment

The recursive pattern is the key design choice: assessment → build → re-assessment → loop. Each cycle reveals new context. One-pass planning is always wrong.
