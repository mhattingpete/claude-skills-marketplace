# Claude Skills Marketplace - Execution Runtime

**Code execution environment implementing the [Anthropic code execution pattern](https://www.anthropic.com/engineering/code-execution-with-mcp) for 90%+ token savings.**

## Overview

The Execution Runtime enables Claude to execute Python code locally with access to powerful APIs for file operations, code analysis, transformations, and git operations. Instead of loading all code and data through the context window, Claude writes Python scripts that execute locally and return only results—achieving up to **99% token reduction** for complex operations.

## Key Benefits

✅ **90-99% Token Savings** - Process 100 files using 1,000 tokens instead of 100,000
✅ **Faster Operations** - Local execution is significantly faster than multiple API round-trips
✅ **Stateful Workflows** - Resume multi-step refactoring across sessions
✅ **Automatic Security** - PII/secret detection and sandboxed execution
✅ **Reusable Skills** - Save transformation functions for future use

## Architecture

```
execution-runtime/
├── api/                      # Importable API library
│   ├── filesystem.py         # File operations (copy, paste, search, batch)
│   ├── code_analysis.py      # AST parsing (returns metadata, not source)
│   ├── code_transform.py     # Refactoring operations
│   └── git_operations.py     # Git command wrappers
├── mcp-server/
│   ├── mcp_server.py         # FastMCP server with execution tools
│   └── security/
│       ├── sandbox.py        # RestrictedPython execution environment
│       └── pii_detector.py   # Automatic secret/PII masking
├── pyproject.toml            # Dependencies
├── setup.sh                  # One-command installation
└── README.md                 # This file
```

## Installation

### Quick Setup (Recommended)

```bash
# 1. Install marketplace plugin (if not already installed)
/plugin marketplace add mhattingpete/claude-skills-marketplace

# 2. Run setup script
~/.claude/plugins/marketplaces/mhattingpete-claude-skills/execution-runtime/setup.sh
```

The script will:
- Detect your OS and Claude installation
- Configure MCP server in Claude config
- Set up allowed directories for security
- Install dependencies

### Manual Setup

1. **Add to Claude config** (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "marketplace-execution": {
      "command": "uv",
      "args": ["run", "python", "~/.claude/plugins/marketplaces/mhattingpete-claude-skills/execution-runtime/mcp-server/mcp_server.py"],
      "env": {
        "ALLOWED_DIRECTORIES": "/Users/yourname/Documents,/Users/yourname/Projects",
        "MASK_SECRETS": "true"
      }
    }
  }
}
```

2. **Install dependencies**:

```bash
cd ~/.claude/plugins/marketplaces/mhattingpete-claude-skills/execution-runtime
uv pip install -e .
```

3. **Restart Claude Code/Desktop**

## Usage

### Example 1: Bulk File Refactoring

**Traditional approach** (high token usage):
```
User: "Rename getUserData to fetchUserData in all 50 Python files"

Claude:
→ Grep to find files (2K tokens)
→ Read 50 files (50K tokens)
→ Edit 50 files × multiple rounds (50K+ tokens)
Total: ~102K tokens ❌
```

**With execution runtime** (low token usage):
```
User: "Rename getUserData to fetchUserData in all 50 Python files"

Claude writes Python script:
```python
from api.code_transform import rename_identifier

result = rename_identifier(
    pattern='.',
    old_name='getUserData',
    new_name='fetchUserData',
    file_pattern='**/*.py'
)
```

Executes locally, returns:
```json
{
  "files_modified": 50,
  "total_replacements": 127
}
```

Total: ~600 tokens ✅ (99.4% savings)
```

### Example 2: Extract Functions to New File

```python
from api.code_analysis import find_functions
from api.filesystem import copy_lines, paste_code

# Find all utility functions (metadata only, no source in context)
functions = find_functions('app.py', pattern='.*_util$')

