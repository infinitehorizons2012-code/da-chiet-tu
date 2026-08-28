import json

with open("public/data/research_data_1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data:
    char = item.get("Chữ Trung Quốc", "")
    if char in ["你", "您", "你们", "老师", "王老师", "学生", "同学", "大家", "好", "谢谢", "不客气", "再见"]:
        print(char.encode('utf-8'))
