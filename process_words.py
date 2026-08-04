import re
import pandas as pd

input_file = "raw_words.txt"
output_file = "hanzicraft_words.xlsx"

# Regex to match [1一886 words](Link)
pattern = re.compile(r'\[(\d+)(.+?)(\d+)\s+words\]\((.*?)\)')

rows = []

try:
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    matches = pattern.findall(text)

    for match in matches:
        seq_num = int(match[0])
        chars = match[1]
        num_words = int(match[2])
        link = match[3]
        
        for char in chars:
            rows.append({
                'Từ Trung Quốc': char,
                'Số thứ tự': seq_num,
                'Số words': num_words,
                'Link': link
            })

    df = pd.DataFrame(rows)
    df.to_excel(output_file, index=False)
    print(f"Created {output_file} with {len(rows)} rows (from {len(matches)} items).")
except FileNotFoundError:
    print(f"File {input_file} not found. Please create it and paste the data.")
