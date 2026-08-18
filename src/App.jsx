import { useState, useEffect, useRef, useMemo } from 'react'
import HanziWriter from 'hanzi-writer'
import './index.css'

import researchDataObj from './data/research_data.json'

const mockDatabase = {
  '妈': {
    char: '妈',
    pinyin: 'mā',
    hanviet: 'MA',
    meaning: 'Mẹ (Mother)',
    mnemonic: 'Người phụ nữ (Nữ) làm lụng như ngựa (Mã) là mẹ.',
    components: [
      { type: 'Radical', char: '女', pinyin: 'nǚ', hanviet: 'NỮ', keyword: 'phụ nữ', color: '#2563eb', strokes: [0, 1, 2], imageUrl: '' },
      { type: 'Phonetic', char: '马', pinyin: 'mǎ', hanviet: 'MÃ', keyword: 'ngựa', color: '#e11d48', strokes: [3, 4, 5], imageUrl: '' }
    ]
  },
  '明': {
    char: '明',
    pinyin: 'míng',
    hanviet: 'MINH',
    meaning: 'Sáng sủa, rõ ràng',
    mnemonic: 'Mặt trời (Nhật) và mặt trăng (Nguyệt) cùng chiếu sáng.',
    components: [
      { type: 'Radical', char: '日', pinyin: 'rì', hanviet: 'NHẬT', keyword: 'mặt trời', color: '#2563eb', strokes: [0, 1, 2, 3], imageUrl: '' },
      { type: 'Component', char: '月', pinyin: 'yuè', hanviet: 'NGUYỆT', keyword: 'mặt trăng', color: '#e11d48', strokes: [4, 5, 6, 7], imageUrl: '' }
    ]
  },
  '南': {
    char: '南',
    pinyin: 'nán',
    hanviet: 'NAM',
    meaning: 'hướng Nam',
    mnemonic: '10 vùng biên giới nuôi dê ở hướng Nam',
    components: [
      { type: 'Radical', char: '十', pinyin: 'shí', hanviet: 'THẬP', keyword: '10', color: '#2563eb', strokes: [0, 1], imageUrl: '' },
      { type: 'Component', char: '冂', pinyin: 'jiōng', hanviet: 'QUYNH', keyword: 'biên giới', color: '#e11d48', strokes: [2, 3], imageUrl: '' },
      { type: 'Component', char: '𢆉', pinyin: 'yáng', hanviet: 'Dê cụt đuôi', keyword: 'dê', color: '#059669', strokes: [4, 5, 6, 7, 8], imageUrl: '' }
    ]
  },
  '茶': {
    char: '茶',
    pinyin: 'chá',
    hanviet: 'TRÀ',
    meaning: 'trà, chè',
    mnemonic: 'Con người (Nhân) nhặt lá cỏ (Thảo) mọc trên cây (Mộc) để làm trà.',
    components: [
      { type: 'Radical', char: '艹', pinyin: 'cǎo', hanviet: 'THẢO', keyword: 'cỏ', color: '#2563eb', strokes: [0, 1, 2], imageUrl: '' },
      { type: 'Component', char: '人', pinyin: 'rén', hanviet: 'NHÂN', keyword: 'con người', color: '#e11d48', strokes: [3, 4], imageUrl: '' },
      { type: 'Component', char: '木', pinyin: 'mù', hanviet: 'MỘC', keyword: 'cây', color: '#059669', strokes: [5, 6, 7, 8], imageUrl: '' }
    ]
  },
  '德': {
    char: '德',
    pinyin: 'dé',
    hanviet: 'ĐỨC',
    meaning: 'Đạo đức, ân đức',
    mnemonic: 'Hành động (彳) quang minh, dù mười (十) con mắt (罒/目) soi xét vẫn giữ một (一) tấm lòng (心) ngay thẳng (Thập Mục Nhất Tâm).',
    components: [
      { type: 'Radical', char: '彳', pinyin: 'chì', hanviet: 'XÍCH', keyword: 'hành động', color: '#3b82f6', strokes: [0, 1, 2], imageUrl: '' },
      { type: 'Component', char: '十', pinyin: 'shí', hanviet: 'THẬP', keyword: 'mười', color: '#10b981', strokes: [3, 4], imageUrl: '' },
      { type: 'Component', char: '罒', pinyin: 'mù', hanviet: 'MỤC (Mắt)', keyword: 'con mắt', color: '#eab308', strokes: [5, 6, 7, 8, 9], imageUrl: '' },
      { type: 'Component', char: '一', pinyin: 'yī', hanviet: 'NHẤT', keyword: 'một', color: '#a855f7', strokes: [10], imageUrl: '' },
      { type: 'Component', char: '心', pinyin: 'xīn', hanviet: 'TÂM', keyword: 'tấm lòng', color: '#ef4444', strokes: [11, 12, 13, 14], imageUrl: '' }
    ]
  }
}

