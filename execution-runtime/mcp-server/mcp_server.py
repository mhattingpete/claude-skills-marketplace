"""
Marketplace Execution Runtime MCP Server

Provides code execution environment for all marketplace plugins.
Implements the Anthropic code execution pattern for massive token savings.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add api directory to Python path for imports
api_path = Path(__file__).parent.parent / "api"
sys.path.insert(0, str(api_path))

from fastmcp import FastMCP
from security.sandbox import create_sandbox_with_api
from security.pii_detector import PIIDetector, mask_secrets
from loguru import logger

# Setup logging
log_dir = Path.home() / ".claude" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "execution-runtime.log"

logger.add(
    log_file,
    rotation="1 MB",
    retention="7 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
)

# Initialize components
sandbox = create_sandbox_with_api()
pii_detector = PIIDetector()

# Create MCP server
mcp = FastMCP(
    name="MarketplaceExecutionRuntime",
    instructions="""
    Code execution environment for Claude Skills Marketplace.

    Provides Python code execution with access to marketplace APIs:
    - api.filesystem: File operations (read, write, copy, paste, search_replace, batch operations)
    - api.code_analysis: AST-based analysis (find_functions, find_classes, analyze_dependencies)
    - api.code_transform: Refactoring operations (rename, remove_debug, batch_refactor)
    - api.git_operations: Git commands (status, add, commit, push, branch)

    Security features:
    - Sandboxed execution (RestrictedPython)
    - Resource limits (30s timeout, 256MB memory)
    - PII/secret detection and masking
    - Restricted imports (whitelist only)

    Use execution mode for:
    - Bulk operations (50+ files)
    - Complex multi-step workflows
    - Iterative transformations
    - Token-efficient processing (90%+ savings)
    """
)


@mcp.tool()
def execute_python(
    code: str,
    mask_pii: bool = True,
    aggressive_masking: bool = False
) -> Dict:
    """
    Execute Python code in sandboxed environment with marketplace API access.

    The code can import from:
    - api.filesystem: File operations
    - api.code_analysis: Code analysis
    - api.code_transform: Transformations
    - api.git_operations: Git commands

    Args:
        code: Python code to execute. Can use 'result = ...' to return a value.
        mask_pii: Automatically mask secrets/PII in results
        aggressive_masking: Also mask emails, IPs, etc. (not just secrets)

    Returns:
        Dict with execution results, stdout, stderr, and status

    Example:
        ```python
        from api.filesystem import copy_lines, paste_code
        from api.code_analysis import find_functions

        # Find all functions in file
        functions = find_functions('app.py', pattern='handle_.*')

        # Copy each function to new file
        for func in functions:
            code = copy_lines('app.py', func['start_line'], func['end_line'])
            paste_code('handlers.py', -1, code)

        result = {"functions_moved": len(functions)}
        ```

    Security:
    - 30 second timeout
    - 256MB memory limit
    - Restricted imports (api.*, stdlib safe modules only)
    - No file system access outside workspace
    - Secrets automatically masked in output
    """
    logger.info(f"Executing Python code ({len(code)} characters)")

    try:
        # Execute in sandbox
        exec_result = sandbox.run(code)

        # Mask sensitive information in results
        if mask_pii and exec_result["status"] == "success":
            if exec_result.get("result"):
                exec_result["result"] = pii_detector.mask_result(
                    exec_result["result"],
                    aggressive=aggressive_masking
                )

            if exec_result.get("stdout"):
                exec_result["stdout"] = mask_secrets(exec_result["stdout"])

            if exec_result.get("stderr"):
                exec_result["stderr"] = mask_secrets(exec_result["stderr"])

        logger.info(f"Execution completed: {exec_result['status']}")
        return exec_result

    except Exception as e:
        logger.error(f"Execution error: {e}")
        return {
            "status": "error",
            "error": f"Unexpected error: {str(e)}",
            "stdout": "",
            "stderr": ""
        }


@mcp.tool()
def save_reusable_skill(
    name: str,
    code: str,
    description: Optional[str] = None
) -> Dict:
    """
    Save reusable transformation skill for future use.

    Skills are saved to ~/.claude/execution-runtime/skills/ and can be
    imported in future execution sessions.

    Args:
        name: Skill name (will be filename)
        code: Python code for the skill
        description: Optional description

    Returns:
        Dict with status and skill path

    Example:
        ```python
        save_reusable_skill(
            name="remove_debug_logs",
            code=\"\"\"
def transform(code):
    import re
    return re.sub(r'^\\s*print\\(.*\\)\\n?', '', code, flags=re.MULTILINE)
\"\"\",
            description="Remove all print statements from code"
        )
        ```
    """
    skills_dir = Path.home() / ".claude" / "execution-runtime" / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)

    skill_path = skills_dir / f"{name}.py"

    try:
        # Add description as docstring if provided
        if description:
            header = f'"""{description}"""\n\n'
            content = header + code
        else:
            content = code

        skill_path.write_text(content)

        logger.info(f"Saved skill '{name}' to {skill_path}")

        return {
            "status": "success",
            "skill_name": name,
            "path": str(skill_path),
            "message": f"Skill saved. Import with: from skills.{name} import *"
        }

    except Exception as e:
        logger.error(f"Error saving skill: {e}")
        return {
            "status": "error",
            "error": str(e)
        }


@mcp.tool()
def create_refactoring_session(
    session_name: str,
    description: Optional[str] = None
) -> Dict:
    """
    Create stateful refactoring session for multi-step operations.

    Sessions save progress to disk, allowing resumption if interrupted.
    Useful for complex refactoring across many files.

    Args:
        session_name: Unique session identifier
        description: Optional description of refactoring

    Returns:
        Dict with session ID and path

    Example:
        ```python
        # Create session
        session = create_refactoring_session(
            "rename-api-functions",
            "Rename all API functions to use new convention"
        )

        # Save progress periodically
        save_session_state(session['id'], {
            'files_processed': ['a.py', 'b.py'],
            'files_remaining': ['c.py', 'd.py', 'e.py'],
            'operations_completed': 45
        })
        ```
    """
    sessions_dir = Path.home() / ".claude" / "execution-runtime" / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)

    import json
    import datetime

    session_data = {
        "name": session_name,
        "description": description,
        "created_at": datetime.datetime.now().isoformat(),
        "state": {},
        "history": []
    }

    session_file = sessions_dir / f"{session_name}.json"

    try:
        session_file.write_text(json.dumps(session_data, indent=2))

        logger.info(f"Created session '{session_name}'")

        return {
            "status": "success",
            "session_id": session_name,
            "path": str(session_file),
            "message": f"Session created. Save state with save_session_state('{session_name}', state)"
        }

    except Exception as e:
        logger.error(f"Error creating session: {e}")
        return {
            "status": "error",
            "error": str(e)
        }


@mcp.tool()
def save_session_state(
    session_id: str,
    state: Dict
) -> Dict:
    """
    Save state for refactoring session.

    Args:
        session_id: Session identifier
        state: State dict to save

    Returns:
        Dict with status
    """
    sessions_dir = Path.home() / ".claude" / "execution-runtime" / "sessions"
    session_file = sessions_dir / f"{session_id}.json"

    if not session_file.exists():
        return {
            "status": "error",
            "error": f"Session '{session_id}' not found"
        }

    try:
        import json
        import datetime

        session_data = json.loads(session_file.read_text())
        session_data["state"] = state
        session_data["updated_at"] = datetime.datetime.now().isoformat()

        # Add to history
        session_data["history"].append({
            "timestamp": datetime.datetime.now().isoformat(),
            "state_snapshot": state
        })

        session_file.write_text(json.dumps(session_data, indent=2))

        logger.info(f"Saved state for session '{session_id}'")

        return {
            "status": "success",
            "session_id": session_id
        }

    except Exception as e:
        logger.error(f"Error saving session state: {e}")
        return {
            "status": "error",
            "error": str(e)
        }


@mcp.tool()
def list_available_apis() -> Dict:
    """
    List all available APIs and their functions for code execution.

    Returns:
        Dict with API modules and their available functions
    """
    return {
        "apis": {
            "filesystem": {
                "functions": [
                    "read_file(file_path, encoding='utf-8')",
                    "write_file(file_path, content, encoding='utf-8', create_backup=False)",
                    "copy_lines(source_file, start_line, end_line, include_line_numbers=False)",
                    "paste_code(target_file, line_number, code, create_backup=True)",
                    "search_replace(file_pattern, search, replace, regex=False, case_sensitive=True, create_backup=True)",
                    "batch_copy(operations: List[Dict])",
                    "batch_transform(operations: List[Dict], transform_fn=None)"
                ],
                "description": "File operations with batch processing"
            },
            "code_analysis": {
                "functions": [
                    "find_functions(file_path, pattern=None, regex=False)",
                    "find_classes(file_path, pattern=None)",
                    "extract_imports(file_path)",
                    "get_function_calls(file_path, function_name)",
                    "analyze_dependencies(file_path)",
                    "find_unused_imports(file_path)"
                ],
                "description": "AST-based code analysis (returns metadata, not source)"
            },
            "code_transform": {
                "functions": [
                    "rename_identifier(pattern, old_name, new_name, file_pattern='**/*.py', regex=False)",
                    "remove_debug_statements(file_path, statements=None)",
                    "convert_to_async(file_path, function_name)",
                    "apply_transformation(file_path, transform_fn, create_backup=True)",
                    "batch_refactor(operations: List[Dict])",
                    "add_docstrings(file_path, style='google')"
                ],
                "description": "Code transformation and refactoring operations"
            },
            "git_operations": {
                "functions": [
                    "git_status(cwd=None)",
                    "git_add(files: List[str], cwd=None)",
                    "git_commit(message, cwd=None)",
                    "git_push(remote='origin', branch=None, cwd=None)",
                    "create_branch(branch_name, checkout=True, cwd=None)",
                    "get_current_branch(cwd=None)",
                    "git_diff(staged=False, files=None, cwd=None)",
                    "git_log(max_count=10, oneline=True, cwd=None)"
                ],
                "description": "Git command wrappers"
            }
        },
        "example_usage": """
from api.filesystem import copy_lines, paste_code, batch_copy
from api.code_analysis import find_functions
from api.code_transform import rename_identifier
from api.git_operations import git_status, git_add, git_commit

# Example: Move all utility functions to new file
functions = find_functions('app.py', pattern='.*_util$')

operations = []
for func in functions:
    operations.append({
        'source_file': 'app.py',
        'start_line': func['start_line'],
        'end_line': func['end_line'],
        'target_file': 'utils.py',
        'target_line': -1  # Append
    })

results = batch_copy(operations)
result = {"functions_moved": len(results)}
        """
    }


def main():
    """Run the MCP server."""
    logger.info("Starting Marketplace Execution Runtime MCP Server")
    mcp.run()


if __name__ == "__main__":
    main()
