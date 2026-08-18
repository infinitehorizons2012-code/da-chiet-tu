import re

with open('src/App.jsx', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update Header
header_old = """function Header({ primaryTab, setPrimaryTab }) {"""
header_new = """function Header({ primaryTab, setPrimaryTab, currentUser, setCurrentUser }) {
  const handleLogout = () => {
    setCurrentUser(null);
  };
"""
code = code.replace(header_old, header_new)

header_username_old = """<span className="username">hang</span>"""
header_username_new = """<span className="username">{currentUser || 'hang'}</span>"""
code = code.replace(header_username_old, header_username_new)

header_logout_old = """<button className="icon-button">🚪</button>"""
header_logout_new = """<button className="icon-button" onClick={handleLogout} title="Đăng xuất">🚪</button>"""
code = code.replace(header_logout_old, header_logout_new)


# 2. Add LoginScreen component before App
login_screen = """
function LoginScreen({ onLogin }) {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    const action = isRegister ? 'register' : 'login';
    try {
      const res = await fetch(`/api/auth?action=${action}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      const data = await res.json();
      if (data.success) {
         if (isRegister) {
            setIsRegister(false);
            setError('Tạo tài khoản thành công! Hãy đăng nhập.');
         } else {
            onLogin(username);
         }
      } else {
         setError(data.error);
      }
    } catch (err) {
      setError('Lỗi kết nối');
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Bạn có chắc chắn muốn xóa tài khoản này và TOÀN BỘ dữ liệu học tập không?')) return;
    try {
      const res = await fetch(`/api/auth?action=delete`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      const data = await res.json();
      if (data.success) {
         setError('Xóa tài khoản thành công!');
         setUsername('');
         setPassword('');
      } else {
         setError(data.error);
      }
    } catch (err) {
      setError('Lỗi kết nối');
    }
  };

  return (
    <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', background: '#f8fafc'}}>
      <div style={{background: 'white', padding: '40px', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)', width: '400px'}}>
        <h2 style={{textAlign: 'center', marginBottom: '20px', color: '#1e293b'}}>{isRegister ? 'Tạo Tài Khoản' : 'Đăng Nhập'}</h2>
        <form onSubmit={handleSubmit} style={{display: 'flex', flexDirection: 'column', gap: '15px'}}>
          <input 
            type="text" 
            placeholder="Tên tài khoản (vd: bebi)" 
            value={username} 
            onChange={e => setUsername(e.target.value)}
            style={{padding: '10px', borderRadius: '6px', border: '1px solid #cbd5e1'}}
            required 
          />
          <input 
            type="password" 
            placeholder="Mật khẩu" 
            value={password} 
            onChange={e => setPassword(e.target.value)}
            style={{padding: '10px', borderRadius: '6px', border: '1px solid #cbd5e1'}}
            required 
          />
          {error && <div style={{color: error.includes('thành công') ? 'green' : 'red', fontSize: '0.9rem'}}>{error}</div>}
          <button type="submit" style={{background: '#3b82f6', color: 'white', padding: '10px', borderRadius: '6px', fontWeight: 'bold', cursor: 'pointer'}}>
            {isRegister ? 'Đăng ký' : 'Đăng nhập'}
          </button>
        </form>
        <div style={{marginTop: '20px', textAlign: 'center', fontSize: '0.9rem'}}>
          <span style={{color: '#64748b', cursor: 'pointer', textDecoration: 'underline'}} onClick={() => setIsRegister(!isRegister)}>
            {isRegister ? 'Đã có tài khoản? Đăng nhập' : 'Chưa có tài khoản? Đăng ký'}
          </span>
        </div>
        {!isRegister && (
          <div style={{marginTop: '15px', textAlign: 'center', fontSize: '0.9rem'}}>
            <span style={{color: '#ef4444', cursor: 'pointer', textDecoration: 'underline'}} onClick={handleDelete}>
              Xóa tài khoản này
            </span>
          </div>
        )}
      </div>
    </div>
  );
}

"""
code = code.replace("function App() {", login_screen + "function App() {")

# 3. Modify App state and data fetching
app_top_old = """function App() {
  const [primaryTab, setPrimaryTab] = useState('tracuu');
  const [activeTab, setActiveTab] = useState('lookup');
  const [dataReady, setDataReady] = useState(false);
  const [globalLookupTerm, setGlobalLookupTerm] = useState('');

  useEffect(() => {
    // 1. Fetch static base data
    Promise.all([
      fetch('/data/research_data_1.json').then(res => res.json()),
      fetch('/data/research_data_2.json').then(res => res.json())
    ])
      .then(([part1, part2]) => {
        researchDataObj.push(...part1, ...part2); // Populate global array
        
        // 2. Fetch user edits from Cloudflare D1 Database
        return fetch('/api/updates');
      })
      .then(res => res.json())
      .then(data => {
        if (data && data.success && data.updates) {
          const updates = data.updates;
          researchDataObj.forEach(item => {
            const char = item['Chữ Trung Quốc'];
            if (updates[char]) {
              Object.assign(item, updates[char]);
            }
          });
        }
        setDataReady(true);
      })
      .catch(err => {
        console.error("Failed to load data:", err);
        setDataReady(true); // Vẫn cho phép chạy dùng data gốc
      });
  }, []);"""

app_top_new = """function App() {
  const [primaryTab, setPrimaryTab] = useState('tracuu');
  const [activeTab, setActiveTab] = useState('lookup');
  const [dataReady, setDataReady] = useState(false);
  const [globalLookupTerm, setGlobalLookupTerm] = useState('');
  const [currentUser, setCurrentUser] = useState(null);
  const [baseDataLoaded, setBaseDataLoaded] = useState(false);

  useEffect(() => {
    // 1. Fetch static base data ONCE
    Promise.all([
      fetch('/data/research_data_1.json').then(res => res.json()),
      fetch('/data/research_data_2.json').then(res => res.json())
    ])
      .then(([part1, part2]) => {
        researchDataObj.push(...part1, ...part2);
        setBaseDataLoaded(true);
      });
  }, []);

  useEffect(() => {
    if (!currentUser || !baseDataLoaded) return;
    
    setDataReady(false);
    // Reset SRS and user data
    researchDataObj.forEach(item => { item.srs = undefined; item.quiz_mapping = undefined; item.parsedComps = undefined; });

    fetch(`/api/updates?username=${currentUser}`)
      .then(res => res.json())
      .then(data => {
        if (data && data.success && data.updates) {
          const updates = data.updates;
          researchDataObj.forEach(item => {
            const char = item['Chữ Trung Quốc'];
            if (updates[char]) {
              Object.assign(item, updates[char]);
            }
          });
        }
        setDataReady(true);
      })
      .catch(err => {
        console.error("Failed to load updates:", err);
        setDataReady(true);
      });
  }, [currentUser, baseDataLoaded]);

  if (!currentUser) {
    return <LoginScreen onLogin={setCurrentUser} />;
  }"""

code = code.replace(app_top_old, app_top_new)

# 4. Header props
code = code.replace("<Header primaryTab={primaryTab} setPrimaryTab={setPrimaryTab} />", "<Header primaryTab={primaryTab} setPrimaryTab={setPrimaryTab} currentUser={currentUser} setCurrentUser={setCurrentUser} />")

# 5. ChiettuAdminTab
code = code.replace("function ChiettuAdminTab() {", "function ChiettuAdminTab({ currentUser }) {")
code = code.replace("<ChiettuAdminTab />", "<ChiettuAdminTab currentUser={currentUser} />")
code = code.replace("body: JSON.stringify({ char, comps: { quiz_mapping: payload } })", "body: JSON.stringify({ char, comps: { quiz_mapping: payload }, username: currentUser })")

# Disable save if not admin
chiettu_save_btn_old = """<button 
              className="save-btn" 
              onClick={handleSave} 
              disabled={saving}
            >
              {saving ? 'Đang lưu...' : 'Lưu Đáp Án'}
            </button>"""
chiettu_save_btn_new = """{currentUser === 'admin' ? (
              <button className="save-btn" onClick={handleSave} disabled={saving}>
                {saving ? 'Đang lưu...' : 'Lưu Đáp Án'}
              </button>
            ) : (
              <div style={{marginTop: '20px', color: '#ef4444', fontWeight: 'bold', textAlign: 'center'}}>Chỉ Admin mới có quyền lưu đáp án.</div>
            )}"""
code = code.replace(chiettu_save_btn_old, chiettu_save_btn_new)


# 6. TongHopTab
code = code.replace("function TongHopTab() {", "function TongHopTab({ currentUser }) {")
code = code.replace("<TongHopTab />", "<TongHopTab currentUser={currentUser} />")
code = code.replace("body: JSON.stringify({", "body: JSON.stringify({\n          username: currentUser,")

# 7. LuyenTapTab
code = code.replace("function LuyenTapTab({ setPrimaryTab, setActiveTab, setGlobalLookupTerm }) {", "function LuyenTapTab({ setPrimaryTab, setActiveTab, setGlobalLookupTerm, currentUser }) {")
code = code.replace("<LuyenTapTab setPrimaryTab={setPrimaryTab} \nsetActiveTab={setActiveTab} setGlobalLookupTerm={setGlobalLookupTerm} />", "<LuyenTapTab setPrimaryTab={setPrimaryTab} setActiveTab={setActiveTab} setGlobalLookupTerm={setGlobalLookupTerm} currentUser={currentUser} />")
code = code.replace("body: JSON.stringify({\n          char: charObj['Chữ Trung Quốc'],", "body: JSON.stringify({\n          username: currentUser,\n          char: charObj['Chữ Trung Quốc'],")

# 8. TracNghiemTab
code = code.replace("function TracNghiemTab() {", "function TracNghiemTab({ currentUser }) {")
code = code.replace("<TracNghiemTab />", "<TracNghiemTab currentUser={currentUser} />")
code = code.replace("body: JSON.stringify({ char: currentChar['Chữ Trung Quốc'], comps: { srs: newSrs } })", "body: JSON.stringify({ username: currentUser, char: currentChar['Chữ Trung Quốc'], comps: { srs: newSrs } })")


with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Patch applied")
