import pandas as pd
import json
import math
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Reading Excel...")
df = pd.read_excel("hanzicraft_dashboard_reordered.xlsx")
print(f"Total rows: {len(df)}")

def clean_data(val):
    if pd.isna(val):
        return ""
    if isinstance(val, (int, float)):
        if math.isnan(val):
            return ""
        return str(val)
    return str(val).strip()

print("Cleaning data...")
data = df.to_dict(orient='records')
cleaned_data = []
for row in data:
    cleaned_row = {k: clean_data(v) for k, v in row.items()}
    cleaned_data.append(cleaned_row)

print("Splitting into two files...")
half = len(cleaned_data) // 2
part1 = cleaned_data[:half]
part2 = cleaned_data[half:]

with open('public/data/research_data_1.json', 'w', encoding='utf-8') as f:
    json.dump(part1, f, ensure_ascii=False)

with open('public/data/research_data_2.json', 'w', encoding='utf-8') as f:
    json.dump(part2, f, ensure_ascii=False)

print("Done! Generated public/data/research_data_1.json and public/data/research_data_2.json")
