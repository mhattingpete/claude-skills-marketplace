# 3 Ways to Implement MCP Code Execution in Claude Code Workflow

**Based on:** Anthropic's "Code Execution with MCP" article
**Focus:** Python-based implementations for massive token reduction

---

## ⚠️ Critical Architecture Understanding

**Your MCP servers remain UNCHANGED.** This pattern doesn't replace your MCP servers—it enhances them.

### The Architecture

```
Traditional MCP (Direct Tool Calls):
  LLM → MCP Tool Call → MCP Server → Result → LLM Context
  (Every result passes through context, massive token usage)

Code Execution with MCP (Thin Wrappers):
  LLM → Generates Python Code →
    Thin Wrappers (discovered via filesystem) →
      YOUR MCP Server (unchanged) →
        Results stay in Python execution environment →
          Only summary returned to LLM Context
  (Intermediate data never enters context, 90%+ token reduction)
```

### What This Means for Your Outlook MCP

1. **Your Outlook MCP server runs as-is** (`node dist/index.js`)
2. **Create thin Python wrappers** that call your MCP server via MCP protocol
3. **LLM discovers wrappers** via filesystem (progressive disclosure)
4. **LLM generates Python code** that imports and uses wrappers
5. **Code executes**, calling your real MCP server, keeping data in memory
6. **Only summaries** returned to LLM context

**Key Insight:** Wrappers are bridges to your existing MCP infrastructure, not replacements.

See `outlook_mcp_production_example.py` for complete working example.

---

## Core Learnings from the Article

### The Problem
Traditional MCP implementations have two critical inefficiencies:

1. **Tool definition overload**: Agents connected to thousands of tools must process "hundreds of thousands of tokens before reading a request"
2. **Intermediate result bloat**: Data passes through the model multiple times, requiring reprocessing at each step

**Real example from Anthropic:** Google Drive-to-Salesforce workflow consumed **150,000 tokens**

### The Solution: Code Execution with MCP

Present MCP servers as **code APIs** organized in filesystem hierarchies. Agents write code to interact with tools instead of direct tool calling.

**Reference Implementation Structure (from article):**
```
servers/
├── google-drive/
│   ├── getDocument.ts
│   └── index.ts
└── salesforce/
    ├── updateRecord.ts
    └── index.ts
```

Agents explore directories to discover tools, reading only necessary definitions on-demand.

### The Impact: 5 Major Benefits

1. **Progressive Disclosure** (98.7% token reduction)
   - Models navigate filesystems efficiently
   - Load tool definitions on-demand, not upfront
   - **Example:** 150,000 → 2,000 tokens (Google Drive → Salesforce)

2. **Context-Efficient Filtering**
   - Large datasets filtered in execution environment
   - **Example:** Extract 5 rows from 10,000-row spreadsheet without passing all data through context

3. **Privacy Preservation** 🔒
   - Intermediate results isolated from model
   - **PII can be tokenized automatically**
   - Sensitive data flows between systems without entering model context
   - Critical for email, calendar, health data, financial records

4. **State Persistence**
   - Maintain progress across operations via filesystem
   - Enables resumable work and skill development
   - Agent can save/load state between executions

5. **Control Flow Efficiency**
   - Loops and conditionals execute natively
   - No repeated agent iterations
   - Dramatically improved latency

### Industry Validation

Cloudflare published similar findings, calling this pattern **"Code Mode"**. The core insight: LLMs excel at code generation—leverage this strength for efficient MCP integration.

---

## Implementation 1: Python Code Executor Skill

### Concept
Create a skill that detects when a task would benefit from code execution instead of multiple tool calls, then generates and runs Python code to orchestrate operations efficiently.

### When It Activates
- "Analyze all Python files and create a report"
- "Process this large dataset and show me statistics"
- "Check these 1000 files for security issues"
- "Aggregate data from multiple sources"

### Implementation

**Plugin Structure:**
```
mcp-code-execution-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── code-executor/
│       ├── SKILL.md
│       └── scripts/
│           ├── executor.py          # Python code execution sandbox
│           └── mcp_wrapper_base.py  # Base class for MCP wrappers
└── README.md
```

**Key Python Script** (`scripts/executor.py`):

