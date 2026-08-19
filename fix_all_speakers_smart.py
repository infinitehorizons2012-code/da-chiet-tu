import re

with open("src/TracNghiemTab.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. replace generateMultipleChoice return block
def replace_gen():
    global content
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'const distractors = validPool.slice(0, 3).map(i => i[answerField]);' in line:
            new_lines = [
                "       const distractors = validPool.slice(0, 3);",
                "       const distractorTexts = distractors.map(i => i[answerField]);",
                "       ",
                "       options = [answerText, ...distractorTexts].sort(() => Math.random() - 0.5);",
                "       ",
                "       let audioMap = {};",
                "       if (mode === 'han_pinyin') {",
                "           audioMap[answerText] = charObj['Link Âm Thanh Pinyin (Cloudinary MP3)'];",
                "           distractors.forEach(i => {",
                "               audioMap[i[answerField]] = i['Link Âm Thanh Pinyin (Cloudinary MP3)'];",
                "           });",
                "       }",
                "       return { questionText, options, correctAnswer: answerText, audioMap };"
            ]
            
            # replace from i to i+4
            content = '\n'.join(lines[:i] + new_lines + lines[i+5:])
            return True
    return False

# 2. replace option button
def replace_opt():
    global content
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if '<button' in line and lines[i+1].strip() == 'key={idx}' and 'onClick={() => handleMcqSelect(option)}' in lines[i+2]:
            # we found the button!
            # replace the style
            for j in range(i, i+15):
                if 'transition: \'all 0.2s\'' in lines[j] and 'display:' not in lines[j]:
                    lines[j] = lines[j].replace("transition: 'all 0.2s'", "transition: 'all 0.2s', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px'")
                
                # replace {option} with the spans
                if lines[j].strip() == '{option}':
                    lines[j] = """                          <span>{option}</span>
                            {session.mode === 'han_pinyin' && mcq.audioMap && mcq.audioMap[option] && (
                                <span onClick={(e) => { e.stopPropagation(); playAudio(mcq.audioMap[option]); }} style={{ fontSize: '1.5rem', cursor: 'pointer', pointerEvents: 'auto' }}>🔊</span>
                            )}"""
            content = '\n'.join(lines)
            return True
    return False

r1 = replace_gen()
r2 = replace_opt()
print(f"Gen: {r1}, Opt: {r2}")

if r1 or r2:
    with open("src/TracNghiemTab.jsx", "w", encoding="utf-8") as f:
        f.write(content)
