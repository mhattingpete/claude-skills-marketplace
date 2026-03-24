---
name: parallel-agent-orchestration
description: |
  Pattern for orchestrating communicating Claude Code teams for massive parallel development.
  Use when: (1) large projects with many independent tasks, (2) need to maximize development
  throughput, (3) tasks have dependency chains that can be parallelized, (4) orchestrating
  work across multiple Claude sessions. Uses native TeamCreate/SendMessage/TaskList for
  real-time agent communication, shared task boards, and automatic 50% context handoff.
author: Claude Code
version: 2.0.0
date: 2026-02-22
---

# Parallel Agent Orchestration with Native Teams

## What Changed in v2 (Claude Code Teams)

**Old pattern (v1):** Fire-and-forget background tasks → poll output files → manual JSON registries.
**New pattern (v2):** TeamCreate → named teammates with bidirectional messaging → shared live task board.

| Old | New |
|-----|-----|
| `run_in_background: true` + file polling | `TeamCreate` + `SendMessage` |
| Manual `agent-registry.json` | Native `TaskCreate/TaskUpdate/TaskList` |
| Output at `/private/tmp/claude/.../tasks/{id}.output` | Messages auto-delivered to orchestrator |
| Orchestrator guesses agent status | Agents message you when done/blocked/at-50% |
| No agent-to-agent communication | Any agent can `SendMessage` to any named teammate |
| Context handoff via `HANDOFF.md` files | `teammate` type has built-in 50% handoff protocol |

---

## When to Use This Pattern

- 5+ independent features that can ship in parallel
- Acting as **coordinator**, not implementer
- Tasks have clear dependency relationships (unblocked by other agents completing)
- Need progress visibility without polling files
- Work must survive context resets (50% handoff built into `teammate` type)

---

## Core Infrastructure

### Agent Types

| Type | Use For | Key Behavior |
|------|---------|--------------|
| `orchestrator` | Team lead — always starts in plan mode | Coordinates teammates, manages handoffs |
| `teammate` | All implementation work | 50% context handoff protocol built in; auto-notifies orchestrator |
| `general-purpose` | One-off research/exploration subagents | No team membership; no messaging |

**Important:** `teammate` agents go idle between turns — this is normal. An idle teammate can still receive messages and will wake up immediately on `SendMessage`.

---

## Step-by-Step Setup

### 1. Create the Team

```
TeamCreate(
  team_name: "igreat-sprint",
  description: "iGreat MVP sprint — Stripe Connect, widgets, white-label, admin"
)
```

This creates:
- `~/.claude/teams/igreat-sprint/config.json` — member registry (name, agentId, agentType)
- `~/.claude/tasks/igreat-sprint/` — shared task directory for all members

### 2. Create All Tasks Upfront

Use `TaskCreate` for every known task. Set `addBlockedBy` to encode dependencies.

```
# Independent tasks (no blockers)
T1 = TaskCreate("Stripe Connect — backend actions", "...")
T2 = TaskCreate("Widget settings page UI", "...")
T3 = TaskCreate("Platform admin — tenant list", "...")

# Dependent tasks
T4 = TaskCreate("Stripe Connect — onboarding UI", "...", addBlockedBy=[T1.id])
T5 = TaskCreate("Widget embed.js script", "...", addBlockedBy=[T2.id])
```

All teammates share this task board — any agent can pick up an unblocked task after finishing its current one.

### 3. Spawn Named Teammates

Spawn one teammate per role. Each gets a name used for all future messaging.

```
Task(
  subagent_type: "teammate",
  name: "backend",
  team_name: "igreat-sprint",
  prompt: """
  You are the backend agent on the iGreat sprint team.
  Your team lead is orchestrator. Read team config at
  ~/.claude/teams/igreat-sprint/config.json to discover teammates.

  Your first task: [full task description + files to read first + technical rules]

  When done, message orchestrator: completed / blocked / next
  """
)
```

Spawn all independent-track teammates simultaneously (one `Task` call per teammate in a single message).

### 4. Assign Tasks via TaskUpdate

After spawning, assign tasks by name:

```
TaskUpdate(taskId: T1.id, owner: "backend", status: "in_progress")
TaskUpdate(taskId: T2.id, owner: "frontend", status: "in_progress")
TaskUpdate(taskId: T3.id, owner: "platform", status: "in_progress")
```

### 5. Receive Messages (Automatic)

You do NOT poll. Teammate messages are auto-delivered as new conversation turns.

