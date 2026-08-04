import re
import pandas as pd

input_file = r'C:\Users\DT.HANG\Downloads\DA chiet tu\hsk5_raw.txt'
output_file = r'C:\Users\DT.HANG\Downloads\DA chiet tu\HSK_words.xlsx'

with open(input_file, 'r', encoding='utf-8') as f:
    text = f.read()

pattern = re.compile(r'\[(.*?)\]\((.*?)\)(\d+)')
matches = pattern.findall(text)

rows = []
for match in matches:
    char = match[0]
    link = match[1]
    stt = int(match[2])
    rows.append({
        'Chữ Trung Quốc': char,
        'STT': stt,
        'Link': link
    })

df = pd.DataFrame(rows)

with pd.ExcelWriter(output_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df.to_excel(writer, sheet_name='HSK5', index=False)

print(f"Successfully added sheet 'HSK5' to {output_file} containing {len(rows)} rows.")
