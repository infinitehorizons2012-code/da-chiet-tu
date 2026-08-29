import urllib.request
import json

url = "https://da-chiet-tu.pages.dev/api/updates?username=admin"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        updates = data.get("updates", {})
        
        # Load master
        with open("public/data/research_data_1.json", "r", encoding="utf-8") as f:
            master_data = json.load(f)
            
        char_map = {item["Chữ Trung Quốc"]: item for item in master_data if "Chữ Trung Quốc" in item}
        updated_count = 0
        for char, data_obj in updates.items():
            if char in char_map:
                item = char_map[char]
                for key, value in data_obj.items():
                    if key not in ["srs", "quiz_mapping"]:
                        item[key] = value
                updated_count += 1
                
        print(f"Updated {updated_count} characters in master JSON.")
        
        with open("public/data/research_data_1.json", "w", encoding="utf-8") as f:
            json.dump(master_data, f, ensure_ascii=False, indent=2)
            
except Exception as e:
    print(f"Error: {e}")
