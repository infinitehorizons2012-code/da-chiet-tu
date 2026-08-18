import { useState, useEffect, useRef, useMemo } from 'react'
import HanziWriter from 'hanzi-writer'
import './index.css'

let researchDataObj = [];



function Header({ primaryTab, setPrimaryTab }) {
  return (
    <header className="app-header">
      <div className="header-left">
        <div className="logo-icon">字</div>
        <div className="logo-text">
          <span className="title">Bản đồ Chiết tự</span>
          <span className="subtitle">HỆ THỐNG PHÂN TÍCH CHỮ HÁN</span>
        </div>
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
          <span className="username">hang</span>
          <span className="user-xp">⚡ 90 XP</span>
        </div>
        <button className="icon-button">🚪</button>
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
            <div className="info-pinyin">{result.pinyin}</div>
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

  const handleSave = async () => {
    setIsSaving(true);
    setSaveStatus('Đang lưu...');
    try {
      const res = await fetch('/api/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
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
                <div className="detail-pinyin">{selectedChar['Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)']} - {selectedChar['Âm Hán Việt (Master 100%)']}</div>
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

function App() {
  const [primaryTab, setPrimaryTab] = useState('tracuu');
  const [activeTab, setActiveTab] = useState('lookup');
  const [dataReady, setDataReady] = useState(false);
  const [globalLookupTerm, setGlobalLookupTerm] = useState('');

  useEffect(() => {
    // 1. Fetch static base data
    Promise.all([
      fetch('/data/research_data_1.json').then(res => res.json()),
      fetch('/data/research_data_2.json').then(res => res.json())
    ])
      .then(([part1, part2]) => {
        researchDataObj.push(...part1, ...part2); // Populate global array
        
        // 2. Fetch user edits from Cloudflare D1 Database
        return fetch('/api/updates');
      })
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
        console.error("Failed to load data:", err);
        setDataReady(true); // Vẫn cho phép chạy dùng data gốc
      });
  }, []);

  if (!dataReady) {
    return <div style={{textAlign: 'center', marginTop: '50px'}}>Đang đồng bộ dữ liệu từ Cloudflare...</div>;
  }

  return (
    <div className="app-container">
      <Header primaryTab={primaryTab} setPrimaryTab={setPrimaryTab} />
      
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
          {activeTab === 'chiettu' && <ChietTuAdminTab globalLookupTerm={globalLookupTerm} setGlobalLookupTerm={setGlobalLookupTerm} />}
        </>
      )}

      {primaryTab === 'tonghop' && <TongHopTab />}
      
      {primaryTab === 'luyentap' && <LuyenTapTab setPrimaryTab={setPrimaryTab} setActiveTab={setActiveTab} setGlobalLookupTerm={setGlobalLookupTerm} />}
      
      {primaryTab === 'tracnghiem' && <TracNghiemTab />}
      
    </div>
  )
}

function ChietTuAdminTab({ globalLookupTerm, setGlobalLookupTerm }) {
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
            
            <button 
              className="save-btn" 
              onClick={handleSave} 
              disabled={saving}
            >
              {saving ? 'Đang lưu...' : 'Lưu Đáp Án'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

function TongHopTab() {
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
    const newSrs = { status: 'bat_dau', streak: 0 };
    
    // Optimistic UI Update
    charObj.srs = newSrs; 
    setRenderTrigger(v => v + 1);

    try {
      const res = await fetch('/api/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
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

  const renderSrsIcon = (srs) => {
    if (!srs) return null;
    switch(srs.status) {
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
                {renderSrsIcon(item.srs)}
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

function LuyenTapTab({ setPrimaryTab, setActiveTab, setGlobalLookupTerm }) {
  const tabs = [
    { id: 'bat_dau', label: '🆕 Bắt đầu' },
    { id: 'san_sang_thi', label: '🎯 Sẵn sàng thi' },
    { id: 'hat_mam', label: '🌱 Hạt mầm' },
    { id: 'cay', label: '🌳 Cây' },
    { id: 'hoa', label: '🌸 Hoa' }
  ];
  const [activeTab, setLocalActiveTab] = useState('bat_dau');
  const [renderTrigger, setRenderTrigger] = useState(0);

  const filteredData = useMemo(() => {
    return researchDataObj.filter(item => item.srs && item.srs.status === activeTab);
  }, [activeTab, renderTrigger]);

  const handleStudy = (char) => {
    setGlobalLookupTerm(char);
    setActiveTab('lookup');
    setPrimaryTab('tracuu');
  };

  const handleMoveToReady = async (charObj) => {
    const originalSrs = { ...charObj.srs };
    const newSrs = { ...charObj.srs, status: 'san_sang_thi' };
    
    // Optimistic UI Update
    charObj.srs = newSrs;
    setRenderTrigger(v => v + 1);

    try {
      const res = await fetch('/api/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
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

  return (
    <div className="luyentap-tab">
      <div className="tab-navigation">
        {tabs.map(tab => (
           <button key={tab.id} className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`} onClick={() => setLocalActiveTab(tab.id)}>
             {tab.label}
           </button>
        ))}
      </div>
      <div className="tonghop-list">
        {filteredData.map((item, idx) => (
          <div key={idx} className="tonghop-item">
             <div className="tonghop-index">{idx + 1}</div>
             <div className="tonghop-char">{item['Chữ Trung Quốc']}</div>
             <div className="tonghop-info">
                <span className="pinyin">{item['Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)']}</span>
                <span className="meaning">{item['Nghĩa Tiếng Việt (Master 100%)']}</span>
             </div>
             <div className="tonghop-actions">
                <button className="study-btn" onClick={() => handleStudy(item['Chữ Trung Quốc'])}>Học</button>
                {activeTab === 'bat_dau' && (
                  <button className="ready-btn" onClick={() => handleMoveToReady(item)}>Xong</button>
                )}
             </div>
          </div>
        ))}
        {filteredData.length === 0 && <div className="empty-msg">Chưa có chữ nào ở mục này.</div>}
      </div>
    </div>
  );
}

function TracNghiemTab() {
  const [dueChars, setDueChars] = useState([]);
  const [currentChar, setCurrentChar] = useState(null);
  const [strokePaths, setStrokePaths] = useState([]);
  const [strokeColors, setStrokeColors] = useState({});
  const [activeComp, setActiveComp] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(false);

  const [isRevealed, setIsRevealed] = useState(false);

  useEffect(() => {
     const eligible = researchDataObj.filter(item => {
        const status = item.srs?.status;
        return status && status !== 'bat_dau';
     });
     eligible.sort(() => Math.random() - 0.5); 
     setDueChars(eligible);
  }, []);

  useEffect(() => {
     if (dueChars.length > 0 && !currentChar) {
         loadNextCharacter(dueChars[0]);
     }
  }, [dueChars, currentChar]);

  const loadNextCharacter = async (charObj) => {
    setLoading(true);
    setFeedback(null);
    setStrokeColors({});
    setActiveComp(null);
    setIsRevealed(false);
    const char = charObj['Chữ Trung Quốc'];
    
    const comps = [];
    const COLORS = [
      '#e11d48', '#2563eb', '#059669', '#eab308', 
      '#a855f7', '#10b981', '#f97316', '#14b8a6', 
      '#6366f1', '#ec4899', '#8b5cf6', '#0ea5e9'
    ];
    let compIndex = 0;
    for (let i = 1; i <= 12; i++) {
      const compStr = charObj[`App_Comp_${i}`];
      if (compStr && compStr !== 'nan' && compStr.trim() !== '') {
        comps.push({
          id: `App_Comp_${i}`,
          text: compStr.trim(),
          color: COLORS[compIndex % COLORS.length]
        });
        compIndex++;
      }
    }
    
    charObj.parsedComps = comps;
    if (comps.length > 0) setActiveComp(comps[0]);
    setCurrentChar(charObj);

    try {
      const res = await fetch(`https://cdn.jsdelivr.net/npm/hanzi-writer-data@2.0/${char}.json`);
      if (res.ok) {
        const data = await res.json();
        setStrokePaths(data.strokes);
      } else {
        setStrokePaths([]);
        setFeedback({ type: 'error', message: `Không tìm thấy nét vẽ cho chữ ${char}`});
      }
    } catch (err) {
      setStrokePaths([]);
    } finally {
      setLoading(false);
    }
  };

  const handleStrokeClick = (strokeIndex) => {
    // Không cho phép tương tác tô màu thủ công nữa theo yêu cầu flashcard
  };

  const updateSrs = async (isCorrect) => {
     if (!currentChar) return;
     let srs = { ...currentChar.srs };
     
     if (isCorrect) {
        if (srs.status === 'san_sang_thi') {
           srs.status = 'hat_mam'; srs.streak = 1;
        } else if (srs.status === 'hat_mam') {
           srs.streak = (srs.streak || 1) + 1;
           if (srs.streak >= 2) srs.status = 'cay';
        } else if (srs.status === 'cay') {
           srs.streak = (srs.streak || 2) + 1;
           if (srs.streak >= 3) srs.status = 'hoa';
        } else if (srs.status === 'hoa') {
           srs.streak = (srs.streak || 3) + 1;
        }
     } else {
        if (srs.status === 'hoa') srs.status = 'cay';
        else if (srs.status === 'cay') srs.status = 'hat_mam';
        else if (srs.status === 'hat_mam') srs.status = 'san_sang_thi';
        srs.streak = 0;
     }

     try {
       await fetch('/api/save', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ char: currentChar['Chữ Trung Quốc'], comps: { srs } })
       });
       currentChar.srs = srs;
     } catch(e) {}
     
     nextChar();
  };

  const checkAnswer = () => {
    if (!currentChar) return;
    const mapping = currentChar.quiz_mapping;
    if (!mapping) {
       setFeedback({ type: 'error', message: 'Chữ này chưa có đáp án trên hệ thống! Vui lòng nhờ admin tạo đáp án trước.'});
       setIsRevealed(true);
       return;
    }

    // Tự động tô màu đáp án
    const correctColors = {};
    for (const compId in mapping) {
       const comp = currentChar.parsedComps.find(c => c.id === compId);
       if (comp) {
          mapping[compId].forEach(idx => {
             correctColors[idx] = comp.color;
          });
       }
    }
    setStrokeColors(correctColors);
    setIsRevealed(true);
  };

  const nextChar = () => {
     setDueChars(prev => {
        const nextQ = prev.slice(1);
        if (nextQ.length > 0) loadNextCharacter(nextQ[0]);
        else setCurrentChar(null);
        return nextQ;
     });
  };

  if (dueChars.length === 0) {
     return <div className="empty-msg" style={{textAlign: 'center', padding: '50px', fontSize: '1.2rem', color: '#64748b'}}>Bạn đã hoàn thành tất cả chữ Hán cần ôn tập hôm nay!</div>;
  }

  if (!currentChar || loading) {
     return <div style={{textAlign: 'center', padding: '50px'}}>Đang tải bài tập...</div>;
  }

  const srsIcons = { 'san_sang_thi': '🎯 Sẵn sàng thi', 'hat_mam': '🌱 Hạt mầm', 'cay': '🌳 Cây', 'hoa': '🌸 Hoa' };

  return (
    <div className="tracnghiem-tab" style={{padding: '20px', maxWidth: '900px', margin: '0 auto'}}>
      <div className="tracnghiem-header" style={{textAlign: 'center', marginBottom: '20px'}}>
         <h2 style={{color: '#1e293b'}}>Trắc nghiệm: Phân tách nét chữ tương ứng linh kiện</h2>
         <div className="srs-badge" style={{display: 'inline-block', background: '#e0f2fe', color: '#0284c7', padding: '5px 15px', borderRadius: '20px', fontWeight: 'bold', marginTop: '10px'}}>
            Cấp bậc hiện tại: {srsIcons[currentChar.srs?.status] || 'Không xác định'}
         </div>
      </div>
      <div className="chiettu-workspace">
        <div className="chiettu-svg-container">
          <svg viewBox="0 0 1024 1024" className="hanzi-svg">
            <g transform="scale(1, -1) translate(0, -900)">
              {strokePaths.map((path, idx) => (
                <path 
                  key={idx} 
                  d={path} 
                  className="hanzi-stroke-path"
                  fill={strokeColors[idx] || '#cbd5e1'} 
                />
              ))}
            </g>
          </svg>
          {feedback && (
             <div className={`feedback-box ${feedback.type}`} style={{marginTop: '20px', padding: '15px', borderRadius: '8px', fontWeight: 'bold', background: feedback.type === 'success' ? '#dcfce7' : '#fee2e2', color: feedback.type === 'success' ? '#166534' : '#991b1b'}}>
                {feedback.message}
             </div>
          )}
        </div>
        
        <div className="chiettu-components-panel" style={{display: 'flex', flexDirection: 'column', justifyContent: 'center'}}>
          {!isRevealed ? (
             <div style={{textAlign: 'center'}}>
               <h3 style={{marginBottom: '20px', color: '#64748b'}}>Hãy tự ghi ra nháp các linh kiện của chữ này</h3>
               <button className="save-btn" onClick={checkAnswer} style={{background: '#3b82f6', fontSize: '1.2rem', padding: '15px 30px', width: '100%'}}>Kiểm tra đối chiếu</button>
             </div>
          ) : (
             <>
               <h3>Đáp án: Các linh kiện ({currentChar['Chữ Trung Quốc']})</h3>
               <div className="comp-list">
                 {currentChar.parsedComps.map(comp => (
                   <div 
                     key={comp.id}
                     className="comp-item"
                     style={{ borderLeftColor: comp.color }}
                   >
                     <div className="comp-color-box" style={{ backgroundColor: comp.color }}></div>
                     <span className="comp-text">{comp.text}</span>
                   </div>
                 ))}
               </div>
               
               {!feedback ? (
                  <div style={{marginTop: '30px'}}>
                     <h4 style={{textAlign: 'center', marginBottom: '15px'}}>Bạn làm đúng chứ?</h4>
                     <div style={{display: 'flex', gap: '15px'}}>
                        <button className="save-btn" onClick={() => updateSrs(false)} style={{background: '#ef4444', flex: 1}}>Sai (Làm lại sau)</button>
                        <button className="save-btn" onClick={() => updateSrs(true)} style={{background: '#10b981', flex: 1}}>Đúng (Lên cấp)</button>
                     </div>
                  </div>
               ) : (
                  <button className="save-btn next-btn" onClick={nextChar} style={{background: '#10b981', marginTop: '20px'}}>Câu Tiếp Theo ➔</button>
               )}
             </>
          )}
        </div>
      </div>
    </div>
  );
}

export default App
