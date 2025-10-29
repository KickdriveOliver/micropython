#!/usr/bin/env python3
"""pic32bit-make-qstr-port.py
oliver.heggelbacher@kfullmo.de 
Custom QSTR generation for MPLAB X projects which add custom Python objects 
(e.g. MovingCap mcdrive) 

This script creates an additional file "qstrdefs.port.generated.h" and inserts a related
#include in the precompiled "qstrdefs.generated.h"
"""

import sys
import os
import re
import argparse
import hashlib
from pathlib import Path

# Configuration - matches MicroPython's default settings
BYTES_IN_HASH = 2  # MICROPY_QSTR_BYTES_IN_HASH
BYTES_IN_LEN = 1   # MICROPY_QSTR_BYTES_IN_LEN

# Character escape mapping for C identifiers (from makeqstrdata.py)
CODEPOINT_TO_NAME = {
    ord(" "): "space",
    ord("!"): "exclam",
    ord('"'): "quot",
    ord("#"): "hash",
    ord("$"): "dollar",
    ord("%"): "percent",
    ord("&"): "ampersand",
    ord("'"): "squot",
    ord("("): "paren_open",
    ord(")"): "paren_close",
    ord("*"): "star",
    ord("+"): "plus",
    ord(","): "comma",
    ord("-"): "minus",
    ord("."): "dot",
    ord("/"): "slash",
    ord(":"): "colon",
    ord(";"): "semicolon",
    ord("<"): "less",
    ord("="): "equals",
    ord(">"): "greater",
    ord("?"): "question",
    ord("@"): "at",
    ord("["): "bracket_open",
    ord("\\"): "backslash",
    ord("]"): "bracket_close",
    ord("^"): "caret",
    ord("`"): "backtick",
    ord("{"): "brace_open",
    ord("|"): "bar",
    ord("}"): "brace_close",
    ord("~"): "tilde",
}

def qstr_escape(qstr_text):
    """Escapes a string to make it a valid C identifier."""
    def esc_char(match):
        char_ord = ord(match.group(0))
        try:
            return "_" + CODEPOINT_TO_NAME[char_ord] + "_"
        except KeyError:
            return "_0x%02x_" % char_ord

    # Handle empty string
    if not qstr_text:
        return ""
    
    # Escape characters that are not valid in C identifiers
    escaped = re.sub(r"[^A-Za-z0-9_]", esc_char, qstr_text)
    
    # Ensure it doesn't start with a digit
    if escaped and escaped[0].isdigit():
        escaped = "_" + escaped
        
    return escaped

def compute_hash(qstr_bytes, bytes_hash):
    """
    Computes the hash of a q-string, matching MicroPython's C implementation.
    This mirrors the djb2 hash algorithm used in qstr.c
    """
    # djb2 algorithm from qstr.c: hash = ((hash << 5) + hash) ^ (*data)
    hash_val = 5381
    for byte in qstr_bytes:
        hash_val = ((hash_val << 5) + hash_val) ^ byte
    
    # Apply mask for the specified number of bytes
    mask = (1 << (8 * bytes_hash)) - 1
    hash_val = hash_val & mask
    
    # Make sure that valid hash is never zero, zero means "hash not computed"
    if hash_val == 0:
        hash_val = 1
        
    return hash_val

def extract_qstrs_from_content(content):
    """Extracts all QSTR references from file content."""
    qstrs = set()
    
    # Pattern 1: Q(string_literal) - direct qstr definitions
    q_pattern = r'Q\(([^)]+)\)'
    for match in re.finditer(q_pattern, content):
        qstr_content = match.group(1).strip()
        # Remove quotes if present
        if qstr_content.startswith('"') and qstr_content.endswith('"'):
            qstr_content = qstr_content[1:-1]
        # Handle escape sequences
        qstr_content = qstr_content.encode().decode('unicode_escape')
        qstrs.add(qstr_content)
    
    # Pattern 2: MP_QSTR_identifier - macro references
    mp_qstr_pattern = r'MP_QSTR_([a-zA-Z_][a-zA-Z0-9_]*)'
    for match in re.finditer(mp_qstr_pattern, content):
        qstrs.add(match.group(1))
    
    # Pattern 3: mp_load_name(MP_QSTR_...) and similar function calls
    load_pattern = r'mp_load_\w+\(MP_QSTR_([a-zA-Z_][a-zA-Z0-9_]*)\)'
    for match in re.finditer(load_pattern, content):
        qstrs.add(match.group(1))
    
    return qstrs

