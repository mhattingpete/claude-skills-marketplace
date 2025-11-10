"""
Example: Bulk Refactoring Across Entire Codebase

This example shows how to rename an identifier across all Python files
in a project with maximum efficiency.
"""

from api.code_transform import rename_identifier

# Rename function across all Python files
result = rename_identifier(
    pattern='.',  # Current directory
    old_name='getUserData',
    new_name='fetchUserData',
    file_pattern='**/*.py',  # All Python files recursively
    regex=False  # Exact identifier match
)

# Result contains summary only (not all file contents!)
# Token usage: ~500 tokens total
# vs ~25,000 tokens with traditional approach
print(f"Modified {result['files_modified']} files")
print(f"Total replacements: {result['total_replacements']}")
