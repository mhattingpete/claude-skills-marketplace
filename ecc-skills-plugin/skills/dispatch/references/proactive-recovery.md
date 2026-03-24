## Proactive Recovery

When a worker fails to start or errors immediately:

1. **Check CLI availability:**
   ```bash
   which agent 2>/dev/null
   which claude 2>/dev/null
   which codex 2>/dev/null
   ```

2. **If the CLI is gone or auth fails:**
   - Tell the user: "The [cursor/claude/codex] CLI is no longer available."
   - List alternative models/backends still available in the config.
   - Ask: "Want me to switch your default and retry with [alternative]?"

3. **If the user agrees:**
   - Update `default:` in config to the alternative model.
   - Re-dispatch the task with the new model.

4. **If no alternatives exist:**
   - Tell the user to install a CLI (`agent`, `claude`, or `codex`) or fix their auth, and stop.
