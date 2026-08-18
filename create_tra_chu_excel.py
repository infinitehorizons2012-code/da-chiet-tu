import pandas as pd
import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

INPUT_FILE = 'hanzicraft_dashboard_reordered.xlsx'
OUTPUT_FILE = 'XieHanzi_TraChu_Database.xlsx'

print("Loading existing scraped XieHanzi database...")
df = pd.read_excel(INPUT_FILE)

print(f"Total rows in master dataset: {len(df)}")
print("\nColumns available in master dataset:")
for idx, col in enumerate(df.columns, 1):
    print(f"  {idx}. {col}")

# Check XieHanzi specific columns
xie_cols = [c for c in df.columns if 'Xie' in c or c in ['Chữ Trung Quốc', 'Chữ', 'Pinyin', 'Hán Việt', 'Nghĩa tiếng Việt']]

print(f"\nExtracted {len(xie_cols)} XieHanzi columns for dedicated Tra-Chứ dataset...")

# Create dedicated Excel file
df_trachu = df.copy()

# Save to XieHanzi_TraChu_Database.xlsx
print(f"Saving dedicated Excel file to {OUTPUT_FILE}...")
with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl') as writer:
    df_trachu.to_excel(writer, index=False)

print("Done creating XieHanzi_TraChu_Database.xlsx!")
