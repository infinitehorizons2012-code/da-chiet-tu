import re

with open('src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_click = """      let newSrs = { ...charObj.srs };
      SKILLS.forEach(skill => {
         newSrs = buildNewSrs({srs: newSrs}, skill.id, 'san_sang_thi', 0);
      });"""

new_click = """      let newSrs = { ...charObj.srs };
      SKILLS.forEach(skill => {
         // Ch? ??y nh?ng k? n?ng ?ang ? m?c bat_dau l?n san_sang_thi. Kh?ng reset c?c k? n?ng ?? c? ti?n ??.
         const currentStatus = getSrsStatus(charObj, skill.id);
         if (currentStatus === 'bat_dau' || !currentStatus) {
            newSrs = buildNewSrs({srs: newSrs}, skill.id, 'san_sang_thi', 0);
         }
      });"""

content = content.replace(old_click, new_click)

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed reset bug in LuyenTapTab")
