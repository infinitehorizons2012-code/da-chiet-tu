import pandas as pd
import sys
import io

# Fix stdout encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EXCEL_FILE = 'hanzicraft_dashboard_reordered.xlsx'

def clean_str(val):
    if pd.isna(val) or val is None:
        return ''
    s = str(val).strip()
    if s.lower() == 'nan' or s.lower() == 'null':
        return ''
    return s

def run():
    print("=== 1. ĐỌC MASTER EXCEL (9.558 HÀNG) ===", flush=True)
    df = pd.read_excel(EXCEL_FILE)
    total = len(df)

    col_char = 'Chữ Trung Quốc'
    col_simp = 'Unihan_Simplified (Chữ Giản thể)'
    col_trad = 'Unihan_Traditional (Chữ Phồn thể)'
    col_diff = 'Phồn/Giản Khác Nhau (Unihan)'

    diff_status_list = []
    diff_count = 0
    same_count = 0

    print("\n=== 2. TÍNH TOÁN SO SÁNH GIẢN THỂ VÀ PHỒN THỂ DỰA TRÊN UNIHAN ===", flush=True)
    for idx, row in df.iterrows():
        c = clean_str(row.get(col_char))
        simp = clean_str(row.get(col_simp)) or c
        trad = clean_str(row.get(col_trad)) or c

        # Kiểm tra sự khác nhau giữa Giản thể và Phồn thể
        if simp != trad or c != simp or c != trad:
            # Hai chữ có biến thể Phồn / Giản khác nhau
            status = f"Khác nhau (Giản: {simp} - Phồn: {trad})"
            diff_count += 1
        else:
            # Phồn / Giản đồng nhất giống nhau
            status = "Giống nhau"
            same_count += 1
            
        diff_status_list.append(status)

    df[col_diff] = diff_status_list

    # Chèn cột mới vào ngay sau Unihan_Traditional
    cols = list(df.columns)
    if col_diff in cols:
        cols.remove(col_diff)
        
    if col_trad in cols:
        trad_idx = cols.index(col_trad)
        cols.insert(trad_idx + 1, col_diff)
    else:
        cols.append(col_diff)
        
    df = df[cols]

    print(f"\nThống kê so sánh Phồn / Giản (Unihan):")
    print(f"  - Số chữ Phồn / Giản KHÁC NHAU: {diff_count} / {total} chữ ({diff_count/total*100:.1f}%)")
    print(f"  - Số chữ Phồn / Giản GIỐNG NHAU: {same_count} / {total} chữ ({same_count/total*100:.1f}%)")

    print("\nSample check first 15 rows:")
    print(df[['Chữ Trung Quốc', col_simp, col_trad, col_diff]].head(15).to_string(index=False))

    print("\n=== 3. LƯU CẬP NHẬT VÀO FILE EXCEL MASTER ===", flush=True)
    with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    print(f"THÀNH CÔNG! Đã bổ sung cột '{col_diff}' chuẩn Unihan cho toàn bộ 9.558 hàng!", flush=True)

if __name__ == '__main__':
    run()
