#!/usr/bin/env python3
"""
Line-based code insertion utility.

This script provides precise line-number-based code insertion,
which complements Claude's native Edit tool (which requires exact string matching).

Usage:
    python line_insert.py <file_path> <line_number> <code> [--backup]

Examples:
    # Insert at line 10
    python line_insert.py src/main.py 10 "print('hello')"

    # Insert with backup
    python line_insert.py src/main.py 10 "print('hello')" --backup
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime


def validate_file_path(file_path: Path) -> None:
    """
    Validate that the file path is safe to use.

    Args:
        file_path: Path object to validate

    Raises:
        ValueError: If path is invalid or unsafe
    """
    # Resolve to absolute path
    abs_path = file_path.resolve()

    # Basic security: prevent directory traversal
    if ".." in str(file_path):
        raise ValueError(f"Path contains '..' which is not allowed: {file_path}")

    # Check parent directory exists (or can be created)
    if not abs_path.parent.exists():
        raise ValueError(f"Parent directory does not exist: {abs_path.parent}")


def create_backup(file_path: Path) -> Path:
    """
    Create a backup of the file with timestamp.

    Args:
        file_path: Path to the file to backup

    Returns:
        Path to the backup file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.with_suffix(f"{file_path.suffix}.backup_{timestamp}")

    if file_path.exists():
        backup_path.write_text(file_path.read_text())
        print(f"✅ Created backup: {backup_path}", file=sys.stderr)

    return backup_path


def insert_code(
    file_path: Path,
    line_number: int,
    code: str,
    create_backup_flag: bool = False
) -> None:
    """
    Insert code at a specific line number in a file.

    Args:
        file_path: Path to the target file
        line_number: Line number where code should be inserted (1-based)
        code: Code to insert (can be multiple lines)
        create_backup_flag: Whether to create a backup before modifying

    Raises:
        ValueError: If line_number is invalid
        IOError: If file operations fail
    """
    # Validate inputs
    validate_file_path(file_path)

    if line_number < 1:
        raise ValueError(f"Line number must be >= 1, got: {line_number}")

    # Create backup if requested and file exists
    if create_backup_flag and file_path.exists():
        create_backup(file_path)

    # Read existing content or start with empty
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    else:
        lines = []
        print(f"ℹ️  Creating new file: {file_path}", file=sys.stderr)

    # Prepare code lines to insert
    code_lines = code.splitlines(keepends=True)
    # Ensure last line has newline if inserting in middle of file
    if code_lines and not code_lines[-1].endswith('\n'):
        code_lines[-1] += '\n'

    # Insert at the specified line (1-based index)
    # Line 1 means insert at the beginning
    # Line len(lines)+1 means append at the end
    insert_index = line_number - 1

    if insert_index > len(lines):
        # If line number is beyond file, pad with empty lines
        lines.extend(['\\n'] * (insert_index - len(lines)))

    # Insert the code
    lines[insert_index:insert_index] = code_lines

    # Write back to file
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"✅ Inserted {len(code_lines)} line(s) at line {line_number} in {file_path}", file=sys.stderr)


def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description="Insert code at a specific line number in a file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Insert a single line at line 10
  %(prog)s src/main.py 10 "print('hello')"

  # Insert multiple lines
  %(prog)s src/main.py 10 "def foo():\\n    pass"

  # Insert with backup
  %(prog)s src/main.py 10 "print('hello')" --backup
        """
    )

    parser.add_argument(
        'file_path',
        type=Path,
        help='Path to the target file'
    )

    parser.add_argument(
        'line_number',
        type=int,
        help='Line number where code should be inserted (1-based)'
    )

    parser.add_argument(
        'code',
        type=str,
        help='Code to insert (use \\n for newlines)'
    )

    parser.add_argument(
        '--backup',
        action='store_true',
        help='Create a backup before modifying the file'
    )

    args = parser.parse_args()

    try:
        insert_code(
            file_path=args.file_path,
            line_number=args.line_number,
            code=args.code,
            create_backup_flag=args.backup
        )
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
