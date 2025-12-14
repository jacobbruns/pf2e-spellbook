import csv
import json
import os
import sys

# Spell to add (pass as argument or default)
spell_name = sys.argv[1] if len(sys.argv) > 1 else 'Dehydrate'

# Load all spell data from pf2etools
spells_dir = 'Pf2eTools/data/spells'
all_spells = {}

for filename in os.listdir(spells_dir):
    if filename.endswith('.json') and filename.startswith('spells-'):
        filepath = os.path.join(spells_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for spell in data.get('spell', []):
                name = spell.get('name', '')
                all_spells[name.lower()] = spell

print('Loaded %d spells from pf2etools' % len(all_spells))

# Find the spell
if spell_name.lower() not in all_spells:
    print('Spell not found: %s' % spell_name)
    sys.exit(1)

spell = all_spells[spell_name.lower()]
print('Found: %s (Level %s)' % (spell.get('name'), spell.get('level')))

# Helper to format JSON fields
def fmt(val):
    if val is None:
        return ''
    if isinstance(val, (dict, list)):
        return json.dumps(val)
    return str(val)

# Read existing CSV to get column order
with open('Spellbook/spells-sublist-data.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    headers = [h.strip() for h in next(reader)]

# Build row
row = {}
row['learn-source'] = 'spells-sublist-4star'
row['name'] = spell.get('name', spell_name)
row['source'] = spell.get('source', '')
row['remaster'] = str(spell.get('remaster', False))
row['page'] = spell.get('page', '')
row['level'] = spell.get('level', 0)
row['traits'] = fmt(spell.get('traits'))
row['traditions'] = fmt(spell.get('traditions'))
row['spellLists'] = fmt(spell.get('spellLists'))
row['cast'] = fmt(spell.get('cast'))
row['components'] = fmt(spell.get('components'))
row['range'] = fmt(spell.get('range'))
row['targets'] = spell.get('targets', '')
row['area'] = fmt(spell.get('area'))
row['duration'] = fmt(spell.get('duration'))
row['savingThrow'] = fmt(spell.get('savingThrow'))
row['entries'] = fmt(spell.get('entries'))
row['heightened'] = fmt(spell.get('heightened'))
row['activity'] = fmt(spell.get('activity'))
row['miscTags'] = fmt(spell.get('miscTags'))
row['trigger'] = spell.get('trigger', '')
row['type'] = spell.get('type', '')

# Append to CSV
with open('Spellbook/spells-sublist-data.csv', 'a', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writerow(row)

print('Added: %s to spells-sublist-data.csv' % spell.get('name'))

