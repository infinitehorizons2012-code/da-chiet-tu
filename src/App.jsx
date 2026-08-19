import TracNghiemTab from './TracNghiemTab';
import { useState, useEffect, useRef, useMemo } from 'react'
import HanziWriter from 'hanzi-writer'
import './index.css'

let researchDataObj = [];

const SKILLS = [
  { id: 'chiettu', label: 'Chiết tự' },
  { id: 'han_pinyin', label: 'Hán -> Pinyin' },
  { id: 'pinyin_han', label: 'Pinyin -> Hán' },
  { id: 'han_hanviet', label: 'Hán -> Hán Việt' },
  { id: 'hanviet_han', label: 'Hán Việt -> Hán' },
  { id: 'han_nghia', label: 'Hán -> Nghĩa' },
  { id: 'han_mnemonic', label: 'Hán -> Mnemonic' },
  { id: 'mnemonic_han', label: 'Mnemonic -> Hán' }
];

const getSrsStatus = (item, skill) => {
  if (!item.srs) return null;
  // Format cũ (chỉ có status string ở gốc)
  if (item.srs.status && typeof item.srs.status === 'string') {
     if (skill === 'chiettu') return item.srs.status;
     return 'bat_dau';
  }
  // Format mới
  if (item.srs[skill]) return item.srs[skill].status;
  return 'bat_dau';
};

const getSrsLevel = (item, skill) => {
  if (!item.srs) return 0;
  if (item.srs.status && typeof item.srs.status === 'string') {
     if (skill === 'chiettu') return item.srs.level || item.srs.streak || 0;
     return 0;
  }
  if (item.srs[skill]) return item.srs[skill].level || item.srs[skill].streak || 0;
  return 0;
};

const getSrsStreak = (item, skill) => {
  if (!item.srs) return 0;
  if (item.srs.status && typeof item.srs.status === 'string') {
     if (skill === 'chiettu') return item.srs.streak || 0;
     return 0;
  }
  if (item.srs[skill]) return item.srs[skill].streak || 0;
  return 0;
};

const buildNewSrs = (item, skillToUpdate, newStatus, newStreak) => {
   let srs = { ...item.srs };
   if (srs.status && typeof srs.status === 'string') {
      const oldStatus = srs.status;
      const oldStreak = srs.streak || 0;
      srs = {};
      SKILLS.forEach(s => {
         srs[s.id] = { status: s.id === 'chiettu' ? oldStatus : 'bat_dau', streak: s.id === 'chiettu' ? oldStreak : 0 };
      });
   } else {
      SKILLS.forEach(s => {
         if (!srs[s.id]) srs[s.id] = { status: 'bat_dau', streak: 0 };
      });
   }
   
   if (skillToUpdate) {
      srs[skillToUpdate] = { status: newStatus, streak: newStreak };
   }
   return srs;
};

function Header({ primaryTab, setPrimaryTab, currentUser, setCurrentUser, userStats }) {
  const handleLogout = () => {
    setCurrentUser(null);
  };

  return (
    <header className="app-header">
      <div className="header-left">
        <div className="logo-icon">字</div>
      </div>
      
      <nav className="header-nav">
        <button className={`nav-item ${primaryTab === 'tracuu' ? 'active' : ''}`} onClick={() => setPrimaryTab('tracuu')}>
          <span className="nav-icon">🔍</span> Tra cứu
        </button>
        <button className={`nav-item ${primaryTab === 'tonghop' ? 'active' : ''}`} onClick={() => setPrimaryTab('tonghop')}>
          <span className="nav-icon">📚</span> Tổng hợp
        </button>
        <button className={`nav-item ${primaryTab === 'luyentap' ? 'active' : ''}`} onClick={() => setPrimaryTab('luyentap')}>
          <span className="nav-icon">📝</span> Luyện tập
        </button>
        <button className={`nav-item ${primaryTab === 'tracnghiem' ? 'active' : ''}`} onClick={() => setPrimaryTab('tracnghiem')}>
          <span className="nav-icon">🎮</span> Trắc nghiệm
        </button>
      </nav>

      <div className="header-right">
        <div className="user-info">
          {userStats && (
          <span style={{ marginRight: '15px', fontWeight: 'bold', fontSize: '0.9rem' }}>
             <span style={{ color: '#f59e0b' }}>⚡ {userStats.xp} XP</span> | <span style={{ color: '#3b82f6' }}>🛡️ {userStats.lp} LP</span>
          </span>
        )}
        </div>
        <button className="icon-button" onClick={handleLogout} title="Đăng xuất">🚪</button>
      </div>
    </header>
  );
}

function HanziDisplay({ char, components }) {
  const containerRef = useRef(null);
  const writerRef = useRef(null);

  // Tạo CSS tuỳ chỉnh bôi màu chính xác vào từng nét vẽ (stroke)
  const customCss = useMemo(() => {
    if (!components) return '';
    let css = '';
    components.forEach(comp => {
      if (comp.strokes) {
        comp.strokes.forEach(idx => {
          css += `
            .custom-hanzi-colors svg path:nth-child(${idx + 1}) {
              fill: ${comp.color} !important;
              stroke: ${comp.color} !important;
            }
          `;
        });
      }
    });
    return css;
  }, [components]);

  useEffect(() => {
    if (!containerRef.current) return;
    
    containerRef.current.innerHTML = '';
    
    writerRef.current = HanziWriter.create(containerRef.current, char, {
      width: 180,
      height: 180,
      padding: 5,
      strokeColor: '#cbd5e1', 
      radicalColor: null, 
      showOutline: false,
      strokeAnimationSpeed: 1.5,
      delayBetweenStrokes: 150,
      onLoadCharDataSuccess: () => {
        setTimeout(() => {
          if (writerRef.current) {
            writerRef.current.animateCharacter();
          }
        }, 300); // 300ms delay for visual smoothness when loading
      }
    });
  }, [char]);

  const handleAnimate = () => {
    if (writerRef.current) {
      writerRef.current.animateCharacter();
    }
  };

  return (
    <div className="char-display-container">
      <div className="custom-hanzi-colors" style={{cursor: 'pointer'}} onClick={handleAnimate} title="Nhấn để xem cách viết">
        <style>{customCss}</style>
        <div ref={containerRef} className="char-writer" />
      </div>
      <button className="animate-button" onClick={handleAnimate}>
        ✍️ Xem cách viết
      </button>
    </div>
  );
}

