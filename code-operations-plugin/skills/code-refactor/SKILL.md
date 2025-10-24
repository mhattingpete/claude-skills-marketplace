---
name: code-refactor
description: Perform bulk code refactoring operations like renaming variables/functions across files, replacing patterns, and updating API calls. Use when users request renaming identifiers, replacing deprecated code patterns, updating method calls, or making consistent changes across multiple locations. Activates on phrases like "rename all instances", "replace X with Y everywhere", "refactor to use", or "update all calls to".
---

# Code Refactor

## Overview

Perform systematic code refactoring operations across files using pattern-based search and replace. This skill focuses on bulk transformations that maintain code functionality while improving structure, naming, or updating APIs.

## When to Use This Skill

Activate this skill when users request:
- **Rename variables/functions**: "Rename `getUserData` to `fetchUserData` everywhere"
- **Replace deprecated patterns**: "Replace all `var` declarations with `let` or `const`"
- **Update API calls**: "Update all calls to the old authentication API"
- **Refactor patterns**: "Convert all callbacks to async/await"
- **Standardize code**: "Make all import statements use absolute paths"

**Activation phrases:**
- "rename [identifier] to [new_name]"
- "replace all [pattern] with [replacement]"
- "refactor to use [new_pattern]"
- "update all calls to [function/API]"
- "convert [old_pattern] to [new_pattern]"
- "standardize [aspect] across the codebase"

## Core Capabilities

### 1. Find All Occurrences

Before refactoring, locate all instances of the pattern to understand scope and impact.

**Search for exact matches:**
```
Grep(pattern="getUserData", output_mode="files_with_matches")
```

**Search with context to verify usage:**
```
Grep(pattern="getUserData", output_mode="content", -n=true, -B=2, -A=2)
```

**Case-insensitive search:**
```
Grep(pattern="getuserdata", -i=true, output_mode="files_with_matches")
```

**Regex patterns:**
```
Grep(pattern="get\\w+Data", output_mode="content")
```

### 2. Replace All Instances

Use the **Edit** tool with `replace_all=true` for bulk replacements:

**Simple replacement:**
```
Edit(
  file_path="src/api.js",
  old_string="getUserData",
  new_string="fetchUserData",
  replace_all=true
)
```

**Multi-line replacement:**
```
Edit(
  file_path="src/auth.js",
  old_string="function authenticate(user) {\\n  return user.valid;\\n}",
  new_string="async function authenticate(user) {\\n  return await validateUser(user);\\n}",
  replace_all=true
)
```

### 3. Targeted Replacement

For single occurrences or when context matters, use Edit without `replace_all`:

```
Edit(
  file_path="src/config.js",
  old_string="const API_URL = 'http://old-api.com'",
  new_string="const API_URL = 'https://new-api.com'"
)
```

## Workflow Examples

### Example 1: Rename Function Across Codebase

**User:** "Rename `getUserData` to `fetchUserData` everywhere"

**Workflow:**
1. **Find all occurrences** to understand scope:
   ```
   Grep(pattern="getUserData", output_mode="files_with_matches")
   ```

2. **Preview changes** by viewing context:
   ```
   Grep(pattern="getUserData", output_mode="content", -n=true, -B=1, -A=1)
   ```

3. **Inform user of scope**: "Found 15 occurrences in 5 files"

4. **Replace in each file**:
   ```
   Edit(file_path="src/api.js", old_string="getUserData", new_string="fetchUserData", replace_all=true)
   Edit(file_path="src/utils.js", old_string="getUserData", new_string="fetchUserData", replace_all=true)
   # ... for each file
   ```

5. **Verify changes**: Re-run Grep to confirm all instances were replaced

6. **Suggest testing**: Recommend running tests to ensure refactoring didn't break functionality

### Example 2: Replace Deprecated Pattern

**User:** "Replace all `var` declarations with `let` or `const`"

**Workflow:**
1. **Find all var declarations**:
   ```
   Grep(pattern="\\bvar\\s+\\w+", output_mode="content", -n=true)
   ```

2. **Analyze each occurrence** to determine whether to use `let` or `const`:
   - Check if variable is reassigned → use `let`
   - Check if variable is constant → use `const`

3. **Replace systematically**:
   ```
   Edit(file_path="src/index.js", old_string="var count = 0", new_string="let count = 0", replace_all=false)
   Edit(file_path="src/index.js", old_string="var MAX_SIZE = 100", new_string="const MAX_SIZE = 100", replace_all=false)
   ```

4. **Use linter if available** to verify syntax:
   ```bash
   npm run lint
   ```

### Example 3: Update API Calls

**User:** "Update all authentication API calls to use the new endpoint"

**Workflow:**
1. **Find all API calls**:
   ```
   Grep(pattern="/api/auth/login", output_mode="content", -n=true)
   ```

2. **Identify variation patterns**:
   - Look for fetch calls, axios calls, or other HTTP methods
   - Check for different HTTP methods (GET, POST, etc.)

3. **Replace with updated endpoint**:
   ```
   Edit(
     file_path="src/auth.js",
     old_string="fetch('/api/auth/login', {",
     new_string="fetch('/api/v2/authentication/login', {",
     replace_all=true
   )
   ```

4. **Update any response handling** if API contract changed

5. **Recommend integration tests**

### Example 4: Convert Callbacks to Async/Await

**User:** "Refactor this file to use async/await instead of callbacks"

