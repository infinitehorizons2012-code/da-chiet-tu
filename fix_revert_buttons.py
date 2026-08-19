import re

with open("src/App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Inject before handleMoveAllToReady
move_regex = re.compile(r"const handleMoveAllToReady = async \(charObj\) => \{")

new_funcs = """const saveSrs = async (charObj, originalSrs, newSrs) => {
        try {
          const res = await fetch('/api/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              username: currentUser,
              char: charObj['Chữ Trung Quốc'],
              comps: { srs: newSrs }
            })
          });
          const data = await res.json();
          if (!data.success) {
            charObj.srs = originalSrs;
            setRenderTrigger(v => v + 1);
          }
        } catch (err) {
          charObj.srs = originalSrs;
          setRenderTrigger(v => v + 1);
        }
      };

      const handleRevertToBatDau = async (charObj) => {
        if (!window.confirm(`Bạn có chắc muốn đưa chữ "${charObj['Chữ Trung Quốc']}" về trạng thái Bắt đầu? Toàn bộ tiến độ trắc nghiệm của chữ này sẽ bị xóa bỏ!`)) return;
        const originalSrs = { ...charObj.srs };
        let newSrs = { ...charObj.srs };
        SKILLS.forEach(skill => {
           newSrs = buildNewSrs({srs: newSrs}, skill.id, 'bat_dau', 0);
        });
        charObj.srs = newSrs;
        setRenderTrigger(v => v + 1);
        await saveSrs(charObj, originalSrs, newSrs);
      };

      const handleRevertToSanSangThi = async (charObj) => {
        if (!window.confirm(`Bạn có chắc muốn đưa chữ "${charObj['Chữ Trung Quốc']}" về Sẵn sàng thi? Tiến độ Hạt mầm/Cây/Hoa của chữ này sẽ bị xóa bỏ!`)) return;
        const originalSrs = { ...charObj.srs };
        let newSrs = { ...charObj.srs };
        SKILLS.forEach(skill => {
           newSrs = buildNewSrs({srs: newSrs}, skill.id, 'san_sang_thi', 0);
        });
        charObj.srs = newSrs;
        setRenderTrigger(v => v + 1);
        await saveSrs(charObj, originalSrs, newSrs);
      };

      const handleMoveAllToReady = async (charObj) => {"""

if move_regex.search(content):
    content = move_regex.sub(new_funcs, content)
    print("Injected functions!")
else:
    print("Failed to find handleMoveAllToReady")

# Replace tonghop-actions inside LuyenTapTab
# Use regex to find it!
# Warning: tonghop-actions is used in BOTH LuyenTapTab and TongHopTab!
# We only want to replace it inside LuyenTapTab.
# LuyenTapTab's tonghop-actions has a button with onClick={() => handleStudy(item['Chữ Trung Quốc'])}
actions_regex = re.compile(r'<div className="tonghop-actions">\s*<button className="study-btn" onClick=\{\(\) => handleStudy\(item\[\'Chữ Trung Quốc\'\]\)\}>Học</button>\s*\{SKILLS\.some\(skill => getSrsStatus\(item, skill\.id\) === \'bat_dau\'\) && \(\s*<button className="ready-btn" onClick=\{\(\) => handleMoveAllToReady\(item\)\}>Sẵn sàng thi</button>\s*\)\}\s*</div>', re.DOTALL)

new_actions = """<div className="tonghop-actions" style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', justifyContent: 'flex-end' }}>
                        <button className="study-btn" onClick={() => handleStudy(item['Chữ Trung Quốc'])}>Học</button>
                        {SKILLS.some(skill => getSrsStatus(item, skill.id) === 'bat_dau') && (
                          <button className="ready-btn" onClick={() => handleMoveAllToReady(item)}>Sẵn sàng thi</button>
                        )}
                        {SKILLS.some(skill => getSrsStatus(item, skill.id) !== 'bat_dau') && (
                          <button onClick={() => handleRevertToBatDau(item)} style={{background: '#ef4444', color: 'white', border: 'none', padding: '8px 12px', borderRadius: '6px', cursor: 'pointer', fontSize: '0.85rem', fontWeight: '500'}}>🔙 Bắt đầu</button>
                        )}
                        {SKILLS.some(skill => ['hat_mam', 'cay', 'hoa'].includes(getSrsStatus(item, skill.id))) && (
                          <button onClick={() => handleRevertToSanSangThi(item)} style={{background: '#f59e0b', color: 'white', border: 'none', padding: '8px 12px', borderRadius: '6px', cursor: 'pointer', fontSize: '0.85rem', fontWeight: '500'}}>🔙 Sẵn sàng thi</button>
                        )}
                     </div>"""

if actions_regex.search(content):
    content = actions_regex.sub(new_actions, content)
    print("Injected buttons!")
else:
    print("Failed to find tonghop-actions")

with open("src/App.jsx", "w", encoding="utf-8") as f:
    f.write(content)

