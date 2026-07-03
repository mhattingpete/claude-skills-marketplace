# Skill Wirer

Auto-discovers, installs, symlinks, and verifies adopted skills across all installed marketplaces. Replaces manual symlink management and routing-table audit.

---
description: Wire, prune, and inventory Claude Code skills across marketplace sources. Scan installed skills, detect phantoms, verify symlinks, and maintain the manifest.

## When to Activate

- "Wire my skills"
- "Install the adopted skill libraries"
- "Check if all my skills are installed"
- "Fix broken skills"
- "Audit my skill wiring"
- "Verify skills"
- "What skills are available?"
- Any session startup where skills might be stale

## Phase 0 — Pre-Flight Check (HARD GATE)

Before running the full 7-step pipeline, run the cheapest disconfirming test:

```bash
scripts/skill-wirer-preflight.sh ~/.claude/skills
```

**Exit codes:**
- **0** (PROCEED) → dead symlinks or corruption found — full pipeline needed
- **1** (BLOCKED) → skills dir missing or not writable — misconfigured, stop
- **2** (CLEAN) → no dead symlinks, no corruption — skip repair, proceed to verification only

**What it saves:** The full 7-step pipeline scans every marketplace directory, deep-scans every skills directory for 3 entry types, and content-verifies every symlink — ~5-30s for a healthy system. The pre-flight detects "nothing to fix" in < 10ms and skips straight to Step 6 (verification).

Pre-flight checks performed:
1. Skills directory exists
2. Skills directory is writable
3. Count broken top-level symlinks
4. Count corrupted skill directories (missing SKILL.md)
5. Check if directory is empty

---

## What It Does

1. Scans all installed marketplaces (`~/.claude/plugins/marketplaces/`) for available skills
2. Deep-scans `~/.claude/skills/` for broken symlinks AT ALL LEVELS — including dead SKILL.md symlinks INSIDE directories (the classic `/tmp/` install pattern)
3. Removes corrupted skill directories with dead symlinks inside; recreates as direct symlinks to valid cache paths
4. Scans plugin caches for cached skill directories that lack symlinks
5. Maps marketplace skill paths → `~/.claude/skills/` — creates missing symlinks
6. Content-verifies every skill: reads actual SKILL.md (not just `ls -la`)
7. Verifies all routing-table-referenced skills are reachable

## Workflow

### Step 1: Scan installed marketplaces

List all marketplace directories:

```
ls ~/.claude/plugins/marketplaces/
ls ~/.claude/plugins/cache/claude-plugins-official/
```

For each marketplace, find all SKILL.md files and extract the skill name (directory name parent):

```
find ~/.claude/plugins/marketplaces/<name> -name "SKILL.md"
find ~/.claude/plugins/cache/claude-plugins-official/<name> -name "SKILL.md"
```

Build a map: `{skill_name: skill_path}` for ALL available skills across ALL marketplaces.

### Step 2: Deep scan ~/.claude/skills/ — detect corruption at ALL levels

**CRITICAL: There are THREE types of skill entries in `~/.claude/skills/`:**

| Type | Structure | Status |
|------|-----------|--------|
| **Direct symlink** | `skillname -> /path/to/cache/skillname/` | HEALTHY |
| **Standalone directory** | `skillname/SKILL.md` (own file) | HEALTHY |
| **Corrupted directory** | `skillname/SKILL.md -> /tmp/...` (dead) | CORRUPTED — must delete whole dir |

The classic `/tmp/` install pattern: old `npx skills add` created `~/.claude/skills/<name>/SKILL.md` symlinks point to `/tmp/<project>-install/.../SKILL.md`. These paths get cleaned on reboot, leaving 39+ dead skills.

