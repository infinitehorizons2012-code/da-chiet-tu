import json
with open("public/data/research_data_1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data:
    char = item.get("Chữ Trung Quốc", "").strip()
    if char == "老师" or char == "谢谢" or "谢谢" in char:
        print("Found:", char.encode('utf-8'))
