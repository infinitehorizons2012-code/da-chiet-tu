import pandas as pd
import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

INPUT_FILE = 'hanzicraft_dashboard_reordered.xlsx'
OUTPUT_FILE = 'XieHanzi_TraChu_Database.xlsx'

print("Reading master database...")
df_master = pd.read_excel(INPUT_FILE)

# Select only valid characters scraped from XieHanzi
# Must have XieHanzi data (Pinyin_Xie or Bộ thủ & thành phần_Xie)
mask_valid = df_master['Bộ thủ & thành phần_Xie'].notna() & (df_master['Bộ thủ & thành phần_Xie'] != 'N/A')

df_sub = df_master[mask_valid].copy()

# Create clean, user-friendly column mapping for XieHanzi Tra Chữ
clean_cols = {
    'Chữ Trung Quốc': 'Chữ Hán',
    'Pinyin_Xie': 'Pinyin',
    'Âm Hán Việt_Xie': 'Âm Hán Việt',
    'Nghĩa Tiếng Việt_Xie': 'Nghĩa Tiếng Việt',
    'Link Âm Thanh_Xie': 'Link Âm Thanh MP3',
    'Bộ thủ & thành phần_Xie': 'Bộ Thủ & Thành Phần',
    'Loại từ & Cách dùng_Xie': 'Loại Từ & Cách Dùng Ngữ Pháp',
    'Nghĩa & Cách dùng như một từ_Xie': 'Nghĩa & Cách Dùng Như Một Từ',
    'Tự nguyên_Xie': 'Tự Nguyên (Nguồn Gốc Chữ)',
    'Dễ nhầm & Liên quan_Xie': 'Dễ Nhầm & Liên Quan',
    'Link': 'Link XieHanzi'
}

df_trachu = pd.DataFrame()
df_trachu['STT'] = range(1, len(df_sub) + 1)

for orig_col, new_name in clean_cols.items():
    if orig_col in df_sub.columns:
        df_trachu[new_name] = df_sub[orig_col]

print(f"Total XieHanzi Tra-Chữ rows formatted: {len(df_trachu)}")
print("\nFinal clean columns in XieHanzi_TraChu_Database.xlsx:")
for col in df_trachu.columns:
    print("  -", col)

print(f"\nWriting clean dedicated Excel file to {OUTPUT_FILE}...")
with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl') as writer:
    df_trachu.to_excel(writer, index=False)

print("Done! Dedicated XieHanzi_TraChu_Database.xlsx successfully generated!")
