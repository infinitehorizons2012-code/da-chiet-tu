import re

with open("src/TracNghiemTab.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update playAudio
old_playAudio = """  const playAudio = (url) => {
      if (url && url.startsWith('http') && audioRef.current) {
          if (audioRef.current.src === url && !audioRef.current.paused) {
              audioRef.current.pause();
              audioRef.current.currentTime = 0;
          } else {
              if (audioRef.current.src !== url) {
                  audioRef.current.src = url;
              } else {
                  audioRef.current.currentTime = 0;
              }
              audioRef.current.play().catch(e => console.log('Audio play blocked', e));
          }
      }
  };"""

new_playAudio = """  const audioInstanceRef = React.useRef(null);
  const playAudio = (url) => {
      if (!url || !url.startsWith('http')) return;
      if (audioInstanceRef.current && audioInstanceRef.current.src === url && !audioInstanceRef.current.paused) {
          audioInstanceRef.current.pause();
          audioInstanceRef.current.currentTime = 0;
      } else {
          if (audioInstanceRef.current && audioInstanceRef.current.src !== url) {
              audioInstanceRef.current.pause();
          }
          if (!audioInstanceRef.current || audioInstanceRef.current.src !== url) {
              audioInstanceRef.current = new Audio(url);
          }
          audioInstanceRef.current.currentTime = 0;
          audioInstanceRef.current.play().catch(e => console.error("Audio block:", e));
      }
  };"""

if old_playAudio in content:
    content = content.replace(old_playAudio, new_playAudio)
else:
    print("Could not replace playAudio")

# 2. Fix the header question text speaker (only show for pinyin_han)
old_h3 = """<h3 style={{ fontSize: '1.3rem', color: '#334155', marginBottom: '30px', whiteSpace: 'pre-wrap' }}>
  {mcq.questionText}
  {(session.mode === 'pinyin_han' || session.mode === 'han_pinyin') && currentChar['Link Âm Thanh Pinyin (Cloudinary MP3)'] && (
      <button onClick={() => playAudio(currentChar['Link Âm Thanh Pinyin (Cloudinary MP3)'])} style={{ marginLeft: '15px', fontSize: '1.5rem', background: 'none', border: 'none', cursor: 'pointer', verticalAlign: 'middle' }}>🔊</button>
  )}
</h3>"""

new_h3 = """<h3 style={{ fontSize: '1.3rem', color: '#334155', marginBottom: '30px', whiteSpace: 'pre-wrap' }}>
  {mcq.questionText}
  {session.mode === 'pinyin_han' && currentChar['Link Âm Thanh Pinyin (Cloudinary MP3)'] && (
      <button onClick={() => playAudio(currentChar['Link Âm Thanh Pinyin (Cloudinary MP3)'])} style={{ marginLeft: '15px', fontSize: '1.5rem', background: 'none', border: 'none', cursor: 'pointer', verticalAlign: 'middle' }}>🔊</button>
  )}
</h3>"""
if old_h3 in content:
    content = content.replace(old_h3, new_h3)
else:
    print("Could not replace h3")

# 3. Add speaker to the correct option if han_pinyin and revealed
old_option = """                        return (
                          <div 
                            key={idx}"""
new_option = """                        return (
                          <div 
                            key={idx}"""

# Wait, let's inject it into the option text
old_option_text = """                              {option}
                            </div>
                          </div>
                        );"""
new_option_text = """                              {option}
                              {session.mode === 'han_pinyin' && isRevealed && option === mcq.correctAnswer && currentChar['Link Âm Thanh Pinyin (Cloudinary MP3)'] && (
                                  <button onClick={(e) => { e.stopPropagation(); playAudio(currentChar['Link Âm Thanh Pinyin (Cloudinary MP3)']); }} style={{ marginLeft: '10px', fontSize: '1.2rem', background: 'none', border: 'none', cursor: 'pointer', verticalAlign: 'middle' }}>🔊</button>
                              )}
                            </div>
                          </div>
                        );"""
if old_option_text in content:
    content = content.replace(old_option_text, new_option_text)
else:
    print("Could not replace option text")

with open("src/TracNghiemTab.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("TracNghiemTab fixes applied")
