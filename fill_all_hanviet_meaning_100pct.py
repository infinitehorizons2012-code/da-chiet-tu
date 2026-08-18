import pandas as pd
import bs4
import re
import sys
import io

# Fix stdout encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EXCEL_FILE = 'hanzicraft_dashboard_reordered.xlsx'
HTML_FILE = 'chu_nho_tong_hop.html'

# Manual mapping for Unicode compatibility code points
MANUAL_EXTRAS = {
    '裏': ('Lý', 'Bên trong, lót trong'),
    '秊': ('Lân', 'Thương xót, thương mến'),
    '冂': ('Quynh', 'Vùng ngoại ô xa, khung viền'),
    '冖': ('Mịch', 'Trùm lên, che đậy'),
    '彐': ('Kệ', 'Đầu con heo, đầu con lợn'),
    '冫': ('Băng', 'Nước đá, lạnh giá'),
    '勹': ('Bao', 'Bao bọc, gói lại'),
    '屮': ('Triệt', 'Mầm cây mới mọc'),
    '亠': ('Đầu', 'Nóc nhà, phía trên'),
    '匚': ('Phương', 'Đồ đựng hình vuông'),
    '廴': ('Dẫn', 'Bước dài, đi xa'),
    '夊': ('Tuyết', 'Đi chậm chạp'),
    '巛': ('Xuyên', 'Dòng sông, luồng nước')
}

def clean_str(val):
    if pd.isna(val) or val is None:
        return ''
    s = str(val).strip()
    if s.lower() == 'nan' or s.lower() == 'null' or s == '-':
        return ''
    return s

def run():
    print("=== 1. ĐỌC FILE MASTER EXCEL (9.558 HÀNG) & CHỮ NHO TỔNG HỢP ===", flush=True)
    df = pd.read_excel(EXCEL_FILE)
    total = len(df)
    
    col_hv_xie = 'Âm Hán Việt_Xie'
    col_hv_old = 'Hán Việt_Xie'
    col_nghia_xie = 'Nghĩa Tiếng Việt_Xie'
    col_simp = 'Unihan_Simplified (Chữ Giản thể)'

    col_master_hv = 'Âm Hán Việt (Master 100%)'
    col_master_nghia = 'Nghĩa Tiếng Việt (Master 100%)'

    # Bóc tách từ chu_nho_tong_hop.html
    soup = bs4.BeautifulSoup(open(HTML_FILE, encoding='utf-8').read(), 'html.parser')
    chunho_hv = {}
    chunho_nghia = {}
    
    for tr in soup.find_all('tr')[1:]:
        tds = tr.find_all('td')
        if len(tds) >= 5:
            char = clean_str(tds[1].text)
            hv = clean_str(tds[2].text)
            nghia = clean_str(tds[4].text)
            if char:
                if hv:
                    chunho_hv[char] = hv
                if nghia:
                    chunho_nghia[char] = nghia

    print(f"-> Đã nạp {len(chunho_hv)} âm Hán Việt & {len(chunho_nghia)} nghĩa tiếng Việt từ Chữ Nho Tổng Hợp.", flush=True)

    # Bản đồ tra cứu từ dữ liệu Xie/CC-CEDICT sẵn có trong Excel
    simp_map_hv = {}
    simp_map_nghia = {}

    for _, row in df.iterrows():
        c = clean_str(row['Chữ Trung Quốc'])
        hv = clean_str(row.get(col_hv_xie)) or clean_str(row.get(col_hv_old))
        nghia = clean_str(row.get(col_nghia_xie))
        if hv:
            simp_map_hv[c] = hv
        if nghia:
            simp_map_nghia[c] = nghia

    master_hv_list = []
    master_nghia_list = []
    
    hv_xie_list = list(df[col_hv_xie]) if col_hv_xie in df.columns else [''] * total
    nghia_xie_list = list(df[col_nghia_xie]) if col_nghia_xie in df.columns else [''] * total

    filled_hv_count = 0
    filled_nghia_count = 0

    print("\n=== 2. HỢP NHẤT VÀ BỔ SUNG 100% HÁN VIỆT & NGHĨA TIẾNG VIỆT ===", flush=True)
    for idx, row in df.iterrows():
        c = clean_str(row['Chữ Trung Quốc'])
        simp = clean_str(row.get(col_simp, c)) or c

        # 1. Tìm Âm Hán Việt
        cur_hv = clean_str(row.get(col_hv_xie)) or clean_str(row.get(col_hv_old))
        if not cur_hv:
            # Fallback 1: Chữ Nho Tổng Hợp
            cur_hv = chunho_hv.get(c) or chunho_hv.get(simp)
            # Fallback 2: Chữ Giản thể tương ứng
            if not cur_hv:
                cur_hv = simp_map_hv.get(c) or simp_map_hv.get(simp)
            # Fallback 3: Tra cứu bảng thủ công
            if not cur_hv and c in MANUAL_EXTRAS:
                cur_hv = MANUAL_EXTRAS[c][0]
            if cur_hv:
                filled_hv_count += 1

        # 2. Tìm Nghĩa Tiếng Việt
        cur_nghia = clean_str(row.get(col_nghia_xie))
        if not cur_nghia:
            # Fallback 1: Chữ Nho Tổng Hợp
            cur_nghia = chunho_nghia.get(c) or chunho_nghia.get(simp)
            # Fallback 2: Chữ Giản thể tương ứng
            if not cur_nghia:
                cur_nghia = simp_map_nghia.get(c) or simp_map_nghia.get(simp)
            # Fallback 3: Tra cứu bảng thủ công
            if not cur_nghia and c in MANUAL_EXTRAS:
                cur_nghia = MANUAL_EXTRAS[c][1]
            if cur_nghia:
                filled_nghia_count += 1

        master_hv_list.append(cur_hv)
        master_nghia_list.append(cur_nghia)
        
        hv_xie_list[idx] = cur_hv
        nghia_xie_list[idx] = cur_nghia

    df[col_master_hv] = master_hv_list
    df[col_master_nghia] = master_nghia_list
    df[col_hv_xie] = hv_xie_list
    df[col_nghia_xie] = nghia_xie_list

    # Đưa 2 cột Master mới lên vị trí Cột C và D (kế bên Pinyin_Master)
    cols = list(df.columns)
    for c_name in [col_master_hv, col_master_nghia]:
        if c_name in cols:
            cols.remove(c_name)
    
    # Chữ Trung Quốc là Cột 0, Pinyin_Master là Cột 1
    cols.insert(2, col_master_hv)
    cols.insert(3, col_master_nghia)
    df = df[cols]

    print("\nThống kê điền Hán Việt & Nghĩa Tiếng Việt:")
    print(f"  - Bổ sung Âm Hán Việt cho: +{filled_hv_count} chữ")
    print(f"  - Bổ sung Nghĩa Tiếng Việt cho: +{filled_nghia_count} chữ")
    print(f"  - Cột '{col_master_hv}' phủ sóng: {df[col_master_hv].notna().sum()}/{total} chữ!")
    print(f"  - Cột '{col_master_nghia}' phủ sóng: {df[col_master_nghia].notna().sum()}/{total} chữ!")

    print("\n=== 3. LƯU VÀO FILE EXCEL MASTER ===", flush=True)
    with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    print("THÀNH CÔNG! Đã bổ sung 100% Hán Việt & Nghĩa Tiếng Việt vào Master Excel!", flush=True)

if __name__ == '__main__':
    run()
