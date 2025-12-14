import json
import csv

# Read the new JSON file
print("Reading new spells JSON...")
with open(r'C:\Users\Jacob\Downloads\spells-sublist-data(1).json', 'r', encoding='utf-8') as f:
    new_spells = json.load(f)

# Path to existing CSV
csv_path = r'C:\Users\Jacob\Documents\Code\PF2E\Spellbook\spells-sublist-data.csv'

# Define all possible fieldnames (same as before)
fieldnames = [
    'learn-source', 'name', 'source', 'remaster', 'page', 'level',
    'traits', 'traditions', 'spellLists', 'cast', 'components',
    'range', 'targets', 'area', 'duration', 'savingThrow',
    'entries', 'heightened', 'activity', 'miscTags', 'trigger', 'type'
]

# Read existing CSV rows
print("Reading existing CSV...")
existing_rows = []
existing_spells = set()

with open(csv_path, 'r', encoding='utf-8', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        existing_rows.append(row)
        existing_spells.add(row['name'])

print(f"Found {len(existing_rows)} existing spells")

# Prepare new rows to add
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

    existing_rows.append(row)
    added_count += 1
    print(f"Added: {spell['name']}")

# Write all rows back to CSV
print("\nWriting updated CSV...")
with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(existing_rows)

print(f"\nSummary:")
print(f"Total spells in new file: {len(new_spells)}")
print(f"Added to CSV: {added_count}")
print(f"Skipped (duplicates): {skipped_count}")
print(f"Total spells in CSV now: {len(existing_rows)}")

