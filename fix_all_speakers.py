import re

with open("src/TracNghiemTab.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old_generate = """       validPool.sort(() => Math.random() - 0.5);
       const distractors = validPool.slice(0, 3).map(i => i[answerField]);
       
       options = [answerText, ...distractors].sort(() => Math.random() - 0.5);
       
       return { questionText, options, correctAnswer: answerText };"""

new_generate = """       validPool.sort(() => Math.random() - 0.5);
       const distractors = validPool.slice(0, 3);
       const distractorTexts = distractors.map(i => i[answerField]);
       
       options = [answerText, ...distractorTexts].sort(() => Math.random() - 0.5);
       
       let audioMap = {};
       if (mode === 'han_pinyin') {
           audioMap[answerText] = charObj['Link Âm Thanh Pinyin (Cloudinary MP3)'];
           distractors.forEach(i => {
               audioMap[i[answerField]] = i['Link Âm Thanh Pinyin (Cloudinary MP3)'];
           });
       }

       return { questionText, options, correctAnswer: answerText, audioMap };"""

if old_generate in content:
    content = content.replace(old_generate, new_generate)
else:
    print("Could not replace generate")


old_option_render = """                        return (
                          <button 
                            key={idx}
                            onClick={() => handleMcqSelect(option)}
                            disabled={isRevealed}
                            style={{
                              padding: '20px', fontSize: '1.2rem', borderRadius: '12px',
                              background: bgColor, color, border,
                              cursor: isRevealed ? 'default' : 'pointer',
                              transition: 'all 0.2s'
                            }}
                          >
                            {option}
                          </button>
                        );"""

new_option_render = """                        return (
                          <button 
                            key={idx}
                            onClick={() => handleMcqSelect(option)}
                            disabled={isRevealed}
                            style={{
                              padding: '20px', fontSize: '1.2rem', borderRadius: '12px',
                              background: bgColor, color, border,
                              cursor: isRevealed ? 'default' : 'pointer',
                              transition: 'all 0.2s',
                              display: 'flex', alignItems: 'center', justifyContent: 'center'
                            }}
                          >
                            <span>{option}</span>
                            {session.mode === 'han_pinyin' && mcq.audioMap && mcq.audioMap[option] && (
                                <span onClick={(e) => { e.stopPropagation(); playAudio(mcq.audioMap[option]); }} style={{ marginLeft: '10px', fontSize: '1.5rem', cursor: 'pointer', pointerEvents: 'auto' }}>🔊</span>
                            )}
                          </button>
                        );"""

if old_option_render in content:
    content = content.replace(old_option_render, new_option_render)
else:
    print("Could not replace option render")

with open("src/TracNghiemTab.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Injected audio map and speakers!")
