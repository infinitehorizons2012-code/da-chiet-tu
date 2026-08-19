with open('src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = "import TracNghiemTab from './TracNghiemTab';\n" + content
# Ensure props are passed to TracNghiemTab in App.jsx
content = content.replace(
    "<TracNghiemTab currentUser={currentUser} userStats={userStats} setUserStats={setUserStats} savedSession={savedSession} setSavedSession={setSavedSession} />",
    "<TracNghiemTab currentUser={currentUser} userStats={userStats} setUserStats={setUserStats} savedSession={savedSession} setSavedSession={setSavedSession} researchDataObj={researchDataObj} getSrsStatus={getSrsStatus} getSrsLevel={getSrsLevel} />"
)

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

with open('src/TracNghiemTab.jsx', 'r', encoding='utf-8') as f:
    trac = f.read()

trac = trac.replace('function TracNghiemTab({ currentUser }) {', 'export default function TracNghiemTab({ currentUser, userStats, setUserStats, savedSession, setSavedSession, researchDataObj, getSrsStatus, getSrsLevel }) {')

with open('src/TracNghiemTab.jsx', 'w', encoding='utf-8') as f:
    f.write(trac)
print("Updated App.jsx and TracNghiemTab.jsx")
