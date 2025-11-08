"""
Thin MCP Wrapper Example - Dynamic Tool Discovery

This demonstrates the "code execution with MCP" pattern from Anthropic's article.
Instead of loading all tools upfront, tools are discovered dynamically via imports.

Key Benefits:
- Tools discovered on-demand (read .py file instead of loading all schemas)
- Intermediate results stay in Python (no context passing)
- Token usage: 150K → 2K (98% reduction)
- LLM writes code instead of making tool calls
"""

from typing import Any, Dict, List, Optional
import json


# ============================================================================
# THIN WRAPPERS - These expose MCP tools as Python functions
# ============================================================================

class FileSystemTools:
    """
    Thin wrapper for filesystem MCP tools.

    The LLM can:
    1. Read this file to discover available tools
    2. Import: from mcp_tools import FileSystemTools
    3. Use: fs = FileSystemTools(); files = fs.list_directory("/path")

    Notice: No heavy schemas loaded upfront - just Python function signatures!
    """

    def list_directory(self, path: str) -> List[Dict[str, Any]]:
        """
        List files in a directory.

        Args:
            path: Directory path to list

        Returns:
            List of file info dicts with: name, size, modified, is_dir
        """
        # In real implementation, this calls the MCP server
        # For demo purposes, mock implementation
        return [
            {"name": "file1.py", "size": 1024, "is_dir": False},
            {"name": "dir1", "size": 4096, "is_dir": True},
        ]

    def read_file(self, path: str, encoding: str = "utf-8") -> str:
        """Read file contents."""
        # Mock implementation
        return f"Contents of {path}"

    def write_file(self, path: str, content: str) -> bool:
        """Write content to file."""
        # Mock implementation
        return True

    def search_files(self, pattern: str, path: str = ".") -> List[str]:
        """Search for files matching pattern."""
        # Mock implementation
        return [f"match1_{pattern}.py", f"match2_{pattern}.py"]


class DatabaseTools:
    """Thin wrapper for database MCP tools."""

    def query(self, sql: str) -> List[Dict[str, Any]]:
        """Execute SQL query and return results."""
        # Mock implementation
        return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """Insert row and return ID."""
        # Mock implementation
        return 123

    def get_schema(self, table: str) -> Dict[str, str]:
        """Get table schema."""
        # Mock implementation
        return {"id": "INTEGER", "name": "TEXT"}


