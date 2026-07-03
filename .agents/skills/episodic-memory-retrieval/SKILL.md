---
name: "episodic-memory-retrieval"
description: "Cross-session memory faculty for the CHORUS brain. Reads from STICKY.md, session diary, git log, audit reports, and memory graph to answer: what happened, what worked, what didn't, where's the knowledge."
license: MIT
metadata:
  tier: "STANDARD"
  category: "Meta / Knowledge Management"
---

# Episodic Memory Retrieval

## Purpose
The CHORUS brain's long-term memory faculty. Humans remember what they learned, what worked, what failed, and where to find information. This skill does the same: given a recall query, it searches across all memory sources, ranks them by relevance, and returns structured facts with confidence and source provenance.

## When to Use
- "What did we decide about {topic}?"
- "Have we solved {problem} before?"
- "Where is the documentation for {system}?"
- "What was the outcome of {previous work}?"
- "Why did {something} fail last time?"
- Session startup: "What's in memory from prior sessions?"
- "What patterns have we documented?"

## Memory Sources (searched in priority order)

### Tier 1 — Hot Memory (fast, always checked)
1. **STICKY.md** — Current session state, priority queue, gotchas, enabled patterns
2. **docs/session-diary.md** — Cross-agent handoff diary, session summaries
3. **STATE.md** — Current task state, evidence, timestamps

### Tier 2 — Structured Memory (search, then read)
4. **Memory graph** (codebase-memory-mcp) — Architecture decisions, pattern docs, project facts
5. **Git log** — Commit history with messages (`git log --oneline --grep=<query>`)
6. **AEO platform memory** (mcp__aeo-platform__memory_recall) — Agent memory for past decisions

### Tier 3 — Episodic Memory (slower, deeper)
7. **Relay channel memory** (relay_receive) — Multi-agent coordination history
8. **Audit reports** (`docs/audit/*.md`) — Self-assessment and gap analysis archives
9. **Artifact logs** (`docs/status/*.json`) — Heartbeat and CI/CD status history

## Process

### Step 1 — Interpret Query
Classify the memory query:
- **Fact recall**: "What env vars does concierge need?" — Specific data
- **Decision recall**: "Why did we pick Fly.io over Railway?" — Architecture decisions
- **Pattern recall**: "What gotchas are there for Playwright?" — Known patterns and antipatterns
- **Failure recall**: "What has broken before?" — Incident history
- **Location recall**: "Where is the deploy script?" — File system location

### Step 2 — Search Tier 1 (hot memory)
Read STICKY.md, session-diary.md, STATE.md in parallel. Parse for relevant facts.
**Time budget**: 5s
**If found**: Return with confidence HIGH, cite source with line reference.

### Step 3 — Search Tier 2 (structured)
If not found in Tier 1, search memory graph and git log in parallel.
**Time budget**: 15s
**If found**: Return with confidence MEDIUM, cite commit SHA or memory key.

### Step 4 — Search Tier 3 (episodic)
If still not found, search audit reports and relay channel.
**Time budget**: 20s
**If found**: Return with confidence LOW, note the source may be stale.

### Step 5 — Return with Confidence
Always return with:
- **Answer**: The factual answer
- **Source**: Which file/system, with path or key
- **Confidence**: HIGH/MEDIUM/LOW (Tier 1/2/3)
- **Timestamp**: When the source was last updated
- **Gap**: "I could not find anything about this" + suggestions for where to look

## Output Format
```json
{
  "query": "Why did we choose Fly.io for concierge?",
  "answer": "Fly.io was chosen over Railway for concierge deployment because Railway requires 24/7 uptime at $25-30/mo (hobby plan), while Fly.io auto-sleeps to ~$1-5/mo. The decision is documented in CLAUDE.md under 'Three-Environment Concierge Deployment'.",
  "confidence": "HIGH",
  "source": "CLAUDE.md (project instructions, Environment Topology section)",
  "source_timestamp": "2026-06-19",
  "tier": "hot-memory"
}
```

## Memory Maintenance
Periodically (as part of self-assessment):
1. **Archive stale facts**: If STICKY.md has facts from >7 days ago, move to session-diary
2. **Prune duplicates**: If git log and memory graph have overlapping facts, keep the one with more evidence
3. **Update timestamps**: Touch memory sources that are still accurate

## Success Criteria
- Every answer has a verifiable source
- Confidence accurately reflects source freshness (not confidence in the answer itself)
- Failed queries return "could not find" + search strategy suggestion
- Tier 1 searches complete in under 5s total overhead

## Integration
- **Triggered by**: Any skill that asks "what was done before"
- **Feeds into**: self-assessment-meta-loop (provides failure history), determination-protocol (provides prior escalation patterns)
- **Updates**: STICKY.md gotchas, session-diary.md append

## Tools Used
- Read (for STICKY.md, session-diary, STATE.md, audit reports)
- Bash / git (for git log search)
- mcp__aeo-platform__memory_recall (for agent memory)
- codebase-memory-mcp (for ADR search)
- relay_receive (for relay channel history)
- Grep (for keyword search across docs/)
