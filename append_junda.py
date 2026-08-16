import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

excel_file = 'hanzicraft_dashboard_reordered.xlsx'

def run():
    print("Scraping Jun Da frequency data from MTSU...")
    char_data = {}
    
    # 3 pages
    urls = [
        "https://lingua.mtsu.edu/chinese-computing/statistics/char/list.php?Which=MO",
        "https://lingua.mtsu.edu/chinese-computing/statistics/char/list.php?Which=MO&cpage=2",
        "https://lingua.mtsu.edu/chinese-computing/statistics/char/list.php?Which=MO&cpage=3"
    ]
    
    for u in urls:
        print(f"Fetching {u}...")
        try:
            resp = requests.get(u, verify=False, timeout=15)
            # Find charset or just use gb2312/gbk
            resp.encoding = 'gbk' 
            soup = BeautifulSoup(resp.text, "html.parser")
            
            tables = soup.find_all('table')
            target_table = None
            for t in tables:
                if len(t.find_all('tr')) > 500:
                    target_table = t
                    break
                    
            if not target_table:
                print(f"Could not find the main table on page {u}!")
                continue
                
            rows = target_table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 5:
                    try:
                        rank = cols[0].text.strip()
                        char = cols[1].text.strip()
                        pct = cols[3].text.strip()
                        
                        if rank.isdigit() and char:
                            char_data[char] = {
                                'Hạng Tần Suất (Jun Da)': int(rank),
                                'Tần Suất % (Jun Da)': float(pct) if pct else None
                            }
                    except Exception:
                        pass
        except Exception as e:
            print(f"Failed to fetch {u}: {e}")
            
    print(f"Extracted frequency for {len(char_data)} characters.")
    
    print("Loading Excel...")
    df = pd.read_excel(excel_file)
    
    if 'Hạng Tần Suất (Jun Da)' not in df.columns:
        df['Hạng Tần Suất (Jun Da)'] = None
    if 'Tần Suất % (Jun Da)' not in df.columns:
        df['Tần Suất % (Jun Da)'] = None
        
    def get_rank(row):
        char = row['Chữ Trung Quốc']
        return char_data.get(char, {}).get('Hạng Tần Suất (Jun Da)')
        
    def get_freq(row):
        char = row['Chữ Trung Quốc']
        return char_data.get(char, {}).get('Tần Suất % (Jun Da)')
        
    df['Hạng Tần Suất (Jun Da)'] = df.apply(get_rank, axis=1)
    df['Tần Suất % (Jun Da)'] = df.apply(get_freq, axis=1)
    
    print("Saving to Excel...")
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        
    print("Done!")

if __name__ == '__main__':
    run()