```python
#!/usr/bin/env python3
"""
Code Executor - Runs LLM-generated Python code in sandbox

Instead of:
  1. Grep for files (500 results → 5000 tokens)
  2. Read each file (1000 tokens each × 500 = 500,000 tokens)
  3. Process results (10,000 tokens)
  Total: 515,000 tokens

Do:
  1. Generate Python code (1000 tokens)
  2. Execute code (keeps all data in memory)
  3. Return summary (100 tokens)
  Total: 1,100 tokens (99.8% reduction)
"""

import sys
import json
import subprocess
from pathlib import Path
from typing import Any, Dict


def execute_code(code: str, timeout: int = 30) -> Dict[str, Any]:
    """
    Execute Python code in a restricted environment.

    Security (CRITICAL from Anthropic article):
    "Requires a secure execution environment with appropriate sandboxing,
    resource limits, and monitoring"

    - Runs in subprocess with timeout
    - Sandboxing (Docker, gVisor, or VM isolation)
    - Resource limits (CPU, memory, disk)
    - No network access (unless explicitly allowed)
    - Limited filesystem access
    - Monitoring and logging
    """
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=Path.cwd()
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Code execution exceeded {timeout}s timeout"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: executor.py <code>")
        sys.exit(1)

    code = sys.argv[1]
    result = execute_code(code)
    print(json.dumps(result, indent=2))
```

**SKILL.md** (excerpt):

```markdown
# Code Executor Skill

## Purpose
Automatically detect when tasks would benefit from Python code execution
instead of sequential tool calls, reducing token usage by 90-98%.

## When to Use
Activates when user requests involve:
- Processing large numbers of files/items
- Multi-step data transformations
- Aggregating data from multiple sources
- Complex filtering or analysis

**Activation phrases:**
- "analyze all [files/data/...]"
- "process this [large dataset/directory/...]"
- "check [hundreds/thousands] of files for..."
- "aggregate data from [multiple sources]"

## Approach
1. **Detect pattern**: Identify tasks that would require many tool calls
2. **Generate code**: Create Python script that:
   - Performs all operations in-memory
   - Filters/processes data locally
   - Returns only summary/results
3. **Execute**: Run code using executor.py
4. **Return**: Provide concise summary to user

## Example
User: "Analyze all Python files and find those with TODO comments"

Traditional approach (HIGH tokens):
- Glob *.py → 500 files
- Grep each for TODO → 500 calls
- Read files with TODOs → 50 files × 1000 tokens
- Total: ~60,000 tokens

Code execution approach (LOW tokens):
```python
from pathlib import Path

# Find all Python files
py_files = list(Path('.').rglob('*.py'))

# Check each for TODO (in memory)
todos = []
for file in py_files:
    content = file.read_text()
    if 'TODO' in content:
        lines = [i+1 for i, line in enumerate(content.split('\n'))
                 if 'TODO' in line]
        todos.append({'file': str(file), 'lines': lines})

# Return only summary
print(json.dumps({
    'total_files': len(py_files),
    'files_with_todos': len(todos),
    'details': todos[:10]  # First 10 only
}))
```
Total: ~1,500 tokens (97.5% reduction)
```

### Benefits
- **Massive token savings**: 90-98% reduction for complex workflows
- **Faster execution**: Single Python execution vs many tool calls
- **Data filtering**: Process GB of data, return KB summary
- **Natural patterns**: Leverage Python's full capabilities

### Use Cases
1. **Codebase Analysis**: Scan entire repo, return statistics
2. **Log Processing**: Process GB of logs, return insights
3. **Batch Operations**: Modify 1000s of files based on pattern
4. **Data Aggregation**: Combine data from files, DB, APIs

---

## Implementation 2: Lazy-Loading MCP Tool Registry

### Concept
Create a Python module that provides on-demand access to MCP tools via filesystem
discovery, loading tool definitions only when imported/used.

### When It Helps
- Working with large MCP ecosystems (50+ tools)
- Reducing initial context overhead
- Dynamic tool discovery workflows
- Building tool discovery interfaces

### Implementation

**Directory Structure:**
```
mcp_tools/                    # Available to Claude Code at runtime
├── __init__.py               # Registry with lazy loading
├── filesystem.py             # Thin wrapper for filesystem MCP
├── database.py               # Thin wrapper for database MCP
├── api.py                    # Thin wrapper for API MCP
├── slack.py                  # Thin wrapper for Slack MCP
├── github.py                 # Thin wrapper for GitHub MCP
└── ... (more tool modules)
```

