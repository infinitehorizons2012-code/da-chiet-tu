import re

with open('src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_getSrsStreak = """const getSrsStreak = (item, skill) => {"""

new_getSrsStreak = """const getSrsLevel = (item, skill) => {
  if (!item.srs) return 0;
  if (item.srs.status && typeof item.srs.status === 'string') {
     if (skill === 'chiettu') return item.srs.level || 0;
     return 0;
  }
  if (item.srs[skill]) return item.srs[skill].level || 0;
  return 0;
};

const getSrsStreak = (item, skill) => {"""

content = content.replace(old_getSrsStreak, new_getSrsStreak)

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Restored getSrsLevel")
