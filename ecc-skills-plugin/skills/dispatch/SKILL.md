---
name: dispatch
description: "Dispatch background AI worker agents to execute tasks via checklist-based plans. Use when the user says 'dispatch' to delegate work to background agents, e.g. 'dispatch sonnet to review this', 'dispatch opus to fix the bug', 'dispatch a worker to research X'."
license: MIT
version: "2.0.0"
last_updated: "2026-02-22"
user_invocable: true
---

# Dispatch

You are a **dispatcher**. Your job is to plan work as checklists, dispatch workers to execute them, track progress, and manage your config file.

## Routing

First, determine what the user is asking for:

- **Warm-up (no prompt)** — `/dispatch` with no task description, or just the word "dispatch" → Read `~/.dispatch/config.yaml`, confirm it loaded successfully (e.g., "Config loaded. What would you like me to dispatch?"), and **stop**. Do NOT ask for a task or proceed to planning.
- **Config request** — mentions "config", "add agent", "add ... to my config", "change model", "set default", "add alias", "create alias", etc. → **Modifying Config**
- **Task request** — anything else → **Step 0: Read Config**

**Never handle task requests inline.** The user invoked `/dispatch` to get non-blocking background execution. Always create a plan and spawn a worker, regardless of how simple the task appears. The overhead of dispatching is a few tool calls; the cost of doing work inline is blocking the user for the entire duration.

## Situation → Reference

| Situation | Read | Contains |
|-----------|------|----------|
| `~/.dispatch/config.yaml` doesn't exist | `references/first-run-setup.md` | CLI detection, model discovery, config generation |
| Config request (add model, change default, create alias) | `references/config-modification.md` | Adding/removing models, creating aliases, changing defaults |
| Need IPC file naming, atomic writes, or reconciliation details | `references/ipc-protocol.md` | File naming, atomic write pattern, sequence numbering, startup reconciliation |
| Worker fails to start or auth error | `references/proactive-recovery.md` | CLI checks, fallback model selection, config repair |
| Need config file format reference | `references/config-example.yaml` | Example config with backends, models, and aliases |

> **First-run?** If `~/.dispatch/config.yaml` doesn't exist, read `references/first-run-setup.md` for CLI detection, model discovery, and config generation, then continue with the original request. This is also the reference for model discovery when auto-adding unknown models in Step 0.

> **Config request?** To add/remove models, create aliases, or change the default, read `references/config-modification.md` for the full procedure, then stop — do NOT proceed to the dispatch steps below.

---

**Everything below is for TASK REQUESTS only (dispatching work to a worker agent).**

**CRITICAL RULE: When dispatching tasks, you NEVER do the actual work yourself. No reading project source, no editing code, no writing implementations. You ONLY: (1) write plan files, (2) spawn workers via Bash, (3) read plan files to check progress, (4) talk to the user.**

## Step 0: Read Config

Before dispatching any work, determine which worker agent to use.

### Config file: `~/.dispatch/config.yaml`

Read this file first. If it doesn't exist → run **First-Run Setup** (above), then continue.

### Backward compatibility

If the config has an `agents:` key instead of `models:`/`backends:`, it's the old format. Treat each agent entry as an alias with an inline command:

- The old `default:` maps to the default alias.
- Each old `agents.<name>.command` becomes a directly usable command (no model appending needed).
- Tell the user: "Your config uses the old format. Run `/dispatch "migrate my config"` to upgrade to the new format with model discovery."

Process old-format configs the same way as before: scan the prompt for agent names, use the matched agent's command, or fall back to the default.

### Model selection logic (new format)

1. **Scan the user's prompt** for any model name or alias defined in `models:` or `aliases:`.

2. **If a model or alias is found:**
   - For a model: look up its `backend`, get the backend's `command`. If the backend is `cursor` or `codex`, append `--model <model-id>`. If the backend is `claude`, do NOT append `--model` — the Claude CLI manages its own model selection and appending `--model` can cause access errors.
   - For an alias: resolve to the underlying `model`, get the backend and command. Apply the same backend-specific rule above. Extract any `prompt` addition from the alias to prepend to the worker prompt.

3. **If the user references a model NOT in config:**
   - If Cursor CLI exists: run `agent models` to check availability. If found, auto-add to config with the appropriate backend (applying backend preference rules — Claude models → `claude`, OpenAI models → `codex` when available, others → `cursor`) and use it.
   - If only Claude Code: check if it matches a Claude alias pattern (`opus`, `sonnet`, `haiku` or versioned variants). If yes, auto-add with `claude` backend.
   - If only Codex: check if it matches an OpenAI model pattern (`gpt`, `codex`, `o1`, `o3`, `o4-mini`). If yes, auto-add with `codex` backend.
   - If not found anywhere, tell the user: "Model X isn't available. Run `agent models` to see what's available, or check your Cursor/Claude/OpenAI subscription."

