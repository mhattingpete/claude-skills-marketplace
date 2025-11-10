---
name: code-transfer
description: Transfer code between files with line-based precision. Use when users request copying code from one location to another, moving functions or classes between files, extracting code blocks, or inserting code at specific line numbers.
---

# Code Transfer

Transfer code between files with precise line-based control. **Dual-mode operation**: native tools (1-10 files) or execution mode (10+ files, 90% token savings).

## Operation Modes

### Basic Mode (Default)
Use Read, Edit, Bash scripts for 1-10 file operations. Works immediately, no setup required.

### Execution Mode (10+ files)
```python
from api.filesystem import batch_copy
from api.code_analysis import find_functions

functions = find_functions('app.py', pattern='handle_.*')
operations = [{
    'source_file': 'app.py',
    'start_line': f['start_line'],
    'end_line': f['end_line'],
    'target_file': 'handlers.py',
    'target_line': -1
} for f in functions]
batch_copy(operations)
```

## When to Use

- "copy this code to [file]"
- "move [function/class] to [file]"
- "extract this to a new file"
- "insert at line [number]"
- "reorganize into separate files"

## Core Operations

### 1. Extract Source Code
```
Read(file_path="src/auth.py")                              # Full file
Read(file_path="src/auth.py", offset=10, limit=20)         # Line range
Grep(pattern="def authenticate", -n=true, -A=10)           # Find function
```

### 2. Insert at Specific Line
Use `line_insert.py` script for line-based insertion:

```bash
python3 skills/code-transfer/scripts/line_insert.py <file> <line_number> <code> [--backup]
```

**Examples:**
```bash
# Insert function at line 50
python3 skills/code-transfer/scripts/line_insert.py src/utils.py 50 "def helper():\n    pass"

# Insert with backup
python3 skills/code-transfer/scripts/line_insert.py src/utils.py 50 "code" --backup

# Insert at beginning
python3 skills/code-transfer/scripts/line_insert.py src/new.py 1 "import os"
```

**When to use:**
- User specifies exact line number
- Inserting into new/empty files
- Inserting at beginning/end without context

### 3. Insert Relative to Content
Use **Edit** when insertion point is relative to existing code:

```
Edit(
  file_path="src/utils.py",
  old_string="def existing():\n    pass",
  new_string="def existing():\n    pass\n\ndef new():\n    return True"
)
```

## Workflow Examples

### Copy Function Between Files
1. Find: `Grep(pattern="def validate_user", -n=true, -A=20)`
2. Extract: `Read(file_path="auth.py", offset=45, limit=15)`
3. Check target: `Read(file_path="validators.py")`
4. Insert: Use `line_insert.py` or Edit based on context

### Extract Class to New File
1. Locate: `Grep(pattern="class DatabaseConnection", -n=true, -A=50)`
2. Extract: `Read(file_path="original.py", offset=100, limit=50)`
3. Create: `Write(file_path="database.py", content="<extracted>")`
4. Update imports: `Edit` in original file
5. Remove old class: `Edit` with replacement

### Insert at Specific Line
1. Validate: `Read(file_path="main.py", offset=20, limit=10)`
2. Insert: `python3 skills/code-transfer/scripts/line_insert.py main.py 25 "logger.info('...')" --backup`
3. Verify: `Read(file_path="main.py", offset=23, limit=5)`

### Reorganize Into Modules
1. Analyze: `Read(file_path="utils.py")`
2. Identify groups: `Grep(pattern="^def |^class ", -n=true)`
3. Extract each category: `Write` new files
4. Update original: Re-export or redirect

## Best Practices

**Planning:**
- Understand dependencies (imports, references)
- Identify exact start/end of code block
- Check target file structure
- Ensure necessary imports included

**Preservation:**
- Include docstrings and comments
- Transfer related functions together
- Update imports in both files
- Maintain formatting/indentation

**Validation:**
- Verify insertion placement
- Check syntax
- Test imports
- Suggest running tests

**Backups:**
- Use `--backup` for significant changes
- Critical file operations
- Large deletions

## Integration

- **code-refactor**: Refactor after transferring
- **test-fixing**: Run tests after reorganizing
- **feature-planning**: Plan large reorganizations
