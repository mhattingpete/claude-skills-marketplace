"""
PRODUCTION EXAMPLE: Outlook MCP with Code Execution Pattern

This shows the ACTUAL architecture from Anthropic's article:

Architecture:
-----------
1. Your Outlook MCP server runs (existing server, unchanged)
2. Thin wrappers call your MCP server via MCP protocol
3. LLM discovers wrappers via filesystem
4. LLM generates Python code that imports wrappers
5. Code executes, calling real MCP server through wrappers
6. Results stay in Python, summary returned to LLM

Key insight: MCP server is UNCHANGED. Wrappers are the bridge.
"""

import json
from typing import Any, Dict, List, Optional


# ============================================================================
# STEP 1: MCP Client (connects to your actual MCP server)
# ============================================================================

class MCPClient:
    """
    Client that connects to your actual Outlook MCP server.

    This is the bridge between Python wrappers and your real MCP server.
    Uses MCP protocol (stdio or SSE) to communicate.
    """

    def __init__(self, server_command: List[str]):
        """
        Initialize MCP client.

        Args:
            server_command: Command to start MCP server
                           e.g., ["node", "path/to/outlook-mcp/dist/index.js"]
        """
        self.server_command = server_command
        self.server_process = None
        # In production: Initialize MCP connection here
        # import mcp
        # self.session = mcp.ClientSession(...)

    def call(self, tool_name: str, **arguments) -> Any:
        """
        Call a tool on the actual MCP server.

        Args:
            tool_name: MCP tool name (e.g., "outlook_list_emails")
            **arguments: Tool arguments

        Returns:
            Tool result from actual MCP server
        """
        # In production, this would:
        # 1. Send request to MCP server via stdio/SSE
        # 2. Wait for response
        # 3. Return result

        # Example using MCP SDK:
        # result = await self.session.call_tool(tool_name, arguments)
        # return result.content

        # Mock for demonstration:
        print(f"[MCP Call] {tool_name}({arguments})")

        # Simulate calling your actual Outlook MCP server
        if tool_name == "outlook_list_emails":
            return [
                {
                    "id": "msg_001",
                    "subject": "Q4 Planning",
                    "from": "manager@company.com",
                    "date": "2025-11-08T10:00:00Z"
                }
            ]
        elif tool_name == "outlook_search_emails":
            return [{"id": "msg_002", "subject": f"Search: {arguments.get('query')}"}]

        return {}


# ============================================================================
# STEP 2: Thin Wrappers (exposed as filesystem for LLM discovery)
# ============================================================================

# This would be in: /mcp_tools/outlook/email.py
class OutlookEmailWrapper:
    """
    Thin wrapper that calls YOUR actual Outlook MCP server.

    This file is discovered by LLM via filesystem exploration.
    Each method calls the real MCP server through MCPClient.
    """

    def __init__(self, mcp_client: MCPClient):
        """
        Initialize with MCP client connected to your server.

        Args:
            mcp_client: Client connected to your Outlook MCP server
        """
        self.client = mcp_client

    def list_emails(
        self,
        folder: str = "inbox",
        limit: int = 50,
        unread_only: bool = False
    ) -> List[Dict[str, Any]]:
        """
        List emails from Outlook.

        This calls your actual Outlook MCP server's list_emails tool.
        """
        # Call YOUR actual MCP server
        return self.client.call(
            "outlook_list_emails",
            folder=folder,
            limit=limit,
            unread_only=unread_only
        )

    def search_emails(self, query: str) -> List[Dict[str, Any]]:
        """Search emails - calls your actual MCP server."""
        return self.client.call("outlook_search_emails", query=query)

    def send_email(self, to: List[str], subject: str, body: str) -> Dict[str, Any]:
        """Send email - calls your actual MCP server."""
        return self.client.call(
            "outlook_send_email",
            to=to,
            subject=subject,
            body=body
        )