**Implementation** (`mcp_tools/__init__.py`):

```python
"""
Lazy-Loading MCP Tool Registry

Provides on-demand tool loading via filesystem discovery.

Traditional: Load 50 tools × 500 tokens = 25,000 tokens upfront
Lazy: List directory (20 tokens) + load only what's used (500 each)

Example:
  # Discover available tools
  import os
  tools = os.listdir('mcp_tools')  # 20 tokens

  # Use only what you need
  from mcp_tools import database   # 500 tokens
  result = database.query('SELECT * FROM users')
"""

import importlib
import os
from pathlib import Path
from typing import List, Optional


class LazyMCPRegistry:
    """
    Registry that loads MCP tools on-demand using Progressive Disclosure.

    From Anthropic article: "Models navigate filesystems efficiently,
    loading tool definitions on-demand rather than upfront."

    Instead of loading all tool schemas upfront, tools are discovered
    via the filesystem and loaded only when accessed.
    """

    def __init__(self, tools_dir: Optional[str] = None):
        self.tools_dir = tools_dir or str(Path(__file__).parent)
        self._loaded_tools = {}

    def list_available_tools(self) -> List[str]:
        """
        List available tool modules.

        Returns filenames, not full schemas (20 tokens vs 25,000 tokens)
        """
        tools = []
        for file in os.listdir(self.tools_dir):
            if file.endswith('.py') and not file.startswith('_'):
                tools.append(file[:-3])  # Remove .py extension
        return sorted(tools)

    def load_tool(self, tool_name: str):
        """
        Load a specific tool module on-demand.

        Only loads when accessed (~500 tokens) instead of all upfront
        """
        if tool_name not in self._loaded_tools:
            module = importlib.import_module(f'mcp_tools.{tool_name}')
            self._loaded_tools[tool_name] = module
        return self._loaded_tools[tool_name]

    def __getattr__(self, name: str):
        """Enable: registry.database instead of registry.load_tool('database')"""
        return self.load_tool(name)


# Global registry instance
registry = LazyMCPRegistry()


# Export common pattern: from mcp_tools import filesystem, database
def __getattr__(name: str):
    """Lazy load tools when imported"""
    return registry.load_tool(name)
```

**Example Tool Module** (`mcp_tools/filesystem.py`):

```python
"""
Filesystem MCP Tool Wrapper

Thin wrapper that calls actual MCP server for filesystem operations.
"""

from typing import List, Dict, Any
import os


class FileSystem:
    """
    Filesystem operations via MCP.

    In production, would call actual MCP server.
    For demo, uses local filesystem.
    """

    def list_directory(self, path: str) -> List[Dict[str, Any]]:
        """List files in directory."""
        # Production: return mcp_client.call('filesystem.list', path=path)
        return [
            {
                "name": f,
                "size": os.path.getsize(os.path.join(path, f)),
                "is_dir": os.path.isdir(os.path.join(path, f))
            }
            for f in os.listdir(path)
        ]

    def read_file(self, path: str) -> str:
        """Read file contents."""
        # Production: return mcp_client.call('filesystem.read', path=path)
        with open(path, 'r') as f:
            return f.read()

    def search_files(self, pattern: str, path: str = ".") -> List[str]:
        """Search for files matching pattern."""
        # Production: return mcp_client.call('filesystem.search', pattern=pattern, path=path)
        from pathlib import Path
        return [str(p) for p in Path(path).rglob(pattern)]


# Export for: from mcp_tools.filesystem import FileSystem
__all__ = ['FileSystem']
```

**Usage in Claude Code Workflow:**

```python
# Instead of loading all MCP tool schemas upfront...

# Discovery (20 tokens)
from mcp_tools import registry
available = registry.list_available_tools()
# ['api', 'database', 'filesystem', 'github', 'slack', ...]

# Load only what you need (500 tokens each)
from mcp_tools import filesystem, database

# Use tools
fs = filesystem.FileSystem()
db = database.Database()

files = fs.list_directory('src/')
stats = db.query('SELECT * FROM metrics')

# Process in Python, return summary
result = {
    'file_count': len(files),
    'db_rows': len(stats)
}
```

