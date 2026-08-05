import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random

FILE_PATH = 'hanzicraft_dashboard_reordered.xlsx'
BATCH_SIZE = 9000

def get_section(soup, title_text):
    heading = soup.find(lambda tag: tag.name in ['h2', 'h3'] and title_text.lower() in tag.text.lower())
    if not heading:
        return ""
    
    header_div = heading.parent
    if header_div:
        content_div = header_div.find_next_sibling('div')
        if content_div:
            return content_div.get_text(separator=' | ', strip=True)
    return ""

def parse_character(char):
    url = f'https://xiehanzi.com/han-tu/{char}/'
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            print(f"[{char}] Status code: {r.status_code}")
            return None, None, None, None
            
        soup = BeautifulSoup(r.text, 'html.parser')
        
        bo_thu = get_section(soup, 'Bộ thủ')
        han_viet = get_section(soup, 'Hán-Việt')
        tu_nguyen = get_section(soup, 'Tự nguyên')
        de_nham_lien_quan = get_section(soup, 'Dễ nhầm')
        
        return bo_thu, han_viet, tu_nguyen, de_nham_lien_quan
    except Exception as e:
        print(f"[{char}] Error: {e}")
        return None, None, None, None

import argparse

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--chars', type=str, help='Danh sách các chữ cần cào, cách nhau bởi khoảng trắng')
    args = parser.parse_args()

    print("Loading data...")
    df = pd.read_excel(FILE_PATH)
    
    # Initialize columns if they don't exist
    for col in ['Bộ thủ & thành phần_Xie', 'Hán Việt_Xie', 'Tự nguyên_Xie', 'Dễ nhầm & Liên quan_Xie']:
        if col not in df.columns:
            df[col] = None
            
    if args.chars:
        # User provided manual list
        char_list = args.chars.strip().split()
        print(f"Manual mode: Requested {len(char_list)} characters.")
        
        # Only select rows that match the provided characters
        mask = df['Chữ Trung Quốc'].isin(char_list)
        to_scrape = df[mask]
        
        found_chars = to_scrape['Chữ Trung Quốc'].tolist()
        not_found = set(char_list) - set(found_chars)
        if not_found:
            print(f"Warning: The following characters were not found in Excel: {', '.join(not_found)}")
            
    else:
        # Fallback to automatic mode
        mask = pd.isna(df['Bộ thủ & thành phần_Xie']) | (df['Bộ thủ & thành phần_Xie'] == '')
        to_scrape = df[mask].head(BATCH_SIZE)
        
    if len(to_scrape) == 0:
        print("No valid characters to scrape from XieHanzi!")
        return
        
    print(f"Scraping batch of {len(to_scrape)} characters from XieHanzi...")
    
    for idx, row in to_scrape.iterrows():
        char = row['Chữ Trung Quốc']
        print(f"Processing {char}...")
        
        b, h, t, d = parse_character(char)
        if b or h or t or d:
            df.at[idx, 'Bộ thủ & thành phần_Xie'] = b
            df.at[idx, 'Hán Việt_Xie'] = h
            df.at[idx, 'Tự nguyên_Xie'] = t
            df.at[idx, 'Dễ nhầm & Liên quan_Xie'] = d
            print(f"[{char}] Success.")
        else:
            print(f"[{char}] No data found.")
            
        # Lưu file Excel tạm mỗi 100 chữ để chống mất dữ liệu nếu bị lỗi giữa chừng
        if (idx + 1) % 100 == 0:
            print(f"--- Đã cào được {idx + 1} chữ, tiến hành lưu tạm (Backup)... ---")
            with pd.ExcelWriter(FILE_PATH, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
                
        time.sleep(random.uniform(0.5, 1.5)) # XieHanzi is fast, no need to wait too long
        
    print("Saving to Excel...")
    with pd.ExcelWriter(FILE_PATH, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    print("Done!")

if __name__ == '__main__':
    run()
