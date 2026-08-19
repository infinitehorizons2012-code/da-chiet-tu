import re

with open('src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_fetch = """      Promise.all([
        fetch('/data/research_data_1.json').then(res => res.json()),
        fetch('/data/research_data_2.json').then(res => res.json())
      ])
        .then(([part1, part2]) => {
          researchDataObj.push(...part1, ...part2);"""

new_fetch = """      Promise.all([
        fetch('/data/research_data_1.json').then(res => res.json()),
        fetch('/data/research_data_2.json').then(res => res.json()),
        fetch('/data/research_data_3.json').then(res => res.json())
      ])
        .then(([part1, part2, part3]) => {
          researchDataObj.push(...part1, ...part2, ...part3);"""

content = content.replace(old_fetch, new_fetch)

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated fetch for 3 parts")