class APITools:
    """Thin wrapper for external API MCP tools."""

    def fetch(self, url: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Fetch data from API endpoint."""
        # Mock implementation
        return {"status": "success", "data": []}

    def post(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """POST data to API endpoint."""
        # Mock implementation
        return {"status": "created", "id": 456}


# ============================================================================
# USAGE EXAMPLE - How LLM uses thin wrappers
# ============================================================================

def example_traditional_approach():
    """
    TRADITIONAL MCP APPROACH (HIGH TOKEN USAGE):

    1. Load all tools upfront (FileSystemTools, DatabaseTools, APITools)
    2. Pass full schemas to LLM (thousands of tokens)
    3. LLM calls tool: list_directory
    4. Result passed back through context (hundreds of tokens)
    5. LLM calls tool: read_file
    6. Result passed back through context
    7. LLM calls tool: database.query
    8. Result passed back through context
    9. LLM calls tool: api.fetch
    10. Final result

    Total: 150,000+ tokens for complex workflow
    """
    pass


def example_thin_wrapper_approach():
    """
    THIN WRAPPER APPROACH (LOW TOKEN USAGE):

    User: "Analyze all Python files, check which ones are in the database,
           and sync missing ones via API"

    LLM generates THIS CODE (all in one execution):
    """
    # Step 1: Discover tools by importing (reads .py file, ~500 tokens)
    # In real usage: from mcp_tools import FileSystemTools, DatabaseTools, APITools
    # For demo, use the classes defined above

    # Step 2: Execute entire workflow in Python sandbox
    fs = FileSystemTools()
    db = DatabaseTools()
    api = APITools()

    # All intermediate results stay IN PYTHON (not passed to context)
    python_files = fs.search_files("*.py")  # 500 files - stays in variable

    # Process in Python - no context passing
    db_files = db.query("SELECT filename FROM tracked_files")
    db_filenames = {row.get("name", "") for row in db_files}  # stays in memory

    missing = [f for f in python_files if f not in db_filenames]  # in memory

    # Sync missing files
    synced = []
    for file in missing:
        content = fs.read_file(file)  # stays in memory
        result = api.post("/sync", {"file": file, "content": content})
        synced.append(result["id"])

    # Step 3: Only return FINAL RESULT to LLM (50 tokens)
    return {
        "total_files": len(python_files),
        "already_tracked": len(db_filenames),
        "newly_synced": len(synced),
        "sync_ids": synced
    }

    """
    Total: ~2,000 tokens (500 for tool discovery + 1500 for code + 50 for result)
    Savings: 98% reduction (150K → 2K)
    """


# ============================================================================
# DYNAMIC DISCOVERY MECHANISM
# ============================================================================

class MCPToolRegistry:
    """
    Registry that enables dynamic tool discovery.

    Instead of loading all tools upfront, tools are discovered when:
    1. LLM reads this module file
    2. LLM sees available tool classes
    3. LLM imports only what it needs
    """

    @staticmethod
    def list_available_tools() -> Dict[str, List[str]]:
        """
        List all available tool categories and their methods.

        This is what LLM would read to discover tools dynamically.
        Much lighter than loading full schemas!
        """
        return {
            "FileSystemTools": [
                "list_directory(path: str)",
                "read_file(path: str)",
                "write_file(path: str, content: str)",
                "search_files(pattern: str)",
            ],
            "DatabaseTools": [
                "query(sql: str)",
                "insert(table: str, data: dict)",
                "get_schema(table: str)",
            ],
            "APITools": [
                "fetch(url: str, params: dict)",
                "post(url: str, data: dict)",
            ]
        }

    @staticmethod
    def get_tool_docs(tool_name: str) -> str:
        """
        Get documentation for a specific tool (on-demand).

        Only loads docs when needed, not upfront.
        """
        tools = {
            "FileSystemTools": FileSystemTools.__doc__,
            "DatabaseTools": DatabaseTools.__doc__,
            "APITools": APITools.__doc__,
        }
        return tools.get(tool_name, "Tool not found")


# ============================================================================
# COMPARISON: Token Usage
# ============================================================================

def token_comparison():
    """
    TOKEN USAGE COMPARISON

    TRADITIONAL APPROACH:
    - Load all tools: 50,000 tokens (full schemas for 50+ tools)
    - Call tool 1: 100 tokens in, 5,000 tokens out
    - Call tool 2: 100 tokens in, 10,000 tokens out
    - Call tool 3: 100 tokens in, 20,000 tokens out
    - Call tool 4: 100 tokens in, 15,000 tokens out
    - ... (10 more tools)
    - Total: ~150,000 tokens

    THIN WRAPPER APPROACH:
    - Import tools: 500 tokens (read .py file with function signatures)
    - Generate code: 1,000 tokens (Python script)
    - Execute code: 0 tokens (runs in sandbox)
    - Return result: 500 tokens (aggregated result only)
    - Total: ~2,000 tokens

    SAVINGS: 98% reduction
    """
    pass


# ============================================================================
# PRACTICAL IMPLEMENTATION PATTERNS
# ============================================================================

def pattern_1_filtering():
    """
    PATTERN 1: Data Filtering

    Traditional: Load 10,000 records through context
    Thin Wrapper: Filter in Python, return summary
    """
    # In real usage: from mcp_tools import DatabaseTools
    db = DatabaseTools()

    # Query returns 10,000 rows - stays in Python memory
    users = db.query("SELECT * FROM users")

    # Filter in Python - no context passing
    active = [u for u in users if u.get("active")]
    premium = [u for u in active if u.get("plan") == "premium"]

    # Only return aggregated result
    return {
        "total_users": len(users),
        "active_users": len(active),
        "premium_users": len(premium),
        "conversion_rate": len(premium) / len(users) if users else 0
    }


def pattern_2_multi_source_aggregation():
    """
    PATTERN 2: Multi-Source Aggregation

    Traditional: 5 tool calls, each passing full results through context
    Thin Wrapper: All data stays in Python, aggregate at end
    """
    # In real usage: from mcp_tools import FileSystemTools, DatabaseTools, APITools
    fs = FileSystemTools()
    db = DatabaseTools()
    api = APITools()

    # Gather from multiple sources - all stays in memory
    local_files = fs.search_files("*.log")
    db_events = db.query("SELECT * FROM events WHERE date > '2025-01-01'")
    api_metrics = api.fetch("/metrics/summary")

    # Aggregate in Python
    total_logs = len(local_files)
    total_events = len(db_events)
    api_requests = api_metrics.get("total_requests", 0)

    # Return only summary
    return {
        "logs_found": total_logs,
        "db_events": total_events,
        "api_requests": api_requests,
        "total_activity": total_logs + total_events + api_requests
    }


def pattern_3_iterative_processing():
    """
    PATTERN 3: Iterative Processing

    Traditional: Process one item, return result, process next item...
    Thin Wrapper: Process all items in loop, return final state
    """
    # In real usage: from mcp_tools import FileSystemTools, APITools
    fs = FileSystemTools()
    api = APITools()

    # Get list of files to process
    files = fs.search_files("*.json")

    # Process all in Python loop - no context passing per iteration
    processed = 0
    errors = []

    for file in files:
        try:
            content = fs.read_file(file)
            result = api.post("/process", {"data": content})
            if result["status"] == "success":
                processed += 1
        except Exception as e:
            errors.append({"file": file, "error": str(e)})

    # Return only summary
    return {
        "total_files": len(files),
        "processed": processed,
        "errors": len(errors),
        "error_details": errors[:5]  # First 5 errors only
    }


if __name__ == "__main__":
    # Demo: Show how tools are discovered
    print("=== MCP Tool Discovery Demo ===\n")

    registry = MCPToolRegistry()
    available = registry.list_available_tools()

    print("Available tools (discovered dynamically):")
    print(json.dumps(available, indent=2))

    print("\n=== Thin Wrapper Execution Demo ===\n")
    result = example_thin_wrapper_approach()
    print("Final result returned to LLM:")
    print(json.dumps(result, indent=2))

    print("\n=== Token Savings ===")
    print("Traditional approach: ~150,000 tokens")
    print("Thin wrapper approach: ~2,000 tokens")
    print("Savings: 98%")
