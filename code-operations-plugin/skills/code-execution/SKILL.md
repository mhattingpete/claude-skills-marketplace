---
name: code-execution
description: Enables writing Python code that executes locally with access to marketplace APIs for bulk operations, complex transformations, and multi-file refactoring. Provides 90%+ token savings for large-scale operations. Activates when user requests bulk operations across many files, complex multi-step workflows, iterative processing, or mentions efficiency/performance.
---

# Code Execution

Execute Python code locally with access to powerful APIs for 90%+ token savings on complex operations.

## When to Use This Skill

**Activate when:**
- Bulk operations: "refactor 50 files", "update all imports", "process entire codebase"
- Complex workflows: "reorganize code structure", "extract all utility functions"
- Iterative processing: "find and transform all matching patterns"
- Performance needs: "do this efficiently", "batch operation", "process in parallel"
- Scale mentions: Any request involving 10+ files or repetitive operations

**Don't activate for:**
- Single file operations (use native tools)
- Simple read/edit tasks (use Read/Edit directly)
- Exploratory tasks (use Grep/Glob first)

## Prerequisites

Check if execution runtime is available:

```python
# Tool will be available if MCP server is configured
mcp__marketplace_execution__execute_python
```

**If not available**, guide user through 2-minute setup:

```
The execution runtime isn't configured yet. This will enable 90%+ token savings for bulk operations.

Setup (takes 2 minutes):
1. Run: ~/.claude/plugins/execution-runtime/setup.sh
2. Restart Claude Code/Desktop
3. Done!

Want me to walk you through it?
```

## Available APIs

### 1. Filesystem Operations
```python
from api.filesystem import (
    read_file, write_file,
    copy_lines, paste_code,
    search_replace,
    batch_copy, batch_transform
)
```

**Key functions:**
- `copy_lines(source_file, start_line, end_line)` - Copy specific lines
- `paste_code(target_file, line_number, code)` - Insert code at line
- `search_replace(file_pattern, search, replace)` - Bulk find/replace
- `batch_copy(operations)` - Process multiple copy operations at once

### 2. Code Analysis (AST-based)
```python
from api.code_analysis import (
    find_functions, find_classes,
    extract_imports, get_function_calls,
    analyze_dependencies
)
```

**Returns metadata only, NOT source code → huge token savings**

Example:
```python
functions = find_functions('app.py', pattern='handle_.*')
# Returns: [{'name': 'handle_request', 'start_line': 45, 'end_line': 60}]
# NOT the full function source code!
```

### 3. Code Transformation
```python
from api.code_transform import (
    rename_identifier,
    remove_debug_statements,
    add_docstrings,
    batch_refactor
)
```

### 4. Git Operations
```python
from api.git_operations import (
    git_status, git_add, git_commit, git_push
)
```

## Execution Pattern

### Step 1: Analyze Scope (in execution)
```python
from api.code_analysis import find_functions
from pathlib import Path

# Find all files (locally, zero context cost)
files = list(Path('.').glob('src/**/*.py'))

# Analyze each file (returns metadata only)
targets = []
for file in files:
    functions = find_functions(str(file), pattern='authenticate_.*')
    targets.extend(functions)

# Only metadata goes to context, not 50KB+ of source code
```

### Step 2: Process Locally
```python
from api.filesystem import copy_lines, paste_code

# Process all targets in execution environment
results = []
for target in targets:
    code = copy_lines(target['file'], target['start_line'], target['end_line'])
    transformed = code.replace('old_pattern', 'new_pattern')
    paste_code('new_file.py', -1, transformed)
    results.append({'file': target['file'], 'status': 'success'})
```

### Step 3: Return Summary Only
```python
# Return summary, not all the code!
result = {
    'files_processed': len(set(r['file'] for r in results)),
    'functions_moved': len(results),
    'errors': [r for r in results if r['status'] == 'error']
}
```

## Example Workflows

### Example 1: Bulk Refactoring
**User:** "Rename getUserData to fetchUserData in all Python files"

**Your response:**
```python
from api.code_transform import rename_identifier

result = rename_identifier(
    pattern='.',
    old_name='getUserData',
    new_name='fetchUserData',
    file_pattern='**/*.py'
)

# Returns: {'files_modified': 47, 'total_replacements': 183}
```

**Token usage:** ~500 tokens (vs ~25,000 without execution)

### Example 2: Extract Functions to New File
**User:** "Move all utility functions from app.py to utils.py"