```
# Deep scan — detects ALL dead symlink levels
for skill in ~/.claude/skills/*; do
  name=$(basename "$skill")
  if [ -L "$skill" ]; then
    target=$(readlink "$skill")
    if [ -d "$skill" ]; then
      echo "LINK_OK  $name -> $target"
    else
      echo "BROKEN   $name -> $target"
    fi
  elif [ -d "$skill" ] && [ "$name" != "_gstack-command" ]; then
    # Check for dead SKILL.md symlink inside directory
    if [ -L "$skill/SKILL.md" ] && [ ! -e "$skill/SKILL.md" ]; then
      echo "CORRUPT  $name -> $(readlink "$skill/SKILL.md") (dead SKILL.md inside)"
    elif [ -f "$skill/SKILL.md" ]; then
      echo "DIR_OK   $name (standalone SKILL.md)"
    else
      echo "EMPTY    $name (no SKILL.md found)"
    fi
  fi
done
```

### Step 3: Repair corrupted directories (NEVER layer fixes)

For each CORRUPT entry (dead `SKILL.md` symlink inside a directory):

**Rule: Never layer a symlink inside a corrupted directory. Remove the entire directory and recreate as a single direct symlink.**

1. Find the valid cache path in the marketplace map (Step 1)
2. `rm -rf ~/.claude/skills/<name>` — delete the WHOLE corrupted directory
3. `ln -sf <valid_cache_path> ~/.claude/skills/<name>` — single direct symlink
4. Verify: `cat ~/.claude/skills/<name>/SKILL.md | head -1` — confirm readable

```
for skill in ~/.claude/skills/*; do
  name=$(basename "$skill")
  if [ -d "$skill" ] && [ -L "$skill/SKILL.md" ] && [ ! -e "$skill/SKILL.md" ]; then
    dead_target=$(readlink "$skill/SKILL.md")
    found_in_cache=$(find_in_marketplace_map "$name")
    if [ -n "$found_in_cache" ]; then
      echo "FIXING  $name (dead: $dead_target → cache: $found_in_cache)"
      rm -rf "$skill"
      ln -sf "$found_in_cache" "$skill"
      cat "$skill/SKILL.md" | head -1 > /dev/null 2>&1 && echo "  → VERIFIED" || echo "  → FAILED"
    else
      echo "ORPHAN  $name (dead: $dead_target, not in any cache)"
      rm -rf "$skill"
    fi
  fi
done
```

For each BROKEN top-level symlink:
1. Look up in the marketplace map from Step 1
2. If found: `rm -f ~/.claude/skills/<name> && ln -sf <cache_path> ~/.claude/skills/<name>`
3. If not found: report as missing, suggest manual install

### Step 4: Create missing symlinks

For each adopted skill collection with cache paths but missing from `~/.claude/skills/`:

**Superpowers (14 skills from cache):**
Cache path: `~/.claude/plugins/cache/claude-plugins-official/superpowers/6.0.3/skills/`
Skills: brainstorming, writing-plans, executing-plans, subagent-driven-development, test-driven-development, systematic-debugging, using-superpowers, dispatching-parallel-agents, writing-skills, verification-before-completion, using-git-worktrees, finishing-a-development-branch, requesting-code-review, receiving-code-review, writing-user-stories

For each skill not already in `~/.claude/skills/`:
```
ln -sf <cache_path>/<skill> ~/.claude/skills/<skill>
```

**Caveman (6 skills):**
Cache path: `~/.claude/plugins/marketplaces/mhattingpete-claude-skills/.agents/skills/` or `~/aeo/claude-skills-marketplace/.agents/skills/`
Skills: caveman, caveman-commit, caveman-compress, caveman-help, caveman-review, caveman-stats

**Marketing skills (40 skills):**
Cache path: `~/.claude/plugins/marketplaces/marketingskills/skills/`
Register as needed — already auto-discovered by marketplace system.

**Trail of Bits (30+ skills):**
Plugin path: `~/.claude/plugins/marketplaces/trailofbits/plugins/*/skills/*/`
Each plugin has its own subdirectory with skills nested 2 levels deep.
These are auto-discovered by marketplace — no symlinks needed.

**alirezarezvani/claude-skills (337 skills):**
Path: `~/.claude/plugins/marketplaces/mhattingpete-claude-skills/`
Auto-discovered by marketplace — no symlinks needed.

### Step 5: Verify routing-table references

