import re

with open('src/TracNghiemTab.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("Link Am Thanh Pinyin (Cloudinary MP3)", "Link Âm Thanh Pinyin (Cloudinary MP3)")

with open('src/TracNghiemTab.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed audio key")
