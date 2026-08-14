import pandas as pd
import sys
import io
from hanzipy.decomposer import HanziDecomposer

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

FILE_PATH = 'hanzicraft_dashboard_reordered.xlsx'

IDC_MAP = {
    'a': '⿰ (Trái - Phải)',
    'd': '⿱ (Trên - Dưới)',
    'c': 'Chữ đơn thể (Atomic)',
    's': '⿴ (Bao quanh toàn bộ)',
    'st': '⿵ (Bao quanh phía trên)',
    'sb': '⿶ (Bao quanh phía dưới)',
    'sl': '⿷ (Bao quanh phía trái)',
    'sr': '⿹ (Bao quanh góc trên phải)',
    'rs': '⿴ (Bao quanh)',
    'r3d': '⿲ (3 phần hàng ngang)',
    'r3a': '⿳ (3 phần hàng dọc)',
    'ba': '⿳ (3 phần hàng dọc)',
    'r3tr': '品 (Kiến trúc tam giác)',
}

def map_idc(dtype):
    if not dtype:
        return ''
    dtype_clean = str(dtype).strip().lower()
    if dtype_clean in IDC_MAP:
        return IDC_MAP[dtype_clean]
    
    # Fallback heuristic for complex sub-codes
    if dtype_clean.startswith('a'):
        return '⿰ (Trái - Phải)'
    elif dtype_clean.startswith('d'):
        return '⿱ (Trên - Dưới)'
    elif dtype_clean.startswith('w') or dtype_clean.startswith('s') or dtype_clean.startswith('r'):
        return '⿴ (Cấu trúc Bao quanh/Phức hợp)'
    return f"Ký hiệu: {dtype_clean}"

def run():
    print("Loading Excel data...")
    df = pd.read_excel(FILE_PATH)
    
    print("Initializing Gavin Grover HanziDecomposer engine...")
    decomposer = HanziDecomposer()
    
    col_idc_raw = 'GavinGrover_IDC_Raw (Mã IDC thô)'
    col_idc_desc = 'GavinGrover_IDC (Ký hiệu & Cấu trúc không gian)'
    
    raw_list = []
    desc_list = []
    
    total = len(df)
    print(f"Processing Gavin Grover IDC spatial symbols for {total} characters...")
    
    for idx, row in df.iterrows():
        char = row['Chữ Trung Quốc']
        
        if pd.isna(char) or str(char).strip() == '' or str(char) == 'nan':
            raw_list.append('')
            desc_list.append('')
            continue
            
        char_str = str(char).strip()
        
        info = decomposer.characters.get(char_str, {})
        dtype = info.get('decomposition_type', '')
        
        raw_list.append(dtype)
        desc_list.append(map_idc(dtype))
        
    df[col_idc_raw] = raw_list
    df[col_idc_desc] = desc_list
    
    print("Saving updated Excel file...")
    with pd.ExcelWriter(FILE_PATH, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        
    print(f"Successfully appended Gavin Grover IDC spatial symbols to {total} rows!")

if __name__ == '__main__':
    run()
