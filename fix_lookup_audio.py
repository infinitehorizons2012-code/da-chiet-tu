import re

with open("src/App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. LookupTab
lookup_tab_regex = re.compile(r"(function LookupTab.*?\{)(.*?)(const handleSearch =)", re.DOTALL)
def add_audio_lookup(m):
    return m.group(1) + m.group(2) + """
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
    """ + m.group(3)

content = lookup_tab_regex.sub(add_audio_lookup, content)

# Modify LookupTab newResult
newResult_old = """        const newResult = {
          char: researchData['Chữ Trung Quốc'],
          pinyin: researchData['Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)'] || '',
          hanviet: researchData['Âm Hán Việt (Master 100%)'] || '',
          meaning: researchData['Nghĩa Tiếng Việt (Master 100%)'] || '',
          mnemonic: researchData['App_Mnemonic'] || '',
          components: []
        };"""
newResult_new = """        const newResult = {
          char: researchData['Chữ Trung Quốc'],
          pinyin: researchData['Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)'] || '',
          hanviet: researchData['Âm Hán Việt (Master 100%)'] || '',
          meaning: researchData['Nghĩa Tiếng Việt (Master 100%)'] || '',
          mnemonic: researchData['App_Mnemonic'] || '',
          audioUrl: researchData['Link Âm Thanh Pinyin (Cloudinary MP3)'] || '',
          components: []
        };"""
content = content.replace(newResult_old, newResult_new)

# Modify LookupTab UI
info_pinyin_old = '<div className="info-pinyin">{result.pinyin}</div>'
info_pinyin_new = """<div className="info-pinyin" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
                {result.pinyin}
                {result.audioUrl && (
                    <span onClick={() => playAudio(result.audioUrl)} style={{ fontSize: '1.2rem', cursor: 'pointer', pointerEvents: 'auto' }}>🔊</span>
                )}
              </div>"""
content = content.replace(info_pinyin_old, info_pinyin_new)


# 2. ResearchTab
research_tab_regex = re.compile(r"(function ResearchTab.*?\{)(.*?)(const handleSave =)", re.DOTALL)
def add_audio_research(m):
    return m.group(1) + m.group(2) + """
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
    """ + m.group(3)

content = research_tab_regex.sub(add_audio_research, content)

# Modify ResearchTab UI
detail_pinyin_old = """                  <div className="detail-pinyin">{selectedChar['Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)']} - {selectedChar['Âm Hán Việt (Master 100%)']}</div>"""
detail_pinyin_new = """                  <div className="detail-pinyin" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
                    {selectedChar['Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)']}
                    {selectedChar['Link Âm Thanh Pinyin (Cloudinary MP3)'] && (
                        <span onClick={() => playAudio(selectedChar['Link Âm Thanh Pinyin (Cloudinary MP3)'])} style={{ fontSize: '1.2rem', cursor: 'pointer', pointerEvents: 'auto' }}>🔊</span>
                    )}
                    - {selectedChar['Âm Hán Việt (Master 100%)']}
                  </div>"""
content = content.replace(detail_pinyin_old, detail_pinyin_new)

with open("src/App.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Injected audio to LookupTab and ResearchTab!")
