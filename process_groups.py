import pandas as pd
import re
import os

raw_path = r"C:\Users\DT.HANG\Downloads\DA chiet tu\raw_groups.txt"
excel_path = r"C:\Users\DT.HANG\Downloads\DA chiet tu\hanzicraft_groups.xlsx"

def process():
    with open(raw_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Pattern: [Root][Pinyin][Characters](Link)
    # Root is typically 1 char. Pinyin is letters + optional digit.
    pattern = r'\[(.)([a-zA-ZüÜ]+[0-5]?)(.*?)\]\((.*?)\)'
    
    rows = []
    for match in re.finditer(pattern, text):
        root = match.group(1)
        pinyin = match.group(2)
        chars = match.group(3)
        link = match.group(4)
        
        group_name = f"{root}{pinyin}"
        
        for c in chars:
            rows.append({
                "Chữ": c,
                "Group": group_name,
                "Link": link
            })
            
    if not rows:
        print("No groups found.")
        return

    new_df = pd.DataFrame(rows)
    
    if os.path.exists(excel_path):
        existing_df = pd.read_excel(excel_path)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = new_df
        
    # Reorder columns just in case
    combined_df = combined_df[['Chữ', 'Group', 'Link']]
        
    combined_df.to_excel(excel_path, index=False)
    print(f"Added {len(rows)} characters to {excel_path}. Total rows: {len(combined_df)}")

if __name__ == "__main__":
    process()