A teammate completing a task sends:
```
SendMessage(type: "message", recipient: "orchestrator",
  content: "Stripe backend done. Branch agent/backend-stripe-connect pushed.
            T1 complete. T4 (onboarding UI) is now unblocked.",
  summary: "Stripe backend complete, T4 unblocked")
```

You respond by:
1. `TaskUpdate(T1, status: "completed")`
2. `TaskUpdate(T4, owner: "frontend", status: "in_progress")`
3. `SendMessage(type: "message", recipient: "frontend", content: "T4 is yours — Stripe onboarding UI. T1 merged.")`

---

## Agent Communication Patterns

### Orchestrator → Teammate
```
SendMessage(type: "message", recipient: "backend",
  content: "T1 is blocked — migrations agent hasn't landed the stripe_account_id column yet.
            Switch to T6 (invoice actions) while you wait.",
  summary: "Blocked, switch to T6")
```

### Teammate → Orchestrator (completion)
```
SendMessage(type: "message", recipient: "orchestrator",
  content: "T6 done. Branch agent/backend-invoices. No blockers found.
            Picking up T8 (payroll actions) from TaskList.",
  summary: "T6 done, picking up T8")
```

### Teammate → Teammate (coordination)
```
# frontend agent to backend agent:
SendMessage(type: "message", recipient: "backend",
  content: "I need the createStripeConnectSession action signature before I wire
            the redirect. What's the return shape?",
  summary: "Need Stripe session return type")
```

Orchestrator gets a brief summary of peer DMs — no need to intervene unless blocked.

### Broadcast (use sparingly)
```
SendMessage(type: "broadcast",
  content: "STOP all work. CI is red on main — type errors in packages/db/schema.
            Infra agent is fixing. Hold branches until green.",
  summary: "CI blocked, hold all branches")
```

---

## Dependency Unblocking Flow

```
T1: DB migration (stripe_account_id column)
  └─→ T4: Stripe Connect backend actions   [blockedBy: T1]
        └─→ T7: Stripe Connect UI          [blockedBy: T4]

T2: Widget API key table
  └─→ T5: Widget settings UI              [blockedBy: T2]
        └─→ T8: Widget embed.js           [blockedBy: T5]
```

When `infra` completes T1:
1. `TaskUpdate(T1, completed)`
2. `TaskUpdate(T4, owner: "backend", in_progress)` — now unblocked
3. Message `backend`: "T1 landed. T4 is unblocked — start Stripe actions."

When `backend` completes T4:
1. `TaskUpdate(T4, completed)`
2. `TaskUpdate(T7, owner: "frontend", in_progress)`
3. Message `frontend`: "T4 merged. T7 (Connect UI) is yours."

---

## 50% Context Handoff (Built into `teammate` Type)

The `teammate` subagent type has a built-in 50% context handoff protocol. When a teammate reaches ~50% context:

1. Teammate finishes its current feature completely (never cuts off mid-feature)
2. Writes `HANDOFF.md` in its repo root:
   ```markdown
   # Handoff — backend agent — [timestamp]
   ## Done
   - T4: Stripe Connect actions (branch: agent/backend-stripe-connect, pushed)
   ## Current state
   - T8: Payroll actions — 40% complete. `processPayroll()` done, `calculateDeductions()` next
   ## Files modified
   - apps/web/app/actions/payroll.ts (lines 1-340 complete)
   ## Next steps
   - Implement `calculateDeductions()` then `generatePayslip()`
   - Run pnpm type-check before pushing
   ## Blockers
   - None
   ```
3. Commits: `git commit -m "handoff: payroll actions at 40% — context reset"`
4. Messages orchestrator: `"Handoff at 50%. T4 done (merged). T8 in progress at 40%. HANDOFF.md committed."`
5. Orchestrator spawns a new teammate named `backend-2` with T8 context:
   ```
   "Read HANDOFF.md first. Continue T8 from where backend agent left off."
   ```

---

## Plan Approval Workflow

For high-risk features (DB migrations, Stripe), require plan approval before coding:

```
Task(
  subagent_type: "teammate",
  mode: "plan",           # Agent starts in plan mode — cannot write code until approved
  name: "infra",
  prompt: "Plan the DB migrations for Stripe Connect. Read schema/organizations.ts first.
           Present your migration plan for approval before executing."
)
```

Infra agent presents plan → you receive `plan_approval_request` → you respond:
```
SendMessage(type: "plan_approval_response",
  request_id: "...",
  recipient: "infra",
  approve: true)
# or:
  approve: false,
  content: "Add a rollback migration. Also scope the index to organization_id.")
```

