import json

with open("public/data/research_data_1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data:
    if item.get("Chữ Trung Quốc") == "一":
        print(item.get("Link Âm Thanh Pinyin (Cloudinary MP3)"))
        break
