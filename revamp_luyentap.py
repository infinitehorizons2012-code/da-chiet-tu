import re

with open('src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# I will replace the entire LuyenTapTab function
start_idx = content.find('function LuyenTapTab')
end_idx = content.find('function App()')

new_func = """function LuyenTapTab({ setPrimaryTab, setActiveTab, setGlobalLookupTerm, currentUser }) {
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
        
        // Find if this character belongs to the activeTab
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

        if (activeTab === 'bat_dau') return hasBatDau && !hasSanSangThi && !hasHatMam && !hasCay && !hasHoa; // ONLY bat_dau
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
      
      // Update ALL skills to san_sang_thi
      let newSrs = { ...charObj.srs };
      SKILLS.forEach(skill => {
         newSrs = buildNewSrs({srs: newSrs}, skill.id, 'san_sang_thi', 0);
      });
      
      // Optimistic UI Update
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
          charObj.srs = originalSrs; // Revert
          setRenderTrigger(v => v + 1);
        }
      } catch (err) {
        charObj.srs = originalSrs; // Revert
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
          <div>
            {tabs.map(tab => (
               <button 
                 key={tab.id}
                 className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`} 
                 onClick={() => setLocalActiveTab(tab.id)}
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

content = content[:start_idx] + new_func + content[end_idx:]

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated LuyenTapTab layout")
