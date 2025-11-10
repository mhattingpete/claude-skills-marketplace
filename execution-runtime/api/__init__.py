"""
Marketplace Execution API

Importable API library for code execution environment.
All plugins share these core capabilities for maximum token efficiency.
"""

__version__ = "1.0.0"

# File operations
from .filesystem import (
    read_file,
    write_file,
    copy_lines,
    paste_code,
    search_replace,
    batch_copy,
    batch_transform,
)

# Code analysis
from .code_analysis import (
    find_functions,
    find_classes,
    extract_imports,
    analyze_dependencies,
    get_function_calls,
)

# Code transformation
from .code_transform import (
    rename_identifier,
    add_type_hints,
    remove_debug_statements,
    convert_to_async,
    apply_transformation,
    batch_refactor,
)

# Git operations
from .git_operations import (
    git_status,
    git_add,
    git_commit,
    git_push,
    create_branch,
)

__all__ = [
    # Filesystem
    "read_file",
    "write_file",
    "copy_lines",
    "paste_code",
    "search_replace",
    "batch_copy",
    "batch_transform",
    # Code analysis
    "find_functions",
    "find_classes",
    "extract_imports",
    "analyze_dependencies",
    "get_function_calls",
    # Code transformation
    "rename_identifier",
    "add_type_hints",
    "remove_debug_statements",
    "convert_to_async",
    "apply_transformation",
    "batch_refactor",
    # Git operations
    "git_status",
    "git_add",
    "git_commit",
    "git_push",
    "create_branch",
]