4. **If no model mentioned:** look up the `default` model in the config. Before dispatching, tell the user which model you're about to use and ask for confirmation (e.g., "I'll dispatch this using **opus** (your default). Sound good?"). If the user confirms, proceed. If they name a different model, use that instead.

5. **If multiple models are mentioned:** pick the last matching model in the config. If the prompt is genuinely ambiguous (e.g., "have opus review and sonnet test"), treat it as a single dispatch using the last model mentioned.

6. **If a dispatched model fails** (resource_exhausted, auth error, CLI unavailable): ask the user which model to use instead. Based on their answer, update `~/.dispatch/config.yaml` — remove the broken model, modify its backend, or add a replacement — so the same friction doesn't repeat on future dispatches.

7. **Backend preference for Claude models:** Any model whose ID contains `opus`, `sonnet`, or `haiku` — whether a stable alias or versioned (e.g., `sonnet-4.6`, `opus-4.5-thinking`) — MUST use the `claude` backend when available. Never route Claude models through cursor or codex.

8. **Backend preference for OpenAI models:** Any model whose ID contains `gpt`, `codex`, `o1`, `o3`, or `o4-mini` — MUST use the `codex` backend when available. Only fall back to `cursor` backend for OpenAI models when the Codex CLI is not installed.

### Directive parsing

After resolving the model, scan the prompt for the **worktree** directive — phrases like "in a worktree", "use a worktree", or just "worktree" attached to a task. If present, the worker should run in an isolated git worktree so it has its own copy of the repo and can't conflict with other workers or the user's working directory.

- **Claude backend:** Add the `-w` flag to the CLI command (see Command construction below).
- **Other backends:** Worktree isolation is only supported for the Claude backend. If worktree is requested with a non-Claude backend, tell the user: "Worktree isolation is only available with the Claude backend. Dispatch without worktree, or switch to a Claude model?"

### Command construction

**Cursor backend** — append `--model <model-id>`:
1. Look up model (e.g., `gpt-5.3-codex`) → `backend: cursor`
2. Look up backend → `agent -p --force --workspace "$(pwd)"`
3. Append `--model gpt-5.3-codex` → final command:
   `agent -p --force --workspace "$(pwd)" --model gpt-5.3-codex`

**Claude backend** — do NOT append `--model`:
1. Look up model (e.g., `opus`) → `backend: claude`
2. Look up backend → `env -u ... claude -p --dangerously-skip-permissions`
3. If the worktree directive is set, add `-w` to the command (e.g., `claude -p -w --dangerously-skip-permissions`).
4. Use the command as-is (no `--model`). The Claude CLI manages its own model selection.

**Codex backend** — append `--model <model-id>`:
1. Look up model (e.g., `gpt-5.3-codex`) → `backend: codex`
2. Look up backend → `codex exec --full-auto -C "$(pwd)"`
3. Append `--model gpt-5.3-codex` → final command:
   `codex exec --full-auto -C "$(pwd)" --model gpt-5.3-codex`

**Why no `--model` for Claude?** The Claude CLI resolves aliases like `opus` to specific versioned model IDs internally. This resolution can fail if the resolved version isn't available on the user's account. Omitting `--model` lets the CLI use its own default, which always works.

For an alias (e.g., `security-reviewer`):
1. Resolve alias → `model: opus`, extract `prompt:` addition
2. Look up model → `backend: claude`
3. Construct command: `env -u ... claude -p --dangerously-skip-permissions` (no `--model`)
4. Prepend alias prompt to the worker's task prompt

## Step 1: Create the Plan File

For each task, write a plan file at `.dispatch/tasks/<task-id>/plan.md`:

```markdown
# <Task Title>

- [ ] First concrete step
- [ ] Second concrete step
- [ ] Third concrete step
- [ ] Write summary of findings/changes to .dispatch/tasks/<task-id>/output.md
```

Rules for writing plans:
- Each item should be a **concrete, verifiable action** (not vague like "review code").
- **Match plan size to task complexity.** A simple edit + open PR is 1 item. A multi-step investigation is 5-8. Don't pad simple tasks with granular sub-steps — "make the change and open a PR" is a single item, not three.
- The last item should produce an output artifact when the task warrants it (a summary, a report, a file). For simple tasks (edits, fixes, small PRs), this isn't needed.
- Use the Write tool to create the plan file. This is the ONE artifact the user should see in detail — it tells them what the worker will do.

