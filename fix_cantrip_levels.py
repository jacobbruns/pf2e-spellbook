import csv
import json

# Path to CSV
csv_path = r'C:\Users\Jacob\Documents\Code\PF2E\Spellbook\spells-sublist-data.csv'

# Read all rows
print("Reading CSV...")
rows = []
with open(csv_path, 'r', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        rows.append(row)

print(f"Found {len(rows)} spells")

# Update cantrip levels
updated_count = 0
for row in rows:
    # Parse the traits JSON
    if row.get('traits'):
        try:
            traits = json.loads(row['traits'])
            if 'cantrip' in traits:
                old_level = row.get('level', 'N/A')
                row['level'] = '0'
                print(f"Updated: {row['name']} (level {old_level} -> 0)")
                updated_count += 1
        except json.JSONDecodeError:
            print(f"Warning: Could not parse traits for {row['name']}")

# Write back to CSV
print(f"\nWriting updated CSV...")
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(rows)

print(f"\n✓ SUCCESS!")
print(f"Updated {updated_count} cantrips to level 0")
print(f"Total spells: {len(rows)}")

