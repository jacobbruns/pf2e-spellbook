import json
import csv

# Read both JSON files
print("Reading threshold spells...")
with open(r'C:\Users\Jacob\Downloads\spells-sublist-data.json', 'r', encoding='utf-8') as f:
    threshold_spells = json.load(f)

print("Reading class spells...")
with open(r'C:\Users\Jacob\Downloads\spells-sublist-data(1).json', 'r', encoding='utf-8') as f:
    class_spells = json.load(f)

# Output path
output_csv = r'C:\Users\Jacob\Documents\Code\PF2E\Spellbook\spells-combined.csv'

# Define fieldnames
fieldnames = [
    'learn-source', 'name', 'source', 'remaster', 'page', 'level',
    'traits', 'traditions', 'spellLists', 'cast', 'components',
    'range', 'targets', 'area', 'duration', 'savingThrow',
    'entries', 'heightened', 'activity', 'miscTags', 'trigger', 'type'
]

# Collect all spells
all_rows = []
spell_names = set()

# Add threshold spells
for spell in threshold_spells:
    if spell['name'] in spell_names:
        continue
    row = {'learn-source': 'thresholds'}
    for key, value in spell.items():
        if isinstance(value, (list, dict)):
            row[key] = json.dumps(value, ensure_ascii=False)
        else:
            row[key] = value
    all_rows.append(row)
    spell_names.add(spell['name'])
    print(f"Added (thresholds): {spell['name']}")

# Add class spells
for spell in class_spells:
    if spell['name'] in spell_names:
        print(f"Skipping duplicate: {spell['name']}")
        continue
    row = {'learn-source': 'class'}
    for key, value in spell.items():
        if isinstance(value, (list, dict)):
            row[key] = json.dumps(value, ensure_ascii=False)
        else:
            row[key] = value
    all_rows.append(row)
    spell_names.add(spell['name'])
    print(f"Added (class): {spell['name']}")

# Write CSV
print(f"\nWriting {len(all_rows)} spells to CSV...")
try:
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"✓ Success! File created at: {output_csv}")
    print(f"Total spells: {len(all_rows)}")
except Exception as e:
    print(f"✗ Error writing file: {e}")