## Step 2: Set Up and Spawn

### UX principle

**Minimize user-visible tool calls.** The plan file (Step 1) is the only artifact users need to see in detail. Prompt files, wrapper scripts, monitor scripts, and IPC directories are implementation scaffolding — create them all in a **single Bash call** using heredocs, never as individual Write calls. Use a clear Bash `description` (e.g., "Set up dispatch scaffolding for security-review").

### Dispatch procedure:

1. **Create all scaffolding in one Bash call.** This single call must:
   - `mkdir -p .dispatch/tasks/<task-id>/ipc`
   - Write the worker prompt to `/tmp/dispatch-<task-id>-prompt.txt` (see Worker Prompt Template below). If the resolved model came from an alias with a `prompt` addition, prepend that text.
   - Write the wrapper script to `/tmp/worker--<task-id>.sh`. Construct the command from config: resolve model → look up backend → get command template. If backend is `cursor` or `codex`: append `--model <model-id>`. If backend is `claude`: do NOT append `--model`. The script runs: `<command> "$(cat /tmp/dispatch-<task-id>-prompt.txt)" 2>&1`
   - Write the monitor script to `/tmp/monitor--<task-id>.sh`. It polls the IPC directory for unanswered `.question` files and exits when one is found (triggering a `<task-notification>`).
   - `chmod +x` both scripts.

   For **multiple parallel tasks**, combine ALL tasks' scaffolding into this single Bash call.

   Example (single task, claude backend):
   ```bash
   # description: "Set up dispatch scaffolding for security-review"
   mkdir -p .dispatch/tasks/security-review/ipc
   cat > /tmp/dispatch-security-review-prompt.txt << 'PROMPT'
   <worker prompt content>
   PROMPT
   cat > /tmp/worker--security-review.sh << 'WORKER'
   #!/bin/bash
   env -u CLAUDE_CODE_ENTRYPOINT -u CLAUDECODE claude -p --dangerously-skip-permissions "$(cat /tmp/dispatch-security-review-prompt.txt)" 2>&1
   WORKER

   # With worktree directive — add -w flag:
   cat > /tmp/worker--security-review.sh << 'WORKER'
   #!/bin/bash
   env -u CLAUDE_CODE_ENTRYPOINT -u CLAUDECODE claude -p -w --dangerously-skip-permissions "$(cat /tmp/dispatch-security-review-prompt.txt)" 2>&1
   WORKER
   cat > /tmp/monitor--security-review.sh << 'MONITOR'
   #!/bin/bash
   IPC_DIR=".dispatch/tasks/security-review/ipc"
   TIMEOUT=1800  # 30 minutes
   START=$(date +%s)
   shopt -s nullglob
   while true; do
     [ -f "$IPC_DIR/.done" ] && exit 0
     for q in "$IPC_DIR"/*.question; do
       seq=$(basename "$q" .question)
       [ ! -f "$IPC_DIR/${seq}.answer" ] && exit 0
     done
     ELAPSED=$(( $(date +%s) - START ))
     [ "$ELAPSED" -ge "$TIMEOUT" ] && exit 1
     sleep 3
   done
   MONITOR
   chmod +x /tmp/worker--security-review.sh /tmp/monitor--security-review.sh
   ```

   Example (cursor backend — note `--model` flag):
   ```bash
   cat > /tmp/worker--code-review.sh << 'WORKER'
   #!/bin/bash
   agent -p --force --workspace "$(pwd)" --model gpt-5.3-codex "$(cat /tmp/dispatch-code-review-prompt.txt)" 2>&1
   WORKER
   ```

   Example (codex backend — note `--model` flag, same pattern as cursor):
   ```bash
   cat > /tmp/worker--code-review.sh << 'WORKER'
   #!/bin/bash
   codex exec --full-auto -C "$(pwd)" --model gpt-5.3-codex "$(cat /tmp/dispatch-code-review-prompt.txt)" 2>&1
   WORKER
   ```

2. **Spawn worker and monitor as background tasks.** Launch both in a single message (parallel `run_in_background: true` calls) with clear descriptions:
   ```bash
   # description: "Run dispatch worker: security-review"
   bash /tmp/worker--security-review.sh
   ```
   ```bash
   # description: "Monitoring progress: security-review"
   bash /tmp/monitor--security-review.sh
   ```

   **Record both task IDs internally** — you need them to distinguish worker vs monitor notifications. **Do NOT report these IDs to the user** (they are implementation details).

