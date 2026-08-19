import re

with open("src/TracNghiemTab.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old_playAudio = """  const playAudio = (url) => {
      if (url && url.startsWith('http') && audioRef.current) {
          audioRef.current.src = url;
          audioRef.current.play().catch(e => console.log('Audio play blocked', e));
      }
  };"""

new_playAudio = """  const playAudio = (url) => {
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

content = content.replace(old_playAudio, new_playAudio)

old_button = """                        {session.mode === 'pinyin_han' && currentChar['Link Âm Thanh Pinyin (Cloudinary MP3)'] && (
                            <button onClick={() => playAudio(currentChar['Link Âm Thanh Pinyin (Cloudinary MP3)'])} style={{ marginLeft: '15px', fontSize: '1.5rem', background: 'none', border: 'none', cursor: 'pointer' }}>🔊</button>
                        )}"""

new_button = """                        {(session.mode === 'pinyin_han' || session.mode === 'han_pinyin') && currentChar['Link Âm Thanh Pinyin (Cloudinary MP3)'] && (
                            <button onClick={() => playAudio(currentChar['Link Âm Thanh Pinyin (Cloudinary MP3)'])} style={{ marginLeft: '15px', fontSize: '1.5rem', background: 'none', border: 'none', cursor: 'pointer' }}>🔊</button>
                        )}"""

content = content.replace(old_button, new_button)

with open("src/TracNghiemTab.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated playAudio and button!")
