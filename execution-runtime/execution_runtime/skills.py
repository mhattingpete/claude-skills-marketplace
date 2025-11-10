"""
Reusable transformation skills for code execution.

Skills are Python modules that can be saved and reused across sessions.
Useful for common transformations like removing debug statements, adding docstrings, etc.
"""

from pathlib import Path
from typing import Optional, List


SKILLS_DIR = Path.home() / ".claude" / "execution-runtime" / "skills"


def save_skill(name: str, code: str, description: Optional[str] = None) -> dict:
    """
    Save reusable skill for future use.

    Skills are saved to ~/.claude/execution-runtime/skills/ and can be
    imported in future execution sessions.

    Args:
        name: Skill name (will be used as filename)
        code: Python code for the skill
        description: Optional description (added as docstring)

    Returns:
        Dict with status, path, and import instructions

    Example:
        >>> save_skill(
        ...     name="remove_debug_logs",
        ...     code='''
        ... def transform(code):
        ...     import re
        ...     code = re.sub(r"^\\s*print\\(.*\\)\\n?", "", code, flags=re.MULTILINE)
        ...     code = re.sub(r"^\\s*import pdb.*\\n?", "", code, flags=re.MULTILINE)
        ...     return code
        ... ''',
        ...     description="Remove debug print and pdb statements"
        ... )
        {'status': 'success', 'skill_name': 'remove_debug_logs', ...}

        # Later, use the skill:
        >>> import sys
        >>> sys.path.insert(0, str(SKILLS_DIR))
        >>> from remove_debug_logs import transform
        >>> cleaned = transform(original_code)
    """
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    skill_path = SKILLS_DIR / f"{name}.py"

    try:
        # Add description as docstring if provided
        if description:
            header = f'"""{description}"""\n\n'
            content = header + code
        else:
            content = code

        skill_path.write_text(content)

        return {
            "status": "success",
            "skill_name": name,
            "path": str(skill_path),
            "import_as": f"from skills.{name} import *"
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def load_skill(name: str) -> str:
    """
    Load skill code.

    Args:
        name: Skill name

    Returns:
        Skill code as string

    Raises:
        FileNotFoundError: If skill doesn't exist

    Example:
        >>> code = load_skill("remove_debug_logs")
        >>> print(code[:50])
        """Remove debug print and pdb statements"""
        ...
    """
    skill_path = SKILLS_DIR / f"{name}.py"

    if not skill_path.exists():
        raise FileNotFoundError(
            f"Skill '{name}' not found. "
            f"Available skills: {', '.join(list_skills())}"
        )

    return skill_path.read_text()


def list_skills() -> List[str]:
    """
    List all available skills.

    Returns:
        List of skill names

    Example:
        >>> skills = list_skills()
        >>> for skill in skills:
        ...     print(f"Available skill: {skill}")
        Available skill: remove_debug_logs
        Available skill: add_docstrings
        ...
    """
    if not SKILLS_DIR.exists():
        return []

    return [f.stem for f in SKILLS_DIR.glob("*.py") if not f.name.startswith("_")]


def delete_skill(name: str):
    """
    Delete a skill.

    Args:
        name: Skill name

    Example:
        >>> delete_skill("old_transformation")
    """
    skill_path = SKILLS_DIR / f"{name}.py"
    if skill_path.exists():
        skill_path.unlink()


def get_skill_path() -> Path:
    """
    Get path to skills directory.

    Useful for adding to sys.path to import skills directly.

    Returns:
        Path to skills directory

    Example:
        >>> import sys
        >>> sys.path.insert(0, str(get_skill_path()))
        >>> from my_skill import transform
    """
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    return SKILLS_DIR
