"""
Code Transformation API

High-level code transformation operations for refactoring and code quality.
"""

import ast
import re
from pathlib import Path
from typing import List, Dict, Optional, Callable
from .filesystem import read_file, write_file, search_replace


def rename_identifier(
    pattern: str,
    old_name: str,
    new_name: str,
    file_pattern: str = "**/*.py",
    regex: bool = False
) -> Dict[str, any]:
    """
    Rename identifier across all matching files.

    Args:
        pattern: Base directory pattern
        old_name: Current identifier name
        new_name: New identifier name
        file_pattern: File glob pattern
        regex: Use regex matching

    Returns:
        Dict with files modified and counts
    """
    base_path = Path(pattern) if Path(pattern).is_dir() else Path.cwd()
    files = list(base_path.glob(file_pattern))

    results = []
    total_replacements = 0

    for file_path in files:
        if not file_path.is_file():
            continue

        try:
            content = read_file(str(file_path))

            # Use word boundaries for identifier replacement
            if regex:
                pattern_str = old_name
            else:
                # Match whole words only (identifier boundaries)
                pattern_str = rf'\b{re.escape(old_name)}\b'

            new_content, count = re.subn(pattern_str, new_name, content)

            if count > 0:
                write_file(str(file_path), new_content, create_backup=True)
                results.append({
                    "file": str(file_path),
                    "replacements": count,
                    "status": "modified"
                })
                total_replacements += count

        except Exception as e:
            results.append({
                "file": str(file_path),
                "status": "error",
                "error": str(e)
            })

    return {
        "files_modified": len([r for r in results if r["status"] == "modified"]),
        "total_replacements": total_replacements,
        "details": results
    }


def add_type_hints(
    file_path: str,
    function_name: Optional[str] = None
) -> Dict[str, any]:
    """
    Add basic type hints to functions.

    Note: This is a simple implementation. For production use,
    consider using tools like MonkeyType or PyAnnotate.

    Args:
        file_path: Path to Python file
        function_name: Specific function to annotate (None for all)

    Returns:
        Dict with status and functions modified
    """
    # This is a placeholder for a more sophisticated implementation
    # A full implementation would use AST manipulation to add type hints
    # based on analysis or type inference

    return {
        "status": "not_implemented",
        "message": "Type hint addition requires sophisticated type inference. "
                   "Consider using tools like MonkeyType or manual annotation."
    }


def remove_debug_statements(
    file_path: str,
    statements: Optional[List[str]] = None
) -> Dict[str, any]:
    """
    Remove debug print statements and logging from code.

    Args:
        file_path: Path to Python file
        statements: List of patterns to remove (default: common debug patterns)

    Returns:
        Dict with status and lines removed
    """
    if statements is None:
        statements = [
            r'^\s*print\(',
            r'^\s*console\.log\(',
            r'^\s*debugger;?',
            r'^\s*import pdb.*',
            r'^\s*pdb\.set_trace\(',
            r'^\s*breakpoint\(',
        ]

    content = read_file(file_path)
    lines = content.splitlines(keepends=True)

    new_lines = []
    removed_count = 0

    for line in lines:
        should_remove = False
        for pattern in statements:
            if re.search(pattern, line):
                should_remove = True
                removed_count += 1
                break

        if not should_remove:
            new_lines.append(line)

    if removed_count > 0:
        write_file(file_path, ''.join(new_lines), create_backup=True)

    return {
        "status": "success",
        "file": file_path,
        "lines_removed": removed_count
    }


def convert_to_async(
    file_path: str,
    function_name: str
) -> Dict[str, any]:
    """
    Convert a synchronous function to async.

    Note: This is a basic implementation that adds async/await keywords.
    Manual review is recommended for complex cases.

    Args:
        file_path: Path to Python file
        function_name: Function to convert

    Returns:
        Dict with status
    """
    content = read_file(file_path)

    # Simple pattern-based conversion
    # Replace 'def function_name' with 'async def function_name'
    pattern = rf'(\s*)def\s+{re.escape(function_name)}\s*\('
    replacement = r'\1async def ' + function_name + '('

    new_content, count = re.subn(pattern, replacement, content)

    if count > 0:
        write_file(file_path, new_content, create_backup=True)
        return {
            "status": "success",
            "file": file_path,
            "message": f"Converted {function_name} to async. Manual review recommended for await calls."
        }
    else:
        return {
            "status": "not_found",
            "message": f"Function {function_name} not found in {file_path}"
        }


