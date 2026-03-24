## Modifying Config

1. Read `~/.dispatch/config.yaml`. If it doesn't exist, run **First-Run Setup** (above), then continue.

2. Apply the user's requested change. The config uses the new schema with `backends:`, `models:`, and `aliases:`.

**Adding a model:**
- If user says "add gpt-5.3 to my config": probe `agent models` to verify availability, then add to `models:` with the appropriate backend.
- Example: `gpt-5.3: { backend: cursor }`

**Creating an alias:**
- If user says "create a security-reviewer alias using opus": add to `aliases:` with optional prompt.
- Example:
```yaml
aliases:
  security-reviewer:
    model: opus
    prompt: >
      You are a security-focused reviewer. Prioritize OWASP Top 10
      vulnerabilities, auth flaws, and injection risks.
```

**Changing the default:**
- If user says "switch default to sonnet": update `default:` field.

**Removing a model:**
- If user says "remove gpt-5.2": delete from `models:`.

3. Run `mkdir -p ~/.dispatch` then write the updated file to `~/.dispatch/config.yaml`.
4. Tell the user what you changed. Done.

**Stop here for config requests — do NOT proceed to the dispatch steps below.**
