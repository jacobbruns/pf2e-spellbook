import csv

# Read price/DC data
price_dc = {}
with open('Spellbook/Learning a Spell.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rank = row['Spell-Rank'].strip()
        price = row['Price'].strip()
        dc = row['Typical-DC'].strip()
        # Map rank to level
        if rank == '0':
            price_dc[0] = (price, dc)
        else:
            level = int(rank.replace('th', '').replace('nd', '').replace('rd', '').replace('st', ''))
            price_dc[level] = (price, dc)

print('Price/DC mapping:', price_dc)

# Read spells CSV
with open('Spellbook/spells-sublist-data.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    headers = [h.strip() for h in next(reader)]
    rows = list(reader)

# Add new columns
headers.extend(['Price', 'Typical DC'])
level_idx = headers.index('level')

for row in rows:
    level = int(row[level_idx].strip()) if row[level_idx].strip().isdigit() else 0
    if level in price_dc:
        row.extend(price_dc[level])
    else:
        row.extend(['', ''])

# Write back
with open('Spellbook/spells-sublist-data.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

print('Added Price and Typical DC columns to %d spells' % len(rows))

