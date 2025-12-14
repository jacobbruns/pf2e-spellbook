import json
import csv
import os

# Read the new JSON file
print("Reading new spells JSON...")
json_path = r'C:\Users\Jacob\Downloads\spells-sublist-data(1).json'
with open(json_path, 'r', encoding='utf-8') as f:
    new_spells = json.load(f)

# Paths
original_csv = r'C:\Users\Jacob\Documents\Code\PF2E\Spellbook\spells-sublist-data.csv'
output_csv = r'C:\Users\Jacob\Documents\Code\PF2E\Spellbook\spells-sublist-data-updated.csv'

# Define all possible fieldnames
fieldnames = [
    'learn-source', 'name', 'source', 'remaster', 'page', 'level',
    'traits', 'traditions', 'spellLists', 'cast', 'components',
    'range', 'targets', 'area', 'duration', 'savingThrow',
    'entries', 'heightened', 'activity', 'miscTags', 'trigger', 'type'
]

# Read existing CSV
print("Reading existing CSV...")
existing_rows = []
existing_spells = set()

with open(original_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        existing_rows.append(dict(row))  # Convert to regular dict
        existing_spells.add(row['name'])

print(f"Found {len(existing_rows)} existing spells")

# Add new spells
added_count = 0
skipped_count = 0

for spell in new_spells:
    if spell['name'] in existing_spells:
        print(f"Skipping duplicate: {spell['name']}")
        skipped_count += 1
        continue
    
    # Create new row
    row = {'learn-source': 'class'}
    for key, value in spell.items():
        if isinstance(value, (list, dict)):
            row[key] = json.dumps(value, ensure_ascii=False)
        else:
            row[key] = value
    
    existing_rows.append(row)
    added_count += 1
    print(f"Added: {spell['name']}")

# Write to NEW file
print(f"\nWriting {len(existing_rows)} total spells to new file...")
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    for row in existing_rows:
        writer.writerow(row)

print(f"\n✓ Success!")
print(f"Summary:")
print(f"  Total spells in new JSON: {len(new_spells)}")
print(f"  Added to CSV: {added_count}")
print(f"  Skipped (duplicates): {skipped_count}")
print(f"  Total spells in new CSV: {len(existing_rows)}")
print(f"\nNew file created at:")
print(f"  {output_csv}")
print(f"\nPlease review the new file, then you can:")
print(f"  1. Delete the old file: {original_csv}")
print(f"  2. Rename the new file to: spells-sublist-data.csv")

