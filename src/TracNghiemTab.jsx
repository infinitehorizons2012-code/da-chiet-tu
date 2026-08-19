import React, { useState, useEffect } from 'react';

export default function TracNghiemTab({ currentUser, userStats, setUserStats, savedSession, setSavedSession, researchDataObj, getSrsStatus, getSrsLevel }) {
  const [quizMode, setQuizMode] = useState('chiettu');
  const [dueChars, setDueChars] = useState([]);
  
  // Session State: { mode, questions: [charObjs], currentIndex, results: { char: true/false } }
  const [session, setSession] = useState(null);
  
  const [currentChar, setCurrentChar] = useState(null);
  const [strokePaths, setStrokePaths] = useState([]);
  const [strokeColors, setStrokeColors] = useState({});
  const [activeComp, setActiveComp] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isRevealed, setIsRevealed] = useState(false);
  const [mcq, setMcq] = useState(null);
  const [selectedOption, setSelectedOption] = useState(null);
  const [sessionFinished, setSessionFinished] = useState(false);

  // Sync XP/LP to Backend
  const syncUserStats = async (newXp, newLp) => {
    try {
      await fetch('/api/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: currentUser,
          char: '__USER_STATS__',
          comps: { srs: { xp: newXp, lp: newLp } }
        })
      });
      setUserStats({ xp: newXp, lp: newLp });
    } catch (e) {
      console.error(e);
    }
  };

  // Sync Session to Backend (for Save & Exit)
  const syncSession = async (sessData) => {
    try {
      await fetch('/api/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: currentUser,
          char: '__QUIZ_SESSION__',
          comps: { srs: sessData }
        })
      });
      setSavedSession(sessData);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
     const eligible = researchDataObj.filter(item => {
        const status = getSrsStatus(item, quizMode);
        return status && status !== 'bat_dau';
     });
     eligible.sort(() => Math.random() - 0.5); 
     setDueChars(eligible);
  }, [quizMode, researchDataObj, getSrsStatus]);

  // When session starts or advances
  useEffect(() => {
     if (session && session.currentIndex < session.questions.length) {
         loadNextCharacter(session.questions[session.currentIndex]);
     } else if (session && session.currentIndex >= session.questions.length && session.questions.length > 0) {
         setSessionFinished(true);
         // Automatically finish and reward
         finishSession();
     }
  }, [session?.currentIndex, session?.questions]);

  const startSession = (numQuestions) => {
      let selected = dueChars.slice(0, numQuestions);
      setSession({
          mode: quizMode,
          questions: selected,
          currentIndex: 0,
          results: {}
      });
      setSessionFinished(false);
  };

  const resumeSession = () => {
      if (savedSession) {
          setQuizMode(savedSession.mode);
          setSession(savedSession);
          setSessionFinished(false);
      }
  };

  const saveAndExit = async () => {
      if (userStats.lp < 120) {
          alert('Bạn cần ít nhất 120 LP để Lưu & Thoát!');
          return;
      }
      await syncUserStats(userStats.xp, userStats.lp - 120);
      await syncSession(session);
      setSession(null);
      setCurrentChar(null);
  };

  const finishSession = async () => {
      // Apply SRS for all results
      let promises = [];
      for (const charObj of session.questions) {
          const char = charObj['Chữ Trung Quốc'];
          const isCorrect = session.results[char];
          
          let currentStatus = getSrsStatus(charObj, session.mode);
          let currentLevel = getSrsLevel(charObj, session.mode);
          let newStatus = currentStatus;
          let newLevel = currentLevel;

          if (isCorrect) {
              if (currentStatus === 'san_sang_thi') { newStatus = 'hat_mam'; newLevel = 1; }
              else if (currentStatus === 'hat_mam') { newLevel += 1; if (newLevel >= 2) newStatus = 'cay'; }
              else if (currentStatus === 'cay') { newLevel += 1; if (newLevel >= 3) newStatus = 'hoa'; }
              else if (currentStatus === 'hoa') { newLevel += 1; }
          } else {
              if (currentStatus === 'hoa') { newStatus = 'cay'; }
              else if (currentStatus === 'cay') { newStatus = 'hat_mam'; }
              else if (currentStatus === 'hat_mam') { newStatus = 'san_sang_thi'; }
              newLevel = 0;
          }
          
          const newSrs = { ...charObj.srs, [session.mode]: { status: newStatus, level: newLevel } };
          charObj.srs = newSrs; // Update local

          promises.push(
              fetch('/api/save', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({
                      username: currentUser, 
                      char: char, 
                      comps: { srs: newSrs } 
                  })
              })
          );
      }

      await Promise.all(promises);
      await syncUserStats(userStats.xp, userStats.lp + 30);
      
      // Clear saved session
      await syncSession(null);
      
      // Auto-hide the congratulation screen after 3.5 seconds
      setTimeout(() => {
          setSession(null);
          setCurrentChar(null);
          setSessionFinished(false);
      }, 3500);
      
      // Refresh due chars
      const eligible = researchDataObj.filter(item => {
        const status = getSrsStatus(item, quizMode);
        return status && status !== 'bat_dau';
      });
      eligible.sort(() => Math.random() - 0.5); 
      setDueChars(eligible);
  };

  const handleNextQuestion = (isCorrect, usedRetry = false) => {
      let newXp = userStats.xp;
      if (isCorrect && !usedRetry) {
          newXp += 30; // +30 XP for correct answer
      }
      
      syncUserStats(newXp, userStats.lp);
      
      setSession(prev => ({
          ...prev,
          results: { ...prev.results, [currentChar['Chữ Trung Quốc']]: isCorrect },
          currentIndex: prev.currentIndex + 1
      }));
  };

  const handleRetry = () => {
      if (userStats.xp < 120) {
          alert('Không đủ 120 XP để thử lại!');
          return;
      }
      syncUserStats(userStats.xp - 120, userStats.lp);
      setIsRevealed(false);
      setFeedback(null);
      setStrokeColors({});
      setSelectedOption(null);
  };

  const generateMultipleChoice = (charObj, mode) => {
     let questionText = '';
     let answerText = '';
     let options = [];
     let questionField = '';
     let answerField = '';
     
     if (mode === 'han_pinyin') {
        questionText = `Chọn Pinyin đúng cho chữ: ${charObj['Chữ Trung Quốc']}`;
        answerText = charObj['Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)'];
        answerField = 'Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)';
     } else if (mode === 'pinyin_han') {
        questionText = `Chọn chữ Hán có Pinyin là: ${charObj['Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)']}`;
        answerText = charObj['Chữ Trung Quốc'];
        answerField = 'Chữ Trung Quốc';
        questionField = 'Pinyin_Master (Pinyin Chuẩn Tổng Hợp 100%)';
     } else if (mode === 'han_hanviet') {
        questionText = `Chọn Âm Hán Việt đúng cho chữ: ${charObj['Chữ Trung Quốc']}`;
        answerText = charObj['Âm Hán Việt (Master 100%)'];
        answerField = 'Âm Hán Việt (Master 100%)';
     } else if (mode === 'hanviet_han') {
        questionText = `Chọn chữ Hán có Âm Hán Việt là: ${charObj['Âm Hán Việt (Master 100%)']}`;
        answerText = charObj['Chữ Trung Quốc'];
        answerField = 'Chữ Trung Quốc';
        questionField = 'Âm Hán Việt (Master 100%)';
     } else if (mode === 'han_nghia') {
        questionText = `Chọn nghĩa đúng cho chữ: ${charObj['Chữ Trung Quốc']}`;
        answerText = charObj['Nghĩa Tiếng Việt (Master 100%)'];
        answerField = 'Nghĩa Tiếng Việt (Master 100%)';
     } else if (mode === 'han_mnemonic') {
        questionText = `Chọn cách ghi nhớ đúng cho chữ: ${charObj['Chữ Trung Quốc']}`;
        answerText = charObj['App_Mnemonic'];
        answerField = 'App_Mnemonic';
     } else if (mode === 'mnemonic_han') {
        questionText = `Mnemonic sau đây là của chữ Hán nào:\n"${charObj['App_Mnemonic']}"`;
        answerText = charObj['Chữ Trung Quốc'];
        answerField = 'Chữ Trung Quốc';
        questionField = 'App_Mnemonic';
     }

     if (!answerText || answerText === 'nan') return null;

     let validPool = researchDataObj.filter(item => {
        if (item['Chữ Trung Quốc'] === charObj['Chữ Trung Quốc']) return false;
        if (!item[answerField] || item[answerField] === 'nan' || item[answerField] === '') return false;
        if (questionField && item[questionField] === charObj[questionField]) return false;
        if (item[answerField] === answerText) return false;
        return true;
     });

     validPool.sort(() => Math.random() - 0.5);
     const distractors = validPool.slice(0, 3).map(i => i[answerField]);
     
     options = [answerText, ...distractors].sort(() => Math.random() - 0.5);
     
     return { questionText, options, correctAnswer: answerText };
  };

  const loadNextCharacter = async (charObj) => {
    setLoading(true);
    setFeedback(null);
    setStrokeColors({});
    setActiveComp(null);
    setIsRevealed(false);
    setSelectedOption(null);
    setMcq(null);
    
    if (session.mode !== 'chiettu') {
       const mcqData = generateMultipleChoice(charObj, session.mode);
       setMcq(mcqData);
       if (!mcqData) {
          setFeedback({ type: 'error', message: 'Dữ liệu của chữ này bị thiếu, không tạo được câu hỏi.' });
       }
       setCurrentChar(charObj);
       setLoading(false);
       return;
    }

    const char = charObj['Chữ Trung Quốc'];
    const comps = [];
    const COLORS = [ '#e11d48', '#2563eb', '#059669', '#eab308', '#a855f7', '#10b981', '#f97316', '#14b8a6', '#6366f1', '#ec4899', '#8b5cf6', '#0ea5e9' ];
    let compIndex = 0;
    for (let i = 1; i <= 12; i++) {
      const compStr = charObj[`App_Comp_${i}`];
      if (compStr && compStr !== 'nan' && compStr.trim() !== '') {
        comps.push({ id: `App_Comp_${i}`, text: compStr.trim(), color: COLORS[compIndex % COLORS.length] });
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

  const CYCLE_COLORS = ['#cbd5e1', '#e11d48', '#2563eb', '#059669', '#eab308', '#a855f7', '#f97316'];

  const handleStrokeClick = (strokeIndex) => {
    if (isRevealed || session.mode !== 'chiettu') return;
    setStrokeColors(prev => {
      const next = { ...prev };
      const currentColor = next[strokeIndex] || '#cbd5e1';
      let currentIndex = CYCLE_COLORS.indexOf(currentColor);
      if (currentIndex === -1) currentIndex = 0;
      const nextIndex = (currentIndex + 1) % CYCLE_COLORS.length;
      next[strokeIndex] = CYCLE_COLORS[nextIndex];
      return next;
    });
  };

  const checkChiettuAnswer = () => {
    if (!currentChar) return;
    const correctMapping = currentChar.quiz_mapping;
    if (!correctMapping) {
       setFeedback({ type: 'error', message: 'Chữ này chưa có đáp án trên hệ thống! Vui lòng nhờ admin tạo đáp án trước.' });
       setIsRevealed(true);
       return;
    }

    const expectedGroups = Object.values(correctMapping).map(arr => [...arr].sort((a,b)=>a-b));
    const userGroupsMap = {};
    Object.entries(strokeColors).forEach(([idxStr, color]) => {
       if (color === '#cbd5e1' || !color) return;
       if (!userGroupsMap[color]) userGroupsMap[color] = [];
       userGroupsMap[color].push(parseInt(idxStr, 10));
    });
    const userGroups = Object.values(userGroupsMap).map(arr => arr.sort((a,b)=>a-b));

    let isCorrect = false;
    if (expectedGroups.length > 0 && expectedGroups.length === userGroups.length) {
       const allMatch = expectedGroups.every(eg => {
          return userGroups.some(ug => ug.length === eg.length && ug.every((v, i) => v === eg[i]));
       });
       isCorrect = allMatch;
    }

    if (isCorrect) {
       setFeedback({ type: 'success', message: 'Tuyệt vời! Con đã phân tách chính xác các linh kiện của chữ này.' });
       setIsRevealed(true);
    } else {
       setFeedback({ type: 'error', message: 'Chưa chính xác rồi. Con xem lại đáp án ở dưới nhé!' });
       setIsRevealed(true);
    }
  };

  const handleMcqSelect = (option) => {
     if (isRevealed) return;
     setSelectedOption(option);
     setIsRevealed(true);
     if (option === mcq.correctAnswer) {
        setFeedback({ type: 'success', message: 'Chính xác!' });
        setTimeout(() => handleNextQuestion(true), 1500);
     } else {
        setFeedback({ type: 'error', message: `Chưa chính xác! Đáp án đúng là: ${mcq.correctAnswer}` });
     }
  };

  const TABS = [
    { id: 'chiettu', label: 'Chiết tự' },
    { id: 'han_pinyin', label: 'Hán -> Pinyin' },
    { id: 'pinyin_han', label: 'Pinyin -> Hán' },
    { id: 'han_hanviet', label: 'Hán -> Hán Việt' },
    { id: 'hanviet_han', label: 'Hán Việt -> Hán' },
    { id: 'han_nghia', label: 'Hán -> Nghĩa' },
    { id: 'han_mnemonic', label: 'Hán -> Mnemonic' },
    { id: 'mnemonic_han', label: 'Mnemonic -> Hán' }
  ];

  if (sessionFinished) {
      return (
          <div className="tracnghiem-tab" style={{ padding: '20px', maxWidth: '900px', margin: '0 auto', textAlign: 'center' }}>
             <h2>🎉 Chúc mừng! Bạn đã hoàn thành bài tập.</h2>
             <p>Bạn nhận được <strong>+30 LP</strong> vì đã hoàn thành.</p>
             <button className="save-btn" onClick={() => { setSession(null); setCurrentChar(null); setSessionFinished(false); }} style={{ background: '#3b82f6', fontSize: '1.2rem', padding: '15px 30px', marginTop: '20px' }}>
                Trở về danh mục
             </button>
          </div>
      );
  }

  if (!session) {
      return (
        <div className="tracnghiem-tab" style={{ padding: '20px', maxWidth: '900px', margin: '0 auto' }}>
          <div className="tab-navigation" style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', marginBottom: '20px', justifyContent: 'center' }}>
              <button 
                className={`tab-btn ${quizMode === 'chiettu' ? 'active' : ''}`} 
                onClick={() => setQuizMode('chiettu')}
                style={{ fontSize: '0.9rem', padding: '8px 12px' }}
              >
                Chiết tự
              </button>

              <select 
                className={`tab-btn ${['han_pinyin','pinyin_han'].includes(quizMode) ? 'active' : ''}`}
                value={['han_pinyin','pinyin_han'].includes(quizMode) ? quizMode : 'placeholder'}
                onChange={(e) => setQuizMode(e.target.value)}
                style={{ fontSize: '0.9rem', padding: '8px 12px', appearance: 'auto' }}
              >
                <option value="placeholder" disabled hidden>Hán ↔ Pinyin ▾</option>
                <option value="han_pinyin">Hán ➔ Pinyin</option>
                <option value="pinyin_han">Pinyin ➔ Hán</option>
              </select>

              <select 
                className={`tab-btn ${['han_hanviet','hanviet_han'].includes(quizMode) ? 'active' : ''}`}
                value={['han_hanviet','hanviet_han'].includes(quizMode) ? quizMode : 'placeholder'}
                onChange={(e) => setQuizMode(e.target.value)}
                style={{ fontSize: '0.9rem', padding: '8px 12px', appearance: 'auto' }}
              >
                <option value="placeholder" disabled hidden>Hán ↔ Hán Việt ▾</option>
                <option value="han_hanviet">Hán ➔ Hán Việt</option>
                <option value="hanviet_han">Hán Việt ➔ Hán</option>
              </select>

              <button 
                className={`tab-btn ${quizMode === 'han_nghia' ? 'active' : ''}`} 
                onClick={() => setQuizMode('han_nghia')}
                style={{ fontSize: '0.9rem', padding: '8px 12px' }}
              >
                Hán ➔ Nghĩa
              </button>

              <select 
                className={`tab-btn ${['han_mnemonic','mnemonic_han'].includes(quizMode) ? 'active' : ''}`}
                value={['han_mnemonic','mnemonic_han'].includes(quizMode) ? quizMode : 'placeholder'}
                onChange={(e) => setQuizMode(e.target.value)}
                style={{ fontSize: '0.9rem', padding: '8px 12px', appearance: 'auto' }}
              >
                <option value="placeholder" disabled hidden>Hán ↔ Mnemonic ▾</option>
                <option value="han_mnemonic">Hán ➔ Mnemonic</option>
                <option value="mnemonic_han">Mnemonic ➔ Hán</option>
              </select>
          </div>

          <div style={{ textAlign: 'center', padding: '30px', background: 'white', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}>
             <h2>Bắt đầu bài trắc nghiệm</h2>
             <p style={{ margin: '20px 0', color: '#64748b' }}>Bạn hiện có <strong>{dueChars.length}</strong> câu hỏi đến hạn trong phần này.</p>
             
             {dueChars.length > 0 ? (
                 <div style={{ display: 'flex', gap: '15px', justifyContent: 'center', marginTop: '20px' }}>
                     <button className="save-btn" onClick={() => startSession(Math.min(5, dueChars.length))} style={{ background: '#3b82f6' }}>Làm {Math.min(5, dueChars.length)} câu</button>
                     {dueChars.length > 5 && <button className="save-btn" onClick={() => startSession(Math.min(10, dueChars.length))} style={{ background: '#3b82f6' }}>Làm {Math.min(10, dueChars.length)} câu</button>}
                     {dueChars.length > 10 && <button className="save-btn" onClick={() => startSession(dueChars.length)} style={{ background: '#3b82f6' }}>Làm tất cả</button>}
                 </div>
             ) : (
                 <p>Tuyệt vời! Bạn đã hoàn thành tất cả bài tập hôm nay.</p>
             )}

             {savedSession && (
                 <div style={{ marginTop: '40px', paddingTop: '20px', borderTop: '1px solid #e2e8f0' }}>
                     <h3>Bạn có một bài tập đang làm dở</h3>
                     <p>Chế độ: {TABS.find(t => t.id === savedSession.mode)?.label}</p>
                     <p>Tiến độ: Câu {savedSession.currentIndex + 1} / {savedSession.questions.length}</p>
                     <button className="save-btn" onClick={resumeSession} style={{ background: '#f59e0b', marginTop: '15px' }}>Tiếp tục bài đang dở</button>
                 </div>
             )}
          </div>
        </div>
      );
  }

  return (
    <div className="tracnghiem-tab" style={{ padding: '20px', maxWidth: '900px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
         <div style={{ fontWeight: 'bold', color: '#64748b' }}>
             Tiến độ: Câu {session.currentIndex + 1} / {session.questions.length}
         </div>
         <button className="save-btn" onClick={saveAndExit} style={{ background: '#f59e0b', padding: '8px 15px', fontSize: '0.9rem' }}>
            Lưu & Thoát (-120 LP)
         </button>
      </div>

      {!currentChar || loading ? (
        <div style={{textAlign: 'center', padding: '50px'}}>Đang tải câu hỏi...</div>
      ) : (
        <>
          <div className="tracnghiem-header" style={{ textAlign: 'center', marginBottom: '20px' }}>
            <div className="srs-badge" style={{ display: 'inline-block', background: '#e0f2fe', color: '#0284c7', padding: '5px 15px', borderRadius: '20px', fontWeight: 'bold' }}>
              Cấp bậc hiện tại: {
                {
                  'san_sang_thi': '🎯 Sẵn sàng thi',
                  'hat_mam': '🌱 Hạt mầm',
                  'cay': '🌳 Cây',
                  'hoa': '🌸 Hoa'
                }[getSrsStatus(currentChar, session.mode)] || 'Không xác định'
              }
            </div>
          </div>

          {session.mode === 'chiettu' ? (
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
                        onClick={() => handleStrokeClick(idx)}
                        style={{ cursor: isRevealed ? 'default' : 'pointer' }}
                      />
                    ))}
                  </g>
                </svg>

                {feedback && (
                  <div className={`feedback-box ${feedback.type}`} style={{ marginTop: '20px', padding: '15px', borderRadius: '8px', fontWeight: 'bold', background: feedback.type === 'success' ? '#dcfce7' : '#fee2e2', color: feedback.type === 'success' ? '#166534' : '#991b1b' }}>
                    {feedback.message}
                  </div>
                )}
              </div>
              
              <div className="chiettu-components-panel" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                {isRevealed ? (
                  <>
                    <h3>Đáp án: Các linh kiện ({currentChar['Chữ Trung Quốc']})</h3>
                    <div className="comp-list">
                      {currentChar.parsedComps.map(comp => (
                        <div key={comp.id} className="comp-item" style={{ borderLeftColor: comp.color }}>
                          <div className="comp-color-box" style={{ backgroundColor: comp.color }}></div>
                          <span className="comp-text">{comp.text}</span>
                        </div>
                      ))}
                    </div>
                    {feedback?.type === 'success' ? (
                      <button className="save-btn next-btn" onClick={() => handleNextQuestion(true)} style={{ background: '#10b981', marginTop: '20px' }}>
                        Câu Tiếp Theo ➔
                      </button>
                    ) : (
                      <div style={{ marginTop: '30px' }}>
                        <h4 style={{ textAlign: 'center', marginBottom: '15px' }}>Bạn làm đúng chứ?</h4>
                        <div style={{ display: 'flex', gap: '15px' }}>
                           <button className="save-btn" onClick={() => handleNextQuestion(false)} style={{ background: '#ef4444', flex: 1 }}>Sai (Tiếp tục)</button>
                           <button className="save-btn" onClick={() => handleNextQuestion(true)} style={{ background: '#10b981', flex: 1 }}>Đúng (+30 XP)</button>
                        </div>
                        <div style={{ marginTop: '15px' }}>
                           <button className="save-btn" onClick={handleRetry} disabled={userStats.xp < 120} style={{ background: userStats.xp >= 120 ? '#8b5cf6' : '#cbd5e1', width: '100%', cursor: userStats.xp >= 120 ? 'pointer' : 'not-allowed' }}>
                              Thử lại (-120 XP)
                           </button>
                        </div>
                      </div>
                    )}
                  </>
                ) : (
                  <div style={{ textAlign: 'center' }}>
                    <h3 style={{ marginBottom: '10px', color: '#64748b' }}>Phân tách nét chữ thành linh kiện</h3>
                    <p style={{ marginBottom: '20px', color: '#64748b', fontSize: '0.9rem' }}>Nhấp vào các nét bên trái để tự động gom nhóm bằng màu sắc.</p>
                    <button className="save-btn" onClick={checkChiettuAnswer} style={{ background: '#3b82f6', fontSize: '1.2rem', padding: '15px 30px', width: '100%' }}>
                      Kiểm tra đối chiếu
                    </button>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="mcq-workspace" style={{ background: 'white', padding: '30px', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.05)', textAlign: 'center' }}>
              {mcq ? (
                <>
                  <h3 style={{ fontSize: '1.3rem', color: '#334155', marginBottom: '30px', whiteSpace: 'pre-wrap' }}>{mcq.questionText}</h3>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
                    {mcq.options.map((option, idx) => {
                      let bgColor = '#f8fafc';
                      let color = '#334155';
                      let border = '2px solid #e2e8f0';
                      
                      if (isRevealed) {
                        if (option === mcq.correctAnswer) {
                          bgColor = '#dcfce7'; color = '#166534'; border = '2px solid #22c55e';
                        } else if (option === selectedOption) {
                          bgColor = '#fee2e2'; color = '#991b1b'; border = '2px solid #ef4444';
                        }
                      }

                      return (
                        <button 
                          key={idx}
                          onClick={() => handleMcqSelect(option)}
                          disabled={isRevealed}
                          style={{
                            padding: '20px', fontSize: '1.2rem', borderRadius: '12px',
                            background: bgColor, color, border,
                            cursor: isRevealed ? 'default' : 'pointer',
                            transition: 'all 0.2s'
                          }}
                        >
                          {option}
                        </button>
                      );
                    })}
                  </div>
                  {feedback && (
                    <div className={`feedback-box ${feedback.type}`} style={{ marginTop: '20px', padding: '15px', borderRadius: '8px', fontWeight: 'bold', background: feedback.type === 'success' ? '#dcfce7' : '#fee2e2', color: feedback.type === 'success' ? '#166534' : '#991b1b' }}>
                      {feedback.message}
                    </div>
                  )}
                  {isRevealed && feedback?.type === 'error' && (
                    <div style={{ marginTop: '20px', display: 'flex', gap: '15px', justifyContent: 'center' }}>
                        <button className="save-btn next-btn" onClick={() => handleNextQuestion(false)} style={{ background: '#ef4444', padding: '10px 30px' }}>
                            Tiếp tục (Sai)
                        </button>
                        <button className="save-btn" onClick={handleRetry} disabled={userStats.xp < 120} style={{ background: userStats.xp >= 120 ? '#8b5cf6' : '#cbd5e1', padding: '10px 30px', cursor: userStats.xp >= 120 ? 'pointer' : 'not-allowed' }}>
                            Thử lại (-120 XP)
                        </button>
                    </div>
                  )}
                </>
              ) : (
                <div>
                   {feedback ? feedback.message : 'Lỗi tạo câu hỏi.'}
                   <button className="save-btn next-btn" onClick={() => handleNextQuestion(false)} style={{ background: '#3b82f6', marginTop: '20px' }}>Bỏ qua chữ này</button>
                </div>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
}