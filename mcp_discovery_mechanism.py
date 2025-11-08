"""
MCP Dynamic Tool Discovery via Filesystem

This demonstrates HOW the LLM discovers tools dynamically instead of loading
all tool schemas upfront.

Key Insight from Anthropic's Article:
"Presenting tools as code on a filesystem allows models to read tool definitions
on-demand, rather than reading them all up-front."

Instead of:
  - Loading 50 tool schemas into context (50,000 tokens)

Do:
  - Provide a filesystem with Python modules
  - LLM reads only the files it needs (500 tokens per tool)
  - LLM imports and uses tools like regular code
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, List


# ============================================================================
# SCENARIO: Large MCP Ecosystem with 50+ Tools
# ============================================================================

"""
TRADITIONAL APPROACH:
---------------------
All tools loaded upfront into system prompt:

System: "You have access to these tools:
  1. filesystem_list_directory(path: str) -> List[Dict]
     Lists files in directory. Returns array of file objects...
     [500 tokens of documentation]

  2. filesystem_read_file(path: str) -> str
     Reads file contents. Parameters: path (required)...
     [500 tokens of documentation]

  3. database_query(sql: str) -> List[Dict]
     Executes SQL query. Returns result set...
     [500 tokens of documentation]

  ... [47 more tools, each 500 tokens]

  Total: 25,000 tokens just for tool definitions!
"

User: "List files in /tmp"
Assistant: Uses tool filesystem_list_directory
Result: [...]

COST: 25,000 tokens (all tools) + 100 tokens (call) = 25,100 tokens


THIN WRAPPER APPROACH:
----------------------
Tools available as Python modules on filesystem:

System: "You have Python execution. Tools available in /mcp_tools/
  Use 'ls /mcp_tools' to discover available tools.
  Import tools as needed: from mcp_tools import filesystem

  Total: ~100 tokens for system prompt
"

User: "List files in /tmp"
Assistant generates code:
  ```python
  # First, discover what filesystem tools exist
  import os
  tools = os.listdir('/mcp_tools')  # Sees: filesystem.py, database.py, ...

  # Read only the file I need
  from mcp_tools import filesystem  # Reads filesystem.py (~500 tokens)

  # Use the tool
  result = filesystem.list_directory('/tmp')
  print(result)
  ```

COST: 100 tokens (system) + 500 tokens (read filesystem.py) + 200 tokens (code)
     = 800 tokens

