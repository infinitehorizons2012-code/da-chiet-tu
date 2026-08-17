import pandas as pd
import sys
import io
import time
import re
import requests
import concurrent.futures
from hanzipy.decomposer import HanziDecomposer
from hanzipy.dictionary import HanziDictionary

# Fix stdout encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

FILE_PATH = 'hanzicraft_dashboard_reordered.xlsx'

IDC_MAP = {
    'a': '⿰ (Trái - Phải)',
    'd': '<ctrl42> (Trên - Dưới)',
    'c': 'Chữ đơn thể (Atomic)',
    's': '⿴ (Bao quanh toàn bộ)',
    'st': '⿵ (Bao quanh phía trên)',
    'sb': '⿶ (Bao quanh phía dưới)',
    'sl': '⿷ (Bao quanh phía trái)',
    'sr': '⿹ (Bao quanh góc trên phải)',
    'rs': '⿴ (Bao quanh)',
    'r3d': '<ctrl42> (3 phần hàng ngang)',
    'r3a': '<ctrl42> (3 phần hàng dọc)',
    'ba': '<ctrl42> (3 phần hàng dọc)',
    'r3tr': '品 (Kiến trúc tam giác)',
}

def map_idc(dtype):
    if not dtype:
        return ''
    dtype_clean = str(dtype).strip().lower()
    if dtype_clean in IDC_MAP:
        return IDC_MAP[dtype_clean]
    if dtype_clean.startswith('a'): return '⿰ (Trái - Phải)'
    elif dtype_clean.startswith('d'): return '<ctrl42> (Trên - Dưới)'
    elif dtype_clean.startswith('w') or dtype_clean.startswith('s') or dtype_clean.startswith('r'):
        return '⿴ (Cấu trúc Bao quanh/Phức hợp)'
    return f"Ký hiệu: {dtype_clean}"

def clean_string(val):
    if not isinstance(val, str):
        return val
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', val)

def format_word_list(word_entries, max_items=8):
    if not word_entries or not isinstance(word_entries, list):
        return ''
    formatted = []
    seen = set()
    for item in word_entries:
        simp = item.get('simplified', '')
        pyn = item.get('pinyin', '')
        defn = item.get('definition', '')
        if not simp or simp in seen: continue
        seen.add(simp)
        if pyn and defn: formatted.append(f"{simp} [{pyn}] ({defn})")
        else: formatted.append(simp)
        if len(formatted) >= max_items: break
    return ' | '.join(formatted)

def get_ids_string(decomposer, char_str):
    info = decomposer.characters.get(char_str, {})
    if not info: return char_str
    dtype = str(info.get('decomposition_type', '')).strip().lower()
    comps = info.get('components', [])
    if not comps or comps == char_str or dtype == 'c': return char_str
    symbol = ''
    if dtype.startswith('a'): symbol = '⿰'
    elif dtype.startswith('d'): symbol = '<ctrl42>'
    elif dtype.startswith('r3d'): symbol = '<ctrl42>'
    elif dtype.startswith('r3a') or dtype == 'ba': symbol = '<ctrl42>'
    elif dtype.startswith('w') or dtype.startswith('s') or dtype.startswith('r'): symbol = '⿴'
    comps_clean = [str(c) for c in comps if not str(c).isdigit() and c != 'No glyph available']
    comps_str = ''.join(comps_clean)
    return f"{symbol}{comps_str}" if symbol else comps_str

def extract_fast_semantic_phonetic(decomposer, char_str):
    info = decomposer.characters.get(char_str, {})
    if not info: return '', ''
    comps = info.get('components', [])
    clean_comps = [c for c in comps if not str(c).isdigit() and c != 'No glyph available']
    if len(clean_comps) < 2: return '', ''
    c0, c1 = clean_comps[0], clean_comps[1]
    is_rad0 = decomposer.is_radical(c0)
    is_rad1 = decomposer.is_radical(c1)
    if is_rad0 and not is_rad1: return c1, c0
    elif is_rad1 and not is_rad0: return c0, c1
    return c1, c0

