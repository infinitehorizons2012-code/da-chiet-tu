import pandas as pd
from playwright.sync_api import sync_playwright
import time
import random
import os

FILE_PATH = 'hanzicraft_dashboard_reordered.xlsx'
BATCH_SIZE = 50

def parse_character(page, char):
    try:
        page.goto(f'https://hanzicraft.com/character/{char}', wait_until='domcontentloaded', timeout=15000)
        # Check for cloudflare
        if "Just a moment..." in page.title():
            print(f"[{char}] Cloudflare detected, waiting a bit...")
            page.wait_for_timeout(5000)
            
        page.wait_for_selector('.decomp-row', timeout=10000)
        
        breakdown_str = ""
        components_str = ""
        
        rows = page.query_selector_all('.decomp-row')
        for row in rows:
            label = row.query_selector('.decomp-label')
            if not label:
                continue
            text = label.inner_text()
            
            if 'Breakdown' in text:
                dtree = row.query_selector('.dtree')
                if dtree:
                    boxes = dtree.query_selector_all('.dtree-box')
                    # Just grab all text from boxes, except the first one if it's the root char
                    chars = [b.inner_text() for b in boxes]
                    # Hanzicraft tree structure can be complex, let's just join them
                    breakdown_str = ", ".join(chars)
                    
            elif 'Components' in text:
                comps = row.query_selector('.decomp-components')
                if comps:
                    tiles = comps.query_selector_all('.decomp-tile')
                    comp_list = []
                    for t in tiles:
                        c_char = t.query_selector('.decomp-tile-char')
                        c_mean = t.query_selector('.decomp-tile-meaning')
                        c_text = c_char.inner_text() if c_char else ""
                        m_text = c_mean.inner_text() if c_mean else "N/A"
                        comp_list.append(f"{c_text} {m_text}")
                    components_str = ", ".join(comp_list)
                    
        return breakdown_str, components_str
    except Exception as e:
        print(f"[{char}] Error: {e}")
        return None, None

def run():
    print("Loading data...")
    df = pd.read_excel(FILE_PATH)
    
    if 'Components_Hanzicraft' not in df.columns:
        df['Components_Hanzicraft'] = None
    if 'Breakdown' not in df.columns:
        df['Breakdown'] = None
        
    # Find rows that need scraping
    mask = pd.isna(df['Components_Hanzicraft']) | (df['Components_Hanzicraft'] == '')
    to_scrape = df[mask]
    
    if len(to_scrape) == 0:
        print("All characters have been scraped!")
        return
        
    to_scrape = to_scrape.head(BATCH_SIZE)
    print(f"Scraping batch of {len(to_scrape)} characters...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        for idx, row in to_scrape.iterrows():
            char = row['Chữ Trung Quốc']
            print(f"Processing {char}...")
            
            b, c = parse_character(page, char)
            if b is not None or c is not None:
                df.at[idx, 'Breakdown'] = b
                df.at[idx, 'Components_Hanzicraft'] = c
                print(f"[{char}] Breakdown: {b} | Components: {c}")
            
            time.sleep(random.uniform(2, 5))
            
        browser.close()
        
    print("Saving to Excel...")
    with pd.ExcelWriter(FILE_PATH, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    print("Done!")

if __name__ == '__main__':
    run()
