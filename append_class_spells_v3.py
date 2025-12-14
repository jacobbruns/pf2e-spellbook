import json
import csv

# Read the new JSON file
print("Reading new spells JSON...")
with open(r'C:\Users\Jacob\Downloads\spells-sublist-data(1).json', 'r', encoding='utf-8') as f:
    new_spells = json.load(f)

# Path to existing CSV
csv_path = r'C:\Users\Jacob\Documents\Code\PF2E\Spellbook\spells-sublist-data.csv'

# Define all possible fieldnames
fieldnames = [
    'learn-source', 'name', 'source', 'remaster', 'page', 'level',
    'traits', 'traditions', 'spellLists', 'cast', 'components',
    'range', 'targets', 'area', 'duration', 'savingThrow',
    'entries', 'heightened', 'activity', 'miscTags', 'trigger', 'type'
]

# Read existing spell names to check for duplicates
print("Reading existing CSV...")
existing_spells = set()
with open(csv_path, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        existing_spells.add(row['name'])

print(f"Found {len(existing_spells)} existing spells")

# Prepare new rows to add
rows_to_add = []
added_count = 0
skipped_count = 0

for spell in new_spells:
    # Skip if spell already exists
    if spell['name'] in existing_spells:
        print(f"Skipping duplicate: {spell['name']}")
        skipped_count += 1
        continue
    
    # Flatten complex fields to strings
    row = {'learn-source': 'class'}  # Set learn-source to 'class'
    for key, value in spell.items():
        if isinstance(value, (list, dict)):
            row[key] = json.dumps(value, ensure_ascii=False)
        else:
            row[key] = value
    
    rows_to_add.append(row)
    added_count += 1
    print(f"Will add: {spell['name']}")

# Append new spells to CSV (one at a time to avoid file descriptor issues)
if rows_to_add:
    print(f"\nAppending {len(rows_to_add)} new spells...")
    for i, row in enumerate(rows_to_add, 1):
        with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
            writer.writerow(row)
        print(f"  [{i}/{len(rows_to_add)}] Appended: {row['name']}")

print(f"\nSummary:")
print(f"Total spells in new file: {len(new_spells)}")
print(f"Added to CSV: {added_count}")
print(f"Skipped (duplicates): {skipped_count}")
print(f"Total spells in CSV now: {len(existing_spells) + added_count}")

