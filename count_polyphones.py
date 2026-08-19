import pandas as pd
import pypinyin
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EXCEL_FILE = 'hanzicraft_dashboard_reordered.xlsx'

def run():
    df = pd.read_excel(EXCEL_FILE)
    total = len(df)
    multi_pyn_list = []
    
    for idx, row in df.iterrows():
        c = str(row['Chữ Trung Quốc']).strip()
        try:
            res = pypinyin.pinyin(c, heteronym=True, style=pypinyin.Style.TONE)
            if res and len(res[0]) > 1:
                pyns = " / ".join(res[0])
                multi_pyn_list.append((c, pyns))
        except Exception:
            pass

    print(f"Tổng số chữ Hán trong Excel: {total}")
    print(f"Số chữ Hán ĐA ÂM TỰ (có từ 2 cách đọc Pinyin trở lên): {len(multi_pyn_list)} / {total} ({len(multi_pyn_list)/total*100:.1f}%)")
    
    print("\nVí dụ 20 chữ Hán Đa Âm Tự tiêu biểu trong dataset:")
    for c, pyns in multi_pyn_list[:20]:
        print(f"  Chữ [{c}] ➔ Các cách đọc Pinyin: {pyns}")

if __name__ == '__main__':
    run()