SAVINGS: 96% reduction (25,100 → 800 tokens)
"""


# ============================================================================
# IMPLEMENTATION: Filesystem-Based Discovery
# ============================================================================

class MCPFilesystemDiscovery:
    """
    Simulates how LLM discovers tools via filesystem instead of schemas.

    In practice, this would be a directory structure like:

    /mcp_tools/
    ├── __init__.py
    ├── filesystem.py       # FileSystem tools
    ├── database.py         # Database tools
    ├── api.py              # API tools
    ├── email.py            # Email tools
    ├── slack.py            # Slack tools
    └── ... (45 more tool modules)
    """

    def __init__(self, tools_directory: str = "/mcp_tools"):
        self.tools_dir = tools_directory

    def list_available_tools(self) -> List[str]:
        """
        LLM discovers tools by listing directory.

        This is like running: ls /mcp_tools/

        Returns only filenames, not full schemas!
        ~20 tokens instead of 25,000 tokens
        """
        return [
            "filesystem.py",
            "database.py",
            "api.py",
            "email.py",
            "slack.py",
            "github.py",
            "aws.py",
            "docker.py",
            "kubernetes.py",
            "analytics.py",
            # ... 40 more tools
        ]

    def read_tool_module(self, tool_name: str) -> str:
        """
        LLM reads a specific tool file ON-DEMAND.

        This is like running: cat /mcp_tools/filesystem.py

        Only reads what's needed (~500 tokens) instead of all tools (25,000 tokens)
        """
        # In real implementation, would read actual file
        # For demo, return mock content

        if tool_name == "filesystem.py":
            return '''
"""Filesystem MCP Tools"""

class FileSystem:
    """Tools for filesystem operations."""

    def list_directory(self, path: str) -> list:
        """List files in directory."""
        import os
        return [
            {"name": f, "size": os.path.getsize(os.path.join(path, f))}
            for f in os.listdir(path)
        ]

    def read_file(self, path: str) -> str:
        """Read file contents."""
        with open(path, 'r') as f:
            return f.read()

    def write_file(self, path: str, content: str) -> bool:
        """Write content to file."""
        with open(path, 'w') as f:
            f.write(content)
        return True
'''
        elif tool_name == "database.py":
            return '''
"""Database MCP Tools"""

class Database:
    """Tools for database operations."""

    def query(self, sql: str) -> list:
        """Execute SQL query."""
        # Implementation would connect to actual DB
        return []

    def insert(self, table: str, data: dict) -> int:
        """Insert row into table."""
        return 1
'''
        else:
            return f"# {tool_name} - Tool module"


# ============================================================================
# DEMONSTRATION: Traditional vs Thin Wrapper
# ============================================================================

def demo_traditional_approach():
    """
    Simulate traditional MCP approach - all tools loaded upfront.
    """
    print("=== TRADITIONAL APPROACH ===\n")

    # Step 1: Load ALL tool definitions into context
    all_tools = """
    Tool 1: filesystem_list_directory - Lists files... [500 tokens]
    Tool 2: filesystem_read_file - Reads files... [500 tokens]
    Tool 3: database_query - Queries database... [500 tokens]
    Tool 4: database_insert - Inserts data... [500 tokens]
    Tool 5: api_fetch - Fetches from API... [500 tokens]
    ... [45 more tools, 500 tokens each]
    """

    tokens_for_tools = 50 * 500  # 50 tools × 500 tokens each
    print(f"1. Load all tool definitions: {tokens_for_tools:,} tokens")

    # Step 2: User makes simple request
    print("2. User: 'List files in /tmp'")

    # Step 3: LLM selects and calls tool
    tokens_for_call = 100
    print(f"3. LLM calls filesystem_list_directory: {tokens_for_call} tokens")

    # Step 4: Result passed back through context
    tokens_for_result = 500
    print(f"4. Result passed to context: {tokens_for_result} tokens")

    total = tokens_for_tools + tokens_for_call + tokens_for_result
    print(f"\n📊 TOTAL: {total:,} tokens\n")

    return total


def demo_thin_wrapper_approach():
    """
    Simulate thin wrapper approach - tools discovered on-demand.
    """
    print("=== THIN WRAPPER APPROACH ===\n")

    discovery = MCPFilesystemDiscovery()

    # Step 1: Lightweight system prompt
    tokens_for_system = 100
    print(f"1. System prompt with filesystem info: {tokens_for_system} tokens")

    # Step 2: User makes request
    print("2. User: 'List files in /tmp'")

    # Step 3: LLM discovers available tools (lists directory)
    available_tools = discovery.list_available_tools()
    tokens_for_discovery = 20  # Just filenames
    print(f"3. LLM lists /mcp_tools/: {tokens_for_discovery} tokens")
    print(f"   Found: {', '.join(available_tools[:5])}...")

    # Step 4: LLM reads ONLY the tool it needs
    tool_content = discovery.read_tool_module("filesystem.py")
    tokens_for_tool = 500  # Just one tool file
    print(f"4. LLM reads filesystem.py: {tokens_for_tool} tokens")

    # Step 5: LLM generates code
    tokens_for_code = 200
    print("5. LLM generates Python code:")
    print("   ```python")
    print("   from mcp_tools import filesystem")
    print("   fs = filesystem.FileSystem()")
    print("   result = fs.list_directory('/tmp')")
    print("   ```")
    print(f"   Code: {tokens_for_code} tokens")

    # Step 6: Code executes - result stays in Python!
    tokens_for_result = 50  # Only summary returned
    print(f"6. Execute code, return summary: {tokens_for_result} tokens")

    total = (tokens_for_system + tokens_for_discovery +
             tokens_for_tool + tokens_for_code + tokens_for_result)
    print(f"\n📊 TOTAL: {total:,} tokens\n")

    return total


def demo_complex_workflow():
    """
    Demonstrate the power of thin wrappers for complex multi-tool workflows.
    """
    print("=== COMPLEX WORKFLOW: Analyze codebase, query DB, send Slack message ===\n")

    print("TRADITIONAL APPROACH:")
    print("  - Load 50 tools: 25,000 tokens")
    print("  - Call filesystem tool: +500 tokens (result)")
    print("  - Call database tool: +1,000 tokens (result)")
    print("  - Process results: +100 tokens")
    print("  - Call slack tool: +200 tokens")
    print("  - Total: ~27,000 tokens")
    print()

    print("THIN WRAPPER APPROACH:")
    print("  - System prompt: 100 tokens")
    print("  - Discover tools: 20 tokens")
    print("  - Read filesystem.py: 500 tokens")
    print("  - Read database.py: 500 tokens")
    print("  - Read slack.py: 500 tokens")
    print("  - Generate Python code:")
    print("    ```python")
    print("    from mcp_tools import filesystem, database, slack")
    print("    ")
    print("    # All intermediate results stay in Python!")
    print("    files = filesystem.FileSystem().list_directory('src/')")
    print("    python_files = [f for f in files if f['name'].endswith('.py')]")
    print("    ")
    print("    stats = database.Database().query('SELECT * FROM code_metrics')")
    print("    high_complexity = [s for s in stats if s['complexity'] > 10]")
    print("    ")
    print("    message = f'Found {len(high_complexity)} complex files'")
    print("    slack.Slack().send_message('#engineering', message)")
    print("    ")
    print("    # Return only summary")
    print("    print({'files': len(python_files), 'complex': len(high_complexity)})")
    print("    ```")
    print("  - Code generation: 300 tokens")
    print("  - Result summary: 50 tokens")
    print("  - Total: ~2,000 tokens")
    print()

    print("💰 SAVINGS: 92% reduction (27,000 → 2,000 tokens)")


# ============================================================================
# KEY INSIGHTS
# ============================================================================

def print_key_insights():
    """
    Summary of why filesystem-based discovery is revolutionary.
    """
    print("\n" + "="*70)
    print("KEY INSIGHTS: Why Thin Wrappers + Filesystem Discovery Works")
    print("="*70 + "\n")

    insights = [
        {
            "title": "1. On-Demand Loading",
            "traditional": "Load ALL 50 tool schemas upfront (25,000 tokens)",
            "thin_wrapper": "List directory (20 tokens), read only tools needed (500 each)",
            "benefit": "Only pay for what you use"
        },
        {
            "title": "2. Intermediate Results Stay Local",
            "traditional": "Every tool result passed through context window",
            "thin_wrapper": "Results stored in Python variables, only summary returned",
            "benefit": "Massive token savings on large datasets"
        },
        {
            "title": "3. Natural Code Patterns",
            "traditional": "LLM must learn special tool-calling syntax",
            "thin_wrapper": "LLM writes normal Python code with imports",
            "benefit": "Leverages existing coding knowledge"
        },
        {
            "title": "4. Composability",
            "traditional": "Each tool call is isolated, hard to chain",
            "thin_wrapper": "Normal Python - loops, variables, functions all work",
            "benefit": "Complex workflows in single execution"
        },
        {
            "title": "5. Data Filtering",
            "traditional": "Fetch 10,000 rows → send all to LLM",
            "thin_wrapper": "Fetch 10,000 rows → filter in Python → send summary",
            "benefit": "Process unlimited data with fixed token cost"
        }
    ]

    for insight in insights:
        print(f"{insight['title']}")
        print(f"  ❌ Traditional: {insight['traditional']}")
        print(f"  ✅ Thin Wrapper: {insight['thin_wrapper']}")
        print(f"  💡 Benefit: {insight['benefit']}\n")


# ============================================================================
# IMPLEMENTATION GUIDE
# ============================================================================

def print_implementation_guide():
    """
    How to implement this in your own projects.
    """
    print("\n" + "="*70)
    print("IMPLEMENTATION GUIDE")
    print("="*70 + "\n")

    print("Step 1: Create Tool Module Structure")
    print("  mkdir /mcp_tools")
    print("  touch /mcp_tools/__init__.py")
    print()

    print("Step 2: Create Thin Wrapper for Each MCP Tool")
    print("  # /mcp_tools/database.py")
    print("  class Database:")
    print("      def query(self, sql: str):")
    print("          # Calls actual MCP server")
    print("          return mcp_client.call('database.query', sql=sql)")
    print()

    print("Step 3: Update System Prompt")
    print("  System: 'You can execute Python code. MCP tools available in /mcp_tools/'")
    print("  System: 'Use os.listdir(\"/mcp_tools\") to discover tools'")
    print("  System: 'Import tools as needed: from mcp_tools import database'")
    print()

    print("Step 4: Provide Python Sandbox")
    print("  - Secure execution environment")
    print("  - Access to /mcp_tools directory")
    print("  - Return mechanism for results")
    print()

    print("Step 5: Let LLM Write Code")
    print("  User: 'Analyze database performance'")
    print("  LLM: Writes Python that imports tools, executes queries, analyzes")
    print()


# ============================================================================
# MAIN DEMO
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("MCP DYNAMIC TOOL DISCOVERY DEMONSTRATION")
    print("="*70 + "\n")

    # Compare approaches
    traditional_tokens = demo_traditional_approach()
    thin_wrapper_tokens = demo_thin_wrapper_approach()

    savings = ((traditional_tokens - thin_wrapper_tokens) / traditional_tokens) * 100
    print(f"💰 SAVINGS: {savings:.1f}% reduction")
    print(f"   ({traditional_tokens:,} → {thin_wrapper_tokens:,} tokens)\n")

    # Complex workflow
    demo_complex_workflow()

    # Insights
    print_key_insights()

    # Implementation guide
    print_implementation_guide()

    print("\n" + "="*70)
    print("CONCLUSION")
    print("="*70)
    print("""
Thin wrappers + filesystem discovery = Game changer for MCP

Instead of loading all tools upfront:
  ✅ Discover tools dynamically (ls /mcp_tools)
  ✅ Load only what you need (import specific tools)
  ✅ Keep intermediate results in code (Python variables)
  ✅ Return only final summary (aggregated results)

Result: 90-98% token reduction for complex workflows
""")
