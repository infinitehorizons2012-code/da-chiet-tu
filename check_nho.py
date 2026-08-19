import json
with open("public/data/research_data_1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("out_nho.txt", "w", encoding="utf-8") as out:
    for item in data:
        val = item.get("ChuNhoTongHop_STT (Giáo trình Chữ Nho)", "")
        if val and val != "nan":
            out.write(f"Char: {item.get('Chữ Trung Quốc')} - Val: {val}\n")
