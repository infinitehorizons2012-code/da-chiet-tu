import re

with open('src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the specific block
old_block = """        <div className="logo-text">
          <span className="title">Bản đồ Chiết tự</span>
          <span className="subtitle">HỆ THỐNG PHÂN TÍCH CHỮ HÁN</span>
        </div>"""

new_block = """        <div className="logo-text">
          <span className="title">HỆ THỐNG PHÂN TÍCH CHỮ HÁN</span>
        </div>"""

content = content.replace(old_block, new_block)

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Replaced text")
