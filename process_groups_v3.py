import re
import pandas as pd
import sys
import os

input_file = "raw_groups_v3.txt"
output_file = "hanzicraft_groups_v3.xlsx"

# Regex to match [RootPinyinCharacters](Link)
# Example: [禾he2和禾龢](https://...)
pattern = re.compile(r'\[(.)([a-zA-ZüÜ]+[0-5]?)(.*?)\]\((.*?)\)')

rows = []
group_index = 1

with open(input_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Find all matches
matches = pattern.findall(text)

for match in matches:
    root = match[0]
    pinyin = match[1]
    characters = match[2]
    link = match[3]
    
    num_chars = len(characters)
    
    for char in characters:
        rows.append({
            'Chữ': char,
            'Group': group_index,
            'Num Characters': num_chars,
            'Link': link
        })
        
    group_index += 1

df = pd.DataFrame(rows)

df.to_excel(output_file, index=False)

print(f"Created {output_file} with {len(rows)} rows and {group_index - 1} groups.")
