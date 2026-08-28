import json

with open("public/data/research_data_1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

vocab = ["你", "您", "们", "老", "师", "王", "学", "生", "同", "大", "家", "好", "谢", "不", "客", "气", "再", "见"]
existing = [item.get("Chữ Trung Quốc", "") for item in data]

missing = [char for char in vocab if char not in existing]
if missing:
    print("Missing:", [m.encode('utf-8') for m in missing])
else:
    print("All exist!")