```python
from api.code_analysis import find_functions
from api.filesystem import copy_lines, paste_code, read_file, write_file

# Find utility functions (metadata only)
functions = find_functions('app.py', pattern='.*_util$')

# Collect imports needed
imports = []
content = read_file('app.py')
for line in content.splitlines():
    if line.strip().startswith('import ') or line.strip().startswith('from '):
        imports.append(line)

# Create new file with imports
write_file('utils.py', '\\n'.join(set(imports)) + '\\n\\n')

# Copy each function
for func in functions:
    code = copy_lines('app.py', func['start_line'], func['end_line'])
    paste_code('utils.py', -1, code + '\\n\\n')

result = {
    'functions_extracted': len(functions),
    'function_names': [f['name'] for f in functions]
}
```

### Example 3: Add Type Hints to 100 Endpoints
**User:** "Add type hints to all API endpoint functions"

```python
from api.code_analysis import find_functions
from api.filesystem import read_file, write_file
from pathlib import Path
import re

# Find all endpoint files
files = list(Path('api').glob('**/*.py'))
endpoints_updated = []

for file in files:
    # Find endpoint functions
    functions = find_functions(str(file), pattern='(get|post|put|delete)_.*')

    if not functions:
        continue

    # Read file content
    content = read_file(str(file))
    lines = content.splitlines()

    # Add type hints (simple heuristic)
    for func in functions:
        func_line_idx = func['start_line'] - 1
        func_line = lines[func_line_idx]

        # Check if already has type hints
        if '->' in func_line:
            continue

        # Add -> Dict return type hint
        if func_line.strip().endswith(':'):
            lines[func_line_idx] = func_line.replace(':', ' -> Dict[str, Any]:')
            endpoints_updated.append(f"{file}:{func['name']}")

    # Write back
    write_file(str(file), '\\n'.join(lines), create_backup=True)

result = {
    'endpoints_updated': len(endpoints_updated),
    'files_modified': len(set(e.split(':')[0] for e in endpoints_updated))
}
```

### Example 4: Codebase Audit
**User:** "Audit code quality across the entire codebase"

```python
from api.code_analysis import analyze_dependencies, find_unused_imports
from pathlib import Path

files = list(Path('.').glob('**/*.py'))

issues = {
    'high_complexity': [],
    'unused_imports': [],
    'large_files': []
}

for file in files:
    # Analyze complexity
    deps = analyze_dependencies(str(file))

    if deps.get('complexity', 0) > 15:
        issues['high_complexity'].append({
            'file': str(file),
            'complexity': deps['complexity'],
            'functions': deps['functions']
        })

    if deps.get('lines', 0) > 500:
        issues['large_files'].append({
            'file': str(file),
            'lines': deps['lines']
        })

    # Find unused imports
    unused = find_unused_imports(str(file))
    if unused:
        issues['unused_imports'].append({
            'file': str(file),
            'unused': unused
        })

result = {
    'files_audited': len(files),
    'high_complexity_count': len(issues['high_complexity']),
    'files_with_unused_imports': len(issues['unused_imports']),
    'large_files_count': len(issues['large_files']),
    'top_issues': issues['high_complexity'][:5]  # Top 5 only
}
```

## Advanced Features

### Stateful Refactoring Sessions

For operations that might be interrupted:

```python
# Create session
session = create_refactoring_session(
    "modernize-codebase",
    "Update to Python 3.11+ syntax"
)

# Process with checkpoints
from pathlib import Path
files = list(Path('.').glob('**/*.py'))

for i, file in enumerate(files):
    # ... process file ...

    # Save progress every 10 files
    if i % 10 == 0:
        save_session_state(session['id'], {
            'processed': i,
            'total': len(files),
            'current_file': str(file)
        })
```

### Reusable Skills

Save transformations for future use:

```python
save_reusable_skill(
    name="modernize_string_formatting",
    code=\"\"\"
def transform(code):
    import re
    # Replace % formatting with f-strings
    # (simplified example)
    pattern = r'"([^"]*)" % \\(([^)]+)\\)'
    replacement = r'f"\\1"'
    return re.sub(pattern, replacement, code)
\"\"\",
    description="Convert old % formatting to f-strings"
)
```

## Token Savings Examples

### Without Execution (Traditional)
```
User: "Refactor 50 files to use new API"

1. Grep to find files → 2K tokens
2. Read 50 files → 50K tokens (1KB each)
3. Edit 50 files → 50K tokens (multiple rounds)
4. Verify changes → 10K tokens

Total: ~112K tokens ❌
```

### With Execution (This Skill)
```
User: "Refactor 50 files to use new API"

Claude writes Python script (~500 tokens):
```python
from api.code_transform import rename_identifier
result = rename_identifier(...)
```

Executes locally, returns summary (~100 tokens):
```json
{"files_modified": 50, "replacements": 247}
```

Total: ~600 tokens ✅ (99.5% savings)
```

