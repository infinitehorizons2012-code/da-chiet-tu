import re

with open('src/TracNghiemTab.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_srs = """            const newSrs = { ...charObj.srs, [session.mode]: { status: newStatus, level: newLevel } };"""

new_srs = """            let baseSrs = { ...charObj.srs };
            if (baseSrs.status && typeof baseSrs.status === 'string') {
               const oldStatus = baseSrs.status;
               const oldLevel = baseSrs.level || baseSrs.streak || 0;
               baseSrs = {};
               const SKILLS = ['chiettu', 'han_pinyin', 'pinyin_han', 'han_hanviet', 'hanviet_han', 'han_nghia', 'han_mnemonic', 'mnemonic_han'];
               SKILLS.forEach(s => {
                  baseSrs[s] = { status: s === 'chiettu' ? oldStatus : 'bat_dau', level: s === 'chiettu' ? oldLevel : 0 };
               });
            }
            const newSrs = { ...baseSrs, [session.mode]: { status: newStatus, level: newLevel } };"""

content = content.replace(old_srs, new_srs)

with open('src/TracNghiemTab.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed finishSession migration bug")
