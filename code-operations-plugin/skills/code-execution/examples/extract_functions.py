"""
Example: Extract Functions to New File

Shows how to find and move functions to a separate file
with minimal token usage.
"""

from api.code_analysis import find_functions
from api.filesystem import copy_lines, paste_code, read_file, write_file

# Find utility functions (returns metadata ONLY, not source code)
functions = find_functions('app.py', pattern='.*_util$', regex=True)

print(f"Found {len(functions)} utility functions")

# Extract imports from original file
content = read_file('app.py')
imports = [line for line in content.splitlines()
           if line.strip().startswith(('import ', 'from '))]

# Create new utils.py with imports
write_file('utils.py', '\\n'.join(set(imports)) + '\\n\\n')

# Copy each function to utils.py
for func in functions:
    print(f"  Moving {func['name']} (lines {func['start_line']}-{func['end_line']})")
    code = copy_lines('app.py', func['start_line'], func['end_line'])
    paste_code('utils.py', -1, code + '\\n\\n')  # -1 = append to end

result = {
    'functions_extracted': len(functions),
    'function_names': [f['name'] for f in functions]
}

# Token usage: ~800 tokens
# vs ~15,000 tokens reading full file into context
