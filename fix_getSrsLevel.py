import re

with open('src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_getSrsLevel = """const getSrsLevel = (item, skill) => {
  if (!item.srs) return 0;
  if (item.srs.status && typeof item.srs.status === 'string') {
     if (skill === 'chiettu') return item.srs.level || 0;
     return 0;
  }
  if (item.srs[skill]) return item.srs[skill].level || 0;
  return 0;
};"""

new_getSrsLevel = """const getSrsLevel = (item, skill) => {
  if (!item.srs) return 0;
  if (item.srs.status && typeof item.srs.status === 'string') {
     if (skill === 'chiettu') return item.srs.level || item.srs.streak || 0;
     return 0;
  }
  if (item.srs[skill]) return item.srs[skill].level || item.srs[skill].streak || 0;
  return 0;
};"""

content = content.replace(old_getSrsLevel, new_getSrsLevel)

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated getSrsLevel")