function LookupTab({ globalLookupTerm, setGlobalLookupTerm }) {
  const [searchTerm, setSearchTerm] = useState(globalLookupTerm || '')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    if (globalLookupTerm) {
      setSearchTerm(globalLookupTerm);
      handleSearch(null, globalLookupTerm);
    }
  }, [globalLookupTerm]);

  
    const audioInstanceRef = React.useRef(null);
    const playAudio = (url) => {
      if (!url) return;
      if (audioInstanceRef.current) {
        if (audioInstanceRef.current.src === url && !audioInstanceRef.current.paused) {
          audioInstanceRef.current.pause();
          audioInstanceRef.current.currentTime = 0;
          return;
        }
        audioInstanceRef.current.pause();
      }
      audioInstanceRef.current = new Audio(url);
      audioInstanceRef.current.play().catch(e => console.error("Audio play failed:", e));
    };
    const handleSearch = async (e, termOverride = null) => {
    if (e) e.preventDefault()
    const char = (termOverride !== null ? termOverride : searchTerm).trim()
    if (!char) return
    
    if (e && char !== globalLookupTerm) {
       setGlobalLookupTerm(char);
    }
    
    const researchData = researchDataObj.find(item => item['Chữ Trung Quốc'] === char);

    if (researchData) {
      const newResult = {
        char: researchData['Chữ Trung Quốc'],
        pinyin: researchData['Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)'] || '',
        hanviet: researchData['Âm Hán Việt (Master 100%)'] || '',
        meaning: researchData['Nghĩa Tiếng Việt (Master 100%)'] || '',
        mnemonic: researchData['App_Mnemonic'] || '',
        components: []
      };

      const colors = ['#2563eb', '#e11d48', '#059669', '#eab308', '#a855f7', '#10b981'];
      let compIndex = 0;
      for (let i = 1; i <= 12; i++) {
        const compStr = researchData[`App_Comp_${i}`];
        if (compStr && compStr !== 'nan' && compStr.trim() !== '') {
          // Parse format like "白 Bạch (106)"
          const match = compStr.trim().match(/^([^\s]+)\s+([^\(]+?)\s*\((.+?)\)$/);
          if (match) {
            newResult.components.push({
              id: `App_Comp_${i}`,
              type: i === 1 ? 'Radical' : 'Component',
              char: match[1],
              hanviet: match[2].trim(),
              keyword: match[3].trim(),
              color: colors[compIndex % colors.length],
              strokes: [], 
              imageUrl: ''
            });
          } else {
             const parts = compStr.trim().split(' ');
             const c = parts[0] || '';
             const hv = parts.slice(1).join(' ') || '';
             newResult.components.push({
              id: `App_Comp_${i}`,
              type: i === 1 ? 'Radical' : 'Component',
              char: c,
              hanviet: hv,
              keyword: hv,
              color: colors[compIndex % colors.length],
              strokes: [], 
              imageUrl: ''
            });
          }
          compIndex++;
        }
      }

      setResult(newResult);
      setError('');

      // If quiz_mapping exists, use it!
      if (researchData.quiz_mapping) {
        newResult.components.forEach(comp => {
          if (researchData.quiz_mapping[comp.id]) {
            comp.strokes = researchData.quiz_mapping[comp.id];
          }
        });
        setResult({ ...newResult });
      } else {
        // Fallback: Dynamically fetch stroke counts (flawed for characters with shared strokes)
        try {
          let currentStrokeIdx = 0;
          let strokeDataUpdated = false;
          for (let comp of newResult.components) {
            if (comp.char) {
              const res = await fetch(`https://cdn.jsdelivr.net/npm/hanzi-writer-data@2.0/${comp.char}.json`);
              if (res.ok) {
                const data = await res.json();
                const count = data.strokes.length;
                comp.strokes = Array.from({length: count}, (_, i) => currentStrokeIdx + i);
                currentStrokeIdx += count;
                strokeDataUpdated = true;
              }
            }
          }
          if (strokeDataUpdated) {
            setResult({
              ...newResult,
              components: newResult.components.map(c => ({...c}))
            });
          }
        } catch (err) {
          console.error("Lỗi khi tải dữ liệu nét chữ:", err);
        }
      }

    } else {
      setError(`Chưa có dữ liệu cho chữ "${char}".`)
    }
  }

  return (
    <div className="tab-content">
      <form className="search-container" onSubmit={handleSearch}>
        <input 
          type="text" 
          className="search-input" 
          placeholder="Nhập chữ Hán (VD: 南, 茶)..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          maxLength={1}
        />
        <button type="submit" className="search-button">Phân tích</button>
      </form>

      {error && <p className="error-text">{error}</p>}

      {result && !error && (
        <div className="infographic-panel">
          {/* Khu vực 1: Từ và cách viết (top-left) */}
          <div className="quadrant-top-left">
            <HanziDisplay char={result.char} components={result.components} />
          </div>

          {/* Đường chia cắt giữa */}
          <div className="divider-line"></div>

          {/* Khu vực 2: Chiết tự (top-right) */}
          <div className="components-list">
            {result.components.map((comp, idx) => (
              <div key={idx} className="breakdown-row">
                <div className="comp-char-block">
                  <div className="comp-char-large" style={{ color: comp.color }}>
                    {comp.char}
                  </div>
                  <div className="comp-hanviet">{comp.hanviet}</div>
                </div>
                
                <div className="horizontal-arrow">→</div>
                
                <div className="comp-image-placeholder">
                  {comp.imageUrl ? (
                    <img src={comp.imageUrl} alt={comp.keyword} />
                  ) : (
                    <div className="placeholder-box">Ảnh<br/>{comp.keyword}</div>
                  )}
                </div>
                
                <div className="comp-keyword-wrapper">
                  <div className="comp-keyword-box">{comp.keyword}</div>
                  <div className="vertical-arrow"></div>
                </div>
              </div>
            ))}
          </div>

          {/* Khu vực 3: Pinyin + Nghĩa + Hán Việt (bottom-left) */}
          <div className="info-block">
            <div className="info-pinyin" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
                {result.pinyin}
                {result.audioUrl && (
                    <span onClick={() => playAudio(result.audioUrl)} style={{ fontSize: '1.2rem', cursor: 'pointer', pointerEvents: 'auto' }}>🔊</span>
                )}
              </div>
            <div className="info-hanviet">{result.hanviet}</div>
            <div className="info-meaning">{result.meaning}</div>
          </div>

          {/* Khu vực 4: Giải thích / Thần chú (bottom-right) */}
          <div className="mnemonic-box">
            {result.mnemonic}
          </div>
        </div>
      )}
    </div>
  )
}

