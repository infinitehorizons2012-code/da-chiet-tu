import pandas as pd
import re
import os

input_file = "raw_input.txt"
excel_file = "hanzicraft_9000.xlsx"

with open(input_file, 'r', encoding='utf-8') as f:
    text = f.read()

pattern = re.compile(r'\[(.*?)\]\((.*?)\)(\d+)')
matches = pattern.findall(text)

new_data = []
for char, url, stt in matches:
    new_data.append({"STT": int(stt), "Chữ Hán": char, "Link": url})

df_new = pd.DataFrame(new_data)

if os.path.exists(excel_file):
    df_old = pd.read_excel(excel_file)
    df_combined = pd.concat([df_old, df_new]).drop_duplicates(subset=['STT'], keep='last').sort_values('STT')
else:
    df_combined = df_new.sort_values('STT')

cols = ['STT', 'Chữ Hán', 'Link']
for col in cols:
    if col not in df_combined.columns:
        df_combined[col] = ""
df_combined = df_combined[cols]

df_combined.to_excel(excel_file, index=False)
print(f"Added {len(new_data)} characters. Total characters in Excel 9000: {len(df_combined)}")
