import pandas as pd
import sys
import io
import time
from hanzipy.decomposer import HanziDecomposer
from hanzipy.dictionary import HanziDictionary

# Fix stdout encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

FILE_PATH = 'hanzicraft_dashboard_reordered.xlsx'

IDC_SYMBOL_MAP = {
    'a': '<ctrl42>',
    'd': '⿱',
    's': '⿴',
    'st': '⿵',
    'sb': '<ctrl42>',
    'sl': '<ctrl42>',
    'sr': '<ctrl42>',
    'rs': '⿴',
    'r3d': '<ctrl42>',
    'r3a': '<ctrl42>',
    'ba': '<ctrl42>',
    'r3tr': '品',
    'c': ''
}

def get_ids_string(decomposer, char_str):
    info = decomposer.characters.get(char_str, {})
    if not info:
        return char_str
        
    dtype = str(info.get('decomposition_type', '')).strip().lower()
    comps = info.get('components', [])
    
    if not comps or comps == char_str or dtype == 'c':
        return char_str
        
    symbol = ''
    if dtype.startswith('a'):
        symbol = '⿰'
    elif dtype.startswith('d'):
        symbol = '⿱'
    elif dtype.startswith('r3d'):
        symbol = '⿲'
    elif dtype.startswith('r3a') or dtype == 'ba':
        symbol = '⿳'
    elif dtype.startswith('w') or dtype.startswith('s') or dtype.startswith('r'):
        symbol = '⿴'
            
    comps_clean = [str(c) for c in comps if not str(c).isdigit() and c != 'No glyph available']
    comps_str = ''.join(comps_clean)
    
    return f"{symbol}{comps_str}" if symbol else comps_str

def extract_fast_semantic_phonetic(decomposer, char_str):
    info = decomposer.characters.get(char_str, {})
    if not info:
        return '', ''
        
    comps = info.get('components', [])
    clean_comps = [c for c in comps if not str(c).isdigit() and c != 'No glyph available']
    
    if len(clean_comps) < 2:
        return '', ''
        
    c0, c1 = clean_comps[0], clean_comps[1]
    is_rad0 = decomposer.is_radical(c0)
    is_rad1 = decomposer.is_radical(c1)
    
    if is_rad0 and not is_rad1:
        semantic = c0
        phonetic = c1
    elif is_rad1 and not is_rad0:
        semantic = c1
        phonetic = c0
    else:
        # Default: first component is radical/semantic in standard Chinese layout
        semantic = c0
        phonetic = c1
        
    return phonetic, semantic

def run():
    print("Loading Excel data...")
    df = pd.read_excel(FILE_PATH)
    
    print("Initializing CHISE, HanziDecomposer & HanziDictionary engines...")
    t0 = time.time()
    decomposer = HanziDecomposer()
    dictionary = HanziDictionary()
    print(f"Engine ready in {time.time() - t0:.2f}s!")
    
    col_ids = 'CHISE_IDS (Chuỗi Chiết tự Không gian Unicode)'
    col_trad = 'CHISE_Traditional (Chữ Phồn thể)'
    col_phonetic = 'CHISE_Phonetic_Component (Thanh phù - Chỉ Âm)'
    col_semantic = 'CHISE_Semantic_Component (Hình phù - Chỉ Ý)'
    col_similarity = 'CHISE_Visual_Similarity (Hình cận tự & Họ chữ cùng linh kiện)'
    
    ids_list = []
    trad_list = []
    phonetic_list = []
    semantic_list = []
    similarity_list = []
    
    total = len(df)
    print(f"Extracting CHISE spatial IDS, Phonetic/Semantic & Visual Similarity for {total} characters...")
    
    dict_sim = dictionary.dictionary_simplified
    
    for idx, row in df.iterrows():
        char = row['Chữ Trung Quốc']
        
        if pd.isna(char) or str(char).strip() == '' or str(char) == 'nan':
            ids_list.append('')
            trad_list.append('')
            phonetic_list.append('')
            semantic_list.append('')
            similarity_list.append('')
            continue
            
        char_str = str(char).strip()
        
        # 1. Unicode IDS string
        ids_str = get_ids_string(decomposer, char_str)
        
        # 2. Traditional character
        trad_str = char_str
        entries = dict_sim.get(char_str, [])
        if entries and isinstance(entries, list):
            trad_str = entries[0].get('traditional', char_str)
            
        # 3. Phonetic vs Semantic components
        phon_str, sem_str = extract_fast_semantic_phonetic(decomposer, char_str)
        
        # 4. Visual similarity / Family characters sharing component
        try:
            sim_chars = decomposer.get_characters_with_component(char_str)
            if sim_chars and isinstance(sim_chars, list):
                filtered_sim = [c for c in sim_chars if c != char_str][:10]
                sim_str = ', '.join(filtered_sim)
            else:
                sim_str = ''
        except Exception:
            sim_str = ''
            
        ids_list.append(ids_str)
        trad_list.append(trad_str)
        phonetic_list.append(phon_str)
        semantic_list.append(sem_str)
        similarity_list.append(sim_str)
        
        if (idx + 1) % 3000 == 0:
            print(f"--- Đã xử lý {idx + 1}/{total} chữ... ---")
            
    df[col_ids] = ids_list
    df[col_trad] = trad_list
    df[col_phonetic] = phonetic_list
    df[col_semantic] = semantic_list
    df[col_similarity] = similarity_list
    
    print("Saving updated Excel file...")
    with pd.ExcelWriter(FILE_PATH, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        
    print(f"Successfully appended CHISE data (IDS, Traditional, Phonetic/Semantic, Similarity) to {total} rows!")

if __name__ == '__main__':
    run()
