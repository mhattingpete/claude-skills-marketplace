"""
Git Operations API

Simplified git command wrappers for execution environment.
"""

import subprocess
from pathlib import Path
from typing import Dict, List, Optional


def _run_git_command(args: List[str], cwd: Optional[str] = None) -> Dict[str, any]:
    """
    Run git command and return result.

    Args:
        args: Git command arguments
        cwd: Working directory

    Returns:
        Dict with stdout, stderr, returncode
    """
    try:
        result = subprocess.run(
            ['git'] + args,
            cwd=cwd or Path.cwd(),
            capture_output=True,
            text=True,
            timeout=30
        )

        return {
            "status": "success" if result.returncode == 0 else "error",
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "error": "Git command timed out after 30 seconds"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def git_status(cwd: Optional[str] = None) -> Dict[str, any]:
    """
    Get git status of repository.

    Args:
        cwd: Working directory (defaults to current directory)

    Returns:
        Dict with status information
    """
    result = _run_git_command(['status', '--porcelain'], cwd=cwd)

    if result["status"] == "success":
        # Parse porcelain output
        lines = result["stdout"].splitlines()
        files = {
            "modified": [],
            "added": [],
            "deleted": [],
            "untracked": []
        }

        for line in lines:
            if not line.strip():
                continue

            status = line[:2]
            filepath = line[3:]

            if status.strip() == 'M' or 'M' in status:
                files["modified"].append(filepath)
            elif status.strip() == 'A' or 'A' in status:
                files["added"].append(filepath)
            elif status.strip() == 'D' or 'D' in status:
                files["deleted"].append(filepath)
            elif status.strip() == '??':
                files["untracked"].append(filepath)

        result["files"] = files
        result["has_changes"] = len(lines) > 0

    return result


def git_add(files: List[str], cwd: Optional[str] = None) -> Dict[str, any]:
    """
    Stage files for commit.

    Args:
        files: List of file paths to stage (or ['.'] for all)
        cwd: Working directory

    Returns:
        Dict with status
    """
    return _run_git_command(['add'] + files, cwd=cwd)


def git_commit(message: str, cwd: Optional[str] = None) -> Dict[str, any]:
    """
    Create git commit.

    Args:
        message: Commit message
        cwd: Working directory

    Returns:
        Dict with status and commit hash
    """
    result = _run_git_command(['commit', '-m', message], cwd=cwd)

    if result["status"] == "success":
        # Extract commit hash from output
        output = result["stdout"]
        if output:
            # Typically first line contains hash
            first_line = output.splitlines()[0]
            # Extract hash (usually in brackets or first word)
            import re
            match = re.search(r'([0-9a-f]{7,40})', first_line)
            if match:
                result["commit_hash"] = match.group(1)

    return result


def git_push(
    remote: str = "origin",
    branch: Optional[str] = None,
    cwd: Optional[str] = None
) -> Dict[str, any]:
    """
    Push commits to remote.

    Args:
        remote: Remote name (default: origin)
        branch: Branch name (defaults to current branch)
        cwd: Working directory

    Returns:
        Dict with status
    """
    args = ['push', remote]
    if branch:
        args.append(branch)

    return _run_git_command(args, cwd=cwd)


def create_branch(
    branch_name: str,
    checkout: bool = True,
    cwd: Optional[str] = None
) -> Dict[str, any]:
    """
    Create new git branch.

    Args:
        branch_name: Name of new branch
        checkout: Checkout the new branch immediately
        cwd: Working directory

    Returns:
        Dict with status
    """
    if checkout:
        result = _run_git_command(['checkout', '-b', branch_name], cwd=cwd)
    else:
        result = _run_git_command(['branch', branch_name], cwd=cwd)

    return result


def get_current_branch(cwd: Optional[str] = None) -> Dict[str, any]:
    """
    Get current git branch name.

    Args:
        cwd: Working directory

    Returns:
        Dict with branch name
    """
    result = _run_git_command(['branch', '--show-current'], cwd=cwd)

    if result["status"] == "success":
        result["branch"] = result["stdout"]

    return result


def git_diff(
    staged: bool = False,
    files: Optional[List[str]] = None,
    cwd: Optional[str] = None
) -> Dict[str, any]:
    """
    Get git diff.

    Args:
        staged: Show staged changes (--cached)
        files: Specific files to diff
        cwd: Working directory

    Returns:
        Dict with diff output
    """
    args = ['diff']
    if staged:
        args.append('--cached')
    if files:
        args.extend(files)

    result = _run_git_command(args, cwd=cwd)

    if result["status"] == "success":
        result["diff"] = result["stdout"]
        result["has_changes"] = len(result["stdout"]) > 0

    return result


def git_log(
    max_count: int = 10,
    oneline: bool = True,
    cwd: Optional[str] = None
) -> Dict[str, any]:
    """
    Get git commit history.

    Args:
        max_count: Maximum number of commits to return
        oneline: Use oneline format
        cwd: Working directory

    Returns:
        Dict with commit history
    """
    args = ['log', f'--max-count={max_count}']
    if oneline:
        args.append('--oneline')

    result = _run_git_command(args, cwd=cwd)

    if result["status"] == "success":
        commits = []
        for line in result["stdout"].splitlines():
            if line.strip():
                # Parse oneline format: hash message
                parts = line.split(' ', 1)
                if len(parts) == 2:
                    commits.append({
                        "hash": parts[0],
                        "message": parts[1]
                    })

        result["commits"] = commits

    return result
