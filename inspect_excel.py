import pandas as pd
df = pd.read_excel(r'C:\Users\DT.HANG\Downloads\DA chiet tu\hanzicraft_dashboard.xlsx')
with open('inspect_excel.txt', 'w', encoding='utf-8') as f:
    f.write(str(df.head()) + '\n\n' + str(df.columns))
