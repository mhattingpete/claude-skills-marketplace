---
name: code-transfer
description: Transfer code between files with line-based precision. Use when users request copying code from one location to another, moving functions or classes between files, extracting code blocks, or inserting code at specific line numbers. Activates on phrases like "copy this code to", "move this function to", "extract this to a new file", or "insert at line N".
---

# Code Transfer

## Overview

Transfer code between files with precise line-based control. This skill enables copying, moving, and inserting code at specific line numbers, which complements Claude's native Edit tool that requires exact string matching.

## When to Use This Skill

Activate this skill when users request:
- **Copy code between files**: "Copy the `authenticate` function from auth.py to utils.py"
- **Move code blocks**: "Move this class to a separate file"
- **Extract code**: "Extract this function into a new file"
- **Line-based insertion**: "Insert this code at line 45"
- **Reorganize code**: "Split this file into multiple modules"

**Activation phrases:**
- "copy this code to [file]"
- "move [function/class] to [file]"
- "extract this to a new file"
- "insert at line [number]"
- "transfer code from X to Y"
- "reorganize this into separate files"

## Core Capabilities

### 1. Extract Source Code

Use the **Read** tool to extract code from source files:

**Full file extraction:**
```
Read(file_path="src/auth.py")
```

**Line range extraction:**
```
Read(file_path="src/auth.py", offset=10, limit=20)
```

**Function/class identification:**
Use Grep to find specific functions or classes:
```
Grep(pattern="def authenticate", path="src/auth.py", output_mode="content", -n=true, -A=10)
```

### 2. Insert Code at Specific Line Numbers

When inserting code at a **specific line number** (not replacing existing text), use the `line_insert.py` script:

**Script location:** `skills/code-transfer/scripts/line_insert.py`

**Usage:**
```bash
python3 skills/code-transfer/scripts/line_insert.py <file_path> <line_number> <code> [--backup]
```