def process_input_files(input_files):
    """Processes specified input files to extract QSTRs."""
    all_qstrs = set()
    
    for file_path in input_files:
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"Warning: File not found: {file_path}")
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                file_qstrs = extract_qstrs_from_content(content)
                all_qstrs.update(file_qstrs)
        except Exception as e:
            print(f"Warning: Error reading {file_path}: {e}")
    
    return all_qstrs

def generate_qstrdefs_generated_port(output_dir, all_qstrs):
    """Generates qstrdefs.port.generated.h, avoiding unnecessary writes."""
    output_path = Path(output_dir) / 'qstrdefs.port.generated.h'
    tmp_output_path = output_path.with_suffix('.h.tmp')

    print(f"Generating {output_path}...")

    # Sort QSTRs using MicroPython's specific ordering rules
    def qstr_sort_key(qstr_text):
        """Custom sort key that matches MicroPython's QSTR ordering."""
        if qstr_text == "":
            return (-200000, "")
        elif qstr_text == "__dir__":
            return (-190000, "__dir__")
        elif qstr_text.startswith("__") and qstr_text.endswith("__"):
            return (-100000, qstr_text)
        else:
            return (0, qstr_text)

    sorted_qstrs = sorted(all_qstrs, key=qstr_sort_key)

    # Generate the new content in a temporary file
    with open(tmp_output_path, 'w', encoding='utf-8') as f:
        f.write("// This file was automatically generated by pic32bit-make-qstr-port.py\n\n")
        f.write('QDEF(MP_QSTR_NULL, (const byte*)"\\x00\\x00\\x00" "")\n')

        for qstr_text in sorted_qstrs:
            qstr_bytes = qstr_text.encode('utf-8')
            qstr_hash = compute_hash(qstr_bytes, BYTES_IN_HASH)
            qstr_len = len(qstr_bytes)

            hash_bytes = [(qstr_hash >> (8 * i)) & 0xff for i in range(BYTES_IN_HASH)]
            len_bytes = [(qstr_len >> (8 * i)) & 0xff for i in range(BYTES_IN_LEN)]

            hash_str = ''.join(f'\\x{b:02x}' for b in hash_bytes)
            len_str = ''.join(f'\\x{b:02x}' for b in len_bytes)

            c_escaped = qstr_text.replace('\\', '\\\\').replace('"', '\\"')

            qstr_id = qstr_escape(qstr_text)
            if not qstr_id:
                qstr_id = ""

            f.write(f'QDEF(MP_QSTR_{qstr_id}, (const byte*)"{hash_str}{len_str}" "{c_escaped}")\n')

    # Check if the new file is different from the existing one
    new_content_same = False
    if output_path.exists():
        try:
            with open(output_path, 'r', encoding='utf-8') as f_orig, \
                 open(tmp_output_path, 'r', encoding='utf-8') as f_new:
                if f_orig.read() == f_new.read():
                    new_content_same = True
        except Exception as e:
            print(f"Warning: Could not compare files: {e}")

    if new_content_same:
        print(f"No changes detected in {output_path}. File not updated.")
        tmp_output_path.unlink()  # Remove the temporary file
    else:
        print(f"Updating {output_path} with {len(sorted_qstrs) + 1} QSTRs.")
        tmp_output_path.replace(output_path)  # Replace original with new file

