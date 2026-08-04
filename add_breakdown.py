import pandas as pd

file_reordered = r'C:\Users\DT.HANG\Downloads\DA chiet tu\hanzicraft_dashboard_reordered.xlsx'

df = pd.read_excel(file_reordered)

if 'Breakdown' not in df.columns:
    df['Breakdown'] = None

idx = df[df['Chữ Trung Quốc'] == '的'].index
if len(idx) > 0:
    df.loc[idx[0], 'Breakdown'] = '白, 勺'

with pd.ExcelWriter(file_reordered, engine='openpyxl') as writer:
    df.to_excel(writer, index=False)