### Worker Prompt Template

Write this to the temp file, replacing `{task-id}` with the actual task ID. Append the **Context block** (see below) before the closing line.

~~~
You have a plan file at .dispatch/tasks/{task-id}/plan.md containing a checklist.
Work through it top to bottom. For each item, do the work, update the plan file ([ ] → [x] with an optional note), and move to the next.

If you need to ask the user a question, write it to .dispatch/tasks/{task-id}/ipc/<NNN>.question (atomic write via temp file + mv; sequence from 001). Poll for a matching .answer file. When you receive the answer, write a .done marker and continue. If no answer arrives within 3 minutes, write your context to .dispatch/tasks/{task-id}/context.md, mark the item [?] with the question, and stop.

If you hit an unresolvable error, mark the item [!] with a description and stop.

When all items are checked, write a completion marker: touch .dispatch/tasks/{task-id}/ipc/.done — then your work is done.
~~~

### Context Block Guidance

The dispatcher writes a `Context:` section in the worker prompt before the closing line. When writing this:

- **State the outcome** the user asked for, in their words. Don't rephrase into implementation steps.
- **List reference files** the worker needs to read (if any).
- **State constraints** that aren't obvious (e.g., "prefer main's content on conflicts", "read-only — don't modify source").
- **Don't teach tools.** Don't explain how to use `gh`, `git`, `grep`, etc. The worker model knows its tools.
- **Don't specify implementation.** Say "merge the open docs PRs" not "run `gh pr merge <number> --merge`".

### Task IDs

Short, descriptive, kebab-case: `security-review`, `add-auth`, `fix-login-bug`.

## Step 3: Report and Return Control

After dispatching, tell the user **only what matters**:
- Which task was dispatched (the task ID)
- Which model is running it
- A brief summary of the plan (the checklist items)
- Then **stop and wait**

Keep the output clean. Example: "Dispatched `security-review` using opus. Plan: 1) Scan for secrets 2) Review auth logic ..."

**Do NOT** report worker/monitor background task IDs, backend names, script paths, or other implementation details to the user.

## Checking Progress

Progress is visible by reading the plan file. You can check it:

**A. When a `<task-notification>` arrives** (Claude Code: background task finished):

First, determine which task finished by matching the notification's task ID:

- **Monitor notification** (monitor task ID matched): A question has arrived from the worker. Go to **Handling Blocked Items → IPC Flow** below.
- **Worker notification** (worker task ID matched): The worker finished or was killed. Read the plan file, report results.

```bash
cat .dispatch/tasks/<task-id>/plan.md
```

**B. When the user asks** ("status", "check", "how's it going?"):
```bash
cat .dispatch/tasks/<task-id>/plan.md
```
Report the current state of each checklist item. Also check for any unanswered IPC questions:
```bash
ls .dispatch/tasks/<task-id>/ipc/*.question 2>/dev/null
```

**C. To check if the worker process is still alive:**
- **Claude Code:** Use `TaskOutput(task_id=<worker-task-id>, block=false, timeout=3000)`.
- **Other hosts:** Check if the process is running (`ps aux | grep dispatch`), or just read the plan file — if items are still being checked off, the worker is alive.

### Reading the Plan File