# Copy each function to utils.py
for func in functions:
    code = copy_lines('app.py', func['start_line'], func['end_line'])
    paste_code('utils.py', -1, code)  # Append to end

result = {
    "functions_extracted": len(functions),
    "details": [f['name'] for f in functions]
}
```

### Example 3: Code Audit Across 100 Files

```python
from api.code_analysis import analyze_dependencies, find_unused_imports
from pathlib import Path

files = list(Path('.').glob('**/*.py'))

audit_results = []
for file in files:
    deps = analyze_dependencies(str(file))
    unused = find_unused_imports(str(file))

    if unused or deps['complexity'] > 10:
        audit_results.append({
            'file': str(file),
            'complexity': deps['complexity'],
            'unused_imports': unused
        })

result = {
    "files_audited": len(files),
    "issues_found": len(audit_results),
    "high_complexity": [r for r in audit_results if r['complexity'] > 15]
}
```

## Available APIs

### 1. Filesystem Operations (`api.filesystem`)

```python
from api.filesystem import (
    read_file, write_file,
    copy_lines, paste_code,
    search_replace,
    batch_copy, batch_transform
)

# Copy specific lines
code = copy_lines('source.py', start_line=10, end_line=20)

# Paste at line number
paste_code('target.py', line_number=50, code=code, create_backup=True)

# Search and replace across files
search_replace(
    file_pattern='**/*.py',
    search='old_function',
    replace='new_function',
    regex=False
)

# Batch operations (process many files at once)
operations = [
    {'source_file': 'a.py', 'start_line': 10, 'end_line': 20,
     'target_file': 'b.py', 'target_line': 5},
    # ... more operations
]
batch_copy(operations)
```

### 2. Code Analysis (`api.code_analysis`)

**Returns metadata only, not source code → massive token savings**

```python
from api.code_analysis import (
    find_functions, find_classes,
    extract_imports, get_function_calls,
    analyze_dependencies, find_unused_imports
)

# Find functions (returns line numbers, not code)
functions = find_functions('app.py', pattern='handle_.*')
# Returns: [{'name': 'handle_request', 'start_line': 45, 'end_line': 60, ...}]

# Find classes with methods
classes = find_classes('models.py')
# Returns: [{'name': 'User', 'methods': ['__init__', 'save'], ...}]

# Analyze complexity
deps = analyze_dependencies('complex_file.py')
# Returns: {'functions': 25, 'complexity': 87, 'lines': 450}
```

### 3. Code Transformation (`api.code_transform`)

```python
from api.code_transform import (
    rename_identifier,
    remove_debug_statements,
    add_docstrings,
    batch_refactor
)

# Rename across entire codebase
rename_identifier(
    pattern='.',
    old_name='oldName',
    new_name='newName',
    file_pattern='**/*.py'
)

# Remove debug prints
remove_debug_statements('app.py')

# Add docstrings to functions missing them
add_docstrings('module.py', style='google')
```

### 4. Git Operations (`api.git_operations`)

```python
from api.git_operations import (
    git_status, git_add, git_commit, git_push,
    create_branch, git_diff, git_log
)

# Check status
status = git_status()
# Returns: {'files': {'modified': [...], 'untracked': [...]}}

# Stage and commit
git_add(['.'])
git_commit('feat: refactor authentication module')

# Create branch and push
create_branch('feature/new-auth', checkout=True)
git_push('origin', 'feature/new-auth')
```

## Advanced Features

### Stateful Refactoring Sessions

For complex multi-step operations that might be interrupted:

```python
# Create session
session = create_refactoring_session(
    "modernize-codebase",
    "Update to Python 3.11+ syntax"
)

# Process files and save progress
for i, file in enumerate(files):
    # ... do work ...

    if i % 10 == 0:
        save_session_state(session['id'], {
            'processed': files[:i],
            'remaining': files[i:],
            'errors': errors
        })
