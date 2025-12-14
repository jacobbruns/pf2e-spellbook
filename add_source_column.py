import csv

# Read the existing CSV
input_path = r'C:\Users\Jacob\Downloads\spells-sublist-data.csv'
output_path = r'C:\Users\Jacob\Downloads\spells-sublist-data.csv'

print(f"Reading from: {input_path}")

# Read all rows
rows = []
with open(input_path, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = list(reader.fieldnames)

    # Add 'learn-source' column if it doesn't exist
    if 'learn-source' not in fieldnames:
        fieldnames.insert(0, 'learn-source')  # Add as first column

    for row in reader:
        # Set 'learn-source' column to 'thresholds'
        row['learn-source'] = 'thresholds'
        rows.append(row)

# Write back to CSV
with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Added 'learn-source' column with value 'thresholds' to {len(rows)} rows")
print(f"Updated file: {output_path}")

