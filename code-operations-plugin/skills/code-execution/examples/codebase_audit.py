"""
Example: Comprehensive Codebase Audit

Analyze code quality across entire project with minimal tokens.
"""

from api.code_analysis import analyze_dependencies, find_unused_imports
from pathlib import Path

# Find all Python files
files = list(Path('.').glob('**/*.py'))
print(f"Analyzing {len(files)} files...")

issues = {
    'high_complexity': [],
    'unused_imports': [],
    'large_files': [],
    'no_docstrings': []
}

# Analyze each file (metadata only, not source!)
for file in files:
    file_str = str(file)

    # Get complexity metrics
    deps = analyze_dependencies(file_str)

    # Flag high complexity
    if deps.get('complexity', 0) > 15:
        issues['high_complexity'].append({
            'file': file_str,
            'complexity': deps['complexity'],
            'functions': deps['functions'],
            'avg_complexity': deps.get('avg_complexity_per_function', 0)
        })

    # Flag large files
    if deps.get('lines', 0) > 500:
        issues['large_files'].append({
            'file': file_str,
            'lines': deps['lines'],
            'functions': deps['functions']
        })

    # Find unused imports
    unused = find_unused_imports(file_str)
    if unused:
        issues['unused_imports'].append({
            'file': file_str,
            'count': len(unused),
            'imports': unused
        })

# Return summary (NOT all the data!)
result = {
    'files_audited': len(files),
    'total_lines': sum(d.get('lines', 0) for d in [analyze_dependencies(str(f)) for f in files]),
    'issues': {
        'high_complexity': len(issues['high_complexity']),
        'unused_imports': len(issues['unused_imports']),
        'large_files': len(issues['large_files'])
    },
    'top_complexity_issues': sorted(
        issues['high_complexity'],
        key=lambda x: x['complexity'],
        reverse=True
    )[:5]  # Only top 5
}

print(f"\\nAudit complete:")
print(f"  High complexity files: {result['issues']['high_complexity']}")
print(f"  Files with unused imports: {result['issues']['unused_imports']}")
print(f"  Large files (>500 lines): {result['issues']['large_files']}")

# Token usage: ~2,000 tokens for 100 files
# vs ~150,000 tokens loading all files into context
