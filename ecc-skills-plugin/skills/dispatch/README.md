# /dispatch

**You don't need 6 terminals.** You need one session that delegates.

`/dispatch` turns your AI coding session into a command center. You describe work, it plans a checklist, fans out to background workers — Claude, GPT, Gemini — and tracks progress. You stay in one clean session. Workers do the heavy lifting in isolated contexts.

<p align="center">
  <img src="assets/before-after.svg" alt="Architecture diagram: Your Session sends a task to the Dispatcher, which fans out to Opus, Sonnet, and Haiku workers in parallel, with a feedback loop for questions and progress. Also supports GPT, Gemini, and other models." width="900" />
</p>

```
/dispatch "do a security review of this project"
```

> **Host requirement:** Dispatch runs inside **Claude Code** — it must be your active session. Other CLIs like Cursor and Codex work as **workers only** (they execute subtasks in the background).

---

## Why dispatch

### Your main session stays lean

The dispatcher **never does the actual work**. It plans, delegates, and tracks. The heavy reasoning — code review, refactoring, test writing — happens in isolated worker contexts. Your main session's context window is preserved for orchestration, not consumed by implementation details.

### Workers ask questions back

This is the part most agent orchestrators get wrong. When a `/dispatch` worker gets stuck, it doesn't silently fail or hallucinate. It **asks a clarifying question** — the dispatcher surfaces it to you, you answer, and the worker continues **without losing context**. No restart, no re-explaining, no lost work.

```
Worker is asking: "requirements.txt doesn't exist. What feature should I implement?"
> Add a /health endpoint that returns JSON with uptime and version.

Answer sent. Worker is continuing.
```

### Non-blocking — you never wait

The moment a worker is dispatched, your session is **immediately free**. Dispatch another task. Ask a question. Write code. The dispatcher handles multiple workers in parallel, reports results as they arrive, and surfaces questions only when they need your input. No polling, no tab-switching, no "is it done yet?"

### Any model, one interface

Mix models per task. Claude for deep reasoning, GPT for broad generation, Gemini for speed. Reference any model by name — if it's not in your config, `/dispatch` auto-discovers and adds it.

```
/dispatch "use gemini-3.1-pro to review the API layer"
```

---

## How it works

1. You run `/dispatch "task description"`
2. A checklist plan is created at `.dispatch/tasks/<id>/plan.md`
3. A background worker picks it up and checks off items as it goes
4. If the worker has a question, it asks — you answer — it continues
5. You get results when it's done, or ask for status anytime

## Setup

On first run, `/dispatch` auto-detects your CLIs (`claude`, `agent`, `codex`), discovers available models, and generates `~/.dispatch/config.yaml`. No manual config needed.

## Configuration

Three sections in `~/.dispatch/config.yaml`:

**Backends** — CLI commands for each provider:
```yaml
backends:
  claude:
    command: >
      env -u CLAUDE_CODE_ENTRYPOINT -u CLAUDECODE
      claude -p --dangerously-skip-permissions
  cursor:
    command: >
      agent -p --force --workspace "$(pwd)"
  codex:
    command: >
      codex exec --full-auto -C "$(pwd)"
```

**Models** — one line each, mapped to a backend:
```yaml
models:
  opus:            { backend: claude }
  sonnet:          { backend: claude }
  gpt-5.3-codex:  { backend: codex }
  gemini-3.1-pro:  { backend: cursor }
```

**Aliases** — named shortcuts with optional role prompts:
```yaml
aliases:
  security-reviewer:
    model: opus
    prompt: >
      You are a security-focused reviewer. Prioritize OWASP Top 10.
```

See [`references/config-example.yaml`](references/config-example.yaml) for the full example.

## Adding models

Reference any model by name — if it's not in your config, `/dispatch` auto-discovers and adds it:

```
/dispatch "use gemini-3.1-pro to review the API layer"
```

Or add manually: `/dispatch "add gpt-5.3 to my config"`

## Plan markers

| Marker | Meaning |
|--------|---------|
| `[ ]`  | Pending |
| `[x]`  | Done |
| `[?]`  | Blocked — waiting for your answer |
| `[!]`  | Error |

## Host compatibility

**Host (the session where you type `/dispatch`):** Claude Code.

**Workers (background agents that execute subtasks):** Any CLI that accepts a prompt — Cursor CLI, Codex CLI, Claude Code, or anything you define in config.

## Best practice: warm up at session start

Run `/dispatch` with no arguments at the beginning of a session to pre-load your config:

```
/dispatch
```

This reads `~/.dispatch/config.yaml` into the dispatcher's context so subsequent dispatches are faster and don't need confirmation prompts. It's a good habit to add as a [Claude Code memory](https://docs.anthropic.com/en/docs/claude-code/memory) so you remember to do it each session:

> "Run /dispatch at the start of each session to warm up the config."

## Cleanup

Delete `.dispatch/` to clean up task files.
