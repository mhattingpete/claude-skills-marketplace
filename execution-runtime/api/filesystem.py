"""
Filesystem Operations API

Core file operations for code execution environment.
Zero tokens in context - all operations run locally.
"""

import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Callable
import re


def read_file(file_path: str, encoding: str = "utf-8") -> str:
    """
    Read entire file content.

    Args:
        file_path: Path to file
        encoding: File encoding (default: utf-8)

    Returns:
        File content as string
    """
    return Path(file_path).read_text(encoding=encoding)


def write_file(
    file_path: str,
    content: str,
    encoding: str = "utf-8",
    create_backup: bool = False
) -> Dict[str, any]:
    """
    Write content to file.

    Args:
        file_path: Path to target file
        content: Content to write
        encoding: File encoding
        create_backup: Create backup before writing

    Returns:
        dict with status and backup path if created
    """
    path = Path(file_path)
    result = {"status": "success", "file": str(path)}

    if create_backup and path.exists():
        backup_path = _create_backup(path)
        result["backup"] = str(backup_path)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding=encoding)

    return result


def copy_lines(
    source_file: str,
    start_line: int,
    end_line: int,
    include_line_numbers: bool = False
) -> str:
    """
    Copy specific line range from source file.

    Args:
        source_file: Path to source file
        start_line: Starting line (1-based)
        end_line: Ending line (1-based, inclusive)
        include_line_numbers: Include line numbers in output

    Returns:
        Copied lines as string
    """
    with open(source_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Convert to 0-based indexing
    start_idx = start_line - 1
    end_idx = end_line  # end_line is inclusive, so no -1 needed for slicing

    selected_lines = lines[start_idx:end_idx]

    if include_line_numbers:
        numbered_lines = []
        for i, line in enumerate(selected_lines, start=start_line):
            numbered_lines.append(f"{i:4d} | {line}")
        return ''.join(numbered_lines)

    return ''.join(selected_lines)


def paste_code(
    target_file: str,
    line_number: int,
    code: str,
    create_backup: bool = True
) -> Dict[str, any]:
    """
    Paste code at specific line number.

    Args:
        target_file: Path to target file
        line_number: Line number to insert at (1-based). Use -1 for append.
        code: Code to insert
        create_backup: Create backup before modifying

    Returns:
        dict with status info
    """
    path = Path(target_file)

    # Read existing content or start with empty
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if create_backup:
            backup_path = _create_backup(path)
    else:
        lines = []
        backup_path = None

    # Prepare code lines
    code_lines = code.splitlines(keepends=True)
    if code_lines and not code_lines[-1].endswith('\n'):
        code_lines[-1] += '\n'

    # Insert at specified line
    if line_number == -1:
        # Append to end
        lines.extend(code_lines)
        insert_line = len(lines) - len(code_lines) + 1
    else:
        insert_idx = line_number - 1
        if insert_idx > len(lines):
            # Pad with empty lines if necessary
            lines.extend(['\n'] * (insert_idx - len(lines)))
        lines[insert_idx:insert_idx] = code_lines
        insert_line = line_number

    # Write back
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    return {
        "status": "success",
        "file": str(path),
        "line": insert_line,
        "lines_inserted": len(code_lines),
        "backup": str(backup_path) if backup_path else None
    }


def search_replace(
    file_pattern: str,
    search: str,
    replace: str,
    regex: bool = False,
    case_sensitive: bool = True,
    create_backup: bool = True
) -> Dict[str, any]:
    """
    Search and replace across files matching pattern.

    Args:
        file_pattern: Glob pattern for files (e.g., "**/*.py")
        search: Search string or regex pattern
        replace: Replacement string
        regex: Treat search as regex
        case_sensitive: Case sensitive search
        create_backup: Create backups before modifying

    Returns:
        dict with files modified and counts
    """
    from pathlib import Path

    base_path = Path.cwd()
    files = list(base_path.glob(file_pattern))

    results = []
    total_replacements = 0

    for file_path in files:
        if not file_path.is_file():
            continue

        try:
            content = file_path.read_text(encoding='utf-8')

            if regex:
                flags = 0 if case_sensitive else re.IGNORECASE
                new_content, count = re.subn(search, replace, content, flags=flags)
            else:
                if case_sensitive:
                    new_content = content.replace(search, replace)
                    count = content.count(search)
                else:
                    # Case insensitive replacement
                    pattern = re.compile(re.escape(search), re.IGNORECASE)
                    new_content, count = pattern.subn(replace, content)

            if count > 0:
                if create_backup:
                    _create_backup(file_path)

                file_path.write_text(new_content, encoding='utf-8')
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


def batch_copy(operations: List[Dict]) -> List[Dict]:
    """
    Execute multiple copy-paste operations in sequence.

    Args:
        operations: List of operation dicts with keys:
            - source_file: Source file path
            - start_line: Start line
            - end_line: End line
            - target_file: Target file path
            - target_line: Target line number
            - create_backup: (optional) Create backup

    Returns:
        List of result dicts
    """
    results = []

    for op in operations:
        try:
            # Copy from source
            code = copy_lines(
                op['source_file'],
                op['start_line'],
                op['end_line']
            )

            # Paste to target
            result = paste_code(
                op['target_file'],
                op['target_line'],
                code,
                create_backup=op.get('create_backup', True)
            )

            result['operation'] = 'copy_paste'
            result['source'] = op['source_file']
            results.append(result)

        except Exception as e:
            results.append({
                "status": "error",
                "operation": "copy_paste",
                "source": op.get('source_file'),
                "target": op.get('target_file'),
                "error": str(e)
            })

    return results


def batch_transform(
    operations: List[Dict],
    transform_fn: Optional[Callable[[str], str]] = None
) -> List[Dict]:
    """
    Apply transformations to multiple files/code blocks.

    Args:
        operations: List of dicts with:
            - file: File path
            - start_line: (optional) Start line
            - end_line: (optional) End line
            - transform: (optional) Custom transform function
        transform_fn: Default transform function to apply

    Returns:
        List of result dicts
    """
    results = []

    for op in operations:
        try:
            file_path = Path(op['file'])

            # Read content
            if 'start_line' in op and 'end_line' in op:
                content = copy_lines(op['file'], op['start_line'], op['end_line'])
                is_partial = True
            else:
                content = read_file(op['file'])
                is_partial = False

            # Apply transformation
            transform = op.get('transform', transform_fn)
            if transform is None:
                raise ValueError("No transform function provided")

            transformed = transform(content)

            # Write back
            if is_partial:
                # Replace the specific lines
                with open(file_path, 'r') as f:
                    lines = f.readlines()

                start_idx = op['start_line'] - 1
                end_idx = op['end_line']

                new_lines = transformed.splitlines(keepends=True)
                lines[start_idx:end_idx] = new_lines

                file_path.write_text(''.join(lines))
            else:
                write_file(op['file'], transformed, create_backup=True)

            results.append({
                "status": "success",
                "file": op['file'],
                "operation": "transform"
            })

        except Exception as e:
            results.append({
                "status": "error",
                "file": op.get('file'),
                "operation": "transform",
                "error": str(e)
            })

    return results


def _create_backup(file_path: Path) -> Path:
    """Create timestamped backup of file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.with_suffix(f"{file_path.suffix}.backup_{timestamp}")
    shutil.copy2(file_path, backup_path)
    return backup_path
