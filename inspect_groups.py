import pandas as pd
file_groups = r'C:\Users\DT.HANG\Downloads\DA chiet tu\hanzicraft_groups.xlsx'
df = pd.read_excel(file_groups)
with open('inspect_groups.txt', 'w', encoding='utf-8') as f:
    f.write(str(df.head()) + '\n\n' + str(df.columns))
