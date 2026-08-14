import pandas as pd
import sys
import io
import json
from hanzipy.decomposer import HanziDecomposer

# Fix stdout encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

FILE_PATH = 'hanzicraft_dashboard_reordered.xlsx'

def run():
    print("Loading Excel data...")
    df = pd.read_excel(FILE_PATH)
    
    print("Initializing Gavin Grover HanziDecomposer engine...")
    decomposer = HanziDecomposer()
    
    col_once = 'GavinGrover_Once (Chiết tự trực tiếp)'
    col_radical = 'GavinGrover_Radical (Chiết tự bộ thủ)'
    col_graphical = 'GavinGrover_Graphical (Chiết tự nét vẽ)'
    
    once_list = []
    radical_list = []
    graphical_list = []
    
    total = len(df)
    print(f"Processing Gavin Grover decomposition for {total} characters...")
    
    for idx, row in df.iterrows():
        char = row['Chữ Trung Quốc']
        
        if pd.isna(char) or str(char).strip() == '' or str(char) == 'nan':
            once_list.append('')
            radical_list.append('')
            graphical_list.append('')
            continue
            
        char_str = str(char).strip()
        
        try:
            res = decomposer.decompose(char_str)
            if isinstance(res, dict):
                once = ' + '.join(res.get('once', []))
                radical = ' + '.join(res.get('radical', []))
                graphical = ' + '.join(res.get('graphical', []))
            else:
                once, radical, graphical = '', '', ''
        except Exception as e:
            once, radical, graphical = '', '', ''
            
        once_list.append(once)
        radical_list.append(radical)
        graphical_list.append(graphical)
        
    df[col_once] = once_list
    df[col_radical] = radical_list
    df[col_graphical] = graphical_list
    
    print("Saving updated Excel file...")
    with pd.ExcelWriter(FILE_PATH, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        
    print(f"Successfully appended Gavin Grover 3-level decomposition to {total} rows!")

if __name__ == '__main__':
    run()
