import re

with open("src/TracNghiemTab.jsx", "r", encoding="utf-8") as f:
    content = f.read()

def replace_mcq():
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'const handleMcqSelect = (option) => {' in line:
            # Insert playAudio after setIsRevealed(true);
            for j in range(i, i+10):
                if 'setIsRevealed(true);' in lines[j]:
                    lines.insert(j + 1, "       if (session.mode === 'han_pinyin') { playAudio(currentChar['Link Âm Thanh Pinyin (Cloudinary MP3)']); }")
                    return '\n'.join(lines)
    return content

new_content = replace_mcq()
if len(new_content) > len(content):
    with open("src/TracNghiemTab.jsx", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Injected via line insert!")
else:
    print("Failed to insert")

