import re

with open('src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_select = """            <select 
              value={selectedSkill} 
              onChange={e => setSelectedSkill(e.target.value)}
              style={{padding: '8px 12px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '1rem', outline: 'none'}}
            >
              {SKILLS.map(s => <option key={s.id} value={s.id}>{s.label}</option>)}
            </select>"""

new_select = """            <select 
              value={selectedSkill} 
              onChange={e => setSelectedSkill(e.target.value)}
              style={{padding: '8px 12px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '1rem', outline: 'none'}}
            >
              <option value="chiettu">Chiết tự</option>
              <optgroup label="Pinyin">
                 <option value="han_pinyin">Hán ➔ Pinyin</option>
                 <option value="pinyin_han">Pinyin ➔ Hán</option>
              </optgroup>
              <optgroup label="Hán Việt">
                 <option value="han_hanviet">Hán ➔ Hán Việt</option>
                 <option value="hanviet_han">Hán Việt ➔ Hán</option>
              </optgroup>
              <option value="han_nghia">Hán ➔ Nghĩa</option>
              <optgroup label="Mnemonic">
                 <option value="han_mnemonic">Hán ➔ Mnemonic</option>
                 <option value="mnemonic_han">Mnemonic ➔ Hán</option>
              </optgroup>
            </select>"""

content = content.replace(old_select, new_select)

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated LuyenTap select")
