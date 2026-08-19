import re

with open("src/App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

user_info_regex = re.compile(r'<div className="user-info">.*?</div>', re.DOTALL)

new_user_info = """<div className="user-info" style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', justifyContent: 'center' }}>
            <span className="username" style={{ marginRight: '15px', color: '#1e293b' }}>{currentUser}</span>
            {userStats && (
            <span style={{ marginRight: '15px', fontWeight: 'bold', fontSize: '0.85rem' }}>
               <span style={{ color: '#f59e0b' }}>⚡ {userStats.xp} XP</span> <span style={{ margin: '0 4px', color: '#cbd5e1' }}>|</span> <span style={{ color: '#3b82f6' }}>🛡️ {userStats.lp} LP</span>
            </span>
            )}
          </div>"""

if user_info_regex.search(content):
    content = user_info_regex.sub(new_user_info, content)
    with open("src/App.jsx", "w", encoding="utf-8") as f:
        f.write(content)
    print("Injected username via regex!")
else:
    print("Could not find old user-info block.")
