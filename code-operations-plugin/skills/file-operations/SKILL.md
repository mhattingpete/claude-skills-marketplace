---
name: file-operations
description: Analyze files and get detailed metadata including size, line counts, modification times, and content statistics. Use when users request file information, statistics, or analysis without modifying files.
---

# File Operations

Analyze files and retrieve metadata using Claude's native tools without modifying files.

## When to Use

- "analyze [file]"
- "get file info for [file]"
- "how many lines in [file]"
- "compare [file1] and [file2]"
- "file statistics"

## Core Operations

### File Size & Metadata
```bash
stat -f "%z bytes, modified %Sm" [file_path]  # Single file
ls -lh [directory]                             # Multiple files
du -h [file_path]                              # Human-readable size
```

### Line Counts
```bash
wc -l [file_path]                              # Single file
wc -l [file1] [file2]                          # Multiple files
find [dir] -name "*.py" | xargs wc -l          # Directory total
```

### Content Analysis
Use **Read** to analyze structure, then count functions/classes/imports.

### Pattern Search
```
Grep(pattern="^def ", output_mode="count", path="src/")        # Count functions
Grep(pattern="TODO|FIXME", output_mode="content", -n=true)    # Find TODOs
Grep(pattern="^import ", output_mode="count")                 # Count imports
```

### Find Files
```
Glob(pattern="**/*.py")
```

## Workflow Examples

### Comprehensive File Analysis
1. Get size/mod time: `stat -f "%z bytes, modified %Sm" file.py`
2. Count lines: `wc -l file.py`
3. Read file: `Read(file_path="file.py")`
4. Count functions: `Grep(pattern="^def ", output_mode="count")`
5. Count classes: `Grep(pattern="^class ", output_mode="count")`

### Compare File Sizes
1. Find files: `Glob(pattern="src/**/*.py")`
2. Get sizes: `ls -lh src/**/*.py`
3. Total size: `du -sh src/*.py`

### Code Quality Metrics
1. Total lines: `find . -name "*.py" | xargs wc -l`
2. Test files: `find . -name "test_*.py" | wc -l`
3. TODOs: `Grep(pattern="TODO|FIXME|HACK", output_mode="count")`

### Find Largest Files
```bash
find . -type f -not -path "./node_modules/*" -exec du -h {} + | sort -rh | head -20
```

## Best Practices

- **Non-destructive**: Use Read/stat/wc, never modify
- **Efficient**: Read small files fully, use Grep for large files
- **Context-aware**: Compare to project averages, suggest optimizations

## Integration

Works with:
- **code-auditor**: Comprehensive analysis
- **code-transfer**: After identifying large files
- **codebase-documenter**: Understanding file purposes
