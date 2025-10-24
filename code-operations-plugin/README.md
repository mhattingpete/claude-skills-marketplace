# Code Operations Skills Plugin

High-precision code manipulation operations including line-based insertion, bulk refactoring, and file analysis.

**Origin:** Converted from [code-copy-mcp](https://github.com/mhattingpete/code-copy-mcp) to native Claude Code skills for simpler setup and better integration.

## Why This Plugin?

The original MCP server provided precise file operations that complemented Claude's native tools. This plugin preserves that functionality while:

✅ **Simpler setup** - No MCP server needed, just install the plugin
✅ **Natural activation** - Skills detect intent automatically from user requests
✅ **Better integration** - Works seamlessly with other Claude Code skills
✅ **Version controlled** - Part of the skills marketplace ecosystem

## Skills Included

### 1. code-transfer

Transfer code between files with line-based precision.

**Activates when you say:**
- "copy this code to [file]"
- "move [function/class] to [file]"
- "extract this to a new file"
- "insert at line [number]"
- "transfer code from X to Y"

**What it does:**
- Extracts code from source files (functions, classes, code blocks)
- Inserts code at specific line numbers using `line_insert.py` script
- Moves code between files while maintaining structure
- Reorganizes code into separate modules

**Example:**
```
User: "Move the DatabaseConnection class from app.py to a new file database.py"

Claude:
1. Finds and extracts the DatabaseConnection class
2. Creates database.py with the extracted class
3. Updates imports in app.py
4. Removes the old class definition
✅ Code successfully transferred
```

**Key feature:** Includes `line_insert.py` Python script for precise line-number-based insertion (works where Edit tool's string matching isn't suitable).

---

### 2. code-refactor

Perform bulk code refactoring operations across files.

**Activates when you say:**
- "rename [identifier] to [new_name]"
- "replace all [pattern] with [replacement]"
- "refactor to use [new_pattern]"
- "update all calls to [function/API]"
- "convert [old_pattern] to [new_pattern]"

**What it does:**
- Renames variables/functions consistently across entire codebase
- Replaces deprecated patterns with modern alternatives
- Updates API calls when endpoints change
- Converts code patterns (callbacks → async/await, var → let/const)
- Standardizes code style across files

**Example:**
```
User: "Rename getUserData to fetchUserData everywhere"

Claude:
1. Searches codebase: Found 15 occurrences in 5 files
2. Previews changes with context
3. Replaces all instances using Edit with replace_all
4. Verifies all replacements completed
5. Suggests running tests
✅ Refactored 15 instances across 5 files
```

---

### 3. file-operations

Analyze files and get detailed metadata without modifying them.

**Activates when you say:**
- "analyze [file]"
- "get file info for [file]"
- "how many lines in [file]"
- "file statistics for [file]"
- "compare [file1] and [file2]"

**What it does:**
- Retrieves file size, modification time, permissions
- Counts lines, words, characters in files
- Analyzes code structure (functions, classes, imports)
- Compares file sizes across directories
- Generates code quality metrics

**Example:**
```
User: "Analyze app.py and tell me about it"

Claude:
app.py Analysis:
- Size: 15.2 KB
- Lines: 456
- Functions: 12
- Classes: 3
- Imports: 8 modules
- Last modified: 2025-10-20
- TODO comments: 3
✅ Analysis complete
```

## Integration Example

The skills work together for complete code manipulation workflows:

```
User: "Refactor utils.py - split it into separate utility modules by category"

Claude:
1. [file-operations] Analyzes utils.py structure
   - Found 45 functions across 3 categories
   - File size: 1,245 lines (too large)

2. [code-transfer] Extracts string utilities
   - Creates string_utils.py
   - Transfers 15 related functions

3. [code-transfer] Extracts file utilities
   - Creates file_utils.py
   - Transfers 18 related functions

4. [code-refactor] Updates all imports
   - Finds 23 files importing from utils.py
   - Updates to use specific utility modules

✅ Successfully refactored utils.py into focused modules
```

## Installation

### From Claude Code CLI

```bash
# Install from marketplace
claude plugins install code-operations-skills

# Or install from local directory
claude plugins install /path/to/code-operations-plugin
```

### Manual Installation

1. Copy `code-operations-plugin/` to `~/.claude/plugins/`
2. Restart Claude Code
3. Skills will activate automatically based on usage patterns

## Usage Tips

### When to Use code-transfer vs Edit

**Use code-transfer when:**
- Moving code between files
- Inserting at specific line numbers
- Creating new files from extracted code
- User specifies "line N"

**Use native Edit when:**
- Replacing existing code in-place
- Insertion point defined by content, not line number
- Simple find-and-replace

### Efficient Refactoring Workflow

1. **Search first** - Use Grep to understand scope
2. **Preview changes** - Show user what will be affected
3. **Execute systematically** - Make changes file by file
4. **Verify** - Re-search to confirm completion
5. **Test** - Suggest running test suite

### File Analysis Best Practices

- Combine multiple metrics for comprehensive analysis
- Use human-readable formats for user reporting
- Suggest optimizations when finding issues
- Compare against project baselines

## Dependencies

**Minimal - only Python stdlib:**
- Python 3.6+ (for `line_insert.py` script)
- No external packages required

## Comparison with Original MCP

| Feature | MCP Server | This Plugin |
|---------|-----------|-------------|
| Line-based insertion | ✅ copy_code tool | ✅ line_insert.py script |
| Bulk refactoring | ✅ search_and_replace | ✅ Edit + replace_all |
| File analysis | ✅ get_file_info | ✅ Bash + Grep + Read |
| Copy entire files | ✅ copy_entire_file | ✅ Read + Write |
| Setup complexity | MCP server config | Plugin install |
| Activation | Explicit tool calls | Natural language |
| Integration | Separate process | Native skills |

**What we kept:**
- Precise line-based insertion capability
- Safety features (backups, validation)
- Comprehensive file operations

**What we improved:**
- No server process needed
- Automatic skill activation
- Better integration with Claude Code ecosystem
- Leverages native tools where possible

## Technical Details

### line_insert.py Script

**Location:** `skills/code-transfer/scripts/line_insert.py`

**Purpose:** Insert code at specific line numbers (complements Edit tool's string matching)

**Features:**
- 1-based line numbering
- Automatic file creation if needed
- Optional timestamped backups
- Multi-line code support
- Basic path validation for security

**Usage:**
```bash
python3 line_insert.py <file_path> <line_number> <code> [--backup]
```

**Example:**
```bash
# Insert function at line 50
python3 line_insert.py src/utils.py 50 "def helper():\\n    pass"

# Insert with backup
python3 line_insert.py src/utils.py 50 "def helper():\\n    pass" --backup
```

### Skill Activation Logic

Skills activate based on natural language patterns in user requests:

**code-transfer triggers:**
- Keywords: "copy", "move", "extract", "transfer", "insert at line"
- Context: Mentions source and target files

**code-refactor triggers:**
- Keywords: "rename", "replace all", "refactor", "update all", "convert"
- Context: Bulk operations across files

**file-operations triggers:**
- Keywords: "analyze", "info", "statistics", "how many", "compare"
- Context: Non-destructive analysis requests

## Version

**1.0.0** - Initial release (converted from code-copy-mcp)

## Author

mhattingpete

## License

MIT (same as original MCP server)

## Contributing

Issues and PRs welcome at the [skills marketplace repository](https://github.com/anthropics/claude-skills-marketplace).

## Related Resources

- **Original MCP:** [code-copy-mcp](https://github.com/mhattingpete/code-copy-mcp)
- **Skills Marketplace:** [claude-skills-marketplace](https://github.com/anthropics/claude-skills-marketplace)
- **Claude Code Docs:** [docs.claude.com/claude-code](https://docs.claude.com/claude-code)
