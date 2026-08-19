import re

with open('src/TracNghiemTab.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add audioUrl to generateMultipleChoice
old_gen = """       return { questionText, options, correctAnswer: answerText };"""
new_gen = """       let audioUrl = null;
       if (mode === 'han_pinyin' || mode === 'pinyin_han') {
           audioUrl = charObj['Link Âm Thanh Pinyin (Cloudinary MP3)'];
       }
       return { questionText, options, correctAnswer: answerText, audioUrl };"""
content = content.replace(old_gen, new_gen)

# 2. Update mcq render to include audio player
old_render = """                  <h3 style={{ fontSize: '1.3rem', color: '#334155', marginBottom: '30px', whiteSpace: 'pre-wrap' }}>{mcq.questionText}</h3>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>"""

new_render = """                  <h3 style={{ fontSize: '1.3rem', color: '#334155', marginBottom: '15px', whiteSpace: 'pre-wrap' }}>{mcq.questionText}</h3>
                    
                    {mcq.audioUrl && mcq.audioUrl.trim() !== '' && mcq.audioUrl !== 'nan' && (
                        <div style={{ marginBottom: '20px' }}>
                            <audio 
                                src={mcq.audioUrl} 
                                controls 
                                autoPlay={isRevealed || session.mode === 'pinyin_han'}
                                key={`${mcq.questionText}-${isRevealed}`}
                            />
                        </div>
                    )}
                    
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>"""
content = content.replace(old_render, new_render)

with open('src/TracNghiemTab.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Added audio player")