# This would be in: /mcp_tools/outlook/calendar.py
class OutlookCalendarWrapper:
    """Thin wrapper for Outlook calendar - calls your actual MCP server."""

    def __init__(self, mcp_client: MCPClient):
        self.client = mcp_client

    def list_events(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List calendar events - calls your actual MCP server."""
        return self.client.call(
            "outlook_list_events",
            start_date=start_date,
            end_date=end_date
        )

    def create_event(
        self,
        subject: str,
        start: str,
        end: str,
        attendees: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Create calendar event - calls your actual MCP server."""
        return self.client.call(
            "outlook_create_event",
            subject=subject,
            start=start,
            end=end,
            attendees=attendees or []
        )


# ============================================================================
# STEP 3: Filesystem Structure (for LLM discovery)
# ============================================================================

"""
Directory structure that LLM explores:

/mcp_tools/
├── __init__.py              # Registry
├── outlook/
│   ├── __init__.py          # Exports email, calendar
│   ├── email.py             # OutlookEmailWrapper
│   └── calendar.py          # OutlookCalendarWrapper
└── README.md                # Brief description of tools

LLM can:
1. List directory: os.listdir('/mcp_tools') → sees 'outlook'
2. Read file: open('/mcp_tools/outlook/email.py') → sees available methods
3. Import: from mcp_tools.outlook import email
"""


# ============================================================================
# STEP 4: LLM-Generated Code (using the wrappers)
# ============================================================================

def example_llm_generated_code():
    """
    This is the code that the LLM would generate.

    Notice:
    - Imports thin wrappers (not direct MCP calls)
    - All data stays in Python
    - Calls actual MCP server through wrappers
    - Only returns summary
    """

    # Initialize MCP client (connected to YOUR actual Outlook MCP server)
    mcp_client = MCPClient(["node", "dist/index.js"])  # Your actual server

    # Import thin wrappers
    email = OutlookEmailWrapper(mcp_client)
    calendar = OutlookCalendarWrapper(mcp_client)

    print("\n=== LLM-Generated Code Executing ===\n")

    # Task: "Find unread emails about Q4, check calendar, schedule meeting"

    # Step 1: Fetch emails (calls REAL MCP server, data stays in Python)
    print("1. Fetching emails from Outlook MCP server...")
    all_emails = email.list_emails(folder="inbox", unread_only=True)
    print(f"   → Fetched {len(all_emails)} emails (stays in memory)")

    # Step 2: Filter in Python (no context passing!)
    print("\n2. Filtering emails in Python...")
    q4_emails = [e for e in all_emails if "Q4" in e.get("subject", "")]
    print(f"   → Found {len(q4_emails)} Q4 emails (stays in memory)")

    # Step 3: Check calendar (calls REAL MCP server, data stays in Python)
    print("\n3. Fetching calendar from Outlook MCP server...")
    events = calendar.list_events(start_date="2025-11-11", end_date="2025-11-15")
    print(f"   → Fetched calendar events (stays in memory)")

    # Step 4: Find free slot in Python (no context passing!)
    print("\n4. Finding free slots in Python...")
    # Process in memory
    free_slot = {"start": "2025-11-12T14:00:00Z", "end": "2025-11-12T15:00:00Z"}
    print(f"   → Found free slot (stays in memory)")

    # Step 5: Create meeting (calls REAL MCP server)
    print("\n5. Creating meeting via Outlook MCP server...")
    meeting = calendar.create_event(
        subject="Q4 Planning Discussion",
        start=free_slot["start"],
        end=free_slot["end"],
        attendees=["manager@company.com"]
    )
    print(f"   → Meeting created")

    # Step 6: Return ONLY summary to LLM (not all the data!)
    print("\n6. Returning summary to LLM...")
    summary = {
        "q4_emails_found": len(q4_emails),
        "meeting_created": meeting.get("id"),
        "meeting_time": meeting.get("start")
    }

    print(f"\n=== Summary Returned to LLM (only this!) ===")
    print(json.dumps(summary, indent=2))

    return summary


# ============================================================================
# STEP 5: Token Comparison
# ============================================================================

def compare_approaches():
    """
    Compare traditional MCP vs code execution approach.
    """

    print("\n" + "="*70)
    print("TOKEN COMPARISON")
    print("="*70)

    print("\n### TRADITIONAL APPROACH (Direct MCP Tool Calls)")
    print("\n1. Load all Outlook MCP tool schemas:")
    print("   - outlook_list_emails schema: 500 tokens")
    print("   - outlook_search_emails schema: 500 tokens")
    print("   - outlook_send_email schema: 500 tokens")
    print("   - outlook_list_events schema: 500 tokens")
    print("   - outlook_create_event schema: 500 tokens")
    print("   - ... (10 more tools)")
    print("   Total: 7,500 tokens")

    print("\n2. Call outlook_list_emails:")
    print("   - Request: 100 tokens")
    print("   - Response: 50 emails × 100 tokens = 5,000 tokens")

    print("\n3. Filter emails (in LLM context):")
    print("   - Process all 50 emails: 2,000 tokens")

    print("\n4. Call outlook_list_events:")
    print("   - Request: 100 tokens")
    print("   - Response: 30 events × 100 tokens = 3,000 tokens")

    print("\n5. Call outlook_create_event:")
    print("   - Request: 100 tokens")
    print("   - Response: 100 tokens")

    print("\n📊 TRADITIONAL TOTAL: 17,900 tokens")

    print("\n" + "="*70)

    print("\n### CODE EXECUTION APPROACH (Thin Wrappers)")
    print("\n1. LLM discovers tools via filesystem:")
    print("   - os.listdir('/mcp_tools') → ['outlook']")
    print("   - List files: 20 tokens")

    print("\n2. LLM reads wrapper files:")
    print("   - Read email.py: 400 tokens (function signatures only)")
    print("   - Read calendar.py: 400 tokens")
    print("   Total: 800 tokens")

    print("\n3. LLM generates Python code:")
    print("   - Code to orchestrate workflow: 800 tokens")

    print("\n4. Code executes (calls real MCP server):")
    print("   - Fetches 50 emails → stays in Python memory (0 context tokens)")
    print("   - Filters in Python → stays in memory (0 context tokens)")
    print("   - Fetches 30 events → stays in memory (0 context tokens)")
    print("   - Creates meeting → stays in memory (0 context tokens)")

    print("\n5. Return summary to LLM:")
    print("   - Small JSON summary: 100 tokens")

    print("\n📊 CODE EXECUTION TOTAL: 1,720 tokens")

    print("\n" + "="*70)
    print(f"\n💰 SAVINGS: 90.4% reduction (17,900 → 1,720 tokens)")
    print("\n" + "="*70)


# ============================================================================
# STEP 6: Production Setup Guide
# ============================================================================

def print_production_setup():
    """
    How to actually set this up with your Outlook MCP server.
    """

    print("\n" + "="*70)
    print("PRODUCTION SETUP WITH YOUR OUTLOOK MCP SERVER")
    print("="*70)

    print("""
Step 1: Keep Your Existing Outlook MCP Server Running
------------------------------------------------------
Your Outlook MCP server runs unchanged:

  $ node dist/index.js

It exposes tools like:
  - outlook_list_emails
  - outlook_search_emails
  - outlook_list_events
  - etc.


Step 2: Create Thin Wrapper Directory
--------------------------------------
Create filesystem structure for LLM discovery:

  /mcp_tools/
  ├── __init__.py
  └── outlook/
      ├── __init__.py
      ├── email.py          # Wraps email tools
      └── calendar.py       # Wraps calendar tools


Step 3: Initialize MCP Client in Each Wrapper
----------------------------------------------
Each wrapper file connects to your actual MCP server:

  # email.py
  import mcp

  # Connect to YOUR running Outlook MCP server
  client = mcp.ClientSession(
      command=["node", "/path/to/outlook-mcp/dist/index.js"]
  )

  class EmailWrapper:
      def list_emails(self, folder="inbox", limit=50):
          # Call YOUR actual MCP server
          result = client.call_tool("outlook_list_emails", {
              "folder": folder,
              "limit": limit
          })
          return result


Step 4: LLM Discovers and Uses Wrappers
----------------------------------------
LLM generates code like:

  # Discover tools
  import os
  tools = os.listdir('/mcp_tools')  # Sees: ['outlook']

  # Read wrapper to see available methods
  from mcp_tools.outlook import email, calendar

  # Use wrappers (which call YOUR real MCP server)
  emails = email.list_emails()
  events = calendar.list_events()

  # Process in Python, return summary
  summary = {
      "total_emails": len(emails),
      "total_events": len(events)
  }


Step 5: Security & Execution Environment
-----------------------------------------
Run LLM-generated code in secure sandbox:

  - Docker container with limited permissions
  - Resource limits (CPU, memory, disk)
  - Network access to MCP server only
  - Timeout enforcement
  - Logging and monitoring


Key Points:
-----------
✅ Your Outlook MCP server is UNCHANGED
✅ Wrappers are just Python bridges to your MCP server
✅ LLM discovers wrappers via filesystem (progressive disclosure)
✅ All data stays in Python execution environment
✅ Only summaries returned to LLM context
✅ 90%+ token reduction while using your existing MCP server
""")


# ============================================================================
# MAIN DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("OUTLOOK MCP + CODE EXECUTION: PRODUCTION EXAMPLE")
    print("="*70)
    print("\nShowing how thin wrappers call YOUR actual Outlook MCP server")
    print("while achieving 90%+ token reduction.\n")

    # Run example
    example_llm_generated_code()

    # Show comparison
    compare_approaches()

    # Show setup guide
    print_production_setup()

    print("\n" + "="*70)
    print("KEY INSIGHT")
    print("="*70)
    print("""
Your Outlook MCP server remains UNCHANGED.

The thin wrappers are just Python files that:
1. Connect to your running MCP server
2. Expose methods that call your MCP tools
3. Allow LLM to discover them via filesystem
4. Enable code execution pattern for massive token savings

Architecture:
  LLM → Python Code → Thin Wrappers → YOUR MCP Server → Outlook API

All intermediate data (emails, events, etc.) stays in Python execution
environment. Only final summaries go back to LLM context.

Result: 90%+ token reduction using your existing MCP infrastructure!
""")
