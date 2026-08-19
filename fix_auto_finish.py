import re

with open('src/TracNghiemTab.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# I want to modify the finishSession to NOT clear the session state immediately,
# but instead just do the backend sync. We can then clear the session state manually.

# Wait, if I just rename finishSession to something else, and create a new useEffect.
# Actually, the simplest way is to auto-run the logic when sessionFinished becomes true.

old_use_effect = """  // When session starts or advances
  useEffect(() => {
     if (session && session.currentIndex < session.questions.length) {
         loadNextCharacter(session.questions[session.currentIndex]);
     } else if (session && session.currentIndex >= session.questions.length && session.questions.length > 0) {
         setSessionFinished(true);
     }
  }, [session?.currentIndex, session?.questions]);"""

new_use_effect = """  // When session starts or advances
  useEffect(() => {
     if (session && session.currentIndex < session.questions.length) {
         loadNextCharacter(session.questions[session.currentIndex]);
     } else if (session && session.currentIndex >= session.questions.length && session.questions.length > 0) {
         setSessionFinished(true);
         // Automatically finish and reward
         finishSession();
     }
  }, [session?.currentIndex, session?.questions]);"""

old_finish = """      // Clear saved session
      await syncSession(null);
      
      setSession(null);
      setCurrentChar(null);
      setSessionFinished(false);"""

new_finish = """      // Clear saved session
      await syncSession(null);
      
      // Auto-hide the congratulation screen after 3.5 seconds
      setTimeout(() => {
          setSession(null);
          setCurrentChar(null);
          setSessionFinished(false);
      }, 3500);"""

content = content.replace(old_use_effect, new_use_effect)
content = content.replace(old_finish, new_finish)

# And remove the button click for finishSession
old_button = """<button className="save-btn" onClick={finishSession} style={{ background: '#10b981', fontSize: '1.2rem', padding: '15px 30px', marginTop: '20px' }}>
                Nhận thưởng & Kết thúc
             </button>"""

new_button = """<button className="save-btn" onClick={() => { setSession(null); setCurrentChar(null); setSessionFinished(false); }} style={{ background: '#3b82f6', fontSize: '1.2rem', padding: '15px 30px', marginTop: '20px' }}>
                Trở về danh mục
             </button>"""

content = content.replace(old_button, new_button)

with open('src/TracNghiemTab.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated successfully")
