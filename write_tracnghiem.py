content = """import React, { useState, useEffect } from 'react';

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
          alert('B?n c?n ít nh?t 120 LP d? Luu & Thoát!');
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
          const char = charObj['Ch? Trung Qu?c'];
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
          
          const newSrs = { ...charObj.srs, [`srs_${session.mode}`]: { status: newStatus, level: newLevel } };
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
      
      setSession(null);
      setCurrentChar(null);
      setSessionFinished(false);
      
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
          results: { ...prev.results, [currentChar['Ch? Trung Qu?c']]: isCorrect },
          currentIndex: prev.currentIndex + 1
      }));
  };

  const handleRetry = () => {
      if (userStats.xp < 120) {
          alert('Không d? 120 XP d? th? l?i!');
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
        questionText = `Ch?n Pinyin dúng cho ch?: ${charObj['Ch? Trung Qu?c']}`;
        answerText = charObj['Pinyin_Master (Pinyin Chu?n T?ng H?p 100%)'];
        answerField = 'Pinyin_Master (Pinyin Chu?n T?ng H?p 100%)';
     } else if (mode === 'pinyin_han') {
        questionText = `Ch?n ch? Hán có Pinyin là: ${charObj['Pinyin_Master (Pinyin Chu?n T?ng H?p 100%)']}`;
        answerText = charObj['Ch? Trung Qu?c'];
        answerField = 'Ch? Trung Qu?c';
        questionField = 'Pinyin_Master (Pinyin Chu?n T?ng H?p 100%)';
     } else if (mode === 'han_hanviet') {
        questionText = `Ch?n Âm Hán Vi?t dúng cho ch?: ${charObj['Ch? Trung Qu?c']}`;
        answerText = charObj['Âm Hán Vi?t (Master 100%)'];
        answerField = 'Âm Hán Vi?t (Master 100%)';
     } else if (mode === 'hanviet_han') {
        questionText = `Ch?n ch? Hán có Âm Hán Vi?t là: ${charObj['Âm Hán Vi?t (Master 100%)']}`;
        answerText = charObj['Ch? Trung Qu?c'];
        answerField = 'Ch? Trung Qu?c';
        questionField = 'Âm Hán Vi?t (Master 100%)';
     } else if (mode === 'han_nghia') {
        questionText = `Ch?n nghia dúng cho ch?: ${charObj['Ch? Trung Qu?c']}`;
        answerText = charObj['Nghia Ti?ng Vi?t (Master 100%)'];
        answerField = 'Nghia Ti?ng Vi?t (Master 100%)';
     } else if (mode === 'han_mnemonic') {
        questionText = `Ch?n cách ghi nh? dúng cho ch?: ${charObj['Ch? Trung Qu?c']}`;
        answerText = charObj['App_Mnemonic'];
        answerField = 'App_Mnemonic';
     } else if (mode === 'mnemonic_han') {
        questionText = `Mnemonic sau dây là c?a ch? Hán nào:\n"${charObj['App_Mnemonic']}"`;
        answerText = charObj['Ch? Trung Qu?c'];
        answerField = 'Ch? Trung Qu?c';
        questionField = 'App_Mnemonic';
     }

     if (!answerText || answerText === 'nan') return null;

     let validPool = researchDataObj.filter(item => {
        if (item['Ch? Trung Qu?c'] === charObj['Ch? Trung Qu?c']) return false;
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
          setFeedback({ type: 'error', message: 'D? li?u c?a ch? này b? thi?u, không t?o du?c câu h?i.' });
       }
       setCurrentChar(charObj);
       setLoading(false);
       return;
    }

    const char = charObj['Ch? Trung Qu?c'];
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
        setFeedback({ type: 'error', message: `Không tìm th?y nét v? cho ch? ${char}`});
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
       setFeedback({ type: 'error', message: 'Ch? này chua có dáp án trên h? th?ng! Vui lòng nh? admin t?o dáp án tru?c.' });
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
       setFeedback({ type: 'success', message: 'Tuy?t v?i! Con dã phân tách chính xác các linh ki?n c?a ch? này.' });
       setIsRevealed(true);
    } else {
       setFeedback({ type: 'error', message: 'Chua chính xác r?i. Con xem l?i dáp án ? du?i nhé!' });
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
        setFeedback({ type: 'error', message: `Chua chính xác! Ðáp án dúng là: ${mcq.correctAnswer}` });
     }
  };

  const TABS = [
    { id: 'chiettu', label: 'Chi?t t?' },
    { id: 'han_pinyin', label: 'Hán -> Pinyin' },
    { id: 'pinyin_han', label: 'Pinyin -> Hán' },
    { id: 'han_hanviet', label: 'Hán -> Hán Vi?t' },
    { id: 'hanviet_han', label: 'Hán Vi?t -> Hán' },
    { id: 'han_nghia', label: 'Hán -> Nghia' },
    { id: 'han_mnemonic', label: 'Hán -> Mnemonic' },
    { id: 'mnemonic_han', label: 'Mnemonic -> Hán' }
  ];

  if (sessionFinished) {
      return (
          <div className="tracnghiem-tab" style={{ padding: '20px', maxWidth: '900px', margin: '0 auto', textAlign: 'center' }}>
             <h2>?? Chúc m?ng! B?n dã hoàn thành bài t?p.</h2>
             <p>B?n nh?n du?c <strong>+30 LP</strong> vì dã hoàn thành.</p>
             <button className="save-btn" onClick={finishSession} style={{ background: '#10b981', fontSize: '1.2rem', padding: '15px 30px', marginTop: '20px' }}>
                Nh?n thu?ng & K?t thúc
             </button>
          </div>
      );
  }

  if (!session) {
      return (
        <div className="tracnghiem-tab" style={{ padding: '20px', maxWidth: '900px', margin: '0 auto' }}>
          <div className="tab-navigation" style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', marginBottom: '20px', justifyContent: 'center' }}>
            {TABS.map(tab => (
              <button 
                key={tab.id}
                className={`tab-btn ${quizMode === tab.id ? 'active' : ''}`} 
                onClick={() => setQuizMode(tab.id)}
                style={{ fontSize: '0.9rem', padding: '8px 12px' }}
              >
                {tab.label}
              </button>
            ))}
          </div>

          <div style={{ textAlign: 'center', padding: '30px', background: 'white', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}>
             <h2>B?t d?u bài tr?c nghi?m</h2>
             <p style={{ margin: '20px 0', color: '#64748b' }}>B?n hi?n có <strong>{dueChars.length}</strong> câu h?i d?n h?n trong ph?n này.</p>
             
             {dueChars.length > 0 ? (
                 <div style={{ display: 'flex', gap: '15px', justifyContent: 'center', marginTop: '20px' }}>
                     <button className="save-btn" onClick={() => startSession(Math.min(5, dueChars.length))} style={{ background: '#3b82f6' }}>Làm {Math.min(5, dueChars.length)} câu</button>
                     {dueChars.length > 5 && <button className="save-btn" onClick={() => startSession(Math.min(10, dueChars.length))} style={{ background: '#3b82f6' }}>Làm {Math.min(10, dueChars.length)} câu</button>}
                     {dueChars.length > 10 && <button className="save-btn" onClick={() => startSession(dueChars.length)} style={{ background: '#3b82f6' }}>Làm t?t c?</button>}
                 </div>
             ) : (
                 <p>Tuy?t v?i! B?n dã hoàn thành t?t c? bài t?p hôm nay.</p>
             )}

             {savedSession && (
                 <div style={{ marginTop: '40px', paddingTop: '20px', borderTop: '1px solid #e2e8f0' }}>
                     <h3>B?n có m?t bài t?p dang làm d?</h3>
                     <p>Ch? d?: {TABS.find(t => t.id === savedSession.mode)?.label}</p>
                     <p>Ti?n d?: Câu {savedSession.currentIndex + 1} / {savedSession.questions.length}</p>
                     <button className="save-btn" onClick={resumeSession} style={{ background: '#f59e0b', marginTop: '15px' }}>Ti?p t?c bài dang d?</button>
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
             Ti?n d?: Câu {session.currentIndex + 1} / {session.questions.length}
         </div>
         <button className="save-btn" onClick={saveAndExit} style={{ background: '#f59e0b', padding: '8px 15px', fontSize: '0.9rem' }}>
            Luu & Thoát (-120 LP)
         </button>
      </div>

      {!currentChar || loading ? (
        <div style={{textAlign: 'center', padding: '50px'}}>Ðang t?i câu h?i...</div>
      ) : (
        <>
          <div className="tracnghiem-header" style={{ textAlign: 'center', marginBottom: '20px' }}>
            <div className="srs-badge" style={{ display: 'inline-block', background: '#e0f2fe', color: '#0284c7', padding: '5px 15px', borderRadius: '20px', fontWeight: 'bold' }}>
              C?p b?c hi?n t?i: {
                {
                  'san_sang_thi': '?? S?n sàng thi',
                  'hat_mam': '?? H?t m?m',
                  'cay': '?? Cây',
                  'hoa': '?? Hoa'
                }[getSrsStatus(currentChar, session.mode)] || 'Không xác d?nh'
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
                    <h3>Ðáp án: Các linh ki?n ({currentChar['Ch? Trung Qu?c']})</h3>
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
                        Câu Ti?p Theo ?
                      </button>
                    ) : (
                      <div style={{ marginTop: '30px' }}>
                        <h4 style={{ textAlign: 'center', marginBottom: '15px' }}>B?n làm dúng ch??</h4>
                        <div style={{ display: 'flex', gap: '15px' }}>
                           <button className="save-btn" onClick={() => handleNextQuestion(false)} style={{ background: '#ef4444', flex: 1 }}>Sai (Ti?p t?c)</button>
                           <button className="save-btn" onClick={() => handleNextQuestion(true)} style={{ background: '#10b981', flex: 1 }}>Ðúng (+30 XP)</button>
                        </div>
                        <div style={{ marginTop: '15px' }}>
                           <button className="save-btn" onClick={handleRetry} disabled={userStats.xp < 120} style={{ background: userStats.xp >= 120 ? '#8b5cf6' : '#cbd5e1', width: '100%', cursor: userStats.xp >= 120 ? 'pointer' : 'not-allowed' }}>
                              Th? l?i (-120 XP)
                           </button>
                        </div>
                      </div>
                    )}
                  </>
                ) : (
                  <div style={{ textAlign: 'center' }}>
                    <h3 style={{ marginBottom: '10px', color: '#64748b' }}>Phân tách nét ch? thành linh ki?n</h3>
                    <p style={{ marginBottom: '20px', color: '#64748b', fontSize: '0.9rem' }}>Nh?p vào các nét bên trái d? t? d?ng gom nhóm b?ng màu s?c.</p>
                    <button className="save-btn" onClick={checkChiettuAnswer} style={{ background: '#3b82f6', fontSize: '1.2rem', padding: '15px 30px', width: '100%' }}>
                      Ki?m tra d?i chi?u
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
                            Ti?p t?c (Sai)
                        </button>
                        <button className="save-btn" onClick={handleRetry} disabled={userStats.xp < 120} style={{ background: userStats.xp >= 120 ? '#8b5cf6' : '#cbd5e1', padding: '10px 30px', cursor: userStats.xp >= 120 ? 'pointer' : 'not-allowed' }}>
                            Th? l?i (-120 XP)
                        </button>
                    </div>
                  )}
                </>
              ) : (
                <div>
                   {feedback ? feedback.message : 'L?i t?o câu h?i.'}
                   <button className="save-btn next-btn" onClick={() => handleNextQuestion(false)} style={{ background: '#3b82f6', marginTop: '20px' }}>B? qua ch? này</button>
                </div>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
}
"""
with open('src/TracNghiemTab.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Wrote TracNghiemTab")
