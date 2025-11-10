---
name: code-refactor
description: Perform bulk code refactoring operations like renaming variables/functions across files, replacing patterns, and updating API calls. Use when users request renaming identifiers, replacing deprecated code patterns, updating method calls, or making consistent changes across multiple locations.
---

# Code Refactor

Systematic code refactoring across files. **Auto-switches to execution mode** for 10+ files (90% token savings).

## Mode Selection

- **1-9 files**: Use native tools (Grep + Edit with replace_all)
- **10+ files**: Automatically use `code-execution` skill

**Execution example (50 files):**
```python
from api.code_transform import rename_identifier
result = rename_identifier('.', 'oldName', 'newName', '**/*.py')
# Returns: {'files_modified': 50, 'total_replacements': 247}
# ~500 tokens vs ~25,000 tokens traditional
```

## When to Use

- "rename [identifier] to [new_name]"
- "replace all [pattern] with [replacement]"
- "refactor to use [new_pattern]"
- "update all calls to [function/API]"
- "convert [old_pattern] to [new_pattern]"

## Core Workflow (Native Mode)

### 1. Find All Occurrences
```
Grep(pattern="getUserData", output_mode="files_with_matches")     # Find files
Grep(pattern="getUserData", output_mode="content", -n=true, -B=2, -A=2)  # Verify with context
```

### 2. Replace All Instances
```
Edit(
  file_path="src/api.js",
  old_string="getUserData",
  new_string="fetchUserData",
  replace_all=true
)
```

### 3. Verify Changes
```
Grep(pattern="getUserData", output_mode="files_with_matches")  # Should return none
```

## Workflow Examples

### Rename Function
1. Find: `Grep(pattern="getUserData", output_mode="files_with_matches")`
2. Count: "Found 15 occurrences in 5 files"
3. Replace in each file with `replace_all=true`
4. Verify: Re-run Grep
5. Suggest: Run tests

### Replace Deprecated Pattern
1. Find: `Grep(pattern="\\bvar\\s+\\w+", output_mode="content", -n=true)`
2. Analyze: Check if reassigned (let) or constant (const)
3. Replace: `Edit(old_string="var count = 0", new_string="let count = 0")`
4. Verify: `npm run lint`

### Update API Calls
1. Find: `Grep(pattern="/api/auth/login", output_mode="content", -n=true)`
2. Replace: `Edit(old_string="'/api/auth/login'", new_string="'/api/v2/authentication/login'", replace_all=true)`
3. Test: Recommend integration tests

## Best Practices

**Planning:**
- Find all instances first
- Review context of each match
- Inform user of scope
- Consider edge cases (strings, comments)

**Safe Process:**
1. Search → Find all
2. Analyze → Verify appropriate
3. Inform → Tell user scope
4. Execute → Make changes
5. Verify → Confirm applied
6. Test → Suggest running tests

**Edge Cases:**
- Strings/comments: Ask if should update
- Exported APIs: Warn of breaking changes
- Case sensitivity: Be explicit

## Tool Reference

**Edit with replace_all:**
- `replace_all=true`: Replace all occurrences
- `replace_all=false`: Replace only first (or fail if multiple)
- Must match EXACTLY (whitespace, quotes)

**Grep patterns:**
- `-n=true`: Show line numbers
- `-B=N, -A=N`: Context lines
- `-i=true`: Case-insensitive
- `type="py"`: Filter by file type

## Integration

- **test-fixing**: Fix broken tests after refactoring
- **code-transfer**: Move refactored code
- **feature-planning**: Plan large refactorings
