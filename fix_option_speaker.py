import re

with open("src/TracNghiemTab.jsx", "r", encoding="utf-8") as f:
    content = f.read()

def replace_option():
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if '{option}' in line and not 'function' in line and not '=' in line:
            # check if next line is </button>
            if i + 1 < len(lines) and '</button>' in lines[i+1]:
                lines[i] = """                          <span style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}>
                            <span>{option}</span>
                            {session.mode === 'han_pinyin' && isRevealed && option === mcq.correctAnswer && currentChar['Link Âm Thanh Pinyin (Cloudinary MP3)'] && (
                                <span onClick={(e) => { e.stopPropagation(); playAudio(currentChar['Link Âm Thanh Pinyin (Cloudinary MP3)']); }} style={{ marginLeft: '10px', fontSize: '1.5rem', cursor: 'pointer', pointerEvents: 'auto' }}>🔊</span>
                            )}
                          </span>"""
                return '\n'.join(lines)
    return content

new_content = replace_option()
if new_content != content:
    with open("src/TracNghiemTab.jsx", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Injected via line insert!")
else:
    print("Failed to replace")

