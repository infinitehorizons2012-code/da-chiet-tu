import pandas as pd
import requests
import bs4
import time
import sys
import io
import re
import concurrent.futures

# Fix stdout encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

FILE_PATH = 'hanzicraft_dashboard_reordered.xlsx'
MAX_WORKERS = 15

def clean_string(val):
    if not isinstance(val, str):
        return val
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', val)

def parse_xiehanzi_full(char):
    if pd.isna(char) or str(char).strip() == '' or str(char) == 'nan':
        return None
        
    char_str = str(char).strip()
    url = f'https://xiehanzi.com/han-tu/{char_str}/'
    
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        if r.status_code != 200:
            return {
                'char': char_str,
                'pinyin': 'N/A',
                'am_han_viet': 'N/A',
                'nghia_tv': 'N/A',
                'audio': '',
                'loai_tu': 'N/A',
                'nghia_cach_dung_tu': 'N/A'
            }
            
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        html_text = r.text
        
        # 1. Audio MP3 Link
        audio_link = ""
        mp3_matches = re.findall(r'(https?://static\.xiehanzi\.com/[^\s"\'<>]+\.mp3)', html_text)
        if mp3_matches:
            audio_link = mp3_matches[0]
            for m in mp3_matches:
                if 'word_audios' in m or 'female' in m or char_str in m:
                    audio_link = m
                    break
                    
        # 2. Pinyin, Âm Hán Việt, Nghĩa Tiếng Việt
        pinyin = ""
        am_han_viet = ""
        nghia_tv = ""
        
        text_blocks = [tag.get_text(separator=' | ', strip=True) for tag in soup.find_all(['div', 'p', 'span', 'header'])]
        for block in text_blocks:
            if 'Nghĩa tiếng Việt' in block and not nghia_tv:
                m = re.search(r'Nghĩa tiếng Việt\s*\|\s*([^\|]+)', block)
                if m:
                    nghia_tv = m.group(1).strip()
            if 'Âm Hán Việt' in block and not am_han_viet:
                m = re.search(r'Âm Hán Việt\s*\|\s*([^\|]+)', block)
                if m:
                    am_han_viet = m.group(1).strip()

        for tag in soup.find_all(['span', 'div', 'p']):
            t = tag.get_text(strip=True)
            if re.match(r'^[a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]+\d*$', t, re.IGNORECASE) and len(t) <= 6:
                pinyin = t
                break

        # 3. Loại từ & cách dùng
        loai_tu_cach_dung = ""
        h3_loaitu = soup.find(lambda t: t.name in ['h2', 'h3'] and 'Loại từ' in t.text)
        if h3_loaitu:
            card = h3_loaitu.find_parent('div', class_=re.compile(r'card|rounded')) or h3_loaitu.parent
            if card:
                loai_tu_cach_dung = card.get_text(separator=' | ', strip=True)

        # 4. Nghĩa & cách dùng như một từ
        nghia_cach_dung_tu = ""
        h3_nghia = soup.find(lambda t: t.name in ['h2', 'h3'] and 'Nghĩa & cách dùng như một từ' in t.text)
        if h3_nghia:
            card = h3_nghia.find_parent('div', class_=re.compile(r'card|rounded')) or h3_nghia.parent
            if card:
                nghia_cach_dung_tu = card.get_text(separator=' | ', strip=True)

        return {
            'char': char_str,
            'pinyin': clean_string(pinyin),
            'am_han_viet': clean_string(am_han_viet),
            'nghia_tv': clean_string(nghia_tv),
            'audio': clean_string(audio_link),
            'loai_tu': clean_string(loai_tu_cach_dung),
            'nghia_cach_dung_tu': clean_string(nghia_cach_dung_tu)
        }
    except Exception as e:
        return {
            'char': char_str,
            'pinyin': '',
            'am_han_viet': '',
            'nghia_tv': '',
            'audio': '',
            'loai_tu': '',
            'nghia_cach_dung_tu': ''
        }

def run():
    print("Loading Excel data...")
    df = pd.read_excel(FILE_PATH)
    
    col_pinyin = 'Pinyin_Xie'
    col_hanviet = 'Âm Hán Việt_Xie'
    col_nghiatv = 'Nghĩa Tiếng Việt_Xie'
    col_audio = 'Link Âm Thanh_Xie'
    col_loaitu = 'Loại từ & Cách dùng_Xie'
    col_nghiatu = 'Nghĩa & Cách dùng như một từ_Xie'
    
    # Initialize columns if missing
    for c in [col_pinyin, col_hanviet, col_nghiatv, col_audio, col_loaitu, col_nghiatu]:
        if c not in df.columns:
            df[c] = None
            
    # Skip rows already scraped
    mask = pd.isna(df[col_audio]) | (df[col_audio] == '')
    indices_to_scrape = df[mask].index.tolist()
    
    total_to_do = len(indices_to_scrape)
    if total_to_do == 0:
        print("All rows are already scraped!", flush=True)
        return

    print(f"Scraping rich XieHanzi data for {total_to_do} remaining characters using {MAX_WORKERS} parallel threads...", flush=True)
    
    t0 = time.time()
    completed = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_idx = {executor.submit(parse_xiehanzi_full, df.at[idx, 'Chữ Trung Quốc']): idx for idx in indices_to_scrape}
        
        for future in concurrent.futures.as_completed(future_to_idx):
            idx = future_to_idx[future]
            completed += 1
            try:
                res = future.result()
                if res:
                    df.at[idx, col_pinyin] = res['pinyin']
                    df.at[idx, col_hanviet] = res['am_han_viet'] if res['am_han_viet'] else df.at[idx, 'Hán Việt_Xie']
                    df.at[idx, col_nghiatv] = res['nghia_tv']
                    df.at[idx, col_audio] = res['audio']
                    df.at[idx, col_loaitu] = res['loai_tu']
                    df.at[idx, col_nghiatu] = res['nghia_cach_dung_tu']
            except Exception as e:
                pass
                
            if completed % 500 == 0 or completed == total_to_do:
                elapsed = time.time() - t0
                speed = completed / elapsed if elapsed > 0 else 0
                print(f"--- Đã cào {completed}/{total_to_do} chữ ({speed:.1f} chữ/giây). Đang lưu tạm vào Excel... ---", flush=True)
                tmp_file = FILE_PATH + '.tmp.xlsx'
                with pd.ExcelWriter(tmp_file, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                import shutil
                shutil.move(tmp_file, FILE_PATH)
                print("--- Lưu tạm thành công! ---", flush=True)
                
    print("Saving final Excel file...", flush=True)
    tmp_file = FILE_PATH + '.tmp.xlsx'
    with pd.ExcelWriter(tmp_file, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    import shutil
    shutil.move(tmp_file, FILE_PATH)
    print(f"Successfully scraped and appended all XieHanzi rich columns for {total_to_do} characters!", flush=True)

if __name__ == '__main__':
    run()