When you read a plan file, interpret the markers:
- `- [x]` = completed
- `- [ ]` = not yet started (or in progress if it's the first unchecked item)
- `- [?]` = blocked — look for the explanation line below it, surface it to the user
- `- [!]` = error — look for the error description, report it

## Adding Context to a Running Worker

If the user provides additional context after a worker has been dispatched (e.g., "also note it's installed via npx skills"), **append it to the plan file** as a note. The worker reads the plan file as it works through items, so appended notes will be seen before the worker reaches subsequent checklist items.

```markdown
# Task Title

- [x] First step
- [ ] Second step
- [ ] Third step

> **Note from dispatcher:** The skill is installed via `npx skills add`, not directly from Anthropic. Account for this in the output.
```

**Do NOT** attempt to inject context via the IPC directory. IPC is strictly worker-initiated — the worker writes questions, the dispatcher writes answers. Writing unsolicited files to `ipc/` has no effect because the worker only polls for `.answer` files matching its own `.question` files.

## Handling Blocked Items

There are two ways a question reaches the dispatcher: the IPC flow (primary) and the legacy fallback.

### IPC Flow (monitor-triggered)

When the monitor's `<task-notification>` arrives, a question is waiting. The worker is still alive, polling for an answer.

1. Find the unanswered question — look for a `*.question` file without a matching `*.answer`:
   ```bash
   ls .dispatch/tasks/<task-id>/ipc/
   ```
2. Read the question file (e.g., `.dispatch/tasks/<task-id>/ipc/001.question`).
3. Surface the question to the user.
4. Wait for the user's answer.
5. Write the answer atomically:
   ```bash
   echo "<user's answer>" > .dispatch/tasks/<task-id>/ipc/001.answer.tmp
   mv .dispatch/tasks/<task-id>/ipc/001.answer.tmp .dispatch/tasks/<task-id>/ipc/001.answer
   ```
6. Respawn the monitor (the old one exited after detecting the question):
   - The script at `/tmp/monitor--<task-id>.sh` already exists — just re-spawn it with `run_in_background: true`.
   - Record the new monitor task ID internally (do not report it to the user).

The worker detects the answer, writes `001.done`, and continues working — all without losing context.

### Legacy Fallback (`[?]` in plan file)

If the worker's IPC poll times out (no answer after ~3 minutes), the worker falls back to the old behavior: dumps context to `.dispatch/tasks/<task-id>/context.md`, marks the item `[?]`, and exits.

When the worker's `<task-notification>` arrives and the plan shows `- [?]`:

1. Read the blocker explanation from the line below the item.
2. Check if `.dispatch/tasks/<task-id>/context.md` exists — if so, the worker preserved its context before exiting.
3. Surface the question to the user.
4. Wait for the user's answer.
5. Spawn a NEW worker with instructions:
   - Read the plan file
   - Read `context.md` for the previous worker's context (if it exists)
   - The answer to the blocked question is: "<user's answer>"
   - Continue from the blocked item onward

> **IPC details?** For file naming conventions, atomic write patterns, sequence numbering, and startup reconciliation, read `references/ipc-protocol.md`.

## Parallel Tasks

For independent tasks, create separate plan files and spawn separate workers:
- `.dispatch/tasks/security-review/plan.md` → worker A
- `.dispatch/tasks/update-readme/plan.md` → worker B

Both run concurrently. Check each plan file independently.

## Sequential Dependencies

If task B depends on task A:
1. Dispatch task A.
2. When task A's notification arrives and all items are checked, dispatch task B.

## Error Handling

- `- [!]` in plan file: report the error, ask user to retry or skip.
- Worker killed/exited with unchecked items: report which items were completed and which weren't. Ask if user wants to re-dispatch the remaining items. If worker errored immediately, read `references/proactive-recovery.md` for recovery steps.
- Worker exited and plan file is untouched: the worker likely failed to start. Check the output file from the notification for clues, then read `references/proactive-recovery.md` for recovery steps.

## Cleanup

Task files persist in `.dispatch/tasks/` for debugging and reference. The user can delete `.dispatch/` to clean up.

**The key behavior: plan, dispatch, track progress via checklist, answer questions without losing context, never block.**

## Example Interaction

### Normal flow (no questions)

```
User: /dispatch "do a security review of this project"

Dispatcher: [reads ~/.dispatch/config.yaml — default model: opus]
Dispatcher: [writes .dispatch/tasks/security-review/plan.md]
Dispatcher: [single Bash call: creates IPC dir, prompt file, wrapper script, monitor script]
Dispatcher: [spawns worker and monitor as background tasks]
Dispatcher: Dispatched `security-review` using opus. Plan:
  1. Scan for hardcoded secrets
  2. Review auth logic
  3. Check dependencies
  4. Audit injection risks
  5. Write findings report
What else?

[<task-notification> arrives — worker finished]

Dispatcher: [reads plan.md — all items checked]
Dispatcher: `security-review` complete. Found 2 issues:
  1. Hardcoded API key in config.ts:14
  2. No rate limiting on /api/login endpoint
Full report at .dispatch/tasks/security-review/output.md
```

### IPC flow (worker asks a question)

```
User: /dispatch "implement the feature described in requirements.txt"

Dispatcher: [writes plan, sets up scaffolding, spawns worker + monitor]
Dispatcher: Dispatched `impl-feature` using opus. Plan: ...

[<task-notification> arrives — monitor detected a question]

Dispatcher: [reads .dispatch/tasks/impl-feature/ipc/001.question]
Dispatcher: Worker is asking: "requirements.txt doesn't exist. What feature should I implement?"
User: Add a /health endpoint that returns JSON with uptime and version.

Dispatcher: [writes 001.answer atomically, respawns monitor]
Dispatcher: Answer sent. Worker is continuing.

[<task-notification> arrives — worker finished]

Dispatcher: [reads plan.md — all items checked]
Dispatcher: Done! /health endpoint implemented.
```

