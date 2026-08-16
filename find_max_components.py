import pandas as pd
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

df = pd.read_excel('hanzicraft_dashboard_reordered.xlsx')

def count_comps_hzc(val):
    if pd.isna(val):
        return 0
    val_str = str(val).strip()
    if not val_str or val_str == 'nan':
        return 0
    return len([c.strip() for c in val_str.split(',') if c.strip()])

def count_comps_gg(val):
    if pd.isna(val):
        return 0
    val_str = str(val).strip()
    if not val_str or val_str == 'nan':
        return 0
    return len([c.strip() for c in val_str.split('+') if c.strip()])

def count_comps_cn(val):
    if pd.isna(val):
        return 0
    val_str = str(val).strip()
    if not val_str or val_str == 'nan' or val_str == '-':
        return 0
    # Count words or bracketed radicals in ChuNhoTongHop
    return len(val_str.split())

df['cnt_hzc'] = df['Components_Hanzicraft'].apply(count_comps_hzc)
df['cnt_gg'] = df['GavinGrover_Radical (Chiết tự bộ thủ)'].apply(count_comps_gg)
df['cnt_cn'] = df['ChuNhoTongHop_LinhKien (Cấu tạo linh kiện)'].apply(count_comps_cn)

top_hzc = df.sort_values(by='cnt_hzc', ascending=False).iloc[0]
top_gg = df.sort_values(by='cnt_gg', ascending=False).iloc[0]
top_cn = df.sort_values(by='cnt_cn', ascending=False).iloc[0]

print("=== TOP BANGCAP TRONG FILE EXCEL ===")
print(f"1. Theo HanziCraft: Chữ [{top_hzc['Chữ Trung Quốc']}] có {top_hzc['cnt_hzc']} linh kiện: {top_hzc['Components_Hanzicraft']}")
print(f"2. Theo Gavin Grover: Chữ [{top_gg['Chữ Trung Quốc']}] có {top_gg['cnt_gg']} linh kiện bộ thủ: {top_gg['GavinGrover_Radical (Chiết tự bộ thủ)']}")
print(f"3. Theo Chữ Nho Tổng Hợp: Chữ [{top_cn['Chữ Trung Quốc']}] có linh kiện: {top_cn['ChuNhoTongHop_LinhKien (Cấu tạo linh kiện)']}")

print("\nTop 5 chữ nhiều linh kiện nhất (HanziCraft):")
for i, row in df.sort_values(by='cnt_hzc', ascending=False).head(5).iterrows():
    print(f"  - Chữ [{row['Chữ Trung Quốc']}]: {row['cnt_hzc']} linh kiện ({row['Components_Hanzicraft']})")

print("\nTop 5 chữ nhiều linh kiện nhất (Gavin Grover):")
for i, row in df.sort_values(by='cnt_gg', ascending=False).head(5).iterrows():
    print(f"  - Chữ [{row['Chữ Trung Quốc']}]: {row['cnt_gg']} linh kiện ({row['GavinGrover_Radical (Chiết tự bộ thủ)']})")
