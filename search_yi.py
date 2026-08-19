import json
with open("public/data/research_data_1.json", "r", encoding="utf-8") as f:
    data1 = json.load(f)
with open("public/data/research_data_2.json", "r", encoding="utf-8") as f:
    data2 = json.load(f)
with open("public/data/research_data_3.json", "r", encoding="utf-8") as f:
    data3 = json.load(f)

data = data1 + data2 + data3

with open("yi_chars.txt", "w", encoding="utf-8") as out:
    for item in data:
        pinyin = item.get("Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)", "")
        if pinyin == "yī":
            out.write(f"{item.get('Chữ Trung Quốc')} | {item.get('Link Âm Thanh Pinyin (Cloudinary MP3)')}\n")
