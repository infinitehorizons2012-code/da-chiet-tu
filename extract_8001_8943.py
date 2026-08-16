import json
import re

transcript_path = r"C:\Users\DT.HANG\.gemini\antigravity\brain\546c092e-9740-4ee8-a87b-644c4acfb8f6\.system_generated\logs\transcript_full.jsonl"
raw_path = r"C:\Users\DT.HANG\Downloads\DA chiet tu\raw_input.txt"

def extract():
    with open(transcript_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    latest_user_input = ""
    for line in reversed(lines):
        try:
            data = json.loads(line)
            if data.get('type') == 'USER_INPUT' and '8001' in data.get('content', ''):
                latest_user_input = data['content']
                break
        except Exception:
            pass
            
    if latest_user_input:
        matches = re.findall(r'\[.*?\]\(.*?\)\d+', latest_user_input)
        with open(raw_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(matches))
        print(f"Extracted {len(matches)} characters.")
    else:
        print("Could not find the user input in transcript.")

if __name__ == "__main__":
    extract()
