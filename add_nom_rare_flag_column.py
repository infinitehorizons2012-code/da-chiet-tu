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

    col_audio = 'Link Âm Thanh Pinyin (Cloudinary MP3)'
    col_flag = 'Đánh Dấu Chữ Cổ / Chữ Nôm Hiếm'

    flag_list = []
    rare_count = 0
    common_count = 0

    print("\n=== 2. ĐÁNH DẤU PHÂN LOẠI CHỮ NHO CỔ / CHỮ NÔM HIẾM ===", flush=True)
    for idx, row in df.iterrows():
        audio_url = clean_str(row.get(col_audio))
        
        # Nếu chữ nằm trong danh sách không có âm thanh thô (hoặc là chữ Nôm/cổ hiếm)
        if not audio_url:
            status = "Chữ Nho Cổ / Chữ Nôm Hiếm (Không có Audio Pinyin)"
            rare_count += 1
        else:
            status = "Chữ Phổ Thông (Có Audio Pinyin)"
            common_count += 1
            
        flag_list.append(status)

    df[col_flag] = flag_list

    # Chèn cột mới vào ngay sau Link Âm Thanh Pinyin (Cloudinary MP3)
    cols = list(df.columns)
    if col_flag in cols:
        cols.remove(col_flag)
        
    if col_audio in cols:
        audio_idx = cols.index(col_audio)
        cols.insert(audio_idx + 1, col_flag)
    else:
        cols.insert(3, col_flag)
        
    df = df[cols]

    print(f"\nThống kê phân loại Chữ Nho Cổ / Chữ Nôm Hiếm:")
    print(f"  - Số chữ NHO CỔ / CHỮ NÔM HIẾM (Thiếu Audio Pinyin): {rare_count} / {total} chữ ({rare_count/total*100:.2f}%)")
    print(f"  - Số chữ PHỔ THÔNG (Có Audio Pinyin): {common_count} / {total} chữ ({common_count/total*100:.2f}%)")

    print("\nMẫu các chữ Nôm cổ hiếm được đánh dấu:")
    sample_rare = df[df[col_flag].str.contains('Hiếm')][['Chữ Trung Quốc', 'Âm Hán Việt (Master 100%)', 'Nghĩa Tiếng Việt (Master 100%)', col_flag]].head(15)
    print(sample_rare.to_string(index=False))

    print("\n=== 3. LƯU CẬP NHẬT VÀO FILE EXCEL MASTER ===", flush=True)
    with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    print(f"THÀNH CÔNG! Đã bổ sung cột '{col_flag}' vào Master Excel!", flush=True)

if __name__ == '__main__':
    run()
