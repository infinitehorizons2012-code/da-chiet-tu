import json
import re
import urllib.parse

transcript_path = r"C:\Users\DT.HANG\.gemini\antigravity\brain\546c092e-9740-4ee8-a87b-644c4acfb8f6\.system_generated\logs\transcript_full.jsonl"
raw_path = r"C:\Users\DT.HANG\Downloads\DA chiet tu\raw_input.txt"

def extract():
    with open(transcript_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    latest_user_input = ""
    for line in reversed(lines):
        try:
            data = json.loads(line)
            if data.get('type') == 'USER_INPUT' and '5001' in data.get('content', ''):
                latest_user_input = data['content']
                break
        except Exception:
            pass
            
    if latest_user_input:
        matches = re.findall(r'\[.*?\]\(.*?\)\d+', latest_user_input)
        
        char_5000 = "夤"
        url_5000 = f"https://hanzicraft.com/dashboard/character/{urllib.parse.quote(char_5000)}"
        missing = f"[{char_5000}]({url_5000})5000"
        
        all_lines = [missing] + matches
        with open(raw_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_lines))
        print(f"Extracted {len(all_lines)} characters (including the missing 5000).")
    else:
        print("Could not find the user input in transcript.")

if __name__ == "__main__":
    extract()
