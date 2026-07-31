import { useState, useEffect, useRef, useMemo } from 'react'
import HanziWriter from 'hanzi-writer'
import './index.css'

const mockDatabase = {
  '妈': {
    char: '妈',
    pinyin: 'mā',
    meaning: 'Mẹ (Mother)',
    components: [
      {
        type: 'Radical (Bộ thủ chỉ nghĩa)',
        char: '女',
        pinyin: 'nǚ',
        meaning: 'Nữ (Phụ nữ). Cho biết chữ này liên quan đến phái nữ.',
        color: '#2563eb', // Blue
        strokes: [0, 1, 2]
      },
      {
        type: 'Phonetic (Thành phần biểu âm)',
        char: '马',
        pinyin: 'mǎ',
        meaning: 'Mã (Con ngựa). Gợi ý cách phát âm là "ma".',
        color: '#e11d48', // Red
        strokes: [3, 4, 5]
      }
    ]
  },
  '明': {
    char: '明',
    pinyin: 'míng',
    meaning: 'Sáng sủa, rõ ràng (Bright, clear)',
    components: [
      {
        type: 'Radical (Bộ thủ)',
        char: '日',
        pinyin: 'rì',
        meaning: 'Nhật (Mặt trời).',
        color: '#2563eb',
        strokes: [0, 1, 2, 3]
      },
      {
        type: 'Component (Thành phần)',
        char: '月',
        pinyin: 'yuè',
        meaning: 'Nguyệt (Mặt trăng). Mặt trời và mặt trăng ở cạnh nhau tạo nên sự sáng sủa.',
        color: '#e11d48',
        strokes: [4, 5, 6, 7]
      }
    ]
  },
  '语': {
    char: '语',
    pinyin: 'yǔ',
    meaning: 'Ngôn ngữ, Lời nói (Language, Words)',
    components: [
      {
        type: 'Radical (Bộ thủ chỉ nghĩa)',
        char: '讠',
        pinyin: 'yán',
        meaning: 'Ngôn (Lời nói). Cho biết chữ liên quan đến ngôn ngữ, giao tiếp.',
        color: '#2563eb',
        strokes: [0, 1]
      },
      {
        type: 'Phonetic (Thành phần biểu âm)',
        char: '吾',
        pinyin: 'wú',
        meaning: 'Ngô (Tôi). Gợi ý âm đọc.',
        color: '#e11d48',
        strokes: [2, 3, 4, 5, 6, 7, 8]
      }
    ]
  },
  '吃': {
    char: '吃',
    pinyin: 'chī',
    meaning: 'Ăn (Eat)',
    components: [
      {
        type: 'Radical (Bộ thủ chỉ nghĩa)',
        char: '口',
        pinyin: 'kǒu',
        meaning: 'Khẩu (Miệng). Chỉ các hành động liên quan đến miệng như ăn, uống.',
        color: '#2563eb',
        strokes: [0, 1, 2]
      },
      {
        type: 'Phonetic (Thành phần biểu âm)',
        char: '乞',
        pinyin: 'qǐ',
        meaning: 'Khất (Ăn xin). Đóng vai trò biểu âm (mặc dù âm hiện đại đã biến đổi).',
        color: '#e11d48',
        strokes: [3, 4, 5]
      }
    ]
  },
  '南': {
    char: '南',
    pinyin: 'nán',
    meaning: 'Hướng Nam (South)',
    components: [
      {
        type: 'Radical (Bộ thủ)',
        char: '十',
        pinyin: 'shí',
        meaning: 'Thập (Số 10). Đóng vai trò bộ thủ chính của chữ.',
        color: '#2563eb', // Blue
        strokes: [0, 1]
      },
      {
        type: 'Component (Thành phần)',
        char: '冂',
        pinyin: 'jiōng',
        meaning: 'Khuynh (Vùng không gian, bao quanh).',
        color: '#e11d48', // Red
        strokes: [2, 3]
      },
      {
        type: 'Component (Thành phần)',
        char: '𢆉',
        pinyin: 'yáng',
        meaning: 'Dạng cổ giống chữ 羊 (Dương - con cừu).',
        color: '#059669', // Green
        strokes: [4, 5, 6, 7, 8]
      }
    ]
  }
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
          // Bôi màu cho path thứ idx+1 bất kể nó nằm ở outline hay nét chính
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
      width: 150,
      height: 150,
      padding: 5,
      strokeColor: '#cbd5e1', 
      radicalColor: null, 
      showOutline: false,
      strokeAnimationSpeed: 1.5,
      delayBetweenStrokes: 150
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

function App() {
  const [searchTerm, setSearchTerm] = useState('')
  const [result, setResult] = useState(mockDatabase['妈'])
  const [error, setError] = useState('')

  const handleSearch = (e) => {
    e.preventDefault()
    const char = searchTerm.trim()
    if (!char) return
    
    if (mockDatabase[char]) {
      setResult(mockDatabase[char])
      setError('')
    } else {
      setError(`Chưa có dữ liệu cho chữ "${char}". Thử các chữ: 妈, 明, 语, 吃, 南.`)
    }
  }

  return (
    <div className="app-container">
      <h1>Học Chiết Tự</h1>
      <p className="subtitle">Khám phá cấu tạo chữ Hán (Radicals & Phonetics)</p>

      <form className="search-container" onSubmit={handleSearch}>
        <input 
          type="text" 
          className="search-input" 
          placeholder="Nhập một chữ Hán (VD: 妈)..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          maxLength={1}
        />
        <button type="submit" className="search-button">Phân tích</button>
      </form>

      {error && <p style={{color: '#e11d48', textAlign: 'center', fontWeight: '500'}}>{error}</p>}

      {result && !error && (
        <div className="glass-panel">
          <div className="char-header">
            {/* Truyền thêm components vào để tô màu từng nét */}
            <HanziDisplay char={result.char} components={result.components} />
            
            <div className="char-info">
              <h2>{result.pinyin}</h2>
              <p>{result.meaning}</p>
            </div>
          </div>
          
          <div className="components-grid">
            {result.components.map((comp, idx) => (
              <div key={idx} className="component-card">
                <h3 style={{ color: comp.color }}>{comp.type}</h3>
                <div className="component-detail">
                  <div className="comp-char" style={{ color: comp.color }}>{comp.char}</div>
                  <div className="comp-desc">
                    <p className="pinyin" style={{ color: comp.color }}>{comp.pinyin}</p>
                    <p>{comp.meaning}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default App
