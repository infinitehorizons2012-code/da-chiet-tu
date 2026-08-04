import re
import pandas as pd
import os

input_file = r'C:\Users\DT.HANG\Downloads\DA chiet tu\hsk1_raw.txt'
output_file = r'C:\Users\DT.HANG\Downloads\DA chiet tu\HSK_words.xlsx'

with open(input_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Pattern for [char](url)number
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

# Create a new file or write to existing one with openpyxl
if os.path.exists(output_file):
    # If the user wants to add multiple sheets later, we can use mode='a'
    # But since it's a new file, we just write it
    pass

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='HSK1', index=False)

print(f"Successfully created {output_file} with sheet 'HSK1' containing {len(rows)} rows.")