**Workflow:**
1. **Analyze callback patterns**:
   ```
   Grep(pattern="function\\s*\\([^)]*\\)\\s*{", output_mode="content", -n=true)
   ```

2. **Identify callback functions** (typically with `callback`, `cb`, or `done` parameters)

3. **Transform each function**:
   ```
   Edit(
     file_path="src/data.js",
     old_string="function loadData(callback) {\\n  db.query('SELECT *', callback);\\n}",
     new_string="async function loadData() {\\n  return await db.query('SELECT *');\\n}"
   )
   ```

4. **Update call sites** to use await:
   ```
   Edit(
     file_path="src/app.js",
     old_string="loadData((err, data) => {\\n  if (err) throw err;\\n  process(data);\\n});",
     new_string="const data = await loadData();\\nprocess(data);"
   )
   ```

5. **Add try-catch for error handling** where callbacks had error parameters

### Example 5: Standardize Import Paths

**User:** "Convert all relative imports to absolute imports"

**Workflow:**
1. **Find all relative imports**:
   ```
   Grep(pattern="from ['\"]\\.\\.?/", output_mode="content", -n=true)
   ```

2. **Calculate absolute path** for each import based on project structure

3. **Replace each import**:
   ```
   Edit(
     file_path="src/components/Button.jsx",
     old_string="import { theme } from '../../utils/theme'",
     new_string="import { theme } from '@/utils/theme'",
     replace_all=true
   )
   ```

4. **Verify module resolution** works with new paths

## Best Practices

### Planning Refactoring

Before executing refactoring:
1. **Understand scope**: Use Grep to find all affected locations
2. **Assess impact**: Review context of each occurrence
3. **Inform user**: Report how many files/instances will be changed
4. **Consider edge cases**: Look for string literals, comments, documentation

### Safe Refactoring Process

**The refactoring workflow should be:**
1. **Search** → Find all instances
2. **Analyze** → Verify each match is appropriate to change
3. **Inform** → Tell user the scope
4. **Execute** → Make the changes
5. **Verify** → Confirm changes were applied correctly
6. **Test** → Suggest running tests

### Handling Special Cases

**String literals and comments:**
- Ask user if they want to update strings/comments containing the identifier
- Usually rename in code only, not in user-facing strings

**Exported APIs:**
- Warn if renaming exported functions (breaking change for consumers)
- Suggest deprecation warnings or maintaining aliases

**Case sensitivity:**
- Be explicit about case-sensitive vs case-insensitive replacements
- Use `-i` flag in Grep for case-insensitive when appropriate

### Verification

After refactoring:
1. **Re-run Grep** to verify all instances were updated
2. **Check syntax**: Use linter or language-specific checker
3. **Read affected files**: Spot-check critical files
4. **Recommend testing**: Suggest running test suite

## Error Handling

### Common Issues and Solutions

**Issue:** "Replacement created syntax errors"
- **Solution:** Ensure old_string and new_string maintain proper syntax
- **Prevention:** Include sufficient context in old_string to ensure valid replacement points

**Issue:** "Not all instances were replaced"
- **Solution:** Check for variations in whitespace, quotes, or formatting
- **Alternative:** Use regex patterns in Grep to find variations, then handle each

**Issue:** "Replaced instances in comments/strings unintentionally"
- **Solution:** Be more specific with old_string context
- **Consider:** Use language-aware tools if available (parsers, AST tools)

**Issue:** "Replace broke tests"
- **Solution:** Review test files separately, update test expectations
- **Prevention:** Preview test file changes before applying

## Tool Usage Reference

### Edit Tool Parameters

**Required:**
- `file_path`: File to modify
- `old_string`: Exact string to find
- `new_string`: Replacement string

**Optional:**
- `replace_all`: Boolean (default: false)
  - `true`: Replace all occurrences in file
  - `false`: Replace only first occurrence (or fail if multiple matches)

**Important notes:**
- `old_string` must match EXACTLY (including whitespace, quotes)
- If multiple matches exist without `replace_all=true`, Edit will fail
- Use `replace_all=true` for bulk refactoring

### Grep for Refactoring

**Useful Grep options for refactoring:**
- `-n=true`: Show line numbers (helps locate changes)
- `-B=N`, `-A=N`: Show context (verify match is correct)
- `-i=true`: Case-insensitive (find variations)
- `output_mode="content"`: See actual code
- `output_mode="count"`: Count occurrences per file
- `type`: Filter by file type (e.g., `type="py"`)

## Integration with Other Tools

### Working with Claude's Native Tools

- **Grep**: Find patterns across codebase
- **Read**: Analyze files before refactoring
- **Edit**: Execute replacements (with replace_all)
- **Bash**: Run linters, formatters, tests after refactoring
- **Glob**: Find files by pattern for targeted refactoring

### Working with Other Skills

- **test-fixing**: Fix tests broken by refactoring
- **code-transfer**: Move refactored code to better locations
- **feature-planning**: Plan large-scale refactoring efforts

## Language-Specific Patterns

### JavaScript/TypeScript

**Common refactoring patterns:**
- `var` → `let`/`const`
- Callbacks → Promises/async-await
- require() → import statements
- CommonJS → ES modules
- Class components → Function components (React)

### Python

**Common refactoring patterns:**
- Old string formatting → f-strings
- `%` formatting → `.format()` or f-strings
- Dict access → `.get()` with defaults
- Type hints additions

### General

**Universal refactoring patterns:**
- Function/variable renaming
- API endpoint updates
- Library version migrations
- Naming convention standardization
- Import path updates
