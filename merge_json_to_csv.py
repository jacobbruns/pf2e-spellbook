import json
import csv
import os

# Define the JSON files and their learn-source values (based on filename)
json_files = [
    {
        'path': r'C:\Users\Jacob\Documents\Code\PF2E\Spellbook\spells-sublist-thresholds.json',
        'learn_source': 'spells-sublist-thresholds'
    },
    {
        'path': r'C:\Users\Jacob\Documents\Code\PF2E\Spellbook\spells-sublist-class.json',
        'learn_source': 'spells-sublist-class'
    },
    {
        'path': r'C:\Users\Jacob\Documents\Code\PF2E\Spellbook\spells-sublist-class2.json',
        'learn_source': 'spells-sublist-class2'
    }
]

# Output path
output_csv = r'C:\Users\Jacob\Documents\Code\PF2E\Spellbook\spells-sublist-data.csv'

# Define all possible fieldnames
fieldnames = [
    'learn-source', 'name', 'source', 'remaster', 'page', 'level',
    'traits', 'traditions', 'spellLists', 'cast', 'components',
    'range', 'targets', 'area', 'duration', 'savingThrow',
    'entries', 'heightened', 'activity', 'miscTags', 'trigger', 'type'
]

# Collect all spells
all_rows = []
spell_names = set()
stats = {}

for json_file in json_files:
    print(f"\nReading: {os.path.basename(json_file['path'])}")
    
    try:
        with open(json_file['path'], 'r', encoding='utf-8') as f:
            spells = json.load(f)
        
        added = 0
        skipped = 0
        
        for spell in spells:
            if spell['name'] in spell_names:
                print(f"  Skipping duplicate: {spell['name']}")
                skipped += 1
                continue
            
            # Create row with learn-source from filename
            row = {'learn-source': json_file['learn_source']}
            for key, value in spell.items():
                if isinstance(value, (list, dict)):
                    row[key] = json.dumps(value, ensure_ascii=False)
                else:
                    row[key] = value
            
            all_rows.append(row)
            spell_names.add(spell['name'])
            added += 1
            print(f"  Added: {spell['name']}")
        
        stats[json_file['learn_source']] = {
            'total': len(spells),
            'added': added,
            'skipped': skipped
        }
    
    except FileNotFoundError:
        print(f"  ✗ File not found: {json_file['path']}")
    except Exception as e:
        print(f"  ✗ Error reading file: {e}")

# Write to CSV
print(f"\n{'='*60}")
print(f"Writing {len(all_rows)} total spells to CSV...")
print(f"{'='*60}")

try:
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(all_rows)
    
    print(f"\n✓ SUCCESS!")
    print(f"\nFile created at:")
    print(f"  {output_csv}")
    
    print(f"\nSummary by source:")
    for source, stat in stats.items():
        print(f"  {source}:")
        print(f"    - Total in JSON: {stat['total']}")
        print(f"    - Added to CSV: {stat['added']}")
        print(f"    - Skipped (duplicates): {stat['skipped']}")
    
    print(f"\nTotal unique spells in CSV: {len(all_rows)}")

except Exception as e:
    print(f"\n✗ ERROR writing CSV: {e}")
    import traceback
    traceback.print_exc()

