# Competitor Landscape: Claude Code Workflow Plugins

**Date:** 2026-06-30  
**Context:** The user asked to find mature alternatives that could replace the sigil-engineering-workflow-plugin toolbelt.

---

## Tier 1: Replace Our Entire Toolbelt

### obra/superpowers — **242,000 stars** ⭐

| Metric | Value |
|--------|-------|
| Stars | 242,000 (dominant, no competition) |
| Latest Release | v6.0.3 (June 18, 2026) |
| Commits | 609 |
| Contributors | 43 |
| License | MIT |
| Harnesses | 11 (Claude Code, Cursor, Codex, Copilot, Gemini, etc.) |

**14 skills covering the full SDLC:**
1. brainstorming → refines ideas before coding
2. using-git-worktrees → isolated workspace per task
3. writing-plans → breaks designs into 2-5 min tasks
4. subagent-driven-development → dispatches subagents per task with review
5. executing-plans → batch execution with human checkpoints
6. test-driven-development → RED-GREEN-REFACTOR cycle
7. requesting-code-review → severity-graded review against plan
8. receiving-code-review → structured response to feedback
9. finishing-a-development-branch → tests → merge/PR/discard
10. systematic-debugging → 4-phase root cause process
11. verification-before-completion → bug fix verification
12. dispatching-parallel-agents → concurrent workflows
13. writing-skills → skill creation best practices
14. using-superpowers → introduction to the system

**Coverage vs our toolbelt:**
| Our Skill | Superpowers Equivalent |
|-----------|----------------------|
| plan-execute | brainstorming + writing-plans + subagent-driven-development |
| test-doctor | test-driven-development |
| safe-commit | using-git-worktrees + finishing-a-development-branch |
| review-apply | requesting-code-review + receiving-code-review |
| solution-ensemble | dispatching-parallel-agents |

**Verdict:** Superpowers is 100x more mature. We cannot compete on engineering workflow. Adopt it.

### cyanheads/git-mcp-server — **226 stars, v2.15.1, 400 commits**

Pure git operations MCP server. 28 tools across 7 categories. Mature (v2.15.1), Apache 2.0. Worth installing for git-specific operations but doesn't replace the full workflow.

---

## Tier 2: Agent/Knowledge Libraries

### rohitg00/awesome-claude-code-toolkit — **2.2k stars**

| Metric | Value |
|--------|-------|
| Agents | 135 (10 categories) |
| Skills | 35 curated |
| Commands | 42 |
| Plugins | 176+ |
| Hooks | 20 |
| License | Apache 2.0 |

Massive catalog of agent definitions. More of a collection than a cohesive plugin. Worth looking at for individual agent ideas but not a replacement for Superpowers.

### GetBindu/awesome-claude-code-and-skills — stars unknown

Another curated collection. Similar format to rohitg00.

---

## Tier 3: Specialized

### anthropics/claude-code-security-review — official Anthropic

GitHub Action for security review of code changes. Official but narrow scope.

### praneybehl/code-review-mcp — MCP code review server

MCP-based code review tool using various LLMs. Niche.

---

## What NOT Covered by Superpowers

These are our defensible moat:

1. **Sigil certification authority** — 5-lens review, structured certificates, evidence markers, adversarial verify. Superpowers has nothing like this.
2. **readme-doctor skill** — README audit + rewrite with domain detection. Superpowers doesn't have this.
3. **reddit-research skill** — Reddit MCP research engine. Unique.
4. **360-review plugin** — user story generator. Unique.
5. **Certificate schema** — interoperable trust standard. If Anthropic adopts this, we win.

---

## Recommendation

| Action | What | Why |
|--------|------|-----|
| **Adopt** | obra/superpowers | 242K stars, 14 skills, covers our entire toolbelt |
| **Install** | cyanheads/git-mcp-server | Mature git MCP, 28 tools, secure by design |
| **Keep** | sigil-plugin | Certification authority — unique moat |
| **Keep** | 360-review-plugin | User story generation — no overlap |
| **Keep** | reddit-research | Reddit MCP — unique skill |
| **Remove** | sigil-engineering-workflow-plugin | Redundant with Superpowers. 5 skills all covered. |
