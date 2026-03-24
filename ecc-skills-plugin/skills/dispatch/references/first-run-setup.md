## First-Run Setup

Triggered when `~/.dispatch/config.yaml` does not exist (checked in Step 0 or Modifying Config). Run through this flow, then continue with the original request.

### 1. Detect CLIs

```bash
which agent 2>/dev/null  # Cursor CLI
which claude 2>/dev/null  # Claude Code
which codex 2>/dev/null  # Codex CLI (OpenAI)
```

### 2. Discover models

Strategy depends on what CLIs are available:

**If Cursor CLI is available** (covers most cases):
- Run `agent models 2>&1` — this lists ALL models the user has access to, including Claude, GPT, Gemini, etc.
- Parse each line: format is `<id> - <Display Name>` (strip `(current)` or `(default)` markers if present).
- This is the single source of truth for model availability.
- For Claude models found here (IDs containing `opus`, `sonnet`, `haiku`), route through the `claude` backend when Claude Code CLI is available.

**If only Claude Code is available** (no Cursor):
- Claude CLI has no `models` command.
- Use stable aliases: `opus`, `sonnet`, `haiku`. These auto-resolve to the latest version (e.g., `opus` → `claude-opus-4-6` today, and will resolve to newer versions as they release).
- This is intentionally version-agnostic — no hardcoded version numbers that go stale.

**If Codex CLI is available:**
- Codex has no `codex models` command. Use a curated set of known model IDs: `gpt-5.3-codex`, `gpt-5.3-codex-spark`, `gpt-5.2`.
- OpenAI models (IDs containing `gpt`, `codex`, `o1`, `o3`, `o4-mini`) should prefer the `codex` backend when available.
- If Cursor CLI is also available, `agent models` may list OpenAI models — prefer routing those through `codex` when the Codex CLI is installed.

**If multiple CLIs are available:**
- Use `agent models` as primary source for model discovery (it's comprehensive).
- Additionally note Claude Code is available as a backend for Claude models.
- Additionally note Codex is available as a backend for OpenAI models.
- Prefer native backends: Claude models → `claude` backend, OpenAI models → `codex` backend.

**If neither is found:**
- Tell the user: "No worker CLI found. Install the Cursor CLI (`agent`), Claude Code CLI (`claude`), or Codex CLI (`codex`), or create a config at `~/.dispatch/config.yaml`."
- Show them the example config at `${SKILL_DIR}/references/config-example.yaml` and stop.

### 3. Present findings via AskUserQuestion

- Show a summary: "Found Cursor CLI with N models" / "Found Claude Code" / "Found Codex CLI"
- List a few notable models (top models from each provider — don't dump 30+ models)
- Ask: "Which model should be your default?"
- Offer 3-4 sensible choices (e.g., the current Cursor default, opus, sonnet, a GPT option)

### 4. Generate `~/.dispatch/config.yaml`

Build the config file with the new schema:

```yaml
default: <user's chosen default>

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

models:
  # Claude
  opus:          { backend: claude }
  sonnet:        { backend: claude }
  haiku:         { backend: claude }
  # GPT / OpenAI
  gpt-5.3-codex: { backend: codex }
  # ... all detected models grouped by provider
```

Rules:
- Include **all** detected models — they're one-liners and it's better to have them available than to require re-discovery.
- **Group by provider** with YAML comments for readability (`# Claude`, `# GPT`, `# Gemini`, etc.).
- **Claude model detection:** Any model ID containing `opus`, `sonnet`, or `haiku` (including versioned variants like `sonnet-4.6`, `opus-4.5-thinking`, etc.) is a Claude model. When the Claude Code CLI is available, ALL Claude models must use `backend: claude`. Never route Claude models through the cursor backend — the Claude CLI manages model selection natively and doesn't need `--model`.
- **OpenAI model detection:** Any model ID containing `gpt`, `codex`, `o1`, `o3`, or `o4-mini` is an OpenAI model. When the Codex CLI is available, ALL OpenAI models must use `backend: codex`. Only fall back to `cursor` backend for OpenAI models when Codex is not installed.
- Only include backends that were actually detected.
- Set user's chosen default.
- Run `mkdir -p ~/.dispatch` then write the file.

### 5. Continue

Proceed with the original dispatch or config request — no restart needed.

### Example

```
User: /dispatch "review the auth module"

Dispatcher: [no ~/.dispatch/config.yaml found — running first-run setup]
Dispatcher: [runs `which agent` → found, `which claude` → found]
Dispatcher: [runs `agent models` → 15 models detected]
Dispatcher: Found Cursor CLI (15 models) and Claude Code. Notable models:
  - opus (Claude) — best for complex tasks
  - sonnet (Claude) — fast and capable
  - gpt-5.3-codex (GPT) — strong for code

AskUserQuestion: Which model should be your default?
  1. opus (Recommended)
  2. sonnet
  3. gpt-5.3-codex

User: opus

Dispatcher: [generates ~/.dispatch/config.yaml with all 15 models, default: opus]
Dispatcher: Config created at ~/.dispatch/config.yaml with 15 models. Default: opus.
Dispatcher: [continues with the original task — dispatches security review using opus]
```