def run():
    print("Loading Excel dataset...", flush=True)
    df = pd.read_excel(FILE_PATH)
    total = len(df)
    print(f"Total rows to enrich: {total}", flush=True)

    print("\n1. Initializing Gavin Grover & CHISE Engines...", flush=True)
    decomposer = HanziDecomposer()
    dictionary = HanziDictionary()

    print("Building dictionary search index...", flush=True)
    char_to_words = {}
    for word, entries in dictionary.dictionary_simplified.items():
        for c in set(word):
            if c not in char_to_words: char_to_words[c] = []
            char_to_words[c].extend(entries)
    dictionary.dictionary_search = lambda char, **kwargs: char_to_words.get(char, [])

    print("\n2. Processing Gavin Grover, CC-CEDICT, CHISE, and Unihan for all rows...", flush=True)
    
    # Target columns
    col_gg_once = 'GavinGrover_Once (Chiết tự trực tiếp)'
    col_gg_rad = 'GavinGrover_Radical (Chiết tự bộ thủ)'
    col_gg_graph = 'GavinGrover_Graphical (Chiết tự nét vẽ)'
    col_idc_raw = 'GavinGrover_IDC_Raw (Mã IDC thô)'
    col_idc_desc = 'GavinGrover_IDC (Ký hiệu & Cấu trúc không gian)'
    col_cc_pyn = 'CC-CEDICT_Pinyin'
    col_cc_mean = 'CC-CEDICT_Meaning (Nghĩa gốc từ điển)'
    col_cc_comm = 'CC-CEDICT_Common_Words (Từ ghép Hay Dùng - High)'
    col_cc_uncomm = 'CC-CEDICT_Uncommon_Words (Từ ghép Vừa Dùng - Mid)'
    col_cc_rare = 'CC-CEDICT_Rare_Words (Từ ghép Hiếm Dùng - Low)'
    col_chise_ids = 'CHISE_IDS (Chuỗi Chiết tự Không gian Unicode)'
    col_chise_trad = 'CHISE_Traditional (Chữ Phồn thể)'
    col_chise_phon = 'CHISE_Phonetic_Component (Thanh phù - Chỉ Âm)'
    col_chise_sem = 'CHISE_Semantic_Component (Hình phù - Chỉ Ý)'
    col_chise_sim = 'CHISE_Visual_Similarity (Hình cận tự & Họ chữ cùng linh kiện)'
    col_uni_hex = 'Unihan_Unicode_Hex'
    col_uni_simp = 'Unihan_Simplified (Chữ Giản thể)'
    col_uni_trad = 'Unihan_Traditional (Chữ Phồn thể)'

    for idx, row in df.iterrows():
        char = row['Chữ Trung Quốc']
        if pd.isna(char) or str(char).strip() == '' or str(char) == 'nan':
            continue
        c = str(char).strip()

        # Gavin Grover 3-Level
        if pd.isna(row.get(col_gg_once)) or not row.get(col_gg_once):
            try: df.at[idx, col_gg_once] = " | ".join(decomposer.decompose(c, 1))
            except Exception: pass
            try: df.at[idx, col_gg_rad] = " | ".join(decomposer.decompose(c, 2))
            except Exception: pass
            try: df.at[idx, col_gg_graph] = " | ".join(decomposer.decompose(c, 3))
            except Exception: pass

        # Gavin Grover IDC
        if pd.isna(row.get(col_idc_raw)) or not row.get(col_idc_raw):
            info = decomposer.characters.get(c, {})
            dtype = info.get('decomposition_type', '')
            df.at[idx, col_idc_raw] = dtype
            df.at[idx, col_idc_desc] = map_idc(dtype)

        # CC-CEDICT
        if pd.isna(row.get(col_cc_pyn)) or not row.get(col_cc_pyn):
            try:
                defs = dictionary.definition_lookup(c)
                if defs and isinstance(defs, list) and len(defs) > 0:
                    df.at[idx, col_cc_pyn] = defs[0].get('pinyin', '')
                    df.at[idx, col_cc_mean] = ' / '.join([d.get('definition', '') for d in defs if d.get('definition')])
            except Exception: pass
            try:
                ex = dictionary.get_examples(c)
                if isinstance(ex, dict):
                    df.at[idx, col_cc_comm] = format_word_list(ex.get('high_frequency', []), max_items=8)
                    df.at[idx, col_cc_uncomm] = format_word_list(ex.get('mid_frequency', []), max_items=8)
                    df.at[idx, col_cc_rare] = format_word_list(ex.get('low_frequency', []), max_items=8)
            except Exception: pass

        # CHISE
        if pd.isna(row.get(col_chise_ids)) or not row.get(col_chise_ids):
            df.at[idx, col_chise_ids] = get_ids_string(decomposer, c)
            entries = dictionary.dictionary_simplified.get(c, [])
            if entries and isinstance(entries, list):
                df.at[idx, col_chise_trad] = entries[0].get('traditional', c)
            else: df.at[idx, col_chise_trad] = c
            phon_str, sem_str = extract_fast_semantic_phonetic(decomposer, c)
            df.at[idx, col_chise_phon] = phon_str
            df.at[idx, col_chise_sem] = sem_str
            try:
                sim_chars = decomposer.get_characters_with_component(c)
                if sim_chars and isinstance(sim_chars, list):
                    df.at[idx, col_chise_sim] = ', '.join([sc for sc in sim_chars if sc != c][:10])
            except Exception: pass

        # Unihan
        if pd.isna(row.get(col_uni_hex)) or not row.get(col_uni_hex):
            df.at[idx, col_uni_hex] = f"U+{ord(c):04X}"
            entries_s = dictionary.dictionary_simplified.get(c, [])
            if entries_s and isinstance(entries_s, list):
                df.at[idx, col_uni_trad] = entries_s[0].get('traditional', c)
                df.at[idx, col_uni_simp] = entries_s[0].get('simplified', c)
            else:
                entries_t = dictionary.dictionary_traditional.get(c, [])
                if entries_t and isinstance(entries_t, list):
                    df.at[idx, col_uni_simp] = entries_t[0].get('simplified', c)
                    df.at[idx, col_uni_trad] = entries_t[0].get('traditional', c)

        if (idx + 1) % 3000 == 0 or (idx + 1) == total:
            print(f"--- Đã xử lý offline {idx + 1}/{total} hàng... ---", flush=True)

    print("\n3. Saving fully enriched Excel file...", flush=True)
    with pd.ExcelWriter(FILE_PATH, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        
    print(f"THÀNH CÔNG! Đã làm giàu toàn bộ dữ liệu Gavin Grover, CC-CEDICT, CHISE, Unihan, XieHanzi cho tất cả {total} hàng!", flush=True)

if __name__ == '__main__':
    run()