---

## Shutdown Protocol

When all tasks are complete:
```
# Shut down each teammate gracefully
SendMessage(type: "shutdown_request", recipient: "backend",
  content: "Sprint complete. All tasks merged. Thank you.")
SendMessage(type: "shutdown_request", recipient: "frontend", ...)
SendMessage(type: "shutdown_request", recipient: "infra", ...)

# After all approve:
TeamDelete()
```

---

## Live Sprint Tracker

Maintain `SPRINT.md` in the repo root — this is the shared source of truth, NOT a JSON registry.

```markdown
# Sprint Tracker — updated 2026-02-22 14:30 UTC

## Summary
Done: 12/49 P0 items | Active agents: 4 | Blocked: 1

## Active
| ID | Feature | Agent | Branch | Status | Blocker |
|----|---------|-------|--------|--------|---------|
| W-007 | Stripe Connect backend | backend | agent/backend-stripe | In Progress | — |
| WDG-001 | Widget settings UI | frontend | agent/frontend-widget | In Progress | — |
| PA-001 | Platform admin tenant list | platform | agent/platform-admin | Blocked | Needs platform_users table |

## Completed This Session
| ID | Feature | Merged | Agent |
|----|---------|--------|-------|
| DB-001 | Stripe migrations | 14:10 | infra |

## Queue (unblocked, unassigned)
1. WDG-002 — Widget API key generation — assign to backend after W-007
2. WL-004 — Brand customisation page — assign to frontend after WDG-001
```

Update SPRINT.md after every merge. Commit alongside feature work — never let it go stale.

---

## iGreat Role Mapping

For the iGreat sprint specifically:

| Teammate Name | Repos | Responsibilities |
|---------------|-------|-----------------|
| `backend` | master.igreat | Server actions, API routes, DB queries |
| `frontend` | master.igreat, igreat.cloud | Dashboard UI, member portal, public pages |
| `integrations` | master.igreat | Stripe Connect, Google Cal, push notifications |
| `mobile` | igreat-client-app | Expo/React Native screens |
| `tests` | master.igreat | Vitest unit + Playwright E2E |
| `infra` | all repos | Migrations, CI/CD, env config — always plan-mode |
| `platform` | igreat.cloud | Platform admin (`/admin`), igreat.cloud dashboard |

One branch per agent per feature: `agent/[role]-[feature]`. Never share branches.

---

## Verification Checklist

Before dispatching agents:
- [ ] `TeamCreate` called — team config exists at `~/.claude/teams/{name}/config.json`
- [ ] All tasks created with `TaskCreate` — dependencies set via `addBlockedBy`
- [ ] Each teammate's prompt includes: files to read first, technical rules, project structure
- [ ] `infra` spawned with `mode: "plan"` for all migration work
- [ ] SPRINT.md created with accurate baseline numbers

During sprint:
- [ ] Every completed task gets `TaskUpdate(status: "completed")` immediately
- [ ] Every unblocked task gets assigned immediately (no idle teammates)
- [ ] SPRINT.md committed after every merge
- [ ] Peer DM summaries reviewed each turn — intervene if agents are stuck

At shutdown:
- [ ] All tasks in `completed` state
- [ ] All branches pushed and PRs merged
- [ ] `TeamDelete()` called after all teammates shut down

---

## Anti-Patterns

- **Orchestrator implementing**: You coordinate only. Agents write code.
- **Conflicting file edits**: Never assign same file to two agents. Plan file ownership upfront.
- **Broadcasting instead of targeting**: `broadcast` is expensive. Default to `SendMessage` to one teammate.
- **Stale SPRINT.md**: Update it every turn. It's your external memory.
- **Launching without plan approval**: Always use `mode: "plan"` for infra/migration work.
- **Ignoring idle notifications**: Idle = waiting for input. Check if they need a new task.
- **Spawning teammates without team_name**: They won't share the task board or be reachable by name.
- **Mid-feature context resets**: Teammates must finish the current feature before handing off.

---

## What You No Longer Need

- `agent-registry.json` — replaced by team config + TaskList
- Polling `/private/tmp/claude/.../tasks/{id}.output` — replaced by auto-delivered messages
- Manual `docs/sessions/orchestrator-handoff.md` — replaced by teammate 50% handoff protocol
- `run_in_background: true` — teammates run autonomously by design; use `teammate` type instead