function ResearchTab({ globalLookupTerm, setGlobalLookupTerm }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortMode, setSortMode] = useState('frequency');
  const [selectedChar, setSelectedChar] = useState(null);
  const [history, setHistory] = useState([]);
  const [isSaving, setIsSaving] = useState(false);
  const [saveStatus, setSaveStatus] = useState('');
  const [editData, setEditData] = useState({});
  const [detailTab, setDetailTab] = useState('Ứng dụng');

  useEffect(() => {
    setEditData({});
    setSaveStatus('');
  }, [selectedChar]);

  
    const audioInstanceRef = React.useRef(null);
    const playAudio = (url) => {
      if (!url) return;
      if (audioInstanceRef.current) {
        if (audioInstanceRef.current.src === url && !audioInstanceRef.current.paused) {
          audioInstanceRef.current.pause();
          audioInstanceRef.current.currentTime = 0;
          return;
        }
        audioInstanceRef.current.pause();
      }
      audioInstanceRef.current = new Audio(url);
      audioInstanceRef.current.play().catch(e => console.error("Audio play failed:", e));
    };
    const handleSave = async () => {
    setIsSaving(true);
    setSaveStatus('Đang lưu...');
    try {
      const res = await fetch('/api/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: currentUser,
          char: selectedChar['Chữ Trung Quốc'],
          comps: editData
        })
      });
      if (!res.ok) {
        throw new Error(`Mã lỗi HTTP: ${res.status}`);
      }
      const data = await res.json();
      if (data.success) {
        setSaveStatus('Đã lưu thành công!');
        Object.assign(selectedChar, editData);
      } else {
        setSaveStatus('Lỗi: ' + data.error);
      }
    } catch (err) {
      setSaveStatus('Lỗi kết nối: ' + err.message);
    }
    setIsSaving(false);
  };

  const handleEditChange = (key, val) => {
    setEditData(prev => ({ ...prev, [key]: val }));
  };

  const isFieldEditable = (key) => key.startsWith('App_Comp_') || key === 'App_Mnemonic';

  const charMap = useMemo(() => {
    const map = new Map();
    researchDataObj.forEach(item => {
      if (item['Chữ Trung Quốc']) map.set(item['Chữ Trung Quốc'], item);
    });
    return map;
  }, []);

  useEffect(() => {
    if (globalLookupTerm) {
      const match = charMap.get(globalLookupTerm);
      if (match && (!selectedChar || selectedChar['Chữ Trung Quốc'] !== globalLookupTerm)) {
        setSelectedChar(match);
      }
    }
  }, [globalLookupTerm, charMap, selectedChar]);

  const handleSidebarSelect = (charObj) => {
    setHistory([]);
    setSelectedChar(charObj);
    setGlobalLookupTerm(charObj['Chữ Trung Quốc']);
  };

  const handleSelectChar = (charObj) => {
    if (selectedChar) {
      setHistory(prev => [...prev, selectedChar]);
    }
    setSelectedChar(charObj);
    setGlobalLookupTerm(charObj['Chữ Trung Quốc']);
  };

  const handleBack = () => {
    if (history.length > 0) {
      const prev = history[history.length - 1];
      setHistory(prevHistory => prevHistory.slice(0, -1));
      setSelectedChar(prev);
      setGlobalLookupTerm(prev['Chữ Trung Quốc']);
    }
  };

  const filteredData = useMemo(() => {
    let baseData = researchDataObj;
    
    if (sortMode === 'chunho') {
      baseData = [...researchDataObj].sort((a, b) => {
        const valA = parseFloat(a['ChuNhoTongHop_STT (Giáo trình Chữ Nho)']);
        const valB = parseFloat(b['ChuNhoTongHop_STT (Giáo trình Chữ Nho)']);
        const validA = !isNaN(valA);
        const validB = !isNaN(valB);
        if (validA && validB) return valA - valB;
        if (validA) return -1;
        if (validB) return 1;
        return 0;
      });
    }

    if (!searchTerm.trim()) return baseData;
    const lower = searchTerm.toLowerCase();
    return baseData.filter(item => {
      return (item['Chữ Trung Quốc'] && item['Chữ Trung Quốc'].includes(lower)) || 
             (item['Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)'] && item['Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)'].toLowerCase().includes(lower)) ||
             (item['Âm Hán Việt (Master 100%)'] && item['Âm Hán Việt (Master 100%)'].toLowerCase().includes(lower))
    });
  }, [searchTerm, sortMode]);

  const renderClickableValue = (val) => {
    if (typeof val !== 'string') return val;
    const cjkRegex = /[\u4e00-\u9fa5]/;
    const chars = Array.from(val);
    return chars.map((char, i) => {
      if (cjkRegex.test(char) && charMap.has(char)) {
        return (
          <span 
            key={i} 
            className="clickable-char" 
            onClick={() => handleSelectChar(charMap.get(char))}
          >
            {char}
          </span>
        );
      }
      return char;
    });
  };

  const DETAIL_TABS = ['Ứng dụng', 'Chữ Nho', 'Xie', 'GavinGrover', 'CHISE', 'Unihan', 'CC-CEDICT', 'Jun Da', 'Phân loại', 'Khác'];
  const getTabForKey = (key) => {
    if (key.startsWith('App_')) return 'Ứng dụng';
    if (key.includes('_Xie')) return 'Xie';
    if (key.includes('GavinGrover')) return 'GavinGrover';
    if (key.includes('CHISE')) return 'CHISE';
    if (key.includes('Unihan')) return 'Unihan';
    if (key.includes('CC-CEDICT')) return 'CC-CEDICT';
    if (key.includes('ChuNhoTongHop') || key === 'STT Chữ Nho Tổng Hợp') return 'Chữ Nho';
    if (key.includes('Jun Da')) return 'Jun Da';
    if (key.includes('HSK') || key === '9000' || key.toLowerCase().includes('group') || key.includes('words')) return 'Phân loại';
    return 'Khác';
  };

  return (
    <div className="research-container">
      <div className="research-sidebar">
        <div className="research-search">
          <input 
            type="text" 
            placeholder="Tìm chữ, pinyin, âm Hán Việt..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <div className="sidebar-tabs">
          <button 
            className={`sidebar-tab ${sortMode === 'frequency' ? 'active' : ''}`}
            onClick={() => setSortMode('frequency')}
          >
            Tần suất
          </button>
          <button 
            className={`sidebar-tab ${sortMode === 'chunho' ? 'active' : ''}`}
            onClick={() => setSortMode('chunho')}
          >
            Giáo trình
          </button>
        </div>
        <div className="research-list">
          {filteredData.slice(0, 500).map((item, idx) => (
             <div 
               key={idx} 
               className={`research-list-item ${selectedChar === item ? 'active' : ''}`}
               onClick={() => handleSidebarSelect(item)}
             >
               <span className="research-list-char">{item['Chữ Trung Quốc']}</span>
               <span className="research-list-pinyin">{item['Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)'] || ''}</span>
             </div>
          ))}
          {filteredData.length > 500 && <div className="research-list-more">...và {filteredData.length - 500} chữ khác</div>}
        </div>
      </div>
      <div className="research-detail">
        {selectedChar ? (
          <div className="research-detail-content">
             <div className="detail-actions-top">
               {history.length > 0 && (
                 <button className="back-btn" onClick={handleBack}>
                   ← Quay lại
                 </button>
               )}
               {Object.keys(selectedChar).some(isFieldEditable) && (
                 <div className="save-container">
                   <button className="save-btn" onClick={handleSave} disabled={isSaving || Object.keys(editData).length === 0}>
                     {isSaving ? 'Đang lưu...' : 'Lưu thay đổi'}
                   </button>
                   {saveStatus && saveStatus !== 'Đang lưu...' && <span className="save-status">{saveStatus}</span>}
                 </div>
               )}
             </div>
             <div className="detail-header">
                <div className="detail-header-char">{selectedChar['Chữ Trung Quốc']}</div>
                <div className="detail-pinyin" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
                    {selectedChar['Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)']}
                    {selectedChar['Link Âm Thanh Pinyin (Cloudinary MP3)'] && (
                        <span onClick={() => playAudio(selectedChar['Link Âm Thanh Pinyin (Cloudinary MP3)'])} style={{ fontSize: '1.2rem', cursor: 'pointer', pointerEvents: 'auto' }}>🔊</span>
                    )}
                    - {selectedChar['Âm Hán Việt (Master 100%)']}
                  </div>
                <div className="detail-meaning">{selectedChar['Nghĩa Tiếng Việt (Master 100%)']}</div>
             </div>

             <div className="detail-inner-tabs">
                {DETAIL_TABS.map(tab => (
                  <button 
                    key={tab}
                    className={`inner-tab ${detailTab === tab ? 'active' : ''}`}
                    onClick={() => setDetailTab(tab)}
                  >
                    {tab}
                  </button>
                ))}
             </div>

             <div className="detail-grid">
               {Object.keys(selectedChar).map((key, idx) => {
                 if (key === 'Chữ Trung Quốc' || key === 'Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)' || key === 'Âm Hán Việt (Master 100%)' || key === 'Nghĩa Tiếng Việt (Master 100%)' || key === 'quiz_mapping') return null;
                 
                 // Lọc theo tab hiện tại
                 if (getTabForKey(key) !== detailTab) return null;

                 const isEditable = isFieldEditable(key);
                 const val = isEditable && editData[key] !== undefined ? editData[key] : selectedChar[key];
                 const isMissing = !val || val === 'nan';
                 
                 return (
                   <div key={idx} className="detail-card">
                     <div className="detail-card-title">{key.toUpperCase()}</div>
                     {isEditable ? (
                       <textarea 
                         className="detail-card-textarea"
                         value={isMissing ? '' : val}
                         onChange={(e) => handleEditChange(key, e.target.value)}
                         placeholder="Nhập nội dung..."
                       />
                     ) : (
                       <div className="detail-card-value">
                         {isMissing ? (
                           <span className="empty-val" style={{fontStyle: 'italic', color: '#94a3b8'}}>Chưa có dữ liệu</span>
                         ) : (
                           renderClickableValue(val)
                         )}
                       </div>
                     )}
                   </div>
                 );
               })}
             </div>
          </div>
        ) : (
          <div className="research-placeholder">Chọn một chữ Hán trong danh sách để xem chi tiết.</div>
        )}
      </div>
    </div>
  )
}


