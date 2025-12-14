import csv
import json
import os

# Spell names to include
spell_names = [
    'Know the Way', 'Void Warp', 'Light', 'Daze', 'Detect Magic', 'Electric Arc',
    'Telekinetic Hand', 'Prestidigitation', 'Read Aura', 'Shield', 'Figment', 'Alarm',
    'Charm', 'Dizzying Colors', 'Mystic Armor', 'Force Barrage', 'Sure Strike',
    'Phantasmal Minion', 'Translate', 'Dispel Magic', 'False Vitality', 'Revealing Light',
    'Web', 'Haste', 'Lightning Bolt', 'Locate', 'Paralyze', 'Slow', 'Eat Fire',
    'Puff of Poison', 'Scatter Scree', 'Warp Step', 'Message', 'Sigil', 'Take Root',
    'Ray of Frost', 'Ignition', 'Slashing Gust', 'Needle Darts', 'Telekinetic Projectile',
    'Command', 'Fear', 'Illusory Object', 'Interposing Earth', 'Runic Body', 'Runic Weapon',
    'Briny Bolt', 'Pocket Library', 'Dehydrate', 'Blood Vendetta', 'Enlarge', 'Invisibility',
    'Laughing Fit', 'Thermal Remedy', 'Fireball', 'Wall of Thorns', 'Roaring Applause', 'Tailwind'
]

# Load all spells from pf2etools
spells_dir = 'Pf2eTools/data/spells'
all_spells = {}
for filename in os.listdir(spells_dir):
    if filename.endswith('.json') and filename.startswith('spells-'):
        with open(os.path.join(spells_dir, filename), 'r', encoding='utf-8') as f:
            data = json.load(f)
            for spell in data.get('spell', []):
                all_spells[spell.get('name', '').lower()] = spell

print('Loaded %d spells from pf2etools' % len(all_spells))

# Load price/DC data
price_dc = {}
with open('Spellbook/Learning a Spell.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rank = row['Spell-Rank'].strip()
        price = row['Price'].strip()
        dc = row['Typical-DC'].strip()
        if rank == '0':
            price_dc[0] = (price, dc)
        else:
            level = int(rank.replace('th','').replace('nd','').replace('rd','').replace('st',''))
            price_dc[level] = (price, dc)

# CSV headers
headers = ['name', 'source', 'remaster', 'page', 'level', 'traits', 'traditions', 
           'spellLists', 'cast', 'components', 'range', 'targets', 'area', 'duration',
           'savingThrow', 'entries', 'heightened', 'activity', 'miscTags', 'trigger', 
           'type', 'Price', 'Typical-DC']

def fmt(val):
    if val is None:
        return ''
    if isinstance(val, (dict, list)):
        return json.dumps(val)
    return str(val)

# Build rows
rows = []
not_found = []
for name in spell_names:
    if name.lower() in all_spells:
        s = all_spells[name.lower()]
        level = s.get('level', 0)
        p, d = price_dc.get(level, ('', ''))
        row = [
            s.get('name', name), s.get('source', ''), str(s.get('remaster', False)),
            s.get('page', ''), level, fmt(s.get('traits')), fmt(s.get('traditions')),
            fmt(s.get('spellLists')), fmt(s.get('cast')), fmt(s.get('components')),
            fmt(s.get('range')), s.get('targets', ''), fmt(s.get('area')),
            fmt(s.get('duration')), fmt(s.get('savingThrow')), fmt(s.get('entries')),
            fmt(s.get('heightened')), fmt(s.get('activity')), fmt(s.get('miscTags')),
            s.get('trigger', ''), s.get('type', ''), p, d
        ]
        rows.append(row)
    else:
        not_found.append(name)

# Write CSV
with open('Spellbook/spells-sublist-data.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

print('Wrote %d spells to spells-sublist-data.csv' % len(rows))
if not_found:
    print('Not found:', not_found)

