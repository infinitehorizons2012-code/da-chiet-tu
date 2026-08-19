import pandas as pd
import pypinyin
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EXCEL_FILE = 'hanzicraft_dashboard_reordered.xlsx'
TRACKING_FILE = 'pinyin_audio_tracking.xlsx'

def run():
    print("=== 1. ĐỌC FILE TRACKING ÂM THANH CLOUDINARY ===", flush=True)
    audio_df = pd.read_excel(TRACKING_FILE)
    print(f"Tổng số hàng trong file tracking: {len(audio_df)}")
    
    audio_map = {}
    for idx, r in audio_df.iterrows():
        fn = str(r['Filename']).strip().lower()
        url = str(r['Cloudinary URL']).strip()
        if pd.notna(r['Cloudinary URL']) and url and url.lower() != 'nan':
            audio_map[fn] = url
            
    print(f"-> Đã nạp thành công {len(audio_map)} link MP3 Cloudinary hợp lệ!", flush=True)

    print("\n=== 2. ĐỌC MASTER EXCEL (9.558 HÀNG) VÀ THỬ NỐI LINK ÂM THANH ===", flush=True)
    df = pd.read_excel(EXCEL_FILE)
    total = len(df)
    
    found_count = 0
    missing_list = []
    
    for idx, row in df.iterrows():
        c = str(row['Chữ Trung Quốc']).strip()
        try:
            # Lấy tone3 từ pypinyin (ví dụ: 'de5', 'yi1', 'shi4', 'bu4', 'le5', 'zai4', 'ren2')
            py_tone3 = pypinyin.pinyin(c, style=pypinyin.Style.TONE3)[0][0].lower()
            
            # Xử lý chuẩn hóa tên file pinyin: nếu không có số ở cuối, thêm số 5 (thanh nhẹ)
            if not re.search(r'\d$', py_tone3):
                py_tone3 += '5'
                
            url = audio_map.get(py_tone3)
            if url:
                found_count += 1
            else:
                missing_list.append((c, py_tone3))
        except Exception as e:
            missing_list.append((c, 'err'))

    print(f"Kết quả nối link âm thanh Cloudinary:")
    print(f"  - Số chữ Hán ghép khớp link MP3 Cloudinary: {found_count} / {total} chữ ({found_count/total*100:.1f}%)")
    print(f"  - Số chữ Hán chưa khớp được: {len(missing_list)} / {total} chữ")

    if missing_list:
        print("\nMẫu các chữ chưa tìm thấy link MP3:")
        print(missing_list[:20])

if __name__ == '__main__':
    run()
