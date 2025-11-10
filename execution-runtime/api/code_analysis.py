"""
Code Analysis API

AST-based code analysis that returns metadata, not full source code.
Massive token savings by avoiding loading full files into context.
"""

import ast
import re
from pathlib import Path
from typing import List, Dict, Optional, Set


def find_functions(
    file_path: str,
    pattern: Optional[str] = None,
    regex: bool = False
) -> List[Dict]:
    """
    Find functions in file, return metadata only (not source code).

    Args:
        file_path: Path to Python file
        pattern: Optional name pattern to filter
        regex: Treat pattern as regex

    Returns:
        List of dicts with function metadata:
        - name: Function name
        - start_line: Starting line number
        - end_line: Ending line number
        - args: List of argument names
        - decorators: List of decorator names
        - docstring: First line of docstring (if any)
        - is_async: Boolean indicating if async function
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read(), filename=file_path)
        except SyntaxError:
            return []

    functions = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_info = {
                'name': node.name,
                'start_line': node.lineno,
                'end_line': node.end_lineno,
                'args': [arg.arg for arg in node.args.args],
                'decorators': _extract_decorators(node),
                'docstring': ast.get_docstring(node, clean=True)[:100] if ast.get_docstring(node) else None,
                'is_async': isinstance(node, ast.AsyncFunctionDef)
            }

            # Filter by pattern if provided
            if pattern:
                if regex:
                    if not re.search(pattern, func_info['name']):
                        continue
                else:
                    if pattern not in func_info['name']:
                        continue

            functions.append(func_info)

    return functions


def find_classes(
    file_path: str,
    pattern: Optional[str] = None
) -> List[Dict]:
    """
    Find classes in file, return metadata only.

    Args:
        file_path: Path to Python file
        pattern: Optional name pattern to filter

    Returns:
        List of dicts with class metadata:
        - name: Class name
        - start_line: Starting line
        - end_line: Ending line
        - bases: List of base class names
        - methods: List of method names
        - docstring: First line of docstring
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read(), filename=file_path)
        except SyntaxError:
            return []

    classes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Get method names
            methods = [
                n.name for n in node.body
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]

            # Get base classes
            bases = []
            for base in node.bases:
                if isinstance(base, ast.Name):
                    bases.append(base.id)
                elif isinstance(base, ast.Attribute):
                    bases.append(f"{base.value.id}.{base.attr}")

            class_info = {
                'name': node.name,
                'start_line': node.lineno,
                'end_line': node.end_lineno,
                'bases': bases,
                'methods': methods,
                'docstring': ast.get_docstring(node, clean=True)[:100] if ast.get_docstring(node) else None
            }

            # Filter by pattern
            if pattern and pattern not in class_info['name']:
                continue

            classes.append(class_info)

    return classes


def extract_imports(file_path: str) -> Dict[str, List[str]]:
    """
    Extract all imports from file.

    Args:
        file_path: Path to Python file

    Returns:
        Dict with:
        - 'imports': List of 'import X' statements
        - 'from_imports': List of 'from X import Y' statements
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read(), filename=file_path)
        except SyntaxError:
            return {'imports': [], 'from_imports': []}

    imports = []
    from_imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name if alias.asname is None else f"{alias.name} as {alias.asname}")

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                from_imports.append(f"from {module} import {alias.name}")

    return {
        'imports': imports,
        'from_imports': from_imports
    }


def get_function_calls(
    file_path: str,
    function_name: str
) -> List[Dict]:
    """
    Find all calls to a specific function in file.

    Args:
        file_path: Path to Python file
        function_name: Name of function to find calls to

    Returns:
        List of dicts with:
        - line: Line number of call
        - context: Name of containing function/class
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read(), filename=file_path)
        except SyntaxError:
            return []

    calls = []
    current_context = None

    class CallVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            nonlocal current_context
            prev_context = current_context
            current_context = node.name
            self.generic_visit(node)
            current_context = prev_context

        def visit_ClassDef(self, node):
            nonlocal current_context
            prev_context = current_context
            current_context = node.name
            self.generic_visit(node)
            current_context = prev_context

        def visit_Call(self, node):
            # Check if this is a call to our target function
            if isinstance(node.func, ast.Name) and node.func.id == function_name:
                calls.append({
                    'line': node.lineno,
                    'context': current_context or '<module>'
                })
            elif isinstance(node.func, ast.Attribute) and node.func.attr == function_name:
                calls.append({
                    'line': node.lineno,
                    'context': current_context or '<module>'
                })
            self.generic_visit(node)

    visitor = CallVisitor()
    visitor.visit(tree)

    return calls


def analyze_dependencies(file_path: str) -> Dict[str, any]:
    """
    Analyze file dependencies and complexity.

    Args:
        file_path: Path to Python file

    Returns:
        Dict with:
        - imports: Number of imports
        - functions: Number of functions
        - classes: Number of classes
        - lines: Total lines
        - complexity: Estimated complexity score
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.splitlines()

    try:
        tree = ast.parse(content, filename=file_path)
    except SyntaxError:
        return {
            'error': 'Syntax error in file',
            'lines': len(lines)
        }

    # Count different elements
    imports = sum(1 for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom)))
    functions = sum(1 for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)))
    classes = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))

    # Simple complexity score based on control flow
    complexity = 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.ExceptHandler)):
            complexity += 1

    return {
        'imports': imports,
        'functions': functions,
        'classes': classes,
        'lines': len(lines),
        'complexity': complexity,
        'avg_complexity_per_function': round(complexity / functions, 2) if functions > 0 else 0
    }


def find_unused_imports(file_path: str) -> List[str]:
    """
    Find potentially unused imports in file.

    Args:
        file_path: Path to Python file

    Returns:
        List of unused import names
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        tree = ast.parse(content, filename=file_path)
    except SyntaxError:
        return []

    # Collect all imported names
    imported_names: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_names.add(alias.asname if alias.asname else alias.name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imported_names.add(alias.asname if alias.asname else alias.name)

    # Collect all used names
    used_names: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used_names.add(node.id)
        elif isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name):
                used_names.add(node.value.id)

    # Find potentially unused (simple heuristic)
    unused = imported_names - used_names

    return sorted(list(unused))


def _extract_decorators(node: ast.FunctionDef) -> List[str]:
    """Extract decorator names from function node."""
    decorators = []
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Name):
            decorators.append(decorator.id)
        elif isinstance(decorator, ast.Attribute):
            decorators.append(decorator.attr)
        elif isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name):
                decorators.append(decorator.func.id)
            elif isinstance(decorator.func, ast.Attribute):
                decorators.append(decorator.func.attr)
    return decorators
