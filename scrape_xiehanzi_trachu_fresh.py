import requests
import bs4
import pandas as pd
import sys
import io
import re
import time
import concurrent.futures
import shutil

# Fix stdout encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_URL = 'https://xiehanzi.com'
OUTPUT_FILE = 'XieHanzi_TraChu_Fresh.xlsx'
TMP_FILE = 'XieHanzi_TraChu_Fresh.tmp.xlsx'
MAX_WORKERS = 15

def clean_string(val):
    if not isinstance(val, str):
        return val
    # Strip illegal ASCII control characters that openpyxl hates
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', val)

def step1_discover_trachu_links():
    print("=== BƯỚC 1: CÀO TRỰC TIẾP TRANG /tra-chu/ ĐỂ LẤY TẤT CẢ DANH MỤC VÀ CHỮ HÁN ===", flush=True)
    start_url = BASE_URL + '/tra-chu/'
    r = requests.get(start_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    
    sub_category_urls = {}
    for a in soup.find_all('a'):
        href = a.get('href', '')
        text = a.get_text(separator=' ', strip=True)
        if href.startswith('/tra-chu/') or href.startswith('/thu-vien-hsk/') or href.startswith('/thu-vien-new-hsk/'):
            full_url = BASE_URL + href if href.startswith('/') else href
            sub_category_urls[full_url] = text
            
    print(f"-> Tìm thấy {len(sub_category_urls)} danh mục con (214 Bộ thủ, HSK...) trên trang /tra-chu/", flush=True)
    
    # Map: char -> dict(char=char, categories=[], url=...)
    discovered_chars = {}
    completed_cats = 0
    total_cats = len(sub_category_urls)
    
    def fetch_cat_page(url_name_tuple):
        cat_url, cat_name = url_name_tuple
        try:
            res = requests.get(cat_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            if res.status_code != 200:
                return []
            sp = bs4.BeautifulSoup(res.text, 'html.parser')
            
            chars_in_page = []
            for a in sp.find_all('a'):
                href = a.get('href', '')
                if '/han-tu/' in href:
                    text = a.get_text(strip=True)
                    c_matches = re.findall(r'[\u4e00-\u9fff]', href + ' ' + text)
                    for c in c_matches:
                        full_char_url = BASE_URL + href if href.startswith('/') else href
                        chars_in_page.append((c, cat_name, full_char_url))
            return chars_in_page
        except Exception as e:
            return []

    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        futures = {executor.submit(fetch_cat_page, item): item for item in sub_category_urls.items()}
        for future in concurrent.futures.as_completed(futures):
            completed_cats += 1
            items = future.result()
            for char, cat_name, char_url in items:
                if char not in discovered_chars:
                    discovered_chars[char] = {
                        'Chữ Hán': char,
                        'Danh Mục Tra Chữ': cat_name,
                        'URL': char_url
                    }
                else:
                    if cat_name and cat_name not in discovered_chars[char]['Danh Mục Tra Chữ']:
                        discovered_chars[char]['Danh Mục Tra Chữ'] += f" | {cat_name}"
                        
            if completed_cats % 30 == 0 or completed_cats == total_cats:
                print(f"--- Đã quét {completed_cats}/{total_cats} danh mục | Tìm thấy {len(discovered_chars)} chữ Hán độc nhất ---", flush=True)
                
    print(f"=== BƯỚC 1 HOÀN TẤT: Tổng cộng phát hiện {len(discovered_chars)} chữ Hán trực tiếp từ trang Tra Cứu XieHanzi! ===", flush=True)
    return list(discovered_chars.values())

def parse_char_details_live(char_info):
    char = char_info['Chữ Hán']
    url = char_info['URL']
    
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        if r.status_code != 200:
            return None
            
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        html_text = r.text
        
        # Audio MP3
        audio_link = ""
        mp3_matches = re.findall(r'(https?://static\.xiehanzi\.com/[^\s"\'<>]+\.mp3)', html_text)
        if mp3_matches:
            audio_link = mp3_matches[0]
            for m in mp3_matches:
                if 'word_audios' in m or 'female' in m or char in m:
                    audio_link = m
                    break
                    
        # Pinyin, Âm Hán Việt, Nghĩa tiếng Việt
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

        # Sections
        def get_sec(title):
            h = soup.find(lambda tag: tag.name in ['h2', 'h3'] and title.lower() in tag.text.lower())
            if not h:
                return ""
            card = h.find_parent('div', class_=re.compile(r'card|rounded')) or h.parent
            return card.get_text(separator=' | ', strip=True) if card else ""

        bo_thu = get_sec('Bộ thủ')
        loai_tu = get_sec('Loại từ')
        nghia_tu = get_sec('Nghĩa & cách dùng như một từ')
        tu_nguyen = get_sec('Tự nguyên')
        de_nham = get_sec('Dễ nhầm')

        return {
            'Chữ Hán': char,
            'Pinyin': clean_string(pinyin),
            'Âm Hán Việt': clean_string(am_han_viet),
            'Nghĩa Tiếng Việt': clean_string(nghia_tv),
            'Link Âm Thanh MP3': clean_string(audio_link),
            'Bộ Thủ & Thành Phần': clean_string(bo_thu),
            'Loại Từ & Cách Dùng Ngữ Pháp': clean_string(loai_tu),
            'Nghĩa & Cách Dùng Như Một Từ': clean_string(nghia_tu),
            'Tự Nguyên (Nguồn Gốc Chữ)': clean_string(tu_nguyen),
            'Dễ Nhầm & Liên Quan': clean_string(de_nham),
            'Danh Mục Tra Cứu': clean_string(char_info['Danh Mục Tra Chữ']),
            'Link XieHanzi': url
        }
    except Exception as e:
        return None

def step2_scrape_all_chars_live(char_list):
    print(f"\n=== BƯỚC 2: CÀO CHI TIẾT TOÀN BỘ {len(char_list)} CHỮ HÁN LIVE TỪ XIEHANZI ===", flush=True)
    
    results = []
    completed = 0
    total = len(char_list)
    t0 = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(parse_char_details_live, item): item for item in char_list}
        
        for future in concurrent.futures.as_completed(futures):
            completed += 1
            res = future.result()
            if res:
                results.append(res)
                
            if completed % 200 == 0 or completed == total:
                elapsed = time.time() - t0
                speed = completed / elapsed if elapsed > 0 else 0
                print(f"--- Đã cào chi tiết {completed}/{total} chữ Hán ({speed:.1f} chữ/giây). Đang sao lưu tạm vào Excel... ---", flush=True)
                
                df_temp = pd.DataFrame(results)
                df_temp.insert(0, 'STT', range(1, len(df_temp) + 1))
                with pd.ExcelWriter(TMP_FILE, engine='openpyxl') as writer:
                    df_temp.to_excel(writer, index=False)
                shutil.move(TMP_FILE, OUTPUT_FILE)
                print("--- Lưu tạm Excel thành công! ---", flush=True)
                
    df_final = pd.DataFrame(results)
    df_final.insert(0, 'STT', range(1, len(df_final) + 1))
    with pd.ExcelWriter(TMP_FILE, engine='openpyxl') as writer:
        df_final.to_excel(writer, index=False)
    shutil.move(TMP_FILE, OUTPUT_FILE)
    print(f"\n=== THÀNH CÔNG! Đã cào tươi 100% {len(df_final)} chữ Hán và lưu vào {OUTPUT_FILE} ===", flush=True)

if __name__ == '__main__':
    discovered = step1_discover_trachu_links()
    step2_scrape_all_chars_live(discovered)
