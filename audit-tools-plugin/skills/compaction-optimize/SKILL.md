# Compaction Optimizer

## Purpose

Reduce wasted tokens from conversation compaction. Each compaction pass costs 30-40K+ tokens of overhead. In a long session that compounds to 500K+ wasted tokens. This skill finds what's driving unnecessary compaction and what to change.

**Cost of one compaction:** ~$0.15-0.30 (Claude Opus). At 15-20 compactions per long session, that's $3-6 in pure overhead.

## When to Use

**Activation phrases:**
- "reduce compaction overhead"
- "optimize context usage"
- "too many compactions"
- "token waste in this session"
- "trim context bloat"
- "wasting tokens on compaction"
- "make sessions last longer before compaction"
- "reduce conversation overhead"

**Skip when:**
- Session just started (first few turns only — less than ~30 tool calls, no compaction yet)
- Task is trivially small (single clarifying question + answer)

## What It Does

Analyzes the current session's compaction patterns and proposes specific changes to reduce overhead. Four phases:

### Phase 1: Diagnose — Find the Waste

Measure how much you're paying per compaction:

```bash
# Check how many times compaction has run
grep -c "Compacting conversation" ~/.claude/projects/*/journal.jsonl 2>/dev/null || echo "no journal found"

# If you can access the current transcript, check its size
ls -lh "$(find ~/.claude/projects -name '*.jsonl' -type f 2>/dev/null | head -1)"
```

Signal that compaction is excessive:
- Compacting every 15-20 turns (too frequent)
- Compaction takes >60 seconds
- You find yourself repeating instructions that were in scope before compaction
- After compaction, the agent misses context you know was established

### Phase 2: Execute — 7 Reduction Levers

Each lever independently reduces compaction overhead. Apply in priority order:

**Lever 1 — Session structure (highest impact)**
Design sessions at task boundaries. One bug fix = one session. One feature = one session. Multi-hour sessions with unrelated tasks interleaved cause the most compaction thrash. Start a fresh session for each logically separate task.

**Lever 2 — Output discipline**
Each tool call and response adds tokens that live until compaction. Terse updates save the most:
- No trailing summaries
- No "I'll continue" or transition prose
- No recaps of what was just discussed
- One sentence per status update
- Use `task`/`todo` for progress tracking (compact format), not narrative

**Lever 3 — Minimize broad-read tools**
Large files read via `Read` saturate context. Before reading:
1. Check if you need the whole file or just a specific function (use `offset`/`limit`)
2. Use `grep`/`search_graph` to find the exact line first, then read that range
3. Pipe tool output to a file (`> /tmp/out.txt`) instead of having it in context

**Lever 4 — Archive before compaction threshold is reached**
When context is ~70% full (you notice responses starting to truncate or slow), proactively:
1. Write a memory note with the current task state
2. Commit work in progress
3. Start a fresh session for the next task segment

Tool: Use `task save` or equivalent before context gets full, not after compaction starts.

**Lever 5 — Avoid long-lived monitors**
`Monitor` with `persistent: true` keeps the entire stdout history in context. Use short-lived monitors that exit after the event fires. Each monitor line that appears in the conversation is a compaction-cost add.

**Lever 6 — Prune stale errors/backtraces**
When debugging, capture the error, fix it, then `grep`-verify the fix. Don't keep 50-line backtraces in context across multiple turns — they stay until compaction. After the fix, the backtrace no longer earns its space.

**Lever 7 — Use the skill system**
Skills bring focused instructions only when invoked. Putting patterns, checklists, and domain knowledge in SKILL.md instead of in-session prose means they occupy zero context between invocations. Every sentence you type in-session instead of referencing a skill is a compaction tax.

### Phase 3: Verify — Measure the Improvement

```bash
# Before/after: how many turns per compaction
echo "Turns to first compaction: $(grep -B5 'Compacting conversation' ~/.claude/projects/*/journal.jsonl 2>/dev/null | grep 'user:' | wc -l)"
```

Target: <2 compactions per hour of active work. If you're hitting compaction faster, one of the levers above is being skipped.

### Phase 4: Report — Summarize Findings

```markdown
## Compaction Audit

- **Compactions detected**: N in current session
- **Estimated waste**: ~N × 35K = XK tokens wasted
- **Top 3 levers**: [lever 1], [lever 2], [lever 3]
- **Changes applied**: [specific changes made]
- **Expected improvement**: ~X% fewer compactions
```

## The Cost Table

| Session type | Typical turns | Compactions | Waste | Cost |
|-------------|--------------|-------------|-------|------|
| Quick bug fix | 10-20 | 0-1 | 0-35K | $0-0.30 |
| Feature session | 30-60 | 2-5 | 70-175K | $0.60-1.50 |
| Long pairing session | 80-200 | 8-20 | 280-700K | $2.40-6.00 |
| Overnight autonomous | 500+ | 25+ | 875K+ | $7.50+ |

If you're in the "Long pairing session" row, applying these levers should halve the compaction count.

## Tools Used

- **Bash**: Check journal for compaction count, measure transcript size
- **Read/Read (offset/limit)**: Targeted reading instead of full file reads
- **Skill system**: Compaction-optimize itself reduces overhead by putting this in SKILL.md rather than in-session

## Success Criteria

- Compaction frequency drops by 50%+ in the next long session
- User reports fewer "it forgot what we were doing" moments after compaction
- Sessions complete more tasks before hitting compaction threshold
