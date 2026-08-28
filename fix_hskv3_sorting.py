import re

with open("src/App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

filter_regex = re.compile(r"if \(activeTab\.startsWith\('HSK v3'\)\) \{\s*const key = activeTab\.replace\('HSK v3 - ', ''\);\s*const vocabList = hsk3Vocab\[key\] \|\| \[\];\s*return researchDataObj\.filter\(item => vocabList\.includes\(item\['Chữ Trung Quốc'\]\)\);\s*\}", re.DOTALL)

new_filter = """if (activeTab.startsWith('HSK v3')) {
            const key = activeTab.replace('HSK v3 - ', '');
            const vocabList = hsk3Vocab[key] || [];
            if (vocabList.length === 0) return [];
            const result = researchDataObj.filter(item => vocabList.includes(item['Chữ Trung Quốc']));
            result.sort((a, b) => vocabList.indexOf(a['Chữ Trung Quốc']) - vocabList.indexOf(b['Chữ Trung Quốc']));
            return result;
        }"""

if filter_regex.search(content):
    content = filter_regex.sub(new_filter, content)
    with open("src/App.jsx", "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed HSK v3 sorting logic using regex!")
else:
    print("Could not find the block to replace using regex.")