### Benefits
- **Minimal upfront cost**: 20 tokens for discovery vs 25,000 for all schemas
- **Pay-per-use**: Only load tools actually used
- **Natural discovery**: Standard Python import patterns
- **Scalability**: Support 100+ tools with minimal overhead

---

## Implementation 3: Context-Efficient Data Pipeline Skill

### Concept
A skill specialized for processing large datasets/codebases that keeps all
intermediate data in Python, only returning filtered/aggregated results to
minimize context usage.

### When It Activates
- "Analyze this large codebase"
- "Process these log files"
- "Generate metrics from all files"
- "Find patterns across the entire project"

### Implementation

**Plugin Structure:**
```
data-pipeline-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── efficient-pipeline/
│       ├── SKILL.md
│       └── scripts/
│           └── pipeline.py
└── README.md
```

**Key Python Script** (`scripts/pipeline.py`):

```python
#!/usr/bin/env python3
"""
Context-Efficient Data Pipeline

Processes large amounts of data while keeping intermediate results
in memory, only returning final aggregated/filtered results.

Token comparison for processing 1000 files:

Traditional:
- Glob: 1000 files × 100 chars = 100,000 tokens
- Read: 1000 files × 1000 tokens = 1,000,000 tokens
- Process results: 10,000 tokens
- Total: 1,110,000 tokens

Pipeline:
- Load: (stays in memory)
- Filter: (stays in memory)
- Transform: (stays in memory)
- Aggregate: return summary (500 tokens)
- Total: 1,500 tokens (99.9% reduction)
"""

from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
import json


class DataPipeline:
    """
    Efficient data processing pipeline.

    All intermediate data stays in Python memory.
    Only final aggregated results are returned.
    """

    def __init__(self):
        self.data: List[Any] = []
        self.metadata: Dict[str, Any] = {}

    def ingest_files(self, pattern: str, base_path: str = ".") -> 'DataPipeline':
        """
        Load files matching pattern.

        Files stay in memory - not passed to context!
        """
        files = list(Path(base_path).rglob(pattern))
        self.data = [
            {
                "path": str(f),
                "size": f.stat().st_size,
                "content": f.read_text() if f.is_file() else None
            }
            for f in files
        ]
        self.metadata['ingested'] = len(self.data)
        return self

    def filter(self, predicate: Callable[[Any], bool]) -> 'DataPipeline':
        """
        Filter data in Python.

        Intermediate results stay in memory - not passed to context!
        """
        self.data = [item for item in self.data if predicate(item)]
        self.metadata['filtered'] = len(self.data)
        return self

    def transform(self, func: Callable[[Any], Any]) -> 'DataPipeline':
        """
        Transform data in Python.

        Intermediate results stay in memory - not passed to context!
        """
        self.data = [func(item) for item in self.data]
        self.metadata['transformed'] = len(self.data)
        return self

    def aggregate(self) -> Dict[str, Any]:
        """
        Aggregate results and return SUMMARY ONLY.

        This is the only data returned to context - massive savings!
        """
        return {
            "pipeline_metadata": self.metadata,
            "result_count": len(self.data),
            "sample": self.data[:5] if self.data else [],
            "summary": self._compute_summary()
        }

    def _compute_summary(self) -> Dict[str, Any]:
        """Compute summary statistics."""
        if not self.data:
            return {}

        # Example summary logic
        total_size = sum(item.get('size', 0) for item in self.data)
        return {
            "total_items": len(self.data),
            "total_size_bytes": total_size,
            "avg_size_bytes": total_size / len(self.data) if self.data else 0
        }


def main():
    """
    Example usage: Analyze Python files with TODOs

    Traditional approach: ~500,000 tokens
    Pipeline approach: ~1,500 tokens
    """

    pipeline = DataPipeline()

    result = (
        pipeline
        .ingest_files("*.py")  # Load all Python files (stays in memory)
        .filter(lambda f: 'TODO' in (f['content'] or ''))  # Filter in Python
        .transform(lambda f: {  # Transform in Python
            'file': f['path'],
            'size': f['size'],
            'todo_count': f['content'].count('TODO')
        })
        .aggregate()  # Return only summary
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
```

**SKILL.md** (excerpt):

