import { useState } from 'react'
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
        meaning: 'Nữ (Phụ nữ). Cho biết chữ này liên quan đến phái nữ.'
      },
      {
        type: 'Phonetic (Thành phần biểu âm)',
        char: '马',
        pinyin: 'mǎ',
        meaning: 'Mã (Con ngựa). Gợi ý cách phát âm là "ma".'
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
        meaning: 'Nhật (Mặt trời).'
      },
      {
        type: 'Component (Thành phần)',
        char: '月',
        pinyin: 'yuè',
        meaning: 'Nguyệt (Mặt trăng). Mặt trời và mặt trăng ở cạnh nhau tạo nên sự sáng sủa.'
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
        meaning: 'Ngôn (Lời nói). Cho biết chữ liên quan đến ngôn ngữ, giao tiếp.'
      },
      {
        type: 'Phonetic (Thành phần biểu âm)',
        char: '吾',
        pinyin: 'wú',
        meaning: 'Ngô (Tôi). Gợi ý âm đọc.'
      }
    ]
  }
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
      setError(`Chưa có dữ liệu cho chữ "${char}". Thử các chữ: 妈, 明, 语.`)
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

      {error && <p style={{color: '#f87171', textAlign: 'center'}}>{error}</p>}

      {result && !error && (
        <div className="glass-panel">
          <div className="char-header">
            <div className="char-large">{result.char}</div>
            <div className="char-info">
              <h2>{result.pinyin}</h2>
              <p>{result.meaning}</p>
            </div>
          </div>
          
          <div className="components-grid">
            {result.components.map((comp, idx) => (
              <div key={idx} className="component-card">
                <h3>{comp.type}</h3>
                <div className="component-detail">
                  <div className="comp-char">{comp.char}</div>
                  <div className="comp-desc">
                    <p className="pinyin">{comp.pinyin}</p>
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
