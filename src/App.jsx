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

  const handleSearch = (e) => {
    e.preventDefault()
    const char = searchTerm.trim()
    if (!char) return
    
    if (mockDatabase[char]) {
      setResult(mockDatabase[char])
      setError('')
    } else {
      setError(`Chưa có dữ liệu cho chữ "${char}". Thử các chữ: 妈, 明, 南, 茶, 德.`)
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
  const [selectedChar, setSelectedChar] = useState(null);
  const [history, setHistory] = useState([]);

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
    if (!searchTerm.trim()) return researchDataObj;
    const lower = searchTerm.toLowerCase();
    return researchDataObj.filter(item => {
      return (item['Chữ Trung Quốc'] && item['Chữ Trung Quốc'].includes(lower)) || 
             (item['Pinyin_Xie'] && item['Pinyin_Xie'].toLowerCase().includes(lower)) ||
             (item['Âm Hán Việt_Xie'] && item['Âm Hán Việt_Xie'].toLowerCase().includes(lower))
    });
  }, [searchTerm]);

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
             {history.length > 0 && (
               <button className="back-btn" onClick={handleBack}>
                 ← Quay lại
               </button>
             )}
             <div className="detail-header">
                <div className="detail-header-char">{selectedChar['Chữ Trung Quốc']}</div>
                <div className="detail-pinyin">{selectedChar['Pinyin_Xie']} - {selectedChar['Âm Hán Việt_Xie']}</div>
             </div>
             <div className="detail-grid">
               {Object.keys(selectedChar).map((key, idx) => {
                 if (key === 'Chữ Trung Quốc' || key === 'Pinyin_Xie' || key === 'Âm Hán Việt_Xie') return null;
                 if (!selectedChar[key] || selectedChar[key] === 'nan') return null;
                 return (
                   <div className="detail-card" key={idx}>
                     <div className="detail-card-title">{key}</div>
                     <div className="detail-card-value">{renderClickableValue(selectedChar[key])}</div>
                   </div>
                 )
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