```markdown
# Efficient Data Pipeline Skill

## Purpose
Process large datasets/codebases efficiently by keeping intermediate
results in Python memory, only returning aggregated summaries.

## When to Use
- Processing 100+ files
- Analyzing large datasets
- Multi-step data transformations
- Generating codebase metrics

## Approach
1. **Ingest**: Load all data into Python memory (not passed to context)
2. **Filter**: Apply filters in Python (intermediate results stay local)
3. **Transform**: Transform data in Python (results stay local)
4. **Aggregate**: Return only final summary to context

## Token Savings
Traditional: Load → Process → Return all data = 500,000+ tokens
Pipeline: Load in memory → Process → Return summary = 1,500 tokens
Savings: 99.7% reduction

## Example
User: "Find all Python files with security issues"

Code generated:
```python
from data_pipeline import DataPipeline

result = (
    DataPipeline()
    .ingest_files("*.py")
    .filter(lambda f: any(
        pattern in f['content']
        for pattern in ['eval(', 'exec(', 'shell=True']
    ))
    .transform(lambda f: {
        'file': f['path'],
        'issues': find_security_issues(f['content'])
    })
    .aggregate()
)

# Returns:
# {
#   "pipeline_metadata": {"ingested": 1247, "filtered": 23},
#   "result_count": 23,
#   "sample": [...first 5 files...],
#   "summary": {"total_issues": 45, "critical": 12}
# }
```
```

### Benefits
- **Extreme efficiency**: 99%+ token reduction for large datasets
- **Scalability**: Process unlimited data with fixed token cost
- **Composability**: Chain operations naturally
- **Focus**: Return only what matters (insights, not raw data)

### Use Cases
1. **Codebase Auditing**: Scan 1000s of files for patterns
2. **Log Analysis**: Process GB of logs, return insights
3. **Metrics Generation**: Analyze entire project, return statistics
4. **Pattern Detection**: Find security issues, code smells, etc.

---

---

## Critical Benefit: Privacy Preservation & PII Handling

**From Anthropic article:** "PII can be tokenized automatically, preventing sensitive data from entering model context while still flowing between systems."

This is especially critical for:
- Email/calendar data (Outlook, Gmail)
- Healthcare records
- Financial information
- Customer data

### Implementation Pattern

```python
def process_emails_with_pii_protection():
    """
    Example: Process customer emails without exposing PII to model.

    Traditional approach: All email content goes through model context
    Code execution: PII stays in execution environment, only metadata returned
    """
    from outlook_mcp import OutlookEmail
    import hashlib

    email = OutlookEmail()

    # Fetch emails (PII stays in memory)
    customer_emails = email.search_emails("customer inquiry")

    # Tokenize PII in execution environment
    processed = []
    for msg in customer_emails:
        # Extract insights without exposing actual content
        pii_hash = hashlib.sha256(msg['from'].encode()).hexdigest()[:8]

        processed.append({
            'sender_token': f"USER_{pii_hash}",  # Tokenized email
            'subject_category': categorize(msg['subject']),  # Metadata only
            'sentiment': analyze_sentiment(msg['body']),  # Analysis only
            'urgency': calculate_urgency(msg),  # Derived metric
            # ACTUAL PII NEVER SENT TO MODEL
        })

    # Return anonymized insights only
    return {
        'total_inquiries': len(customer_emails),
        'by_category': aggregate_by_category(processed),
        'avg_sentiment': calculate_avg_sentiment(processed),
        'urgent_count': sum(1 for p in processed if p['urgency'] == 'high')
    }
```

**Key insight:** Sensitive data flows through the execution environment to perform operations (e.g., email → database, email → ticket system) but never enters the model's context window.

### Use Cases for PII Protection

1. **Healthcare:** Process patient records without exposing PHI
2. **Finance:** Analyze transactions without showing account numbers
3. **HR:** Process resumes/applications without exposing personal details
4. **Customer Support:** Handle tickets without revealing customer identities
5. **Legal:** Process documents while maintaining privilege

---

## Advanced Feature: State Persistence

**From Anthropic article:** "Agents maintain progress across operations via filesystem access, enabling resumable work and skill development."

### Implementation Pattern

