---
name: reddit-pain-researcher
description: >-
  Mines specified subreddits for labor-intensive tasks, pain points, and
  automation desires that professionals wish they could eliminate. Extracts
  quotes, time-cost estimates, and ripe-for-automation signals. Repeatable:
  maintains trend state across runs so you can see how automation landscape
  and pain points shift over weeks/months. Compiles results into structured
  markdown reports.
triggers:
  - research pain points
  - find automation opportunities
  - reddit pain research
  - what are people struggling with
  - labor pain audit
  - what do people want to automate
  - pain point research
  - automation discovery
  - subreddit pain mining
  - labor research
  - trend analysis
  - find problems to solve
  - what's painful for freelancers
  - what do small businesses struggle with
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Agent
  - AskUserQuestion
  - mcp__reddit-mcp__get_subreddit_hot_posts
  - mcp__reddit-mcp__get_subreddit_new_posts
  - mcp__reddit-mcp__get_subreddit_top_posts
  - mcp__reddit-mcp__get_subreddit_rising_posts
  - mcp__reddit-mcp__get_post_content
  - mcp__reddit-mcp__get_post_comments
  - mcp__aeo-platform__web_search
---
# Reddit Pain Researcher

**Reddit Pain Researcher — repeatable subreddit mining for labor pain points.** Discovers what professionals in specific subreddits find painful, time-consuming, and ripe for automation. Tracks trends across runs. Outputs structured MD reports with quotes, time-cost estimates, and automation potential scores.

**Why repeatable:** Pain points shift. New tools emerge. Subreddits evolve. Running this monthly reveals which problems are getting worse, which are being solved, and what new pains have appeared. The state file makes every run comparable to the last.

**Why Sigil:** Five-lens rigor (Engineering, Security, UX, CEO/Strategy, QA) applies naturally to automation opportunity assessment — is this problem technically solvable, safe to automate, delightful for users, strategically valuable, and verifiably fixed?

---

## When to Invoke

- **New automation product research** — "what should I build to help small businesses?"
- **Monthly trend audit** — "run the pain point sweep again"
- **Targeting a niche** — "what pains do bookkeepers have?"
- **n8n workflow ideas** — "what can I automate for freelancers?"
- **Competitive intelligence** — "what are people complaining about in r/sales?"
- **Content research** — "what battles are people fighting that I can write about?"
- **Any time the user asks:**
  - "find me automation opportunities"
  - "what's painful for [profession]?"
  - "research [subreddit] for complaints about [task]"
  - "run the pain research again"
  - "show trends from last time"

---

## Pipeline

### State Tracking

The researcher maintains persistence in `reddit-pain-state.json` at the current working directory:

```json
{
  "research_target": "SMB automation opportunities",
  "run_count": 3,
  "last_run": "2026-07-01",
  "default_subreddits": ["smallbusiness", "freelance", "Entrepreneur", "sales", "Bookkeeping", "recruiting", "marketing", "webdev", "consulting", "copywriting"],
  "default_themes": ["automation", "pain point", "time consuming", "annoying", "waste of time", "wish I could automate", "manual work", "data entry", "administrative", "repetitive"],
  "runs": [
    {
      "run_id": 1,
      "date": "2026-07-01",
      "brief": "initial sweep",
      "threads_analyzed": 15,
      "total_comments_scanned": 1200,
      "pain_points_found": 12
    }
  ],
  "trends": {
    "persistent_pains": [
      {"id": "content-marketing", "name": "Content marketing overwhelm", "appearances": 3, "last_seen": "2026-07-01", "automation_potential": "VERY HIGH"}
    ],
    "new_pains": [],
    "resolved_pains": [],
    "automation_readiness_changes": []
  },
  "pains": [
    {
      "id": "pp-001",
      "title": "Content marketing overwhelm",
      "subreddits": ["smallbusiness"],
      "thread_ids": ["1ujiq5a"],
      "first_seen": "2026-07-01",
      "last_seen": "2026-07-01",
      "total_upvotes_observed": 61,
      "quotes_saved": ["The guide insisted that to stay relevant, I need to produce three high quality short form videos a day..."],
      "best_time_cost": "20-30 hrs/week",
      "automation_potential": "VERY HIGH",
      "automation_approach": "AI repurposing pipeline (blog to social to email)",
      "n8n_playbook": "webhook -> AI content transform -> schedule -> multi-channel publish"
    }
  ]
}
```

State is loaded at the start of each run and updated at the end. This makes the researcher **resumable and trendable** — if interrupted, the next invocation loads saved state and continues.

---

### Phase 0 — RESEARCH BRIEF (gather requirements)

**Always run this phase first.** Establish the scope of the research:

1. **Ask the user** (if brief not provided in the trigger message):
   - What is the research target? (e.g., "SMB automation", "bookkeeper pains", "freelance headaches")
   - Which subreddits to mine? (default list above if unspecified)
   - What themes to search for? (default list above if unspecified)
   - Shallow (just titles) or deep (comments too)? Default: deep.
   - Save results as filename? Default: `reddit-pain-report-YYYY-MM-DD.md`

