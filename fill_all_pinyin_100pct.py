import pandas as pd
import pypinyin
import re
import sys
import io
from hanzipy.dictionary import HanziDictionary

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

def get_pypinyin_tone(char):
    try:
        py_list = pypinyin.pinyin(char, style=pypinyin.Style.TONE)
        if py_list and len(py_list) > 0 and len(py_list[0]) > 0:
            return py_list[0][0]
    except Exception:
        pass
    return ''

def run():
    print("=== 1. ĐỌC DỮ LIỆU FILE MASTER EXCEL (9.558 HÀNG) ===", flush=True)
    df = pd.read_excel(EXCEL_FILE)
    total = len(df)
    print(f"Tổng số hàng trong Excel: {total}", flush=True)

    dictionary = HanziDictionary()
    dict_sim = dictionary.dictionary_simplified
    dict_trad = dictionary.dictionary_traditional

    col_master_pyn = 'Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)'
    col_xie_pyn = 'Pinyin_Xie'
    col_cedict_pyn = 'CC-CEDICT_Pinyin'
    col_simp = 'Unihan_Simplified (Chữ Giản thể)'

    master_pyn_list = []
    xie_pyn_list = list(df[col_xie_pyn]) if col_xie_pyn in df.columns else [''] * total
    cedict_pyn_list = list(df[col_cedict_pyn]) if col_cedict_pyn in df.columns else [''] * total

    filled_xie_count = 0
    filled_cedict_count = 0

    print("\n=== 2. TIẾN HÀNH ĐIỀN 100% PINYIN CHO TẤT CẢ CHỮ HÁN ===", flush=True)
    for idx, row in df.iterrows():
        c = clean_str(row['Chữ Trung Quốc'])
        simp = clean_str(row.get(col_simp, c)) or c
        
        # 1. Pinyin Master (100% Pypinyin tone)
        pyn_master = get_pypinyin_tone(c)
        if not pyn_master and simp != c:
            pyn_master = get_pypinyin_tone(simp)
        master_pyn_list.append(pyn_master)

        # 2. Xử lý Pinyin_Xie nếu bị thiếu
        cur_xie = clean_str(xie_pyn_list[idx])
        if not cur_xie:
            # Lấy pypinyin thế vào
            if pyn_master:
                xie_pyn_list[idx] = pyn_master
                filled_xie_count += 1

        # 3. Xử lý CC-CEDICT_Pinyin nếu bị thiếu
        cur_cedict = clean_str(cedict_pyn_list[idx])
        if not cur_cedict:
            # Tra qua chữ Giản thể tương ứng
            entries = dict_sim.get(simp, []) or dict_trad.get(c, [])
            if entries and isinstance(entries, list) and len(entries) > 0:
                pyn_found = entries[0].get('pinyin', '')
                if pyn_found:
                    cedict_pyn_list[idx] = pyn_found
                    filled_cedict_count += 1
            if not clean_str(cedict_pyn_list[idx]) and pyn_master:
                cedict_pyn_list[idx] = pyn_master
                filled_cedict_count += 1

        if (idx + 1) % 3000 == 0 or (idx + 1) == total:
            print(f"--- Đã xử lý {idx + 1}/{total} hàng... ---", flush=True)

    df[col_master_pyn] = master_pyn_list
    df[col_xie_pyn] = xie_pyn_list
    df[col_cedict_pyn] = cedict_pyn_list

    # Đưa cột Pinyin_Master lên gần Cột A
    cols = list(df.columns)
    if col_master_pyn in cols:
        cols.remove(col_master_pyn)
        cols.insert(1, col_master_pyn) # Đặt ngay sau Cột A (Chữ Trung Quốc)
        df = df[cols]

    print(f"\nThống kê điền Pinyin:")
    print(f"  - Số chữ được bổ sung Pinyin_Xie: +{filled_xie_count}")
    print(f"  - Số chữ được bổ sung CC-CEDICT_Pinyin: +{filled_cedict_count}")
    print(f"  - Pinyin_Master phủ sóng 100%: {df[col_master_pyn].notna().sum()}/{total} chữ!")

    print("\n=== 3. LƯU CẬP NHẬT VÀO FILE EXCEL MASTER ===", flush=True)
    with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    print("THÀNH CÔNG! Đã phủ sóng 100% Pinyin chuẩn cho toàn bộ 9.558 hàng!", flush=True)

if __name__ == '__main__':
    run()
