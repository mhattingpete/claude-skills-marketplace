---
name: file-operations
description: Analyze files and get detailed metadata including size, line counts, modification times, and content statistics. Use when users request file information, statistics, or analysis without modifying files. Activates on phrases like "analyze this file", "get file info", "how many lines", "file statistics", or "show file details".
---

# File Operations

## Overview

Analyze files and retrieve detailed metadata using Claude's native tools. This skill provides convenient workflows for gathering file statistics, comparing files, and analyzing code structure without making modifications.

## When to Use This Skill

Activate this skill when users request:
- **File metadata**: "What's the size of config.json?"
- **Line counts**: "How many lines are in this file?"
- **File comparison**: "Compare the sizes of these two files"
- **Code statistics**: "Analyze the structure of this Python file"
- **File details**: "Show me info about all JavaScript files"

**Activation phrases:**
- "analyze [file]"
- "get file info for [file]"
- "how many lines in [file]"
- "file statistics for [file]"
- "show details of [file]"
- "compare [file1] and [file2]"

## Core Operations

### 1. Get File Size and Modification Time

Use **Bash** commands for quick file metadata:

**Single file info:**
```bash
stat -f "%z bytes, modified %Sm" [file_path]
```

**Multiple files:**
```bash
ls -lh [directory]
```

**File size in human-readable format:**
```bash
du -h [file_path]
```

### 2. Count Lines in Files

**Line count for single file:**
```bash
wc -l [file_path]
```

**Line count for multiple files:**
```bash
wc -l [file1] [file2] [file3]
```

**Total lines in directory:**
```bash
find [directory] -name "*.py" | xargs wc -l
```

### 3. Analyze File Content

Use **Read** tool to analyze structure:

```
Read(file_path="src/app.py")
```

Then analyze the content:
- Count functions/classes
- Identify imports
- Check documentation coverage
- Assess complexity

### 4. Search for Patterns

Use **Grep** to analyze code patterns:

**Count function definitions:**
```
Grep(pattern="^def ", output_mode="count", path="src/")
```

**Find TODOs:**
```
Grep(pattern="TODO|FIXME|XXX", output_mode="content", -n=true)
```

**Count imports:**
```
Grep(pattern="^import |^from .* import", output_mode="count", path="src/")
```

### 5. Find Files by Pattern

Use **Glob** to discover files:

```
Glob(pattern="**/*.py")
```

## Workflow Examples

### Example 1: Comprehensive File Analysis

**User:** "Analyze app.py and tell me about it"

**Workflow:**
1. **Get file size and modification time**:
   ```bash
   stat -f "%z bytes, modified %Sm" app.py
   ```

2. **Count lines**:
   ```bash
   wc -l app.py
   ```

3. **Read the file**:
   ```
   Read(file_path="app.py")
   ```

4. **Analyze structure**:
   - Count functions: `Grep(pattern="^def ", output_mode="count", path="app.py")`
   - Count classes: `Grep(pattern="^class ", output_mode="count", path="app.py")`
   - Find imports: `Grep(pattern="^import |^from ", output_mode="content", -n=true, path="app.py")`

5. **Report findings**:
   ```
   app.py Analysis:
   - Size: 15.2 KB
   - Lines: 456
   - Functions: 12
   - Classes: 3
   - Imports: 8 modules
   - Last modified: 2025-10-20
   ```

### Example 2: Compare File Sizes

**User:** "Compare the sizes of all Python files in src/"

**Workflow:**
1. **Find all Python files**:
   ```
   Glob(pattern="src/**/*.py")
   ```

2. **Get sizes for each file**:
   ```bash
   ls -lh src/**/*.py
   ```

3. **Calculate total size**:
   ```bash
   du -sh src/*.py
   ```

4. **Present comparison**:
   ```
   Python Files in src/:
   - auth.py: 25 KB (largest)
   - utils.py: 18 KB
   - config.py: 3 KB
   - main.py: 12 KB
   Total: 58 KB across 4 files
   ```

### Example 3: Code Quality Metrics

**User:** "Give me code quality metrics for the project"

**Workflow:**
1. **Total line count**:
   ```bash
   find . -name "*.py" -not -path "./venv/*" | xargs wc -l
   ```

2. **Count test coverage** (test files vs source files):
   ```bash
   find . -name "test_*.py" | wc -l
   find . -name "*.py" -not -name "test_*" | wc -l
   ```

3. **Find TODOs and FIXMEs**:
   ```
   Grep(pattern="TODO|FIXME|HACK|XXX", output_mode="count")
   ```

