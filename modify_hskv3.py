import re

with open("src/App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update hsk3Vocab
old_vocab = r"'HSK1 - Lesson 1': \[.*?\]"
new_vocab = r"'HSK1 - Lesson 1': ['你', '您', '们', '老', '师', '王', '学', '生', '同', '大', '家', '好', '谢', '不', '客', '气', '再', '见']"
content = re.sub(old_vocab, new_vocab, content, flags=re.DOTALL)

# 2. Add 'Tổng' to UI
# We find:
# <div className="dropdown-menu" style={{position: 'absolute', top: 0, left: '100%', backgroundColor: 'white', border: '1px solid #e2e8f0', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)', zIndex: 101, minWidth: '120px', padding: '5px 0', maxHeight: '300px', overflowY: 'auto'}}>
#    {Array.from({length: 15}, (_, i) => i + 1).map(lesson => (
old_ui = r"(\{Array\.from\(\{length: 15\}, \(_, i\) => i \+ 1\)\.map\(lesson => \()"
new_ui = """<div className="dropdown-item" onClick={() => { setActiveTab(`HSK v3 - ${level} - Tổng`); setShowHskV3Menu(false); }} style={{padding: '10px 20px', cursor: 'pointer', color: '#334155'}}>
                               Tổng
                             </div>
                             \\1"""
content = re.sub(old_ui, new_ui, content)

# 3. Update filteredData
old_filter = """if (activeTab.startsWith('HSK v3')) {
            const key = activeTab.replace('HSK v3 - ', '');
            const vocabList = hsk3Vocab[key] || [];
            if (vocabList.length === 0) return [];
            const result = researchDataObj.filter(item => vocabList.includes(item['Chữ Trung Quốc']));
            result.sort((a, b) => vocabList.indexOf(a['Chữ Trung Quốc']) - vocabList.indexOf(b['Chữ Trung Quốc']));
            return result;
        }"""
new_filter = """if (activeTab.startsWith('HSK v3')) {
            const key = activeTab.replace('HSK v3 - ', '');
            if (key.endsWith(' - Tổng')) {
                const level = key.split(' - ')[0]; // e.g. "HSK1"
                const col = colMap[level];
                return researchDataObj.filter(item => {
                    const val = item[col];
                    return val !== undefined && val !== '' && val !== 'nan' && val !== null;
                }).sort((a, b) => {
                    const vA = parseFloat(a[col]);
                    const vB = parseFloat(b[col]);
                    return (isNaN(vA) ? 0 : vA) - (isNaN(vB) ? 0 : vB);
                });
            } else {
                const vocabList = hsk3Vocab[key] || [];
                if (vocabList.length === 0) return [];
                const result = researchDataObj.filter(item => vocabList.includes(item['Chữ Trung Quốc']));
                result.sort((a, b) => vocabList.indexOf(a['Chữ Trung Quốc']) - vocabList.indexOf(b['Chữ Trung Quốc']));
                return result;
            }
        }"""
content = content.replace(old_filter, new_filter)

with open("src/App.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Injected HSK v3 modifications!")