def update_qstrdefs_generated(output_dir):
    """Updates qstrdefs.generated.h, avoiding unnecessary writes."""
    generated_path = Path(output_dir) / 'qstrdefs.generated.h'
    tmp_generated_path = generated_path.with_suffix('.h.tmp')
    port_generated_path = Path(output_dir) / 'qstrdefs.port.generated.h'

    if not generated_path.exists():
        print(f"Error: {generated_path} does not exist. Skipping update.")
        return

    if not port_generated_path.exists():
        print(f"Error: {port_generated_path} does not exist. Skipping update.")
        return

    # Read the QSTR definitions from the port-generated file
    with open(port_generated_path, 'r', encoding='utf-8') as f:
        port_qstr_lines = {line.strip() for line in f if line.startswith('QDEF(')}

    # Process the original file and write the modified content to a temporary file
    with open(generated_path, 'r', encoding='utf-8') as f_orig, \
         open(tmp_generated_path, 'w', encoding='utf-8') as f_new:

        original_content = f_orig.readlines()
        new_content = []

        # Check if the include line is already present
        include_line = '#include "qstrdefs.port.generated.h"\n'
        if include_line not in original_content:
            new_content.extend([
                "// This file was automatically modified by pic32bit-make-qstr-port.py\n",
                include_line,
                "\n"
            ])

        # Process each line for potential modifications
        for line in original_content:
            # Comment out duplicate QSTR definitions
            if line.startswith('QDEF(') and line.strip() in port_qstr_lines:
                new_content.append(f'// in qstrdefs.port.generated.h: {line}')
            # Undo previous commenting if QSTR is no longer a duplicate
            elif line.startswith('// in qstrdefs.port.generated.h: QDEF('):
                original_line = line.replace('// in qstrdefs.port.generated.h: ', '')
                if original_line.strip() not in port_qstr_lines:
                    new_content.append(original_line)
                else:
                    new_content.append(line) # Keep it commented
            else:
                new_content.append(line)

        f_new.writelines(new_content)

    # Compare the temporary file with the original file
    new_content_same = False
    try:
        with open(generated_path, 'r', encoding='utf-8') as f_orig, \
             open(tmp_generated_path, 'r', encoding='utf-8') as f_new:
            if f_orig.read() == f_new.read():
                new_content_same = True
    except Exception as e:
        print(f"Warning: Could not compare files: {e}")

    if new_content_same:
        print(f"No changes detected in {generated_path}. File not updated.")
        tmp_generated_path.unlink()
    else:
        print(f"Updating {generated_path} to include port QSTRs and handle duplicates.")
        tmp_generated_path.replace(generated_path)

def main():
    parser = argparse.ArgumentParser(
        description="Generate QSTR files for MicroPython MPLAB X projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pic32bit-make-qstr-port.py --input_files mpconfigport.h mccom.c mcdrive.c --output_dir ./build/genhdr
        """
    )
    
    parser.add_argument('--input_files', nargs='+', required=True,
                       help="List of input files to process for QSTRs")
    parser.add_argument('--output_dir', required=True,
                       help="Directory to place the generated QSTR files")
    parser.add_argument('--verbose', '-v', action='store_true',
                       help="Enable verbose output")
    
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir).resolve()
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=== MicroPython QSTR Generation for MPLAB X ===")
    print(f"Output directory: {output_dir}")
    
    try:
        # Step 1: Process input files to extract QSTRs
        all_qstrs = process_input_files(args.input_files)
        
        if args.verbose:
            print(f"\nQSTR Summary:")
            print(f"  Total unique QSTRs: {len(all_qstrs)}")
        
        # Step 2: Generate qstrdefs.port.generated.h
        generate_qstrdefs_generated_port(output_dir, all_qstrs)
        
        # Step 3: Update qstrdefs.generated.h
        update_qstrdefs_generated(output_dir)
        
        print("\n=== QSTR Generation Complete ===")
        print(f"Generated files in: {output_dir}")
        print("  - qstrdefs.port.generated.h")
        
    except Exception as e:
        print(f"Error during QSTR generation: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()