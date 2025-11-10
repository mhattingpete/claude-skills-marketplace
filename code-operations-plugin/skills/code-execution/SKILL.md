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

## Check Availability

Tool exists: `mcp__marketplace_execution__execute_python`

If not available, guide user: `~/.claude/plugins/marketplaces/mhattingpete-claude-skills/execution-runtime/setup.sh`

## Available APIs

```python
# Filesystem - returns only what you need
from api.filesystem import copy_lines, paste_code, search_replace, batch_copy

# Code Analysis - returns METADATA only (not source code!)
from api.code_analysis import find_functions, find_classes, analyze_dependencies

# Transformations - bulk refactoring
from api.code_transform import rename_identifier, remove_debug_statements, batch_refactor

# Git operations
from api.git_operations import git_status, git_add, git_commit
```

## Pattern

1. **Analyze locally** (metadata only, not source)
2. **Process locally** (all operations in execution)
3. **Return summary** (not data!)

## Examples

**Bulk refactor (50 files):**
```python
from api.code_transform import rename_identifier
result = rename_identifier('.', 'oldName', 'newName', '**/*.py')
# Returns: {'files_modified': 50, 'total_replacements': 247}
```

**Extract functions:**
```python
from api.code_analysis import find_functions
from api.filesystem import copy_lines, paste_code

functions = find_functions('app.py', pattern='.*_util$')  # Metadata only!
for func in functions:
    code = copy_lines('app.py', func['start_line'], func['end_line'])
    paste_code('utils.py', -1, code)

result = {'functions_moved': len(functions)}
```

**Code audit (100 files):**
```python
from api.code_analysis import analyze_dependencies
from pathlib import Path

files = list(Path('.').glob('**/*.py'))
issues = []

for file in files:
    deps = analyze_dependencies(str(file))  # Metadata only!
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
