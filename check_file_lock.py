import os

csv_path = r'C:\Users\Jacob\Documents\Code\PF2E\Spellbook\spells-sublist-data.csv'

try:
    # Try to open the file in write mode
    with open(csv_path, 'a', encoding='utf-8') as f:
        print("✓ File is NOT locked - safe to proceed")
except PermissionError:
    print("✗ File IS LOCKED - please close Excel or any program that has the CSV file open")
except Exception as e:
    print(f"Error: {e}")