2. **Load state** — If `reddit-pain-state.json` exists, load it and report last-run summary:
   ```
   Previous run: 2026-06-15 (3 weeks ago)
   Pains found: 12
   Persistent: content marketing, resume screening, lead follow-up
   New this run: none yet
   ```

3. **Define scope document** — Write a research brief (`reddit-research-brief-YYYY-MM-DD.md`) with:
   - Target and purpose
   - Subreddit list
   - Search themes
   - Depth (titles vs comments)
   - How many threads per subreddit (default: 3-5)

---

### Phase 1 — SUBREDDIT SCAN

For each subreddit in the research scope:

1. **Search hot posts** using `mcp__reddit-mcp__get_subreddit_hot_posts` with the subreddit name and limit=15
2. **Search new posts** using `mcp__reddit-mcp__get_subreddit_new_posts` with limit=15
3. **Filter titles** against the theme list. A match is: any theme keyword appearing in the title (case-insensitive)
4. Rank matched threads by upvotes. Keep top 3-5 per subreddit.

**Gathering the raw material:**
```
Subreddit: r/smallbusiness
Matched threads:
- "Anyone else tired of marketing advice that ignores reality?" (61↑, 64 comments) — theme: "automation", "annoying"
- "how do you follow up with leads without feeling annoying?" (33↑, 39 comments) — theme: "pain point"
- ...etc
```

**Synthesize short description per thread** — extract the core pain signal from title + subreddit context. Do NOT fetch full content yet (Phase 2 handles that).

If no threads match on a subreddit, note it: `r/webdev — no strong matches for current themes.`

---

### Phase 2 — DEEP COMMENT EXTRACTION

For each high-ranked matched thread (top 3 per subreddit, capped at 20 total):

1. **Fetch full post content** using `mcp__reddit-mcp__get_post_content` with `comment_limit=30, comment_depth=3`
2. **Read all top-level comments** and their replies
3. **Extract quote-worthy lines** — any comment that:
   - Explicitly names a time cost ("takes 3 days", "an hour and a half", "20 hours a week")
   - Voices strong emotional pain ("makes you want to blow your brains out", "this shit doesn't fly with me")
   - Describes a process that could be automated
   - Mentions money wasted or lost
   - Has high upvotes relative to thread (top 20% of comments)
4. **Record each thread as a structured pain point candidate**

**Per-thread extraction schema (track in working memory, compile in Phase 4):**
```
thread_id:
  subreddit:
  title:
  upvotes:
  total_comments:
  pain_summary: "one-line description of the pain"
  quotes:
    - score=N: "exact quote"
    - score=N: "exact quote"
  time_cost_estimate: "from comment evidence or inferred"
  automation_signals: [list of signals that this is automatable]
  ripe_for_automation: HIGH/MODERATE/LOW
```

---

### Phase 3 — AGGREGATION AND SCORING

Consolidate all extracted pain points into a unified list:

1. **De-duplicate** — If the same pain appears in multiple threads (e.g., "lead follow-up" mentioned in both r/smallbusiness and r/Entrepreneur), merge them into one pain point with multiple source citations.

2. **Score each pain point** on three axes (1-10):
   - **Frequency**: How many threads/comments mention this? (1 = fringe, 10 = every thread)
   - **Emotional intensity**: How strong is the language? (1 = mild annoyance, 10 = "blow my brains out")
   - **Automation feasibility**: Can this be solved with n8n + AI today? (1 = requires PhD, 10 = 1-hour n8n workflow)

   Composite score = geometric mean of all three. Use this for final ranking.

3. **Tag each with:**
   - `automation_approach`: The best n8n/AI approach to solve it
   - `n8n_playbook`: A one-line description of the n8n workflow
   - `value_proposition`: What the user gains (time saved, revenue recovered, stress removed)

---

### Phase 4 — COMPILATION AND OUTPUT

**Write the report file:** `reddit-pain-report-YYYY-MM-DD.md`

Structure:

