import pandas as pd
from bs4 import BeautifulSoup
import os

html_file = 'chu_nho_tong_hop.html'
excel_file = 'hanzicraft_dashboard_reordered.xlsx'

def run():
    print("Reading HTML file...")
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    char_to_stt = {}
    
    # Find all table rows
    rows = soup.find_all('tr')
    for row in rows:
        stt_td = row.find('td', class_='stt')
        char_td = row.find('td', class_='char')
        
        if stt_td and char_td:
            stt = stt_td.text.strip()
            char = char_td.text.strip()
            if stt and char:
                # Store the STT (some characters might appear multiple times or STT might be string, just keep first or overwrite)
                char_to_stt[char] = stt

    print(f"Extracted {len(char_to_stt)} characters from HTML.")
    
    print("Loading Excel file...")
    df = pd.read_excel(excel_file)
    
    # Create column if not exists
    if 'STT Chữ Nho Tổng Hợp' not in df.columns:
        df['STT Chữ Nho Tổng Hợp'] = None
        
    # Map the STT
    def map_stt(row):
        char = row['Chữ Trung Quốc']
        return char_to_stt.get(char, None)
        
    df['STT Chữ Nho Tổng Hợp'] = df.apply(map_stt, axis=1)
    
    # Optional: order the columns so it's next to Chữ Trung Quốc or somewhere visible
    # Or just keep it at the end. We'll just keep it at the end as pandas does by default.
    
    print("Saving to Excel...")
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        
    print("Done!")

if __name__ == '__main__':
    run()