Read the CLAUDE.md routing table. Extract all skill names that are referenced.
For each referenced skill, verify it exists in at least ONE of:
- `~/.claude/skills/<skill>/`
- `~/.claude/plugins/marketplaces/*/skills/<skill>/` (1 level deep)
- `~/.claude/plugins/marketplaces/*/*/skills/<skill>/` (2 levels deep — ToB pattern)
- `~/.claude/plugins/cache/claude-plugins-official/*/*/skills/<skill>/` (Superpowers pattern)

Report MISSING for any skill not found in any of these paths.

### Step 6: Install missing marketplaces

If a collection is entirely missing (e.g., Humanizer), attempt auto-install:

| Collection | Install Command |
|-----------|-----------------|
| Humanizer | `claude plugin marketplace add blader/humanizer` (or npx: `npx skills add blader/humanizer`) |
| Caveman | `claude plugin marketplace add JuliusBrussee/caveman` (or npx) |
| Superpowers | Already installed via marketplace |

If install fails (CAPTCHA, auth, etc.), flag it as BLOCKED and describe the remediation.

### Step 7: Content verification — read NOT ls

**Root cause of past failures:** The previous algorithm only ran `ls -la` to check symlinks. `ls` shows the file exists; it does NOT prove the file is readable. A dead symlink inside a directory (e.g. `~/claude/skills/brainstorming/SKILL.md -> /tmp/...`) passes `ls -la` but fails `cat`. The fix: read actual content.

```
VERIFIED=0
FAILED=0
for skill in ~/.claude/skills/*; do
  name=$(basename "$skill")
  if [ -f "$skill/SKILL.md" ] && head -1 "$skill/SKILL.md" > /dev/null 2>&1; then
    first_line=$(head -1 "$skill/SKILL.md")
    VERIFIED=$((VERIFIED + 1))
  elif [ -L "$skill" ] && head -1 "$skill/SKILL.md" > /dev/null 2>&1; then
    first_line=$(head -1 "$skill/SKILL.md")
    VERIFIED=$((VERIFIED + 1))
  else
    echo "UNREADABLE $name"
    FAILED=$((FAILED + 1))
  fi
done
echo "Verified: $VERIFIED, Failed: $FAILED"
```

## Output Format

```
═══ SKILL WIRER REPORT ═══
Date: <timestamp>

### Summary
Total skills available: <N> (across all marketplaces + skills dir)
Skills in ~/.claude/skills/: <N>
Broken symlinks fixed: <N>
Missing symlinks created: <N>

### Marketplaces Found
✅ superpowers (14 skills)
✅ caveman (6 skills)
✅ marketingskills (40 skills)
✅ mhattingpete-claude-skills (337 skills)
✅ trailofbits (30+ skills)

### Skills in ~/.claude/skills/
<list of skills with status: OK/DEAD_FIXED/MISSING_SYMLINK_CREATED>

### Routing Table Audit
✅ brainstorming -> superpowers/6.0.3/skills/brainstorming
✅ dispatching-parallel-agents -> superpowers/6.0.3/skills/dispatching-parallel-agents
❌ humanizer -> *** NOT FOUND ***
...

### Actions Taken
- Fixed 3 broken symlinks
- Created 12 missing symlinks
- Installed 1 new marketplace
```

## Success Criteria

- All 5 adopted collections are accessible
- Zero broken symlinks in `~/.claude/skills/`
- All routing-table-referenced skills resolve to a real path
- Report is written to `sigil-plugin/skills/skill-wirer/wire-report.json` for state tracking

## Tools Used

- **Bash**: File operations, symlink management, `find`/`ls` for discovery
- **Read**: Read CLAUDE.md routing table for verification
- **Write**: Write wire report to state file
- **Edit**: If CLAUDE.md routing table references are stale, flag them

## Error Handling

- **Permission denied**: `ln -sf` needs write access to `~/.claude/skills/`. If blocked, report permission error and suggest `sudo` or manual fix.
- **Cache missing**: If `superpowers/6.0.3` not found, check other versions in `claude-plugins-official/`. Report the full list of available versions.
- **Marketplace not installed**: Report the `claude plugin marketplace add` command for manual install.
- **CLAUDE.md locked**: If `protect-files.sh` blocks reading CLAUDE.md, read from the routing table sections that are already visible.