```markdown
# Reddit Labor Pain Report — YYYY-MM-DD

**Research target:** [from brief]
**Subreddits scanned:** [list]
**Threads analyzed:** [N]
**Total comments scanned:** [N]
**Pain points found:** [N]

---

## Executive Summary

[2-3 paragraph synthesis of the most important findings]

**Top 3 automation opportunities right now:**
1. [Pain point] — [time cost] — [automation approach]
2. [Pain point] — [time cost] — [automation approach]
3. [Pain point] — [time cost] — [automation approach]

---

## Trend Analysis (vs previous runs)

[Only if state file exists with previous runs]

| Pain Point | This Run | Previous Run | Trend |
|------------|----------|-------------|-------|
| Content marketing | 20-30 hrs/wk | 15-25 hrs/wk | Worsening |
| Lead follow-up | Revenue loss | Revenue loss | Stable |
| [New pain] | NEW | N/A | Emerging |

**Summary:**
- Persistent pains: [list, count]
- New this run: [list, count]
- Resolved/disappeared: [list, count]

---

## Full Pain Point Catalog

### #[rank]. Pain Point Name
**Sources:** r/subreddit (+N upvotes, +N comments), r/subreddit2

**What it costs:**
- [time cost estimate]
- [additional cost]

**Vocal pain:**
> "[exact quote, with attribution]" (+score)

> "[exact quote, with attribution]" (+score)

**Ripe for automation:** [RATING]
**Best approach:** [automation approach]
**n8n playbook:** [n8n_playbook description]
**Value prop:** [value proposition]

---

## Consolidated Ripe-for-Automation Ranking

| Rank | Pain Point | Time Cost | Automation | Best Approach |
|------|-----------|-----------|------------|-------------|
| 1 | ... | ... | VERY HIGH | ... |
| 2 | ... | ... | HIGH | ... |

---

## Methodology

- Subreddits: [list]
- Search themes: [list]
- Thread selection: hot + new, filtered by theme keywords, top 3-5 per subreddit
- Quote extraction: all comments read, emotional/financial/time-cost signals extracted
- Scoring: composite of frequency, intensity, and feasibility (geometric mean)

---

## Appendix: Raw Thread Links

| Subreddit | Thread | Upvotes | Comments | Link |
|-----------|--------|---------|----------|------|
| ... | ... | ... | ... | reddit.com/r/.../... |
```

---

### Phase 5 — STATE UPDATE

After writing the report, update `reddit-pain-state.json`:

1. Increment `run_count`
2. Set `last_run` to today's date
3. Append a new entry to `runs[]` with summary stats
4. For each pain point:
   - If new (not in `pains[]` by matching `title`): add to `pains[]` and to `trends.new_pains`
   - If existing (matched by `title`): update `last_seen`, increment `total_upvotes_observed`, append new quotes
5. Update `trends`:
   - `persistent_pains`: pains seen in 2+ consecutive runs
   - `resolved_pains`: pains from previous runs that didn't appear this run
   - `automation_readiness_changes`: any pain whose score changed significantly
6. Write updated state to `reddit-pain-state.json`

---

### Phase 6 — PRESENT RESULTS

Deliver the report to the user with:

```
═══ REDDIT PAIN RESEARCH: COMPLETE ═══

Report written: reddit-pain-report-YYYY-MM-DD.md
State file: reddit-pain-state.json

Pain points found: [N]
Top automation opportunity: [name] — [time cost saved]

Trends vs last run:
  - [N] persistent pains continued
  - [N] new pains emerged
  - [N] pains no longer trending

Next steps:
  1. Build an n8n workflow for the top opportunity
  2. Re-run this research next month to track trends
  3. Drill deeper into any specific pain point
```

---

## Pre-Flight Checks

Run these before entering Phase 1:

**Check 1 — State file exists?**
If `reddit-pain-state.json` exists, read it and report last-run summary. Use it to inform the trend analysis section.

**Check 2 — Target clear?**
If the trigger message does not contain a clear research target or subreddit list, ask the user. Do not proceed with defaults silently.

**Check 3 — Workspace clean?**
If a previous report file exists with today's date, ask the user if they want to overwrite or create a dated variant.

---

## Retry and Recovery

- **Reddit API rate limit**: If a specific subreddit query fails, skip it and note it in the report. Do not retry more than once.
- **Empty subreddit results**: If a subreddit returns 0 useful threads, report it as "no strong matches" and move on.
- **State file corrupted**: If state file is unparseable, start fresh, warn the user, and archive the corrupted file.
- **User interrupts mid-run**: Save partial data to a checkpoint file (`reddit-pain-checkpoint.json`) so the next run can pick up. Phase state is tracked in the checkpoint.

---

## Reference

- Research brief template: `references/reddit-search-brief-template.md`
- This skill works with **sigil** for automation-feasibility scoring on specific pain points
- Use with **n8n** playbook generation for immediate implementation
- Trend data accumulates in `reddit-pain-state.json` — keep this in a version-controlled or synced directory for long-term trend tracking
- Trend diff engine: `scripts/pain-trend-diff.py` — computes structured comparison between runs. Usage: `python3 scripts/pain-trend-diff.py reddit-pain-state.json --markdown`
- Trend diff wrapper: `scripts/pain-trend-diff.sh` — convenience shell wrapper. Usage: `./scripts/pain-trend-diff.sh` from the plugin root

## Tool Usage Summary

| Tool | Phase | Purpose |
|------|-------|---------|
| `get_subreddit_hot_posts` | 1 | Initial thread discovery |
| `get_subreddit_new_posts` | 1 | Catch threads that didn't make hot but are fresh |
| `get_subreddit_top_posts` | 1 | Timeframe-specific search (week/month/year) |
| `web_search` | 3,4 | Validate automation approaches, find n8n templates |
| `Bash` | 4,5 | Write report file, update state JSON |
| `AskUserQuestion` | 0 | Clarify research scope if ambiguous |
