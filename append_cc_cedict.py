import pandas as pd
import sys
import io
import time
from hanzipy.dictionary import HanziDictionary

# Fix stdout encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

FILE_PATH = 'hanzicraft_dashboard_reordered.xlsx'

def format_word_list(word_entries, max_items=8):
    if not word_entries or not isinstance(word_entries, list):
        return ''
    
    formatted = []
    seen = set()
    for item in word_entries:
        simp = item.get('simplified', '')
        pyn = item.get('pinyin', '')
        defn = item.get('definition', '')
        
        if not simp or simp in seen:
            continue
        seen.add(simp)
        
        if pyn and defn:
            formatted.append(f"{simp} [{pyn}] ({defn})")
        else:
            formatted.append(simp)
            
        if len(formatted) >= max_items:
            break
            
    return ' | '.join(formatted)

def run():
    print("Loading Excel data...")
    df = pd.read_excel(FILE_PATH)
    
    print("Initializing CC-CEDICT & Leiden Weibo Dictionary engine...")
    dictionary = HanziDictionary()
    
    print("Pre-building inverted index for 100,000+ dictionary words...")
    t0 = time.time()
    char_to_words = {}
    for word, entries in dictionary.dictionary_simplified.items():
        for c in set(word):
            if c not in char_to_words:
                char_to_words[c] = []
            char_to_words[c].extend(entries)
            
    # Override slow regex search with ultra-fast inverted index
    dictionary.dictionary_search = lambda char, **kwargs: char_to_words.get(char, [])
    print(f"Index built in {time.time() - t0:.2f}s!")
    
    col_pinyin = 'CC-CEDICT_Pinyin'
    col_meaning = 'CC-CEDICT_Meaning (Nghĩa gốc từ điển)'
    col_common = 'CC-CEDICT_Common_Words (Từ ghép Hay Dùng - High)'
    col_uncommon = 'CC-CEDICT_Uncommon_Words (Từ ghép Vừa Dùng - Mid)'
    col_rare = 'CC-CEDICT_Rare_Words (Từ ghép Hiếm Dùng - Low)'
    
    pinyin_list = []
    meaning_list = []
    common_list = []
    uncommon_list = []
    rare_list = []
    
    total = len(df)
    print(f"Extracting CC-CEDICT dictionary & word frequency entries for {total} characters...")
    
    for idx, row in df.iterrows():
        char = row['Chữ Trung Quốc']
        
        if pd.isna(char) or str(char).strip() == '' or str(char) == 'nan':
            pinyin_list.append('')
            meaning_list.append('')
            common_list.append('')
            uncommon_list.append('')
            rare_list.append('')
            continue
            
        char_str = str(char).strip()
        
        # 1. Lookup definition
        try:
            defs = dictionary.definition_lookup(char_str)
            if defs and isinstance(defs, list) and len(defs) > 0:
                pyn = defs[0].get('pinyin', '')
                meanings = ' / '.join([d.get('definition', '') for d in defs if d.get('definition')])
            else:
                pyn, meanings = '', ''
        except Exception:
            pyn, meanings = '', ''
            
        # 2. Lookup word examples categorized by Weibo frequency
        try:
            ex = dictionary.get_examples(char_str)
            if isinstance(ex, dict):
                comm = format_word_list(ex.get('high_frequency', []), max_items=8)
                uncomm = format_word_list(ex.get('mid_frequency', []), max_items=8)
                rare = format_word_list(ex.get('low_frequency', []), max_items=8)
            else:
                comm, uncomm, rare = '', '', ''
        except Exception:
            comm, uncomm, rare = '', '', ''
            
        pinyin_list.append(pyn)
        meaning_list.append(meanings)
        common_list.append(comm)
        uncommon_list.append(uncomm)
        rare_list.append(rare)
        
        if (idx + 1) % 2000 == 0:
            print(f"--- Đã xử lý {idx + 1}/{total} chữ... ---")
            
    df[col_pinyin] = pinyin_list
    df[col_meaning] = meaning_list
    df[col_common] = common_list
    df[col_uncommon] = uncommon_list
    df[col_rare] = rare_list
    
    print("Saving updated Excel file...")
    with pd.ExcelWriter(FILE_PATH, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        
    print(f"Successfully appended CC-CEDICT data and word frequency lists to {total} rows!")

if __name__ == '__main__':
    run()
