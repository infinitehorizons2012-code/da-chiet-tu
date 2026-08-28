import re

with open("src/App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add states for HSK v3
state_regex = re.compile(r"const \[showHskMenu, setShowHskMenu\] = useState\(false\);")
new_states = """const [showHskMenu, setShowHskMenu] = useState(false);
    const [showHskV3Menu, setShowHskV3Menu] = useState(false);
    const [activeHskV3Sub, setActiveHskV3Sub] = useState(null);
    
    const hskV3Data = useMemo(() => {
        const data = {};
        for(let i=1; i<=9; i++) {
            data[`HSK${i}`] = {};
            // For now just 15 lessons per level as placeholder, except HSK1 Lesson 1
            const numLessons = 15; 
            for(let j=1; j<=numLessons; j++) {
                data[`HSK${i}`][`Lesson ${j}`] = [];
            }
        }
        data['HSK1']['Lesson 1'] = ['你', '您', '你们', '老师', '王老师', '学生', '同学', '大家', '好', '谢谢', '不客气', '再见'];
        return data;
    }, []);
"""
content = state_regex.sub(new_states, content)

# 2. Modify filteredData to handle HSKv3
filter_regex = re.compile(r"if \(activeTab\.startsWith\('Chữ Nho'\)\) \{\s*baseTab = 'Chữ Nho';\s*\}")
new_filter = """if (activeTab.startsWith('Chữ Nho')) {
          baseTab = 'Chữ Nho';
      }
      
      if (activeTab.startsWith('HSKv3')) {
          const parts = activeTab.split('-');
          const hskLevel = parts[1];
          const lesson = parts[2];
          const words = hskV3Data[hskLevel] && hskV3Data[hskLevel][lesson] ? hskV3Data[hskLevel][lesson] : [];
          
          if (words.length === 0) return [];
          
          // Filter and sort exactly based on the array order
          const result = researchDataObj.filter(item => words.includes(item['Chữ Trung Quốc']));
          result.sort((a, b) => words.indexOf(a['Chữ Trung Quốc']) - words.indexOf(b['Chữ Trung Quốc']));
          return result;
      }"""
content = filter_regex.sub(new_filter, content)

# 3. Add HSK v3 dropdown to UI
hsk_btn_regex = re.compile(r"(<div className=\"tab-dropdown\".*?>\s*<button className=\{`tab-btn \$\{activeTab\.startsWith\('HSK'\) \? 'active' : ''\}`\}>.*?</button>\s*\{showHskMenu && \(\s*<div.*?</div>\s*\)\}\s*</div>)")

new_hsk_btn = r"""\1
           <div className="tab-dropdown" onMouseEnter={() => setShowHskV3Menu(true)} onMouseLeave={() => setShowHskV3Menu(false)} style={{position: 'relative'}}>
             <button className={`tab-btn ${activeTab.startsWith('HSKv3') ? 'active' : ''}`}>
               {activeTab.startsWith('HSKv3') ? activeTab.replace('HSKv3-', '') : 'HSK v3'} ▼
             </button>
             {showHskV3Menu && (
               <div className="dropdown-menu" style={{position: 'absolute', top: '100%', left: 0, backgroundColor: 'white', border: '1px solid #e2e8f0', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)', zIndex: 100, minWidth: '150px', padding: '5px 0'}}>
                 {Object.keys(hskV3Data).map(hsk => (
                   <div 
                     key={hsk} 
                     className="dropdown-item" 
                     onMouseEnter={() => setActiveHskV3Sub(hsk)}
                     style={{padding: '10px 20px', cursor: 'pointer', color: '#334155', display: 'flex', justifyContent: 'space-between', position: 'relative'}}
                   >
                     <span>{hsk}</span>
                     <span>▶</span>
                     {activeHskV3Sub === hsk && (
                        <div className="sub-dropdown-menu" style={{position: 'absolute', top: 0, left: '100%', backgroundColor: 'white', border: '1px solid #e2e8f0', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)', zIndex: 101, minWidth: '120px', padding: '5px 0', maxHeight: '300px', overflowY: 'auto'}}>
                          {Object.keys(hskV3Data[hsk]).map(lesson => (
                            <div 
                              key={lesson} 
                              className="dropdown-item" 
                              onClick={() => { setActiveTab(`HSKv3-${hsk}-${lesson}`); setShowHskV3Menu(false); setActiveHskV3Sub(null); }} 
                              style={{padding: '10px 20px', cursor: 'pointer', color: '#334155'}}
                            >
                              {lesson}
                            </div>
                          ))}
                        </div>
                     )}
                   </div>
                 ))}
               </div>
             )}
           </div>"""
content = hsk_btn_regex.sub(new_hsk_btn, content)

with open("src/App.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Injected HSK v3 dropdown logic!")