4. **Find missing docstrings**:
   ```
   Grep(pattern="^def |^class ", output_mode="content", -n=true, -A=1)
   ```
   (Then analyze which don't have docstrings)

5. **Report metrics**:
   ```
   Code Quality Metrics:
   - Total lines of code: 3,456
   - Source files: 28
   - Test files: 15 (54% coverage by count)
   - TODOs/FIXMEs: 12
   - Functions without docstrings: 8
   ```

### Example 4: Find Largest Files

**User:** "What are the largest files in this project?"

**Workflow:**
1. **List all files by size**:
   ```bash
   find . -type f -not -path "./node_modules/*" -not -path "./.git/*" -exec du -h {} + | sort -rh | head -20
   ```

2. **Identify file types** of largest files

3. **Analyze if large files need refactoring**:
   - If source code file > 500 lines, suggest splitting
   - If data file, check if it should be externalized

4. **Present findings**:
   ```
   Largest Files:
   1. data/dataset.json - 2.3 MB (consider externalizing)
   2. src/processor.py - 1,245 lines (suggest refactoring)
   3. build/bundle.js - 856 KB (expected for bundle)
   ```

### Example 5: Directory Structure Analysis

**User:** "Show me the structure of the src/ directory"

**Workflow:**
1. **Use tree command** (if available):
   ```bash
   tree src/ -L 2
   ```

2. **Or use find**:
   ```bash
   find src/ -type f -o -type d | sort
   ```

3. **Count files by type**:
   ```bash
   find src/ -name "*.py" | wc -l
   find src/ -name "*.js" | wc -l
   find src/ -name "*.json" | wc -l
   ```

4. **Analyze organization**:
   - Check for consistent directory structure
   - Identify orphaned files
   - Note missing documentation

5. **Present structure**:
   ```
   src/ Directory Structure:
   ├── api/ (8 Python files)
   ├── models/ (5 Python files)
   ├── utils/ (12 Python files)
   ├── tests/ (15 test files)
   └── config.json

   Total: 40 Python files, 1 config
   ```

## Best Practices

### Non-Destructive Analysis

This skill should NEVER modify files:
- Use `Read` not `Write`
- Use `stat/ls/wc` not modification commands
- Use `Grep` with `output_mode` not `sed/awk`

### Efficient Information Gathering

**For small files (<100 lines):**
- Read entire file and analyze in context

**For large files (>1000 lines):**
- Use Grep to find specific patterns
- Use `wc -l` for line counts
- Use `head/tail` for quick preview

**For many files:**
- Use Glob to find files first
- Use parallel Bash commands where appropriate
- Summarize rather than showing all details

### Context-Aware Reporting

When reporting file information:
- Include relevant context (e.g., "large for a config file")
- Compare to project averages
- Suggest optimizations if appropriate
- Use human-readable formats

## Integration with Other Tools

### Working with Claude's Native Tools

- **Read**: Read full file content for analysis
- **Grep**: Search patterns, count occurrences
- **Glob**: Find files by pattern
- **Bash**: Execute stat, wc, du, ls, find commands

### Working with Other Skills

- **code-auditor**: For comprehensive codebase analysis
- **code-transfer**: After identifying large files that need splitting
- **codebase-documenter**: For understanding file purposes and relationships

## Common Use Cases

### Development Workflow

**Pre-commit analysis:**
- Check file sizes before committing
- Count lines of new code
- Verify no large files added

**Code review:**
- Compare file versions
- Check complexity metrics
- Identify files needing attention

**Refactoring decisions:**
- Find largest/most complex files
- Identify files with too many responsibilities
- Locate duplicate code patterns

### Project Management

**Progress tracking:**
- Count lines of code over time
- Track test coverage ratios
- Monitor technical debt (TODOs)

**Documentation:**
- Find undocumented files
- Identify missing docstrings
- Check README completeness

## Tool Reference

### Bash Commands for File Operations

**File size:**
- `du -h [file]` - Human-readable size
- `stat -f "%z" [file]` - Exact bytes (macOS)
- `stat -c "%s" [file]` - Exact bytes (Linux)

**Line counts:**
- `wc -l [file]` - Count lines
- `wc -w [file]` - Count words
- `wc -c [file]` - Count bytes

**File info:**
- `stat [file]` - Complete file stats
- `file [file]` - File type
- `ls -lh [file]` - Permissions, size, date

**Find files:**
- `find [dir] -name "pattern"` - Find by name
- `find [dir] -type f -size +1M` - Find large files
- `find [dir] -mtime -7` - Modified in last 7 days

### Grep for Analysis

**Count occurrences:**
```
Grep(pattern="pattern", output_mode="count")
```

**Find with context:**
```
Grep(pattern="pattern", output_mode="content", -n=true, -B=2, -A=2)
```

**Count per file:**
```
Grep(pattern="pattern", output_mode="count", path="dir/")
```
