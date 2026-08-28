import json

with open("public/data/research_data_1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

existing_chars = set()
for item in data:
    if "Chữ Trung Quốc" in item:
        existing_chars.add(item["Chữ Trung Quốc"].strip())

vocab = ["你", "您", "你们", "老师", "王老师", "学生", "同学", "大家", "好", "谢谢", "不客气", "再见"]

added = 0
for v in vocab:
    if v not in existing_chars:
        # Create an empty record for it
        new_item = {
            "Chữ Trung Quốc": v,
            "Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)": "",
            "Âm Hán Việt (Master 100%)": "",
            "Nghĩa Tiếng Việt (Master 100%)": "",
            # Add other keys to prevent undefined errors
        }
        # Populate all keys from data[0] with empty strings
        for k in data[0].keys():
            if k not in new_item:
                new_item[k] = ""
                
        data.append(new_item)
        added += 1

if added > 0:
    with open("public/data/research_data_1.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Added {added} missing vocabulary words to research_data_1.json")
else:
    print("All vocabulary words already exist.")
