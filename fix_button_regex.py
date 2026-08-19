import re

with open("src/TracNghiemTab.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Let's replace the whole button block!
old_button_regex = re.compile(r"<button\s+key=\{idx\}.*?</button>", re.DOTALL)

new_button = """<button 
                            key={idx}
                            onClick={() => handleMcqSelect(option)}
                            disabled={isRevealed}
                            style={{
                              padding: '20px', fontSize: '1.2rem', borderRadius: '12px',
                              background: bgColor, color: color, border: border,
                              cursor: isRevealed ? 'default' : 'pointer',
                              transition: 'all 0.2s',
                              display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px'
                            }}
                          >
                            <span>{option}</span>
                            {session.mode === 'han_pinyin' && mcq.audioMap && mcq.audioMap[option] && (
                                <span onClick={(e) => { e.stopPropagation(); playAudio(mcq.audioMap[option]); }} style={{ fontSize: '1.5rem', cursor: 'pointer', pointerEvents: 'auto' }}>🔊</span>
                            )}
                          </button>"""

content = old_button_regex.sub(new_button, content)

with open("src/TracNghiemTab.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Replaced button entirely!")