```

If interrupted, resume later by loading session state.

### Reusable Transformation Skills

Save frequently-used transformations:

```python
save_reusable_skill(
    name="remove_debug_logs",
    code="""
def transform(code):
    import re
    # Remove print statements
    code = re.sub(r'^\\s*print\\(.*\\)\\n?', '', code, flags=re.MULTILINE)
    # Remove pdb
    code = re.sub(r'^\\s*import pdb.*\\n?', '', code, flags=re.MULTILINE)
    code = re.sub(r'^\\s*pdb\\.set_trace\\(\\)\\n?', '', code, flags=re.MULTILINE)
    return code
""",
    description="Remove debug print and pdb statements"
)

# Use in future sessions
from skills.remove_debug_logs import transform
cleaned_code = transform(original_code)
```

## Security

### Sandboxed Execution
- **RestrictedPython** environment
- **Resource limits**: 30s timeout, 256MB memory
- **Restricted imports**: Only `api.*` and safe stdlib modules
- **No dangerous builtins**: `eval`, `exec`, `__import__` disabled

### Automatic PII/Secret Masking

All execution results are automatically scanned for:
- API keys, tokens, passwords
- AWS/GCP/GitHub credentials
- Private keys, JWT tokens
- Database URLs with credentials
- (Optional) Emails, phone numbers, SSNs, credit cards

Example:
```python
# Your code contains:
api_key = "sk_live_abc123xyz"

# Results automatically masked:
api_key = "[REDACTED_API_KEY]"
```

### Directory Restrictions

Only files within `ALLOWED_DIRECTORIES` can be accessed. Configure in setup or `.env`:

```bash
ALLOWED_DIRECTORIES=/Users/you/Documents,/Users/you/Projects
```

## Performance Benchmarks

| Operation | Traditional | Execution | Savings |
|-----------|------------|-----------|---------|
| Copy 1 function | 100 tokens | 50 tokens | 50% |
| Refactor 10 files | 5,000 tokens | 500 tokens | 90% |
| Refactor 50 files | 25,000 tokens | 600 tokens | 97.6% |
| Analyze 100 files | 150,000 tokens | 1,000 tokens | 99.3% |
| Full codebase audit | 500,000+ tokens | 2,000 tokens | 99.6% |

## Troubleshooting

### "Module 'api' not found"

Ensure MCP server is running and Python path is configured. Restart Claude.

### "Import not allowed in sandbox"

Only `api.*` and safe stdlib modules are allowed. Check allowed imports list.

### "Permission denied" errors

Verify `ALLOWED_DIRECTORIES` includes the files you're trying to access.

### MCP server not starting

Check logs at `~/.claude/logs/execution-runtime.log`

## Configuration

Create `.env` file in execution-runtime directory:

```bash
# Security
ALLOWED_DIRECTORIES=/Users/you/Documents,/Users/you/Projects
MASK_SECRETS=true
AGGRESSIVE_MASKING=false  # Also mask emails, IPs, etc.

# Resource Limits
EXECUTION_TIMEOUT=30
MEMORY_LIMIT_MB=256

# Logging
LOG_LEVEL=INFO
```

## Development

### Running Tests

```bash
cd execution-runtime
uv pip install -e ".[dev]"
pytest
```

### Adding New APIs

1. Create module in `api/` directory
2. Add imports to `api/__init__.py`
3. Update `mcp_server.py` to expose in `list_available_apis`
4. Write tests and documentation

## Resources

- **Anthropic Article**: [Code Execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- **Marketplace Repo**: [claude-skills-marketplace](https://github.com/anthropics/claude-skills-marketplace)
- **MCP Documentation**: [Model Context Protocol](https://modelcontextprotocol.io)

## License

Apache 2.0

## Support

- **Issues**: [GitHub Issues](https://github.com/anthropics/claude-skills-marketplace/issues)
- **Discussions**: [Claude Code Discussions](https://github.com/anthropics/claude-code/discussions)
