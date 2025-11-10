"""
Session management for multi-step refactoring operations.

Stateful sessions allow complex refactoring work to be saved and resumed if interrupted.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List


SESSIONS_DIR = Path.home() / ".claude" / "execution-runtime" / "sessions"


class Session:
    """
    Stateful refactoring session for multi-step operations.

    Example:
        >>> session = Session("modernize-codebase", "Update to Python 3.11+ syntax")
        >>> session.save_state({'processed': ['a.py', 'b.py'], 'remaining': ['c.py']})
        >>> state = session.load_state()
        >>> print(state['processed'])
        ['a.py', 'b.py']
    """

    def __init__(self, name: str, description: str = ""):
        """
        Create or load session.

        Args:
            name: Unique session identifier
            description: Optional description of the refactoring work
        """
        self.name = name
        self.description = description
        self.session_file = SESSIONS_DIR / f"{name}.json"

        SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

        if not self.session_file.exists():
            self._create_new()

    def _create_new(self):
        """Create new session file."""
        data = {
            "name": self.name,
            "description": self.description,
            "created_at": datetime.now().isoformat(),
            "state": {},
            "history": []
        }
        self.session_file.write_text(json.dumps(data, indent=2))

    def save_state(self, state: Dict):
        """
        Save current state to disk.

        Args:
            state: State dictionary to save. Can contain any JSON-serializable data.

        Example:
            >>> session.save_state({
            ...     'files_processed': ['a.py', 'b.py'],
            ...     'files_remaining': ['c.py', 'd.py'],
            ...     'operations_completed': 45
            ... })
        """
        data = json.loads(self.session_file.read_text())
        data["state"] = state
        data["updated_at"] = datetime.now().isoformat()
        data["history"].append({
            "timestamp": datetime.now().isoformat(),
            "state_snapshot": state
        })
        self.session_file.write_text(json.dumps(data, indent=2))

    def load_state(self) -> Dict:
        """
        Load current state from disk.

        Returns:
            Current state dictionary

        Example:
            >>> state = session.load_state()
            >>> print(state.get('files_processed', []))
            ['a.py', 'b.py']
        """
        data = json.loads(self.session_file.read_text())
        return data.get("state", {})

    def get_history(self) -> List[Dict]:
        """
        Get session history with timestamps.

        Returns:
            List of historical state snapshots with timestamps

        Example:
            >>> history = session.get_history()
            >>> for entry in history:
            ...     print(f"{entry['timestamp']}: {entry['state_snapshot']}")
        """
        data = json.loads(self.session_file.read_text())
        return data.get("history", [])

    def delete(self):
        """Delete this session."""
        if self.session_file.exists():
            self.session_file.unlink()

    @property
    def exists(self) -> bool:
        """Check if session file exists."""
        return self.session_file.exists()

    @property
    def path(self) -> str:
        """Get session file path."""
        return str(self.session_file)


def create_session(name: str, description: str = "") -> Session:
    """
    Create new refactoring session.

    Args:
        name: Unique session identifier
        description: Optional description

    Returns:
        Session object

    Example:
        >>> session = create_session("rename-api-functions", "Rename all API functions")
        >>> session.save_state({'progress': 50})
    """
    return Session(name, description)


def load_session(name: str) -> Session:
    """
    Load existing session.

    Args:
        name: Session identifier

    Returns:
        Session object

    Raises:
        FileNotFoundError: If session doesn't exist

    Example:
        >>> session = load_session("rename-api-functions")
        >>> state = session.load_state()
    """
    session_file = SESSIONS_DIR / f"{name}.json"
    if not session_file.exists():
        raise FileNotFoundError(f"Session '{name}' not found")

    return Session(name)


def list_sessions() -> List[str]:
    """
    List all available sessions.

    Returns:
        List of session names

    Example:
        >>> sessions = list_sessions()
        >>> for name in sessions:
        ...     print(f"Session: {name}")
    """
    if not SESSIONS_DIR.exists():
        return []

    return [f.stem for f in SESSIONS_DIR.glob("*.json")]


def delete_session(name: str):
    """
    Delete a session.

    Args:
        name: Session identifier

    Example:
        >>> delete_session("old-refactoring-work")
    """
    session = Session(name)
    session.delete()
