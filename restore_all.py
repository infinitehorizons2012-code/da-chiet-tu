import re

with open('src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add import TracNghiemTab
if 'import TracNghiemTab' not in content:
    content = "import TracNghiemTab from './TracNghiemTab';\n" + content

# 2. Add userStats and savedSession state to App
old_state = """  const [currentUser, setCurrentUser] = useState(null);
  const [baseDataLoaded, setBaseDataLoaded] = useState(false);"""
new_state = """  const [currentUser, setCurrentUser] = useState(null);
  const [userStats, setUserStats] = useState({ xp: 0, lp: 0 });
  const [savedSession, setSavedSession] = useState(null);
  const [baseDataLoaded, setBaseDataLoaded] = useState(false);"""
content = content.replace(old_state, new_state)

# 3. Modify fetch updates to load stats and session
old_fetch = """        .then(data => {
          const updates = data.updates || {};"""
new_fetch = """        .then(data => {
          const updates = data.updates || {};
          
          if (updates['__USER_STATS__']) {
              setUserStats(updates['__USER_STATS__'].stats || { xp: 0, lp: 0 });
          }
          if (updates['__QUIZ_SESSION__']) {
              setSavedSession(updates['__QUIZ_SESSION__'].session || null);
          }
"""
content = content.replace(old_fetch, new_fetch)

# 4. Pass props to Header
old_header = """<Header primaryTab={primaryTab} setPrimaryTab={setPrimaryTab} currentUser={currentUser} setCurrentUser={setCurrentUser} />"""
new_header = """<Header primaryTab={primaryTab} setPrimaryTab={setPrimaryTab} currentUser={currentUser} setCurrentUser={setCurrentUser} userStats={userStats} />"""
content = content.replace(old_header, new_header)

# 4b. Update Header component definition
old_header_def = """function Header({ primaryTab, setPrimaryTab, currentUser, setCurrentUser }) {"""
new_header_def = """function Header({ primaryTab, setPrimaryTab, currentUser, setCurrentUser, userStats }) {"""
content = content.replace(old_header_def, new_header_def)

# 4c. Update Header HTML for LP/XP
old_header_html = """<span className="username">{currentUser || 'hang'}</span>"""
new_header_html = """{userStats && (
          <span style={{ marginRight: '15px', fontWeight: 'bold', fontSize: '0.9rem' }}>
             <span style={{ color: '#f59e0b' }}>⚡ {userStats.xp} XP</span> | <span style={{ color: '#3b82f6' }}>🛡️ {userStats.lp} LP</span>
          </span>
        )}
        <span className="username">{currentUser || 'hang'}</span>"""
content = content.replace(old_header_html, new_header_html)

# 5. Remove internal TracNghiemTab
start_idx = content.find('function TracNghiemTab')
if start_idx != -1:
    # find next function or end
    end_idx = content.find('export default App', start_idx)
    if end_idx != -1:
        content = content[:start_idx] + content[end_idx:]

# 6. Pass props to TracNghiemTab
old_trac = """{primaryTab === 'tracnghiem' && <TracNghiemTab currentUser={currentUser} />}"""
new_trac = """{primaryTab === 'tracnghiem' && <TracNghiemTab currentUser={currentUser} userStats={userStats} setUserStats={setUserStats} savedSession={savedSession} setSavedSession={setSavedSession} researchDataObj={researchDataObj} getSrsStatus={getSrsStatus} getSrsLevel={getSrsLevel} />}"""
content = content.replace(old_trac, new_trac)

# 7. Add getSrsLevel
old_streak = """const getSrsStreak = (item, skill) => {"""
new_streak = """const getSrsLevel = (item, skill) => {
  if (!item.srs) return 0;
  if (item.srs.status && typeof item.srs.status === 'string') {
     if (skill === 'chiettu') return item.srs.level || 0;
     return 0;
  }
  if (item.srs[skill]) return item.srs[skill].level || 0;
  return 0;
};

const getSrsStreak = (item, skill) => {"""
if 'const getSrsLevel' not in content:
    content = content.replace(old_streak, new_streak)

# 8. Remove logo text
old_logo = """        <div className="logo-icon">字</div>
        <div className="logo-text">
          <span className="title">Bản đồ Chiết tự</span>
          <span className="subtitle">HỆ THỐNG PHÂN TÍCH CHỮ HÁN</span>
        </div>"""
new_logo = """        <div className="logo-icon">字</div>"""
content = content.replace(old_logo, new_logo)

# 9. Completely replace LuyenTapTab
luyen_start = content.find('function LuyenTapTab')
if luyen_start != -1:
    luyen_end = content.find('export default App', luyen_start)
    
    new_luyentap = """function LuyenTapTab({ setPrimaryTab, setActiveTab, setGlobalLookupTerm, currentUser }) {
    const tabs = [
      { id: 'bat_dau', label: '🆕 Bắt đầu' },
      { id: 'san_sang_thi', label: '🎯 Sẵn sàng thi' },
      { id: 'hat_mam', label: '🌱 Hạt mầm' },
      { id: 'cay', label: '🌲 Cây' },
      { id: 'hoa', label: '🌸 Hoa' }
    ];
    const [activeTab, setLocalActiveTab] = useState('bat_dau');
    const [renderTrigger, setRenderTrigger] = useState(0);

    const filteredData = useMemo(() => {
      return researchDataObj.filter(item => {
        if (!item.srs) return false;
        
        let hasBatDau = false;
        let hasSanSangThi = false;
        let hasHatMam = false;
        let hasCay = false;
        let hasHoa = false;
        
        SKILLS.forEach(skill => {
           const st = getSrsStatus(item, skill.id);
           if (st === 'bat_dau') hasBatDau = true;
           if (st === 'san_sang_thi') hasSanSangThi = true;
           if (st === 'hat_mam') hasHatMam = true;
           if (st === 'cay') hasCay = true;
           if (st === 'hoa') hasHoa = true;
        });

        if (activeTab === 'bat_dau') return hasBatDau && !hasSanSangThi && !hasHatMam && !hasCay && !hasHoa;
        if (activeTab === 'san_sang_thi') return hasSanSangThi;
        if (activeTab === 'hat_mam') return hasHatMam;
        if (activeTab === 'cay') return hasCay;
        if (activeTab === 'hoa') return hasHoa;
        return false;
      });
    }, [activeTab, renderTrigger]);

    const handleStudy = (char) => {
      setGlobalLookupTerm(char);
      setActiveTab('lookup');
      setPrimaryTab('tracuu');
    };

    const handleMoveAllToReady = async (charObj) => {
      const originalSrs = { ...charObj.srs };
      
      let newSrs = { ...charObj.srs };
      SKILLS.forEach(skill => {
         newSrs = buildNewSrs({srs: newSrs}, skill.id, 'san_sang_thi', 0);
      });
      
      charObj.srs = newSrs;
      setRenderTrigger(v => v + 1);

      try {
        const res = await fetch('/api/save', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: currentUser,
            char: charObj['Chữ Trung Quốc'],
            comps: { srs: newSrs }
          })
        });
        const data = await res.json();
        if (!data.success) {
          charObj.srs = originalSrs;
          setRenderTrigger(v => v + 1);
        }
      } catch (err) {
        charObj.srs = originalSrs;
        setRenderTrigger(v => v + 1);
      }
    };

    const getIconForStatus = (status) => {
        if (status === 'san_sang_thi') return '🎯';
        if (status === 'hat_mam') return '🌱';
        if (status === 'cay') return '🌲';
        if (status === 'hoa') return '🌸';
        return '⚪';
    };

    return (
      <div className="tonghop-tab">
        <div className="tab-navigation" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', gap: '5px', overflowX: 'auto', paddingBottom: '10px' }}>
            {tabs.map(tab => (
               <button 
                 key={tab.id}
                 className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`} 
                 onClick={() => setLocalActiveTab(tab.id)}
                 style={{ whiteSpace: 'nowrap' }}
               >
                 {tab.label}
               </button>
            ))}
          </div>
        </div>
        <div className="tonghop-list">
          {filteredData.map((item, idx) => (
            <div key={idx} className="tonghop-item" style={{ display: 'flex', flexDirection: 'column', padding: '15px' }}>
               <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
                   <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
                       <div className="tonghop-index">{idx + 1}</div>
                       <div className="tonghop-char">{item['Chữ Trung Quốc']}</div>
                       <div className="tonghop-info" style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                          <span className="pinyin">{item['Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)']}</span>
                          <span className="nghia">{item['Nghĩa Tiếng Việt (Master 100%)']}</span>
                       </div>
                   </div>
                   <div className="tonghop-actions">
                      <button className="study-btn" onClick={() => handleStudy(item['Chữ Trung Quốc'])}>Học</button>
                      {activeTab === 'bat_dau' && (
                        <button className="ready-btn" onClick={() => handleMoveAllToReady(item)}>Sẵn sàng thi</button>
                      )}
                   </div>
               </div>
               
               <div style={{ marginTop: '15px', background: '#f8fafc', padding: '10px', borderRadius: '8px', display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
                  {SKILLS.map(skill => {
                      const st = getSrsStatus(item, skill.id);
                      return (
                          <div key={skill.id} style={{ display: 'flex', alignItems: 'center', gap: '5px', fontSize: '0.85rem', background: 'white', padding: '4px 8px', borderRadius: '4px', border: '1px solid #e2e8f0' }}>
                              <span title={st}>{getIconForStatus(st)}</span>
                              <span style={{ color: '#64748b' }}>{skill.label}</span>
                          </div>
                      );
                  })}
               </div>
            </div>
          ))}
          {filteredData.length === 0 && <div className="empty-msg">Chưa có chữ nào ở mục này.</div>}
        </div>
      </div>
    );
}
"""
    content = content[:luyen_start] + new_luyentap + "\n" + content[luyen_end:]


with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Restored ALL fixes!")
