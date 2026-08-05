import pandas as pd
from hanzipy.dictionary import HanziDictionary

excel_file = 'hanzicraft_dashboard_reordered.xlsx'

def run():
    print("Loading HanziDictionary...")
    hd = HanziDictionary()
    
    print("Loading Excel...")
    df = pd.read_excel(excel_file)
    
    if 'Hạng Tần Suất (Jun Da)' not in df.columns:
        df['Hạng Tần Suất (Jun Da)'] = None
    if 'Tần Suất % (Jun Da)' not in df.columns:
        df['Tần Suất % (Jun Da)'] = None
        
    def get_rank(row):
        char = row['Chữ Trung Quốc']
        try:
            res = hd.get_character_frequency(char)
            if res != 'Character not found':
                return int(res['number'])
        except Exception:
            pass
        return None
        
    def get_freq(row):
        char = row['Chữ Trung Quốc']
        try:
            res = hd.get_character_frequency(char)
            if res != 'Character not found':
                return float(res['percentage'])
        except Exception:
            pass
        return None
        
    print("Applying frequencies...")
    df['Hạng Tần Suất (Jun Da)'] = df.apply(get_rank, axis=1)
    df['Tần Suất % (Jun Da)'] = df.apply(get_freq, axis=1)
    
    print("Saving to Excel...")
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        
    print("Done!")

if __name__ == '__main__':
    run()
