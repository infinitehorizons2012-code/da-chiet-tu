import re

with open("src/App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add state for Chữ Nho dropdown
hsk_menu_regex = re.compile(r"const \[showHskMenu, setShowHskMenu\] = useState\(false\);")
new_states = """const [showHskMenu, setShowHskMenu] = useState(false);
    const [showNhoMenu, setShowNhoMenu] = useState(false);
    
    // Generate Nho groups: Nhom 1 (1-5), Nhom 2 (6-10), ..., up to ~1200
    const nhoGroups = ['Tổng'];
    for(let i = 1; i <= 240; i++) {
       nhoGroups.push(`Nhóm ${i}`);
    }"""
content = hsk_menu_regex.sub(new_states, content)

# 2. Modify filteredData to handle "Chữ Nho" and "Chữ Nho - Nhóm X"
filter_regex = re.compile(r"const col = colMap\[activeTab\];\s*return researchDataObj\.filter.*?\}\)\.sort", re.DOTALL)
new_filter = """let baseTab = activeTab;
      if (activeTab.startsWith('Chữ Nho')) {
          baseTab = 'Chữ Nho';
      }
      const col = colMap[baseTab];
      return researchDataObj.filter(item => {
        const val = item[col];
        if (val === undefined || val === '' || val === 'nan' || val === null) return false;
        
        if (activeTab.startsWith('Chữ Nho - Nhóm')) {
            const groupNum = parseInt(activeTab.replace('Chữ Nho - Nhóm ', ''));
            const stt = parseFloat(val);
            const min = (groupNum - 1) * 5 + 1;
            const max = groupNum * 5;
            if (stt < min || stt > max) return false;
        }
        return true;
      }).sort"""
content = filter_regex.sub(new_filter, content)

# 3. Modify colMap sort to handle baseTab
sort_regex = re.compile(r"if \(activeTab === 'Chỉ Âm'\) \{\s*const strA = a\[col\] \|\| '';")
new_sort = """if (baseTab === 'Chỉ Âm') {
          const strA = a[col] || '';"""
content = sort_regex.sub(new_sort, content)


# 4. Modify UI to add dropdown for Chữ Nho
nho_tab_regex = re.compile(r"<button className=\{`tab-btn \$\{activeTab === 'Chữ Nho' \? 'active' : ''\}`\} onClick=\{\(\) => setActiveTab\('Chữ Nho'\)\}>Chữ Nho</button>")
new_nho_tab = """<div className="tab-dropdown" onMouseEnter={() => setShowNhoMenu(true)} onMouseLeave={() => setShowNhoMenu(false)} style={{position: 'relative'}}>
             <button className={`tab-btn ${activeTab.startsWith('Chữ Nho') ? 'active' : ''}`} onClick={() => setActiveTab('Chữ Nho - Tổng')}>
               {activeTab.startsWith('Chữ Nho') ? (activeTab === 'Chữ Nho - Tổng' ? 'Chữ Nho' : activeTab.replace('Chữ Nho - ', '')) : 'Chữ Nho'} ▼
             </button>
             {showNhoMenu && (
               <div className="dropdown-menu" style={{position: 'absolute', top: '100%', left: 0, backgroundColor: 'white', border: '1px solid #e2e8f0', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)', zIndex: 100, minWidth: '120px', padding: '5px 0', maxHeight: '300px', overflowY: 'auto'}}>
                 {nhoGroups.map(grp => (
                   <div key={grp} className="dropdown-item" onClick={() => { setActiveTab(`Chữ Nho - ${grp}`); setShowNhoMenu(false); }} style={{padding: '10px 20px', cursor: 'pointer', color: '#334155'}}>
                     {grp}
                   </div>
                 ))}
               </div>
             )}
           </div>"""
content = nho_tab_regex.sub(new_nho_tab, content)

# 5. Modify tonghop-index to show ChuNho STT
index_regex = re.compile(r'<div className="tonghop-index">\{idx \+ 1\}</div>')
new_index = """<div className="tonghop-index">
                  {activeTab.startsWith('Chữ Nho') ? (item['ChuNhoTongHop_STT (Giáo trình Chữ Nho)'] !== undefined ? item['ChuNhoTongHop_STT (Giáo trình Chữ Nho)'] : idx + 1) : idx + 1}
               </div>"""
content = index_regex.sub(new_index, content)

with open("src/App.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Injected Chữ Nho dropdown logic!")