## Decision Tree: When to Use Execution Mode

```
Is operation on 10+ files?
├─ YES → Use execution mode
└─ NO → Is it complex multi-step?
    ├─ YES → Use execution mode
    └─ NO → Is it iterative/repetitive?
        ├─ YES → Use execution mode
        └─ NO → Use native tools (Read/Edit/Grep)
```

## Best Practices

### 1. Always Return Summaries, Not Data
```python
# ❌ BAD - Returns all code to context
results = []
for file in files:
    code = read_file(file)
    results.append({'file': file, 'code': code})  # Huge!
result = results

# ✅ GOOD - Returns summary only
files_processed = 0
for file in files:
    code = read_file(file)
    # ... process locally ...
    files_processed += 1
result = {'files_processed': files_processed}
```

### 2. Use Code Analysis, Not Source Reading
```python
# ❌ BAD - Reads full source into context
code = read_file('app.py')
# Now 10KB of code is in context

# ✅ GOOD - Gets metadata only
functions = find_functions('app.py')
# Only ~200 bytes of metadata in context
```

### 3. Batch Operations
```python
# ❌ BAD - Multiple operations
for file in files:
    code = copy_lines(file, 10, 20)
    paste_code(target, -1, code)

# ✅ GOOD - Single batch operation
operations = [
    {'source_file': f, 'start_line': 10, 'end_line': 20,
     'target_file': target, 'target_line': -1}
    for f in files
]
batch_copy(operations)
```

### 4. Error Handling
```python
results = []
errors = []

for file in files:
    try:
        # ... process file ...
        results.append({'file': str(file), 'status': 'success'})
    except Exception as e:
        errors.append({'file': str(file), 'error': str(e)})

result = {
    'success_count': len(results),
    'error_count': len(errors),
    'errors': errors[:5]  # Only first 5 errors
}
```

## Security

All execution is automatically secured:

✅ **Sandboxed** - RestrictedPython environment
✅ **Resource limits** - 30s timeout, 256MB memory
✅ **Restricted imports** - Only `api.*` and safe stdlib
✅ **PII masking** - Secrets automatically redacted from results
✅ **Directory restrictions** - Only allowed directories accessible

## Troubleshooting

### "Module 'api' not found"
```
The execution runtime isn't properly configured. Run:
~/.claude/plugins/execution-runtime/setup.sh
```

### "Import not allowed in sandbox"
```python
# ❌ NOT ALLOWED
import requests  # Not in whitelist
import os  # Restricted

# ✅ ALLOWED
import re  # Safe stdlib
import json  # Safe stdlib
from api.filesystem import copy_lines  # Marketplace API
```

### "Execution timeout"
Process is taking >30 seconds. Break into smaller batches:

```python
# ❌ Process all 1000 files at once (timeout)
for file in all_files:  # Too many!
    process(file)

# ✅ Process in batches
from itertools import islice

def chunks(iterable, size):
    iterator = iter(iterable)
    while chunk := list(islice(iterator, size)):
        yield chunk

for batch in chunks(all_files, 50):
    for file in batch:
        process(file)
```

## Integration with Other Skills

- **code-transfer**: Use execution mode for bulk transfers (10+ operations)
- **code-refactor**: Automatically switches to execution for bulk refactoring
- **test-fixing**: Can analyze test failures locally before fixing
- **git-pushing**: Combine with git operations to commit batches

## Performance Metrics

| Operation | Files | Traditional | Execution | Savings |
|-----------|-------|-------------|-----------|---------|
| Copy functions | 1 | 100 tokens | 50 tokens | 50% |
| Rename identifier | 10 | 5K tokens | 500 tokens | 90% |
| Bulk refactor | 50 | 25K tokens | 600 tokens | 97.6% |
| Code audit | 100 | 150K tokens | 1K tokens | 99.3% |
| Codebase reorganization | 200+ | 500K+ tokens | 2K tokens | 99.6% |

## Summary

**Use execution mode when:**
- Operating on 10+ files
- Complex multi-step workflows
- Iterative processing
- Performance is important

**Benefits:**
- 90-99% token savings
- Faster execution
- Stateful operations
- Automatic security

**Setup:**
```bash
~/.claude/plugins/execution-runtime/setup.sh
```

**Example:**
```python
from api.code_transform import rename_identifier
result = rename_identifier('.', 'old_name', 'new_name', '**/*.py')
```

**Result:** Process 50 files with 600 tokens instead of 25,000 tokens ✨