def apply_transformation(
    file_path: str,
    transform_fn: Callable[[str], str],
    create_backup: bool = True
) -> Dict[str, any]:
    """
    Apply custom transformation function to file.

    Args:
        file_path: Path to file
        transform_fn: Function that takes content and returns transformed content
        create_backup: Create backup before modifying

    Returns:
        Dict with status
    """
    try:
        content = read_file(file_path)
        transformed = transform_fn(content)

        if content != transformed:
            write_file(file_path, transformed, create_backup=create_backup)
            return {
                "status": "success",
                "file": file_path,
                "modified": True
            }
        else:
            return {
                "status": "success",
                "file": file_path,
                "modified": False,
                "message": "No changes after transformation"
            }

    except Exception as e:
        return {
            "status": "error",
            "file": file_path,
            "error": str(e)
        }


def batch_refactor(operations: List[Dict]) -> List[Dict]:
    """
    Execute multiple refactoring operations in sequence.

    Args:
        operations: List of operation dicts with:
            - type: 'rename', 'remove_debug', 'custom'
            - ... type-specific parameters

    Returns:
        List of result dicts
    """
    results = []

    for op in operations:
        try:
            op_type = op.get('type')

            if op_type == 'rename':
                result = rename_identifier(
                    pattern=op.get('pattern', '.'),
                    old_name=op['old_name'],
                    new_name=op['new_name'],
                    file_pattern=op.get('file_pattern', '**/*.py')
                )
                results.append(result)

            elif op_type == 'remove_debug':
                result = remove_debug_statements(
                    file_path=op['file_path'],
                    statements=op.get('statements')
                )
                results.append(result)

            elif op_type == 'search_replace':
                result = search_replace(
                    file_pattern=op['file_pattern'],
                    search=op['search'],
                    replace=op['replace'],
                    regex=op.get('regex', False)
                )
                results.append(result)

            elif op_type == 'custom':
                result = apply_transformation(
                    file_path=op['file_path'],
                    transform_fn=op['transform_fn']
                )
                results.append(result)

            else:
                results.append({
                    "status": "error",
                    "error": f"Unknown operation type: {op_type}"
                })

        except Exception as e:
            results.append({
                "status": "error",
                "operation": op.get('type', 'unknown'),
                "error": str(e)
            })

    return results


def add_docstrings(
    file_path: str,
    style: str = "google"
) -> Dict[str, any]:
    """
    Add placeholder docstrings to functions/classes missing them.

    Args:
        file_path: Path to Python file
        style: Docstring style ('google', 'numpy', or 'sphinx')

    Returns:
        Dict with status and functions modified
    """
    with open(file_path, 'r') as f:
        content = f.read()

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return {"status": "error", "error": "Syntax error in file"}

    lines = content.splitlines()
    modifications = []

    # Find functions/classes without docstrings
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            if ast.get_docstring(node) is None:
                # Calculate indentation
                line_idx = node.lineno - 1
                indent = len(lines[line_idx]) - len(lines[line_idx].lstrip())

                # Create placeholder docstring
                if style == "google":
                    docstring = '"""TODO: Add description."""'
                elif style == "numpy":
                    docstring = '"""\n    TODO: Add description.\n    """'
                else:  # sphinx
                    docstring = '"""TODO: Add description."""'

                modifications.append({
                    "line": node.lineno,
                    "indent": indent,
                    "docstring": docstring,
                    "name": node.name
                })

    if modifications:
        # Insert docstrings (in reverse order to maintain line numbers)
        for mod in sorted(modifications, key=lambda x: x["line"], reverse=True):
            line_idx = mod["line"]
            indent_str = " " * (mod["indent"] + 4)
            docstring_line = f"{indent_str}{mod['docstring']}\n"
            lines.insert(line_idx, docstring_line)

        new_content = '\n'.join(lines)
        write_file(file_path, new_content, create_backup=True)

        return {
            "status": "success",
            "file": file_path,
            "docstrings_added": len(modifications),
            "functions": [m["name"] for m in modifications]
        }
    else:
        return {
            "status": "success",
            "file": file_path,
            "docstrings_added": 0,
            "message": "All functions/classes already have docstrings"
        }
