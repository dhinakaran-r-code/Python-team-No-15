import os
import re

template_dir = 'templates'
pattern = re.compile(r'\{\{[^}]*\n')

print("Scanning for split template tags...")
for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = pattern.findall(content)
                if matches:
                    print(f"File: {path}")
                    lines = content.splitlines()
                    for i, line in enumerate(lines):
                        if '{{' in line and '}}' not in line:
                            # Verify if it closes on next line(s) - simple check
                            if i + 1 < len(lines) and '}}' in lines[i+1]:
                                print(f"  Line {i+1}: {line.strip()} ... {lines[i+1].strip()}")
                            else:
                                # Might be multi-line
                                print(f"  Line {i+1}: {line.strip()} (Partial Match)")
