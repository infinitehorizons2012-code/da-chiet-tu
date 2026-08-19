import pandas as pd
import pypinyin
import re
import sys
import io

# Fix stdout encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EXCEL_FILE = 'hanzicraft_dashboard_reordered.xlsx'
TRACKING_FILE = 'pinyin_audio_tracking.xlsx'

def run():
    print("=== 1. ĐỌC TỆP MÃ HÓA ÂM THANH CLOUDINARY PINYIN ===", flush=True)
    audio_df = pd.read_excel(TRACKING_FILE)
    audio_map = {}
    
    for idx, r in audio_df.iterrows():
        fn = str(r['Filename']).strip().lower()
        url = str(r['Cloudinary URL']).strip()
        if pd.notna(r['Cloudinary URL']) and url and url.lower() != 'nan':
            audio_map[fn] = url
            
    print(f"-> Đã nạp thành công {len(audio_map)} link MP3 Cloudinary từ file pinyin_audio_tracking.xlsx!", flush=True)

    print("\n=== 2. GHÉP LINK CLOUDINARY MP3 CHO TOÀN BỘ 9.558 HÀNG MASTER EXCEL ===", flush=True)
    df = pd.read_excel(EXCEL_FILE)
    total = len(df)
    
    col_master_pyn = 'Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)'
    col_audio = 'Link Âm Thanh Pinyin (Cloudinary MP3)'

    cloudinary_audio_list = []
    found_count = 0
    missing_count = 0

    for idx, row in df.iterrows():
        c = str(row['Chữ Trung Quốc']).strip()
        url = ''
        
        try:
            # Lấy pinyin tone3 (ví dụ: 'de5', 'yi1', 'shi4', 'bu4', 'le5', 'zai4', 'ren2')
            py_tone3 = pypinyin.pinyin(c, style=pypinyin.Style.TONE3)[0][0].lower()
            if not re.search(r'\d$', py_tone3):
                py_tone3 += '5'

            # Tra trực tiếp
            url = audio_map.get(py_tone3, '')

            # Tra fallback 1: Thanh 5 ➔ Thanh 1 ➔ Thanh 4
            if not url and py_tone3.endswith('5'):
                base = py_tone3[:-1]
                url = audio_map.get(base + '1') or audio_map.get(base + '4') or audio_map.get(base + '2') or audio_map.get(base)

            # Tra fallback 2: Chuyển v <-> u cho nǚ / lǜ (nv3 / nu3, lv4 / lu4)
            if not url and 'v' in py_tone3:
                url = audio_map.get(py_tone3.replace('v', 'u'))
            if not url and 'u' in py_tone3:
                url = audio_map.get(py_tone3.replace('u', 'v'))
        except Exception:
            pass

        if url:
            found_count += 1
            cloudinary_audio_list.append(url)
        else:
            missing_count += 1
            cloudinary_audio_list.append('')

    df[col_audio] = cloudinary_audio_list

    # Chèn cột mới vào ngay sau Pinyin_Master (Cột B)
    cols = list(df.columns)
    if col_audio in cols:
        cols.remove(col_audio)
        
    if col_master_pyn in cols:
        pyn_idx = cols.index(col_master_pyn)
        cols.insert(pyn_idx + 1, col_audio)
    else:
        cols.insert(2, col_audio)
        
    df = df[cols]

    print(f"\nThống kê phủ sóng Âm Thanh Pinyin Cloudinary MP3:")
    print(f"  - Số chữ Hán CÓ LINK ÂM THANH CLOUDINARY: {found_count} / {total} chữ ({found_count/total*100:.2f}%)")
    print(f"  - Số chữ Hán không có âm thanh thô: {missing_count} / {total} chữ")

    print("\nSample check first 10 rows:")
    print(df[['Chữ Trung Quốc', col_master_pyn, col_audio]].head(10).to_string(index=False))

    print("\n=== 3. LƯU CẬP NHẬT VÀO FILE EXCEL MASTER ===", flush=True)
    with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    print(f"THÀNH CÔNG! Đã bổ sung cột '{col_audio}' vào Master Excel!", flush=True)

if __name__ == '__main__':
    run()
