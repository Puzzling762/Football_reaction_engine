import os
import pandas as pd
import csv
from io import StringIO

# Paths
file_path = r"D:\Projects\Fifa15_AI\COMBINED_EXPORT.csv"
output_dir = r"D:\Projects\Fifa15_AI\exported_data"
os.makedirs(output_dir, exist_ok=True)

# Read all lines
print("📖 Reading file...")
with open(file_path, 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f if line.strip()]

print(f"📊 Total lines read: {len(lines)}")

sheets = {}
current_sheet = None
current_lines = []

# Detect sheets - look for lines with "=== SHEET:"
for line in lines:
    # Check if this is a sheet header (with or without quotes)
    if "=== SHEET:" in line:
        # Save previous sheet
        if current_sheet and current_lines:
            sheets[current_sheet] = current_lines
            print(f"✅ Detected sheet '{current_sheet}' with {len(current_lines)} lines")
        
        # Extract sheet name - remove quotes and === markers
        current_sheet = line.replace('"', '').replace("=== SHEET:", "").replace("===", "").strip().replace(" ", "_")
        current_lines = []
        print(f"🆕 Found new sheet: {current_sheet}")
    else:
        current_lines.append(line)

# Add last sheet
if current_sheet and current_lines:
    sheets[current_sheet] = current_lines
    print(f"✅ Detected sheet '{current_sheet}' with {len(current_lines)} lines")

print(f"\n📋 Total sheets detected: {len(sheets)}")

# Convert to CSVs
for sheet_name, data_lines in sheets.items():
    if not data_lines or len(data_lines) < 2:
        print(f"⚠️  Skipping sheet '{sheet_name}' - insufficient data")
        continue
    
    print(f"\n🔧 Processing '{sheet_name}'...")
    
    # Join lines into a single string and use csv module to parse
    # This handles quoted values properly
    csv_string = '\n'.join(data_lines)
    
    try:
        # Use StringIO to treat string as file, then use csv.reader
        csv_file = StringIO(csv_string)
        reader = csv.reader(csv_file)
        
        # Read all rows
        rows = list(reader)
        
        if len(rows) < 2:
            print(f"⚠️  Skipping sheet '{sheet_name}' - no data rows")
            continue
        
        # First row is header
        header = rows[0]
        data_rows = rows[1:]
        
        # Create DataFrame
        df = pd.DataFrame(data_rows, columns=header)
        
        # Save to CSV
        out_path = os.path.join(output_dir, f"{sheet_name.lower()}.csv")
        df.to_csv(out_path, index=False)
        
        print(f"✅ Saved {out_path}")
        print(f"   📊 {len(df)} rows, {len(df.columns)} columns")
        print(f"   📝 Columns: {header[:5]}{'...' if len(header) > 5 else ''}")
        
    except Exception as e:
        print(f"❌ Error processing sheet '{sheet_name}': {e}")

print("\n🎉 Export complete!")