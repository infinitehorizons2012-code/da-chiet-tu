import pandas as pd
file_words = r'C:\Users\DT.HANG\Downloads\DA chiet tu\hanzicraft_words.xlsx'
df = pd.read_excel(file_words)
with open('inspect_words.txt', 'w', encoding='utf-8') as f:
    f.write(str(df.head()) + '\n\n' + str(df.columns))
