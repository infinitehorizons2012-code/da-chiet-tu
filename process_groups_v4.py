import re
import pandas as pd

input_file = "raw_groups_v4.txt"
output_file = "hanzicraft_groups_v4.xlsx"

# Regex to match [1人942 characters](Link)
# E.g. [23戈矛201 characters](https://hanzicraft.com/dashboard/character/%E6%88%88%E7%9F%9B)
pattern = re.compile(r'\[(\d+)(.+?)(\d+)\s+characters\]\((.*?)\)')

rows = []

with open(input_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Find all matches
matches = pattern.findall(text)

for match in matches:
    group_index = int(match[0])
    roots = match[1]
    num_chars = int(match[2])
    link = match[3]
    
    # In case the roots part contains multiple characters (like '戈矛' or '己已巳')
    for root in roots:
        rows.append({
            'Chữ': root,
            'Group': group_index,
            'Num Characters': num_chars,
            'Link': link
        })

df = pd.DataFrame(rows)
df.to_excel(output_file, index=False)

print(f"Created {output_file} with {len(rows)} rows (from {len(matches)} groups).")