**Parameters:**
- `file_path`: Target file path (creates if doesn't exist)
- `line_number`: Where to insert (1-based index)
- `code`: Code to insert (use literal newlines or \\n)
- `--backup`: Optional flag to create timestamped backup

**Examples:**
```bash
# Insert a function at line 50
python3 skills/code-transfer/scripts/line_insert.py src/utils.py 50 "def helper():\\n    pass"

# Insert with backup
python3 skills/code-transfer/scripts/line_insert.py src/utils.py 50 "def helper():\\n    pass" --backup

# Insert at beginning of file
python3 skills/code-transfer/scripts/line_insert.py src/new.py 1 "import os\\nimport sys"
```

**When to use line_insert.py vs Edit:**
- **Use line_insert.py** when:
  - User specifies exact line number
  - Inserting into new/empty files
  - Inserting at beginning/end without context
  - Creating new sections in files

- **Use Edit** when:
  - Replacing existing code (you have the exact old_string)
  - Inserting relative to existing code (add after/before specific content)
  - The insertion point is defined by content, not line number

### 3. Replace or Insert Adjacent to Existing Code

When the insertion point is **relative to existing content**, use the **Edit** tool:

```
Edit(
  file_path="src/utils.py",
  old_string="def existing_function():\\n    pass",
  new_string="def existing_function():\\n    pass\\n\\ndef new_function():\\n    return True"
)
```

## Workflow Examples

### Example 1: Copy Function Between Files

**User:** "Copy the `validate_user` function from auth.py to validators.py"

**Workflow:**
1. **Find the function** using Grep:
   ```
   Grep(pattern="def validate_user", path="auth.py", output_mode="content", -n=true, -A=20)
   ```

2. **Extract the complete function** using Read (with line offset/limit from grep results):
   ```
   Read(file_path="auth.py", offset=45, limit=15)
   ```

3. **Check target file structure** to determine insertion point:
   ```
   Read(file_path="validators.py")
   ```

4. **Insert using appropriate method**:
   - If user specified line number → use `line_insert.py`
   - If inserting at end → use `line_insert.py` with line number = file length + 1
   - If inserting near existing code → use Edit

### Example 2: Extract Class to New File

**User:** "Move the `DatabaseConnection` class to a new file database.py"

**Workflow:**
1. **Locate the class**:
   ```
   Grep(pattern="class DatabaseConnection", output_mode="content", -n=true, -A=50)
   ```

2. **Extract full class definition**:
   ```
   Read(file_path="original.py", offset=100, limit=50)
   ```

3. **Create new file with the class**:
   ```
   Write(file_path="database.py", content="<extracted_class>")
   ```

4. **Update imports in original file** (using Edit):
   ```
   Edit(
     file_path="original.py",
     old_string="class DatabaseConnection:",
     new_string="from database import DatabaseConnection\\n"
   )
   ```

5. **Remove old class from original** (using Edit with empty replacement if needed)

### Example 3: Insert at Specific Line Number

**User:** "Insert this logging code at line 25 in main.py"

**Workflow:**
1. **Validate the target location** (optional but recommended):
   ```
   Read(file_path="main.py", offset=20, limit=10)
   ```

2. **Use line_insert.py script**:
   ```bash
   python3 skills/code-transfer/scripts/line_insert.py main.py 25 "logger.info('Starting process')\\nlogger.debug('Debug mode enabled')" --backup
   ```

3. **Verify the insertion**:
   ```
   Read(file_path="main.py", offset=23, limit=5)
   ```

### Example 4: Reorganize File Into Multiple Modules

**User:** "Split utils.py into separate files for each utility category"

**Workflow:**
1. **Analyze the file structure**:
   ```
   Read(file_path="utils.py")
   ```

2. **Identify logical groupings** using Grep:
   ```
   Grep(pattern="^def |^class ", path="utils.py", output_mode="content", -n=true)
   ```

3. **For each category**, extract and create new files:
   - Extract string utilities → `Write(file_path="string_utils.py", content=...)`
   - Extract file utilities → `Write(file_path="file_utils.py", content=...)`
   - etc.

4. **Update original file** to re-export or redirect

## Best Practices

### Planning Before Transferring

Before transferring code:
1. **Understand dependencies**: Check imports, references to other code
2. **Identify scope**: Determine exact start/end of code block
3. **Check target location**: Verify target file structure and appropriate insertion point
4. **Consider imports**: Ensure necessary imports are included

### Preserving Code Context

When transferring code:
- **Include docstrings** and comments
- **Transfer related functions** together if they're interdependent
- **Update imports** in both source and target files
- **Maintain formatting** and indentation

### Validation

After transferring:
1. **Verify insertion**: Read the affected areas to confirm correct placement
2. **Check syntax**: Ensure no syntax errors introduced
3. **Test imports**: Verify that import statements work
4. **Suggest testing**: Recommend running tests if available

### When to Create Backups

Always create backups (`--backup` flag) when:
- Making significant structural changes
- User explicitly requests safety
- Working with critical files
- Operations involve deletion of large code blocks

## Error Handling

### Common Issues and Solutions

**Issue:** "Line number out of range"
- **Solution:** Check file length first with `wc -l` or Read tool

**Issue:** "Indentation errors after insertion"
- **Solution:** Ensure extracted code maintains proper indentation level for target context

**Issue:** "Import errors after transfer"
- **Solution:** Analyze dependencies and add necessary imports to target file

**Issue:** "Code inserted at wrong location"
- **Solution:** Verify line numbers by reading context around insertion point first

## Integration with Other Tools

### Working with Claude's Native Tools

- **Read**: Extract source code (supports line ranges)
- **Edit**: Insert relative to existing content (requires exact string match)
- **Write**: Create new files with transferred code
- **Grep**: Find functions, classes, or patterns across files
- **Bash**: Get file info (`wc -l`), verify syntax (`python -m py_compile`)

### Working with Other Skills

- **code-refactor**: After transferring, refactor code to fit new context
- **test-fixing**: Run tests after reorganizing to ensure nothing broke
- **feature-planning**: Plan large-scale code reorganization before transferring

## Script Details

### line_insert.py

**Purpose:** Insert code at specific line numbers when Edit tool's string matching isn't suitable.

**Key features:**
- 1-based line numbering (line 1 = first line)
- Automatic file creation if target doesn't exist
- Optional timestamped backups
- Multi-line code support
- UTF-8 encoding

**Security:** Basic path validation to prevent directory traversal

**Dependencies:** Python 3.6+ (stdlib only, no external packages needed)

**Output:** Writes to stderr for status messages, making it safe to use with stdout capture
