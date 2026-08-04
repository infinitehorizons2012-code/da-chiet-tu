import pandas as pd

file_reordered = r'C:\Users\DT.HANG\Downloads\DA chiet tu\hanzicraft_dashboard_reordered.xlsx'
file_hsk = r'C:\Users\DT.HANG\Downloads\DA chiet tu\HSK_words.xlsx'

df_reordered = pd.read_excel(file_reordered)
xls_hsk = pd.ExcelFile(file_hsk)

for sheet in xls_hsk.sheet_names:
    df_hsk = pd.read_excel(xls_hsk, sheet_name=sheet)
    # create mapping from Chữ Trung Quốc to STT
    mapping = dict(zip(df_hsk['Chữ Trung Quốc'], df_hsk['STT']))
    # map to new column named after the sheet (e.g. HSK1, HSK2...)
    df_reordered[sheet] = df_reordered['Chữ Trung Quốc'].map(mapping)

# Save the file
with pd.ExcelWriter(file_reordered, engine='openpyxl') as writer:
    df_reordered.to_excel(writer, index=False)
