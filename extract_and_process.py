import json
import re
import pandas as pd

transcript_path = r"C:\Users\DT.HANG\.gemini\antigravity\brain\546c092e-9740-4ee8-a87b-644c4acfb8f6\.system_generated\logs\transcript_full.jsonl"
output_file = r"C:\Users\DT.HANG\Downloads\DA chiet tu\hanzicraft_words.xlsx"

# Regex to match [1一886 words](Link)
pattern = re.compile(r'\[(\d+)(.+?)(\d+)\s+words\]\((.*?)\)')
all_text = ""

print("Reading conversation transcript...")
try:
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get('type') == 'USER_INPUT':
                    content = data.get('content', '')
                    if isinstance(content, str):
                        all_text += content + "\n"
            except json.JSONDecodeError:
                continue

    matches = pattern.findall(all_text)
    
    # We might have duplicates if the user pasted overlapping chunks
    # Let's use a dictionary to keep unique groups by sequence number
    unique_groups = {}
    for match in matches:
        seq_num = int(match[0])
        chars = match[1]
        num_words = int(match[2])
        link = match[3]
        unique_groups[seq_num] = (chars, num_words, link)
        
    rows = []
    # Sort by sequence number
    for seq_num in sorted(unique_groups.keys()):
        chars, num_words, link = unique_groups[seq_num]
        for char in chars:
            rows.append({
                'Từ Trung Quốc': char,
                'Số thứ tự': seq_num,
                'Số words': num_words,
                'Link': link
            })

    df = pd.DataFrame(rows)
    df.to_excel(output_file, index=False)
    print(f"Successfully created {output_file} with {len(rows)} rows (from {len(unique_groups)} unique groups).")
except Exception as e:
    print(f"Error: {e}")
