import re

# Paths
txt_path = r"C:\Users\Jacob\Documents\Code\PF2E\Tarondor's Guide to the Pathfinder 2e (REMASTERED) Wizard.txt"
md_path = r"C:\Users\Jacob\Documents\Code\PF2E\Tarondor's Guide to the Pathfinder 2e (REMASTERED) Wizard.md"

print("Reading text file...")
with open(txt_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("Converting to Markdown...")

# The file already has good structure, just need to enhance it for Markdown
lines = content.split('\n')
md_lines = []

for line in lines:
    # Convert numbered headings (e.g., "1.2.3. HEADING") to proper Markdown headers
    # Main sections like "1. INTRODUCTION"
    if re.match(r'^\d+\.\s+[A-Z\s]+$', line.strip()):
        md_lines.append(f"# {line.strip()}")
    # Subsections like "1.1. THE COLOR CODE"
    elif re.match(r'^\d+\.\d+\.\s+[A-Z\s]+$', line.strip()):
        md_lines.append(f"## {line.strip()}")
    # Sub-subsections like "1.1.1. SOMETHING"
    elif re.match(r'^\d+\.\d+\.\d+\.\s+[A-Z\s]+$', line.strip()):
        md_lines.append(f"### {line.strip()}")
    # Keep underscores as horizontal rules
    elif line.strip() == '________________':
        md_lines.append('---')
    else:
        md_lines.append(line)

md_content = '\n'.join(md_lines)

print("Writing Markdown file...")
with open(md_path, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"\n✓ SUCCESS!")
print(f"Markdown file created at:")
print(f"  {md_path}")
print(f"Total lines: {len(md_lines)}")

