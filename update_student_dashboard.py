import os

file_path = 'templates/student_dashboard.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Target string from the file view (lines 16-17)
target = """<span class="badge bg-secondary mb-2">{{ student_profile.get_department_display }} {{
                student_profile.year|ordinal }} Year</span>"""

replacement = """<span class="badge bg-soft-primary text-primary border border-primary mb-2">Student - {{ student_profile.get_department_display }} {{ student_profile.year|ordinal }} Year</span>"""

new_content = content.replace(target, replacement)

if target not in content:
    print("Target not found! Dumping content around line 16:")
    lines = content.splitlines()
    for i in range(10, 20):
        if i < len(lines):
            print(f"{i+1}: {lines[i]}")
else:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully updated student_dashboard.html")
