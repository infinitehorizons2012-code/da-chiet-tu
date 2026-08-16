import pandas as pd
file_groups_v4 = r'C:\Users\DT.HANG\Downloads\DA chiet tu\hanzicraft_groups_v4.xlsx'
df = pd.read_excel(file_groups_v4)
with open('inspect_groups_v4.txt', 'w', encoding='utf-8') as f:
    f.write(str(df.head()) + '\n\n' + str(df.columns))
