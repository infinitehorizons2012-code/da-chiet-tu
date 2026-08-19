import re

with open("src/App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Replace detail-pinyin using regex to ignore exact spaces
detail_pinyin_regex = re.compile(r'<div className="detail-pinyin">\{selectedChar\[\'Pinyin_Master \(Pinyin Chuẩn Tổng Hợp 100\%\)\'\]\}\s*-\s*\{selectedChar\[\'Âm Hán Việt \(Master 100\%\)\'\]\}</div>')

detail_pinyin_new = """<div className="detail-pinyin" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
                    {selectedChar['Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)']}
                    {selectedChar['Link Âm Thanh Pinyin (Cloudinary MP3)'] && (
                        <span onClick={() => playAudio(selectedChar['Link Âm Thanh Pinyin (Cloudinary MP3)'])} style={{ fontSize: '1.2rem', cursor: 'pointer', pointerEvents: 'auto' }}>🔊</span>
                    )}
                    - {selectedChar['Âm Hán Việt (Master 100%)']}
                  </div>"""

if detail_pinyin_regex.search(content):
    content = detail_pinyin_regex.sub(detail_pinyin_new, content)
    with open("src/App.jsx", "w", encoding="utf-8") as f:
        f.write(content)
    print("Replaced detail-pinyin!")
else:
    print("Could not find detail-pinyin")