function Header() {
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
        <button className="nav-item active">
          <span className="nav-icon">🔍</span> Tra cứu
        </button>
        <button className="nav-item">
          <span className="nav-icon">📚</span> Tổng hợp
        </button>
        <button className="nav-item">
          <span className="nav-icon">📝</span> Luyện tập
        </button>
        <button className="nav-item">
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

function LookupTab() {
  const [searchTerm, setSearchTerm] = useState('')
  const [result, setResult] = useState(mockDatabase['南'])
  const [error, setError] = useState('')

  const handleSearch = async (e) => {
    if (e) e.preventDefault()
    const char = searchTerm.trim()
    if (!char) return
    
    const researchData = researchDataObj.find(item => item['Chữ Trung Quốc'] === char);

    if (researchData) {
      const newResult = {
        char: researchData['Chữ Trung Quốc'],
        pinyin: researchData['Pinyin_Xie'] || '',
        hanviet: researchData['Âm Hán Việt_Xie'] || '',
        meaning: researchData['Nghĩa Tiếng Việt_Xie'] || '',
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

      // Dynamically fetch stroke counts to color the character
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

    } else if (mockDatabase[char]) {
      setResult(mockDatabase[char])
      setError('')
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

function ResearchTab() {
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

  const handleSidebarSelect = (charObj) => {
    setHistory([]);
    setSelectedChar(charObj);
  };

  const handleSelectChar = (charObj) => {
    if (selectedChar) {
      setHistory(prev => [...prev, selectedChar]);
    }
    setSelectedChar(charObj);
  };

  const handleBack = () => {
    if (history.length > 0) {
      const prev = history[history.length - 1];
      setHistory(prevHistory => prevHistory.slice(0, -1));
      setSelectedChar(prev);
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
             (item['Pinyin_Xie'] && item['Pinyin_Xie'].toLowerCase().includes(lower)) ||
             (item['Âm Hán Việt_Xie'] && item['Âm Hán Việt_Xie'].toLowerCase().includes(lower))
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

  const DETAIL_TABS = ['Ứng dụng', 'Cơ bản', 'Mở rộng', 'Tham khảo'];
  const getTabForKey = (key) => {
    if (key.startsWith('App_')) return 'Ứng dụng';
    if (key.includes('Nghĩa Tiếng Việt') || key.includes('Hán Việt_') || key.includes('Bộ thủ') || key.includes('Tự nguyên')) return 'Cơ bản';
    if (key.includes('Cách dùng') || key.includes('Tần Suất') || key === '9000') return 'Mở rộng';
    return 'Tham khảo';
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
               <span className="research-list-pinyin">{item['Pinyin_Xie'] || ''}</span>
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
                <div className="detail-pinyin">{selectedChar['Pinyin_Xie']} - {selectedChar['Âm Hán Việt_Xie']}</div>
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
                 if (key === 'Chữ Trung Quốc' || key === 'Pinyin_Xie' || key === 'Âm Hán Việt_Xie') return null;
                 
                 // Lọc theo tab hiện tại
                 if (getTabForKey(key) !== detailTab) return null;

                 const isEditable = isFieldEditable(key);
                 const val = isEditable && editData[key] !== undefined ? editData[key] : selectedChar[key];
                 if (!isEditable && (!val || val === 'nan')) return null;
                 
                 return (
                   <div key={idx} className="detail-card">
                     <div className="detail-card-title">{key.toUpperCase()}</div>
                     {isEditable ? (
                       <textarea 
                         className="detail-card-textarea"
                         value={val === 'nan' ? '' : val}
                         onChange={(e) => handleEditChange(key, e.target.value)}
                         placeholder="Nhập nội dung..."
                       />
                     ) : (
                       <div className="detail-card-value">{renderClickableValue(val)}</div>
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
  const [activeTab, setActiveTab] = useState('lookup');
  const [dataReady, setDataReady] = useState(false);

  useEffect(() => {
    // Fetch user edits from Cloudflare D1 Database
    fetch('/api/updates')
      .then(res => res.json())
      .then(data => {
        if (data.success && data.updates) {
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
        console.error("Failed to load D1 updates:", err);
        setDataReady(true); // Vẫn cho phép chạy dùng data gốc
      });
  }, []);

  if (!dataReady) {
    return <div style={{textAlign: 'center', marginTop: '50px'}}>Đang đồng bộ dữ liệu từ Cloudflare...</div>;
  }

  return (
    <div className="app-container">
      <Header />
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
      </div>
      
      {activeTab === 'lookup' ? <LookupTab /> : <ResearchTab />}
    </div>
  )
}

export default App
