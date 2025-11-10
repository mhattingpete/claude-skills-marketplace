---
name: code-execution
description: Execute Python code locally with marketplace API access for 90%+ token savings on bulk operations. Activates when user requests bulk operations (10+ files), complex multi-step workflows, iterative processing, or mentions efficiency/performance.
---

# Code Execution

Execute Python locally with API access. **90-99% token savings** for bulk operations.

## When to Use

- Bulk operations (10+ files)
- Complex multi-step workflows
- Iterative processing across many files
- User mentions efficiency/performance

## How to Use

Use direct Python imports in Claude Code:

```python
from execution_runtime import fs, code, transform, git

# Code analysis (metadata only!)
functions = code.find_functions('app.py', pattern='handle_.*')

# File operations
code_block = fs.copy_lines('source.py', 10, 20)
fs.paste_code('target.py', 50, code_block)

# Bulk transformations
result = transform.rename_identifier('.', 'oldName', 'newName', '**/*.py')

# Git operations
git.git_add(['.'])
git.git_commit('feat: refactor code')
```

**If not installed:** Run `~/.claude/plugins/marketplaces/mhattingpete-claude-skills/execution-runtime/setup.sh`

## Available APIs

- **Filesystem** (`fs`): copy_lines, paste_code, search_replace, batch_copy
- **Code Analysis** (`code`): find_functions, find_classes, analyze_dependencies - returns METADATA only!
- **Transformations** (`transform`): rename_identifier, remove_debug_statements, batch_refactor
- **Git** (`git`): git_status, git_add, git_commit, git_push

## Pattern

1. **Analyze locally** (metadata only, not source)
2. **Process locally** (all operations in execution)
3. **Return summary** (not data!)

## Examples

**Bulk refactor (50 files):**
```python
from execution_runtime import transform
result = transform.rename_identifier('.', 'oldName', 'newName', '**/*.py')
# Returns: {'files_modified': 50, 'total_replacements': 247}
```

**Extract functions:**
```python
from execution_runtime import code, fs

functions = code.find_functions('app.py', pattern='.*_util$')  # Metadata only!
for func in functions:
    code_block = fs.copy_lines('app.py', func['start_line'], func['end_line'])
    fs.paste_code('utils.py', -1, code_block)

result = {'functions_moved': len(functions)}
```

**Code audit (100 files):**
```python
from execution_runtime import code
from pathlib import Path

files = list(Path('.').glob('**/*.py'))
issues = []

for file in files:
    deps = code.analyze_dependencies(str(file))  # Metadata only!
    if deps.get('complexity', 0) > 15:
        issues.append({'file': str(file), 'complexity': deps['complexity']})

result = {'files_audited': len(files), 'high_complexity': len(issues)}
```

## Best Practices

✅ Return summaries, not data
✅ Use code_analysis (returns metadata, not source)
✅ Batch operations
✅ Handle errors, return error count

❌ Don't return all code to context
❌ Don't read full source when you need metadata
❌ Don't process files one by one

## Token Savings

| Files | Traditional | Execution | Savings |
|-------|-------------|-----------|---------|
| 10 | 5K tokens | 500 | 90% |
| 50 | 25K tokens | 600 | 97.6% |
| 100 | 150K tokens | 1K | 99.3% |
