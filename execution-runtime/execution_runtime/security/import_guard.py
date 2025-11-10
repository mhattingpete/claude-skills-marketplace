"""
Lightweight import restrictions for code execution.

Provides import whitelisting without full sandboxing, since Claude Code
already handles resource limits, timeouts, and filesystem restrictions.
"""

from typing import List, Set


class ImportGuard:
    """
    Lightweight import restriction without full sandboxing.

    For Claude Code, this provides an additional layer of import restrictions
    while relying on Claude Code's existing sandbox for resource management.
    """

    # Allowed standard library modules
    ALLOWED_STDLIB_MODULES: Set[str] = {
        're', 'json', 'datetime', 'math', 'collections',
        'itertools', 'functools', 'operator', 'pathlib',
        'typing', 'dataclasses', 'enum', 'copy', 'heapq',
        'bisect', 'array', 'weakref', 'types', 'string',
        'textwrap', 'unicodedata', 'stringprep', 'difflib',
        'hashlib', 'hmac', 'secrets', 'os.path', 'fnmatch',
        'linecache', 'tempfile', 'glob', 'shutil', 'pprint',
        'contextlib', 'abc', 'atexit', 'traceback', 'time',
        'argparse', 'logging', 'platform', 'errno',
        'io', 'codecs', 'ast', 'inspect', 'dis'
    }

    def __init__(self, allowed_patterns: List[str] = None):
        """
        Initialize import guard.

        Args:
            allowed_patterns: Additional allowed import patterns (e.g., ['api.*', 'execution_runtime.*'])
        """
        self.allowed_patterns = allowed_patterns or ['api.*', 'execution_runtime.*']

    def is_allowed(self, module_name: str) -> bool:
        """
        Check if module import is allowed.

        Args:
            module_name: Full module name to check

        Returns:
            True if allowed, False otherwise

        Example:
            >>> guard = ImportGuard()
            >>> guard.is_allowed('json')
            True
            >>> guard.is_allowed('api.filesystem')
            True
            >>> guard.is_allowed('os')  # os is restricted by default
            False
        """
        base_module = module_name.split('.')[0]

        # Check stdlib whitelist
        if base_module in self.ALLOWED_STDLIB_MODULES:
            return True

        # Check if full module name is in stdlib (for os.path, etc.)
        if module_name in self.ALLOWED_STDLIB_MODULES:
            return True

        # Check patterns
        for pattern in self.allowed_patterns:
            if pattern.endswith('.*'):
                # Wildcard pattern like 'api.*'
                prefix = pattern[:-2]
                if module_name.startswith(prefix + '.') or module_name == prefix:
                    return True
            elif pattern == module_name:
                # Exact match
                return True

        return False

    def restrict_import(self, module_name: str):
        """
        Raise ImportError if module not allowed.

        Args:
            module_name: Module name to check

        Raises:
            ImportError: If module not in whitelist

        Example:
            >>> guard = ImportGuard()
            >>> guard.restrict_import('json')  # OK
            >>> guard.restrict_import('os')  # Raises ImportError
            Traceback (most recent call last):
                ...
            ImportError: Import of 'os' not allowed...
        """
        if not self.is_allowed(module_name):
            raise ImportError(
                f"Import of '{module_name}' not allowed. "
                f"Allowed stdlib: {sorted(self.ALLOWED_STDLIB_MODULES)[:10]}... "
                f"and patterns: {self.allowed_patterns}"
            )

    def create_restricted_import(self):
        """
        Create a restricted __import__ function.

        Returns:
            Function that can be used to replace __import__

        Example:
            >>> guard = ImportGuard()
            >>> restricted_import = guard.create_restricted_import()
            >>> # Use in restricted globals:
            >>> globals_dict = {'__import__': restricted_import, ...}
        """
        def restricted_import(name, globals=None, locals=None, fromlist=(), level=0):
            """Restricted import that checks whitelist."""
            self.restrict_import(name)
            return __import__(name, globals, locals, fromlist, level)

        return restricted_import


# Default instance for common use
default_guard = ImportGuard()


def is_import_allowed(module_name: str) -> bool:
    """
    Check if module import is allowed using default guard.

    Args:
        module_name: Module name to check

    Returns:
        True if allowed, False otherwise

    Example:
        >>> is_import_allowed('json')
        True
        >>> is_import_allowed('subprocess')
        False
    """
    return default_guard.is_allowed(module_name)


def restrict_import(module_name: str):
    """
    Raise ImportError if module not allowed (using default guard).

    Args:
        module_name: Module name to check

    Raises:
        ImportError: If module not in whitelist

    Example:
        >>> restrict_import('json')  # OK
        >>> restrict_import('subprocess')  # Raises ImportError
        Traceback (most recent call last):
            ...
        ImportError: Import of 'subprocess' not allowed...
    """
    default_guard.restrict_import(module_name)
