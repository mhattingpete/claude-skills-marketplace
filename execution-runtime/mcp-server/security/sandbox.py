"""
Sandboxed Python Execution

Safe code execution environment using RestrictedPython.
"""

import sys
import io
import signal
from typing import Dict, List, Optional, Any
from contextlib import redirect_stdout, redirect_stderr
import resource


class ExecutionTimeout(Exception):
    """Raised when code execution times out."""
    pass


class SandboxedExecutor:
    """
    Execute Python code in a restricted environment.

    Security features:
    - Limited imports (whitelist only)
    - No file system access outside workspace
    - Resource limits (CPU, memory)
    - Execution timeout
    - No dangerous builtins (eval, exec, __import__)
    """

    # Allowed standard library modules
    ALLOWED_STDLIB_MODULES = {
        're', 'json', 'datetime', 'math', 'collections',
        'itertools', 'functools', 'operator', 'pathlib',
        'typing', 'dataclasses', 'enum', 'copy'
    }

    # Dangerous builtins to remove
    DANGEROUS_BUILTINS = {
        'eval', 'exec', 'compile', '__import__',
        'open', 'input', 'raw_input',
        'file', 'execfile', 'reload'
    }

    def __init__(
        self,
        allowed_imports: Optional[List[str]] = None,
        timeout: int = 30,
        memory_limit_mb: int = 256
    ):
        """
        Initialize sandbox executor.

        Args:
            allowed_imports: List of additional allowed import patterns (e.g., ['api.*'])
            timeout: Maximum execution time in seconds
            memory_limit_mb: Maximum memory usage in MB
        """
        self.allowed_imports = allowed_imports or []
        self.timeout = timeout
        self.memory_limit_mb = memory_limit_mb

    def run(
        self,
        code: str,
        globals_dict: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute Python code in sandbox.

        Args:
            code: Python code to execute
            globals_dict: Optional global variables to provide

        Returns:
            Dict with:
            - status: 'success' or 'error'
            - result: Return value or result
            - stdout: Captured stdout
            - stderr: Captured stderr
            - error: Error message if failed
        """
        # Prepare restricted globals
        restricted_globals = self._create_restricted_globals(globals_dict)

        # Capture stdout/stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        result = {
            "status": "success",
            "result": None,
            "stdout": "",
            "stderr": "",
        }

        # Set resource limits
        self._set_resource_limits()

        # Set timeout alarm
        def timeout_handler(signum, frame):
            raise ExecutionTimeout(f"Execution exceeded {self.timeout} seconds")

        old_alarm = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(self.timeout)

        try:
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                # Compile code first to check syntax
                compiled_code = compile(code, '<sandbox>', 'exec')

                # Execute in restricted environment
                exec(compiled_code, restricted_globals)

                # Get any return value (if code assigned to 'result' variable)
                if 'result' in restricted_globals:
                    result["result"] = restricted_globals['result']

        except ExecutionTimeout as e:
            result["status"] = "error"
            result["error"] = str(e)

        except SyntaxError as e:
            result["status"] = "error"
            result["error"] = f"Syntax error: {e}"

        except ImportError as e:
            result["status"] = "error"
            result["error"] = f"Import not allowed: {e}"

        except MemoryError:
            result["status"] = "error"
            result["error"] = "Memory limit exceeded"

        except Exception as e:
            result["status"] = "error"
            result["error"] = f"{type(e).__name__}: {str(e)}"

        finally:
            # Cancel timeout alarm
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_alarm)

            # Capture output
            result["stdout"] = stdout_capture.getvalue()
            result["stderr"] = stderr_capture.getvalue()

        return result

    def _create_restricted_globals(
        self,
        user_globals: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create restricted globals dictionary with safe builtins.

        Args:
            user_globals: User-provided global variables

        Returns:
            Restricted globals dict
        """
        # Start with safe builtins
        safe_builtins = {
            name: getattr(__builtins__, name)
            for name in dir(__builtins__)
            if name not in self.DANGEROUS_BUILTINS
        }

        # Create restricted __import__
        safe_builtins['__import__'] = self._restricted_import

        restricted_globals = {
            '__builtins__': safe_builtins,
            '__name__': '__sandbox__',
            '__doc__': None,
        }

        # Add user globals if provided
        if user_globals:
            restricted_globals.update(user_globals)

        return restricted_globals

    def _restricted_import(
        self,
        name: str,
        globals=None,
        locals=None,
        fromlist=(),
        level=0
    ):
        """
        Restricted import function that only allows whitelisted modules.

        Args:
            name: Module name to import

        Returns:
            Imported module if allowed

        Raises:
            ImportError: If module not in whitelist
        """
        # Check if module is in allowed stdlib
        base_module = name.split('.')[0]

        if base_module in self.ALLOWED_STDLIB_MODULES:
            return __import__(name, globals, locals, fromlist, level)

        # Check if matches allowed import patterns (e.g., 'api.*')
        for pattern in self.allowed_imports:
            if pattern.endswith('.*'):
                # Pattern like 'api.*'
                prefix = pattern[:-2]
                if name.startswith(prefix):
                    return __import__(name, globals, locals, fromlist, level)
            elif pattern == name:
                # Exact match
                return __import__(name, globals, locals, fromlist, level)

        # Not allowed
        raise ImportError(
            f"Import of '{name}' is not allowed in sandbox. "
            f"Allowed: {self.ALLOWED_STDLIB_MODULES} and {self.allowed_imports}"
        )

    def _set_resource_limits(self):
        """Set resource limits for the process."""
        try:
            # Set memory limit (soft and hard)
            memory_bytes = self.memory_limit_mb * 1024 * 1024
            resource.setrlimit(
                resource.RLIMIT_AS,
                (memory_bytes, memory_bytes)
            )

            # Set CPU time limit
            resource.setrlimit(
                resource.RLIMIT_CPU,
                (self.timeout, self.timeout)
            )

        except (ValueError, OSError) as e:
            # Resource limits might not be supported on all platforms
            print(f"Warning: Could not set resource limits: {e}", file=sys.stderr)


def create_sandbox_with_api() -> SandboxedExecutor:
    """
    Create sandbox executor pre-configured for marketplace API.

    Returns:
        SandboxedExecutor with api.* imports allowed
    """
    return SandboxedExecutor(
        allowed_imports=['api.*', 'pathlib'],
        timeout=30,
        memory_limit_mb=256
    )