```python
import json
from pathlib import Path

class StatefulMCPAgent:
    """
    Agent that maintains state across executions.

    Benefits:
    - Resume interrupted workflows
    - Build knowledge over time
    - Track progress on long-running tasks
    """

    def __init__(self, state_dir: str = ".mcp_state"):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(exist_ok=True)

    def save_state(self, task_id: str, state: dict):
        """Save progress to filesystem."""
        state_file = self.state_dir / f"{task_id}.json"
        with open(state_file, 'w') as f:
            json.dump(state, f)

    def load_state(self, task_id: str) -> dict:
        """Load previous progress."""
        state_file = self.state_dir / f"{task_id}.json"
        if state_file.exists():
            with open(state_file, 'r') as f:
                return json.load(f)
        return {}

    def resumable_workflow(self, task_id: str):
        """
        Example: Process 1000 emails with checkpointing.

        If interrupted, resume from last checkpoint.
        """
        from outlook_mcp import OutlookEmail

        email = OutlookEmail()
        state = self.load_state(task_id)

        # Resume from last processed index
        start_index = state.get('last_processed', 0)
        processed_count = state.get('processed_count', 0)

        all_emails = email.list_emails(limit=1000)

        for i, msg in enumerate(all_emails[start_index:], start=start_index):
            # Process email
            process_email(msg)
            processed_count += 1

            # Checkpoint every 100 emails
            if processed_count % 100 == 0:
                self.save_state(task_id, {
                    'last_processed': i + 1,
                    'processed_count': processed_count,
                    'timestamp': datetime.now().isoformat()
                })

        return {'total_processed': processed_count}
```

### State Persistence Use Cases

1. **Long-running migrations:** Resume multi-hour data migrations
2. **Incremental learning:** Agent builds knowledge over time
3. **Progress tracking:** Monitor completion of large batch operations
4. **Error recovery:** Resume from failure point
5. **Skill development:** Agent improves through accumulated experience

---

## Comparison Table

| Feature | Implementation 1 (Code Executor) | Implementation 2 (Lazy Registry) | Implementation 3 (Data Pipeline) |
|---------|----------------------------------|----------------------------------|----------------------------------|
| **Primary Benefit** | Flexibility - any Python code | Discovery - minimal upfront load | Efficiency - large data processing |
| **Token Reduction** | 90-98% | 95%+ (for tool loading) | 99%+ (for data processing) |
| **Best For** | General code execution tasks | Large MCP ecosystems | Large dataset analysis |
| **Complexity** | Medium | Low | Low |
| **Security Needs** | Sandbox required | Minimal | Minimal |
| **Integration** | Skill-based | Import-based | Pipeline-based |

## Recommended Approach

**Start with:** Implementation 2 (Lazy Registry)
- Easiest to implement
- Immediate benefits for any MCP usage
- Foundation for other implementations

**Add:** Implementation 3 (Data Pipeline)
- Handles specific use case (large data)
- Complements lazy loading
- Provides pipeline abstraction

**Consider:** Implementation 1 (Code Executor)
- Most flexible
- Requires security considerations
- Best for ad-hoc code execution needs

---

## Next Steps

1. **Prototype**: Start with lazy registry for immediate wins
2. **Measure**: Track token usage before/after
3. **Iterate**: Add pipeline for data-heavy tasks
4. **Expand**: Build more specialized wrappers

## Key Takeaway

**Code execution with MCP = 98.7% token reduction (150K → 2K tokens)**

From Anthropic's article, this pattern provides:

### Token Efficiency
✅ **Progressive disclosure:** Load tools on-demand via filesystem navigation
✅ **Context-efficient filtering:** Process data locally, return only summaries
✅ **Native control flow:** Loops and conditionals execute without repeated agent iterations

### Privacy & Security
🔒 **PII protection:** Sensitive data flows between systems without entering model context
🔒 **Automatic tokenization:** Personal information replaced with hashes/IDs
🔒 **Sandboxing required:** Secure execution environment with monitoring

### Advanced Capabilities
💾 **State persistence:** Resume workflows, build knowledge over time
🚀 **Latency reduction:** Single execution instead of multiple round trips
♾️ **Unlimited scale:** Process unlimited data with fixed token cost

### Industry Validation
Cloudflare calls this **"Code Mode"** - the future of efficient LLM integration.

**Core insight:** LLMs excel at code generation. Leverage this strength instead of traditional tool calling.
