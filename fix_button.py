import re

with open("src/TracNghiemTab.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old_h3 = """<h3 style={{ fontSize: '1.3rem', color: '#334155', marginBottom: '30px', whiteSpace: 'pre-wrap' }}>{mcq.questionText}</h3>"""

new_h3 = """<h3 style={{ fontSize: '1.3rem', color: '#334155', marginBottom: '30px', whiteSpace: 'pre-wrap' }}>
  {mcq.questionText}
  {(session.mode === 'pinyin_han' || session.mode === 'han_pinyin') && currentChar['Link Âm Thanh Pinyin (Cloudinary MP3)'] && (
      <button onClick={() => playAudio(currentChar['Link Âm Thanh Pinyin (Cloudinary MP3)'])} style={{ marginLeft: '15px', fontSize: '1.5rem', background: 'none', border: 'none', cursor: 'pointer', verticalAlign: 'middle' }}>🔊</button>
  )}
</h3>"""

if old_h3 in content:
    content = content.replace(old_h3, new_h3)
    with open("src/TracNghiemTab.jsx", "w", encoding="utf-8") as f:
        f.write(content)
    print("Injected button!")
else:
    print("Failed to find h3!")
