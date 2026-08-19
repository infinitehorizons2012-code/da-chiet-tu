import re

with open('src/TracNghiemTab.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the TABS rendering logic
old_tabs_render = """          <div className="tab-navigation" style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', marginBottom: '20px', justifyContent: 'center' }}>
            {TABS.map(tab => (
              <button 
                key={tab.id}
                className={`tab-btn ${quizMode === tab.id ? 'active' : ''}`} 
                onClick={() => setQuizMode(tab.id)}
                style={{ fontSize: '0.9rem', padding: '8px 12px' }}
              >
                {tab.label}
              </button>
            ))}
          </div>"""

new_tabs_render = """          <div className="tab-navigation" style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', marginBottom: '20px', justifyContent: 'center' }}>
              <button 
                className={`tab-btn ${quizMode === 'chiettu' ? 'active' : ''}`} 
                onClick={() => setQuizMode('chiettu')}
                style={{ fontSize: '0.9rem', padding: '8px 12px' }}
              >
                Chiết tự
              </button>

              <select 
                className={`tab-btn ${['han_pinyin','pinyin_han'].includes(quizMode) ? 'active' : ''}`}
                value={['han_pinyin','pinyin_han'].includes(quizMode) ? quizMode : 'placeholder'}
                onChange={(e) => setQuizMode(e.target.value)}
                style={{ fontSize: '0.9rem', padding: '8px 12px', appearance: 'auto' }}
              >
                <option value="placeholder" disabled hidden>Hán ↔ Pinyin ▾</option>
                <option value="han_pinyin">Hán ➔ Pinyin</option>
                <option value="pinyin_han">Pinyin ➔ Hán</option>
              </select>

              <select 
                className={`tab-btn ${['han_hanviet','hanviet_han'].includes(quizMode) ? 'active' : ''}`}
                value={['han_hanviet','hanviet_han'].includes(quizMode) ? quizMode : 'placeholder'}
                onChange={(e) => setQuizMode(e.target.value)}
                style={{ fontSize: '0.9rem', padding: '8px 12px', appearance: 'auto' }}
              >
                <option value="placeholder" disabled hidden>Hán ↔ Hán Việt ▾</option>
                <option value="han_hanviet">Hán ➔ Hán Việt</option>
                <option value="hanviet_han">Hán Việt ➔ Hán</option>
              </select>

              <button 
                className={`tab-btn ${quizMode === 'han_nghia' ? 'active' : ''}`} 
                onClick={() => setQuizMode('han_nghia')}
                style={{ fontSize: '0.9rem', padding: '8px 12px' }}
              >
                Hán ➔ Nghĩa
              </button>

              <select 
                className={`tab-btn ${['han_mnemonic','mnemonic_han'].includes(quizMode) ? 'active' : ''}`}
                value={['han_mnemonic','mnemonic_han'].includes(quizMode) ? quizMode : 'placeholder'}
                onChange={(e) => setQuizMode(e.target.value)}
                style={{ fontSize: '0.9rem', padding: '8px 12px', appearance: 'auto' }}
              >
                <option value="placeholder" disabled hidden>Hán ↔ Mnemonic ▾</option>
                <option value="han_mnemonic">Hán ➔ Mnemonic</option>
                <option value="mnemonic_han">Mnemonic ➔ Hán</option>
              </select>
          </div>"""

content = content.replace(old_tabs_render, new_tabs_render)

with open('src/TracNghiemTab.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated TracNghiemTab tabs")
