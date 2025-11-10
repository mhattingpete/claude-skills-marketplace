"""
Claude Code Execution Runtime.

Provides high-level APIs for bulk code operations with 90%+ token savings.

Quick start:
    from execution_runtime import fs, code, transform, git

    # Find all functions (metadata only - no source in context!)
    functions = code.find_functions('app.py', pattern='handle_.*')

    # Rename identifier across codebase
    result = transform.rename_identifier('.', 'oldName', 'newName', '**/*.py')

    # Copy lines between files
    code_block = fs.copy_lines('source.py', 10, 20)
    fs.paste_code('target.py', 50, code_block)

    # Git operations
    git.git_add(['.'])
    git.git_commit('feat: refactor code')

For automatic PII/secret masking:
    from execution_runtime import mask_secrets

    result = {'api_key': 'sk_live_abc123'}
    masked = mask_secrets(str(result))
    # Returns: {'api_key': '[REDACTED_API_KEY]'}
"""

__version__ = "2.0.0"
__author__ = "Anthropic"

# Import API modules with convenient aliases
# Note: api package is at parent level for MCP server compatibility
import sys
from pathlib import Path

# Add parent directory to path to import from api/
_parent_dir = Path(__file__).parent.parent
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

from api import (
    filesystem as fs,
    code_analysis as code,
    code_transform as transform,
    git_operations as git
)

# Import security utilities (will be created in execution_runtime package)
try:
    from .security.pii_detector import mask_secrets, PIIDetector, mask_result
except ImportError:
    # Fallback to mcp-server location during transition
    from mcp_server.security.pii_detector import mask_secrets, PIIDetector, mask_result as mask_result_fn
    mask_result = mask_result_fn

# Import session and skills management (will be created)
try:
    from .sessions import Session, create_session, load_session
    from .skills import save_skill, load_skill, list_skills
except ImportError:
    # Temporarily unavailable during migration
    Session = None
    create_session = None
    load_session = None
    save_skill = None
    load_skill = None
    list_skills = None

__all__ = [
    # Version
    '__version__',

    # API modules (aliased)
    'fs',
    'code',
    'transform',
    'git',

    # Security
    'mask_secrets',
    'PIIDetector',
    'mask_result',

    # Session management
    'Session',
    'create_session',
    'load_session',

    # Skills management
    'save_skill',
    'load_skill',
    'list_skills',
]
