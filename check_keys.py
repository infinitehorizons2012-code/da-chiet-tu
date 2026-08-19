import json
with open("public/data/research_data_1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for key in data[0].keys():
    if "Nho" in key or "Nhóm" in key or "Group" in key:
        print(key.encode('utf-8'))
