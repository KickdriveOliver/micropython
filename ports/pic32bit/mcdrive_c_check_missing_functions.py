import re

# Read the contents of targetlib.c and mcdrive.c
with open('../../../IEC61800/targetlib.c', 'r') as f:
    targetlib_content = f.read()

with open('mcdrive.c', 'r') as f:
    mcdrive_content = f.read()

# Extract function names using regular expressions
targetlib_functions = re.findall(r'Lib_\w+\(', targetlib_content)
mcdrive_functions = re.findall(r'Lib_\w+\(', mcdrive_content)

# Find functions mentioned in both files
common_functions = set(targetlib_functions) & set(mcdrive_functions)

# Find functions mentioned only in targetlib.c
targetlib_only_functions = set(targetlib_functions) - common_functions

print("Functions mentioned both in targetlib.c and mcdrive.c:")
print(common_functions)

print("\nFunctions mentioned only in targetlib.c:")
print(targetlib_only_functions)