function LoginScreen({ onLogin }) {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    const action = isRegister ? 'register' : 'login';
    try {
      const res = await fetch(`/api/auth?action=${action}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      const data = await res.json();
      if (data.success) {
         if (isRegister) {
            setIsRegister(false);
            setError('Tạo tài khoản thành công! Hãy đăng nhập.');
         } else {
            onLogin(username);
         }
      } else {
         setError(data.error);
      }
    } catch (err) {
      setError('Lỗi kết nối: ' + err.message);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Bạn có chắc chắn muốn xóa tài khoản này và TOÀN BỘ dữ liệu học tập không?')) return;
    try {
      const res = await fetch(`/api/auth?action=delete`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      const data = await res.json();
      if (data.success) {
         setError('Xóa tài khoản thành công!');
         setUsername('');
         setPassword('');
      } else {
         setError(data.error);
      }
    } catch (err) {
      setError('Lỗi kết nối: ' + err.message);
    }
  };

  return (
    <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', background: '#f8fafc'}}>
      <div style={{background: 'white', padding: '40px', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)', width: '400px'}}>
        <h2 style={{textAlign: 'center', marginBottom: '20px', color: '#1e293b'}}>{isRegister ? 'Tạo Tài Khoản' : 'Đăng Nhập'}</h2>
        <form onSubmit={handleSubmit} style={{display: 'flex', flexDirection: 'column', gap: '15px'}}>
          <input 
            type="text" 
            placeholder="Tên tài khoản (vd: bebi)" 
            value={username} 
            onChange={e => setUsername(e.target.value)}
            style={{padding: '10px', borderRadius: '6px', border: '1px solid #cbd5e1'}}
            required 
          />
          <input 
            type="password" 
            placeholder="Mật khẩu" 
            value={password} 
            onChange={e => setPassword(e.target.value)}
            style={{padding: '10px', borderRadius: '6px', border: '1px solid #cbd5e1'}}
            required 
          />
          {error && <div style={{color: error.includes('thành công') ? 'green' : 'red', fontSize: '0.9rem'}}>{error}</div>}
          <button type="submit" style={{background: '#3b82f6', color: 'white', padding: '10px', borderRadius: '6px', fontWeight: 'bold', cursor: 'pointer'}}>
            {isRegister ? 'Đăng ký' : 'Đăng nhập'}
          </button>
        </form>
        <div style={{marginTop: '20px', textAlign: 'center', fontSize: '0.9rem'}}>
          <span style={{color: '#64748b', cursor: 'pointer', textDecoration: 'underline'}} onClick={() => setIsRegister(!isRegister)}>
            {isRegister ? 'Đã có tài khoản? Đăng nhập' : 'Chưa có tài khoản? Đăng ký'}
          </span>
        </div>
        {!isRegister && (
          <div style={{marginTop: '15px', textAlign: 'center', fontSize: '0.9rem'}}>
            <span style={{color: '#ef4444', cursor: 'pointer', textDecoration: 'underline'}} onClick={handleDelete}>
              Xóa tài khoản này
            </span>
          </div>
        )}
      </div>
    </div>
  );
}

function App() {
  const [primaryTab, setPrimaryTab] = useState('tracuu');
  const [activeTab, setActiveTab] = useState('lookup');
  const [dataReady, setDataReady] = useState(false);
  const [globalLookupTerm, setGlobalLookupTerm] = useState('');
  const [currentUser, setCurrentUser] = useState(null);
  const [userStats, setUserStats] = useState({ xp: 0, lp: 0 });
  const [savedSession, setSavedSession] = useState(null);
  const [baseDataLoaded, setBaseDataLoaded] = useState(false);

  useEffect(() => {
    // 1. Fetch static base data ONCE
    Promise.all([
      fetch('/data/research_data_1.json').then(res => res.json()),
      fetch('/data/research_data_2.json').then(res => res.json())
    ])
      .then(([part1, part2]) => {
        researchDataObj.push(...part1, ...part2);
        setBaseDataLoaded(true);
      });
  }, []);

  useEffect(() => {
    if (!currentUser || !baseDataLoaded) return;
    
    setDataReady(false);
    // Reset SRS and user data
    researchDataObj.forEach(item => { item.srs = undefined; item.quiz_mapping = undefined; item.parsedComps = undefined; });

    fetch(`/api/updates?username=${currentUser}`)
      .then(res => res.json())
      .then(data => {
        if (data && data.success && data.updates) {
          const updates = data.updates;
          researchDataObj.forEach(item => {
            const char = item['Chữ Trung Quốc'];
            if (updates[char]) {
              Object.assign(item, updates[char]);
            }
          });
        }
        setDataReady(true);
      })
      .catch(err => {
        console.error("Failed to load updates:", err);
        setDataReady(true);
      });
  }, [currentUser, baseDataLoaded]);

  if (!currentUser) {
    return <LoginScreen onLogin={setCurrentUser} />;
  }

  if (!dataReady) {
    return <div style={{textAlign: 'center', marginTop: '50px'}}>Đang đồng bộ dữ liệu từ Cloudflare...</div>;
  }

  return (
    <div className="app-container">
      <Header primaryTab={primaryTab} setPrimaryTab={setPrimaryTab} currentUser={currentUser} setCurrentUser={setCurrentUser} userStats={userStats} />
      
      {primaryTab === 'tracuu' && (
        <>
          <div className="tab-navigation">
            <button 
              className={activeTab === 'lookup' ? 'tab-btn active' : 'tab-btn'} 
              onClick={() => setActiveTab('lookup')}
            >
              Tra Cứu Nhanh
            </button>
            <button 
              className={activeTab === 'research' ? 'tab-btn active' : 'tab-btn'} 
              onClick={() => setActiveTab('research')}
            >
              Nghiên Cứu Chi Tiết
            </button>
            <button 
              className={activeTab === 'chiettu' ? 'tab-btn active' : 'tab-btn'} 
              onClick={() => setActiveTab('chiettu')}
            >
              Chiết Tự (Tô nét)
            </button>
          </div>
          
          {activeTab === 'lookup' && <LookupTab globalLookupTerm={globalLookupTerm} setGlobalLookupTerm={setGlobalLookupTerm} />}
          {activeTab === 'research' && <ResearchTab globalLookupTerm={globalLookupTerm} setGlobalLookupTerm={setGlobalLookupTerm} />}
          {activeTab === 'chiettu' && <ChietTuAdminTab globalLookupTerm={globalLookupTerm} setGlobalLookupTerm={setGlobalLookupTerm} currentUser={currentUser} />}
        </>
      )}

      {primaryTab === 'tonghop' && <TongHopTab currentUser={currentUser} />}
      
      {primaryTab === 'luyentap' && <LuyenTapTab setPrimaryTab={setPrimaryTab} setActiveTab={setActiveTab} setGlobalLookupTerm={setGlobalLookupTerm} currentUser={currentUser} />}
      
      {primaryTab === 'tracnghiem' && <TracNghiemTab currentUser={currentUser} userStats={userStats} setUserStats={setUserStats} savedSession={savedSession} setSavedSession={setSavedSession} researchDataObj={researchDataObj} getSrsStatus={getSrsStatus} getSrsLevel={getSrsLevel} />}
      
    </div>
  )
}

function ChietTuAdminTab({ globalLookupTerm, setGlobalLookupTerm, currentUser }) {
  const [searchTerm, setSearchTerm] = useState(globalLookupTerm || '')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [strokePaths, setStrokePaths] = useState([])
  const [strokeColors, setStrokeColors] = useState({}) // { strokeIndex: colorCode }
  const [activeComp, setActiveComp] = useState(null)
  const [saving, setSaving] = useState(false)

  // Colors mapping for 12 components
  const COLORS = [
    '#e11d48', '#2563eb', '#059669', '#eab308', 
    '#a855f7', '#10b981', '#f97316', '#14b8a6', 
    '#6366f1', '#ec4899', '#8b5cf6', '#0ea5e9'
  ];

  useEffect(() => {
    if (globalLookupTerm) {
      setSearchTerm(globalLookupTerm);
      handleLoadCharacter(globalLookupTerm);
    }
  }, [globalLookupTerm]);

  const handleLoadCharacter = async (charToLoad) => {
    const char = charToLoad.trim();
    if (!char) return;

    if (char !== globalLookupTerm) {
      setGlobalLookupTerm(char);
    }

    const researchData = researchDataObj.find(item => item['Chữ Trung Quốc'] === char);

    if (researchData) {
      const comps = [];
      let compIndex = 0;
      for (let i = 1; i <= 12; i++) {
        const compStr = researchData[`App_Comp_${i}`];
        if (compStr && compStr !== 'nan' && compStr.trim() !== '') {
          comps.push({
            id: `App_Comp_${i}`,
            text: compStr.trim(),
            color: COLORS[compIndex % COLORS.length]
          });
          compIndex++;
        }
      }

      setResult({ char, comps });
      setError('');
      setStrokeColors({});
      setActiveComp(comps[0] || null);

      // Load existing quiz_mapping if any
      if (researchData.quiz_mapping) {
        const existingMapping = researchData.quiz_mapping;
        const newStrokeColors = {};
        comps.forEach(comp => {
          if (existingMapping[comp.id]) {
            existingMapping[comp.id].forEach(strokeIdx => {
              newStrokeColors[strokeIdx] = comp.color;
            });
          }
        });
        setStrokeColors(newStrokeColors);
      }

      // Fetch SVG data
      try {
        const res = await fetch(`https://cdn.jsdelivr.net/npm/hanzi-writer-data@2.0/${char}.json`);
        if (res.ok) {
          const data = await res.json();
          setStrokePaths(data.strokes);
        } else {
          setStrokePaths([]);
          setError(`Không tìm thấy dữ liệu nét vẽ cho chữ "${char}" từ HanziWriter.`);
        }
      } catch (err) {
        setStrokePaths([]);
        setError(`Lỗi tải dữ liệu nét vẽ: ${err.message}`);
      }
    } else {
      setError(`Chưa có dữ liệu cho chữ "${char}".`);
      setResult(null);
      setStrokePaths([]);
    }
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    handleLoadCharacter(searchTerm);
  };

  const handleStrokeClick = (strokeIndex) => {
    if (!activeComp) return;
    
    setStrokeColors(prev => {
      const next = { ...prev };
      // Toggle color off if clicking the same color
      if (next[strokeIndex] === activeComp.color) {
        delete next[strokeIndex];
      } else {
        next[strokeIndex] = activeComp.color;
      }
      return next;
    });
  };

  const handleSave = async () => {
    if (!result) return;
    
    setSaving(true);
    
    // Reverse map: group stroke indices by active component IDs
    const quiz_mapping = {};
    Object.entries(strokeColors).forEach(([strokeIdxStr, color]) => {
      const strokeIdx = parseInt(strokeIdxStr, 10);
      const comp = result.comps.find(c => c.color === color);
      if (comp) {
        if (!quiz_mapping[comp.id]) quiz_mapping[comp.id] = [];
        quiz_mapping[comp.id].push(strokeIdx);
      }
    });

    // Ensure they are sorted numerically
    Object.keys(quiz_mapping).forEach(k => {
      quiz_mapping[k].sort((a, b) => a - b);
    });

    try {
      const res = await fetch('/api/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: currentUser,
          char: result.char,
          comps: { quiz_mapping }
        })
      });
      const data = await res.json();
      if (data.success) {
        alert('Đã lưu đáp án thành công!');
        // Update local object so it persists across tab switches
        const item = researchDataObj.find(i => i['Chữ Trung Quốc'] === result.char);
        if (item) item.quiz_mapping = quiz_mapping;
      } else {
        alert('Lỗi lưu: ' + data.error);
      }
    } catch (err) {
      alert('Lỗi mạng: ' + err.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="tab-content chiettu-admin">
      <form className="search-container" onSubmit={handleSearchSubmit}>
        <input 
          type="text" 
          className="search-input" 
          placeholder="Nhập chữ Hán cần tạo đáp án..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          maxLength={1}
        />
        <button type="submit" className="search-button">Tải chữ</button>
      </form>

      {error && <p className="error-text">{error}</p>}

      {result && strokePaths.length > 0 && (
        <div className="chiettu-workspace">
          <div className="chiettu-svg-container">
            <svg 
              viewBox="0 0 1024 1024" 
              className="hanzi-svg"
            >
              <g transform="scale(1, -1) translate(0, -900)">
                {strokePaths.map((path, idx) => (
                  <path 
                    key={idx} 
                    d={path} 
                    className="hanzi-stroke-path"
                    fill={strokeColors[idx] || '#cbd5e1'} 
                    onClick={() => handleStrokeClick(idx)}
                  />
                ))}
              </g>
            </svg>
            <p className="hint-text">Click vào nét vẽ để tô màu theo linh kiện đang chọn bên phải</p>
          </div>

          <div className="chiettu-components-panel">
            <h3>Danh sách Linh kiện</h3>
            <div className="comp-list">
              {result.comps.map(comp => (
                <div 
                  key={comp.id}
                  className={`comp-item ${activeComp && activeComp.id === comp.id ? 'active' : ''}`}
                  style={{ borderLeftColor: comp.color }}
                  onClick={() => setActiveComp(comp)}
                >
                  <div className="comp-color-box" style={{ backgroundColor: comp.color }}></div>
                  <span className="comp-text">{comp.text}</span>
                </div>
              ))}
            </div>
            
            {currentUser === 'admin' ? (
              <button className="save-btn" onClick={handleSave} disabled={saving}>
                {saving ? 'Đang lưu...' : 'Lưu Đáp Án'}
              </button>
            ) : (
              <div style={{marginTop: '20px', color: '#ef4444', fontWeight: 'bold', textAlign: 'center'}}>Chỉ Admin mới có quyền lưu đáp án.</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function TongHopTab({ currentUser }) {
  const hskTabs = ['HSK1', 'HSK2', 'HSK3', 'HSK4', 'HSK5', 'HSK6'];
  const colMap = {
    '9000': '9000',
    'HSK1': 'HSK1', 'HSK2': 'HSK2', 'HSK3': 'HSK3', 'HSK4': 'HSK4', 'HSK5': 'HSK5', 'HSK6': 'HSK6',
    'Chữ Nho': 'ChuNhoTongHop_STT (Giáo trình Chữ Nho)',
    'Chỉ Âm': 'Group',
    'Components': 'group2',
    'Characters': 'Số thứ tự words'
  };
  const [activeTab, setActiveTab] = useState('Tìm Kiếm');
  const [searchTerm, setSearchTerm] = useState('');
  const [targetCharToScroll, setTargetCharToScroll] = useState('');
  const [renderTrigger, setRenderTrigger] = useState(0);
  const [showHskMenu, setShowHskMenu] = useState(false);
  
  const filteredData = useMemo(() => {
    if (activeTab === 'Tìm Kiếm') {
        if (!searchTerm.trim()) return [];
        const term = searchTerm.toLowerCase();
        return researchDataObj.filter(item => {
           return (item['Chữ Trung Quốc'] && item['Chữ Trung Quốc'].includes(term)) ||
                  (item['Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)'] && item['Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)'].toLowerCase().includes(term)) ||
                  (item['Âm Hán Việt (Master 100%)'] && item['Âm Hán Việt (Master 100%)'].toLowerCase().includes(term)) ||
                  (item['Nghĩa Tiếng Việt (Master 100%)'] && item['Nghĩa Tiếng Việt (Master 100%)'].toLowerCase().includes(term));
        }).slice(0, 100);
    }
    const col = colMap[activeTab];
    return researchDataObj.filter(item => {
      const val = item[col];
      return val !== undefined && val !== '' && val !== 'nan' && val !== null;
    }).sort((a, b) => {
      if (activeTab === 'Chỉ Âm') {
        const strA = a[col] || '';
        const strB = b[col] || '';
        return strA.localeCompare(strB);
      }
      const vA = parseFloat(a[col]);
      const vB = parseFloat(b[col]);
      return (isNaN(vA) ? 0 : vA) - (isNaN(vB) ? 0 : vB);
    });
  }, [activeTab, searchTerm, renderTrigger]);

  useEffect(() => {
     if (targetCharToScroll) {
        setTimeout(() => {
           const el = document.getElementById(`tonghop-item-${targetCharToScroll}`);
           if (el) {
              el.scrollIntoView({ behavior: 'smooth', block: 'center' });
           }
        }, 100);
     }
  }, [activeTab, targetCharToScroll, filteredData]);

  const handleAddToPractice = async (charObj) => {
    const char = charObj['Chữ Trung Quốc'];
    if (charObj.srs) {
      alert('Chữ này đã có trong danh sách Luyện tập!');
      return;
    }
    const newSrs = buildNewSrs(charObj, null, null, null); // Builds default structure
    
    // Optimistic UI Update
    charObj.srs = newSrs; 
    setRenderTrigger(v => v + 1);

    try {
      const res = await fetch('/api/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: currentUser,
          char: char,
          comps: { srs: newSrs }
        })
      });
      const data = await res.json();
      if (!data.success) {
        charObj.srs = null; // Revert
        setRenderTrigger(v => v + 1);
        alert('Lỗi lưu: ' + data.error);
      }
    } catch (err) {
      charObj.srs = null; // Revert
      setRenderTrigger(v => v + 1);
      alert('Lỗi kết nối: ' + err.message);
    }
  };

  const renderSrsIcon = (srs, item) => {
    if (!srs) return null;
    const status = getSrsStatus(item, 'chiettu');
    switch(status) {
      case 'bat_dau': return <span title="Bắt đầu">🆕</span>;
      case 'san_sang_thi': return <span title="Sẵn sàng thi">🎯</span>;
      case 'hat_mam': return <span title="Hạt mầm">🌱</span>;
      case 'cay': return <span title="Cây">🌳</span>;
      case 'hoa': return <span title="Hoa">🌸</span>;
      default: return null;
    }
  };

  return (
    <div className="tonghop-tab">
      <div className="tab-navigation">
         <button className={`tab-btn ${activeTab === 'Tìm Kiếm' ? 'active' : ''}`} onClick={() => setActiveTab('Tìm Kiếm')}>Tìm Kiếm</button>
         <button className={`tab-btn ${activeTab === '9000' ? 'active' : ''}`} onClick={() => setActiveTab('9000')}>9000</button>
         
         <div className="tab-dropdown" onMouseEnter={() => setShowHskMenu(true)} onMouseLeave={() => setShowHskMenu(false)} style={{position: 'relative'}}>
           <button className={`tab-btn ${activeTab.startsWith('HSK') ? 'active' : ''}`}>
             {activeTab.startsWith('HSK') ? activeTab : 'HSK'} ▾
           </button>
           {showHskMenu && (
             <div className="dropdown-menu" style={{position: 'absolute', top: '100%', left: 0, backgroundColor: 'white', border: '1px solid #e2e8f0', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)', zIndex: 100, minWidth: '100px', padding: '5px 0'}}>
               {hskTabs.map(hsk => (
                 <div key={hsk} className="dropdown-item" onClick={() => { setActiveTab(hsk); setShowHskMenu(false); }} style={{padding: '10px 20px', cursor: 'pointer', color: '#334155'}}>
                   {hsk}
                 </div>
               ))}
             </div>
           )}
         </div>

         <button className={`tab-btn ${activeTab === 'Chữ Nho' ? 'active' : ''}`} onClick={() => setActiveTab('Chữ Nho')}>Chữ Nho</button>
         <button className={`tab-btn ${activeTab === 'Chỉ Âm' ? 'active' : ''}`} onClick={() => setActiveTab('Chỉ Âm')}>Chỉ Âm</button>
         <button className={`tab-btn ${activeTab === 'Components' ? 'active' : ''}`} onClick={() => setActiveTab('Components')}>Components</button>
         <button className={`tab-btn ${activeTab === 'Characters' ? 'active' : ''}`} onClick={() => setActiveTab('Characters')}>Characters</button>
      </div>
      <div className="tonghop-list">
        {activeTab === 'Tìm Kiếm' && (
           <div style={{marginBottom: '20px', textAlign: 'center'}}>
              <input 
                 type="text" 
                 className="search-input" 
                 placeholder="Tìm chữ Hán, pinyin, âm Hán Việt, nghĩa..." 
                 value={searchTerm} 
                 onChange={e => setSearchTerm(e.target.value)} 
                 style={{padding: '10px', width: '80%', fontSize: '1.1rem', borderRadius: '5px', border: '1px solid #ccc'}}
              />
              <p style={{fontSize: '0.9rem', color: '#666', marginTop: '10px'}}>
                  Tìm kiếm và bấm "Ghim" ở chữ bạn muốn, sau đó chuyển sang tab khác để tự động nhảy đến vị trí chữ đó.
              </p>
           </div>
        )}
        {filteredData.map((item, idx) => (
          <div 
             key={idx} 
             id={`tonghop-item-${item['Chữ Trung Quốc']}`} 
             className={`tonghop-item ${targetCharToScroll === item['Chữ Trung Quốc'] ? 'highlighted-item' : ''}`}
          >
             <div className="tonghop-index">{idx + 1}</div>
             <div className="tonghop-char">{item['Chữ Trung Quốc']}</div>
             <div className="tonghop-info">
                <span className="pinyin">{item['Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)']}</span>
                <span className="meaning">{item['Nghĩa Tiếng Việt (Master 100%)']}</span>
                {(activeTab === 'Chỉ Âm' || activeTab === '214 Bộ Thủ' || activeTab === 'Từ Ghép') && (
                    <span style={{color: '#8b5cf6', fontSize: '0.85rem', marginTop: '4px'}}>
                        Nhóm / Giá trị: {item[colMap[activeTab]]}
                    </span>
                )}
             </div>
             <div className="tonghop-actions">
                {targetCharToScroll === item['Chữ Trung Quốc'] ? (
                    <button className="study-btn" style={{marginRight: '10px', background: '#10b981'}} onClick={() => setTargetCharToScroll('')}>📌 Bỏ ghim</button>
                ) : (
                    <button className="study-btn" style={{marginRight: '10px', background: '#64748b'}} onClick={() => setTargetCharToScroll(item['Chữ Trung Quốc'])}>Ghim</button>
                )}
                {renderSrsIcon(item.srs, item)}
                {!item.srs && (
                  <button className="add-btn" onClick={() => handleAddToPractice(item)} title="Thêm vào Luyện tập">+</button>
                )}
             </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function LuyenTapTab({ setPrimaryTab, setActiveTab, setGlobalLookupTerm, currentUser }) {
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
         // Ch? ??y nh?ng k? n?ng ?ang ? m?c bat_dau l?n san_sang_thi. Kh?ng reset c?c k? n?ng ?? c? ti?n ??.
         const currentStatus = getSrsStatus(charObj, skill.id);
         if (currentStatus === 'bat_dau' || !currentStatus) {
            newSrs = buildNewSrs({srs: newSrs}, skill.id, 'san_sang_thi', 0);
         }
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
                      {SKILLS.some(skill => getSrsStatus(item, skill.id) === 'bat_dau') && (
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

export default App
