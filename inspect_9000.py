import pandas as pd

file_9000 = r'C:\Users\DT.HANG\Downloads\DA chiet tu\hanzicraft_9000.xlsx'
df = pd.read_excel(file_9000)

with open('inspect_9000.txt', 'w', encoding='utf-8') as f:
    f.write(str(df.head()) + '\n\n' + str(df.columns))
