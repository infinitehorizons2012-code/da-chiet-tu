import re

with open('src/TracNghiemTab.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add audioRef
old_state = """  const [mcq, setMcq] = useState(null);
  const [selectedOption, setSelectedOption] = useState(null);
  const [sessionFinished, setSessionFinished] = useState(false);"""
new_state = """  const [mcq, setMcq] = useState(null);
  const [selectedOption, setSelectedOption] = useState(null);
  const [sessionFinished, setSessionFinished] = useState(false);
  const audioRef = React.useRef(null);"""
if 'audioRef' not in content:
    content = content.replace(old_state, new_state)

# 2. Add Audio play logic when question loads for pinyin_han, and when correct answer is clicked for han_pinyin
# In loadNextCharacter, if pinyin_han, play audio
# Actually it's better to do it in useEffect listening to currentChar
old_effect = """  const saveAndExit = async () => {"""
new_effect = """  useEffect(() => {
     if (currentChar && session && session.mode === 'pinyin_han' && !isRevealed) {
         const audioUrl = currentChar['Link Am Thanh Pinyin (Cloudinary MP3)'];
         if (audioUrl && audioUrl.startsWith('http')) {
             if (audioRef.current) {
                 audioRef.current.src = audioUrl;
                 audioRef.current.play().catch(e => console.log('Audio autoplay blocked', e));
             }
         }
     }
  }, [currentChar, session?.mode, isRevealed]);

  const playAudio = (url) => {
      if (url && url.startsWith('http') && audioRef.current) {
          audioRef.current.src = url;
          audioRef.current.play().catch(e => console.log('Audio play blocked', e));
      }
  };

  const saveAndExit = async () => {"""
if 'audioRef.current.src' not in content:
    content = content.replace(old_effect, new_effect)

# 3. Play audio on correct answer for han_pinyin
old_mcq = """        if (isCorrect) {
            setFeedback({ type: 'success', message: 'Chính xác! 🎉' });
            setSession(prev => ({ ...prev, results: { ...prev.results, [char]: true } }));
        } else {
            setFeedback({ type: 'error', message: `Sai rồi. Đáp án đúng là: ${mcq.correctAnswer}` });
            setSession(prev => ({ ...prev, results: { ...prev.results, [char]: false } }));
        }"""
new_mcq = """        if (isCorrect) {
            setFeedback({ type: 'success', message: 'Chính xác! 🎉' });
            setSession(prev => ({ ...prev, results: { ...prev.results, [char]: true } }));
            if (session.mode === 'han_pinyin') {
                playAudio(currentChar['Link Am Thanh Pinyin (Cloudinary MP3)']);
            }
        } else {
            setFeedback({ type: 'error', message: `Sai rồi. Đáp án đúng là: ${mcq.correctAnswer}` });
            setSession(prev => ({ ...prev, results: { ...prev.results, [char]: false } }));
            if (session.mode === 'han_pinyin') {
                playAudio(currentChar['Link Am Thanh Pinyin (Cloudinary MP3)']);
            }
        }"""
if "playAudio(currentChar['Link Am Thanh Pinyin" not in content:
    content = content.replace(old_mcq, new_mcq)

# 4. Add <audio> element to JSX
old_jsx = """      <div className="tracnghiem-tab" style={{ padding: '20px', maxWidth: '900px', margin: '0 auto' }}>"""
new_jsx = """      <div className="tracnghiem-tab" style={{ padding: '20px', maxWidth: '900px', margin: '0 auto' }}>
        <audio ref={audioRef} style={{ display: 'none' }} />"""
if "<audio ref={audioRef}" not in content:
    content = content.replace(old_jsx, new_jsx)

# 5. Add a small audio button next to question text if it's pinyin_han
old_qtext = """                    <h2 style={{ fontSize: '2rem', marginBottom: '30px' }}>{mcq.questionText}</h2>"""
new_qtext = """                    <h2 style={{ fontSize: '2rem', marginBottom: '30px' }}>
                        {mcq.questionText}
                        {session.mode === 'pinyin_han' && currentChar['Link Am Thanh Pinyin (Cloudinary MP3)'] && (
                            <button onClick={() => playAudio(currentChar['Link Am Thanh Pinyin (Cloudinary MP3)'])} style={{ marginLeft: '15px', fontSize: '1.5rem', background: 'none', border: 'none', cursor: 'pointer' }}>🔊</button>
                        )}
                    </h2>"""
if "🔊" not in content:
    content = content.replace(old_qtext, new_qtext)

with open('src/TracNghiemTab.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Audio feature added!")
