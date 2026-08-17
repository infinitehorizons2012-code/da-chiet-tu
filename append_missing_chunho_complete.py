import pandas as pd
import sys
import io
import bs4
import re
import requests
import concurrent.futures
from hanzipy.decomposer import HanziDecomposer

# Fix stdout encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EXCEL_PATH = 'hanzicraft_dashboard_reordered.xlsx'
HTML_PATH = r'C:\Users\DT.HANG\Downloads\DA chiet tu\chu_nho_tong_hop.html'

def clean_string(val):
    if not isinstance(val, str):
        return val
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', val)

def is_valid_chinese_char(c):
    if not c or not isinstance(c, str):
        return False
    c = c.strip()
    if len(c) != 1:
        return False
    # Check Unicode CJK block
    code = ord(c)
    return (0x4E00 <= code <= 0x9FFF) or (0x3400 <= code <= 0x4DBF) or (0x20000 <= code <= 0x2A6DF) or (0x2F00 <= code <= 0x2FDF)

def run():
    print("=== 1. ĐỌC CHÍNH XÁC TẤT CẢ CHỮ HÁN TỪ chu_nho_tong_hop.html ===", flush=True)
    html_content = open(HTML_PATH, encoding='utf-8').read()
    soup = bs4.BeautifulSoup(html_content, 'html.parser')
    trs = soup.find_all('tr')
    
    html_entries = []
    for tr in trs[1:]:
        tds = [td.get_text(separator=" ", strip=True) for td in tr.find_all(['td', 'th'])]
        if len(tds) >= 8:
            stt = tds[0].strip()
            char = tds[1].strip()
            linh_kien = tds[6].strip()
            giai_thich = tds[7].strip()
            
            if is_valid_chinese_char(char):
                html_entries.append({
                    'stt': stt,
                    'char': char,
                    'linh_kien': linh_kien if linh_kien != '-' else 'Chữ đơn thể / Nét căn bản',
                    'giai_thich': giai_thich
                })
                
    print(f"-> Đã bóc tách {len(html_entries)} chữ Hán hợp lệ từ chu_nho_tong_hop.html!", flush=True)

    print("\n=== 2. KIỂM TRA CHỮ HÁN THIẾU SO VỚI CỘT A TRONG EXCEL ===", flush=True)
    df_excel = pd.read_excel(EXCEL_PATH)
    col_char = 'Chữ Trung Quốc'
    
    existing_chars = set(df_excel[col_char].dropna().astype(str).str.strip())
    print(f"-> Excel hiện tại đang có {len(existing_chars)} chữ Hán ở Cột A.", flush=True)

    # Lọc ra các chữ trong Chữ Nho Tổng Hợp chưa có ở Cột A của Excel
    seen_missing = set()
    missing_entries = []
    for e in html_entries:
        c = e['char']
        if c not in existing_chars and c not in seen_missing:
            seen_missing.add(c)
            missing_entries.append(e)

    print(f"\n---> XÁC NHẬN CÓ {len(missing_entries)} CHỮ HÁN (PHỒN THỂ / CỔ ĐIỂN) CÒN THIẾU CẦN BỔ SUNG VÀO CỘT A! <---", flush=True)
    for idx, item in enumerate(missing_entries, 1):
        print(f"  {idx:3d}. Chữ: [{item['char']}] (STT Chữ Nho: {item['stt']}) | Linh kiện: {item['linh_kien'][:30]}...", flush=True)

    if len(missing_entries) == 0:
        print("\nTất cả chữ Hán trong Chữ Nho Tổng Hợp đã đầy đủ 100% trong Excel!", flush=True)
        return

    print(f"\n=== 3. CÀO DỮ LIỆU XIEHANZI LIVE CHO {len(missing_entries)} CHỮ HÁN BỔ SUNG ===", flush=True)
    
    def parse_xiehanzi_live(char_str):
        url = f'https://xiehanzi.com/han-tu/{char_str}/'
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            if r.status_code != 200:
                return {'char': char_str}
            sp = bs4.BeautifulSoup(r.text, 'html.parser')
            html_text = r.text
            
            # Audio MP3 Link
            audio_link = ""
            mp3_matches = re.findall(r'(https?://static\.xiehanzi\.com/[^\s"\'<>]+\.mp3)', html_text)
            if mp3_matches:
                audio_link = mp3_matches[0]
                for m in mp3_matches:
                    if 'word_audios' in m or 'female' in m or char_str in m:
                        audio_link = m
                        break
                        
            pinyin = ""
            am_han_viet = ""
            nghia_tv = ""
            text_blocks = [tag.get_text(separator=' | ', strip=True) for tag in sp.find_all(['div', 'p', 'span', 'header'])]
            for block in text_blocks:
                if 'Nghĩa tiếng Việt' in block and not nghia_tv:
                    m = re.search(r'Nghĩa tiếng Việt\s*\|\s*([^\|]+)', block)
                    if m: nghia_tv = m.group(1).strip()
                if 'Âm Hán Việt' in block and not am_han_viet:
                    m = re.search(r'Âm Hán Việt\s*\|\s*([^\|]+)', block)
                    if m: am_han_viet = m.group(1).strip()

            for tag in sp.find_all(['span', 'div', 'p']):
                t = tag.get_text(strip=True)
                if re.match(r'^[a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]+\d*$', t, re.IGNORECASE) and len(t) <= 6:
                    pinyin = t
                    break

            def get_sec(title):
                h = sp.find(lambda tag: tag.name in ['h2', 'h3'] and title.lower() in tag.text.lower())
                if not h: return ""
                card = h.find_parent('div', class_=re.compile(r'card|rounded')) or h.parent
                return card.get_text(separator=' | ', strip=True) if card else ""

            return {
                'char': char_str,
                'pinyin': clean_string(pinyin),
                'am_han_viet': clean_string(am_han_viet),
                'nghia_tv': clean_string(nghia_tv),
                'audio': clean_string(audio_link),
                'bo_thu': clean_string(get_sec('Bộ thủ')),
                'loai_tu': clean_string(get_sec('Loại từ')),
                'nghia_tu': clean_string(get_sec('Nghĩa & cách dùng như một từ')),
                'tu_nguyen': clean_string(get_sec('Tự nguyên')),
                'de_nham': clean_string(get_sec('Dễ nhầm')),
                'url': url
            }
        except Exception:
            return {'char': char_str}

    xie_results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        futures = {executor.submit(parse_xiehanzi_live, e['char']): e['char'] for e in missing_entries}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                xie_results[res['char']] = res

    # Chiết tự Gavin Grover
    decomposer = HanziDecomposer()
    
    col_stt_cn = 'STT Chữ Nho Tổng Hợp' if 'STT Chữ Nho Tổng Hợp' in df_excel.columns else 'ChuNhoTongHop_STT (Giáo trình Chữ Nho)'
    col_lk_cn = 'ChuNhoTongHop_LinhKien (Cấu tạo linh kiện)'
    col_gt_cn = 'ChuNhoTongHop_Chietyu_Giaithich (Chiết tự & Giải thích)'

    print(f"\n=== 4. TẠO {len(missing_entries)} HÀNG MỚI ĐẦY ĐỦ CÁC CỘT VÀ NỐI VÀO CỘT A ===", flush=True)
    new_rows = []
    for item in missing_entries:
        c = item['char']
        xie = xie_results.get(c, {})
        
        # Gavin Grover 3 cấp độ
        try: d_once = " | ".join(decomposer.decompose(c, 1))
        except Exception: d_once = ""
        try: d_rad = " | ".join(decomposer.decompose(c, 2))
        except Exception: d_rad = ""
        try: d_graph = " | ".join(decomposer.decompose(c, 3))
        except Exception: d_graph = ""

        row = {col: None for col in df_excel.columns}
        
        # Cột A: Chữ Trung Quốc
        row[col_char] = c
        row['Link'] = f"https://xiehanzi.com/han-tu/{c}/"
        
        # Các cột Chữ Nho Tổng Hợp
        row[col_stt_cn] = item['stt']
        row[col_lk_cn] = item['linh_kien']
        row[col_gt_cn] = item['giai_thich']
        
        # Gavin Grover
        if 'GavinGrover_Once (Chiết tự trực tiếp)' in row: row['GavinGrover_Once (Chiết tự trực tiếp)'] = d_once
        if 'GavinGrover_Radical (Chiết tự bộ thủ)' in row: row['GavinGrover_Radical (Chiết tự bộ thủ)'] = d_rad
        if 'GavinGrover_Graphical (Chiết tự nét vẽ)' in row: row['GavinGrover_Graphical (Chiết tự nét vẽ)'] = d_graph

        # XieHanzi Rich Columns
        if 'Pinyin_Xie' in row: row['Pinyin_Xie'] = xie.get('pinyin', '')
        if 'Âm Hán Việt_Xie' in row: row['Âm Hán Việt_Xie'] = xie.get('am_han_viet', '')
        if 'Nghĩa Tiếng Việt_Xie' in row: row['Nghĩa Tiếng Việt_Xie'] = xie.get('nghia_tv', '')
        if 'Link Âm Thanh_Xie' in row: row['Link Âm Thanh_Xie'] = xie.get('audio', '')
        if 'Bộ thủ & thành phần_Xie' in row: row['Bộ thủ & thành phần_Xie'] = xie.get('bo_thu', '')
        if 'Loại từ & Cách dùng_Xie' in row: row['Loại từ & Cách dùng_Xie'] = xie.get('loai_tu', '')
        if 'Nghĩa & Cách dùng như một từ_Xie' in row: row['Nghĩa & Cách dùng như một từ_Xie'] = xie.get('nghia_tu', '')
        if 'Tự nguyên_Xie' in row: row['Tự nguyên_Xie'] = xie.get('tu_nguyen', '')
        if 'Dễ nhầm & Liên quan_Xie' in row: row['Dễ nhầm & Liên quan_Xie'] = xie.get('de_nham', '')
        
        new_rows.append(row)

    df_new_rows = pd.DataFrame(new_rows)
    df_final = pd.concat([df_excel, df_new_rows], ignore_index=True)
    
    print(f"\n=== 5. XUẤT FILE EXCEL ĐÃ BỔ SUNG (TỔNG CỘNG {len(df_final)} HÀNG) ===", flush=True)
    with pd.ExcelWriter(EXCEL_PATH, engine='openpyxl') as writer:
        df_final.to_excel(writer, index=False)
        
    print(f"THÀNH CÔNG! Đã bổ sung trọn vẹn {len(missing_entries)} chữ Hán còn thiếu từ 'chu_nho_tong_hop.html' vào Cột A và điền đầy đủ các cột tương ứng!", flush=True)

if __name__ == '__main__':
    run()
