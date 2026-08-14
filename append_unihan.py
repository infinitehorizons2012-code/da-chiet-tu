import pandas as pd
import sys
import io
import time
from hanzipy.dictionary import HanziDictionary

# Fix stdout encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

FILE_PATH = 'hanzicraft_dashboard_reordered.xlsx'

def get_unihan_variants(dictionary, char_str):
    # Unicode Hex CodePoint
    if len(char_str) == 1:
        hex_code = f"U+{ord(char_str):04X}"
    else:
        hex_code = ', '.join([f"U+{ord(c):04X}" for c in char_str])
        
    simplified = char_str
    traditional = char_str
    
    # 1. Lookup in simplified dictionary
    entries_simp = dictionary.dictionary_simplified.get(char_str, [])
    if entries_simp and isinstance(entries_simp, list):
        traditional = entries_simp[0].get('traditional', char_str)
        simplified = entries_simp[0].get('simplified', char_str)
    else:
        # 2. Lookup in traditional dictionary
        entries_trad = dictionary.dictionary_traditional.get(char_str, [])
        if entries_trad and isinstance(entries_trad, list):
            simplified = entries_trad[0].get('simplified', char_str)
            traditional = entries_trad[0].get('traditional', char_str)
            
    return hex_code, simplified, traditional

def run():
    print("Loading Excel data...")
    df = pd.read_excel(FILE_PATH)
    
    print("Initializing Unihan & HanziDictionary engine...")
    t0 = time.time()
    dictionary = HanziDictionary()
    print(f"Unihan engine ready in {time.time() - t0:.2f}s!")
    
    col_hex = 'Unihan_Unicode_Hex'
    col_simp = 'Unihan_Simplified (Chữ Giản thể)'
    col_trad = 'Unihan_Traditional (Chữ Phồn thể)'
    
    hex_list = []
    simp_list = []
    trad_list = []
    
    total = len(df)
    print(f"Extracting Unihan Unicode Hex, Simplified & Traditional variants for {total} characters...")
    
    for idx, row in df.iterrows():
        char = row['Chữ Trung Quốc']
        
        if pd.isna(char) or str(char).strip() == '' or str(char) == 'nan':
            hex_list.append('')
            simp_list.append('')
            trad_list.append('')
            continue
            
        char_str = str(char).strip()
        
        hex_code, simplified, traditional = get_unihan_variants(dictionary, char_str)
        
        hex_list.append(hex_code)
        simp_list.append(simplified)
        trad_list.append(traditional)
        
        if (idx + 1) % 4000 == 0:
            print(f"--- Đã xử lý {idx + 1}/{total} chữ... ---")
            
    df[col_hex] = hex_list
    df[col_simp] = simp_list
    df[col_trad] = trad_list
    
    print("Saving updated Excel file...")
    with pd.ExcelWriter(FILE_PATH, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        
    print(f"Successfully appended Unihan data (Unicode Hex, Simplified, Traditional) to {total} rows!")

if __name__ == '__main__':
    run()
