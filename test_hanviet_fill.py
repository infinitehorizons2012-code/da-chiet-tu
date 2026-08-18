import pandas as pd
import bs4
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EXCEL_FILE = 'hanzicraft_dashboard_reordered.xlsx'
HTML_FILE = 'chu_nho_tong_hop.html'

def run():
    df = pd.read_excel(EXCEL_FILE)
    print(f"TOTAL ROWS IN EXCEL: {len(df)}")
    
    col_hv = 'Âm Hán Việt_Xie'
    col_nghia = 'Nghĩa Tiếng Việt_Xie'
    col_simp = 'Unihan_Simplified (Chữ Giản thể)'

    print(f"Missing [{col_hv}] before: {df[col_hv].isna().sum()}")
    print(f"Missing [{col_nghia}] before: {df[col_nghia].isna().sum()}")

    # 1. Bóc tách từ chu_nho_tong_hop.html
    soup = bs4.BeautifulSoup(open(HTML_FILE, encoding='utf-8').read(), 'html.parser')
    chunho_hv = {}
    chunho_nghia = {}
    
    for tr in soup.find_all('tr')[1:]:
        tds = tr.find_all('td')
        if len(tds) >= 5:
            char = tds[1].text.strip()
            hv = tds[2].text.strip()
            nghia = tds[4].text.strip()
            if char:
                if hv and hv != '-':
                    chunho_hv[char] = hv
                if nghia and nghia != '-':
                    chunho_nghia[char] = nghia

    print(f"Parsed {len(chunho_hv)} Hán Việt entries & {len(chunho_nghia)} Meaning entries from HTML.")

    # 2. Tạo bản đồ tra cứu từ Giản thể hiện có trong Excel
    simp_map_hv = {}
    simp_map_nghia = {}
    for _, row in df.iterrows():
        c = str(row['Chữ Trung Quốc']).strip()
        hv = str(row.get(col_hv, '')).strip()
        nghia = str(row.get(col_nghia, '')).strip()
        if hv and hv.lower() != 'nan':
            simp_map_hv[c] = hv
        if nghia and nghia.lower() != 'nan':
            simp_map_nghia[c] = nghia

    still_missing_hv = []
    still_missing_nghia = []

    for idx, row in df.iterrows():
        c = str(row['Chữ Trung Quốc']).strip()
        simp = str(row.get(col_simp, c)).strip()
        if not simp or simp.lower() == 'nan':
            simp = c

        hv = str(row.get(col_hv, '')).strip()
        if pd.isna(row.get(col_hv)) or not hv or hv.lower() == 'nan':
            found_hv = chunho_hv.get(c) or chunho_hv.get(simp) or simp_map_hv.get(c) or simp_map_hv.get(simp)
            if not found_hv:
                still_missing_hv.append((c, simp))

        nghia = str(row.get(col_nghia, '')).strip()
        if pd.isna(row.get(col_nghia)) or not nghia or nghia.lower() == 'nan':
            found_nghia = chunho_nghia.get(c) or chunho_nghia.get(simp) or simp_map_nghia.get(c) or simp_map_nghia.get(simp)
            if not found_nghia:
                still_missing_nghia.append((c, simp))

    print(f"\nRemaining missing Hán Việt after ChuNho & Simplification fallback: {len(still_missing_hv)}")
    print(f"Remaining missing Nghĩa tiếng Việt after ChuNho & Simplification fallback: {len(still_missing_nghia)}")

    if still_missing_hv:
        print("\nSample characters still missing Hán Việt:")
        print(still_missing_hv[:30])

if __name__ == '__main__':
    run()
