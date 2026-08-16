import pandas as pd
file_hsk = r'C:\Users\DT.HANG\Downloads\DA chiet tu\HSK_words.xlsx'
xls = pd.ExcelFile(file_hsk)
sheet_names = xls.sheet_names

out = f"Sheets: {sheet_names}\n\n"
for sheet in sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet)
    out += f"Sheet '{sheet}' columns: {list(df.columns)}\n"

with open('inspect_hsk.txt', 'w', encoding='utf-8') as f:
    f.write(out)
