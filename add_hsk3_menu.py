import re

with open("src/App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. State variables
state_old = "const [showNhoMenu, setShowNhoMenu] = useState(false);"
state_new = """const [showNhoMenu, setShowNhoMenu] = useState(false);
    const [showHskV3Menu, setShowHskV3Menu] = useState(false);
    const [hskV3HoverLevel, setHskV3HoverLevel] = useState(null);
    const hskV3Levels = ['HSK1', 'HSK2', 'HSK3', 'HSK4', 'HSK5', 'HSK6', 'HSK7', 'HSK8', 'HSK9'];
    const hsk3Vocab = {
        'HSK1 - Lesson 1': ['你', '您', '你们', '老师', '王老师', '学生', '同学', '大家', '好', '谢谢', '不客气', '再见']
    };"""
content = content.replace(state_old, state_new)

# 2. filteredData logic
filter_old = """let baseTab = activeTab;
      if (activeTab.startsWith('Chữ Nho')) {"""
filter_new = """if (activeTab.startsWith('HSK v3')) {
          const key = activeTab.replace('HSK v3 - ', '');
          const vocabList = hsk3Vocab[key] || [];
          return researchDataObj.filter(item => vocabList.includes(item['Chữ Trung Quốc']));
      }
      
      let baseTab = activeTab;
      if (activeTab.startsWith('Chữ Nho')) {"""
content = content.replace(filter_old, filter_new)

# 3. Fix existing HSK logic
old_hsk_btn = """<button className={`tab-btn ${activeTab.startsWith('HSK') ? 'active' : ''}`}>
               {activeTab.startsWith('HSK') ? activeTab : 'HSK'} ▼
             </button>"""
new_hsk_btn = """<button className={`tab-btn ${activeTab.startsWith('HSK') && !activeTab.startsWith('HSK v3') ? 'active' : ''}`}>
               {activeTab.startsWith('HSK') && !activeTab.startsWith('HSK v3') ? activeTab : 'HSK'} ▼
             </button>"""
content = content.replace(old_hsk_btn, new_hsk_btn)

# 4. Add new HSK v3 dropdown
new_hsk_v3 = """
           <div className="tab-dropdown" onMouseEnter={() => setShowHskV3Menu(true)} onMouseLeave={() => setShowHskV3Menu(false)} style={{position: 'relative'}}>
             <button className={`tab-btn ${activeTab.startsWith('HSK v3') ? 'active' : ''}`}>
               {activeTab.startsWith('HSK v3') ? (activeTab === 'HSK v3' ? 'HSK v3' : activeTab.replace('HSK v3 - ', '')) : 'HSK v3'} ▼
             </button>
             {showHskV3Menu && (
               <div className="dropdown-menu" style={{position: 'absolute', top: '100%', left: 0, backgroundColor: 'white', border: '1px solid #e2e8f0', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)', zIndex: 100, minWidth: '120px', padding: '5px 0'}}>
                 {hskV3Levels.map(level => (
                   <div key={level} className="dropdown-item" onMouseEnter={() => setHskV3HoverLevel(level)} onMouseLeave={() => setHskV3HoverLevel(null)} style={{padding: '10px 20px', cursor: 'pointer', color: '#334155', position: 'relative'}}>
                     {level} ►
                     {hskV3HoverLevel === level && (
                       <div className="dropdown-menu" style={{position: 'absolute', top: 0, left: '100%', backgroundColor: 'white', border: '1px solid #e2e8f0', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)', zIndex: 101, minWidth: '120px', padding: '5px 0', maxHeight: '300px', overflowY: 'auto'}}>
                         {Array.from({length: 15}, (_, i) => i + 1).map(lesson => (
                           <div key={lesson} className="dropdown-item" onClick={() => { setActiveTab(`HSK v3 - ${level} - Lesson ${lesson}`); setShowHskV3Menu(false); }} style={{padding: '10px 20px', cursor: 'pointer', color: '#334155'}}>
                             Lesson {lesson}
                           </div>
                         ))}
                       </div>
                     )}
                   </div>
                 ))}
               </div>
             )}
           </div>"""
           
# Inject after HSK dropdown
# The HSK dropdown ends with:
#                    </div>
#                  ))}
#                </div>
#              )}
#            </div>
old_hsk_block_end = """</div>
                 ))}
               </div>
             )}
           </div>"""
           
# Need to be careful. I will use regex to find the HSK dropdown block
hsk_block_regex = re.compile(r'(<div className="tab-dropdown" onMouseEnter=\{.*?setShowHskMenu\(true\).*?</div>\s*)\n\s*<div className="tab-dropdown" onMouseEnter=\{.*?setShowNhoMenu', re.DOTALL)
match = hsk_block_regex.search(content)
if match:
    # Insert new_hsk_v3 before showNhoMenu dropdown
    content = content[:match.end(1)] + new_hsk_v3 + "\n           <div className=\"tab-dropdown\" onMouseEnter={() => setShowNhoMenu" + content[match.end():]
    print("Injected HSK v3 dropdown!")
else:
    print("Could not find HSK dropdown block to inject after.")

with open("src/App.jsx", "w", encoding="utf-8") as f:
    f.write(content)

