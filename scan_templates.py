import os
import re

template_dir = 'templates'
output_file = 'scan_results.txt'

print(f"Scanning {template_dir} for split template tags...")

with open(output_file, 'w', encoding='utf-8') as out:
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    for i, line in enumerate(lines):
                        if '{{' in line and '}}' not in line:
                            out.write(f"File: {path}\n")
                            out.write(f"  Line {i+1}: {line.strip()}\n")
                            if i + 1 < len(lines):
                                out.write(f"    Next: {lines[i+1].strip()}\n")
                            out.write("\n")
                        elif '{%' in line and '%}' not in line:
                             # Check for multi-line block tags too (like the if tag earlier)
                            # But ignore blocktrans or acceptable multi-line tags if any
                            # Generally safe to flag for review
                            out.write(f"File: {path} (Block Tag Split)\n")
                            out.write(f"  Line {i+1}: {line.strip()}\n")
                            if i + 1 < len(lines):
                                out.write(f"    Next: {lines[i+1].strip()}\n")
                            out.write("\n")

                except Exception as e:
                    out.write(f"Error reading {path}: {e}\n")

print(f"Scan complete. Results written to {output_file}")
