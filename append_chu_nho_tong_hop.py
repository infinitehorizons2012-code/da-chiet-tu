import pandas as pd
import sys
import io
import bs4

# Fix stdout encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EXCEL_PATH = 'hanzicraft_dashboard_reordered.xlsx'
HTML_PATH = r'C:\Users\DT.HANG\Downloads\DA chiet tu\chu_nho_tong_hop.html'

def run():
    print("Parsing HTML file chu_nho_tong_hop.html...")
    html_content = open(HTML_PATH, encoding='utf-8').read()
    soup = bs4.BeautifulSoup(html_content, 'html.parser')
    trs = soup.find_all('tr')
    
    html_map = {}
    for tr in trs[1:]:
        tds = [td.get_text(separator=" ", strip=True) for td in tr.find_all(['td', 'th'])]
        if len(tds) >= 8:
            stt = tds[0]
            char = tds[1]
            linh_kien = tds[6]
            giai_thich = tds[7]
            
            if char and char not in html_map:
                html_map[char] = {
                    'stt': stt,
                    'linh_kien': linh_kien if linh_kien != '-' else 'Chữ đơn thể / Nét căn bản',
                    'giai_thich': giai_thich
                }
                
    print(f"Loaded {len(html_map)} character entries from HTML!")
    
    print("Loading Excel data...")
    df = pd.read_excel(EXCEL_PATH)
    
    col_stt = 'ChuNhoTongHop_STT (Giáo trình Chữ Nho)'
    col_lk = 'ChuNhoTongHop_LinhKien (Cấu tạo linh kiện)'
    col_gt = 'ChuNhoTongHop_Chietyu_Giaithich (Chiết tự & Giải thích)'
    
    stt_list = []
    lk_list = []
    gt_list = []
    
    total = len(df)
    matched_count = 0
    
    print(f"Mapping HTML data into Excel for {total} characters...")
    for idx, row in df.iterrows():
        char = row['Chữ Trung Quốc']
        
        if pd.isna(char) or str(char).strip() == '' or str(char) == 'nan':
            stt_list.append('')
            lk_list.append('')
            gt_list.append('')
            continue
            
        char_str = str(char).strip()
        
        if char_str in html_map:
            entry = html_map[char_str]
            stt_list.append(entry['stt'])
            lk_list.append(entry['linh_kien'])
            gt_list.append(entry['giai_thich'])
            matched_count += 1
        else:
            stt_list.append('')
            lk_list.append('')
            gt_list.append('')
            
    df[col_stt] = stt_list
    df[col_lk] = lk_list
    df[col_gt] = gt_list
    
    print(f"Matched {matched_count}/{total} rows with Chữ Nho Tổng Hợp data!")
    
    print("Saving updated Excel file...")
    with pd.ExcelWriter(EXCEL_PATH, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        
    print("Successfully appended Chữ Nho Tổng Hợp columns to Excel!")

if __name__ == '__main__':
    run()
